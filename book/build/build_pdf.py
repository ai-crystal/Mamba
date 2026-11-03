#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建《从 LSSL 到 Mamba-3》PDF。

用法：
    python book/build/build_pdf.py              # 排版并输出 output/*.pdf
    python book/build/build_pdf.py --figures    # 先重绘插图与封面
    python book/build/build_pdf.py --html       # 只生成 HTML，便于调试

依赖：Python 3.10+（markdown、pygments、pymupdf、websocket-client）、
      Node（渲染 KaTeX，首次运行会自动下载到 book/build/vendor/）、
      Chrome 或 Edge（无头打印）。
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

BOOK = Path(__file__).resolve().parent.parent
ROOT = BOOK.parent
BUILD = BOOK / "build"
OUT_DIR = ROOT / "output"
VENDOR = BUILD / "vendor"

TITLE = "从 LSSL 到 Mamba-3"
SUBTITLE = "状态空间模型笔记"
AUTHOR = "Dr. Dezeming"
VERSION = "2026 年 11 月"

# 篇 -> 章
PARTS = [
    ("part1.md", "第一篇　背景：序列模型的三难与连续时间系统",
     ["ch01.md", "ch02.md", "ch03.md"]),
    ("part2.md", "第二篇　记忆：HiPPO",
     ["ch04.md", "ch05.md", "ch06.md"]),
    ("part3.md", "第三篇　LSSL：一个统一的序列层",
     ["ch07.md", "ch08.md", "ch09.md"]),
    ("part4.md", "第四篇　S4：让状态空间可计算",
     ["ch10.md", "ch11.md", "ch12.md", "ch13.md", "ch14.md"]),
    ("part5.md", "第五篇　S5 及其时代",
     ["ch15.md", "ch16.md"]),
    ("part6.md", "第六篇　Mamba：选择性",
     ["ch17.md", "ch18.md", "ch19.md", "ch20.md", "ch21.md"]),
    ("part7.md", "第七篇　Mamba-2：状态空间对偶",
     ["ch22.md", "ch23.md", "ch24.md", "ch25.md", "ch26.md", "ch27.md"]),
    ("part8.md", "第八篇　Mamba-3：推理优先",
     ["ch28.md", "ch29.md", "ch30.md", "ch31.md", "ch32.md"]),
    ("part9.md", "第九篇　实践与收尾",
     ["ch33.md", "ch34.md", "ch35.md"]),
]
APPENDIX = ("appendix.md", "附录", ["appA.md", "appB.md", "appC.md"])
FRONT = ["title.md", "copyright.md", "preface.md"]
BACK = ["afterword.md"]

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
    proc = subprocess.run([node, str(BUILD / "math_render.js")],
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
        return (f'<figure class="book-figure"><img src="file:///{abs_src}" '
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
h2.chapter-title {
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
.cover .veil { background: linear-gradient(180deg, rgba(6,12,28,.78) 0%,
  rgba(6,12,28,.15) 38%, rgba(6,12,28,.10) 62%, rgba(6,12,28,.86) 100%); }
.cover .inner { position: absolute; left: 22mm; right: 22mm; top: 34mm; }
.cover .kicker { font-size: 10pt; letter-spacing: 3pt; color: #cfe0ff; margin-bottom: 8mm; }
.cover h1 { font-size: 38pt; line-height: 1.22; margin: 0 0 7mm; color: #fff; }
.cover .sub { font-size: 15pt; color: #dbe6ff; margin: 0; }
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
.titlepage .author { font-size: 12pt; color: #222; }
.colophon { page-break-after: always; font-size: 9.5pt; color: #333; }
.colophon h2 { font-size: 13pt; border: none; margin-top: 0; }
.colophon p { text-indent: 0; margin-bottom: 2mm; }

/* 目录 */
.toc { page-break-before: always; page-break-after: always; }
.toc h2 { font-size: 20pt; border-bottom: 1pt solid #222; padding-bottom: 4mm; margin: 0 0 7mm; }
.toc-part { font-size: 9.5pt; font-weight: 700; margin: 4.5mm 0 1.5mm; color: #111; }
.toc-entry { display: flex; align-items: baseline; font-size: 10pt; margin: 0 0 1.5mm;
  padding-left: 6mm; }
.toc-entry .dots { flex: 1 1 auto; border-bottom: .6pt dotted #bbb; margin: 0 2mm;
  transform: translateY(-1mm); }
.toc-entry .p { flex: 0 0 auto; color: #555; }
"""


def cover_html() -> str:
    img = (BOOK / "images" / "cover.jpg").as_posix()
    return f"""
<section class="cover">
  <img class="bg" src="file:///{img}" alt="">
  <div class="veil"></div>
  <div class="inner">
    <div class="kicker">STATE SPACE MODELS</div>
    <h1>{TITLE}</h1>
    <p class="sub">{SUBTITLE}：从 HiPPO 到 Mamba-3</p>
  </div>
  <div class="foot">
    <div class="author">{AUTHOR}</div>
    <div class="meta">{VERSION}</div>
  </div>
</section>
"""


def backcover_html(marks: bool = True) -> str:
    img = (BOOK / "images" / "backcover.jpg").as_posix()
    mark_end = '<span class="chmark">CHMARKEND</span>' if marks else ""
    return f"""
<section class="backcover">{mark_end}
  <img class="bg" src="file:///{img}" alt="">
  <div class="veil"></div>
  <div class="inner">
    <h2>关于这本书</h2>
    <p>从 2020 年的 HiPPO 到 2026 年的 Mamba-3，这条线索试图回答同一个问题：怎样用固定大小的状态压缩任意长的历史，同时保持线性的训练成本。</p>
    <p>书里逐个拆解七个模型的动机、推导与取舍。每一次进步都不是发明了新东西，而是把旧问题换了一个问法，再借来另一个领域已有的工具。</p>
    <p class="sig">{AUTHOR}</p>
  </div>
</section>
"""


def titlepage_html() -> str:
    return f"""
<section class="titlepage">
  <h1>{TITLE}</h1>
  <p class="sub">{SUBTITLE}</p>
  <p class="author">{AUTHOR}</p>
</section>
"""


def toc_html(entries, page_map) -> str:
    rows = []
    for kind, text, key in entries:
        if kind == "part":
            rows.append(f'<div class="toc-part">{html.escape(text)}</div>')
        else:
            page = str(page_map.get(key, "")) if page_map else ""
            rows.append(f'<div class="toc-entry"><span>{html.escape(text)}</span>'
                        f'<span class="dots"></span><span class="p">{page}</span></div>')
    return f'<section class="toc"><h2>目录</h2>{"".join(rows)}</section>'


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
                          f'<h2 class="chapter-title">{html.escape(title)}</h2>{body}</section>')
    chunks.append(back_html)
    chunks.append(backcover_html(marks))
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{TITLE}</title><style>{katex_css}</style><style>{CSS}</style></head>
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
    starts = sorted((k, v) for k, v in page_map.items() if k not in ("BACK", "END"))
    first_body = starts[0][1] if starts else 1
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
        try:
            if not is_start and cur:
                short = cur if len(cur) <= 24 else cur[:23] + "…"
                page.insert_text((51, 30), TITLE, fontsize=7.5, fontfile=font,
                                 fontname="hei", color=grey)
                page.insert_textbox(pymupdf.Rect(w - 51 - 250, 21, w - 51, 34), short,
                                    fontsize=7, fontfile=font, fontname="hei",
                                    color=grey, align=2)
            page.insert_textbox(pymupdf.Rect(51, h - 30, w - 51, h - 16), str(pno),
                                fontsize=8.5, fontfile=font, fontname="hei",
                                color=grey2, align=1)
        except Exception:
            pass
    doc.saveIncr()
    doc.close()


# ------------------------------------------------------------------ 主流程
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--out", default=str(OUT_DIR / "from-lssl-to-mamba3.pdf"))
    args = ap.parse_args()

    if args.figures:
        import runpy
        print("[..] 重绘插图")
        runpy.run_path(str(BOOK / "code" / "make_all.py"), run_name="__main__")
        runpy.run_path(str(BOOK / "code" / "make_covers.py"), run_name="__main__")

    ensure_katex()
    node = find_node()

    # 目录条目
    entries = []
    for part_file, part_title, chapters in PARTS:
        entries.append(("part", part_title, part_file))
        for ch in chapters:
            raw = (BOOK / "chapters" / ch).read_text(encoding="utf-8")
            t = re.search(r"^#\s+(.+)$", raw, re.M).group(1).strip()
            entries.append(("chapter", t, ch))

    # 正文
    chunks = []
    for part_file, part_title, chapters in PARTS:
        _, pbody = convert(BOOK / "front" / part_file, node, drop_h1=True)
        chunks.append(("part", (part_title, pbody)))
        for ch in chapters:
            raw = (BOOK / "chapters" / ch).read_text(encoding="utf-8")
            title = re.search(r"^#\s+(.+)$", raw, re.M).group(1).strip()
            _, body = convert(BOOK / "chapters" / ch, node, drop_h1=True)
            chunks.append(("chapter", (ch, title, body)))
            print("[ok]", ch)

    # 附录
    app_file, app_title, app_chaps = APPENDIX
    entries.append(("part", app_title, app_file))
    chunks.append(("part", (app_title, "")))
    for ch in app_chaps:
        raw = (BOOK / "appendix" / ch).read_text(encoding="utf-8")
        title = re.search(r"^#\s+(.+)$", raw, re.M).group(1).strip()
        _, body = convert(BOOK / "appendix" / ch, node, drop_h1=True)
        chunks.append(("chapter", (ch, title, body)))
        entries.append(("chapter", title, ch))
        print("[ok]", ch)

    # 前辅文
    front_parts = [titlepage_html()]
    for f in FRONT[1:]:
        _, body = convert(BOOK / "front" / f, node, drop_h1=True)
        cls = "colophon" if f == "copyright.md" else ""
        front_parts.append(f'<section class="{cls} page-break">{body}</section>')
    front_html = "".join(front_parts)

    # 后辅文
    back_body = ""
    for f in BACK:
        _, body = convert(BOOK / "front" / f, node, drop_h1=True)
        mk = '<span class="chmark">CHMARKBACK</span>'
        back_body += ("<section class=\"page-break\">" + mk + body + "</section>")

    html_doc = assemble(chunks, front_html, toc_html(entries, None), back_html=back_body)
    html_path = BUILD / "out" / "book.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_doc, encoding="utf-8")
    print("[ok] html")

    if args.html:
        return

    tmp = BUILD / "out" / "_pass1.pdf"
    print("[..] pass 1")
    print_pdf(html_path, tmp, find_chrome())

    keys = [k for kind, _, k in entries if kind == "chapter"] + ["BACK", "END"]
    page_map = locate(tmp, keys)
    html_doc = assemble(chunks, front_html, toc_html(entries, page_map), marks=False, back_html=back_body)
    html_path.write_text(html_doc, encoding="utf-8")

    print("[..] pass 2")
    out = Path(args.out)
    print_pdf(html_path, out, find_chrome())
    tmp.unlink(missing_ok=True)

    titles = {}
    for kind, payload in chunks:
        if kind == "chapter":
            titles[payload[0]] = payload[1]
    titles["BACK"] = "后记"
    stamp(out, page_map, titles)

    import pymupdf

    # 压缩：重写内容流，去掉冗余对象
    tmp2 = out.with_suffix(".tmp.pdf")
    doc = pymupdf.open(str(out))
    doc.save(str(tmp2), garbage=4, deflate=True, clean=True)
    doc.close()
    tmp2.replace(out)

    doc = pymupdf.open(str(out))
    mb = out.stat().st_size / 1024 / 1024
    print(f"[done] {out}  {doc.page_count} 页  {mb:.1f} MB")
    toc = doc.get_toc()
    print(f"       书签 {len(toc)} 条")
    doc.close()


if __name__ == "__main__":
    main()
