# Transformer — QA

> 学习过程中困惑的点
> 创建日期：2026-04-29

---

## Q1：残差连接 + LayerNorm（反复遗漏）

**每经过一个子层，都要加上输入（残差）再做归一化。** 这是 Transformer 层的标准模式，不是可选项。

- Encoder 层：`Multi-Head Self-Attention → Add & Norm` → `FFN → Add & Norm`
- Decoder 层：`Masked Self-Attention → Add & Norm` → `Cross-Attention → Add & Norm` → `FFN → Add & Norm`

残差连接的两个作用：
1. **前向保特征**：浅层特征直达深层，不丢失
2. **反向传梯度**：梯度可以走捷径直接回传，缓解深层网络的梯度消失

---

## Q2：Positional Encoding 的原因（缺关键术语）

Self-Attention 是 **permutation equivariant（置换等变）** 的：打乱输入 token 顺序，输出只是跟着打乱，模型完全察觉不到。所以 Self-Attention **只看关系不看位置**，必须额外注入位置信息。

---

## Q3：Encoder vs Decoder 的本质区别

不是"看到全局信息"vs"逐字吐出"，而是**注意力的方向性**：
- **Encoder = 双向注意力**（能看到前后所有位置）→ 适合理解型任务（分类、NER），代表 BERT
- **Decoder = 单向注意力（masked）**（只能看过去）→ 适合生成型任务（对话、代码），代表 GPT
- **Encoder-Decoder = 先双向理解再单向生成** → 适合翻译、摘要，代表 T5、BART

---

## Q4：GPT 为什么只用 Decoder（3 个理由）

1. **训练数据无需配对**：Decoder-Only 的预训练任务 = 预测下一个 token，互联网上任何文本都能当训练数据。Encoder-Decoder 需要配对数据（如翻译对），数据规模有瓶颈
2. **规模涌现**：足够大的模型，生成能力会涌现出理解能力。"能生成就能理解，但能理解不一定能生成"
3. **架构简洁 + KV Cache 友好**：所有 token 共享相同的因果注意力模式，推理时缓存已计算的 K/V，只算新 token

---

## Q5：Cross-Attention 的作用

Q 来自 Decoder，K/V 来自 Encoder。**让 Decoder 在生成每个词时，能"回头看" Encoder 编码的输入信息，决定当前应该关注输入的哪些部分。** 没有它，Decoder 就是在凭空生成，跟输入没关系。

---

