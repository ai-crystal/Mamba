# -*- coding: utf-8 -*-
"""CH19 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_memory():
    fig, axes = plt.subplots(1, 2, figsize=(16.0 / 2.54, 5.4 / 2.54))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")

    ax = axes[0]
    ax.add_patch(FancyBboxPatch((0.4, 8.2), 9.2, 3.4,
                                 boxstyle="round,pad=0,rounding_size=0.2",
                                 fc="#f7f7f7", ec=MUTED, lw=0.8))
    bs = chr(92)
    ax.text(5, 10.9, "HBM（显存，慢而大）", ha="center", fontsize=8)
    for i in range(3):
        ax.add_patch(Rectangle((1.1 + i * 2.85, 8.9), 2.3, 1.5, fc="#e8ebee", ec="none"))
    ax.add_patch(FancyBboxPatch((2.6, 1.6), 4.8, 2.8,
                                 boxstyle="round,pad=0,rounding_size=0.2",
                                 fc="#fff4ec", ec=ORANGE, lw=0.9))
    ax.text(5, 3.0, "SRAM", ha="center", fontsize=8.5, color=ORANGE)
    ax.annotate("", xy=(5.0, 4.5), xytext=(5.0, 8.1),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.0))
    ax.text(5.4, 7.0, f"写/读 ${bs}bar A,{bs}bar B$" + chr(10) + "$(B,L,D,N)$，$O(N)$ 倍", fontsize=7, color=ORANGE, va="center", ha="left", linespacing=1.5)

    ax = axes[1]
    ax.add_patch(FancyBboxPatch((0.4, 8.2), 9.2, 3.4,
                                 boxstyle="round,pad=0,rounding_size=0.2",
                                 fc="#f7f7f7", ec=MUTED, lw=0.8))
    ax.text(5, 10.9, "HBM", ha="center", fontsize=8)
    ax.text(5, 9.5, r"$\Delta,A,B,C$：$O(BLD+DN)$", ha="center", fontsize=7.2)
    ax.add_patch(FancyBboxPatch((1.8, 1.6), 6.4, 2.8,
                                 boxstyle="round,pad=0,rounding_size=0.2",
                                 fc="#eef4f0", ec=GREEN, lw=0.9))
    ax.text(5, 3.3, "融合 kernel", ha="center", fontsize=8.2, color=GREEN)
    ax.text(5, 2.4, r"离散化 → 扫描 → 乘 $C$", ha="center", fontsize=7)
    ax.annotate("", xy=(3.2, 4.5), xytext=(3.2, 8.1),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0))
    ax.annotate("", xy=(6.8, 8.1), xytext=(6.8, 4.5),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0))
    ax.text(2.85, 6.3, "只读参数", fontsize=6.8, color=GREEN, ha="right", va="center")
    ax.text(7.15, 6.3, "只写\n$(B,L,D)$", fontsize=6.8, color=GREEN, ha="left", va="center",
            linespacing=1.5)
    save(fig, "fig19-01-memory.svg")


# ================================================================
# 图 15-1  半可分矩阵的块结构
# ================================================================


FIGURES = ['fig_memory']