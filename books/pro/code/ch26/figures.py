# -*- coding: utf-8 -*-
"""CH26 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_heads():
    fig, ax = canvas(16.0, 0.5)
    H = 4
    patterns = [
        ("MHA / MHS", [1, 1, 1], "三者都独立"),
        ("MQA / MCS", [1, 1, H], r"$C$ 独立"),
        ("MKA / MES", [1, H, 1], r"$B$ 独立"),
        ("MVA / MIS", [H, 1, 1], r"$X$ 独立"),
    ]
    for k, (name, cfg, note) in enumerate(patterns):
        x0 = 3 + k * 24.5
        label(ax, x0 + 9, 92, name, fs=8.4, weight="bold")
        for r, (cnt, lab) in enumerate(zip(cfg, [r"$X$", r"$B$", r"$C$"])):
            cw = 12.0 / cnt
            for c in range(cnt):
                box(ax, x0 + c * cw + (cw - 4.4) / 2, 66 - r * 13, 4.4, 9, "",
                    fc="#eef3f8" if cnt > 1 else "#f2f2f2",
                    ec=BLUE if cnt > 1 else MUTED, lw=0.7)
            label(ax, x0 - 1.4, 70.5 - r * 13, lab, fs=7.2, ha="right", color=MUTED)
        label(ax, x0 + 9, 18, note, fs=6.8, color=MUTED)
    label(ax, 50, 4, "蓝：该参数在 head 间独立；灰：跨 head 共享", fs=7, color=MUTED)
    save(fig, "fig17-heads.svg")


# ================================================================
# 图 19-1  算术强度
# ================================================================


FIGURES = ['fig_heads']