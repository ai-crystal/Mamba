# -*- coding: utf-8 -*-
"""CH10 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_s4_pipeline():
    fig, ax = canvas(16.2, 0.78)
    rows = [
        (78, "目标", r"$\bar K_i=\bar C\bar A^{\,i}\bar B,\quad i=0,\dots,L-1$",
         r"需要对 $A$ 求 $L$ 次幂", LIGHT, INK),
        (60, "降维一", r"$\hat K(z)=\bar C(I-\bar Az)^{-1}\bar B$",
         r"生成函数：幂 → 逆；在 $L$ 次单位根上取值后 iFFT", "#eef3f8", BLUE),
        (42, "降维二", r"$(\Lambda-PQ^{*})^{-1}$ 用 Woodbury 展开",
         "低秩项被精确消掉，只剩对角矩阵的逆", "#fdf3ee", ORANGE),
        (24, "降维三", r"$M_{ij}=\frac{1}{\omega_i-\lambda_j}$",
         "柯西核：有稳定的近线性算法", "#eef4f0", GREEN),
    ]
    for y, tag, formula, note, fc, ec in rows:
        box(ax, 4, y, 12, 12, tag, fc=fc, ec=ec, fs=8, weight="bold", color=ec)
        box(ax, 18, y, 46, 12, formula, fc="white", ec=ec, fs=7.2)
        label(ax, 67, y + 6, note, fs=7.2, ha="left", color=MUTED)

    for y in [78, 60, 42]:
        arrow(ax, 50, y - 0.6, 50, y - 12.4, color=MUTED, lw=0.9)

    box(ax, 18, 5, 62, 11,
        r"$\tilde O(N+L)$ 时间、$O(N+L)$ 空间，达到下界 $\Omega(N+L)$",
        fc="#f7f7f7", ec=INK, fs=8)
    save(fig, "fig09-s4-pipeline.svg")


# ---------------------------------------------------------------- 主流程


FIGURES = ['fig_s4_pipeline']