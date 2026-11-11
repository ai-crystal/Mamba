# 附录 B 论文清单与术语表

## B.1 论文清单

下表按时间顺序列出本书涉及的全部核心论文。"贡献"一栏只有一句话，不能替代正文；章节一栏给出本书中精读该论文的位置。arXiv 编号与会议信息以可核实者为准，凡无法从论文原文或公开著录中确认的，一律标注为"未核实"，引用请以官方版本为准。

| 论文 | 作者与机构 | 年份 / 会议 | arXiv | 一句话贡献 | 本书章节 |
|---|---|---|---|---|---|
| HiPPO: Recurrent Memory with Optimal Polynomial Projections | Albert Gu, Tri Dao, Stefano Ermon, Atri Rudra, Christopher Ré（Stanford；University at Buffalo, SUNY） | 2020 / 会议信息未核实 | 2008.07669 | 把"记忆"形式化为在线函数逼近，用正交多项式投影导出最优的状态转移矩阵 | [第 4 章](../chapters/ch04.md)、[第 5 章](../chapters/ch05.md)、[第 6 章](../chapters/ch06.md) |
| LSSL: Combining Recurrent, Convolutional, and Continuous-time Models with Linear State-Space Layers | Albert Gu, Isys Johnson, Karan Goel, Khaled Saab, Tri Dao, Atri Rudra, Christopher Ré（Stanford；University at Buffalo, SUNY） | 2021 / 会议信息未核实 | 2110.13985 | 把连续时间 SSM 做成神经网络层，证明它同时是 RNN、CNN 与 ODE 三种身份的联合体 | [第 7 章](../chapters/ch07.md)、[第 8 章](../chapters/ch08.md)、[第 9 章](../chapters/ch09.md) |
| S4: Efficiently Modeling Long Sequences with Structured State Spaces | Albert Gu, Karan Goel, Christopher Ré（Stanford） | 2021 / 会议信息未核实 | 2111.00396 | 用 NPLR 参数化 + Woodbury + 柯西核，把 SSM 的卷积核计算降到 $\tilde O(N+L)$，首次解决长程依赖 | [第 10 章](../chapters/ch10.md)～[第 13 章](../chapters/ch13.md) |
| DSS: Diagonal State Spaces are as Effective as Structured State Spaces | Ankit Gupta（IBM Research）, Albert Gu（Stanford）, Jonathan Berant（Tel Aviv University） | 2022 / 会议信息未核实 | 2203.14343 | 证明只用**对角**状态矩阵 + ZOH + softmax 归一化，就能达到 S4 的效果 | [第 14 章](../chapters/ch14.md) |
| S4D: On the Parameterization and Initialization of Diagonal State Space Models | Albert Gu, Ankit Gupta, Karan Goel, Christopher Ré（Stanford；IBM Research） | 2022 / 会议信息未核实 | 2206.11893 | 把对角 SSM 的核归结为一次 Vandermonde 乘法，并给出多种对角线初始化（S4D-Lin / S4D-Inv / S4D-LegS） | [第 14 章](../chapters/ch14.md)、[第 33 章](../chapters/ch33.md) |
| How to Train Your HiPPO: State Space Models with Generalized Orthogonal Basis Projections | Albert Gu, Isys Johnson, Aman Timalsina, Atri Rudra, Christopher Ré（Stanford；University at Buffalo, SUNY） | 2022 / 会议信息未核实 | 2206.12037 | 把 HiPPO 推广到任意正交基，系统研究 SSM 的参数化与初始化，解释 S4 为何"必须用 HiPPO 初始化" | [第 6 章](../chapters/ch06.md)、[第 14 章](../chapters/ch14.md) |
| S5: Simplified State Space Layers for Sequence Modeling | Jimmy T. H. Smith, Andrew Warrington, Scott W. Linderman（Stanford） | 2022 / ICLR 2023 | 2208.04933 | 用 MIMO + 并行扫描走通时域计算路径，只需一个 SSM 层即可处理全部通道 | [第 15 章](../chapters/ch15.md) |
| H3: Hungry Hungry Hippos: Towards Language Modeling with State Space Models | Daniel Y. Fu, Tri Dao, Khaled K. Saab, Armin W. Thomas, Atri Rudra, Christopher Ré（Stanford；University at Buffalo, SUNY） | 2022 / 会议信息未核实 | 2212.14052 | 把 SSM 与"移位-乘"（shift-and-multiply）机制拼在一起，补上 SSM 在联想回忆上的短板 | [第 16 章](../chapters/ch16.md) |
| Hyena: Hyena Hierarchy | 作者与机构未核实 | 2023 | 未核实 | 用长卷积 + 门控的层级结构替代注意力，在长上下文上达到接近注意力的质量 | [第 16 章](../chapters/ch16.md) |
| Mamba-1: Mamba: Linear-Time Sequence Modeling with Selective State Spaces | Albert Gu（Carnegie Mellon University）, Tri Dao（Princeton University） | 2023 / 会议信息未核实 | 2312.00752 | 让 $\Delta,B,C$ 依赖输入，打破 LTI，配合硬件感知的选择性扫描，首次在中小规模上匹配 Transformer | [第 17 章](../chapters/ch17.md)～[第 21 章](../chapters/ch21.md) |
| Mamba-2: Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality | Tri Dao（Princeton University）, Albert Gu（Carnegie Mellon University） | 2024 / ICML 2024 | 2405.21060 | 用半可分矩阵证明"SSM 就是（掩码）线性注意力"，并给出 SSD 块分解算法，训练提速 2–8× | [第 22 章](../chapters/ch22.md)～[第 27 章](../chapters/ch27.md) |
| Mamba-3: Mamba-3: Improved Sequence Modeling using State Space Principles | Aakash Lahoti, Kevin Y. Li, Berlin Chen, Caitlin Wang, Aviv Bick, J. Zico Kolter, Tri Dao, Albert Gu（Carnegie Mellon University；Princeton University；Together AI；Cartesia AI） | 2026 | 2603.15569 | 用指数-梯形离散化、复值状态（数据依赖 RoPE）与 MIMO 同时提升质量与推理效率，并恢复状态追踪能力 | [第 28 章](../chapters/ch28.md)～[第 32 章](../chapters/ch32.md) |
| Unlocking State-Tracking in Linear RNNs through Negative Eigenvalues | Riccardo Grazzi, Julien Siems, Arber Zela, Jörg K. H. Franke, Frank Hutter, Massimiliano Pontil（Istituto Italiano di Tecnologia；University of Freiburg；ELLIS Institute Tübingen；University College London） | 2025 / ICLR 2025 | 2411.12537 | 证明状态转移矩阵特征值仅取正值的 LRNN 无法解 parity，而引入负特征值可以，并给出理论刻画 | [第 28 章](../chapters/ch28.md)、[第 30 章](../chapters/ch30.md) |
| Linear Attention: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention | Angelos Katharopoulos 等（作者与机构未核实） | 2020 / 会议信息未核实 | 2006.16236 | 去掉 softmax 后注意力可重排为 $Q\cdot\mathrm{cumsum}(K^\top V)$，于是推理变成常数时间的递推 | [第 23 章](../chapters/ch23.md)、[第 24 章](../chapters/ch24.md) |
| RetNet: Retentive Network | 作者与机构未核实 | 2023 | 未核实 | 并行、递归、分块三种表示统一的保留机制，与 1-SS 掩码高度相关 | [第 16 章](../chapters/ch16.md)、[第 23 章](../chapters/ch23.md) |
| RWKV: 标题未核实（RWKV 系列） | 作者与机构未核实 | 2023 | 未核实 | 用线性递推 + 门控的类 RNN 架构做大规模语言建模 | [第 16 章](../chapters/ch16.md) |
| GLA: Gated Linear Attention | 作者与机构未核实 | 2023 / 2024 | 未核实 | 给线性注意力加上数据依赖的衰减，与对角 SSM 在数学上同族 | [第 16 章](../chapters/ch16.md)、[第 23 章](../chapters/ch23.md) |
| GatedDeltaNet: 标题未核实（Gated Delta 网络） | 作者与机构未核实 | 2024 | 未核实 | 在 DeltaNet 的更新规则上加门控，是 Mamba-3 的主要对比基线之一 | [第 16 章](../chapters/ch16.md)、[第 32 章](../chapters/ch32.md) |

