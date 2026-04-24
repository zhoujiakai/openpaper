# Transformer — AI 笔记

> 来源：
> - Attention Is All You Need（论文原文，已完成精读，位于 closed/Attention_Is_All_You_Need/）
> - [3Blue1Brown: Attention in Transformers, Step-by-Step](https://www.3blue1brown.com/lessons/attention/)
> - [3Blue1Brown: But what is a GPT?](https://www.3blue1brown.com/lessons/gpt)
> - [Cameron R. Wolfe: Decoder-Only Transformers](https://cameronrwolfe.substack.com/p/decoder-only-transformers-the-workhorse)
> - [Hugging Face LLM Course: Transformer Architectures](https://huggingface.co/learn/llm-course/en/chapter1/6)
> - [Dive into Deep Learning: Multi-Head Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html)
> - [Sebastian Raschka: Understanding Self-Attention & Multi-Head Attention](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)
>
> 生成时间：2026-04-24
> 学习目标：面试准备 — 能清晰回答 Transformer 的四个核心问题

---

## 一句话总结

Transformer 是一种完全基于注意力机制的序列处理架构，用 Self-Attention 替代 RNN 的顺序计算，实现了全局依赖建模和高度并行化；它的三个变体（Encoder-Only、Decoder-Only、Encoder-Decoder）分别支撑了 BERT、GPT、翻译模型等不同任务。

---

## 核心概念

| # | 概念 | 定义 | 关键细节 |
|---|------|------|----------|
| 1 | Self-Attention | 让序列中每个位置直接关注所有其他位置的机制 | Q/K/V 三元组，权重 = softmax(QK^T / sqrt(d_k))，输出是 V 的加权和 |
| 2 | Multi-Head Attention | 并行运行多个独立的 Self-Attention，拼接后投影 | 每个头学习不同的"关注模式"，捕捉不同类型的关系 |
| 3 | Encoder | 双向理解输入序列的组件 | 每层 = Multi-Head Self-Attention + FFN，能看到完整输入 |
| 4 | Decoder | 自回归生成输出序列的组件 | 每层 = Masked Self-Attention + Cross-Attention + FFN，不能看到未来 |
| 5 | Positional Encoding | 给无序的注意力机制注入位置信息 | 正弦/余弦函数或可学习嵌入，因为 Attention 本身是位置无关的 |
| 6 | Masked Attention | 防止解码器在生成时"偷看"未来信息 | 将未来位置的注意力权重设为 -inf，softmax 后变为 0 |

---

## Section 1: Transformer 的核心结构

### 整体架构：Encoder-Decoder

原始 Transformer（2017）为机器翻译设计，采用 **Encoder-Decoder** 结构：

```
输入序列 ──→ [Encoder × N] ──→ 编码表示 z ──→ [Decoder × N] ──→ 输出序列
```

**Encoder**：将输入序列 $(x_1, ..., x_n)$ 编码为连续表示 $\mathbf{z} = (z_1, ..., z_n)$。

**Decoder**：给定 $\mathbf{z}$，自回归地逐个生成输出序列 $(y_1, ..., y_m)$。

### 每个 Encoder 层的组成

```
Input
  ↓
  ├── Multi-Head Self-Attention ──→ Add & LayerNorm
  ↓
  ├── Feed-Forward Network (FFN) ──→ Add & LayerNorm
  ↓
Output (维度始终 = d_model = 512)
```

关键设计：
- **残差连接（Add）**：`output = LayerNorm(x + Sublayer(x))`，缓解深层网络的梯度消失
- **LayerNorm**：对每个样本的每个位置独立归一化，稳定训练
- **维度统一**：所有子层输出维度 = d_model，方便残差连接

### 每个 Decoder 层的组成

```
Input
  ↓
  ├── Masked Multi-Head Self-Attention ──→ Add & LayerNorm  (自己看自己，不能看未来)
  ↓
  ├── Cross-Attention (Q 来自 Decoder，K/V 来自 Encoder) ──→ Add & LayerNorm
  ↓
  ├── Feed-Forward Network (FFN) ──→ Add & LayerNorm
  ↓
Output
```

Decoder 比 Encoder 多了一个 **Cross-Attention**（交叉注意力），用于"查阅"Encoder 编码的输入信息。

### 类比理解

把 Transformer 想象成一个翻译团队：

| 组件 | 类比 | 作用 |
|------|------|------|
| Encoder | 阅读理解专家 | 通读源语言全文，理解每个词的上下文含义 |
| Cross-Attention | 翻译时的"回头看原文" | 生成每个输出词时，决定该关注源文的哪些部分 |
| Masked Self-Attention | "只能看到已写好的部分" | 翻译第 5 个词时不能偷看第 6 个词 |

---

## Section 2: Encoder 和 Decoder 各自的作用

### Encoder 的作用：**双向理解**

Encoder 中的 Self-Attention 是 **无 mask 的**，每个位置可以关注所有位置（包括前后）。

这意味着：
- "bank" 这个词能同时看到 "river"（前面）和 "money"（后面）
- 产生的是**上下文感知的表示**（contextualized representation）
- 同一个词在不同语境下会有不同的编码

**典型应用**：BERT（Encoder-Only），适合理解型任务：
- 文本分类（情感分析）
- 命名实体识别（NER）
- 问答系统中的"阅读理解"

### Decoder 的作用：**自回归生成**

Decoder 中的 Self-Attention 是 **masked 的**，每个位置只能关注之前的位置。

这意味着：
- 生成第 t 个 token 时，只能看到 token 1 到 t-1
- 必须基于已生成的内容"预测下一个"
- 本质是一个 **next-token prediction** 任务

**典型应用**：GPT（Decoder-Only），适合生成型任务：
- 文本续写
- 对话生成
- 代码生成

### Encoder-Decoder 的作用：**先理解再生成**

两个组件协同：
1. Encoder 先双向理解输入
2. Decoder 通过 Cross-Attention 查阅 Encoder 的输出
3. Decoder 自回归地生成输出

**典型应用**：
- 机器翻译（原文 → 译文）
- 文本摘要（长文 → 短文）
- T5、BART 等模型

### 对比总结

| 维度 | Encoder | Decoder (Masked) | Encoder-Decoder |
|------|---------|-------------------|-----------------|
| 注意力方向 | 双向 | 单向（只看过去） | 编码双向 + 生成单向 |
| 训练方式 | Masked LM（遮盖预测） | Next-token prediction | Teacher forcing |
| 代表模型 | BERT | GPT | T5, BART, 原始 Transformer |
| 擅长 | 理解/分类/标注 | 生成/对话/续写 | 翻译/摘要 |
| 能否看到全文 | 能 | 不能 | Encoder 能，Decoder 不能 |

---

## Section 3: GPT 系列为什么只用 Decoder？

### 核心答案

GPT 系列选择 Decoder-Only 架构，原因是：**统一任务为 next-token prediction，使所有文本数据都能作为训练数据，无需配对数据，规模化能力更强。**

### 详细分析

#### 1. 训练数据的可获得性

| 架构 | 训练需要什么 | 数据规模瓶颈 |
|------|------------|-------------|
| Encoder-Decoder | 配对的输入-输出（如英德句子对） | 翻译数据有限 |
| Encoder-Only (BERT) | 无标注文本 + 人工构造的遮盖任务 | 遮盖预测 ≠ 生成能力 |
| **Decoder-Only (GPT)** | **任何文本序列** | **几乎无限** |

Decoder-Only 的预训练任务 = "给定前面的 token，预测下一个 token"。互联网上的每一篇文章、每一段对话、每一行代码都是天然的训练数据。

#### 2. 能力的涌现

Andrej Karpathy 的解释（[Reddit 来源](https://www.reddit.com/r/MachineLearning/comments/14onn56/d_eli5_why_is_the_gpt_family_of_models_based_on/)）：

> 原始 Transformer 的 Encoder 在翻译场景下有意义（需要双向理解源语言）。但对于通用语言建模，next-token prediction 已经足够 — 随着模型规模增大，生成能力涌现出理解能力。

简单说：**能生成，就能理解；但能理解，不一定能生成。**

#### 3. 架构简洁性

Decoder-Only 的优势：
- 所有 token 共享相同的注意力模式（均为 causal/masked）
- KV Cache 实现更简单（推理时缓存已计算的 K/V，只需计算新 token）
- 扩展性已被验证（GPT-4、Claude、Llama 均为 Decoder-Only）

#### 4. 为什么不用 Encoder-Decoder 做 LLM？

可以，但不是主流：
- T5 是 Encoder-Decoder，但在纯生成任务上不如 Decoder-Only 高效
- Encoder-Decoder 的推理需要同时维护编码和解码两个部分
- 对于开放式对话/生成，Encoder（双向理解）的优势体现不明显

### 一句话总结

GPT 用 Decoder-Only，不是因为 Encoder 没用，而是因为 next-token prediction 这个单一任务 + 海量数据 + 足够大的模型，已经能涌现出足够强的通用能力。

---

## Section 4: Multi-Head Attention 的意义

### 直觉理解

想象你在阅读一句话："The animal didn't cross the street because **it** was too tired."

理解 "it" 指代什么，需要同时考虑：
- **语法关系**："it" 是从句的主语
- **语义指代**："it" 可能指 animal 或 street
- **常识推理**：tired 的通常是 animal 而不是 street

**一个注意力头很难同时捕捉所有这些关系。**

### Multi-Head 做了什么

把 Q、K、V 分别投影到 h 个不同的低维子空间，在每个子空间独立计算注意力，最后拼接：

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) · W_O

其中 head_i = Attention(Q · W_Q_i, K · W_K_i, V · W_V_i)
```

原始论文：h = 8 个头，每个头的维度 = d_model / h = 512 / 8 = 64。

### 每个头学到什么

研究发现，不同的头确实学到了不同的关注模式：

| 头的类型 | 学到的模式 | 示例 |
|----------|----------|------|
| 语法头 | 关注句法结构 | 主语关注谓语 |
| 指代头 | 关注代词指代 | "it" 关注 "animal" |
| 位置头 | 关注相邻 token | 关注前一个或后一个词 |
| 语义头 | 关注语义相关词 | "bank" 关注 "money" 或 "river" |

### 为什么不直接用一个大头？

理论上，一个维度为 512 的单头注意力也能学到这些模式。但：

1. **优化更容易**：多个小头各自学习一个简单模式，比一个复杂函数更容易优化
2. **表示子空间**：每个头投影到不同的子空间，有更多"视角"看同一个输入
3. **鲁棒性**：即使某个头没学好，其他头仍能提供有用信息
4. **计算量不变**：h 个 d_k 维头的计算量 = 1 个 d_model 维头

### 类比

| 类比 | 解释 |
|------|------|
| 多人审稿 | 一篇论文让 8 位审稿人看，每人关注不同方面（创新性、实验、写作），综合意见比一人更全面 |
| 多角度拍照 | 同一物体从 8 个角度拍，比一张正面照信息更丰富 |
| 集成学习 | 类似随机森林中多棵树各自学不同特征，合起来更强 |

---

## 面试高频考点

| 考点 | 标准答案要点 | 常见错误 |
|------|-------------|----------|
| Transformer 核心结构 | Encoder-Decoder，每层 = Self-Attention + FFN + 残差 + LayerNorm | 忘记提残差连接和 LayerNorm |
| Encoder vs Decoder | Encoder 双向无 mask，Decoder 单向有 mask；Decoder 多一个 Cross-Attention | 混淆 Masked Attention 和普通 Self-Attention 的区别 |
| GPT 为什么只用 Decoder | Next-token prediction 天然适合生成；训练数据无需配对；规模增大涌现理解能力 | 误以为 Encoder 没用，实际是 Decoder-Only 在规模化上更优 |
| Multi-Head Attention | 多个子空间独立关注，捕捉不同关系模式；计算量不变 | 以为多头增加计算量；不知道每个头维度 = d_model/h |
| Self-Attention 计算复杂度 | O(n²·d)，n 是序列长度 | 忘记序列长度的二次方复杂度是 Transformer 的瓶颈 |
| Positional Encoding | Attention 本身是排列不变的，需要额外注入位置信息 | 不知道为什么需要位置编码 |

---

## 与其他架构的对比

| 维度 | Transformer | RNN/LSTM | CNN |
|------|-------------|----------|-----|
| 并行性 | 高（所有位置同时计算） | 低（必须顺序计算） | 中（局部并行） |
| 长距离依赖 | O(1) 步直达 | O(n) 步传递 | O(n/k) 步传递 |
| 计算复杂度 | O(n²·d) | O(n·d²) | O(n·k·d²) |
| 适合短序列 | 不如 RNN 高效 | 高效 | 高效 |
| 适合长序列 | 注意力复杂度爆炸 | 梯度消失 | 受限于感受野 |
