# -*- coding: utf-8 -*-
"""CH03 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_layer_interface():
    fig, ax = canvas(16.0, 0.42)
    box(ax, 2, 40, 14, 22, "输入\n$(B,L,H)$", fc="#f7f7f7", fs=7.4)
    box(ax, 24, 40, 30, 22, "H 个独立 SSM（每个 $N$ 维）\n逐通道卷积", fc="#eef3f8",
        fs=7.4, ec=BLUE)
    box(ax, 62, 40, 16, 22, "逐位置\n线性混合", fc="white", fs=7.4, ec=INK)
    box(ax, 84, 40, 14, 22, "非线性\n$\\sigma$", fc="white", fs=7.4, ec=INK)
    arrow(ax, 16.4, 51, 23.6, 51, color=BLUE)
    arrow(ax, 54.4, 51, 61.6, 51)
    arrow(ax, 78.4, 51, 83.6, 51)
    label(ax, 50, 28, "输出 $(B,L,H)$，与 RNN / CNN / Transformer 的层接口一致", fs=7.2, color=MUTED)
    save(fig, "fig24-layer.svg")


FIGURES = ['fig_layer_interface']