> 关于未核实项：本表中的会议名与部分 arXiv 编号，凡未能在论文原文文本中直接确认的，均标注"未核实"。Hyena、RetNet、RWKV、GLA、GatedDeltaNet 的 arXiv 编号本次未核实，不作填写，请读者自行查阅官方版本。

---

## B.2 术语表

本表按中文术语拼音 / 英文缩写字母排序，共 70 余条。查表时注意两点：一是同一概念在不同论文里的名字不同（例如“半可分”与“结构化秩矩阵”、“顺序半可分”与“结构化状态空间”）；二是同一个缩写在不同语境下含义不同（SSM 既可指 state space model 也可指 semiseparable matrix，SSS 既可指 structured state space 也可指 sequentially semiseparable——Mamba-2 论文自己拿这个巧合开玩笑）。

每条给出中文名、英文原名与一句话定义。

| 术语 | 英文原名 | 定义 |
|---|---|---|
| 边界重置 | boundary reset | Mamba-2 中让状态在序列分块边界处清零（或从初始状态重启）的处理，使块间计算可并行 |
| 半可分矩阵 | semiseparable matrix | 下三角方向上每个子块秩不超过 $N$ 的矩阵，与 SSM 等价 |
| 半可分阶 | semiseparable order / rank | 上述子块秩的上界 $N$，对应 SSM 的状态维度 |
| 并行扫描 | parallel scan / associative scan | 用结合算子把前缀计算转成 $O(\log L)$ 深度的分治算法 |
| 长程依赖 | long-range dependency (LRD) | 序列中相距很远的元素之间的依赖关系 |
| 长程竞技场 | Long Range Arena (LRA) | 一组专门评测长序列建模能力的基准，S4 系列的主战场 |
| 乘法 | Hadamard product | 逐元素相乘，$B\odot C$，S4D 的核公式中用到 |
| 重计算 | recomputation | 反向传播时不存中间状态、而是从输入重算，用计算换内存 |
| 稠密矩阵 | dense matrix | 无结构、需 $O(T^2)$ 存储的矩阵，是结构化的反面 |
| 等价变换 | conjugation | $(A,B,C)\sim(V^{-1}AV,V^{-1}B,CV)$，保持输入输出映射不变 |
| 范德蒙德矩阵 | Vandermonde matrix | 元素 $V_{n,\ell}=\lambda_n^{\ell}$ 的矩阵，等价于多点多项式求值 |
| 分块对角旋转 | block-diagonal rotation | 由若干 $2\times2$ 旋转矩阵拼成的转移矩阵，Mamba-3 复值状态的实等价形式 |
| 分块分解 | block decomposition | 把序列变换矩阵按 chunk 切块，块内用注意力式乘法、块间用低秩传播 |
| 关联扫描算子 | associative scan operator | 满足结合律的二元算子，如 $(a_t,b_t)\otimes(a_s,b_s)=(a_ta_s,a_tb_s+b_t)$ |
| 状态 | state | 对历史的固定维摘要，$x(t)\in\mathbb{R}^N$ 或 Mamba 记号下的 $h_t$ |
| 状态扩张因子 | state expansion factor | 状态维度 $N$ 相对输入维度的放大倍数 |
| 状态空间模型 | state space model (SSM) | 由 $x'=Ax+Bu,\ y=Cx+Du$ 定义的线性动态系统，可做序列层 |
| 状态空间对偶 | structured state space duality (SSD) | SSM 与结构化掩码注意力之间的等价理论，Mamba-2 的核心 |
| 状态追踪 | state tracking | 模型沿序列逐步维护变量状态的能力，如 parity；LTI 模型无法完成 |
| 结构化矩阵 | structured matrix | 用远少于 $O(T^2)$ 参数可表示的矩阵类（半可分、柯西、范德蒙德等） |
| 结构化掩码注意力 | structured masked attention (SMA) | 带结构化掩码 $L$ 的注意力，$Y=(L\circ(QK^\top))V$ |
| 核融合 | kernel fusion | 把多个操作合并进一个 GPU kernel，减少 HBM 读写 |
| 卷积核 | convolution kernel | LTI SSM 等价于卷积时的核 $\bar K=(\bar C\bar B,\bar C\bar A\bar B,\dots)$ |
| 柯西核 | Cauchy kernel | 元素为 $1/(\omega_i-\lambda_j)$ 的矩阵，S4 卷积核计算的归约目标 |
| 快速多极子方法 | Fast Multipole Method (FMM) | 把远处节点聚成展开、近处单独算的近线性算法，用于柯西核 |
| 离散化 | discretization | 把连续 ODE 换成离散递推的过程 |
| 零阶保持 | zero-order hold (ZOH) | 假设区间内输入恒定，$\bar A=e^{\Delta A}$、$\bar B=A^{-1}(e^{\Delta A}-I)B$ |
| 双线性变换 | bilinear transform / Tustin | 用区间端点平均近似积分，$\bar A=(I-\frac\Delta2A)^{-1}(I+\frac\Delta2A)$ |
| 前向欧拉 | forward Euler | 取左端点，$\bar A=I+\Delta A$，一阶显式 |
| 后向欧拉 | backward Euler | 取右端点，$\bar A=(I-\Delta A)^{-1}$，隐式 |
| 指数-欧拉 | exponential-Euler | Mamba-1/2 实际实现的离散化，$h_t=e^{\Delta_tA_t}h_{t-1}+\Delta_tB_tx_t$ |
| 指数-梯形 | exponential-trapezoidal | Mamba-3 提出的二阶离散化，含凸组合系数 $\lambda_t$ |
| 矩阵指数 | matrix exponential | $e^M=\sum_k M^k/k!$，线性 ODE 的传播算子 |
| 正规矩阵 | normal matrix | 满足 $AA^{*}=A^{*}A$ 的矩阵，可被酉矩阵稳定对角化 |
| 正规加低秩 | normal plus low-rank (NPLR) | 把 $A$ 写成酉对角化部分 + 低秩修正的形式，S4 参数化 |
| 对角加低秩 | diagonal plus low-rank (DPLR) | NPLR 共轭后的形式，$A=\Lambda-PQ^{*}$ |
| 条件数 | condition number | $\kappa(V)=\|V\|\|V^{-1}\|$，衡量对角化在浮点下是否可靠 |
| 谱定理 | spectral theorem | 正规矩阵可被酉矩阵对角化的定理 |
| 生成函数 | generating function (SSMGF) | $\hat K(z)=C^{*}(I-Az)^{-1}B$，把卷积核转到"求逆"而非"求幂" |
| 柯西矩阵 | Cauchy matrix | 见"柯西核" |
| 顺序半可分 | sequentially semiseparable (SSS) | $M_{ji}=C_j^\top A_j\cdots A_{i+1}B_i$ 这一参数化表示 |
| 1-SS 矩阵 | 1-semiseparable (1-SS) matrix | $M_{ji}=a_{j:i}$，等价于标量递推 |
| 累积乘积和 | cumprodsum | $h_t=a_th_{t-1}+b_t$，1-SS 乘法与标量 SSM 递推的统称 |
| 累积和 | cumsum | $a_t\equiv1$ 时的 cumprodsum，线性注意力中的关键操作 |
| 门控 | gating | 用 sigmoid/SiLU 等函数产生的乘性（0~1）开关，控制信息流 |
| 时间尺度 | timescale / $\Delta$ | 离散化步长，选择性 SSM 中它是最重要的输入依赖参数 |
| 时间尺度等变 | timescale equivariance | 输入时间被拉伸时输出同步拉伸的性质，HiPPO-LegS 具备 |
| 短卷积 | short convolution | Mamba 等模型中紧随输入投影的深度可分离一维卷积 |
| 算术强度 | arithmetic intensity | FLOPs 与访存字节数之比，决定 kernel 是算力受限还是带宽受限 |
| 访存瓶颈 | memory-bound | 算力空闲、带宽打满的状态，SSM 解码的常态 |
| 多输入多输出 | multi-input multi-output (MIMO) | 输入输出为向量、状态为矩阵的 SSM，提高算术强度 |
| 单输入单输出 | single-input single-output (SISO) | 输入输出为标量的经典 SSM 设定 |
| 多查询注意力 | multi-query attention (MQA) | 多个查询头共享一组 KV，降低 KV cache |
| 多头注意力 | multi-head attention (MHA) | 标准注意力，每个头有独立 KV |
| 多值注意力 | multi-value attention (MVA) | 与 MQA 对偶：多个 Q 共享 K、各有独立 V |
| 联想回忆 | associative recall | 根据上文线索取出对应内容的能力（induction head 的基础） |
| 归纳头 | induction head | 在上下文中学到"复制前文下一个 token"的注意力头 |
| 混合架构 | hybrid architecture | 大多数层用 SSM、少数层用注意力的模型设计 |
| 选择性 | selection / selectivity | 让 $\Delta,B,C$ 依赖输入，从而能"记住或忽略"特定内容 |
| 线性时不变 | linear time-invariant (LTI) | 参数不随时间变化的线性系统，等价于卷积 |
| 线性时变 | linear time-varying (LTV) | 参数随时间/输入变化，不再等价于固定卷积 |
| 旋转位置编码 | rotary position embedding (RoPE) | 用旋转矩阵给 $Q,K$ 编码位置；Mamba-3 用数据依赖版 |
| BC / QK 归一化 | BC normalization / QK normalization | 在 $B,C$（对应 $Q,K$）投影后做 RMS 归一化，稳定训练 |
| 状态空间对偶算法 | SSD algorithm | Mamba-2 的块分解训练算法，对标 FlashAttention 式实现 |
| 半可分掩码 | semiseparable mask | 满足半可分条件的注意力掩码 $L$ |
| 直通项 | feedthrough / $D$ | $y$ 直接依赖 $u$ 的项，通常等价于一个残差连接 |
| 递归模式 | recurrent mode | 逐时间步更新的 SSM 计算方式，推理时使用 |
| 卷积模式 | convolutional mode | 用 FFT 卷积一次性算出整段输出的训练方式 |
| 数值不稳定 | numerical instability | 中间量指数级增长导致浮点结果失去意义 |
| 特征值 | eigenvalue | 决定系统衰减/振荡模式的本征值；Mamba 用 $-e^{A_{\log}}$ 保证负实部 |
| 酉矩阵 | unitary matrix | 满足 $UU^{*}=I$ 的矩阵，范数保持、条件数为 1 |
| 位移秩 | displacement rank | 矩阵满足低秩位移方程的程度，是快速算法的结构化依据 |
| 膨胀卷积模式 | dilated mode | 1-SS 乘法的一种分解：按 1、2、4、8…… 的步长逐步传播信息 |
| 状态传递模式 | state-passing / chunkwise mode | 1-SS 乘法的分块实现，块内递推、块间传递状态 |
| 块长 | chunk length / $\mathsf{C}$ | 块分解中一个 chunk 包含的时间步数，通常取 64/128/256 |
| 序列变换矩阵 | sequence transformation matrix $M$ | 把输入序列线性映射为输出序列的 $T\times T$ 矩阵，亦记作 $L$ |
| 状态传递 | state passing | 把上一块的末状态作为下一块初状态的过程 |
| 谱半径 | spectral radius | 矩阵特征值模的最大值；小于 1 时递推会衰减 |
| 收缩性 | contraction | 转移矩阵谱半径 $<1$，保证递推不会指数爆炸 |
| GSS | gated state space | 给 SSM 加门控的变体，属于 S4 之后的生态（具体出处未核实） |
| LRU | linear recurrent unit | 用对角线性递推做语言建模的早期尝试，Mamba 的直接前辈之一 |
| HiPPO-LegS | scaled Legendre | 对所有历史 $[0,t]$ 均匀加权并做尺度归一化的 HiPPO 变体，无时间尺度超参 |
| S4D-Lin | diagonal linear init | 把对角元初始化为等间距实数的 S4D 初始化 |
| S4D-Inv | diagonal inverse init | 把对角元初始化为与状态维成反比的 S4D 初始化 |
| 掩码 | mask | 在注意力中屏蔽未来位置（因果）或特定位置（稀疏）的矩阵 |
| 状态追踪复杂度类 | TC0 | 可由常数深度阈值电路求解的问题类，是 LRNN 状态追踪能力的理论上界 |
| 长上下文检索 | needle-in-a-haystack | 在长文里找回一条指定信息，评测长上下文能力的常用基准 |
| Path-X | Path-X | LRA 中最难的 16k 长序列任务，S4 首次解决 |
| 序列 CIFAR | sCIFAR | 把 CIFAR-10 图像按像素排成序列的分类任务，LRA 之一 |

