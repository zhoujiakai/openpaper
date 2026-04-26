# OpenPaper 仓库记忆文件

> 本文件供 AI 助手快速加载仓库上下文，避免重复探索。

## 仓库定位

个人学习资源与笔记知识库，追踪论文、书籍、播客等学习进度。主要语言：中文。

## 目录结构

```
openpaper/
├── .gitignore
├── README.md              # 项目主索引，含目录树和导航链接
├── MEMORY.md              # AI 上下文记忆（本文件）
├── skills/                # Claude Code 技能定义
│   ├── paper-reading/     # 吴恩达式论文精读助手（SKILL.md）
│   └── zjk-mastery/ # 技术知识精通学习工作流（SKILL.md + output-templates.md）
├── open/                  # 待读/进行中资源
│   ├── README.md          # 待读论文清单（按领域分类）
│   ├── web3-bitcoin/               # 比特币白皮书（英文/中文/双语/学习指南）
│   ├── web3-learn-blockchains-by-building-one/  # Python 区块链实战项目
│   ├── ai-bert/                    # BERT 论文 PDF
│   ├── ai-claude-skill-guide/      # Claude Skills 构建教程（PDF）
│   ├── cv-yolov1/                  # YOLOv1 论文 + CV 学习路线图
│   ├── cv-rcnn/                    # R-CNN 论文 PDF
│   ├── cv-openpose/                # OpenPose 论文 PDF
│   ├── cv-deepsort/                # DeepSORT 论文 PDF
│   ├── eng-liuxiaoyan-vocab-book/  # 刘晓燕考研英语词汇笔记
│   └── se-leetcode-top-100-liked/  # LeetCode 热题100题解（Python3，17个专题）
├── closed/                # 已完成资源
│   ├── README.md          # 已读论文清单
│   ├── ai-attention-is-all-you-need/  # Transformer 论文精读（原文/翻译/笔记/对话记录/图表）
│   ├── ai-transformer/             # Transformer 知识精通（AI笔记/题库/进度/掌握度报告）掌握度 90%
│   ├── ai-prompt-engineering/      # Prompt Engineering 知识精通（掌握度 85%）
│   ├── ai-rag/                     # RAG 知识精通（掌握度 80%）
│   ├── ai-agent/                   # Agent 与工作流 知识精通（掌握度 75%）
│   └── ai-python-async/            # Python 异步 知识精通（掌握度 85%）
└── more/                  # 书籍与播客
    ├── README.more.open.md    # 待读书籍（12本，含哲学/文学/写作/心理学/商业）
    ├── README.more.closed.md  # 已读书籍与播客
    └── mao-selected-works/    # 《毛泽东选集》读书笔记（含《论持久战》）
```

## 内容领域

| 领域 | 内容 | 状态 |
|------|------|------|
| AI/NLP | Transformer（精读完成）、BERT（待读）、Claude Skills 教程（待读） | closed/open |
| 计算机视觉 | YOLOv1, R-CNN, OpenPose, DeepSORT | open |
| Web3/区块链 | 比特币白皮书（中英双语+学习指南）、区块链 Python 实战 | open |
| 算法 | LeetCode 热题100（Python3 题解）、剑指 Offer 50 题 | open |
| 英语 | 刘晓燕考研词汇笔记 | open |
| 书籍 | 12本待读 + 《论持久战》已完成 | more |
| 播客 | "没人知道"、跨界拜访计划、岩石里的花 | more |

## 关键文件速查

| 文件 | 用途 |
|------|------|
| `README.md` | 项目主索引 |
| `open/README.md` | 待读论文清单（按 AI/CV/NLP 等分类） |
| `open/cv-yolov1/README.cv.md` | CV 学习路线图（YOLOv5/v8/v11/v26、PaddleOCR） |
| `closed/README.md` | 已完成论文清单 |
| `more/README.more.open.md` | 待读书籍（12本，含完整元数据） |
| `more/README.more.closed.md` | 已读书籍/播客 |
| `skills/paper-reading/SKILL.md` | 论文精读技能定义（约293行） |
| `skills/zjk-mastery/SKILL.md` | 知识精通学习工作流（约171行） |
| `skills/zjk-mastery/references/output-templates.md` | 学习产出模板（AI笔记/个人笔记/题库/进度/报告） |
| `open/se-leetcode-top-100-liked/leetcode-top-100-liked.md` | LeetCode 题解 |
| `open/eng-liuxiaoyan-vocab-book/liuxiaoyan-vocab-book.md` | 英语词汇笔记 |
| `open/ai-claude-skill-guide/The-Complete-Guide-to-Building-Skill-for-Claude.pdf` | Claude Skills 构建教程 |
| `more/mao-selected-works/mao-selected-works.md` | 毛选读书笔记 |

## Claude Code 技能

1. **paper-reading**：吴恩达式论文精读助手，支持逐节引导、提问纠正、自动搜索补充资料、保存/恢复学习进度
2. **zjk-mastery**：技术知识精通学习工作流，三阶段闭环（输入→思考→输出），支持内容发现、AI笔记、苏格拉底问答、模拟题测试、A4默写、间隔重复回测（周/月/年）

安装方式：将 `skills/` 下的目录复制到 `~/.claude/skills/`

## 组织约定

- `open/` = 待读/进行中，`closed/` = 已完成，`more/` = 书籍播客
- 每个子目录通常包含一个同名 `.md` 笔记文件
- 论文目录通常包含：原文 PDF、中文翻译、学习笔记
- Git 分支策略：单分支 `main`，直接提交

## 知识精通学习计划（2026-04-24 开始）

7 个主题，面试准备导向，使用 zjk-mastery skill 三阶段闭环。

