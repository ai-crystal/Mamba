# -*- coding: utf-8 -*-
"""CH11 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_nplr():
    fig, ax = canvas(16.0, 0.30)
    n = 18
    ii, jj = np.mgrid[0:n, 0:n]
    A = np.where(ii > jj, -np.sqrt((2 * ii + 1) * (2 * jj + 1)),
                 np.where(ii == jj, -(ii + 1.0), 0.0))
    A = A / np.abs(A).max()
    S = np.where(ii > jj, -0.5 * np.sqrt((2 * ii + 1) * (2 * jj + 1)),
                 np.where(ii < jj, 0.5 * np.sqrt((2 * ii + 1) * (2 * jj + 1)),
                          -0.5))
    S = S / np.abs(S).max()
    P = np.sqrt(np.arange(n) + 0.5)[:, None]
    PP = (P @ P.T) / (P @ P.T).max()

    items = [(A, "HiPPO 矩阵 $A$"), (S, "$A^{(N)}$（正规部分）"),
             (PP, "$PP^{\\top}$（秩 1）")]
    x = 3.0
    for k, (mat, title) in enumerate(items):
        ax.imshow(mat, cmap="RdBu_r", vmin=-1, vmax=1,
                  extent=[x, x + 15, 34, 76], aspect="auto")
        ax.text(x + 7.5, 80, title, ha="center", va="bottom", fontsize=8, color=INK)
        x += 15
        if k == 0:
            ax.text(x + 3.5, 55, "$-$", fontsize=15, color=MUTED, ha="center", va="center")
            x += 7.0
        elif k == 1:
            ax.text(x + 3.5, 55, "$=$", fontsize=15, color=MUTED, ha="center", va="center")
            x += 7.0

    ax.text(3, 22, "$A=A^{(N)}-PP^{\\top}$，其中 $r=1$（HiPPO-LegS）或 $r=2$（LegT / LagT）",
            ha="left", va="top", fontsize=7.6, color=BLUE)
    save(fig, "fig10-nplr.svg")


FIGURES = ['fig_nplr']
