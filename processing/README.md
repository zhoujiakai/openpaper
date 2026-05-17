# 进行中

## ML

### 吴恩达机器学习

- 类型：网课
- 讲师：Andrew Ng（吴恩达）
- 链接：https://www.bilibili.com/video/BV16jyuBBEom
- 材料：https://github.com/fengdu78/Coursera-ML-AndrewNg-Notes
- 来源：经典网课
- 开始日期：2026-05-17
- 进度：01:34:46 / 19:36:58，第 13 / 142 集，约 8%
- 笔记：[ml-吴恩达机器学习/](ml-吴恩达机器学习/)

### 周志华机器学习

- 类型：书
- 作者：周志华
- 作者介绍：南京大学计算机系教授，欧洲科学院外籍院士，ACM Fellow，IEEE Fellow，AAAI Fellow，主要从事人工智能、机器学习、数据挖掘等领域研究，是中国最具影响力的机器学习学者之一。
- 出版年份：2016年
- 出版社：清华大学出版社
- 来源：经典教材，素有"西瓜书"之称
- 进度：第 0 / 16 章，约 0%
- 说明：中国机器学习领域经典入门教材，因封面为西瓜图案而俗称"西瓜书"。全书 16 章分三部分：基础（1-3 章）、经典方法（4-10 章）、进阶知识（11-16 章），覆盖监督学习、无监督学习、集成学习、深度学习等核心主题。适合初学者建立系统的机器学习认知框架。

### 机器学习基础算法（决策树/随机森林/SVM）
- 类型：技术主题学习（Mastery 三阶段工作流）
- 来源：sklearn 官方文档 + MIT 讲义 + GeeksforGeeks 面试题
- 紧急程度：高
- 关键词：决策树、随机森林、SVM、CART、Gini、熵、信息增益、Bagging、Boosting、核函数、RBF、剪枝、OOB、GridSearchCV
- 说明：从零基础出发，面试+实战两用。核心三件套：① 决策树（分裂准则 Gini/熵、预剪枝 vs 后剪枝、CART 二叉树）② 随机森林（Bootstrap + 随机特征双重随机、Bagging 降方差原理、OOB 误差估计、MDI 特征重要性及其局限）③ SVM（间隔最大化直觉、支持向量定义、Hard/Soft Margin、核技巧、C-γ 调参）
- 笔记：[ml-机器学习基础/](ml-机器学习基础/)

### LSTM
- 类型：技术主题学习
- 说明：长短期记忆网络（Long Short-Term Memory），循环神经网络的改进版本，解决长序列梯度消失问题。
- 笔记：[ml-lstm/](ml-lstm/)

## 算法

### LeetCode 热题100
- 类型：算法题解笔记
- 来源：LeetCode 官方学习计划
- 链接：https://leetcode.cn/studyplan/top-100-liked/
- 解题语言：Python 3
- 说明：LeetCode 热题 100 题解，涵盖 17 个主题（哈希、双指针、滑动窗口、子串、数组、矩阵、链表、二叉树、图论、回溯、二分查找、栈、堆、贪心、动态规划、多维动态规划、技巧），每题包含思路分析和代码实现
- 笔记：[se-LeetCode热题100/](se-LeetCode热题100/)

## 控制理论

### 江协科技 PID 入门教程（编码电机控制 / 倒立摆）

- 类型：网课
- 讲师：江协科技
- 链接：https://www.bilibili.com/video/av113576383612352
- 来源：B 站实战教程，PID 控制入门经典
- 总时长：约 8.3 小时，共 12 章
- 章节：
  1. 课程介绍、PID 基础、离散化 PID 与实现逻辑
  2. 电机驱动代码、编码器原理、SerialPlot 使用、PID 闭环实验
  3. 积分抗饱和、积分分离、微分先行、不完全微分
  4. 输出偏置、输入死区、双环 PID（速度+位置）
  5. 倒立摆系统设计、实现、自动起摆
- 笔记：[ctrl-江协PID倒立摆/](ctrl-江协PID倒立摆/)
- 开始日期：2026-05-17

## 英语

### 刘晓燕《考研英语你还在背单词吗》
- 类型：词汇学习笔记
- 作者：刘晓燕
- 链接：https://appfb9e4aqm2459.h5.xiaoeknow.com/p/course/column/p_678b5352e4b0694ca04c5f27
- 说明：基于《考研英语你还在背单词吗》整理的词汇笔记，按 Lesson 分组，标注重点词汇
- 笔记：[eng-刘晓燕英语/](eng-刘晓燕英语/)

## 软件工程

### Claude Code 源码

- 类型：开源项目源码学习
- 来源：https://github.com/shareAI-lab/learn-claude-code
- 进度：已完成 5/12 章，第 6 章待学习
- 说明：从零实现自己的 Claude Code（Anthropic 推出的终端 AI 编程助手，可直接编辑文件、执行命令、管理 Git 等工作流），包含 claw0 等模块。
- 笔记：[se-ClaudeCode源码/](se-ClaudeCode源码/)

### OpenClaw 源码

- 类型：开源项目源码学习
- 来源：https://github.com/shareAI-lab/claw0
- 主语言：Python（教学实现）
- 说明：通过 claw0 教学仓库学习 OpenClaw 架构。claw0 从零开始，每节一个可运行的 Python 文件（~7000 行），10 个 section 逐步构建 AI Agent Gateway：Agent Loop → Tool Use → Sessions → Channels → Gateway → Intelligence → Heartbeat → Delivery → Resilience → Concurrency。学完即可阅读 OpenClaw 生产代码。
- 笔记：[se-OpenClaw源码/](se-OpenClaw源码/)
