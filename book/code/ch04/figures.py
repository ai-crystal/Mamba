# -*- coding: utf-8 -*-
"""CH04 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_hippo_measures():
    fig, axes = plt.subplots(1, 3, figsize=(16.0 / 2.54, 4.2 / 2.54),
                             sharey=True)
    t = 1.0
    theta = 0.45

    ax = axes[0]
    ax.add_patch(Rectangle((t - theta, 0), theta, 1.0, fc=BLUE, alpha=0.28, ec=BLUE, lw=0.9))
    ax.axvspan(0, t - theta, color=LIGHT, alpha=0.6, lw=0)
    ax.annotate("", xy=(t - theta, 1.12), xytext=(t, 1.12),
                arrowprops=dict(arrowstyle="<|-|>", lw=0.7, color=MUTED))
    ax.text((t - theta + t) / 2, 1.20, r"$\theta$", ha="center", fontsize=8, color=MUTED)

    ax = axes[1]
    x = np.linspace(0, t, 400)
    ax.fill_between(x, np.exp(-(t - x) * 6), color=GREEN, alpha=0.25, lw=0)
    ax.plot(x, np.exp(-(t - x) * 6), color=GREEN, lw=1.2)

    ax = axes[2]
    ax.add_patch(Rectangle((0, 0), t, 1.0, fc=ORANGE, alpha=0.22, ec=ORANGE, lw=0.9))

    for ax in axes:
        ax.set_xlim(0, 1.02)
        ax.set_ylim(0, 1.32)
        ax.set_xlabel(r"过去的时间 $x$", fontsize=7.5)
        ax.set_xticks([0, t])
        ax.set_xticklabels(["0", r"$t$"], fontsize=7)
        ax.set_yticks([])
        for s in ["top", "right", "left"]:
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color(MUTED)
        ax.tick_params(colors=MUTED, length=2)
    axes[0].set_ylabel("权重密度", fontsize=7.5, color=MUTED)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig04-hippo-measures.svg")


# ================================================================
# 图 4-2  HiPPO 的计算流程
# ================================================================


FIGURES = ['fig_hippo_measures']