---

## B.3 三条推荐阅读路线

### 路线一：只想懂 Mamba 是什么（约 8 小时）

适合"下一份工作要用 Mamba，但没时间啃理论"的读者。跳过长推导，抓住主线动机。

| 顺序 | 章节 | 关注什么 | 预计耗时 |
|---|---|---|---|
| 1 | [第 1 章](../chapters/ch01.md) | 序列建模的三难：长度、表达力、效率 | 30 min |
| 2 | [第 2 章](../chapters/ch02.md) | $x'=Ax+Bu$ 与矩阵指数（可略过部分推导） | 60 min |
| 3 | [第 5 章](../chapters/ch05.md) | HiPPO 只想懂"压缩什么"，可跳过推导 | 50 min |
| 4 | [第 9 章](../chapters/ch09.md) | LSSL 为什么不可用 | 30 min |
| 5 | [第 10 章](../chapters/ch10.md)、[第 12 章](../chapters/ch12.md) | S4 的核心思想与算法骨架 | 90 min |
| 6 | [第 17 章](../chapters/ch17.md)～[第 20 章](../chapters/ch20.md) | 选择性、硬件感知扫描、Mamba 块 | 120 min |
| 7 | [第 24 章](../chapters/ch24.md)、[第 25 章](../chapters/ch25.md) | SSD 是什么、为什么快 | 70 min |
| 8 | [第 28 章](../chapters/ch28.md)～[第 31 章](../chapters/ch31.md) | Mamba-3 的三个改动 | 90 min |

