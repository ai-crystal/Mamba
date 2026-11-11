# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "code" / "ch01" / "figures.py"
lines = p.read_text(encoding="utf-8").split("\n")
out = []
i = 0
while i < len(lines):
    if "ax.text(9.6, 5.0," in lines[i]:
        out.append('    ax.text(9.6, 5.0, "每个输出" + chr(10) + "回看全部历史", ha="center", va="center",')
        i += 2
        continue
    out.append(lines[i])
    i += 1
p.write_text("\n".join(out), encoding="utf-8")
print("ok")
