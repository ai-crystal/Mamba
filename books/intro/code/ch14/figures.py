# -*- coding: utf-8 -*-
"""CH14 插图：这条线的时间轴。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_timeline():
    fig, ax = canvas(16.0, 0.58)
    items = [
        ("2020", "HiPPO", "把记忆写成优化问题，给出状态矩阵"),
        ("2021", "LSSL", "变成一层网络，同时是 RNN、CNN、ODE"),
        ("2021", "S4", "结构化参数化，把卷积核算出来"),
        ("2022", "S5", "换用并行扫描，纯时域计算"),
        ("2023", "Mamba", "让参数依赖输入，学会选择"),
        ("2024", "Mamba-2", "证明 SSM 与线性注意力同构"),
        ("2026", "Mamba-3", "复值状态、梯形离散化、MIMO"),
    ]
    x_line = 36.0
    top, bottom = 90.0, 8.0
    ax.plot([x_line, x_line], [bottom, top], color=LIGHT, lw=2.2, solid_capstyle="round")

    step = (top - bottom) / (len(items) - 1)
    for i, (year, name, note) in enumerate(items):
        y = top - i * step
        ax.add_patch(Circle((x_line, y), 1.0, fc="white", ec=BLUE, lw=1.1, zorder=5))
        ax.text(x_line - 3.0, y, year, ha="right", va="center", fontsize=7.6, color=BLUE)
        ax.text(x_line + 3.0, y + 1.6, name, ha="left", va="bottom",
                fontsize=8.6, color=INK, weight="bold")
        ax.text(x_line + 3.0, y - 1.4, note, ha="left", va="top",
                fontsize=7.0, color=MUTED)
    save(fig, "fig14-01-timeline.svg")


FIGURES = ["fig_timeline"]
