# -*- coding: utf-8 -*-
"""CH29 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_masks():
    T = 26
    ii, jj = np.mgrid[0:T, 0:T]
    a = np.exp(-0.18 * (ii - jj))
    L2 = np.where(ii >= jj, a, 0.0)

    beta = 0.25
    L3 = np.zeros((T, T))
    for i in range(T):
        for j in range(T):
            if i == j:
                L3[i, j] = 0.75
            elif i == j + 1:
                L3[i, j] = beta
            elif i > j + 1:
                L3[i, j] = a[i, j] * (0.75 * a[j, j] + beta)
    L3 = L3 / L3.max()

    fig, axes = plt.subplots(1, 2, figsize=(13.2 / 2.54, 5.2 / 2.54))
    for ax, mat, title, note in [
        (axes[0], L2, "Mamba-2：对角掩码", r"$L_{ji}=a_{j:i}$"),
        (axes[1], L3, "Mamba-3：1-SS × 2-band", r"$L=\mathrm{1SS}(\alpha)\cdot\mathrm{band}(\beta,\gamma)$")]:
        ax.imshow(mat, cmap="Blues", interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel(note, fontsize=7.4, color=MUTED, labelpad=4)
        for s in ax.spines.values():
            s.set_color(MUTED); s.set_linewidth(0.6)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig19-masks.svg")


# ================================================================
# 图 21-1  注意力层比例（Mamba-2 论文 Table 2 数据）
# ================================================================


FIGURES = ['fig_masks']