#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付前体检。

用法：
    python books/build/check.py            # 体检全部册
    python books/build/check.py intro      # 只体检一册

检查项：册配置、章节顺序、标题字符、代码围栏、插图引用与章号、跨册引用、
站内链接、PDF 体积与页数。任何一项出错都会返回非零退出码，构建脚本据此中断。
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BOOKS_DIR = ROOT / "books"
OUT_DIR = ROOT / "output"
LIMIT_MB = 20.0

# 会直接搞坏排版或公式渲染的字符：报错
BAD_HEADING_CHARS = set("\\$<>{}")
# 只是好看不好看、可能影响锚点的字符：提醒
SOFT_HEADING_CHARS = set("^_%&|#*[]`~")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FIG_NAME_RE = re.compile(r"^fig(\d{2})-(\d{2})-[a-z0-9-]+\.png$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warns: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    def show(self, title: str) -> None:
        print(f"\n== {title}")
        for m in self.warns:
            print("  [warn]", m)
        for m in self.errors:
            print("  [ERR ]", m)


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def md_files(book_dir: Path) -> list[Path]:
    return sorted(p for p in book_dir.rglob("*.md") if p.is_file())


def iter_lines_outside_fence(path: Path):
    """逐行产出 (行号, 文本, 是否在代码块内, 围栏信息)。"""
    fence = None
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^\s*(`{3,})", line)
        if m:
            ticks = m.group(1)
            if fence is None:
                fence = ticks
                yield i, line, True, (ticks, "open")
                continue
            if len(ticks) >= len(fence) and not line.strip()[len(ticks):].strip():
                fence = None
                yield i, line, True, (ticks, "close")
                continue
        yield i, line, fence is not None, (fence, "body")


def check_config(rep: Report, name: str) -> tuple[dict, dict] | None:
    book_dir = BOOKS_DIR / name
    meta_path = book_dir / "book.json"
    struct_path = book_dir / "structure.json"
    if not meta_path.exists() or not struct_path.exists():
        rep.err(f"{name}: 缺少 book.json 或 structure.json")
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        struct = json.loads(struct_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        rep.err(f"{name}: 配置文件不是合法 JSON（{exc}）")
        return None

    for key in ("title", "pdf", "author"):
        if not meta.get(key):
            rep.err(f"{name}: book.json 缺少字段 {key}")
    pdf = str(meta.get("pdf", ""))
    if "/" in pdf or "\\" in pdf:
        rep.err(f"{name}: pdf 只能写文件名，不要带目录（{pdf}）")
    if not pdf.endswith(".pdf"):
        rep.err(f"{name}: pdf 字段必须以 .pdf 结尾（{pdf}）")
    for key in ("cover", "backcover"):
        img = meta.get(key)
        if img and not (book_dir / "images" / img).exists():
            rep.err(f"{name}: book.json 里的 {key} 不存在（images/{img}）")

    for req in ("front", "parts"):
        if req not in struct:
            rep.err(f"{name}: structure.json 缺少 {req}")
    return meta, struct


def check_structure(rep: Report, name: str, struct: dict) -> list[str]:
    book_dir = BOOKS_DIR / name
    listed: list[str] = []

    front = struct.get("front", [])
    if not front:
        rep.err(f"{name}: structure.json 的 front 为空")
    for f in front:
        if not (book_dir / "front" / f).exists():
            rep.err(f"{name}: 前辅文不存在 front/{f}")

    for part in struct.get("parts", []):
        pf = part.get("file", "")
        if not pf:
            rep.err(f"{name}: parts 里有一项缺少 file")
            continue
        if not (book_dir / "front" / pf).exists():
            rep.err(f"{name}: 篇首文件不存在 front/{pf}")
        if not part.get("chapters"):
            rep.err(f"{name}: {pf} 没有列出章节")
        for ch in part.get("chapters", []):
            if not (book_dir / "chapters" / ch).exists():
                rep.err(f"{name}: 章节不存在 chapters/{ch}")
            listed.append(ch)

    appendix = struct.get("appendix")
    if appendix:
        for ch in appendix.get("chapters", []):
            if not (book_dir / "appendix" / ch).exists():
                rep.err(f"{name}: 附录不存在 appendix/{ch}")
            listed.append(ch)

    for f in struct.get("back", []):
        if not (book_dir / "front" / f).exists():
            rep.err(f"{name}: 后辅文不存在 front/{f}")

    dup = {c for c in listed if listed.count(c) > 1}
    for c in sorted(dup):
        rep.err(f"{name}: {c} 在 structure.json 里出现了多次")

    on_disk = {p.name for p in (book_dir / "chapters").glob("*.md")}
    missing = on_disk - set(listed) - set(struct.get("_ignore", []))
    for c in sorted(missing):
        rep.err(f"{name}: chapters/{c} 没有写进 structure.json（不会被排版，也不会被站点收录）")

    # 站点侧栏与章节顺序的一致性
    sidebar = book_dir / "_sidebar.md"
    if not sidebar.exists():
        rep.err(f"{name}: 缺少 books/{name}/_sidebar.md")
    else:
        text = sidebar.read_text(encoding="utf-8")
        for c in sorted(on_disk):
            if f"chapters/{c}" not in text:
                rep.warn(f"{name}: _sidebar.md 里没有 chapters/{c}")
    return listed


def check_headings(rep: Report, name: str, path: Path) -> None:
    h1 = 0
    for no, line, in_fence, _ in iter_lines_outside_fence(path):
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if not m:
            continue
        level, text = len(m.group(1)), m.group(2)
        if level == 1:
            h1 += 1
        bad = sorted({c for c in text if c in BAD_HEADING_CHARS})
        if bad:
            rep.err(f"{rel(path)}:{no} 标题含会破坏排版的字符 {' '.join(bad)}（{text}）")
        soft = sorted({c for c in text if c in SOFT_HEADING_CHARS})
        if soft:
            rep.warn(f"{rel(path)}:{no} 标题含标点类字符 {' '.join(soft)}，核对一下显示效果（{text}）")
        if text != text.strip():
            rep.err(f"{rel(path)}:{no} 标题首尾有空白：{text!r}")
        if len(text) > 60:
            rep.warn(f"{rel(path)}:{no} 标题过长（{len(text)} 字）：{text}")
    if path.parent.name in ("chapters", "appendix") and h1 != 1:
        rep.err(f"{rel(path)} 应该恰好有一个一级标题，实际 {h1} 个")


def check_fences(rep: Report, path: Path) -> None:
    fence = None
    start = 0
    for no, line, _, _ in iter_lines_outside_fence(path):
        m = re.match(r"^\s*(`{3,})(.*)$", line)
        if not m:
            continue
        ticks, info = m.group(1), m.group(2)
        if fence is None:
            fence, start = ticks, no
        elif len(ticks) >= len(fence) and not info.strip():
            fence = None
        elif len(ticks) >= len(fence):
            rep.warn(f"{rel(path)}:{no} 代码块内出现了同一层级的围栏，可能造成嵌套错乱")
    if fence is not None:
        rep.err(f"{rel(path)}:{start} 代码块没有闭合")


def check_images(rep: Report, name: str, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if path.parent.name not in ("chapters", "appendix"):
        return
    ch_no = re.match(r"^ch(\d+)\.md$", path.name)
    app_no = re.match(r"^app([A-Z])\.md$", path.name)
    chapter = int(ch_no.group(1)) if ch_no else None

    for idx, line in enumerate(lines):
        for m in IMG_RE.finditer(line):
            src = m.group(1)
            target = (path.parent / src).resolve()
            if not target.exists():
                rep.err(f"{rel(path)} 引用的图片不存在：{src}")
                continue
            sub = target.parent.name
            if re.match(r"^ch\d+$", sub) and chapter is not None:
                if int(sub[2:]) != chapter:
                    rep.err(f"{rel(path)} 引用了别章的图片目录：{src}")
            if re.match(r"^ch\d+$", sub):
                mm = FIG_NAME_RE.match(target.name)
                if not mm:
                    rep.err(f"{rel(target)} 文件名应为 fig<章号>-<序号>-<英文短名>.png")
                elif int(mm.group(1)) != int(sub[2:]):
                    rep.err(f"{rel(target)} 文件名章号与所在目录章号不一致")
            # 图注在图片下一行，且编号与章号一致
            nxt = ""
            for j in range(idx + 1, min(idx + 4, len(lines))):
                if lines[j].strip():
                    nxt = lines[j].strip()
                    break
            if not nxt.startswith("*图"):
                rep.warn(f"{rel(path)}:{idx + 1} 图片下面没有图注（*图 N-M　……*）")
            elif chapter is not None:
                cm = re.match(r"^\*图\s*(\d+)-(\d+)", nxt)
                if cm and int(cm.group(1)) != chapter:
                    rep.err(f"{rel(path)}:{idx + 1} 图注章号与本章不一致：{nxt}")
    if app_no is None and chapter is None:
        return


def check_cross_book(rep: Report, name: str, path: Path, forbidden: list[str]) -> None:
    """禁止跨册引用：路径、另一册的分册名与副标题。"""
    text = path.read_text(encoding="utf-8")
    others = [b for b in ("intro", "pro") if b != name]
    for other in others:
        for m in re.finditer(rf"books/{other}/|\.\./{other}/", text):
            line = text[: m.start()].count("\n") + 1
            rep.err(f"{rel(path)}:{line} 跨册引用另一本书（{other}），改稿后会失效")
    for word in forbidden:
        for m in re.finditer(re.escape(word), text):
            line = text[: m.start()].count("\n") + 1
            rep.err(f"{rel(path)}:{line} 提到了另一册（“{word}”），单册改稿会对不上")
    for word in ("另一册", "另一本书", "姊妹篇", "上册", "下册"):
        for m in re.finditer(re.escape(word), text):
            line = text[: m.start()].count("\n") + 1
            rep.err(f"{rel(path)}:{line} 出现了指向其他书的措辞“{word}”")


def check_chapter_refs(rep: Report, path: Path, total: int) -> None:
    """正文里的“第 N 章”不能超出本册章数（超了往往就是跨册残留）。"""
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"第\s*(\d+)\s*(?:[~～—-]\s*(\d+)\s*)?章", text):
        hi = int(m.group(2) or m.group(1))
        if hi > total:
            line = text[: m.start()].count("\n") + 1
            rep.err(f"{rel(path)}:{line} 引用了本册不存在的章节（{m.group(0)}，本册共 {total} 章）")


def check_md_links(rep: Report, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for m in LINK_RE.finditer(text):
        link = m.group(1)
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        link = link.split("#")[0]
        if not link:
            continue
        if not link.endswith(".md") and not link.endswith(".pdf"):
            continue
        target = (path.parent / link).resolve()
        if not target.exists() and not (ROOT / link).exists():
            line = text[: m.start()].count("\n") + 1
            rep.err(f"{rel(path)}:{line} 链接指向的文件不存在：{link}")


def check_site(rep: Report) -> None:
    for f in ("index.html", "README.md", "_sidebar.md", "_coverpage.md", ".nojekyll"):
        if not (ROOT / f).exists():
            rep.err(f"站点根目录缺少 {f}")
    for f in ("README.md", "_sidebar.md", "_coverpage.md", "index.html"):
        p = ROOT / f
        if not p.exists():
            continue
        if f == "index.html":
            continue
        text = p.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            link = m.group(1)
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            raw = link
            snippet = text[m.start():m.end()]
            if link.endswith(".pdf") and ":ignore" not in snippet:
                rep.warn(f"{f} 的 PDF 链接没加 ' :ignore'，docsify 会当页面去读：{raw}")
            link = link.split("#")[0]
            if link.startswith("/"):
                target = ROOT / link.lstrip("/")
            else:
                target = ROOT / link
            if not target.exists():
                line = text[: m.start()].count("\n") + 1
                rep.err(f"{f}:{line} 站内链接不存在：{raw}")


def check_pdfs(rep: Report, meta_by_book: dict[str, dict]) -> None:
    try:
        import pymupdf
    except ImportError:
        rep.warn("没有安装 pymupdf，跳过 PDF 检查")
        return
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    for name, meta in meta_by_book.items():
        pdf = OUT_DIR / meta["pdf"]
        if not pdf.exists():
            rep.err(f"{name}: 缺少 PDF output/{meta['pdf']}，请先构建")
            continue
        mb = pdf.stat().st_size / 1024 / 1024
        doc = pymupdf.open(str(pdf))
        pages = doc.page_count
        toc = len(doc.get_toc())
        title = doc.metadata.get("title") or ""
        doc.close()
        if mb > LIMIT_MB:
            rep.err(f"{name}: PDF {mb:.1f} MB，超过 {LIMIT_MB:.0f} MB 上限")
        if pages < 10:
            rep.err(f"{name}: PDF 只有 {pages} 页，可能排版失败")
        if toc < 10:
            rep.err(f"{name}: PDF 书签只有 {toc} 条，目录可能没生成")
        if "状态空间模型" not in title:
            rep.warn(f"{name}: PDF 元数据标题可疑：{title!r}")

        # 页脚页码：抽查正文页，确认盖上了（曾经因为变量名写错静默漏盖）
        doc = pymupdf.open(str(pdf))
        body = list(range(5, max(6, doc.page_count - 2)))
        if len(body) > 24:
            step = len(body) / 24
            body = [body[int(i * step)] for i in range(24)]
        missing = 0
        for i in body:
            page = doc[i]
            band = pymupdf.Rect(0, page.rect.height - 36, page.rect.width, page.rect.height)
            if str(i + 1) not in {w[4] for w in page.get_text("words", clip=band)}:
                missing += 1
        doc.close()
        if missing > max(1, len(body) // 12):
            rep.err(f"{name}: 抽查 {len(body)} 页里有 {missing} 页没有页脚页码")

        # 右侧页眉应当跟着章走刷（曾经因为按 key 字母序排序，全书停在「前言」）
        doc = pymupdf.open(str(pdf))
        heads = set()
        for i in body:
            page = doc[i]
            band = pymupdf.Rect(page.rect.width - 320, 15, page.rect.width - 40, 40)
            heads.add("".join(w[4] for w in page.get_text("words", clip=band)))
        doc.close()
        heads.discard("")
        if len(heads) < 3 or not any(h.startswith("第") for h in heads):
            rep.err(f"{name}: 页眉没有跟着章节变化（抽查到的只有 {sorted(heads)[:4]}）")
        row = next((line for line in readme.splitlines() if meta["pdf"] in line), "")
        m = re.search(r"(\d+)\s*页", row)
        if not m:
            rep.warn(f"{name}: README 里没有标注 {meta['pdf']} 的页数")
        elif int(m.group(1)) != pages:
            rep.err(f"{name}: README 写 {m.group(1)} 页，实际 {pages} 页")


def check_git_tracks(rep: Report) -> None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                             capture_output=True, text=True, check=False)
    except OSError:
        return
    if out.returncode != 0:
        rep.warn("不是 git 仓库或没有 git，跳过仓库检查")
        return
    tracked = [line for line in out.stdout.splitlines() if line]
    for prefix in ("_private/", "papers/", "books/build/vendor/", "books/build/out/"):
        hit = [t for t in tracked if t.startswith(prefix)]
        if hit:
            rep.err(f"这些本地资料被 git 跟踪了（{prefix}，{len(hit)} 个文件）")
    if not any(t.startswith(".gitignore") for t in tracked):
        rep.err(".gitignore 没有被跟踪")


def main() -> int:
    names = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not names:
        names = sorted(p.name for p in BOOKS_DIR.iterdir()
                       if p.is_dir() and (p / "book.json").exists())
    rep = Report()
    meta_by_book: dict[str, dict] = {}
    pdfs: dict[str, str] = {}

    # 先把每册的元数据读出来，供「禁止提到另一册」使用
    for name in names:
        cfg = check_config(rep, name)
        if cfg:
            meta_by_book[name] = cfg[0]

    forbidden_by_book: dict[str, list[str]] = {}
    for name, meta in meta_by_book.items():
        words: list[str] = []
        for other, om in meta_by_book.items():
            if other == name:
                continue
            for key in ("edition", "subtitle"):
                v = str(om.get(key, "")).strip()
                if v:
                    words.append(v)
        forbidden_by_book[name] = words

    for name in names:
        print(f"-- 体检 {name}")
        if name not in meta_by_book:
            continue
        meta = meta_by_book[name]
        struct = json.loads((BOOKS_DIR / name / "structure.json").read_text(encoding="utf-8"))
        if meta["pdf"] in pdfs:
            rep.err(f"{name} 与 {pdfs[meta['pdf']]} 的 PDF 输出文件名相同（{meta['pdf']}）")
        pdfs[meta["pdf"]] = name

        check_structure(rep, name, struct)
        chs = [int(m.group(1)) for m in
               (re.match(r"^ch(\d+)\.md$", p.name) for p in (BOOKS_DIR / name / "chapters").glob("*.md")) if m]
        total = max(chs) if chs else 0
        for path in md_files(BOOKS_DIR / name):
            check_headings(rep, name, path)
            check_fences(rep, path)
            check_images(rep, name, path)
            check_cross_book(rep, name, path, forbidden_by_book.get(name, []))
            if path.parent.name in ("chapters", "front", "appendix"):
                check_chapter_refs(rep, path, total)
            check_md_links(rep, path)

        # 图片目录与孤儿图
        images = BOOKS_DIR / name / "images"
        used = set()
        for path in md_files(BOOKS_DIR / name):
            for m in IMG_RE.finditer(path.read_text(encoding="utf-8")):
                used.add((path.parent / m.group(1)).resolve())
        for img in sorted(images.rglob("*")):
            if img.suffix.lower() not in (".png", ".jpg"):
                continue
            if img.resolve() not in used and img.name not in ("cover.jpg", "backcover.jpg"):
                rep.warn(f"{name}: 这张图没有被正文引用 {rel(img)}")

    check_site(rep)
    check_pdfs(rep, meta_by_book)
    check_git_tracks(rep)
    rep.show("体检结果")

    print()
    if rep.errors:
        print(f"体检未通过：{len(rep.errors)} 个错误，{len(rep.warns)} 个提醒")
        return 1
    print(f"体检通过：{len(rep.warns)} 个提醒")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
