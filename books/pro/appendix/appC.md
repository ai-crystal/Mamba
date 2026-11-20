# 附录 C 公式速查与符号表

本附录是"做题时翻书"用的，分三部分：符号表（按体系分组）、公式速查卡（按模型分组）、五模型横向对比表。每张公式卡给出"一行核心形式 + 一句说明 + 来源（论文与式号）"。

两条使用提醒：

1. 式号以原文为准。本附录的式号来自论文公开版本，但 `pdftotext` 抽取会造成式号错位；若与原文不一致，请以原文 PDF 为准。
2. 符号存在体系切换。第 1～16 章沿用经典控制论记号（输入 $u$、状态 $x$），第 17 章起切换为 Mamba 论文记号（输入 $x$、状态 $h$）。两套记号在同一张表里并排时，先看子表标题。

符号约定见本节表格；术语的中英文对照见[附录 B](appB.md)。

---

## C.1 全书符号表

三组符号表分别对应三层语境：通用序列记号（全书通用）、S4 体系连续时间记号（第 2～16 章）、Mamba 体系记号（第 17 章起）。先确定正在读哪一章，再查对应的子表，否则很容易把同一个字母的两种含义搞混。

### C.1.1 通用序列与模型记号

| 符号 | 含义 | 形状 | 首次出现 |
|---|---|---|---|
| $L$ / $T$ | 序列长度（同一章内统一；$T$ 主要用于 Mamba-2/3 的矩阵视角） | 标量 | [第 1 章](../chapters/ch01.md) |
| $B$ | batch size | 标量 | [第 1 章](../chapters/ch01.md) |
| $D$ / $H$ | 模型维度 / 隐藏通道数（同一章内统一） | 标量 | [第 1 章](../chapters/ch01.md) |
| $N$ | SSM 状态维度（state size / state expansion factor） | 标量 | [第 2 章](../chapters/ch02.md) |
| $P$ | head 维度（Mamba-2 起） | 标量 | [第 23 章](../chapters/ch23.md) |
| $\mathsf{C}$ | chunk 长度（块分解用，第 25 章起；与输出矩阵 $C$ 靠上下文区分） | 标量 | [第 25 章](../chapters/ch25.md) |
| $R$ | MIMO rank（第 31 章） | 标量 | [第 31 章](../chapters/ch31.md) |
| $u_t$ / $x_t$ | 输入（S4 体系用 $u$；Mamba 体系用 $x$） | 标量或 $\mathbb{R}^{D}$ | [第 2 章](../chapters/ch02.md) |
| $y_t$ | 输出 | 标量或 $\mathbb{R}^{D}$ | [第 2 章](../chapters/ch02.md) |
| $x_t$ / $h_t$ | 潜状态（S4 体系用 $x$；Mamba 体系用 $h$） | $\mathbb{R}^{N}$ | [第 2 章](../chapters/ch02.md) |
| $\Delta$ / $\Delta t$ | 离散化步长（timescale / 时间尺度） | 标量 | [第 2 章](../chapters/ch02.md) |
| $\bar A,\bar B,\bar C,\bar D$ | 离散化后的参数 | 同连续时 | [第 3 章](../chapters/ch03.md) |

> 记号切换提醒：第 1～16 章（S4 体系）用"输入 $u$、状态 $x$"；第 17 章起（Mamba 体系）切换为"输入 $x$、状态 $h$"，并在[第 17 章](../chapters/ch17.md)给出对照表。

### C.1.2 S4 体系：连续时间记号（第 2～16 章）

