# -*- coding: utf-8 -*-
"""把标题里的 LaTeX 转成 Unicode 纯文本，避免标题含特殊字符。"""
import re
from pathlib import Path

GREEK = {
    "\\Delta": "Δ", "\\Theta": "Θ", "\\Lambda": "Λ", "\\Omega": "Ω",
    "\\alpha": "α", "\\beta": "β", "\\gamma": "γ", "\\delta": "δ",
    "\\lambda": "λ", "\\mu": "μ", "\\sigma": "σ", "\\tau": "τ",
    "\\theta": "θ", "\\phi": "φ", "\\pi": "π", "\\eta": "η",
    "\\epsilon": "ε", "\\omega": "ω", "\\rho": "ρ",
}
SYM = {
    "\\top": "ᵀ", "\\odot": "⊙", "\\approx": "≈", "\\leq": "≤", "\\le": "≤",
    "\\geq": "≥", "\\ge": "≥", "\\times": "×", "\\cdot": "·", "\\to": "→",
    "\\infty": "∞", "\\in": "∈", "\\sum": "Σ", "\\prod": "∏",
}
WRAP = re.compile(r"\\(?:text|mathrm|operatorname)\{([^{}]*)\}")


def plain(tex: str) -> str:
    t = tex
    for k, v in {**GREEK, **SYM}.items():
        t = t.replace(k, v)
    t = t.replace("\\mathbb{R}", "R").replace("\\mathbb{C}", "C")
    t = t.replace("\\mathrm{Re}", "Re")
    t = WRAP.sub(r"\1", t)
    for ch in ("\\", "{", "}", "^", "_"):
        t = t.replace(ch, "")
    return t.strip()


def main() -> None:
    files = sorted(Path("chapters").glob("*.md")) + sorted(Path("appendix").glob("*.md"))
    for p in files:
        s = p.read_text(encoding="utf-8")
        out = []
        changed = False
        for line in s.split("\n"):
            if line.startswith("#") and "$" in line:
                line = re.sub(r"\$([^$]+)\$", lambda m: plain(m.group(1)), line)
                line = line.rstrip()
                changed = True
            out.append(line)
        if changed:
            p.write_text("\n".join(out), encoding="utf-8")
            print("fixed", p)


if __name__ == "__main__":
    main()
