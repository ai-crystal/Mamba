# -*- coding: utf-8 -*-
"""CH09 插图：固定权重与按内容选择。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_selection():
    n = 30
    pos = [3, 9, 16, 22, 27]
    signal = np.full(n, 0.25)
    signal[pos] = 1.0

    fig, axes = plt.subplots(2, 1, figsize=(16.0 / 2.54, 4.4 / 2.54), sharex=True,
                             gridspec_kw={"height_ratios": [1.1, 1.6]})

    ax = axes[0]
    ax.bar(np.arange(n), signal, color=["#c0603c" if i in pos else "#dde3ea" for i in range(n)],
           width=0.72)
    ax.set_ylim(0, 1.35)
    ax.set_yticks([])
    ax.text(0.01, 0.90, "输入", transform=ax.transAxes, fontsize=8,
            color=MUTED, va="top")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    ax = axes[1]
    fixed = np.exp(-(n - 1 - np.arange(n)) / 9.0) * 0.55 + 0.18
    select = np.zeros(n) + 0.18
    for p in pos:
        select[p] = 1.0
    ax.plot(np.arange(n), fixed, color=MUTED, lw=1.3, label="固定权重")
    ax.plot(np.arange(n), select, color=BLUE, lw=1.3, marker="o", ms=2.6,
            label="按内容选择")
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    ax.set_xlabel("位置", fontsize=8)
    ax.legend(fontsize=7, frameon=False, ncol=2, loc="upper left")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    fig.subplots_adjust(hspace=0.22, left=0.06, right=0.98)
    save(fig, "fig09-01-selection.svg")


FIGURES = ["fig_selection"]
