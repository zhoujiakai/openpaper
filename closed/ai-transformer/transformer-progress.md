# Transformer — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-29（上次 2026-04-24）

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现与整理 | ✅ 已完成 | 4 个 Section 全部生成 |
| 2. 深度理解（苏格拉底式精读） | ✅ 已完成 | 4/4 Section |
| 3. 知识检验（A4 默写） | ✅ 已完成 | 周测掌握度 82% |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: 核心结构 | ✅ | 良好 — 正确理解 mask 的作用和残差连接 |
| Section 2: Encoder 和 Decoder 各自的作用 | ✅ | 良好 — 经引导后理解双向 vs 单向的本质区别 |
| Section 3: GPT 为什么只用 Decoder | ✅ | 良好 — 正确理解数据配对差异和规模涌现 |
| Section 4: Multi-Head Attention 的意义 | ✅ | 很好 — 独立说出多模式冲突和子空间分离 |

## 已掌握的关键知识点

### Section 1: 核心结构
- Mask 防止训练时"偷看"答案
- 残差连接的作用：前向保特征 + 反向传梯度

### Section 2: Encoder 和 Decoder 各自的作用
- Encoder 双向理解，Decoder 单向生成
- 情感分析等理解型任务适合 Encoder（BERT）
- Cross-Attention：Q 来自 Decoder，K/V 来自 Encoder

### Section 3: GPT 为什么只用 Decoder
- Decoder-Only 无需配对数据，任何文本都可训练
- 规模涌现：足够大的模型通过预测下一个词涌现出理解能力

### Section 4: Multi-Head Attention
- 多头避免不同关注模式的冲突和平均化
- 计算量不变（h × d_k = d_model）

## 被纠正过的误区

- 用"低维度到高维度"描述残差连接 → 应为"浅层到深层"，维度不改变
- 对 Encoder-Decoder 和 Decoder-Only 的数据区别，最初只想到长度问题 → 核心区别是"配对数据 vs 连续文本"
