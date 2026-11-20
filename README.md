# 状态空间模型

**在线阅读**：[ai-crystal.github.io/Mamba](https://ai-crystal.github.io/Mamba/)　（带搜索、侧栏与分册导航）

一套讲状态空间模型的书，分两本：《故事与直觉》讲动机与结论，《理论、算法与实现》讲推导与实现。两本覆盖同一批模型：HiPPO、LSSL、S4、S5、Mamba、Mamba-2、Mamba-3。入门版讲动机、直觉与结论，专业版讲推导、算法与实现。

| 册 | 讲什么 | 适合谁 | 篇幅 | 在线阅读 | PDF |
|---|---|---|---|---|---|
| **入门版**《故事与直觉》 | 动机、直觉、结论，不推公式 | 想先建立整体地图的读者 | 14 章 / 41 页 | [网页版](https://ai-crystal.github.io/Mamba/#/books/intro/chapters/ch01) ｜ [原文](books/intro/chapters/ch01.md) | [PDF 6.3 MB](output/mamba-intro.pdf ':ignore') |
| **专业版**《理论、算法与实现》 | 完整推导、算法细节、可运行代码 | 要做研究或实现的人 | 35 章 / 363 页 | [网页版](https://ai-crystal.github.io/Mamba/#/books/pro/chapters/ch01) ｜ [原文](books/pro/chapters/ch01.md) | [PDF 15.6 MB](output/from-lssl-to-mamba3.pdf ':ignore') |

建议先读入门版，再挑感兴趣的章节读专业版。两本各自完整，只读一本也不影响理解。

## 阅读入口

- [网页版站点](https://ai-crystal.github.io/Mamba/)　— 带搜索、侧栏与分册导航，手机上也能读
- [入门版前言](books/intro/front/preface.md) ｜ [入门版后记](books/intro/front/afterword.md)
- [专业版前言](books/pro/front/preface.md) ｜ [专业版后记](books/pro/front/afterword.md)
- [附录 A　数学工具箱](books/pro/appendix/appA.md) ｜ [附录 B　论文与术语](books/pro/appendix/appB.md) ｜ [附录 C　公式速查](books/pro/appendix/appC.md)

## 这本书想讲清楚的一件事

序列建模的核心问题只有一个，怎样用有限的存储记住任意长的历史。Transformer 的答案是不压缩，代价随长度二次增长；循环网络把历史压进固定状态，代价是压缩过程一旦设计得不好，信息就永久丢失。

从 2020 年的 HiPPO 到 2026 年的 Mamba-3，这条线一直在试第三种答案：用一个可学习的线性动力系统来压缩历史，让压缩方式本身由数据决定，同时保持线性的训练成本。书里逐个拆解这七个模型的动机、推导与取舍。

每一次进步都不是发明了新东西，而是把旧问题换了一个问法，再借来另一个领域已有的工具。

## 作者

Dr. Dezeming
