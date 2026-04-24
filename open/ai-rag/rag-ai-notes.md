# RAG（Retrieval-Augmented Generation）— AI 笔记

> 来源：
> 1. Pinecone 官方 RAG 指南 — https://www.pinecone.io/learn/retrieval-augmented-generation/
> 2. Pinecone RAG 电子书系列 — https://www.pinecone.io/learn/series/rag/
> 3. LangChain 官方 RAG 教程（中文） — https://www.langchain.com.cn/docs/tutorials/rag/
> 4. Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — https://arxiv.org/abs/2005.11401
> 5. 腾讯云 RAG 技术全解析 — https://cloud.tencent.com/developer/article/2649862
> 6. CSDN RAG 原理流程实战 — https://blog.csdn.net/weixin_43882318/article/details/158810432
> 生成时间：2026-04-24
> 学习目标：面试准备 — 理解 RAG 每个环节背后的工程决策

---

## 一句话总结

RAG 是一种在 LLM 生成回答前，先从外部知识库中检索相关文档，将检索结果作为上下文喂给模型的技术，目的是减少幻觉、提供准确的领域知识。

## 核心概念

| # | 概念 | 定义 | 关键细节 |
|---|------|------|----------|
| 1 | RAG | 检索增强生成，在生成前先检索外部知识 | 不修改模型参数，是"外挂式"知识增强 |
| 2 | Ingestion（索引） | 将原始数据加载、分块、嵌入、存入向量数据库 | 离线进行，数据更新时实时刷新 |
| 3 | Retrieval（检索） | 根据用户 query 从向量数据库中找到最相关的文档块 | 语义搜索、关键词搜索、混合搜索 |
| 4 | Augmentation（增强） | 将检索结果和用户 query 组装成增强 prompt | 关键：让模型基于检索到的内容回答 |
| 5 | Generation（生成） | LLM 基于增强 prompt 生成最终回答 | 模型被引导使用检索到的上下文 |
| 6 | Chunking（分块） | 将长文档拆分成小块便于索引和检索 | 策略选择是 RAG 效果的关键变量 |
| 7 | Embedding（嵌入） | 将文本转换为高维向量表示 | 嵌入模型质量直接影响检索精度 |
| 8 | Reranking（重排） | 对检索结果进行二次排序，提升相关性 | 两阶段检索：先粗筛再精排 |
| 9 | Hybrid Search（混合搜索） | 结合语义搜索（dense）和关键词搜索（sparse） | 同时捕捉语义和精确匹配 |
| 10 | Agentic RAG | 用 Agent 编排 RAG 各环节 | Agent 决定查什么、用什么工具、结果可信度 |

## 关键公式 / 代码模式

| 公式/模式 | 含义 | 记忆要点 |
|-----------|------|----------|
| `cos(q, d) = (q·d) / (|q|×|d|)` | 余弦相似度，衡量 query 和文档向量的相关性 | 最常用的相似性度量 |
| `dense + sparse → rerank → top-k` | 混合检索 + 重排的标准流水线 | 两阶段：粗筛→精排 |
| `chunk_size=1000, chunk_overlap=200` | LangChain 默认分块参数 | overlap 防止上下文被截断 |
| `vectorstore.as_retriever(search_type="similarity", k=6)` | LangChain 检索器配置 | k 值决定返回多少文档块 |
| Prompt: `{CONTEXT} + {QUESTION} → Answer` | 增强提示词的标准结构 | 核心指令："基于 CONTEXT 回答，不知道就说不知道" |

## 逐节详解

### Section 1: 为什么需要 RAG — LLM 的局限性

LLM 有五个核心局限性，RAG 正是为了解决它们：

1. **知识截止（Knowledge Cutoff）**：模型训练数据冻结在某个时间点，无法回答最新信息
2. **领域深度不足**：通用模型在专业领域（如医疗、法律）的回答可能不完整或不准确
3. **缺少私有数据**：企业内部数据（流程、政策、邮件）不在训练集中
4. **无法溯源**：模型不能引用来源，用户无法验证回答的准确性
5. **概率性输出**：模型对所有可能的续接都分配概率，可能选择错误的续接（幻觉）

RAG 的四个核心优势：
- 访问实时数据和私有/领域数据
- 建立信任（可提供来源引用）
- 更强的可控性（控制数据源、检索策略、安全合规）
- 比微调/重训成本更低

### Section 2: RAG 完整链路 — 四个阶段

RAG 的完整链路是一个四阶段流水线：**Ingestion → Retrieval → Augmentation → Generation**

**阶段 1：Ingestion（索引/入库）**

三个子步骤：
1. **数据清洗 + 分块（Chunking）**：将原始文档（PDF、网页、邮件等）拆成小块
2. **创建向量嵌入（Embedding）**：用 Embedding 模型将每个文本块转成高维向量
3. **存入向量数据库**：如 Pinecone、Chroma、Milvus、Weaviate

