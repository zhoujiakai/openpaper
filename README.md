# OpenPaper

论文、书籍与播客等学习资源收集与笔记。

## 目录结构

```
├── README.md              # 项目说明
├── MEMORY.md              # AI 上下文记忆，供 AI 助手快速加载仓库信息
├── skills/                # Claude Code 技能封装
│   ├── paper-reading/     # 吴恩达式论文精读助手
│   ├── interview-baguwen/ # 面试八股文生成器
│   └── knowledge-mastery/ # 知识精通学习工作流
├── open/                  # 待看资源
│   ├── README.md          # 待看资源列表（Web3 / AI / CV / 英语 / 软件工程）
│   ├── web3-bitcoin/               # 比特币白皮书（原文、中英对照、学习指南）
│   ├── web3-learn-blockchains-by-building-one/  # Python 区块链实践项目
│   ├── ai-bert/                    # BERT 论文
│   ├── ai-claude-skill-guide/      # Claude Code Skills 构建官方教程
│   ├── cv-yolov1/                  # YOLOv1 论文 + CV 学习路线
│   ├── cv-rcnn/                    # R-CNN 论文
│   ├── cv-openpose/                # OpenPose 论文
│   ├── cv-deepsort/                # DeepSORT 论文
│   ├── eng-liuxiaoyan-vocab-book/  # 刘晓燕《考研英语你还在背单词吗》词汇笔记
│   └── se-leetcode-top-100-liked/  # LeetCode 热题100 题解（Python 3，17 主题）
├── closed/                # 已完成
│   ├── README.md          # 已看论文列表
│   ├── ai-attention-is-all-you-need/ # Transformer 论文精读（原文、翻译、笔记）
│   ├── ai-transformer/             # Transformer 知识精通（掌握度 90%）
│   ├── ai-prompt-engineering/      # Prompt Engineering 知识精通（掌握度 85%）
│   └── ai-rag/                     # RAG 知识精通（掌握度 80%）
└── more/                  # 书籍与播客
    ├── README.more.open.md    # 待看书籍与播客
    ├── README.more.closed.md  # 已看书籍与播客
    └── mao-selected-works/    # 毛泽东选集读书笔记
```

## 使用方式

- [待看论文](open/README.md) — 计划阅读的论文
- [已看论文](closed/README.md) — 已完成阅读的论文及笔记
- [待看书籍与播客](more/README.more.open.md) — 计划看的书籍和播客
- [已看书籍与播客](more/README.more.closed.md) — 已完成阅读的书籍和播客

## Claude Code Skills

> 提示：搭配 [Typeless](https://www.typeless.com/zh-cn) 语音输入使用体验更佳，口述回答比打字更轻松自然。

- **paper-reading** — 吴恩达式论文精读助手，引导你逐节阅读论文，通过提问和纠正帮助理解核心概念，自动生成学习笔记和保存进度
- **interview-baguwen** — 面试八股文生成器，基于简历技术技能生成全面的面试问答准备指南
- **knowledge-mastery** — 技术知识精通学习工作流，三阶段闭环（输入→思考→输出），支持内容发现、AI 笔记生成、苏格拉底式问答、模拟题测试、A4 默写检验、间隔重复回测（周/月/年）

## 工具推荐

- [Typora](https://typora.io) — 所见即所得的 Markdown 编辑器，轻量流畅，适合日常阅读和编辑 Markdown 笔记
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic 官方 CLI 编程助手，擅长代码编写、文件操作和终端任务，本仓库的 Skills 和学习笔记均借助它完成
- [flomo](https://flomoapp.com) — 轻量级卡片笔记，通过标签组织而非文件夹，支持微信输入，适合随手记录灵感和碎片想法
- [GitHub](https://github.com) — 全球最大的代码托管平台，也可用于管理和版本控制 Markdown 笔记（本仓库即托管于此）
- [百度网盘](https://pan.baidu.com) — 开启同步空间功能后可自动同步本地文件夹到云端，适合多设备间同步笔记和 PDF 等学习资料
- [即刻](https://m.okjike.com) — 兴趣社区，聚集了大量技术和产品相关话题，适合发现好内容、分享学习心得
- [Typeless](https://www.typeless.com/zh-cn) — 语音输入工具，支持多语言实时转文字，适合不想打字的场景

## 推荐资源

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — 一个优质开源合集，收集了"通过从零亲手构建技术来理解其原理"的教程，涵盖数据库、编译器、操作系统、Web 服务器、区块链等方向，适合在阅读论文之余通过动手实践加深理解。
- [ljg-skills](https://github.com/lijigang/ljg-skills) — 李继刚维护的 Claude Code Skills 合集，包含概念解剖、白话引擎、写作引擎、内容铸卡、论文阅读等 15 个技能，设计思路独特，适合扩展 Claude Code 的能力边界。
