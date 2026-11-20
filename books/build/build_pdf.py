#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按册排版 PDF。

用法：
    python books/build/build_pdf.py --book pro           # 排版一册
    python books/build/build_pdf.py --book intro --figures   # 先重绘插图再排版
    python books/build/build_pdf.py --book pro --no-opt  # PDF 超 20MB 也不压图
    python books/build/build_pdf.py                      # 列出可构建的册

每册的元数据读 books/<册名>/book.json，章节顺序读同目录的 structure.json。
依赖：Python 3.10+（markdown、pygments、pymupdf、websocket-client、pillow）、
      Node（渲染 KaTeX，首次运行自动下载到 books/build/vendor/）、Chrome 或 Edge。
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VENDOR = HERE / "vendor"
OUT_DIR = ROOT / "output"
TMP_ROOT = HERE / "out"
LIMIT_MB = 20.0

# 压图重排时，把正文里的原始插图映射到临时目录里的压缩副本。
# 键是原始图片的绝对路径，值是压缩后的绝对路径。
IMG_MAP: dict[str, str] = {}


class Book:
    """一册书的根目录、元数据与章节顺序。

    元数据全部来自 books/<册名>/book.json，章节顺序来自同目录的
    structure.json，构建脚本不再写死任何书名或章号。
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.root = ROOT / "books" / key
        meta_path = self.root / "book.json"
        struct_path = self.root / "structure.json"
        if not meta_path.exists() or not struct_path.exists():
            raise SystemExit(f"{self.root} 缺少 book.json 或 structure.json")
        self.meta = json.loads(meta_path.read_text(encoding="utf-8"))
        self.struct = json.loads(struct_path.read_text(encoding="utf-8"))

        self.title = self.meta["title"]
        self.edition = self.meta.get("edition", "")
        self.subtitle = self.meta.get("subtitle", "")
        self.series = self.meta.get("series", "")
        self.author = self.meta.get("author", "")
        self.version = self.meta.get("version", "")
        self.out_name = self.meta["pdf"]
        self.toc_sections = bool(self.meta.get("toc_sections", False))
        self.cover = self.meta.get("cover", "cover.jpg")
        self.backcover = self.meta.get("backcover", "backcover.jpg")
        self.blurb = self.meta.get("blurb", [])
        self.images = self.root / "images"
        self.chapters = self.root / "chapters"
        self.front_dir = self.root / "front"
        self.appendix_dir = self.root / "appendix"
        self.tmp = TMP_ROOT / key

    def __repr__(self) -> str:
        return f"<Book {self.key} {self.title}{self.edition}>"


# 当前构建的书，main() 里赋值
CFG: Book = None  # type: ignore[assignment]


def available_books() -> list[str]:
    out = []
    for p in sorted((ROOT / "books").iterdir()):
        if p.is_dir() and (p / "book.json").exists():
            out.append(p.name)
    return out

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
NODE_CANDIDATES = [
    "node",
    r"C:\Program Files\nodejs\node.exe",
    r"C:\Users\Administrator\AppData\Local\Temp\nodejs\node.exe",
    "/tmp/nodejs/node.exe",
]


# ------------------------------------------------------------------ 环境
def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("chrome") or shutil.which("msedge")
    if found:
        return found
    raise SystemExit("找不到 Chrome/Edge")


def find_node() -> str:
    for c in NODE_CANDIDATES:
        if c == "node":
            p = shutil.which("node")
            if p:
                return p
        elif Path(c).exists():
            return c
    raise SystemExit("找不到 Node")


def ensure_katex() -> Path:
    """确保本地有 KaTeX，缺失时下载一次。"""
    dist = VENDOR / "package" / "dist" / "katex.js"
    if dist.exists():
        return dist
    VENDOR.mkdir(parents=True, exist_ok=True)
    tgz = VENDOR / "katex.tgz"
    url = "https://registry.npmjs.org/katex/-/katex-0.16.11.tgz"
    print("[..] 下载 KaTeX")
    try:
        with urlopen(url, timeout=90) as r, open(tgz, "wb") as f:
            f.write(r.read())
        with tarfile.open(tgz) as tf:
            tf.extractall(VENDOR)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"KaTeX 下载失败，请手动放到 {VENDOR}：{exc}")
    return dist


# ------------------------------------------------------------------ Markdown
FENCE_RE = re.compile(r"^(`{3,})([^\n]*)\n(.*?)^\1[ \t]*$", re.S | re.M)
DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)([^\n$]+?)(?<!\\)\$")


def extract_code(text: str, store: list) -> str:
    def repl(m):
        lang = (m.group(2) or "").strip().split()[0] if (m.group(2) or "").strip() else ""
        store.append((lang, m.group(3).rstrip("\n")))
        return f"@@CODE{len(store)-1}@@"

    return FENCE_RE.sub(repl, text)


def extract_math(text: str, store: list) -> str:
    def disp(m):
        store.append((m.group(1).strip(), True))
        return f"@@MATH{len(store)-1}@@"

    def inl(m):
        store.append((m.group(1).strip(), False))
        return f"@@MATH{len(store)-1}@@"

    text = DISPLAY_MATH_RE.sub(disp, text)
    return INLINE_MATH_RE.sub(inl, text)


def render_math(items, node: str) -> list[str]:
    payload = json.dumps({"items": [{"tex": t, "display": d} for t, d in items]})
    proc = subprocess.run([node, str(HERE / "math_render.js")],
                          input=payload.encode("utf-8"),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.decode("utf-8", "ignore"))
    return json.loads(proc.stdout)["html"]


def highlight_code(lang: str, body: str) -> str:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import TextLexer, get_lexer_by_name

    try:
        lexer = get_lexer_by_name(lang) if lang else TextLexer()
    except Exception:
        lexer = TextLexer()
    code = highlight(body, lexer, HtmlFormatter(nowrap=True))
    return (f'<div class="codeblock"><div class="codeblock-lang">{html.escape(lang or "text")}</div>'
            f"<pre><code>{code}</code></pre></div>")


def slug(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text)
    t = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", t.strip())
    return t.strip("-")[:60] or "sec"


IMAGE_LINE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")


def convert(path: Path, node: str, drop_h1: bool = True) -> tuple[str, str]:
    import markdown

    raw = path.read_text(encoding="utf-8")
    title = ""
    if drop_h1:
        m = re.search(r"^#\s+(.+)$", raw, re.M)
        if m:
            title = m.group(1).strip()
            raw = raw[: m.start()] + raw[m.end():]

    codes: list = []
    maths: list = []
    text = extract_code(raw, codes)
    text = extract_math(text, maths)

    figs: list = []
    lines = []
    for line in text.split("\n"):
        mm = IMAGE_LINE_RE.match(line.strip())
        if mm:
            figs.append((mm.group(1).strip(), mm.group(2).strip()))
            lines.append(f"@@FIG{len(figs)-1}@@")
        else:
            lines.append(line)
    text = "\n".join(lines)

    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    body = md.convert(text)

    body = re.sub(r"<h([1-4])>(.*?)</h\1>",
                  lambda m: f'<h{m.group(1)} id="{slug(m.group(2))}">{m.group(2)}</h{m.group(1)}>',
                  body, flags=re.S)

    def code_repl(m):
        idx = int(re.match(r".*?(\d+)", m.group(0)).group(1))
        return highlight_code(*codes[idx])

    body = re.sub(r"<p>\s*@@CODE(\d+)@@\s*</p>|@@CODE(\d+)@@", code_repl, body)

    def fig_repl(m):
        idx = int(re.match(r".*?(\d+)", m.group(0)).group(1))
        cap, src = figs[idx]
        abs_src = (path.parent / src).resolve().as_posix()
        use_src = IMG_MAP.get(abs_src, abs_src)
        return (f'<figure class="book-figure"><img src="file:///{use_src}" '
                f'alt="{html.escape(cap)}"><figcaption>{cap}</figcaption></figure>')

    body = re.sub(r"<p>\s*@@FIG(\d+)@@\s*</p>|@@FIG(\d+)@@", fig_repl, body)

    rendered = render_math(maths, node)
    body = re.sub(r"@@MATH(\d+)@@", lambda m: rendered[int(m.group(1))], body)
    return title, body


# ------------------------------------------------------------------ 模板
CSS = r"""
@page { size: A4; margin: 20mm 18mm 18mm 18mm; }
@page:first { margin: 0; }
@page full { size: A4; margin: 0; }