| 符号 | 含义 | 形状 | 首次出现 |
|---|---|---|---|
| $A$ | 状态转移矩阵（系统矩阵） | $\mathbb{R}^{N\times N}$ | [第 2 章](../chapters/ch02.md) |
| $B$ | 输入矩阵 | $\mathbb{R}^{N\times 1}$ | [第 2 章](../chapters/ch02.md) |
| $C$ | 输出矩阵 | $\mathbb{R}^{1\times N}$ | [第 2 章](../chapters/ch02.md) |
| $D$ | 直通项（feedthrough） | $\mathbb{R}$ | [第 2 章](../chapters/ch02.md) |
| $\Lambda$ | 对角矩阵（DPLR 的对角部分） | $\mathbb{C}^{N\times N}$ | [第 11 章](../chapters/ch11.md) |
| $P,Q$ | 低秩因子 | $\mathbb{C}^{N\times r}$，$r=1$ 或 $2$ | [第 11 章](../chapters/ch11.md) |
| $V$ | 对角化矩阵（Lemma 3.2 中 $V_{ij}=\binom{i+j}{i-j}$） | $\mathbb{C}^{N\times N}$ | [第 10 章](../chapters/ch10.md) |
| $\hat K(z)$ | SSM 生成函数 | $\mathbb{C}$ | [第 12 章](../chapters/ch12.md) |
| $\bar K$ | SSM 卷积核 | $\mathbb{R}^{L}$ | [第 3 章](../chapters/ch03.md) |
| $\mathcal{C}(M,N)$ | 柯西矩阵-向量乘法代价 | 标量 | [第 12 章](../chapters/ch12.md) |

### C.1.3 Mamba 体系记号（第 17 章起）

| 符号 | 含义 | 形状 | 首次出现 |
|---|---|---|---|
| $x_t$ | 输入（Mamba 论文记号） | $\mathbb{R}^{D}$ 或 $\mathbb{R}^{B\times L\times D}$ | [第 17 章](../chapters/ch17.md) |
| $h_t$ | 潜状态（Mamba 论文记号） | $\mathbb{R}^{N}$，扩展后 $\mathbb{R}^{(B,L,D,N)}$ | [第 18 章](../chapters/ch18.md) |
| $\mathring A,\mathring B,\mathring C$ | 连续参数（Mamba-2 论文用 $\mathring A$；Mamba-2/3 正文常省略横线直接写 $A$） | 同前 | [第 24 章](../chapters/ch24.md) |
| $A_t,B_t,C_t,\Delta_t$ | 时间/输入相关的选择性参数 | 带 $L$ 维，如 $\Delta:(B,L,D)$ | [第 18 章](../chapters/ch18.md) |
| $L$ | 掩码矩阵（1-SS 或 decay mask） | $\mathbb{R}^{T\times T}$ | [第 22 章](../chapters/ch22.md) |
| $M$ | 半可分序列变换矩阵 | $\mathbb{R}^{T\times T}$ | [第 22 章](../chapters/ch22.md) |
| $M_{ji}$ | 矩阵元 $C_j^\top A_j\cdots A_{i+1}B_i$（$j$ 行、$i$ 列，$j\ge i$） | 标量 | [第 22 章](../chapters/ch22.md) |
| $G$ | Gram 矩阵 $QK^\top$ | $\mathbb{R}^{T\times T}$ | [第 23 章](../chapters/ch23.md) |
| $Q,K,V$ | 注意力中的查询 / 键 / 值，对应 SSM 的 $C,B,X$ | $\mathbb{R}^{T\times P}$ 等 | [第 24 章](../chapters/ch24.md) |
| $\alpha_t,\beta_t,\gamma_t$ | Mamba-3 指数-梯形离散化系数（$\alpha_t=e^{\Delta_tA_t}$） | 标量 | [第 29 章](../chapters/ch29.md) |
| $\lambda_t$ | 梯形插值的凸组合系数，$\lambda_t\in[0,1]$ | 标量 | [第 29 章](../chapters/ch29.md) |
| $A_t+i\Theta_t$ | 复值 SSM 的（实部 + 虚部）对角参数 | $\mathbb{C}^{N/2}$ | [第 30 章](../chapters/ch30.md) |
| $R(\theta)$ | 二维旋转矩阵 | $\mathbb{R}^{2\times2}$ | [第 30 章](../chapters/ch30.md) |
| $R$ | MIMO rank（与上面的实矩阵记号冲突时按上下文区分） | 标量 | [第 31 章](../chapters/ch31.md) |

最容易混淆的四组符号如下，读书时先确认这四件事，能排除大部分困惑：

