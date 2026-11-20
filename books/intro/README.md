# 状态空间模型 · 入门版

## 故事与直觉

这本书讲的是同一条线上七个模型的来龙去脉：HiPPO、LSSL、S4、S5、Mamba、Mamba-2、Mamba-3。它们都在回答同一个问题，怎样把很长的历史压进一个固定大小的状态，同时把该记的东西记住。

全书不推公式。每一步都按同一顺序讲：上一代卡在哪里，这一代换了个什么问法，代价落在哪。读完能判断这些模型各自适合什么场景，也知道每个结论该回哪篇论文去查。

- 适合：想先建立整体地图、暂时不打算推公式的读者
- 前置：会训练网络，知道 Transformer 和 RNN 大致怎么工作就够了
- 篇幅：14 章，41 页

## 怎么读

第一篇摆问题，三种记忆方式各自的代价。第二篇把记忆写成数学，落到一个统一的层。第三篇讲选择性怎么让模型学会挑内容记。第四篇讲混合架构和选型。

想直接看结论，读第 1、5、9、13 章。想顺着来龙去脉走，按顺序读。

## 目录

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

## 下载

[PDF（41 页，6.3 MB）](output/mamba-intro.pdf ':ignore')

[网页版阅读](https://ai-crystal.github.io/Mamba/#/books/intro/README)　｜　[返回系列首页](README.md)