> 索引通常是离线进行的。数据更新时可实时刷新索引。

**阶段 2：Retrieval（检索）**

1. 将用户的 query 也通过同一个 Embedding 模型转成向量
2. 在向量数据库中做相似性搜索（如余弦相似度）
3. 返回最相关的 top-k 文档块

高级检索方式：
- **混合搜索**：语义搜索（dense vector）+ 关键词搜索（sparse vector，如 BM25）
- **Multi-Query**：将用户 query 改写成多个变体，提高召回率
- **最大边际相关性（MMR）**：在相关性和多样性之间平衡，避免返回重复内容

**阶段 3：Augmentation（增强）**

将检索到的文档块和用户 query 组装成增强 prompt：

```
QUESTION: <用户的问题>
CONTEXT: <检索到的相关文档块>

基于 CONTEXT 回答 QUESTION。如果 CONTEXT 中没有答案，就说不知道。
```

**阶段 4：Generation（生成）**

LLM 基于增强 prompt 生成最终回答。关键点：模型被引导使用检索到的上下文，而不是依赖自身的参数记忆。

### Section 3: Chunking 策略详解

分块策略是 RAG 效果的关键变量——**分块质量对检索精度的影响甚至大于 Embedding 模型的选择**。

| 策略 | 原理 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|----------|
| **固定大小分块** | 按字符数/词数切割 | 简单高效，稳定可靠 | 可能切断句子或语义 | 通用基线方案 |
| **固定大小 + 重叠** | 相邻块之间有 N 字符重叠 | 保留上下文连贯性 | 增加存储和冗余 | 最常用的通用方案 |
| **按句子分块** | 以句子边界切割 | 尊重自然语言结构 | 块大小不一，可能组合无关句子 | 短文本场景 |
| **语义分块** | 按语义相似度分组 | 理论上最优 | 计算成本高，实测不一定优于固定大小 | 需要高精度的场景 |
| **递归/结构感知** | 按文档层级（段落、章节）递归切割 | 尊重文档结构 | 需要结构化输入 | 有明确结构的文档 |
| **LLM 驱动分块** | 用 LLM 决定分块边界 | 最具上下文感知 | 成本最高，延迟最大 | 对质量要求极高的场景 |

关键发现（来自学术研究）：
- 固定大小分块（200-1000 字符）在很多基准测试中表现不亚于语义分块
- RecursiveCharacterTextSplitter（递归字符分割器）是 LangChain 推荐的通用分割器
- chunk_size 和 chunk_overlap 的选择需要根据数据类型和查询模式调优

### Section 4: Embedding 模型与向量数据库

**Embedding 模型选择维度：**
- 向量维度（dimension）：影响存储和计算成本
- 多语言支持
- 领域特化（如医疗、法律）
- 性能基准（MTEB 排行榜）

常见 Embedding 模型：
- OpenAI `text-embedding-3-small/large`
- Cohere `embed-multilingual`
- BGE 系列（开源，中文友好）
- E5 系列（微软，多语言）

**向量数据库对比：**

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| Pinecone | 全托管，开箱即用 | 快速上线、不想运维 |
| Chroma | 轻量级，本地运行 | 开发测试、小规模应用 |
| Milvus | 开源，高性能 | 大规模生产环境 |
| Weaviate | 开源，支持混合搜索 | 需要多模态搜索 |
| Qdrant | Rust 实现，高性能 | 性能敏感场景 |

### Section 5: 混合检索与 Reranking

**为什么纯向量检索不够？**

纯语义搜索（dense）的局限：
- 对领域专有名词、缩写、产品名称可能检索不准
- 无法精确匹配关键词（如错误码、型号）

纯关键词搜索（sparse，如 BM25）的局限：
- 无法理解同义词、语义相近但用词不同的查询
- 无法捕捉语义层面的相关性

**混合搜索的原理：**
1. 同时进行 dense search（语义）和 sparse search（关键词）
2. 合并两个结果集（去重）
3. 用 Reranking 模型重新排序

**什么是 Reranking？**

Reranking 是两阶段检索的第二阶段：
- 第一阶段（粗筛）：向量相似性搜索快速返回 top-k（如 top-100）候选
- 第二阶段（精排）：Reranker 模型对候选进行更精确的相关性打分，选出最终 top-k（如 top-10）

常用 Reranker：
- Cohere Rerank（API 服务）
- cross-encoder 模型（如 `bge-reranker-large`）
- LLM 作为 Reranker

为什么需要 Reranking？因为：
- 向量相似性搜索是双塔模型（query 和 doc 独立编码），精度有限
- Reranker 用 cross-encoder（query 和 doc 一起编码），精度更高但速度更慢
- 所以用两阶段：先快后准

