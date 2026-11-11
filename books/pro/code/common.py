#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全书插图生成脚本。

所有图都是按正文含义用 matplotlib 重绘的矢量图（SVG），不是截图、也不是位图生成。
运行：python figures/src/make_figures.py
输出：figures/*.svg
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle, Arc
from matplotlib.lines import Line2D

CODE = Path(__file__).resolve().parent
BOOK = CODE.parent
IMAGES = BOOK / "images"
CURRENT = IMAGES / "front"

# ---------------------------------------------------------------- 样式
INK = "#1f2933"
MUTED = "#7b8794"
LIGHT = "#e4e7eb"
BLUE = "#3d6b9e"
ORANGE = "#c0603c"
GREEN = "#3f7d63"
PURPLE = "#6b5b95"

plt.rcParams.update({
    "font.family": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "font.size": 9,
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",
    "svg.fonttype": "path",
    "figure.dpi": 100,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
    "axes.linewidth": 0.8,
})


def canvas(w=16.0, ratio=0.6):
    """坐标系固定为 100×100，ratio 控制画布高宽比。"""
    fig, ax = plt.subplots(figsize=(w / 2.54, w * ratio / 2.54))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    """把图保存为 PNG，文件名去掉 .svg 后缀。"""
    path = CURRENT / Path(name).with_suffix(".png").name
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="png", dpi=200, transparent=False, facecolor="white")
    plt.close(fig)
    print("  ->", path.relative_to(BOOK))


def box(ax, x, y, w, h, text, fc="white", ec=INK, lw=0.9, fs=8.5,
        color=INK, radius=1.2, style="round", weight="normal", z=2, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"{style},pad=0,rounding_size={radius}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=z, alpha=alpha)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=color, zorder=z + 1, weight=weight,
                linespacing=1.35)
    return p


def arrow(ax, x1, y1, x2, y2, color=INK, lw=0.9, style="-|>", ls="-",
          rad=0.0, shrinkA=1, shrinkB=1, z=3, ms=6):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=ms, linewidth=lw, color=color,
                        linestyle=ls, shrinkA=shrinkA, shrinkB=shrinkB,
                        connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(a)


def label(ax, x, y, text, fs=8, color=INK, ha="center", va="center",
          weight="normal", z=5, bbox=None, rotation=0):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
            weight=weight, zorder=z, rotation=rotation, bbox=bbox,
            linespacing=1.35)


def heat(ax, mat, cmap, vmin=None, vmax=None, origin="upper", extent=None):
    ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin,
              interpolation="nearest", extent=extent, aspect="equal")


