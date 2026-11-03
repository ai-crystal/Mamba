# -*- coding: utf-8 -*-
"""CH01 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_matrix_mixers():
    n = 40
    ii, jj = np.mgrid[0:n, 0:n]
    lower = (ii >= jj).astype(float)

    # (a) 因果卷积：Toeplitz，每条对角线相同
    conv = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i >= j:
                conv[i, j] = math.exp(-(i - j) / 8.0) * (0.6 + 0.4 * math.cos((i - j) / 3.0))
    # (b) LTI SSM：同样的 Toeplitz，但由低维状态生成（结构与卷积同族）
    ssm = conv.copy()
    # (c) 选择性 SSM：权重随位置变化（行内模式不再平移不变）
    rng = np.random.default_rng(7)
    gain = np.exp(-np.abs(ii - jj) / 7.0) * (0.55 + 0.45 * rng.random((n, n)))
    sel = np.where(ii >= jj, gain, 0.0)
    # (d) 注意力：下三角稠密，行归一化
    q = rng.normal(size=(n, 16))
    k = rng.normal(size=(n, 16))
    att = (q @ k.T) / 4.0
    att = np.where(ii >= jj, att, -np.inf)
    att = np.exp(att - att.max(axis=1, keepdims=True))
    att = att / att.sum(axis=1, keepdims=True)

    panels = [
        (conv, "因果卷积", r"$M_{ji}=w_{j-i}$"),
        (ssm, "线性递推（SSM）", r"$M_{ji}=c_j^{\top}A^{j-i}b_i$"),
        (sel, "选择性 SSM", r"$M_{ji}=c_j^{\top}\!\prod_{k}A_k\,b_i$"),
        (att, "自注意力", r"$M_{ji}\propto e^{q_j^{\top}k_i}$"),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(16.4 / 2.54, 4.6 / 2.54))
    for ax, (mat, title, formula) in zip(axes, panels):
        ax.imshow(mat, cmap="Blues", interpolation="nearest", vmin=0,
                  vmax=max(1e-9, mat.max()))
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color(MUTED); s.set_linewidth(0.6)
        ax.set_xlabel(formula, fontsize=8, color=BLUE, labelpad=4)
    fig.subplots_adjust(wspace=0.18, bottom=0.2)
    save(fig, "fig01-matrix-mixers.svg")


# ================================================================
# 图 2-1  连续 / 递归 / 卷积三视图
# ================================================================


FIGURES = ['fig_matrix_mixers']