1. $B$ 既是 batch size 又是输入矩阵：看形状就能分辨，写成 $B\in\mathbb{R}^{N\times1}$ 或论文里用作大写矩阵时，它是输入矩阵；写成 $B\times L\times D$ 这种张量形状时，它是 batch。
2. $C$ 既是输出矩阵又是 chunk 长度：本书用「输出矩阵 $C$」与「chunk 长度 $\mathsf{C}$」区分，$\mathsf{C}$ 从[第 25 章](../chapters/ch25.md)才开始出现。
3. $D$ 既是模型维度又是直通项：直通项 $D\in\mathbb{R}$ 通常在写 SSM 四元组 $(A,B,C,D)$ 时出现；模型维度 $D$ 则在形状标注里出现。
4. $L$ 既是序列长度又是掩码矩阵：第 22 章起 $L\in\mathbb{R}^{T\times T}$ 专指 1-SS 掩码矩阵，此时序列长度一律写 $T$。

---

## C.2 公式速查卡

下面是全书最值得记住的公式，按模型分组。建议的读法是先看公式卡里的“一行核心形式”，再回到对应章节看推导；速查卡的作用是“提醒”，不是“替代”。

### C.2.1 连续 SSM

$$
x'(t)=Ax(t)+Bu(t),\qquad y(t)=Cx(t)+Du(t),\qquad x\in\mathbb{R}^N
$$

连续时间状态空间模型的标准形式；分子与分母同名的两个式子是"状态方程"与"输出方程"。（S4 论文式 (1)；HiPPO 论文 Sec 2.1）

### C.2.2 离散 SSM

$$
x_k=\bar A x_{k-1}+\bar B u_k,\qquad y_k=\bar C x_k+\bar D u_k
$$

把 (C.2.1) 按步长 $\Delta$ 采样后的递推形式；三种离散化见下。（S4 论文式 (3)；S4D 论文式 (6) 附近的定义）

$$
\underbrace{\bar A=e^{\Delta A},\quad \bar B=A^{-1}(e^{\Delta A}-I)B}_{\text{ZOH}}\qquad
\underbrace{\bar A=(I-\tfrac{\Delta}{2}A)^{-1}(I+\tfrac{\Delta}{2}A),\quad \bar B=(I-\tfrac{\Delta}{2}A)^{-1}\Delta B}_{\text{双线性}}
$$

ZOH 假设区间内输入恒定（$A$ 可逆时可化简）；双线性取端点平均，S4 采用后者以配合 Woodbury。（HiPPO 论文 Appendix B.3；S4 论文式 (3)；S4D 论文 Sec 3.1）

### C.2.3 卷积核（LTI）

$$
\bar K=(\bar C\bar B,\ \bar C\bar A\bar B,\ \dots,\ \bar C\bar A^{L-1}\bar B),\qquad y=\bar K * u
$$

LTI SSM 等价于一次卷积；训练时可用 FFT 一次算出整段输出。（S4 论文式 (4)(5)；S4D 论文式 (6)）

### C.2.4 HiPPO-LegS 矩阵

$$
A_{nk}=\begin{cases}(2n+1)^{1/2}(2k+1)^{1/2} & n>k\\ n+1 & n=k\\ 0 & n<k\end{cases},
\qquad B_n=(2n+1)^{1/2}
$$

$n$ 为行、$k$ 为列，$0\le n,k\le N-1$；这是 S4/Mamba 初始化的默认 $A$。（HiPPO 论文式 (2)(3) 附近 Theorem 2；S4 论文式 (2)）

$$
\frac{d}{dt}c(t)=-\frac{1}{t}Ac(t)+\frac{1}{t}Bf(t),\qquad
c_{k+1}=\Big(1-\frac{A}{k}\Big)c_k+\frac{1}{k}Bf_k
$$

连续与离散（Euler 形式）的 HiPPO-LegS 动力学；$1/t$ 缩放带来时间尺度不变性。（HiPPO 论文 Theorem 2 式 (3)(4)）

### C.2.5 LSSL

