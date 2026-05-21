# OpenPaper

> 比起选择从哪获得成就感，人更多需要做的选择是为哪件事痛苦。（by 刘旸）

学习资源收集与笔记。

## 目录结构

```
├── README.md               # 项目说明
├── CLAUDE.md               # AI 上下文记忆
├── open/                   # 待看的技术资源
│   └── README.md
├── processing/             # 进行中的技术资源
│   └── README.md
├── closed/                 # 已完成的技术资源
│   └── README.md
└── more/                   # 非技术资源
    ├── README.md           # 正在读
    ├── README.open.md      # 待读
    ├── README.closed.md    # 已读
    └── README.recommend.md # 推荐
```

## 工具

- [Typora](https://typora.io) — 所见即所得的 Markdown 编辑器，轻量流畅，适合日常阅读和编辑 Markdown 笔记
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic 官方 CLI 编程助手，擅长代码编写、文件操作和终端任务，本仓库的 Skills 和学习笔记均借助它完成；Max 套餐 $200/月
- [GLM Coding Plan](https://open.bigmodel.cn/dev/howuse/codingplan) — 智谱AI 提供的编程套餐（lite / pro / max），调用 GLM-5.1 大模型 API，供 Claude Code 等 CLI 工具使用；max 套餐 1266.3 元/季度（422 元/月）
- [Gemini](https://gemini.google.com) — Google 的 AI 助手，内置 Imagen 3 图像生成能力，适合 AI 画图；AI Premium 套餐 $19.99/月
- [flomo](https://flomoapp.com) — 轻量级卡片笔记，通过标签组织而非文件夹，支持微信输入，适合随手记录灵感和碎片想法
- [GitHub](https://github.com) — 全球最大的代码托管平台，也可用于管理和版本控制 Markdown 笔记（本仓库即托管于此）
- [百度网盘](https://pan.baidu.com) — 开启同步空间功能后可自动同步本地文件夹到云端，适合多设备间同步笔记和 PDF 等学习资料
- [即刻](https://m.okjike.com) — 兴趣社区，聚集了大量技术和产品相关话题，适合发现好内容、分享学习心得
- [Typeless](https://www.typeless.com/zh-cn) — 语音输入工具，支持多语言实时转文字，适合不想打字的场景

## 设备控制

设备控制这个方向的学习安排。

- 吴恩达的机器学习网课 → [processing/ml-吴恩达机器学习](processing/ml-吴恩达机器学习/)，掌握LSTM → [open/ml-lstm](open/ml-lstm/) 等模型的应用方法，能够开发一个机器学习系统，实现对设备的智能优化控制。
- 江协科技的PID基础教程 → [open/ctrl-江协PID倒立摆](open/ctrl-江协PID倒立摆/)，掌握PID算法应用，具体实践控制编码电机的实验。

## 开发技术

掌握基本的开发技术。

- Python异步 → [closed/ai-python-async](closed/ai-python-async/)
- FastAPI → [closed/se-fastapi](closed/se-fastapi/)、SQLAlchemy → [closed/se-sqlalchemy](closed/se-sqlalchemy/)、Pydantic → [closed/se-fastapi](closed/se-fastapi/)
- Celery 异步任务队列 → [open/se-celery](open/se-celery/)
- Redis缓存中间件 → [open/se-redis](open/se-redis/)，Python多级缓存架构、分布式锁、缓存雪崩/穿透解决方案、哨兵集群搭建
- Docker容器化、Nginx反向代理部署
- MySQL、PostgreSQL 数据库设计和SQL 调优，实践过分库分表、索引优化，使用 SQLAlchemy 进行ORM映射和慢查询分析
- 理解微服务架构中的概念 → [closed/se-microservice](closed/se-microservice/)
- 设计模式：装饰器、生成器等
- 消息队列 RabbitMQ & Kafka → [open/se-message-queue](open/se-message-queue/)

掌握一些AI应用的技术。

- Transformer的原理 → [closed/ai-transformer](closed/ai-transformer/)
- Prompt Engineering → [closed/ai-prompt-engineering](closed/ai-prompt-engineering/)
- RAG → [closed/ai-rag](closed/ai-rag/)
- Agent与工作流 → [closed/ai-agent](closed/ai-agent/)
- Claude Code源码 → [open/se-ClaudeCode源码](open/se-ClaudeCode源码/)
- OpenClaw源码 → [open/se-OpenClaw源码](open/se-OpenClaw源码/)
- LangChain、LangGraph、LangSmith
- Python爬虫 → [open/se-web-scraping-anti-detection](open/se-web-scraping-anti-detection/)

## 算法

- LeetCode热题100 → [open/al-LeetCode热题100](open/al-LeetCode热题100/)
- 剑指offer50道题
- 深度优先&广度优先算法等
- 周志华机器学习西瓜书 → [open/ml-周志华机器学习](open/ml-周志华机器学习/)
- 吴恩达机器学习网课 → [processing/ml-吴恩达机器学习](processing/ml-吴恩达机器学习/)

# 后记

回顾一下笔者的后端学习历程。

本科专业是软件工程，本科期间，学了基本的Java语法之后，学习java的servlet，接着学了spring做后端项目，学了Vue写前端项目，还学了android项目的开发。在一门课程设计中，和同学一起做了springboot + uniapp项目。这就是本科期间做的前后端的所有内容了。工作之后的第二份工作，是为企业搭建智能问答系统，用FastAPI和LangcChain，当时最新的大语言模型好像是gpt4o，模型能力的迭代速度很快。

再回顾一下笔者的算法学习历程。

本科期间，最开始是学习C语言，兼顾着学了一点点的C++，接着学习了数据结构和算法这门课程。三年级上学期学了python数据处理，学习pandas和爬虫程序。四年级快毕业的时候，在学校附近一家小公司做视觉应用的开发，在这个公司实习，主要负责摄像头接入和调焦，集成一些目标检测、姿态估计、多目标跟踪等模型进行逻辑分析。还有传感器数据接入和处理的业务。

创建这个仓库的起因，是基于一直以来的困惑：具体学会了哪些知识，学习效率如何，评估方法。

有一个明显的感觉，就是学习效率不高，学习过程看不见摸不着，今天学一点，过几天再学一点，问题在于没有进度条和日志，无法评估掌握程度和学习效率。

网上优质的学习教程很多，本仓库中有多处引用并标识。笔者把学习过程和笔记开源，是因为公开学习过程会更加有学习动力。若读者能够从中受益，也是一件喜悦的事情。

本仓库会一直开源，持续构建更新。
