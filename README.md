# 从 LSSL 到 Mamba-3

一套讲状态空间模型的书，分两本。

| | 讲什么 | 适合谁 | 入口 |
|---|---|---|---|
| **入门版**《故事与直觉》 | 动机、直觉、结论，不推公式 | 想先建立整体地图的读者 | [开始阅读](books/intro/chapters/ch01.md) ｜ [PDF](output/mamba-intro.pdf) |
| **专业版**《理论、算法与实现》 | 完整推导、算法细节、可运行代码 | 要做研究或实现的人 | [开始阅读](books/pro/chapters/ch01.md) ｜ [PDF](output/from-lssl-to-mamba3.pdf) |

两本覆盖同一批模型：HiPPO、LSSL、S4、S5、Mamba、Mamba-2、Mamba-3。建议先读入门版，再挑感兴趣的章节读专业版。

## 入口

- [入门版前言](books/intro/front/preface.md)
- [专业版前言](books/pro/front/preface.md)
- [入门版目录](#入门版目录)
- [专业版目录](#专业版目录)

---

## 入门版目录

### 第一篇　问题

1. [三种模型，三种记忆方式](books/intro/chapters/ch01.md)
2. [一个状态能记住多少](books/intro/chapters/ch02.md)
3. [注意力的代价](books/intro/chapters/ch03.md)

### 第二篇　一个大胆的想法

4. [把记忆变成一个数学问题](books/intro/chapters/ch04.md)
5. [一种层，三种身份](books/intro/chapters/ch05.md)
6. [让不可能的计算变得可能](books/intro/chapters/ch06.md)
7. [简化到几行代码](books/intro/chapters/ch07.md)

### 第三篇　学会选择

8. [固定压缩的极限](books/intro/chapters/ch08.md)
9. [让参数学会看输入](books/intro/chapters/ch09.md)
10. [让显卡愿意跑](books/intro/chapters/ch10.md)
11. [矩阵视角：SSM 就是注意力](books/intro/chapters/ch11.md)
12. [补上两块短板](books/intro/chapters/ch12.md)

### 第四篇　今天与明天

13. [混合架构：为什么还留着注意力](books/intro/chapters/ch13.md)
14. [怎么选，往哪走](books/intro/chapters/ch14.md)

---

## 专业版目录

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
- [后记](books/pro/front/afterword.md)
