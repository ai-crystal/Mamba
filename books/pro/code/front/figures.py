# -*- coding: utf-8 -*-
"""前言与全书结构图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_book_map():
    fig, ax = canvas(16.5, 0.5)
    parts = [
        ("一", "背景", ["三难困境", "连续 SSM"]),
        ("二", "HiPPO", ["记忆＝投影", "非正规"]),
        ("三", "LSSL", ["三视图", "算不动"]),
        ("四", "S4", ["DPLR", "S4D"]),
        ("五", "S5", ["并行扫描", "门控生态"]),
        ("六", "Mamba-1", ["选择性", "融合扫描"]),
        ("七", "Mamba-2", ["半可分矩阵", "SSD"]),
        ("八", "Mamba-3", ["梯形离散", "RoPE＋MIMO"]),
    ]
    w, gap, x0 = 10.8, 1.75, 0.5
    step = w + gap
    for i, (num, name, items) in enumerate(parts):
        x = x0 + i * step
        box(ax, x, 46, w, 38, "", fc="#fbfbfb", ec=LIGHT, lw=0.9, radius=0.8)
        label(ax, x + w / 2, 79, num, fs=6.4, color=MUTED)
        label(ax, x + w / 2, 72, name, fs=6.2, weight="bold")
        for j, it in enumerate(items):
            label(ax, x + w / 2, 62 - j * 8, it, fs=5.4, color=MUTED)
        if i:
            arrow(ax, x - gap + 0.45, 65, x - 0.5, 65, lw=0.7, ms=5, shrinkA=0, shrinkB=0)
    label(ax, 50, 38, "主线：压缩什么 → 怎么压缩得动 → 压缩策略依赖内容 → 用矩阵乘压缩 → 更精确、更省带宽",
          fs=7.0)
    label(ax, 50, 26, "每一代要解决的问题，都来自上一代留下的具体失败模式", fs=7.0, color=MUTED)
    label(ax, 50, 13, "第九篇（第 33~35 章）：从零实现、训练实践、开放问题", fs=7.0, color=BLUE)
    save(fig, "fig00-01-book-map.svg")


FIGURES = ["fig_book_map"]
