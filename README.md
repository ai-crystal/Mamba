# 从 LSSL 到 Mamba-3

## 状态空间模型笔记

作者：**Dr. Dezeming**

[开始阅读](book/chapters/ch01.md)　[下载 PDF](output/from-lssl-to-mamba3.pdf)

---

序列建模的核心问题只有一个：怎样用有限的存储，记住任意长的历史。

Transformer 的答案是“不压缩”，把整段上下文留在 KV cache 里，需要时直接查。循环网络的答案相反，把历史压进一个固定大小的状态。过去六年里，有一条技术路线在尝试第三种答案：用可学习的线性动力系统来压缩历史，让压缩方式由数据决定，同时保持线性的训练成本。

这本书沿着这条路线，把七个模型逐个拆开：HiPPO、LSSL、S4、S5、Mamba、Mamba-2、Mamba-3。每一代都在接手上一代留下的具体缺陷，理解这条链条，比记住任何单个模型的公式都重要。

## 目录

### 第一篇　背景：序列模型的三难与连续时间系统

1. [序列建模的三难困境](book/chapters/ch01.md)
2. [连续时间线性系统与状态空间模型](book/chapters/ch02.md)
3. [从连续到离散：SSM 如何成为一个神经网络层](book/chapters/ch03.md)

### 第二篇　记忆：HiPPO

4. [记忆问题的形式化](book/chapters/ch04.md)
5. [HiPPO 框架与三个具体推导](book/chapters/ch05.md)
6. [HiPPO 的性质与遗产](book/chapters/ch06.md)

### 第三篇　LSSL

7. [一个拥有三重身份的网络层](book/chapters/ch07.md)
8. [表达力：RNN 与卷积都是特例](book/chapters/ch08.md)
9. [LSSL 的阿喀琉斯之踵](book/chapters/ch09.md)

### 第四篇　S4

10. [朴素对角化为什么会失败](book/chapters/ch10.md)
11. [NPLR 与 DPLR：把病态矩阵拆开](book/chapters/ch11.md)
12. [S4 算法：从矩阵幂到柯西核](book/chapters/ch12.md)
13. [三种模式：架构细节与实验](book/chapters/ch13.md)
14. [S4D 与 DSS：对角化的胜利](book/chapters/ch14.md)

### 第五篇　S5 及其时代

15. [S5：并行扫描与 MIMO 状态空间](book/chapters/ch15.md)
16. [S4 之后的生态](book/chapters/ch16.md)

### 第六篇　Mamba：选择性

17. [核心洞察：线性时不变是瓶颈](book/chapters/ch17.md)
18. [S6：选择机制的数学](book/chapters/ch18.md)
19. [硬件感知的并行扫描](book/chapters/ch19.md)
20. [Mamba 架构](book/chapters/ch20.md)
21. [选择性 SSM 的机理与实验](book/chapters/ch21.md)

### 第七篇　Mamba-2：状态空间对偶

22. [半可分矩阵：SSM 的矩阵真身](book/chapters/ch22.md)
23. [结构化掩码注意力](book/chapters/ch23.md)
24. [状态空间对偶](book/chapters/ch24.md)
25. [SSD 算法：块分解](book/chapters/ch25.md)
26. [Mamba-2 架构](book/chapters/ch26.md)
27. [混合架构与新能效前沿](book/chapters/ch27.md)

### 第八篇　Mamba-3：推理优先

28. [从 Mamba-2 到 Mamba-3](book/chapters/ch28.md)
29. [指数-梯形离散化](book/chapters/ch29.md)
30. [复值状态与数据依赖旋转](book/chapters/ch30.md)
31. [MIMO：把解码从访存瓶颈里救出来](book/chapters/ch31.md)
32. [架构与实验](book/chapters/ch32.md)

### 第九篇　实践与收尾

33. [从零实现：S4D、S6 与 SSD](book/chapters/ch33.md)
34. [训练实践：技巧与陷阱](book/chapters/ch34.md)
35. [开放问题与学习路线](book/chapters/ch35.md)

### 附录

- [附录 A　数学工具箱](book/appendix/appA.md)
- [附录 B　论文与术语](book/appendix/appB.md)
- [附录 C　公式速查与符号表](book/appendix/appC.md)