合计约 9 小时；若只求"能读论文"，第 2、5 章可再压缩。

### 路线二：想完整掌握理论（约 25 小时）

按顺序从 [第 1 章](../chapters/ch01.md) 读到 [第 35 章](../chapters/ch35.md)。建议配纸笔，重点章节：

- 数学最重：[第 12 章](../chapters/ch12.md)（S4 算法）、[第 22 章](../chapters/ch22.md)～[第 25 章](../chapters/ch25.md)（半可分与 SSD）。配合本附录 A 的 A.4～A.10。
- 理论密度最高：[第 5 章](../chapters/ch05.md)（HiPPO 推导）、[第 29 章](../chapters/ch29.md)、[第 30 章](../chapters/ch30.md)（含 Mamba-3 的 Proposition 2/3/4 证明）。
- 需要回顾前置：读 [第 10 章](../chapters/ch10.md) 前先读附录 A.7；读 [第 25 章](../chapters/ch25.md) 前先读附录 A.8～A.9。

预计 25 小时（含推导复算）；若只求通读、不自己推导，约 15 小时。

### 路线三：想动手实现（约 12 小时）

以代码为中心，理论按需回查。

| 顺序 | 章节 / 材料 | 关注什么 | 预计耗时 |
|---|---|---|---|
| 1 | [第 2 章](../chapters/ch02.md)、[第 3 章](../chapters/ch03.md) | 把连续 SSM 写成递推与卷积两种形式 | 60 min |
| 2 | [第 14 章](../chapters/ch14.md) | S4D 只用 Vandermonde，最好上手 | 50 min |
| 3 | [第 33 章](../chapters/ch33.md) | 逐行实现 S4D 与 Mamba | 180 min |
| 4 | [第 19 章](../chapters/ch19.md) | 手写选择性扫描、核融合与重计算 | 90 min |
| 5 | [第 25 章](../chapters/ch25.md) | 实现 SSD 的块分解（可参考 Listing 1） | 120 min |
| 6 | [第 34 章](../chapters/ch34.md) | 初始化、数值稳定性、常见坑 | 60 min |
| 7 | [第 31 章](../chapters/ch31.md) | MIMO 的 SISO 分解实现与吞吐测量 | 60 min |