连续 SSM 层同时具备三种身份，但朴素实现需要

$$
O(N^2L)\ \text{计算},\qquad O(NL)\ \text{内存}
$$

这是 LSSL 不可用的原因（逐时间步做 $N\times N$ 矩阵乘）。（S4 论文 Introduction；LSSL 论文）

### C.2.6 S4：DPLR 与柯西核

$$
A=V\Lambda V^{*}-PQ^{\top}\quad(\text{NPLR}),\qquad
A=\Lambda-PQ^{*}\quad(\text{DPLR})
$$

$A$ 是"酉对角化部分 + 低秩修正"；共轭后变成对角加低秩。HiPPO-LegS/LagT/LegT 的秩 $r=1$ 或 $2$。（S4 论文 Theorem 1 式 (6)）

$$
(A+UV^{*})^{-1}=A^{-1}-A^{-1}U\big(I_p+V^{*}A^{-1}U\big)^{-1}V^{*}A^{-1}
$$

Woodbury 恒等式：把低秩项的求逆降为 $p\times p$ 小矩阵求逆。（S4 论文 Proposition 4）

$$
\hat K(z)=C^{*}(I-Az)^{-1}B\quad\Longrightarrow\quad
\hat K(\omega)=\frac{2}{1+\omega}\Big[\,k_{00}(\omega)-k_{01}(\omega)\big(1+k_{11}(\omega)\big)^{-1}k_{10}(\omega)\Big]
$$

生成函数把"矩阵幂"换成"矩阵逆"，再用 Woodbury 修正低秩项；四个 $k_{\cdot\cdot}$ 各是一次柯西乘法。核心结论：$K$ 可归约为 4 次柯西乘法，$\tilde O(N+L)$ 时间与 $O(N+L)$ 空间。（S4 论文 Algorithm 1、Theorem 3、Lemma C.3）

$$
M_{ij}=\frac{1}{\omega_i-\lambda_j},\qquad
\mathcal{C}(M,N)=\begin{cases}O(MN)&\text{朴素}\\ O\big((M+N)\log^{2}(M+N)\big)&\text{精确}\end{cases}
$$

柯西矩阵定义与代价。（S4 论文 Definition 3、Proposition 5）

### C.2.7 S4D：Vandermonde

$$
K=(B\odot C)\cdot V_L(\bar A),\qquad V_L(\bar A)_{n,\ell}=\bar A_n^{\ell}
$$

对角 SSM 的卷积核就是一次 Vandermonde-向量乘法；$\odot$ 为逐元素积。（S4D 论文式 (7)）

### C.2.8 S5：ZOH 与并行扫描

$$
x_k=\bar A x_{k-1}+\bar B u_k,\qquad
c_k=(\bar A,\ \bar B u_k),\qquad
q_i\bullet q_j=\big(q_{j,a}q_{i,a},\ q_{j,a}q_{i,b}+q_{j,b}\big)
$$

S5 用 MIMO 对角 SSM + 结合扫描在时域并行；对角 $A$ 时并行时间 $O(P\log L)$、总计算量 $O(PL)$。（S5 论文 Sec 2.2、Appendix H 式 (33)(34)）

### C.2.9 S6（Mamba-1 / Mamba-2）：离散化与选择性参数

$$
\bar A=\exp(\Delta A),\qquad \bar B=(\Delta A)^{-1}\big(\exp(\Delta A)-I\big)\cdot\Delta B\quad(\text{论文声称的 ZOH})
$$

$$
h_t=\bar A_t h_{t-1}+\bar B_t x_t\quad(\text{实现实际使用的指数-Euler})
$$

$$
\Delta_t=\operatorname{softplus}\big(\text{Parameter}+s_\Delta(x_t)\big),\quad
B_t=s_B(x_t),\quad C_t=s_C(x_t),\quad A=-\exp(A_{\log})
$$

让 $\Delta,B,C$ 依赖输入即可打破 LTI；$\Delta$ 的最重要后果是"按内容决定该不该写进状态"。（Mamba 论文 Sec 3.2、Algorithm 2、式 (4)）

