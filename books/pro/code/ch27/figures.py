# -*- coding: utf-8 -*-
"""CH27 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_attn_ratio():
    layers = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 15, 24]
    ppl = [8.60, 8.38, 8.32, 8.29, 8.29, 8.28, 8.26, 8.27, 8.28, 8.30, 8.34, 8.50]
    fig, ax = plt.subplots(figsize=(16.0 / 2.54, 5.0 / 2.54))
    ax.plot(layers, ppl, color=BLUE, lw=1.4, marker="o", ms=3.5)
    ax.axhline(8.68, color=MUTED, lw=0.9, ls="--")
    ax.text(23.5, 8.692, "纯 Transformer++  8.68", fontsize=6.8, color=MUTED,
            ha="right", va="bottom")
    ax.scatter([6], [8.26], color=ORANGE, zorder=5, s=26)
    ax.annotate("6 / 48 ≈ 12.5%\n8.26", xy=(6, 8.26), xytext=(9.4, 8.40),
                fontsize=7, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
    ax.set_xlabel("48 层中注意力层的数量", fontsize=8)
    ax.set_ylabel("Pile 困惑度", fontsize=7.6)
    ax.set_ylim(top=8.735)
    ax.grid(alpha=0.25, lw=0.5)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)
    save(fig, "fig27-01-attn-ratio.svg")


# ================================================================
# 图 22-1  实数缩放与复数旋转
# ================================================================


FIGURES = ['fig_attn_ratio']