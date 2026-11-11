# -*- coding: utf-8 -*-
"""CH04 插图：多项式基与逼近。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_hippo_basis():
    t = np.linspace(0, 1, 500)
    f = np.exp(-1.6 * t) * np.cos(6 * t) + 0.25
    x = 2 * t - 1

    fig, axes = plt.subplots(1, 2, figsize=(16.0 / 2.54, 4.8 / 2.54))

    ax = axes[0]
    for k in range(5):
        ax.plot(t, np.polynomial.legendre.Legendre.basis(k)(x), lw=1.0,
                label=f"$P_{k}$")
    ax.set_xlim(0, 1)
    ax.set_ylabel("基函数", fontsize=8, labelpad=3)
    ax.legend(fontsize=7, frameon=False, ncol=5, loc="lower center",
              bbox_to_anchor=(0.5, -0.34), handlelength=1.6, columnspacing=1.1)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    ax = axes[1]
    ax.plot(t, f, color=INK, lw=1.6, label="输入")
    for n, ls in [(2, (0, (4, 2))), (4, (0, (2, 1.4))), (8, "-")]:
        A = np.stack([np.polynomial.legendre.Legendre.basis(k)(x) for k in range(n)], axis=1)
        coef, *_ = np.linalg.lstsq(A, f, rcond=None)
        ax.plot(t, A @ coef, lw=1.0, ls=ls, label=f"{n} 项")
    ax.set_xlim(0, 1)
    ax.set_xlabel("时间", fontsize=8)
    ax.set_ylabel("逼近", fontsize=8, labelpad=3)
    ax.legend(fontsize=7, frameon=False, ncol=2, loc="upper right")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    fig.subplots_adjust(wspace=0.25, bottom=0.26, left=0.10, right=0.97)
    save(fig, "fig03-hippo.svg")


FIGURES = ["fig_hippo_basis"]
