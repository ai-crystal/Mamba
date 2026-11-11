# -*- coding: utf-8 -*-
"""CH20 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_mamba_block():
    fig, ax = canvas(16.2, 0.66)

    box(ax, 2, 30, 9, 12, "输入\n$(B,L,D)$", fc="#f7f7f7", fs=6.8)
    # 上支路
    box(ax, 15, 50, 16, 9, r"Linear $D\to ED$", fc="white", fs=7, ec=BLUE)
    box(ax, 35, 50, 12, 9, "Conv1d\n$k=4$", fc="white", fs=6.6, ec=INK)
    box(ax, 51, 50, 8, 9, "SiLU", fc="white", fs=6.6, ec=INK)
    box(ax, 63, 48, 15, 13, "Selective\nSSM", fc="#fdf3ee", fs=7.2, ec=ORANGE)
    # 下支路
    box(ax, 15, 26, 16, 9, r"Linear $D\to ED$", fc="white", fs=7, ec=BLUE)
    box(ax, 35, 26, 8, 9, "SiLU", fc="white", fs=6.6, ec=INK)
    # 乘法
    ax.add_patch(Circle((84, 42), 1.7, fc="white", ec=INK, lw=0.8, zorder=6))
    ax.text(84, 42, "×", fontsize=8, ha="center", va="center", zorder=7)
    box(ax, 69, 12, 20, 9, r"Linear $ED\to D$", fc="white", fs=7, ec=BLUE)

    arrow(ax, 11.2, 39, 14.6, 53.5, color=BLUE)
    arrow(ax, 11.2, 33, 14.6, 30.5, color=BLUE)
    for x1, x2 in [(31.2, 34.6), (47.2, 50.6), (59.2, 62.6)]:
        arrow(ax, x1, 54.5, x2, 54.5)
    for x1, x2 in [(31.2, 34.6)]:
        arrow(ax, x1, 30.5, x2, 30.5)
    arrow(ax, 78.2, 54.5, 82.4, 43.4, color=ORANGE)
    arrow(ax, 43.4, 30.5, 82.3, 40.7, color=INK, rad=-0.08)
    arrow(ax, 84, 40.2, 84, 21.4, color=BLUE)

    label(ax, 70.5, 66, r"$\Delta,B,C$ 由 $x'$ 投影", fs=6.6, color=ORANGE)
    arrow(ax, 70.5, 64.4, 70.5, 61.4, color=ORANGE, ls=(0, (3, 2)), lw=0.7)
    label(ax, 22, 20, "门控分支", fs=6.6, color=MUTED, ha="center")
    label(ax, 60, 16.5, "输出 + 残差", fs=6.8, color=MUTED, ha="left")
    save(fig, "fig23-mamba-block.svg")


# ================================================================
# 图 24-2  SSM 层的接口
# ================================================================


FIGURES = ['fig_mamba_block']