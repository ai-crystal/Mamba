# 状态空间模型 · 专业版

## 理论、算法与实现

这是系列里的完整版。七个模型逐个拆开讲：动机、推导、算法、实现上的取舍。公式给到能自己复现的程度，实验数字都能追到论文的某一页。

- 适合：要做研究、要自己写实现、或者需要判断某个改动值不值得试的读者
- 前置：微积分、线性代数、概率论的基本功；会训练网络，看得懂 PyTorch
- 篇幅：35 章加三个附录，363 页

## 怎么读

第一篇建语言，连续时间系统与离散化，后面每一章都会用到。第二、三篇是地基层，HiPPO 与 LSSL。第四、五篇讲 S4 与它带出来的生态。第六到八篇是 Mamba 三代的递进。第九篇落地，实现细节与训练中的坑。

三个附录可以随时查：数学工具箱、论文清单与术语表、公式速查。

这本书可以独立从头读到尾，不需要先读别的书：每一章都从上一代留下的具体失败讲起，前置只要微积分、线性代数和会训练网络。赶时间的话，可以只读第 1、2、10、17、18、20、22、24、29、31、33 章，这条线能串起全部关键转折。

## 目录

### 第一篇　背景

1. [序列建模的三难困境](books/pro/chapters/ch01.md)
2. [连续时间线性系统与状态空间模型](books/pro/chapters/ch02.md)
3. [从连续到离散](books/pro/chapters/ch03.md)

### 第二篇　记忆：HiPPO

4. [记忆问题的形式化](books/pro/chapters/ch04.md)
5. [HiPPO 框架与三个推导](books/pro/chapters/ch05.md)
6. [HiPPO 的性质与遗产](books/pro/chapters/ch06.md)

### 第三篇　LSSL

7. [一个拥有三重身份的网络层](books/pro/chapters/ch07.md)
8. [表达力](books/pro/chapters/ch08.md)
9. [阿喀琉斯之踵](books/pro/chapters/ch09.md)

### 第四篇　S4

10. [朴素对角化为什么会失败](books/pro/chapters/ch10.md)
11. [NPLR 与 DPLR](books/pro/chapters/ch11.md)
12. [从矩阵幂到柯西核](books/pro/chapters/ch12.md)
13. [三种模式与实验](books/pro/chapters/ch13.md)
14. [S4D 与 DSS](books/pro/chapters/ch14.md)

### 第五篇　S5 及其时代

15. [S5](books/pro/chapters/ch15.md)
16. [S4 之后的生态](books/pro/chapters/ch16.md)

### 第六篇　Mamba

17. [线性时不变是瓶颈](books/pro/chapters/ch17.md)
18. [S6：选择机制的数学](books/pro/chapters/ch18.md)
19. [硬件感知的并行扫描](books/pro/chapters/ch19.md)
20. [Mamba 架构](books/pro/chapters/ch20.md)
21. [机理与实验](books/pro/chapters/ch21.md)

### 第七篇　Mamba-2

22. [半可分矩阵](books/pro/chapters/ch22.md)
23. [结构化掩码注意力](books/pro/chapters/ch23.md)
24. [状态空间对偶](books/pro/chapters/ch24.md)
25. [SSD 算法](books/pro/chapters/ch25.md)
26. [Mamba-2 架构](books/pro/chapters/ch26.md)
27. [混合架构与实验](books/pro/chapters/ch27.md)

### 第八篇　Mamba-3

28. [两个新问题](books/pro/chapters/ch28.md)
29. [指数-梯形离散化](books/pro/chapters/ch29.md)
30. [复值状态与旋转](books/pro/chapters/ch30.md)
31. [MIMO](books/pro/chapters/ch31.md)
32. [架构与实验](books/pro/chapters/ch32.md)

### 第九篇　实践与收尾

33. [从零实现](books/pro/chapters/ch33.md)
34. [训练实践](books/pro/chapters/ch34.md)
35. [开放问题](books/pro/chapters/ch35.md)

### 附录

- [附录 A　数学工具箱](books/pro/appendix/appA.md)
- [附录 B　论文与术语](books/pro/appendix/appB.md)
- [附录 C　公式速查](books/pro/appendix/appC.md)

## 下载

[PDF（363 页，15.6 MB）](output/state-space-models-pro.pdf ':ignore')

[网页版阅读](https://ai-crystal.github.io/Mamba/#/books/pro/README)　｜　[返回系列首页](README.md)
