# OpenPaper 仓库记忆文件

> 本文件供 AI 助手快速加载仓库上下文，避免重复探索。

## 仓库定位

个人学习资源与笔记知识库，追踪论文、书籍、播客等学习进度。主要语言：中文。

## 目录结构

```
openpaper/
├── README.md               # 项目说明
├── memory.md               # AI 上下文记忆（本文件）
├── open/                   # 待看
│   └── README.md
├── processing/             # 进行中
│   └── README.md
├── closed/                 # 已完成
│   └── README.md
└── more/                   # 书籍与播客
    ├── README.md           # 正在读
    ├── README.open.md      # 待读
    ├── README.closed.md    # 已读
    └── README.recommend.md # 推荐
```

## Claude Code 技能

所有 Skill 在独立仓库 [openskill](https://github.com/zhoujiakai/openskill) 中维护。

- [zjk-mastery](https://github.com/zhoujiakai/openskill/tree/main/zjk-mastery) — 技术知识精通学习工作流
- [zjk-openpaper](https://github.com/zhoujiakai/openskill/tree/main/zjk-openpaper) — 个人知识库浏览器与管理工具

## 组织约定

- `processing/` = 进行中，`open/` = 待看，`closed/` = 已完成，`more/` = 书籍、播客、公众号
- 使用三级标题（`###`）标识资源条目，代替加粗（`**`）
- 书/播客/公众号用带前缀的子目录存放笔记：`书-`、`播客-`、`公众号-`
- 论文和知识精通主题按 `ai-<topic>/`、`se-<topic>/` 命名
- Git 分支策略：单分支 `main`，直接提交

## 最近提交

- `cdf85c9` 重构 more/ 目录，精简 README 目录树，统一三级标题
- `d1dc5cb` 重命名 mao-selected-works 为 毛泽东选集
- `fa7f4b0` 重构毛选笔记目录结构，添加吴恩达机器学习学习计划
- `0eeb20b` 精简知识库结构与索引，新增 LSTM 与 processing 目录
- `5c55aea` 更新 ML 基础算法笔记，新增控制理论目录和学习进度跟踪文件
