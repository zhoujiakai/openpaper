# OpenPaper

论文、书籍与播客等学习资源收集与笔记。

## 目录结构

```
├── README.md               # 项目说明
├── memory.md               # AI 上下文记忆
├── open/                   # 待看的技术资源
│   └── README.md
├── processing/             # 进行中的技术资源
│   └── README.md
├── closed/                 # 已完成的技术资源
│   └── README.md
└── more/                   # 非技术的书籍与播客
    ├── README.md           # 正在读
    ├── README.open.md      # 待读
    ├── README.closed.md    # 已读
    └── README.recommend.md # 推荐
```

## Claude Code Skills

所有 Skill 在独立仓库 [openskill](https://github.com/zhoujiakai/openskill) 中维护。

- [zjk-mastery](https://github.com/zhoujiakai/openskill/tree/main/zjk-mastery) — 技术知识精通学习工作流，三阶段闭环（输入→思考→输出），支持内容发现、AI 笔记生成、苏格拉底式问答、模拟题测试、A4 默写检验、间隔重复回测（周/月/年）
- [zjk-openpaper](https://github.com/zhoujiakai/openskill/tree/main/zjk-openpaper) — 个人知识库浏览器与管理工具，浏览、搜索、管理本仓库中的学习资源

> 提示：搭配 [Typeless](https://www.typeless.com/zh-cn) 语音输入使用体验更佳。

## 工具推荐

- [Typora](https://typora.io) — 所见即所得的 Markdown 编辑器，轻量流畅，适合日常阅读和编辑 Markdown 笔记
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic 官方 CLI 编程助手，擅长代码编写、文件操作和终端任务，本仓库的 Skills 和学习笔记均借助它完成；Max 套餐 $200/月
- [GLM Coding Plan](https://open.bigmodel.cn/dev/howuse/codingplan) — 智谱AI 提供的编程套餐（lite / pro / max 三档），调用 GLM-5.1 大模型 API，供 Claude Code 等 CLI 工具使用；max 套餐 1266.3 元/季度（约 422 元/月）
- [Gemini](https://gemini.google.com) — Google 的 AI 助手，内置 Imagen 3 图像生成能力，适合 AI 画图；AI Premium 套餐 $19.99/月
- [flomo](https://flomoapp.com) — 轻量级卡片笔记，通过标签组织而非文件夹，支持微信输入，适合随手记录灵感和碎片想法
- [GitHub](https://github.com) — 全球最大的代码托管平台，也可用于管理和版本控制 Markdown 笔记（本仓库即托管于此）
- [百度网盘](https://pan.baidu.com) — 开启同步空间功能后可自动同步本地文件夹到云端，适合多设备间同步笔记和 PDF 等学习资料
- [即刻](https://m.okjike.com) — 兴趣社区，聚集了大量技术和产品相关话题，适合发现好内容、分享学习心得
- [Typeless](https://www.typeless.com/zh-cn) — 语音输入工具，支持多语言实时转文字，适合不想打字的场景

## 推荐资源

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — 一个优质开源合集，收集了"通过从零亲手构建技术来理解其原理"的教程，涵盖数据库、编译器、操作系统、Web 服务器、区块链等方向，适合在阅读论文之余通过动手实践加深理解。
- [ljg-skills](https://github.com/lijigang/ljg-skills) — 李继刚维护的 Claude Code Skills 合集，包含概念解剖、白话引擎、写作引擎、内容铸卡、论文阅读等 15 个技能，设计思路独特，适合扩展 Claude Code 的能力边界。
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic 官方 Agent Skills 仓库，提供经过验证的 Claude Code 技能，可通过 `/plugin marketplace add anthropics/skills` 安装。
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — 社区最热门的 Claude Code 资源精选合集（38.8k stars），涵盖 Skills、Hooks、Slash Commands 等，适合发现和探索社区产出的优质技能。
- [3Blue1Brown - Attention in Transformers](https://www.3blue1brown.com/lessons/attention) — 通过精美动画逐步可视化讲解 Transformer 中 Attention 机制的运作原理（Query、Key、Value、Attention Pattern、Multi-Head Attention），直观易懂，适合配合 Attention Is All You Need 论文一起学习。
- [计算机视觉研究院](https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI0NTE0ODA5MA==) — 微信公众号，专注计算机视觉领域，持续分享 CV 前沿论文解读、技术实践和行业动态，适合跟踪 CV 方向的最新进展。
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) — Claude Code Harness 工程逆向教学。12 个递进章节，从最小 agent loop 开始逐步拆解 Claude Code 架构机制：工具调度、计划分解、子代理隔离、按需知识加载、上下文压缩、任务持久化、后台执行、多代理协作、自治取任务和工作树隔离。
- [claw0](https://github.com/shareAI-lab/claw0) — 从零到一构建 AI Agent Gateway。10 个递进章节，每章一个可独立运行的 Python 文件，从 agent loop 开始逐步构建到生产级网关，涵盖工具调用、会话管理、多 IM 渠道、网关路由、智能体个性与记忆、心跳与定时任务、可靠投递、弹性容错和并发控制。

