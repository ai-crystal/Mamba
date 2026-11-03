# -*- coding: utf-8 -*-
"""前言与全书结构图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_book_map():
    fig, ax = canvas(16.0, 0.5)
    parts = [
        ("一 背景", ["三难困境", "连续 SSM"], 1.5),
        ("二 HiPPO", ["记忆＝投影"], 13.5),
        ("三 LSSL", ["三视图", "非正规"], 25.5),
        ("四 S4", ["DPLR＋柯西核", "S4D"], 37.5),
        ("五 S5", ["并行扫描", "门控生态"], 49.5),
        ("六 Mamba-1", ["选择性", "融合扫描"], 61.5),
        ("七 Mamba-2", ["半可分矩阵", "SSD"], 73.5),
        ("八 Mamba-3", ["梯形＋RoPE", "MIMO"], 85.5),
    ]
    for name, items, x in parts:
        box(ax, x, 52, 11, 30, "", fc="#fbfbfb", ec=LIGHT, lw=0.9)
        label(ax, x + 5.5, 76, name, fs=7.2, weight="bold")
        for i, it in enumerate(items):
            label(ax, x + 5.5, 66 - i * 8, it, fs=6.2, color=MUTED)
    for k in range(len(parts) - 1):
        arrow(ax, parts[k][2] + 11.2, 67, parts[k + 1][2] - 0.3, 67, lw=0.7, ms=5)
    label(ax, 50, 42, "主线：压缩什么 → 如何压缩得动 → 策略依赖内容 → 用矩阵乘压缩 → 更精确、更省带宽",
          fs=7.2)
    label(ax, 50, 28, "每一代要解决的问题，都来自上一代留下的具体失败模式", fs=7.2, color=MUTED)
    label(ax, 50, 14, "第 33~35 章：实现、训练实践、开放问题", fs=7.2, color=BLUE)
    save(fig, "fig22-book-map.svg")




# ================================================================
# 图 24-1  Mamba block 数据流
# ================================================================


FIGURES = ['fig_book_map']