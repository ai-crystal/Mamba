# -*- coding: utf-8 -*-
"""CH08 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_picard():
    fig, ax = canvas(16.0, 0.92)
    label(ax, 50, 96, "连续 ODE", fs=9, weight="bold")
    label(ax, 50, 89, r"$\dot x(t)=-x(t)+f(t,x(t))$", fs=9, color=BLUE)

    xs = [8, 28, 48, 68, 88]
    for i, x in enumerate(xs):
        fc = "#eef3f8" if i % 2 == 0 else "#fdf3ee"
        box(ax, x - 7.5, 58, 15, 16, f"第 {i} 次\nPicard 迭代" if i < 4 else "极限",
            fc=fc, fs=7.4, ec=BLUE if i % 2 == 0 else ORANGE)
        if i < 4:
            arrow(ax, x + 7.7, 66, xs[i + 1] - 7.7, 66, lw=0.9)
    label(ax, 50, 44, r"$x_{i+1}(t)=x_i(t_0)+\int_{t_0}^{t} f(s,x_i(s))\,ds$", fs=8.6, color=BLUE)

    label(ax, 50, 33, "同一件事，用层数表示", fs=8.4, color=MUTED)

    for i, x in enumerate(xs):
        fc = "#eef3f8" if i % 2 == 0 else "#fdf3ee"
        box(ax, x - 7.5, 8, 15, 14, "LSSL 层\n($N=1$)" if i < 4 else "输出",
            fc=fc, fs=7.4, ec=BLUE if i % 2 == 0 else ORANGE)
        if i < 4:
            arrow(ax, x + 7.7, 15, xs[i + 1] - 7.7, 15, lw=0.9)
    for x in xs[:-1]:
        label(ax, x + 10, 26, r"$\sigma$", fs=8, color=MUTED)

    label(ax, 50, 1.0, "结论：时间轴上的非线性可以搬到深度方向，换回线性递推的并行性",
          fs=7.4, color=MUTED)
    save(fig, "fig07-picard.svg")


# ================================================================
# 图 10-1  非正规矩阵：特征向量夹角与 V 的增长
# ================================================================


FIGURES = ['fig_picard']