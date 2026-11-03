# -*- coding: utf-8 -*-
"""CH23 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_contraction():
    fig, ax = canvas(16.0, 0.62)
    label(ax, 25, 94, "二次顺序", fs=9, weight="bold")
    label(ax, 75, 94, "线性顺序", fs=9, weight="bold")

    box(ax, 3, 74, 14, 11, r"$Q:(T,N)$", fc="#eef3f8", ec=BLUE, fs=7.4)
    box(ax, 3, 59, 14, 11, r"$K:(S,N)$", fc="#eef3f8", ec=BLUE, fs=7.4)
    box(ax, 25, 66, 18, 13, "$G=QK^{\\top}$\n$(T,S)$", fc="white", ec=BLUE, fs=7.4)
    arrow(ax, 17.4, 79.5, 24.6, 74.5, color=BLUE)
    arrow(ax, 17.4, 64.5, 24.6, 69.5, color=BLUE)
    box(ax, 25, 48, 18, 11, r"$M=L\circ G$", fc="white", ec=ORANGE, fs=7.4)
    arrow(ax, 34, 65.4, 34, 59.6, color=ORANGE)
    box(ax, 25, 33, 18, 11, r"$Y=MV$", fc="white", ec=GREEN, fs=7.4)
    box(ax, 3, 34, 14, 10, r"$V:(S,P)$", fc="#eef3f8", ec=BLUE, fs=7.4)
    arrow(ax, 17.4, 39, 24.6, 39, color=GREEN)
    arrow(ax, 34, 47.4, 34, 44.6, color=GREEN)
    label(ax, 3, 24, r"瓶颈：$G$ 是 $T\times S$ 的稠密矩阵", fs=7.2, color=ORANGE, ha="left")

    box(ax, 57, 74, 14, 11, r"$V:(S,P)$", fc="#eef3f8", ec=BLUE, fs=7.4)
    box(ax, 57, 59, 14, 11, r"$K:(S,N)$", fc="#eef3f8", ec=BLUE, fs=7.4)
    box(ax, 79, 66, 18, 13, "$Z=VK^{\\top}$\n$(S,P,N)$", fc="white", ec=BLUE, fs=7.4)
    arrow(ax, 71.4, 79.5, 78.6, 74.5, color=BLUE)
    arrow(ax, 71.4, 64.5, 78.6, 69.5, color=BLUE)
    box(ax, 79, 48, 18, 11, r"$H=L\,Z$", fc="white", ec=ORANGE, fs=7.4)
    arrow(ax, 88, 65.4, 88, 59.6, color=ORANGE)
    box(ax, 79, 33, 18, 11, r"$Y=QH$", fc="white", ec=GREEN, fs=7.4)
    arrow(ax, 88, 47.4, 88, 44.6, color=GREEN)
    label(ax, 57, 24, r"瓶颈：只有 $L$ 这一步同时含 $T$ 与 $S$", fs=7.2, color=ORANGE, ha="left")
    label(ax, 56, 11, r"$L$ 是因果掩码时，$LZ$ 就是沿序列的累积求和，$O(T)$", fs=7.4, color=GREEN)
    save(fig, "fig15-contraction.svg")


# ================================================================
# 图 17-1  SSD 块分解
# ================================================================


FIGURES = ['fig_contraction']