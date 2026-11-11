# -*- coding: utf-8 -*-
"""CH14 插图。"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_timeline():
    fig, ax = canvas(16.0, 0.42)
    items = [
        (2020, "HiPPO", "记忆的数学形式"),
        (2021, "LSSL", "一个层，三种身份"),
        (2021, "S4", "把卷积核算出来"),
        (2022, "S5", "并行扫描"),
        (2023, "Mamba", "让参数看输入"),
        (2024, "Mamba-2", "SSM 就是注意力"),
        (2026, "Mamba-3", "补上状态追踪"),
    ]
    n = len(items)
    ax.plot([6, 94], [50, 50], color=LIGHT, lw=2.0, solid_capstyle="round")
    for i, (year, name, note) in enumerate(items):
        x = 8 + i * (84 / (n - 1))
        up = i % 2 == 0
        ax.plot([x, x], [50, 50 + (10 if up else -10)], color=MUTED, lw=0.8)
        ax.add_patch(Circle((x, 50), 1.1, fc="white", ec=BLUE, lw=1.0, zorder=5))
        ax.text(x, 63 if up else 37, name, ha="center",
                va="bottom" if up else "top", fontsize=8, color=INK, weight="bold")
        ax.text(x, 69 if up else 31, note, ha="center",
                va="bottom" if up else "top", fontsize=6.6, color=MUTED)
        ax.text(x, 44.5 if up else 55.5, str(year), ha="center",
                va="top" if up else "bottom", fontsize=7, color=BLUE)
    save(fig, "fig05-timeline.svg")




FIGURES = ['fig_timeline']
