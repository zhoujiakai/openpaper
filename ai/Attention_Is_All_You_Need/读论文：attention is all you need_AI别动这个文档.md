# Attention Is All You Need

- 类型：论文，2017年6月 arXiv 首发
- 作者：Ashish Vaswani、Illia Polosukhin（Google Brain 团队）等
- 来源：NeurIPS 2017 (Conference on Neural Information Processing Systems)
- 链接：
    - arXiv: https://arxiv.org/abs/1706.03762
    - NeurIPS: https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
- 被引用数：171,777+（Semantic Scholar，截止2026年4月6日）



## 摘要

讨论对象：序列转换模型。

旧方法：循环神经网络和卷积神经网络，包含编码器和解码器，最优秀的模型还会使用注意力机制将编码器和解码器连接起来。

新方法：论文提出：Transformer，只使用注意力机制，不再使用任何循环神经网络或卷积神经网络。

效果好：质量高、并行性好。泛化性好。

- 质量高：在 WMT 2014 英德翻译任务上，达到 28.4 BLEU，比最好的模型高 2 BLEU 以上。
- 并行性好：在 WMT 2014 英法翻译任务上，使用 8 块 GPU 上花费3.5天，达到 41.8 BLEU，成本仅是最好模型的一小部分。
- 泛化性好：在英语句法成分分析任务上，成功应用，无论训练数据是多是少。



## 1 引言

（铺垫）拔高RNN：RNN 是王者

（诊断）打倒RNN：RNN 天生串行，没法并行

（验证）验证：别人试过优化，无法根本解决

（转机）引出关键角色：注意力很强，却一直在RNN主导的模型中打辅助

（亮相）拿出最终解决方案：Transformer 让注意力当主角，完全摒弃RNN

（亮相）验证：8 块 P100 GPU 上训练 12 小时就达到翻译任务的 SOTA



## 2 背景

别人都试过什么？为什么还不够？

铺垫：CNN 路线，并行了，可是远距离连接仍需 O(n) 或 O(log n) 步

亮相：Transformer 的优势 O(1)，代价是平均，用多头弥补

来源：Self-attention 和 Memory Networks，注意力已经被用过，但没有当过主角

总结陈词：我们是第一个完全用 self-attention 的转换模型



## 3 模型架构



### 3.1 编码器和解码器堆叠

#### 编码器

N = 6 堆叠

每层两个子层

#### 解码器

N = 6 堆叠

每层3个子层

### 3.2 注意力



#### 3.2.1 缩放点积注意力



#### 3.2.2 多头注意力



#### 3.2.3 注意力在 Transformer 中的三种应用



### 3.3 逐位置前馈网络



### 3.4 嵌入和 Softmax



### 3.5 位置编码



## 4 为什么用自注意力



## 5 训练



## 6 结果



## 7 结论