### C.2.10 Mamba-2 / SSD：Mji 与块分解

$$
M_{ji}=C_j^{\top}A_j\cdots A_{i+1}B_i\quad(j\ge i),\qquad
y=M x=\mathrm{SSS}(A,B,C)\cdot x
$$

状态维度 $N$ 的 SSM 等价于一个 $N$-半可分矩阵的乘法；对角块用二次（注意力）形式算，块间用低秩传播。算法总代价 $O(TN^2)$（$P=N$）。（Mamba-2 论文 Definition 3.2、Theorem 3.5、Theorem 6.1、Sec 6）

$$
Y=(L\circ(QK^\top))V,\qquad L=\mathrm{1SS}(a),\qquad
h_t=a_t h_{t-1}+b_t\ (\text{cumprodsum})
$$

SSD 的注意力形式与 1-SS 掩码；块分解的核心理由是"矩阵乘对硬件友好"。（Mamba-2 论文式 (10)(11)(15)、Sec 3.2.2）

### C.2.11 Mamba-3：指数-梯形与复值 RoPE

$$
h_t=\alpha_t h_{t-1}+\beta_t B_{t-1}x_{t-1}+\gamma_t B_t x_t,\qquad
\alpha_t=e^{\Delta_tA_t},\ \beta_t=(1-\lambda_t)\Delta_t e^{\Delta_tA_t},\ \gamma_t=\lambda_t\Delta_t
$$

指数-梯形离散化：对状态-输入积分用数据依赖的凸组合（端点加权），比 Euler 高阶；$\lambda_t=1$ 退化成 Mamba-2 的指数-Euler。（Mamba-3 论文 Proposition 1 式 (5)(6)）

$$
h_t=\alpha_t R_t h_{t-1}+\beta_t R_t B_{t-1}x_{t-1}+\gamma_t B_t x_t,\qquad
R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{bmatrix}
$$

复值 SSM 的实等价形式：块对角旋转矩阵 + 标量衰减。（Mamba-3 论文 Proposition 2 式 (9)）

$$
h_t=e^{\Delta_tA_t}h_{t-1}+\Big(\prod_{i=0}^{t}R_i\Big)^{\top}\Delta_tB_tx_t,\qquad
y_t=\Big[\Big(\prod_{i=0}^{t}R_i\Big)^{\top}C_t\Big]^{\top}h_t
$$

"RoPE trick"：把数据依赖的累积旋转作用在 $B,C$（即 $Q,K$）上，避免逐步做矩阵旋转。（Mamba-3 论文 Proposition 3 式 (10)）

### C.2.12 MIMO 的 SISO 分解

$$
h_t^{(j)}\leftarrow \alpha_t h_{t-1}^{(j)}+\Delta_t B_t^{(j)}x_t^{(j)},\qquad
y_t^{(i)}\leftarrow \sum_j C_t^{(i)\top}h_t^{(j)}
$$

MIMO SSM 可写为 $R^2$ 个共享同一衰减的 SISO SSM：$R$ 个输入 rank 与 $R$ 个输出 rank 交叉求和；算术强度随 $R$ 线性提升，解码速度近似不变。（Mamba-3 论文 Sec 3.3 式 (12)）

---

## C.3 五个模型横向对比

下表把五个主角模型放在同一张表里，方便回答"S4 与 Mamba 到底差在哪"这类问题。读表时重点关注三件事：状态矩阵的结构（决定能算多快）、是否时变（决定能不能做内容选择）、计算模式（决定训练/推理分别在平台上快不快）。