预计 10～12 小时（含调参时间）。建议每实现一层就跑一次小规模消融，不要一次写完再 debug。

---

## B.4 一条主线上的关键转折

如果不想逐章读，下面用一句话串起整条演化链，每条都对应上表的一篇论文：

1. 2020 HiPPO：把“记忆”变成“在线函数逼近”，用正交多项式投影从数学上定义了最优的状态矩阵。
2. 2021 LSSL：把连续 SSM 做成层，证明它同时是 RNN、CNN 与 ODE；但 $O(N^2L)$ 的计算与 $O(NL)$ 的内存让它不可用。
3. 2021 S4：发现 HiPPO 矩阵能对角化但数值上不能对角化，于是用 NPLR + Woodbury + 柯西核把卷积核降到 $\tilde O(N+L)$，首次解出 Path-X。
4. 2022 DSS / S4D / How to Train Your HiPPO：反过来问“真的有必须用非对角矩阵吗”；答案是不需要，对角 SSM 就已足够，而且核计算只是一次 Vandermonde 乘法。
5. 2022 S5 / H3：S5 用 MIMO + 并行扫描开辟时域路径；H3 指出 SSM 在联想回忆上的先天短板，用“移位-乘”补齐。
6. 2023 Mamba-1：诊断出真正的瓶颈是 LTI 本身，于是让 $\Delta,B,C$ 依赖输入，并用硬件感知的选择性扫描把代价压回线性。
7. 2024 Mamba-2：用半可分矩阵证明“SSM 就是掩码线性注意力”，把重算变成矩阵乘，训练提速 2–8×，并引出混合架构。
8. 2025 负特征值：证明“特征值只能取正”是 Mamba 解不出 parity 的根源，为复值状态铺路。
9. 2026 Mamba-3：指数-梯形离散化（更准的积分）+ 复值状态 / 数据依赖 RoPE（状态追踪）+ MIMO（把访存瓶颈变成计算），三项一起补齐质量与推理效率。

读完全书回头再看这九句话，你会发现它们只是同一个问题的九种回答：“用固定大小的状态压缩历史，该怎么压缩、代价又该怎么分摊？”

---

**返回**：[全书总目录](../../README.md) ｜ [附录 A 数学工具箱](appA.md) ｜ [附录 C 公式速查与符号表](appC.md)
