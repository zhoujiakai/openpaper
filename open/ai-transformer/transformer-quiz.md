# Transformer — 题库

> 生成时间：2026-04-24
> 题目数量：10
> 关联笔记：transformer-ai-notes.md

---

## 题目

### Q1 [选择题] Transformer 的 Encoder 每层包含哪些子层？

A. Self-Attention + Cross-Attention + FFN
B. Self-Attention + FFN
C. Masked Self-Attention + FFN
D. Masked Self-Attention + Cross-Attention + FFN

- **正确答案**：B
- **评分要点**：选择了正确选项即通过
- **知识点**：核心结构

### Q2 [选择题] Self-Attention 的计算复杂度是？

A. O(n·d)
B. O(n²·d)
C. O(n·d²)
D. O(n²·d²)

- **正确答案**：B
- **评分要点**：选择了正确选项即通过
- **知识点**：Self-Attention 复杂度

### Q3 [简答题] Decoder 的 Masked Self-Attention 为什么要加 mask？去掉会怎样？

- **参考答案**：
  1. Decoder 的训练任务是 next-token prediction
  2. 训练时输入是完整目标序列（teacher forcing）
  3. 不加 mask 则模型在预测第 t 个 token 时直接看到答案
  4. Mask 将未来位置的注意力权重设为 -inf，softmax 后为 0
- **评分要点**：
  1. 必须提到"防止看到未来/答案"
  2. 加分项：提到 teacher forcing 或训练时输入完整序列
- **知识点**：Masked Attention

### Q4 [简答题] GPT 系列为什么选择 Decoder-Only 架构？给出至少两个理由。

- **参考答案**：
  1. 训练数据无需配对：Decoder-Only 只需连续文本（预测下一个 token），不需要"A→B"配对数据，互联网文本都可用
  2. 规模涌现理解能力：足够大的模型通过预测下一个词，被迫学会语法、语义、推理（能生成就能理解）
  3. 架构简洁推理高效：KV Cache 实现简单，推理更快
- **评分要点**：
  1. 至少提到 2 个理由
  2. 第 1 个理由必须提到"数据不需要配对"
  3. 加分项：提到规模涌现
- **知识点**：GPT Decoder-Only

### Q5 [简答题] Multi-Head Attention 为什么要用多个头，而不是一个大的注意力头？

- **参考答案**：
  1. 不同 token 之间有多种关系（语法、语义、指代、位置等）
  2. 一个头需要同时学所有模式，容易冲突和平均化
  3. 多个头各自投影到不同子空间，独立学习不同关注模式
  4. 计算量不变（h × d_k = d_model）
- **评分要点**：
  1. 必须提到"避免不同模式的冲突/平均化"
  2. 需要说明每个头关注不同方面
  3. 加分项：提到计算量不变
- **知识点**：Multi-Head Attention

### Q6 [对比题] Encoder 和 Decoder 的 Self-Attention 有什么本质区别？各适合什么任务？

- **参考答案**：
  | 维度 | Encoder | Decoder |
  |------|---------|---------|
  | Mask | 无 mask，双向 | 有 mask，单向（因果） |
  | 上下文 | 能看到所有位置 | 只能看到之前位置 |
  | 适合任务 | 理解型（分类、NER、情感分析） | 生成型（对话、续写、代码） |
  | 代表模型 | BERT | GPT |

- **评分要点**：至少指出 3 个区别维度
- **知识点**：Encoder vs Decoder

### Q7 [对比题] Cross-Attention 和 Self-Attention 的区别？

- **参考答案**：
  | 维度 | Self-Attention | Cross-Attention |
  |------|---------------|-----------------|
  | Q/K/V 来源 | 全部来自同一层 | Q 来自 Decoder，K/V 来自 Encoder |
  | 作用 | 序列内部关联 | 跨序列信息查阅 |
  | 出现位置 | Encoder + Decoder | 仅 Decoder |

- **评分要点**：至少指出 Q/K/V 来源的区别
- **知识点**：Cross-Attention

### Q8 [简答题] 为什么 Transformer 需要 Positional Encoding？

- **参考答案**：
  1. Self-Attention 是位置无关的（permutation equivariant）
  2. 只关心 token 两两关系，不关心位置
  3. 没有 Positional Encoding 时，"我爱北京"和"北京爱我"对模型等价
  4. Positional Encoding 为每个位置注入唯一的位置标签
- **评分要点**：
  1. 必须提到 Attention 本身不关心位置/顺序
  2. 必须提到 Positional Encoding 的作用是注入位置信息
- **知识点**：Positional Encoding

### Q9 [简答题] 残差连接在 Transformer 中的作用是什么？

- **参考答案**：
  1. 前向传播：浅层特征直接传到深层，不丢失
  2. 反向传播：梯度通过捷径回流，避免梯度消失
  3. 公式：LayerNorm(x + Sublayer(x))
- **评分要点**：
  1. 需要同时提到前向和反向两个作用
  2. 加分项：提到具体公式
- **知识点**：残差连接

### Q10 [应用题] 假设你要做一个"文档摘要"系统，输入一篇长文章，输出一段摘要。你会选择 Encoder-Only、Decoder-Only 还是 Encoder-Decoder？为什么？

- **参考答案**：选 Encoder-Decoder。原因：
  1. 需要双向理解完整文章（Encoder 的强项）
  2. 需要自回归生成摘要文本（Decoder 的强项）
  3. 通过 Cross-Attention 在生成时查阅原文关键信息
- **评分要点**：
  1. 正确选择 Encoder-Decoder
  2. 给出理由：同时需要理解+生成
  3. 加分项：提到 Cross-Attention 的作用
- **知识点**：综合应用

---

## 测试记录

### 2026-04-24 A4 默写测试

| 知识点 | 结果 | 备注 |
|--------|------|------|
| 核心结构 | 🟢 通过 | 遗漏残差+LayerNorm，已补充 |
| Masked Attention | 🟢 通过 | |
| Encoder vs Decoder | 🟢 通过 | 翻译不属于 Encoder-Only，已纠正 |
| GPT 为什么只用 Decoder | 🟢 通过（重测） | 首次未通过，重测通过 |
| Multi-Head Attention | 🟢 通过 | |
| 残差连接 | 🟢 通过 | |
| Positional Encoding | 🟢 通过（引导后） | 新知识点，经提示后掌握 |
| Self-Attention 复杂度 | 🟢 通过 | |

通过率：8/8（100%）
下次回测：2026-05-01 周测
