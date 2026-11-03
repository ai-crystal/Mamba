# -*- coding: utf-8 -*-
"""把旧章节文件名链接改写为新结构下的相对路径。"""
import glob
import os
import re
from pathlib import Path

ROOT = Path(".").resolve()
NEW = {}
for i in range(1, 36):
    NEW[f"{i:02d}"] = ROOT / "book" / "chapters" / f"ch{i:02d}.md"
NEW["00"] = ROOT / "book" / "front" / "preface.md"
NEW["90"] = ROOT / "book" / "appendix" / "appA.md"
NEW["91"] = ROOT / "book" / "appendix" / "appB.md"
NEW["92"] = ROOT / "book" / "appendix" / "appC.md"

PAT = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(\s+'[^']*')?\)")


def fix(path: Path) -> int:
    s = path.read_text(encoding="utf-8")
    n = 0

    def repl(m):
        nonlocal n
        text, target, title = m.group(1), m.group(2), m.group(3) or ""
        base = target.split("#")[0]
        if not base or base.startswith("http"):
            return m.group(0)
        mm = re.match(r"^(\d{2})-.*\.md$", base)
        if mm and mm.group(1) in NEW:
            rel = os.path.relpath(NEW[mm.group(1)], path.parent).replace("\\", "/")
            n += 1
            return f"[{text}]({rel}{title})"
        if base == "README.md" and path.parent != ROOT:
            rel = os.path.relpath(ROOT / "README.md", path.parent).replace("\\", "/")
            n += 1
            return f"[{text}]({rel}{title})"
        return m.group(0)

    s2 = PAT.sub(repl, s)
    if s2 != s:
        path.write_text(s2, encoding="utf-8")
    return n


if __name__ == "__main__":
    total = 0
    for f in glob.glob("book/**/*.md", recursive=True) + ["README.md"]:
        total += fix(Path(f))
    print("rewritten links:", total)
