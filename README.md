# OpenPaper

论文、书籍与播客等学习资源收集与笔记。

## 目录结构

```
├── README.md              # 项目说明
├── README.open.md         # 待看论文
├── README.closed.md       # 已看论文
├── README.more.open.md    # 待看书籍与播客
├── README.more.closed.md  # 已看书籍与播客
├── skills/            # Claude Code 技能封装
│   ├── paper-reading/     # 吴恩达式论文精读助手
│   └── interview-baguwen/ # 面试八股文生成器
├── ai/                # AI 相关论文与笔记
│   ├── Attention_Is_All_You_Need/  # 含原论文、中文翻译、精读笔记
│   ├── bert.pdf
│   └── ……
├── cv/                # 计算机视觉相关论文与笔记
│   ├── README.cv.md
│   ├── rcnn.pdf
│   ├── yolov1.pdf
│   ├── openpose.pdf
│   ├── deepsort.pdf
│   └── ……
└── web3/              # Web3 相关论文与笔记
    ├── README.web3.md
    ├── bitcoin.pdf
    └── ……
```

## 使用方式

- [待看论文](README.open.md) — 计划阅读的论文
- [已看论文](README.closed.md) — 已完成阅读的论文及笔记
- [待看书籍与播客](README.more.open.md) — 计划看的书籍和播客
- [已看书籍与播客](README.more.closed.md) — 已完成阅读的书籍和播客

## AI 辅助工具（Claude Code Skills）

`skills/` 目录下封装了两个 Claude Code 技能，复制到 `~/.claude/skills/` 即可使用：

- **paper-reading** — 吴恩达式论文精读助手，引导你逐节阅读论文，通过提问和纠正帮助理解核心概念，自动生成学习笔记和保存进度
- **interview-baguwen** — 面试八股文生成器，基于简历技术技能生成全面的面试问答准备指南

> 提示：搭配 [Typeless](https://www.typeless.com/zh-cn) 语音输入使用体验更佳，口述回答比打字更轻松自然。

## 分类

- **ai/** — 人工智能（Transformer、BERT、LLM 等）
- **cv/** — 计算机视觉（YOLO、R-CNN、OpenPose、DeepSORT 等）
- **web3/** — 区块链与 Web3（Bitcoin 等）

## 推荐资源

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — 一个优质开源合集，收集了"通过从零亲手构建技术来理解其原理"的教程，涵盖数据库、编译器、操作系统、Web 服务器、区块链等方向，适合在阅读论文之余通过动手实践加深理解。
