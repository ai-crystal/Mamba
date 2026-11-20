# -*- coding: utf-8 -*-
"""CH25 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_ssd():
    fig, ax = canvas(16.2, 0.78)
    n, q = 30, 10
    x0, y0, w, h = 6, 40, 34, 36
    ax.add_patch(Rectangle((x0, y0), w, h, fc="#fbfbfb", ec=MUTED, lw=0.8))
    for k in range(0, n, q):
        ax.plot([x0, x0 + w], [y0 + h - k / n * h] * 2, color=LIGHT, lw=0.7)
        ax.plot([x0 + k / n * w] * 2, [y0, y0 + h], color=LIGHT, lw=0.7)
    for b in range(3):
        ax.add_patch(Rectangle((x0 + b / 3 * w, y0 + h - (b + 1) / 3 * h),
                               w / 3, h / 3, fc=ORANGE, alpha=0.22, ec=ORANGE, lw=0.8))
    for b in range(3):
        ax.text(x0 + (b + 0.5) / 3 * w, y0 + h - (b + 0.5) / 3 * h, "块内\n二次",
                ha="center", va="center", fontsize=6.2, color=ORANGE, linespacing=1.3)
    ax.add_patch(Rectangle((x0, y0 + h - h / 3), w / 3, h / 3, fill=False,
                           ec=GREEN, lw=1.0, ls="--"))
    ax.text(x0 - 2.0, y0 + h - h / 6, "低秩块", ha="right", va="center",
            fontsize=6.2, color=GREEN)
    label(ax, 23, 79, r"把 $M$ 切成 $Q\times Q$ 的块", fs=8.2)
    label(ax, 23, 36, r"$Y=Y_{\mathrm{diag}}+Y_{\mathrm{off}}$", fs=7.8)

    steps = [
        ("① 块内输出", r"$Y_{\mathrm{diag}}=\mathrm{attn}(C,B,X)$，初状态设为 0", ORANGE),
        ("② 右因子", r"$S_j=\sum_{i\in\mathrm{chunk}}B_i^{\top}A_{\cdot:i}x_i$，块末状态", BLUE),
        ("③ 中心因子", r"$H_j=\alpha_{j:j-1}H_{j-1}+S_j$，块间递推（长度 $T/Q$）", GREEN),
        ("④ 左因子", r"$Y_{\mathrm{off}}=C^{\top}H\cdot\alpha$，历史经状态的贡献", PURPLE),
    ]
    for k, (tag, formula, col) in enumerate(steps):
        yy = 68 - k * 15
        box(ax, 46, yy, 18, 11, tag, fc="white", ec=col, fs=7.2, color=col)
        label(ax, 66, yy + 5.5, formula, fs=6.6, ha="left", color=INK)
    save(fig, "fig25-01-ssd.svg")


# ================================================================
# 图 18-1  head 模式
# ================================================================


FIGURES = ['fig_ssd']