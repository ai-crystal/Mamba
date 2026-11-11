# -*- coding: utf-8 -*-
"""CH31 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_arith():
    fig, ax = plt.subplots(figsize=(16.0 / 2.54, 4.8 / 2.54))
    names = ["SISO 解码", "MIMO R=4", "MIMO R=16", "H100 bf16 矩阵乘"]
    vals = [2.5, 10, 40, 295]
    cols = [ORANGE, GREEN, GREEN, MUTED]
    ax.barh(range(len(vals)), vals, color=cols, height=0.55)
    ax.set_xscale("log")
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(names, fontsize=7.6)
    ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v * 1.15, i, f"{v:g}", va="center", fontsize=7.6, color=INK)
    ax.set_xlabel("算术强度（FLOPs / 字节）", fontsize=8)
    ax.set_xlim(1, 1200)
    ax.axvline(295, color=MUTED, lw=0.8, ls="--")
    ax.text(300, -0.5, "硬件脊点", fontsize=7, color=MUTED)
    ax.grid(axis="x", alpha=0.25, lw=0.5, which="both")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)
    save(fig, "fig18-arith.svg")


# ================================================================
# 图 20-1  Mamba-2 与 Mamba-3 的掩码
# ================================================================


FIGURES = ['fig_arith']