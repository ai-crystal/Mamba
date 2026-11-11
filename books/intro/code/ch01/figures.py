# -*- coding: utf-8 -*-
"""入门版插图：三种记忆方式、压缩与重建、HiPPO 投影、选择机制、时间线。"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


# ---------------------------------------------------------------- 图 1-1
def fig_three_ways():
    fig, axes = plt.subplots(1, 3, figsize=(16.0 / 2.54, 4.8 / 2.54))
    for ax in axes:
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 10)
        ax.axis("off")

    def tokens(ax, y=6.6, n=5):
        xs = [1.4 + i * 2.3 for i in range(n)]
        for i, x in enumerate(xs):
            ax.add_patch(Circle((x, y), 0.42, fc="#eef3f8", ec=BLUE, lw=0.8))
            if i < n - 1:
                arrow(ax, x + 0.45, y, xs[i + 1] - 0.45, y, color=BLUE, lw=0.7, ms=5)
        return xs

    ax = axes[0]
    xs = tokens(ax)
    ax.text(6, 8.6, "循环网络", ha="center", fontsize=9.5, color=INK)
    ax.add_patch(FancyBboxPatch((2.0, 1.9), 8.0, 1.8, boxstyle="round,pad=0,rounding_size=0.2",
                                fc="#fdf3ee", ec=ORANGE, lw=1.0))
    ax.text(6, 2.8, "一个固定大小的状态", ha="center", fontsize=7.6, color=ORANGE)
    for x in xs:
        arrow(ax, x, 3.9, x, 6.1, color=MUTED, lw=0.6, ms=5)
    ax.text(6, 0.9, "所有历史都压进这一个状态", ha="center", fontsize=7.2, color=MUTED)

    ax = axes[1]
    xs = tokens(ax)
    ax.text(6, 8.6, "卷积", ha="center", fontsize=9.5, color=INK)
    ax.add_patch(FancyBboxPatch((xs[1] - 0.6, 5.95), 3 * 2.3, 1.3,
                                boxstyle="round,pad=0,rounding_size=0.15",
                                fc="#fdf3ee", ec=ORANGE, lw=0.9, alpha=0.85))
    ax.text(6, 3.3, "只看最近的几个点", ha="center", fontsize=7.6, color=ORANGE)
    arrow(ax, 6, 5.9, 6, 3.9, color=ORANGE, lw=0.8)
    ax.text(6, 0.9, "窗口多大，要事先定死", ha="center", fontsize=7.2, color=MUTED)

    ax = axes[2]
    n = 6
    x0, y0, c = 2.2, 2.8, 0.62
    for i in range(n):
        for j in range(n):
            if j <= i:
                alpha = 0.14 + 0.12 * ((i - j) % 3)
                ax.add_patch(Rectangle((x0 + j * c, y0 + (n - 1 - i) * c), c * 0.92, c * 0.92,
                                       fc=BLUE, alpha=alpha, ec="none"))
    ax.add_patch(Rectangle((x0 - 0.08, y0 + (n - 4) * c - 0.08), 4 * c + 0.1, c + 0.1,
                           fill=False, ec=ORANGE, lw=1.0))
    ax.text(6, 8.6, "注意力", ha="center", fontsize=9.5, color=INK)
    ax.text(9.6, 5.0, "每个输出" + chr(10) + "回看全部历史", ha="center", va="center",
            fontsize=7.2, color=ORANGE, linespacing=1.5)
    ax.text(6, 0.9, "记住得最全，代价也最大", ha="center", fontsize=7.2, color=MUTED)
    save(fig, "fig01-three-ways.svg")


# ---------------------------------------------------------------- 图 2-1
FIGURES = ["fig_three_ways"]
