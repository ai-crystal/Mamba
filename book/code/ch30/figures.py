# -*- coding: utf-8 -*-
"""CH30 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_rope():
    fig, axes = plt.subplots(1, 2, figsize=(15.2 / 2.54, 5.0 / 2.54))

    ax = axes[0]
    t = np.linspace(0, 3.4, 200)
    ax.plot(t, np.exp(-0.7 * t), color=BLUE, lw=1.3)
    ax.plot(t, -np.exp(-0.7 * t), color=BLUE, lw=1.3, ls=":")
    ax.axhline(0, color=MUTED, lw=0.6)
    ax.set_xlabel("时间", fontsize=7.6)
    ax.set_ylabel("状态", fontsize=7.6)
    ax.text(1.6, 0.72, r"$e^{\lambda t},\ \lambda<0$", fontsize=7.6, color=BLUE)
    ax.set_ylim(-1.1, 1.1)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6.8)

    ax = axes[1]
    th = np.linspace(0, 6 * math.pi, 300)
    r = np.exp(-0.13 * th)
    ax.plot(r * np.cos(th), r * np.sin(th), color=ORANGE, lw=1.2)
    ax.annotate("", xy=(1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=0.9))
    ax.annotate("", xy=(-1, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=0.9))
    ax.text(-0.95, 0.26, "翻转 180°", fontsize=6.8, color=GREEN)
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.2, 1.2)
    ax.axhline(0, color=MUTED, lw=0.5)
    ax.axvline(0, color=MUTED, lw=0.5)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    fig.subplots_adjust(wspace=0.25)
    save(fig, "fig21-rope.svg")


# ================================================================
# 图 23-1  全书结构
# ================================================================


FIGURES = ['fig_rope']