# RAG — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-29（上次 2026-04-24）

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现 | ✅ 已完成 | AI 笔记已生成 |
| 2. 深度理解 | ✅ 已完成 | Section 8/8 |
| 3. 知识检验 | ✅ 已完成 | 掌握度 80%，A4 默写 + 补强重测完成 |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: 为什么需要 RAG — LLM 的局限性 | ✅ 精读完成 | 完全掌握 |
| Section 2: RAG 完整链路 — 四个阶段 | ✅ 精读完成 | 完全掌握 |
| Section 3: Chunking 策略详解 | ✅ 精读完成 | 基本掌握 |
| Section 4: Embedding 模型与向量数据库 | ✅ 精读完成 | 完全掌握 |
| Section 5: 混合检索与 Reranking | ✅ 精读完成 | 完全掌握 |
| Section 6: LangChain RAG 实战流水线 | ✅ 精读完成 | 完全掌握 |
| Section 7: RAG vs 微调 vs 长上下文 | ✅ 精读完成 | 完全掌握 |
| Section 8: Agentic RAG — RAG 的进化方向 | ✅ 精读完成 | 完全掌握 |

## 下次从哪里继续

进入间隔重复回测阶段：
- 周测：2026-05-01 → ✅ 2026-04-29 已完成（掌握度 83%）
- 月测：2026-05-24

## 已掌握的关键知识点

### RAG 四阶段
Ingestion（分块+嵌入+存库）→ Retrieval（query 向量化+相似性搜索）→ Augmentation（拼入 prompt）→ Generation（LLM 生成）

### Chunking 策略
固定大小+overlap 是通用基线；有结构的文档用递归分块；围绕数据天然语义单元设计

### 混合检索 + Reranking
Dense（语义）+ Sparse（关键词）→ Reranking（bi-encoder 粗筛 + cross-encoder 精排）

### RAG vs 微调 vs 长上下文
知识不足→RAG，行为/格式不对→微调，全文理解→长上下文

### Agentic RAG
传统 RAG 查一次就完，Agentic RAG 有反馈循环（评估→改 query→重查）

## 被纠正过的误区

- RAG 四阶段和 LangChain 五步是不同框架，不能混用。RAG：Ingestion→Retrieval→Augmentation→Generation；LangChain：Load→Split→Store→Retrieve→Generate
- 长上下文不是 RAG，是两种不同思路。RAG 检索关键段落，长上下文一次性喂入全文
- Reranking 不是 LLM，是专用的 BERT 编码器模型（cross-encoder）
- 语义分块不一定优于固定大小分块，实测效果需要验证
- Reranking 的核心不是混合搜索合并，而是 cross-encoder 比 bi-encoder 精度更高但更慢，所以两阶段平衡

## 需要复习的内容

1. 六种 Chunking 策略的后三种具体场景
2. LangChain 五步不要多加 Reranking
3. 生成偏离排查要从生成端分析（Prompt 约束、模型知识干扰、few-shot）
