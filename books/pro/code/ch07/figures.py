# -*- coding: utf-8 -*-
"""CH07 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_lssl_views():
    fig, axes = plt.subplots(1, 3, figsize=(16.2 / 2.54, 4.4 / 2.54))
    L, H = 9, 4

    for ax, title, note in zip(
            axes,
            ["递归：竖着切", "卷积：横着切", "连续：没有“步”"],
            ["固定时间步，逐列推进\n每步 $O(N)$，与已有长度无关",
             "固定通道，整行一次算完\nFFT，$O(L\\log L)$，可并行",
             "输入是函数，输出是函数\n$\\Delta$ 只是采样参数"]):
        ax.set_xlim(0, L)
        ax.set_ylim(0, H + 1)
        for i in range(L):
            for j in range(H):
                ax.add_patch(Rectangle((i + 0.08, j + 0.08), 0.84, 0.84,
                                       fc="white", ec=LIGHT, lw=0.8))
        ax.set_xticks([]); ax.set_yticks([])
        ax.text(L / 2, -0.55, note, ha="center", va="top", fontsize=7, color=MUTED)
        for s in ax.spines.values():
            s.set_visible(False)

    ax = axes[0]
    ax.add_patch(Rectangle((2.05, 0.05), 0.9, H + 0.9, fc=ORANGE, alpha=0.22, ec=ORANGE, lw=1.1))
    arrow(ax, 2.5, H + 1.15, 4.6, H + 1.15, color=ORANGE, lw=0.9)

    ax = axes[1]
    ax.add_patch(Rectangle((0.05, 2.05), L + 0.9, 0.9, fc=BLUE, alpha=0.18, ec=BLUE, lw=1.1))

    ax = axes[2]
    xs = np.linspace(0, L, 100)
    ax.plot(xs, 2 + 1.2 * np.sin(xs * 0.9) * np.exp(-xs / 6), color=GREEN, lw=1.3)
    ax.set_ylim(-1.0, H + 1.2)
    save(fig, "fig07-01-lssl-views.svg")


# ================================================================
# 图 8-1  Picard 迭代与深 LSSL
# ================================================================


FIGURES = ['fig_lssl_views']