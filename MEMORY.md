# OpenPaper 仓库记忆文件

> 本文件供 AI 助手快速加载仓库上下文，避免重复探索。

## 仓库定位

个人学习资源与笔记知识库，追踪论文、书籍、播客等学习进度。主要语言：中文。

## 目录结构

```
openpaper/
├── .gitignore
├── README.md              # 项目主索引，含目录树和导航链接
├── memory.md              # AI 上下文记忆（本文件）
├── open/                  # 待读/进行中资源
│   └── README.md          # 待读论文清单（按领域分类）
├── closed/                # 已完成资源
│   └── README.md          # 已读论文清单
└── more/                  # 书籍与播客
    ├── README.more.open.md    # 待读书籍（12本，含哲学/文学/写作/心理学/商业）
    └── README.more.closed.md  # 已读书籍与播客
```

## Claude Code 技能

所有 Skill 在独立仓库 [openskill](https://github.com/zhoujiakai/openskill) 中维护。

- [zjk-mastery](https://github.com/zhoujiakai/openskill/tree/main/zjk-mastery) — 技术知识精通学习工作流
- [zjk-openpaper](https://github.com/zhoujiakai/openskill/tree/main/zjk-openpaper) — 个人知识库浏览器与管理工具

## 组织约定

- `processing/` = 进行中，`open/` = 待读，`closed/` = 已完成，`more/` = 书籍播客
- 每个子目录通常包含一个同名 `.md` 笔记文件
- Git 分支策略：单分支 `main`，直接提交

每个主题的文件结构：`open/ai-<topic>/` 下包含 `-ai-notes.md`、`-progress.md`、`-quiz.md`、`-mastery-report.md`、`-personal-notes.md`

## 最近提交

- `58c4cb6` 添加知识精通学习工作流 skill（zjk-mastery）
- `7756f3b` 添加 MIT 6.034 人工智能课程到待读清单
- `470d054` 添加《论持久战》读书笔记，更新 README 目录结构
- `5c89c8b` 添加刘晓燕考研英语词汇笔记和剑指 Offer 题集
- `d6c7b4f` 添加 LeetCode 热题100题解和区块链学习项目
