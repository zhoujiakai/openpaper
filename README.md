# OpenPaper

论文、书籍与播客等学习资源收集与笔记。

## 目录结构

```
├── README.md              # 项目说明
├── MEMORY.md              # AI 上下文记忆，供 AI 助手快速加载仓库信息
├── skills/                # Claude Code 技能封装
│   ├── paper-reading/     # 吴恩达式论文精读助手
│   └── interview-baguwen/ # 面试八股文生成器
├── open/                  # 待看资源
│   ├── README.md          # 待看资源列表（Web3 / AI / CV / 英语 / 软件工程）
│   ├── README.cv.md       # CV 学习路线
│   ├── bert/                # BERT 论文
│   ├── rcnn/               # R-CNN 论文
│   ├── yolov1/             # YOLOv1 论文
│   ├── openpose/           # OpenPose 论文
│   ├── deepsort/           # DeepSORT 论文
│   ├── bitcoin/           # 比特币白皮书（原文、中英对照、学习指南）
│   ├── learn_blockchains _by_building_one/  # Python 区块链实践项目
│   ├── liuxiaoyan-vocab-book/  # 刘晓燕《考研英语你还在背单词吗》词汇笔记
│   ├── leetcode-top-100-liked/  # LeetCode 热题100 题解（Python 3，17 主题）
│   └── claude-skill-guide/      # Claude Code Skills 构建官方教程
├── closed/                # 已完成
│   ├── README.md          # 已看论文列表
│   └── Attention_Is_All_You_Need/  # Transformer 论文精读（原文、翻译、笔记）
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

## AI 辅助工具（Claude Code Skills）

`skills/` 目录下封装了两个 Claude Code 技能，复制到 `~/.claude/skills/` 即可使用：

- **paper-reading** — 吴恩达式论文精读助手，引导你逐节阅读论文，通过提问和纠正帮助理解核心概念，自动生成学习笔记和保存进度
- **interview-baguwen** — 面试八股文生成器，基于简历技术技能生成全面的面试问答准备指南

> 提示：搭配 [Typeless](https://www.typeless.com/zh-cn) 语音输入使用体验更佳，口述回答比打字更轻松自然。

## 推荐资源

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — 一个优质开源合集，收集了"通过从零亲手构建技术来理解其原理"的教程，涵盖数据库、编译器、操作系统、Web 服务器、区块链等方向，适合在阅读论文之余通过动手实践加深理解。