| 维度 | S4 | S5 | Mamba-1 (S6) | Mamba-2 (SSD) | Mamba-3 |
|---|---|---|---|---|---|
| 状态矩阵结构 | NPLR / DPLR（对角加低秩，复） | 对角（P 个 MIMO 状态） | 对角（实，$A=-\exp(A_{\log})$） | 标量 × 单位阵（对角 + 分块） | 复值块对角旋转 $+$ 标量衰减 |
| 是否时变 | 否（LTI） | 可选（保留 LTI 为主） | **是**（$\Delta,B,C$ 依赖输入） | **是** | **是** |
| 计算模式 | 卷积（训练）/ 递归（推理） | 并行扫描 | 选择性扫描（核融合 + 重计算） | 块分解（对角块注意力 + 块间低秩） | 块分解（SSD）+ RoPE |
| 训练复杂度 | $\tilde O(N+L)$（核计算） | $O(PL)$（并行扫描） | $O(BLDN)$（扫描） | $O(TN^2)$（$P=N$） | $O(TN^2)$ 量级 |
| 推理复杂度 | $O(N)$/步 | $O(PL)$/步（$N$ 步内直接算） | $O(N)$/步 | $O(N^2)$/步（状态 $N^2$） | $O(N^2)$/步（MIMO 后访存不变、算力增 $R$ 倍） |
| 关键创新 | NPLR + Woodbury + 柯西核 | MIMO + 并行扫描 | 选择机制 + 硬件感知扫描 | 状态空间对偶；半可分矩阵；块分解 | 指数-梯形离散化；复值状态/RoPE；MIMO |
| 局限 | LTI 无法做内容选择；DPLR 装备复杂 | 对角化后表达力受限，语言建模偏弱 | 选择性使卷积模式失效，只能递归；kernel 复杂 | 块分解有 chunk 超参；状态大时显存与重算成本高 | 实现复杂度最高；梯形参数需调；仍是固定大小状态 |

> 说明：训练 / 推理复杂度一栏按本书正文统一口径（$L$ 序列长、$B$ batch、$H$ 隐藏维、$N$ 状态维、$T$ 序列长、$P$ head 维）。S4 的一行与 S4 论文 Table 1 一致；Mamba-2 的 $O(TN^2)$ 出自 Mamba-2 论文 Theorem 6.1（取 $P=N$ 时下界紧）。Mamba-3 的复杂度与 Mamba-2 同阶，其收益体现在算术强度与质量上，故写"量级"。

### 三句话总结这张表

- 从 S4 到 S5：状态矩阵从"非对角但可拆"缩到"对角"，换来的是可以用并行扫描走时域，代价是表达力下降。
- 从 S5 到 Mamba-1/2：核心在让参数依赖输入（时变），并不在换矩阵；这是唯一能解决"选择性复制"这类任务的办法。代价是卷积模式失效，必须用扫描或块分解。
- 从 Mamba-2 到 Mamba-3：训练算法不再大改，而是同时修正离散化精度（指数-梯形）、动力学表达（复值旋转）、硬件效率（MIMO）三个维度。

---

## C.4 一页纸的“公式地图”

若只允许带一页纸进考场，应该是：

1. 连续：$x'=Ax+Bu$，解 $x(t)=e^{tA}x(0)$。
2. 离散：$\bar A=e^{\Delta A}$（ZOH）或 $\bar A=(I-\frac{\Delta}{2}A)^{-1}(I+\frac{\Delta}{2}A)$（双线性）。
3. 卷积：$\bar K=(\bar C\bar B,\bar C\bar A\bar B,\dots)$。
4. S4：$A=\Lambda-PQ^{*}$（DPLR）$\Rightarrow$ Woodbury 修正 $\Rightarrow$ 4 次柯西乘。
5. S4D：$K=(B\odot C)V_L(\bar A)$。
6. S6：$\Delta=\operatorname{softplus}(\cdot)$，$A=-\exp(A_{\log})$，$\bar A_t=\exp(\Delta_tA_t)$。
7. SSD：$M_{ji}=C_j^{\top}A_j\cdots A_{i+1}B_i$，$Y=(L\circ(QK^{\top}))V$。
8. Mamba-3：$h_t=\alpha_th_{t-1}+\beta_tB_{t-1}x_{t-1}+\gamma_tB_tx_t$，旋转用 $R(\theta)$。

这八行公式串起来，就是本书从 LSSL 到 Mamba-3 的全部骨架。

---

**返回**：[全书总目录](../../../README.md) ｜ [附录 A 数学工具箱](appA.md) ｜ [附录 B 论文清单与术语表](appB.md)
