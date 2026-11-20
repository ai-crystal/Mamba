# -*- coding: utf-8 -*-
"""CH02 插图。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import *  # noqa: F401,F403


def fig_ssm_views():
    fig, ax = canvas(16.2, 0.86)

    # 连续
    box(ax, 3, 62, 26, 20, "", fc="#fbfbfb")
    label(ax, 16, 78.5, "连续视图", fs=9, weight="bold")
    label(ax, 16, 71, r"$\dot x(t)=Ax(t)+Bu(t)$", fs=8.5, color=BLUE)
    label(ax, 16, 65.5, r"$y(t)=Cx(t)+Du(t)$", fs=8.5, color=BLUE)

    # 递归
    box(ax, 37, 62, 26, 20, "", fc="#fbfbfb")
    label(ax, 50, 78.5, "递归视图", fs=9, weight="bold")
    label(ax, 50, 71, r"$x_k=\bar A x_{k-1}+\bar B u_k$", fs=8.5, color=BLUE)
    label(ax, 50, 65.5, r"$y_k=Cx_k$", fs=8.5, color=BLUE)

    # 卷积
    box(ax, 71, 62, 26, 20, "", fc="#fbfbfb")
    label(ax, 84, 78.5, "卷积视图", fs=9, weight="bold")
    label(ax, 84, 71, r"$\bar K=(\bar C\bar B,\ \bar C\bar A\bar B,\dots)$", fs=8)
    label(ax, 84, 65.5, r"$y=\bar K * u$", fs=8.5, color=BLUE)

    arrow(ax, 29.4, 72, 36.6, 72)
    label(ax, 33, 57, r"离散化 $\Delta$", fs=7, color=MUTED)

    arrow(ax, 63.4, 72, 70.6, 72)
    label(ax, 67, 57, "展开", fs=7, color=MUTED)

    # 用途
    for x, t, c in [(16, "处理非均匀采样\n改变采样率", GREEN),
                    (50, "推理：$O(N)$/步\n常量内存", ORANGE),
                    (84, "训练：FFT\n完全并行", PURPLE)]:
        box(ax, x - 10, 40, 20, 13, t, fc="white", ec=c, lw=0.8, fs=7.4, color=c)
        arrow(ax, x, 61.4, x, 53.6, color=c, lw=0.8)

    # 共同瓶颈
    box(ax, 21, 12, 58, 16, "", fc="#f7f4ef", ec=ORANGE, lw=0.9)
    label(ax, 50, 23.5, "三个视图的共同瓶颈", fs=8.8, weight="bold", color=ORANGE)
    label(ax, 50, 16.5, r"算出卷积核需要 $\bar A$ 的幂：朴素 $O(N^2L)$ 时间、$O(NL)$ 空间",
          fs=7.4)
    arrow(ax, 50, 39.4, 50, 28.6, color=ORANGE, lw=0.8, ls=(0, (3, 2)))
    save(fig, "fig02-01-ssm-views.svg")


# ================================================================
# 图 2-2  四种离散化对同一连续核的逼近
# ================================================================


def fig_discretization():
    lam = -0.9 + 1.7j
    A = np.array([[lam.real, -lam.imag], [lam.imag, lam.real]])

    t = np.linspace(0, 12, 800)
    cont = np.exp(lam * t)

    dt = 0.45
    ks = np.arange(0, 27)
    tk = ks * dt

    def disc(kind):
        if kind == "euler":
            Abar = np.eye(2) + dt * A
        elif kind == "beuler":
            Abar = np.linalg.inv(np.eye(2) - dt * A)
        elif kind == "bilinear":
            Abar = np.linalg.inv(np.eye(2) - dt * A / 2) @ (np.eye(2) + dt * A / 2)
        else:  # zoh
            Abar = np.eye(2) * math.exp(dt * lam.real) @ np.array(
                [[math.cos(dt * lam.imag), -math.sin(dt * lam.imag)],
                 [math.sin(dt * lam.imag), math.cos(dt * lam.imag)]])
        out = []
        v = np.array([1.0, 0.0])
        for _ in ks:
            out.append(v[0])
            v = Abar @ v
        return np.array(out)

    fig, axes = plt.subplots(1, 2, figsize=(16.2 / 2.54, 6.0 / 2.54))

    ax = axes[0]
    ax.plot(t, cont.real, color=INK, lw=1.4, label=r"连续核 $\mathrm{Re}\,Ce^{tA}B$")
    styles = [("euler", "前向欧拉", ORANGE, (0, (4, 2))),
              ("beuler", "后向欧拉", GREEN, (0, (1, 1.5))),
              ("bilinear", "双线性", BLUE, (0, (5, 1.6, 1, 1.6))),
              ("zoh", "ZOH", PURPLE, (0, (6, 2)))]
    for kind, name, col, ls in styles:
        ax.plot(tk, disc(kind), color=col, lw=1.0, ls=ls, marker="o", ms=2.4,
                label=name)
    ax.set_xlabel(r"时间 $t$", fontsize=8)
    ax.set_ylabel("核的值", fontsize=8)
    ax.grid(alpha=0.25, lw=0.5)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    ax = axes[1]
    dts = np.linspace(0.01, 1.2, 400)
    err = {}
    for kind, name, col, ls in styles:
        e = []
        for d in dts:
            globals()["dt"] = d
            Abar = {
                "euler": np.eye(2) + d * A,
                "beuler": np.linalg.inv(np.eye(2) - d * A),
                "bilinear": np.linalg.inv(np.eye(2) - d * A / 2) @ (np.eye(2) + d * A / 2),
                "zoh": np.array([[math.cos(d * lam.imag), -math.sin(d * lam.imag)],
                                 [math.sin(d * lam.imag), math.cos(d * lam.imag)]])
                * math.exp(d * lam.real),
            }[kind]
            exact = np.array([[math.cos(d * lam.imag), -math.sin(d * lam.imag)],
                              [math.sin(d * lam.imag), math.cos(d * lam.imag)]]) * math.exp(d * lam.real)
            e.append(np.linalg.norm(Abar - exact) / max(1e-12, np.linalg.norm(exact)))
        err[kind] = np.array(e)
    globals()["dt"] = 0.45
    for kind, name, col, ls in styles:
        ax.loglog(dts, err[kind] + 1e-12, color=col, lw=1.1, ls=ls, label=name)
    ax.set_xlabel(r"步长 $\Delta$", fontsize=8)
    ax.set_ylabel("相对误差", fontsize=8)
    # 两张图共用左下角图例，右图不再重复标注，避免线压在文字上
    ax.grid(alpha=0.25, which="both", lw=0.5)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=7)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, fontsize=6.6, frameon=False, ncol=5,
               loc="lower center", bbox_to_anchor=(0.5, -0.02),
               columnspacing=1.0, handlelength=1.8)
    fig.subplots_adjust(wspace=0.28, bottom=0.3)
    save(fig, "fig02-02-discretization.svg")


# ================================================================
# 图 4-1  三种 HiPPO 测度
# ================================================================


FIGURES = ['fig_ssm_views', 'fig_discretization']