html { font-size: 10.5pt; }
body {
  font-family: "Microsoft YaHei", "Noto Sans SC", sans-serif;
  color: #1a1a1a; line-height: 1.75; text-align: justify; margin: 0;
}
h1, h2, h3, h4 { font-family: "Microsoft YaHei", "Noto Sans SC", sans-serif;
  color: #111; line-height: 1.35; page-break-after: avoid; }

h1.part-title { font-size: 26pt; margin: 60mm 0 10mm; font-weight: 700; }
p.part-lead { font-size: 10.5pt; color: #333; text-indent: 2em; }
.chapter-title {
  font-size: 19pt; margin: 0 0 9mm; padding-bottom: 4mm;
  border-bottom: 1.1pt solid #222;
}
h2 { font-size: 13pt; margin: 8mm 0 3mm; }
h3 { font-size: 11.5pt; margin: 6mm 0 2mm; }
h4 { font-size: 10.5pt; margin: 5mm 0 2mm; color: #333; }

p { margin: 0 0 2.6mm; text-indent: 2em; }
li p, td p, blockquote p { text-indent: 0; }
ul, ol { margin: 0 0 2.6mm; padding-left: 6mm; }
li { margin-bottom: 1.2mm; }
strong { font-weight: 700; color: #000; }

code { font-family: "Cascadia Mono", Consolas, monospace; font-size: .9em;
  background: #f3f3f3; padding: .1em .3em; border-radius: 2px; }
.codeblock { margin: 3mm 0 3.5mm; border: .6pt solid #d8d8d8; border-radius: 3px;
  background: #fafafa; overflow: hidden; }
.codeblock-lang { font-size: 7.5pt; color: #777; background: #f0f0f0;
  padding: 1mm 2.5mm; border-bottom: .5pt solid #e2e2e2; }
.codeblock pre { margin: 0; padding: 2.5mm 3mm; white-space: pre-wrap; word-break: break-all; }
.codeblock code { font-family: "Cascadia Mono", Consolas, monospace; font-size: 8.2pt;
  line-height: 1.45; background: none; padding: 0; }

table { border-collapse: collapse; margin: 3mm auto 4mm; font-size: 9pt;
  max-width: 100%; page-break-inside: avoid; }
thead { background: #f2f2f2; }
th, td { border: .5pt solid #cfcfcf; padding: 1.4mm 2.2mm; text-align: left; vertical-align: top; }
th { font-weight: 600; }
tbody tr:nth-child(even) { background: #fafafa; }

blockquote { margin: 3mm 0; padding: 2mm 4mm; border-left: 2.2pt solid #bbb;
  background: #f7f7f7; color: #333; }

.book-figure { margin: 6mm 0 5mm; text-align: center; page-break-inside: avoid; }
.book-figure img { width: 100%; height: auto; }
.book-figure figcaption { font-size: 8.8pt; color: #444; margin-top: 2mm; text-indent: 0; }
.book-figure + p { text-align: center; text-indent: 0; font-size: 8.8pt;
  color: #444; margin: -3mm 0 4mm; }

hr { border: none; border-top: .6pt solid #ddd; margin: 6mm 0; }
.katex-display { margin: 3mm 0; overflow: hidden; page-break-inside: avoid;
  font-size: 0.9em; }
::-webkit-scrollbar { display: none; width: 0; height: 0; }

.page-break { page-break-before: always; }
.chmark { color: #fff; font-size: 4pt; line-height: 0; }

/* 封面与封底 */
.cover, .backcover {
  page: full;
  width: 100%; height: 100vh; position: relative; overflow: hidden;
  page-break-after: always; color: #fff;
}
.cover img.bg, .backcover img.bg {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
}
.veil { position: absolute; inset: 0; }
.cover .veil { background: linear-gradient(180deg, rgba(6,12,28,.93) 0%,
  rgba(6,12,28,.82) 20%, rgba(6,12,28,.44) 34%, rgba(6,12,28,.12) 62%,
  rgba(6,12,28,.88) 100%); }
.cover .inner { position: absolute; left: 22mm; right: 22mm; top: 34mm; }
.cover .kicker { font-size: 10pt; letter-spacing: 3pt; color: #cfe0ff; margin-bottom: 8mm; }
.cover .covertitle { font-size: 38pt; line-height: 1.22; margin: 0 0 7mm; color: #fff;
  font-weight: 700; text-shadow: 0 2px 18px rgba(0,0,0,.55); }
.cover .sub { font-size: 15pt; color: #eaf1ff; margin: 0;
  text-shadow: 0 2px 14px rgba(0,0,0,.6); }
.cover .foot { position: absolute; left: 22mm; right: 22mm; bottom: 24mm; }
.cover .author { font-size: 12pt; color: #eaf0ff; }
.cover .meta { font-size: 9pt; color: #9fb3d9; margin-top: 2mm; }

.backcover .veil { background: rgba(8,14,26,.55); }
.backcover .inner { position: absolute; left: 24mm; right: 24mm; top: 60mm; }
.backcover h2 { font-size: 15pt; color: #fff; border: none; margin: 0 0 8mm; }
.backcover p { color: #e6ecf7; text-indent: 2em; font-size: 10.5pt; }
.backcover .sig { margin-top: 18mm; text-align: right; color: #cfe0ff; text-indent: 0; }

/* 扉页与版权页 */
.titlepage { page-break-after: always; padding-top: 55mm; text-align: center; }
.titlepage h1 { font-size: 30pt; margin: 0 0 6mm; letter-spacing: 1pt; }
.titlepage .sub { font-size: 14pt; color: #444; margin: 0 0 30mm; }
.titlepage .edition { font-size: 10.5pt; color: #666; margin: 0 0 22mm;
  letter-spacing: .18em; }
.titlepage .author { font-size: 12pt; color: #222; }
.colophon { page-break-after: always; font-size: 9.5pt; color: #333; }
.colophon h2 { font-size: 13pt; border: none; margin-top: 0; }
.colophon p { text-indent: 0; margin-bottom: 2mm; }

/* 目录 */
.toc { page-break-before: always; page-break-after: always; }
.toc .toc-title { font-size: 20pt; border-bottom: 1pt solid #222; padding-bottom: 4mm; margin: 0 0 7mm; }
.toc-part { font-size: 9.5pt; font-weight: 700; margin: 4.5mm 0 1.5mm; color: #111; }
.toc-entry { display: flex; align-items: baseline; font-size: 10pt; margin: 0 0 1.5mm;
  padding-left: 6mm; }
.toc-entry.toc-sub { font-size: 9pt; padding-left: 12mm; color: #333; }
.toc-entry.toc-sub .p { color: #777; }
.toc-entry .dots { flex: 1 1 auto; border-bottom: .6pt dotted #bbb; margin: 0 2mm;
  transform: translateY(-1mm); }
.toc-entry .p { flex: 0 0 auto; color: #555; }
"""


def cover_html() -> str:
    img = (CFG.images / CFG.cover).as_posix()
    return f"""
<section class="cover">
  <img class="bg" src="file:///{img}" alt="">
  <div class="veil"></div>
  <div class="inner">
    <div class="kicker">{CFG.series} · {CFG.edition}</div>
    <div class="covertitle">{CFG.title}</div>
    <p class="sub">{CFG.subtitle}</p>
  </div>
  <div class="foot">
    <div class="author">{CFG.author}</div>
    <div class="meta">{CFG.version}</div>
  </div>
</section>
"""


def backcover_html(marks: bool = True) -> str:
    img = (CFG.images / CFG.backcover).as_posix()
    mark_end = '<span class="chmark">CHMARKEND</span>' if marks else ""
    paras = "".join(f"<p>{html.escape(t)}</p>" for t in CFG.blurb)
    return f"""
<section class="backcover">{mark_end}
  <img class="bg" src="file:///{img}" alt="">
  <div class="veil"></div>
  <div class="inner">
    <h2>关于这本书</h2>
    {paras}
    <p class="sig">{CFG.author}</p>
  </div>
</section>
"""


def titlepage_html() -> str:
    return f"""
<section class="titlepage">
  <h1>{CFG.title}</h1>
  <p class="sub">{CFG.subtitle}</p>
  <p class="edition">{CFG.edition}</p>
  <p class="author">{CFG.author}</p>
</section>
"""


def toc_html(entries, page_map) -> str:
    rows = []
    for kind, text, key in entries:
        if kind == "part":
            rows.append(f'<div class="toc-part">{html.escape(text)}</div>')
        elif kind == "section":
            page = str(page_map.get(key, "")) if page_map else ""
            rows.append(f'<div class="toc-entry toc-sub"><span>{html.escape(text)}</span>'
                        f'<span class="dots"></span><span class="p">{page}</span></div>')
        else:
            page = str(page_map.get(key, "")) if page_map else ""
            rows.append(f'<div class="toc-entry"><span>{html.escape(text)}</span>'
                        f'<span class="dots"></span><span class="p">{page}</span></div>')
    return f'<section class="toc"><h1 class="toc-title">目录</h1>{"".join(rows)}</section>'


# ------------------------------------------------------------------ 组装
def assemble(parts_html, front_html, toc, marks=True, back_html="") -> str:
    if not marks:
        back_html = re.sub(r'<span class="chmark">.*?</span>', "", back_html)
    katex_css = (VENDOR / "package" / "dist" / "katex.min.css").read_text(encoding="utf-8")
    chunks = [cover_html(), front_html, toc]
    for kind, payload in parts_html:
        if kind == "part":
            title, body = payload
            chunks.append(f'<section class="page-break"><h1 class="part-title">{html.escape(title)}</h1>{body}</section>')
        else:
            key, title, body = payload
            mark = f'<span class="chmark">CHMARK{key}</span>' if marks else ""
            chunks.append(f'<section class="chapter page-break" id="{key}">{mark}'
                          f'<h1 class="chapter-title">{html.escape(title)}</h1>{body}</section>')
    chunks.append(back_html)
    chunks.append(backcover_html(marks))
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{CFG.title}（{CFG.edition}）</title><style>{katex_css}</style><style>{CSS}</style></head>
<body>{''.join(chunks)}</body></html>"""


# ------------------------------------------------------------------ 打印
def free_port() -> int:
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


def wait_devtools(port: int, timeout: float = 25.0) -> str:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1) as r:
                return json.loads(r.read())["webSocketDebuggerUrl"]
        except Exception:
            time.sleep(0.3)
    raise SystemExit("DevTools 未就绪")


class CDP:
    def __init__(self, url: str):
        import websocket
        self.ws = websocket.create_connection(url, timeout=180)
        self.mid = 0

    def send(self, method, params=None, session=None):
        self.mid += 1
        msg = {"id": self.mid, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self.ws.send(json.dumps(msg))
        while True:
            data = json.loads(self.ws.recv())
            if data.get("id") == self.mid:
                if "error" in data:
                    raise RuntimeError(data["error"])
                return data.get("result", {})


def print_pdf(html_path: Path, pdf_path: Path, chrome: str, outline: bool = True) -> None:
    port = free_port()
    profile = tempfile.mkdtemp(prefix="cdp-")
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
         "--disable-extensions", "--font-render-hinting=none",
         f"--remote-debugging-port={port}", "--remote-allow-origins=*",
         f"--user-data-dir={profile}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        cdp = CDP(wait_devtools(port))
        tid = cdp.send("Target.createTarget", {"url": "about:blank"})["targetId"]
        sid = cdp.send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
        cdp.send("Page.enable", {}, sid)
        cdp.send("Emulation.setEmulatedMedia", {"media": "print"}, sid)
        cdp.send("Page.navigate", {"url": "file:///" + html_path.as_posix().lstrip("/")}, sid)
        time.sleep(1.2)
        cdp.send("Runtime.evaluate", {"expression":
                 "document.fonts.ready.then(()=>Promise.all([...document.images].map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r}))))",
                 "awaitPromise": True}, sid)
        params = {
            "printBackground": True,
            "paperWidth": 8.27, "paperHeight": 11.69,
            "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,
            "displayHeaderFooter": False,
            "preferCSSPageSize": True,
            "scale": 1,
            "transferMode": "ReturnAsBase64",
        }
        if outline:
            params["generateDocumentOutline"] = True
        res = cdp.send("Page.printToPDF", params, sid)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(base64.b64decode(res["data"]))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)


# ------------------------------------------------------------------ 页码
def locate(pdf_path: Path, keys: list[str]) -> dict[str, int]:
    import pymupdf

    doc = pymupdf.open(str(pdf_path))
    texts = [p.get_text().replace(" ", "").replace("\n", "") for p in doc]
    out, cursor = {}, 0
    for key in keys:
        needle = f"CHMARK{key}"
        for i in range(cursor, len(texts)):
            if needle in texts[i]:
                out[key] = i + 1
                cursor = i
                break
    doc.close()
    return out


def stamp(pdf_path: Path, page_map: dict[str, int], chapter_titles: dict[str, str]) -> None:
    import pymupdf

    doc = pymupdf.open(str(pdf_path))
    back_start = page_map.get("BACK", 10**9)
    end_start = page_map.get("END", 10**9)
    # 按页码排，不能直接 sorted(dict.items())：那样按 key 的字母序，
    # 有附录时 appA.md 会排到 ch01.md 前面，页眉就会一直停在第一篇之前
    starts = sorted(((k, v) for k, v in page_map.items() if k not in ("BACK", "END")),
                    key=lambda kv: kv[1])
    body_pages = [v for k, v in page_map.items() if k not in ("PRE", "BACK", "END")]
    first_body = min(body_pages) if body_pages else 1
    font = r"C:\Windows\Fonts\simhei.ttf"
    grey = (0.55, 0.55, 0.55)
    grey2 = (0.45, 0.45, 0.45)
    for idx in range(doc.page_count):
        pno = idx + 1
        if pno < first_body or pno >= end_start:
            continue
        page = doc[idx]
        w, h = page.rect.width, page.rect.height
        cur, cur_key = "", None
        if pno >= back_start:
            cur, cur_key = "后记", "BACK"
        else:
            for key, sp in starts:
                if sp <= pno:
                    cur, cur_key = chapter_titles.get(key, ""), key
                else:
                    break
        is_start = cur_key in page_map and page_map[cur_key] == pno
        if not is_start and cur:
            short = cur if len(cur) <= 24 else cur[:23] + "…"
            try:
                page.insert_text((51, 30), CFG.title, fontsize=7.5, fontfile=font,
                                 fontname="hei", color=grey)
                page.insert_textbox(pymupdf.Rect(w - 51 - 250, 21, w - 51, 34), short,
                                    fontsize=7, fontfile=font, fontname="hei",
                                    color=grey, align=2)
            except Exception as exc:  # noqa: BLE001
                print(f"[!!] 页眉写入失败 p{pno}: {exc}")
        try:
            page.insert_textbox(pymupdf.Rect(51, h - 30, w - 51, h - 16), str(pno),
                                fontsize=8.5, fontfile=font, fontname="hei",
                                color=grey2, align=1)
        except Exception as exc:  # noqa: BLE001
            print(f"[!!] 页码写入失败 p{pno}: {exc}")
    doc.saveIncr()
    doc.close()


# ------------------------------------------------------------------ 主流程
# ------------------------------------------------------------------ 压图

def make_compressed_images(cfg: Book, quality: int, max_width: int | None = None) -> int:
    """把插图转成压缩 JPEG 写到临时目录，并登记到 IMG_MAP。返回总字节数。"""
    from PIL import Image

    IMG_MAP.clear()
    dst_dir = cfg.tmp / f"img-q{quality}"
    total = 0
    for src in sorted(cfg.images.rglob("*.png")):
        im = Image.open(src).convert("RGB")
        if max_width and im.width > max_width:
            h = int(im.height * max_width / im.width)
            im = im.resize((max_width, h), Image.LANCZOS)
        dst = dst_dir / (src.relative_to(cfg.images).as_posix().replace("/", "_") + ".jpg")
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
        total += dst.stat().st_size
        IMG_MAP[src.as_posix()] = dst.as_posix()
    return total


# ------------------------------------------------------------------ 组装与排版

def collect(cfg: Book, node: str):
    """读取 structure.json，返回目录条目、正文块与前后辅文。"""
    entries: list[tuple[str, str, str]] = []
    chunks: list[tuple[str, tuple]] = []
    titles: dict[str, str] = {}

    def md_title(path: Path) -> str:
        raw = path.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", raw, re.M)
        if not m:
            raise SystemExit(f"{path} 缺少一级标题")
        return m.group(1).strip()

    if (cfg.front_dir / "preface.md").exists():
        entries.append(("chapter", "前言", "PRE"))
        titles["PRE"] = "前言"

    for part in cfg.struct["parts"]:
        part_path = cfg.front_dir / part["file"]
        part_title = md_title(part_path)
        entries.append(("part", part_title, part["file"]))
        _, pbody = convert(part_path, node, drop_h1=True)
        chunks.append(("part", (part_title, pbody)))

        for ch in part["chapters"]:
            ch_path = cfg.chapters / ch
            raw = ch_path.read_text(encoding="utf-8")
            title = md_title(ch_path)
            titles[ch] = title
            _, body = convert(ch_path, node, drop_h1=True)

            if cfg.toc_sections:
                secs = re.findall(r"^##\s+(.+)$", raw, re.M)
                counter = {"i": 0}

                def mark(m, ch=ch, counter=counter):
                    i = counter["i"]
                    counter["i"] += 1
                    return f'<span class="chmark">CHMARK{ch}@S{i}</span>' + m.group(0)

                body = re.sub(r'<h2 id="[^"]*">', mark, body)
                for i in range(counter["i"]):
                    if i < len(secs):
                        entries.append(("section", secs[i], f"{ch}@S{i}"))

            chunks.append(("chapter", (ch, title, body)))
            entries.append(("chapter", title, ch))
            print("[ok]", ch)

    appendix = cfg.struct.get("appendix")
    if appendix:
        app_title = appendix.get("title", "附录")
        entries.append(("part", app_title, "appendix"))
        chunks.append(("part", (app_title, "")))
        for ch in appendix["chapters"]:
            ch_path = cfg.appendix_dir / ch
            title = md_title(ch_path)
            titles[ch] = title
            _, body = convert(ch_path, node, drop_h1=True)
            chunks.append(("chapter", (ch, title, body)))
            entries.append(("chapter", title, ch))
            print("[ok]", ch)

    if cfg.struct.get("back"):
        entries.append(("chapter", "后记", "BACK"))
        titles["BACK"] = "后记"

    front_parts = [titlepage_html()]
    for f in cfg.struct["front"][1:]:
        _, body = convert(cfg.front_dir / f, node, drop_h1=True)
        cls = "colophon" if f == "copyright.md" else ""
        mk = '<span class="chmark">CHMARKPRE</span>' if f == "preface.md" else ""
        front_parts.append(f'<section class="{cls} page-break">{mk}{body}</section>')

    back_body = ""
    for f in cfg.struct.get("back", []):
        _, body = convert(cfg.front_dir / f, node, drop_h1=True)
        back_body += '<section class="page-break"><span class="chmark">CHMARKBACK</span>' + body + "</section>"

    return entries, chunks, "".join(front_parts), back_body, titles


def compile_book(cfg: Book, entries, chunks, front_html, back_body, out: Path) -> dict[str, int]:
    """两趟排版：第一趟定位页码，第二趟写入带页码的目录。"""
    cfg.tmp.mkdir(parents=True, exist_ok=True)
    html_path = cfg.tmp / f"{cfg.key}.html"
    pdf_tmp = cfg.tmp / "_pass1.pdf"

    html_path.write_text(
        assemble(chunks, front_html, toc_html(entries, None), back_html=back_body),
        encoding="utf-8")
    print("[..] pass 1")
    print_pdf(html_path, pdf_tmp, find_chrome())

    keys = [k for kind, _, k in entries if kind in ("chapter", "section")] + ["END"]
    page_map = locate(pdf_tmp, keys)
    html_path.write_text(
        assemble(chunks, front_html, toc_html(entries, page_map), marks=False, back_html=back_body),
        encoding="utf-8")

    print("[..] pass 2")
    print_pdf(html_path, out, find_chrome())
    pdf_tmp.unlink(missing_ok=True)
    return page_map


def finalize(cfg: Book, out: Path, page_map: dict, titles: dict) -> tuple[int, int, float]:
    """盖页眉页码，写入 PDF 元数据并做一次无痕压缩。"""
    stamp(out, page_map, titles)

    import pymupdf

    doc = pymupdf.open(str(out))
    doc.set_metadata({
        "title": f"{cfg.title}（{cfg.edition}）",
        "author": cfg.author,
        "subject": cfg.subtitle,
        "keywords": f"{cfg.title}, {cfg.subtitle}, SSM, Mamba",
        "creator": "books/build/build_pdf.py",
        "producer": cfg.author,
    })
    tmp2 = out.with_suffix(".tmp.pdf")
    doc.save(str(tmp2), garbage=4, deflate=True, clean=True)
    pages = doc.page_count
    marks = len(doc.get_toc())
    doc.close()
    tmp2.replace(out)
    mb = out.stat().st_size / 1024 / 1024
    return pages, marks, mb


# ------------------------------------------------------------------ 主流程

def main() -> None:
    global CFG

    ap = argparse.ArgumentParser(description="按 books/<册名>/book.json 排版一册书")
    ap.add_argument("--book", default=None, help="册名（books 下的目录名），默认先列清单")
    ap.add_argument("--figures", action="store_true", help="先重绘插图与封面")
    ap.add_argument("--html", action="store_true", help="只生成 HTML，不排版 PDF")
    ap.add_argument("--no-opt", action="store_true", help="PDF 超限也不压图")
    ap.add_argument("--out", default=None, help="自定义输出路径")
    args = ap.parse_args()

    books = available_books()
    if not args.book:
        print("可构建的册：", " ".join(books))
        return
    if args.book not in books:
        raise SystemExit(f"没有这一册：{args.book}（可选：{' '.join(books)}）")

    cfg = Book(args.book)
    CFG = cfg
    print(f"[..] 构建《{cfg.title}》{cfg.edition}")

    if args.figures:
        import runpy
        print("[..] 重绘插图")
        runpy.run_path(str(cfg.root / "code" / "make_all.py"), run_name="__main__")
        runpy.run_path(str(cfg.root / "code" / "make_covers.py"), run_name="__main__")

    ensure_katex()
    node = find_node()
    entries, chunks, front_html, back_body, titles = collect(cfg, node)

    if args.html:
        cfg.tmp.mkdir(parents=True, exist_ok=True)
        (cfg.tmp / f"{cfg.key}.html").write_text(
            assemble(chunks, front_html, toc_html(entries, None), back_html=back_body),
            encoding="utf-8")
        print("[ok] html ->", cfg.tmp / f"{cfg.key}.html")
        return

    out = Path(args.out) if args.out else (OUT_DIR / cfg.out_name)
    out.parent.mkdir(parents=True, exist_ok=True)

    attempts = [(None, None)] if args.no_opt else [(None, None), (88, 1700), (80, 1500), (70, 1300)]
    pages = marks = 0
    mb = 0.0
    for quality, width in attempts:
        IMG_MAP.clear()
        if quality:
            total = make_compressed_images(cfg, quality, width)
            print(f"[..] 压图 q={quality} 宽≤{width}px，共 {total/1024/1024:.1f} MB")
        page_map = compile_book(cfg, entries, chunks, front_html, back_body, out)
        pages, marks, mb = finalize(cfg, out, page_map, titles)
        if mb <= LIMIT_MB:
            break
        print(f"[!!] {mb:.1f} MB 超过 {LIMIT_MB:.0f} MB，继续压图")

    print(f"[done] {out}  {pages} 页  {mb:.1f} MB  书签 {marks} 条")
    print(f"       中间产物：{cfg.tmp}")

    manifest = TMP_ROOT / "manifest.json"
    data = {}
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data[cfg.key] = {
        "title": cfg.title,
        "edition": cfg.edition,
        "pdf": out.name,
        "pages": pages,
        "mb": round(mb, 2),
        "bookmarks": marks,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
