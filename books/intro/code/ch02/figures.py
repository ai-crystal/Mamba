# -*- coding: utf-8 -*-
"""CH02 插图：压缩与重建。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_compress():
    t = np.linspace(0, 1, 600)
    f = (np.sin(2 * np.pi * 1.1 * t) * 0.6
         + np.sin(2 * np.pi * 2.7 * t + 0.8) * 0.3
         + 0.12 * np.sin(2 * np.pi * 7.3 * t))

    x = 2 * t - 1
    A = np.stack([np.polynomial.legendre.Legendre.basis(k)(x) for k in range(6)], axis=1)
    coef, *_ = np.linalg.lstsq(A, f, rcond=None)
    rec = A @ coef

    fig, axes = plt.subplots(3, 1, figsize=(16.0 / 2.54, 7.4 / 2.54),
                             gridspec_kw={"height_ratios": [2.6, 2.0, 2.6]})

    ax = axes[0]
    ax.plot(t, f, color=INK, lw=1.2)
    ax.set_ylabel("原始信号", fontsize=8, labelpad=6)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    ax = axes[1]
    ax.axis("off")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1.45)
    for k, c in enumerate(coef):
        box(ax, k + 0.12, 0.28, 0.76, 0.62, f"{c:+.2f}", fc="#fdf3ee", ec=ORANGE,
            fs=7.4, lw=0.8, radius=0.05)
    ax.text(3.0, 1.28, "压缩成六个系数", ha="center", va="center",
            fontsize=7.4, color=ORANGE)

    ax = axes[2]
    ax.plot(t, f, color=MUTED, lw=0.9, ls="--", label="原始")
    ax.plot(t, rec, color=BLUE, lw=1.4, label="重建")
    ax.set_ylabel("重建", fontsize=8, labelpad=6)
    ax.set_xlabel("时间", fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.95, 0.95)
    ax.set_yticks([])
    ax.legend(fontsize=7, frameon=False, loc="upper right", ncol=2, handlelength=2.0)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for a in axes:
        a.tick_params(labelsize=7, colors=MUTED)
    fig.subplots_adjust(hspace=0.34, top=0.97, bottom=0.12, left=0.17, right=0.97)
    save(fig, "fig02-compress.svg")


FIGURES = ["fig_compress"]
