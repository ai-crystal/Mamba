# -*- coding: utf-8 -*-
"""CH22 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_semiseparable():
    n, q = 24, 8
    rng = np.random.default_rng(11)
    M = np.zeros((n, n))
    for j in range(n):
        for i in range(n):
            if j >= i:
                M[j, i] = math.exp(-(j - i) / 6.0) * (0.5 + 0.5 * rng.random())
    fig, ax = plt.subplots(figsize=(9.8 / 2.54, 8.4 / 2.54))
    ax.imshow(M, cmap="Blues", interpolation="nearest")
    for k in range(0, n, q):
        ax.add_patch(Rectangle((k - 0.5, k - 0.5), q, q, fill=False, ec=ORANGE, lw=1.0))
    ax.add_patch(Rectangle((-0.35, q - 0.35), q - 0.3, q - 0.3, fill=False, ec=GREEN,
                           lw=1.3, ls=(0, (4, 2))))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel(r"输入位置 $i$", fontsize=7.5)
    ax.set_ylabel(r"输出位置 $j$", fontsize=7.5)
    for s in ax.spines.values():
        s.set_color(MUTED); s.set_linewidth(0.6)
    save(fig, "fig22-01-semiseparable.svg")


# ================================================================
# 图 16-1  两种缩约顺序
# ================================================================


FIGURES = ['fig_semiseparable']