| # | 主题 | 状态 | 进度 |
|---|------|------|------|
| 1 | Transformer | ✅ 完成 | 掌握度 90%，周测 05-01 |
| 2 | Prompt Engineering | ✅ 完成 | 掌握度 85%，周测 05-01，个人笔记待写 |
| 3 | RAG | ✅ 完成 | 掌握度 80%，周测 05-01 |
| 4 | Agent 与工作流 | ✅ 完成 | 掌握度 75%，周测 05-02，个人笔记待写 |
| 5 | Python 异步 | ✅ 完成 | 掌握度 85%，周测 05-03 |
| 6 | 消息队列 | 🔜 进行中 | 阶段 1 完成，AI 笔记已生成 |
| 7 | 微服务架构 | ⏳ 未开始 | — |

每个主题的文件结构：`open/ai-<topic>/` 下包含 `-ai-notes.md`、`-progress.md`、`-quiz.md`、`-mastery-report.md`

### 主题 1: Transformer

**定位：** 会用 LangChain 调 API，还需要理解 LLM 背后在做什么。面试中对 Transformer 熟悉度不够，需要理解并掌握。

**学习资源：**
- Attention Is All You Need（论文原文）
- 3Blue1Brown 的 Transformer 可视化视频

**目标问题：**
- Transformer 的核心结构是什么？
- Encoder 和 Decoder 各自的作用？
- GPT 系列为什么只用 Decoder？
- Multi-Head Attention 的意义是什么？

### 主题 2: Prompt Engineering

**定位：** 不是背提示词技巧，而是理解它们为什么有效。

**学习资源：**
- OpenAI 官方 Prompt Engineering
- Anthropic 官方 Prompt Engineering
- Prompt Engineering Guide

**目标问题：**
- Few-shot 为什么有效？
- 什么是 In-Context Learning？
- Chain-of-Thought 为什么能提升推理能力？
- 结构化输出（JSON）的底层是怎么实现的？
- System Prompt 和 User Prompt 的区别是什么？

### 主题 3: RAG

**定位：** 做过 RAG，需要把每个环节背后的工程决策理解透。

**学习资源：**
- LangChain RAG 官方教程
- Pinecone 的 RAG 学习指南

**目标问题：**
- RAG 的完整链路是什么？从文档入库到查询生成，经过哪些步骤？
- 分块策略有哪几种（按字符、按句子、按语义）？各有什么优劣？
- 纯向量检索 vs 混合检索各适合什么场景？
- 什么是 Reranking？为什么检索后还需要重排？

### 主题 4: Agent 与工作流

**定位：** 用过 ReAct；Agent 有多种模式，不同场景需要不同架构，需要进一步掌握。

**学习资源：**
- LangGraph 官方文档的 Agent Architectures
- LangChain 博客中关于 Multi-Agent 的文章

**目标问题：**
- ReAct 模式是什么？适合什么场景？
- Plan-and-Execute 和 ReAct 的区别？
- Multi-Agent 协作有哪些常见模式？各自优劣？
- Function Calling 的底层机制是什么？

### 主题 5: Python 异步

**定位：** 需要理解事件循环在底层做了什么，否则遇到并发 bug 无从排查。

**学习资源：**
- Python 官方文档 asyncio
- Real Python 的 asyncio 系列文章

**目标问题：**
- 事件循环（Event Loop）是什么？
- 单线程怎么实现并发的？
- await 的时候发生了什么？
- asyncio.gather vs asyncio.TaskGroup 的区别？
- 为什么数据库操作要用 AsyncSession？同步 Session 在异步代码里会怎样？
- asyncio、多线程、多进程分别适合什么场景？

### 主题 6: 消息队列

**定位：** 用过 RocketMQ，RabbitMQ 和 Kafka 是业界另外两个主流选型。理解架构差异，才能正确技术选型。

**学习资源：**
- RabbitMQ 官方教程
- aio-pika 文档
- Kafka 官方文档

**目标问题：**
- RabbitMQ 的 Exchange 类型各适合什么场景？
- prefetch_count 是什么？设大设小各有什么影响？
- Kafka 的 Topic、Partition、Consumer Group 各是什么？Partition 怎么实现并行消费？
- Kafka 为什么吞吐量比 RabbitMQ 高？
- RabbitMQ 适合什么场景？Kafka 适合什么场景？
- 幂等消费有哪些实现方式？各有什么优劣？

### 主题 7: 微服务架构

**定位：** 了解过 Spring 的微服务，较深的应用实践上还有空间。自行学习探索，理解概念为主。

**学习资源：** 无专门资源，自行探索。Java 生态微服务概念完善，概念相通。

**目标问题：**
- 微服务和单体架构各有什么优劣？什么时候不该用微服务？
- 服务拆分的依据是什么？怎么判断两个功能该放一个服务还是拆开？
- 服务间通信用同步（HTTP/RPC）还是异步（消息队列），怎么选？
- 什么是 API 网关？
- 什么是服务熔断？
- 什么是幂等性？为什么在微服务中特别重要？
- 什么是分布式链路追踪？Trace ID 怎么在服务间传递？
- 配置管理在微服务中怎么做？环境变量 vs 配置中心各适合什么场景？

## 最近提交

- `58c4cb6` 添加知识精通学习工作流 skill（zjk-mastery）
- `7756f3b` 添加 MIT 6.034 人工智能课程到待读清单
- `470d054` 添加《论持久战》读书笔记，更新 README 目录结构
- `5c89c8b` 添加刘晓燕考研英语词汇笔记和剑指 Offer 题集
- `d6c7b4f` 添加 LeetCode 热题100题解和区块链学习项目
