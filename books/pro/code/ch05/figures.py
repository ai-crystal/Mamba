# -*- coding: utf-8 -*-
"""CH05 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_hippo_flow():
    fig, ax = canvas(16.2, 0.62)

    box(ax, 2, 68, 20, 13, "输入函数\n$f(x),\\ x\\leq t$", fc="#fbfbfb", fs=7.6)
    box(ax, 28, 68, 22, 13, "选一个测度 $\\mu^{(t)}$\n（谁更重要）", fc="#fbfbfb", fs=7.6)
    box(ax, 56, 68, 20, 13, "正交多项式基\n$g_n(t,x)$", fc="#fbfbfb", fs=7.6)
    box(ax, 80, 68, 18, 13, "投影\n$g^{(t)}=\\mathrm{proj}_t f$", fc="#eef3f8", fs=7.6, ec=BLUE)

    arrow(ax, 22.4, 74.5, 27.6, 74.5)
    arrow(ax, 50.4, 74.5, 55.6, 74.5)
    arrow(ax, 76.4, 74.5, 79.6, 74.5)

    box(ax, 76, 44, 22, 13, "系数\n$c_n(t)=\\langle f,g_n\\rangle_{\\mu^{(t)}}$", fc="#eef3f8", fs=7.4, ec=BLUE)
    arrow(ax, 89, 67.4, 89, 57.6, color=BLUE)

    box(ax, 44, 44, 26, 13, r"对 $t$ 求导，合并同类项", fc="#fdf3ee", fs=7.6, ec=ORANGE)
    arrow(ax, 79.6, 50.5, 70.4, 50.5, color=ORANGE)

    box(ax, 40, 18, 34, 14,
        r"$\frac{d}{dt}c(t)=-A(t)\,c(t)+B(t)\,f(t)$" + "\n" + "这就是一个 SSM",
        fc="#fdf3ee", fs=8, ec=ORANGE, lw=1.0)
    arrow(ax, 57, 43.4, 57, 32.6, color=ORANGE)

    label(ax, 18, 52, "测度决定 $A$ 的形状：\n滑动窗口 → LegT\n指数衰减 → LagT\n缩放窗口 → LegS",
          fs=7.2, color=MUTED, ha="left")
    save(fig, "fig05-01-hippo-flow.svg")


# ================================================================
# 图 7-1  LSSL 的三种切法
# ================================================================


FIGURES = ['fig_hippo_flow']