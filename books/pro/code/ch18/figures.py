# -*- coding: utf-8 -*-
"""CH18 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_shapes():
    fig, ax = canvas(16.0, 0.5)
    label(ax, 24, 92, "S4（时不变）", fs=9, weight="bold")
    label(ax, 72, 92, "S6（时变）", fs=9, weight="bold")

    # S4: (D,N)
    for i in range(3):
        box(ax, 8 + i * 11, 62, 9, 12, "", fc="#eef3f8", ec=BLUE, lw=0.7)
    label(ax, 24, 78, r"$\bar A,\ \bar B:(D,N)$", fs=8, color=BLUE)
    label(ax, 24, 55, r"参数量与 $L$ 无关", fs=7.2, color=MUTED)

    # S6: (B,L,D,N)
    for i in range(3):
        for j in range(4):
            box(ax, 56 + i * 6.2, 46 + j * 6.6, 5.4, 5.6, "", fc="#fdf3ee", ec=ORANGE, lw=0.6)
    label(ax, 66, 78, r"$\bar A,\ \bar B:(B,L,D,N)$", fs=8, color=ORANGE)
    label(ax, 72, 36, "$B{=}32,\\ L{=}2048,\\ D{=}1024,\\ N{=}16$\n$\\approx10^{9}$ 个数（FP32 约 4 GB）",
          fs=7.2, color=MUTED)

    arrow(ax, 44, 67, 54, 67, color=MUTED)
    label(ax, 49, 71, "选择性", fs=7, color=MUTED)
    label(ax, 50, 12, r"同一个模型规模，仅仅因为参数依赖输入，中间张量就膨胀了 $N$ 倍",
          fs=7.4, color=MUTED)
    save(fig, "fig18-01-shapes.svg")


# ================================================================
# 图 14-1  显存层级与核融合
# ================================================================


FIGURES = ['fig_shapes']