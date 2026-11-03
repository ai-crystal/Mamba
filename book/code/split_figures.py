# -*- coding: utf-8 -*-
"""把单文件插图脚本拆成 common.py + 每章 figures.py。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "code" / "_legacy_figsrc" / "make_figures.py"
text = LEGACY.read_text(encoding="utf-8")

# 函数 -> 章
MAP = {
    "fig_matrix_mixers": "ch01",
    "fig_ssm_views": "ch02",
    "fig_discretization": "ch02",
    "fig_layer_interface": "ch03",
    "fig_hippo_measures": "ch04",
    "fig_hippo_flow": "ch05",
    "fig_lssl_views": "ch07",
    "fig_picard": "ch08",
    "fig_s4_pipeline": "ch10",
    "fig_nplr": "ch11",
    "fig_selective": "ch17",
    "fig_shapes": "ch18",
    "fig_memory": "ch19",
    "fig_mamba_block": "ch20",
    "fig_semiseparable": "ch22",
    "fig_contraction": "ch23",
    "fig_ssd": "ch25",
    "fig_heads": "ch26",
    "fig_attn_ratio": "ch27",
    "fig_masks": "ch29",
    "fig_rope": "ch30",
    "fig_arith": "ch31",
    "fig_book_map": "front",
}

# 提取函数体
blocks = {}
for m in re.finditer(r"^(def (fig_\w+)\(\):.*?)(?=^def |^if __name__|\Z)", text, re.S | re.M):
    body, name = m.group(1).rstrip() + "\n", m.group(2)
    blocks[name] = body

missing = set(MAP) - set(blocks)
print("missing:", missing)

header_end = text.index("# ================================================================\n# 图 1-1")
header = text[:header_end]

# common.py：样式与工具，save 输出 PNG
common = header.replace(
    'ROOT = Path(__file__).resolve().parents[2]\nOUT = ROOT / "figures"\nOUT.mkdir(exist_ok=True)',
    'CODE = Path(__file__).resolve().parent\nBOOK = CODE.parent\nIMAGES = BOOK / "images"\nCURRENT = IMAGES / "front"'
)
common = common.replace(
    '''def save(fig, name):
    path = OUT / name
    fig.savefig(path, format="svg", transparent=True)
    plt.close(fig)
    print("  ->", path.name)''',
    '''def save(fig, name):
    """把图保存为 PNG，文件名去掉 .svg 后缀。"""
    path = CURRENT / Path(name).with_suffix(".png").name
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="png", dpi=200, transparent=False, facecolor="white")
    plt.close(fig)
    print("  ->", path.relative_to(BOOK))'''
)
(ROOT / "code" / "common.py").write_text(common, encoding="utf-8")

# 每章的 figures.py
groups = {}
for fn, ch in MAP.items():
    groups.setdefault(ch, []).append(fn)

for ch, fns in sorted(groups.items()):
    d = ROOT / "code" / ch
    d.mkdir(parents=True, exist_ok=True)
    parts = [
        "# -*- coding: utf-8 -*-",
        f'"""{"前言与全书结构图" if ch == "front" else ch.upper() + " 插图"}。"""',
        "import sys",
        "from pathlib import Path",
        "",
        "sys.path.insert(0, str(Path(__file__).resolve().parents[1]))",
        "from common import *  # noqa: F401,F403",
        "",
        "",
    ]
    for fn in fns:
        parts.append(blocks[fn])
        parts.append("")
    parts.append(f"FIGURES = {fns!r}")
    (d / "figures.py").write_text("\n".join(parts), encoding="utf-8")
    print("wrote", d / "figures.py", fns)