### Section 6: LangChain RAG 实战流水线

LangChain 的 RAG 流水线由 5 步组成：

```
加载(Load) → 分割(Split) → 存储(Store) → 检索(Retrieve) → 生成(Generate)
```

**核心组件：**
1. **DocumentLoader**：从数据源加载文档（160+ 集成）
2. **TextSplitter**：将文档分割成块（RecursiveCharacterTextSplitter 推荐）
3. **VectorStore + Embeddings**：嵌入并存储到向量数据库
4. **Retriever**：根据 query 检索相关文档块
5. **LLM + Prompt**：基于检索结果生成答案

**LCEL 链式调用：**
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**高级检索技术：**
- **MultiQueryRetriever**：将 query 改写成多个变体，提高召回
- **MultiVectorRetriever**：为每个文档生成多个嵌入，提高命中
- **MMR（最大边际相关性）**：平衡相关性和多样性
- **SelfQueryRetriever**：从 query 中自动提取元数据过滤条件

### Section 7: RAG vs 微调 vs 长上下文

| 维度 | RAG | 微调（Fine-tuning） | 长上下文（Long Context） |
|------|-----|---------------------|------------------------|
| 数据时效性 | 实时更新 | 需重新训练 | 取决于输入数据 |
| 成本 | 低（只需索引和检索） | 高（需要训练数据和 GPU） | 中（长上下文 token 费用高） |
| 幻觉控制 | 好（基于检索事实） | 一般 | 一般 |
| 定制化 | 数据层面 | 模型风格/行为层面 | 数据层面 |
| 适用场景 | 实时数据、私有数据、Q&A | 改变模型输出风格/格式 | 全文分析、长文档理解 |
| 知识更新 | 即时（更新索引） | 慢（需要重训） | 即时（更新输入） |

选择建议：
- 需要实时/私有数据 → RAG
- 需要改变模型行为/风格 → 微调
- 需要分析整个长文档 → 长上下文
- 可以组合使用：RAG + 微调

### Section 8: Agentic RAG — RAG 的进化方向

传统 RAG 是一条简单的线性流水线。Agentic RAG 让 Agent 成为 RAG 的编排者：

**Agent 在 RAG 中做什么？**
- 构建更有效的查询（Query Rewriting）
- 选择合适的检索工具
- 评估检索结果的相关性和准确性
- 应用推理来验证信息，决定信任或丢弃
- 迭代优化：如果结果不满意，修改查询重新检索

**Agentic RAG 架构：**
```
用户查询 → Agent（LLM）→ 决定用哪些工具 → 调用检索工具 → 评估结果 → 生成/重试
```

**GraphRAG（2024-2025 重要突破）：**
- 在传统向量检索基础上引入知识图谱
- 捕捉实体间的结构化关系
- 支持更复杂的推理和全局性查询
- 适合需要理解实体关系的场景

## 与其他方法的对比

| 维度 | RAG | 纯 LLM | Fine-tuning |
|------|-----|--------|-------------|
| 知识来源 | 外部知识库 + 模型参数 | 仅模型参数 | 更新后的模型参数 |
| 数据更新 | 即时（更新索引） | 需重训 | 需重训 |
| 部署复杂度 | 中（需要向量数据库） | 低 | 高 |
| 可解释性 | 高（可引用来源） | 低 | 低 |
| 幻觉风险 | 低 | 高 | 中 |
| 适用数据类型 | 非结构化文本 | 通用 | 特定领域 |

## 面试高频考点

| 考点 | 标准答案要点 | 常见错误 |
|------|-------------|----------|
| RAG 完整链路 | Ingestion → Retrieval → Augmentation → Generation 四步 | 漏掉 Augmentation 步骤 |
| 分块策略选择 | 固定大小+重叠是通用基线；语义分块不一定优于固定大小 | 认为语义分块一定最好 |
| 为什么需要 Reranking | 双塔模型精度有限，cross-encoder 更准但更慢，两阶段平衡速度和精度 | 以为检索一次就够了 |
| 混合搜索原理 | dense（语义）+ sparse（关键词）→ 合并 → rerank | 只知道向量搜索 |
| RAG vs 微调 | RAG 更新知识、微调改变行为，两者可组合 | 认为 RAG 完全替代微调 |
| Embedding 模型选择 | 看维度、多语言、领域适配、MTEB 基准 | 只考虑维度大小 |
| chunk_size 怎么选 | 取决于数据类型和查询模式，需要实验调优 | 认为有固定最优值 |
| Agentic RAG | Agent 编排 RAG 流程，自动决定查什么、用什么工具、结果可不可信 | 和传统 RAG 混淆 |
