# -*- coding: utf-8 -*-
"""CH17 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_selective():
    n = 48
    rng = np.random.default_rng(3)
    ii, jj = np.mgrid[0:n, 0:n]
    lti = np.where(ii >= jj, np.exp(-(ii - jj) / 9.0), 0.0)
    g = np.exp(-np.abs(ii - jj) / 9.0) * (0.25 + 0.75 * rng.random((n, n)))
    s6 = np.where(ii >= jj, g, 0.0)

    fig = plt.figure(figsize=(16.2 / 2.54, 5.4 / 2.54))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1], wspace=0.22)

    ax = fig.add_subplot(gs[0, 0])
    ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    tokens = ["a", "", "b", "", "", "c", "", "d", "", "e"]
    for i, t in enumerate(tokens):
        color = "#c0603c" if t else "#eef0f2"
        txt = t if t else ""
        ax.add_patch(Rectangle((i * 0.95 + 0.1, 6.4), 0.75, 0.75, fc=color, ec="none"))
        ax.text(i * 0.95 + 0.47, 6.78, txt, ha="center", va="center",
                color="white" if t else "none", fontsize=8)
    for i, t in enumerate(["a", "b", "c", "d", "e"]):
        ax.add_patch(Rectangle((i * 0.95 + 2.2, 3.6), 0.75, 0.75, fc="#c0603c", ec="none"))
        ax.text(i * 0.95 + 2.58, 3.98, t, ha="center", va="center", color="white", fontsize=8)
    ax.annotate("", xy=(2.2, 5.2), xytext=(0.3, 6.2),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                connectionstyle="arc3,rad=-0.25"))
    ax.text(5.0, 8.4, "输入：要记的 token 位置随机", ha="center", fontsize=8)
    ax.text(5.0, 2.4, "输出：按原顺序复述", ha="center", fontsize=8)
    ax.text(5.0, 0.6, "间距不是常数 → 固定卷积核必然失败", ha="center",
            fontsize=7.4, color=ORANGE)

    for ax, mat, title, note in [
        (fig.add_subplot(gs[0, 1]), lti, "线性时不变", "每条对角线相同\n权重与内容无关"),
        (fig.add_subplot(gs[0, 2]), s6, "选择性 SSM", "每一行都不一样\n权重由输入决定")]:
        ax.imshow(mat, cmap="Blues", vmin=0, vmax=1, interpolation="nearest")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlabel(note, fontsize=7.2, color=MUTED, labelpad=4, linespacing=1.5)
        for s in ax.spines.values():
            s.set_color(MUTED); s.set_linewidth(0.6)
    save(fig, "fig17-01-selective.svg")


# ================================================================
# 图 13-1  S4 与 S6 的张量形状
# ================================================================


FIGURES = ['fig_selective']