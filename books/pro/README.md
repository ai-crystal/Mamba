# 专业版

> 理论、算法与实现

这是系列里的完整版。七个模型逐个拆开讲：动机、推导、算法、实现上的取舍。公式给到能自己复现的程度，实验数字都能追到论文的某一页。

第一篇建语言，连续时间系统与离散化，后面每一章都会用到。第二、三篇是地基层，HiPPO 与 LSSL。第四、五篇讲 S4 与它带出来的生态。第六到八篇是 Mamba 三代的递进。第九篇落地，实现细节与训练中的坑。

共 35 章 · 363 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/v2-pro.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　序列建模的三难困境](chapters/ch01.md)
- [第 2 章　连续时间线性系统与状态空间模型](chapters/ch02.md)
- [第 3 章　从连续到离散：SSM 如何成为一个神经网络层](chapters/ch03.md)
- [第 4 章　记忆问题的形式化：把"记住历史"变成一个优化问题](chapters/ch04.md)
- [第 5 章　HiPPO 框架与三个具体推导](chapters/ch05.md)
- [第 6 章　HiPPO 的性质与遗产](chapters/ch06.md)
- [第 7 章　LSSL：一个拥有三重身份的网络层](chapters/ch07.md)
- [第 8 章　LSSL 的表达力：RNN 与卷积都是它的特例](chapters/ch08.md)
- [第 9 章　LSSL 的阿喀琉斯之踵](chapters/ch09.md)
- [第 10 章　S4 的起点：为什么朴素对角化会失败](chapters/ch10.md)
- [第 11 章　NPLR 与 DPLR：把病态矩阵拆开](chapters/ch11.md)
- [第 12 章　S4 算法：从矩阵幂到柯西核](chapters/ch12.md)
- [第 13 章　S4 的三种模式：架构细节与实验](chapters/ch13.md)
- [第 14 章　S4D 与 DSS：对角化的胜利](chapters/ch14.md)
- [第 15 章　S5：并行扫描与 MIMO 状态空间](chapters/ch15.md)
- [第 16 章　S4 之后的生态：H3、Hyena、GSS、LRU](chapters/ch16.md)
- [第 17 章　核心洞察：线性时不变是瓶颈](chapters/ch17.md)
- [第 18 章　S6：选择机制的数学](chapters/ch18.md)
- [第 19 章　硬件感知的并行扫描](chapters/ch19.md)
- [第 20 章　Mamba 架构：一个既没有注意力也没有 MLP 的块](chapters/ch20.md)
- [第 21 章　选择性 SSM 的机理与实验结果](chapters/ch21.md)
- [第 22 章　半可分矩阵：SSM 的矩阵真身](chapters/ch22.md)
- [第 23 章　结构化掩码注意力：把线性注意力一般化](chapters/ch23.md)
- [第 24 章　状态空间对偶：SSM 就是线性注意力](chapters/ch24.md)
- [第 25 章　SSD 算法：块分解的艺术](chapters/ch25.md)
- [第 26 章　Mamba-2 架构：从注意力借来的设计语言](chapters/ch26.md)
- [第 27 章　Mamba-2 的实验：混合架构与新能效前沿](chapters/ch27.md)
- [第 28 章　从 Mamba-2 到 Mamba-3：两个新问题](chapters/ch28.md)
- [第 29 章　指数-梯形离散化](chapters/ch29.md)
- [第 30 章　复值状态与数据依赖 RoPE](chapters/ch30.md)
- [第 31 章　MIMO：把解码从访存瓶颈里救出来](chapters/ch31.md)
- [第 32 章　Mamba-3 架构与实验](chapters/ch32.md)
- [第 33 章　从零实现：S4D、S6 与 SSD](chapters/ch33.md)
- [第 34 章　训练实践：技巧、陷阱与生态](chapters/ch34.md)
- [第 35 章　总结：开放问题与学习路线](chapters/ch35.md)

### 附录

- [附录 A 数学工具箱](appendix/appA.md)
- [附录 B 论文清单与术语表](appendix/appB.md)
- [附录 C 公式速查与符号表](appendix/appC.md)

---

[返回系列首页](../../README.md)
