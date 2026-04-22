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
│   └── interview-baguwen/ # 基于简历的面试八股文生成器（SKILL.md）
├── open/                  # 待读/进行中资源
│   ├── README.md          # 待读论文清单（按领域分类，约152行）
│   ├── README.cv.md       # 计算机视觉学习路线图（YOLO 系列、PaddleOCR）
│   ├── bitcoin/           # 比特币白皮书（英文/中文/双语/学习指南）
│   ├── learn_blockchains_by_building_one/  # Python 区块链实战项目
│   ├── leetcode-top-100-liked/  # LeetCode 热题100题解（Python3，17个专题）
│   ├── liuxiaoyan-vocab-book/   # 刘晓燕考研英语词汇笔记
│   ├── sword-to-offer/          # 剑指Offer 50题
│   ├── claude-skill-guide/      # Claude Code Skills 构建官方教程（PDF）
│   └── *.pdf              # 待读论文 PDF（BERT, R-CNN, YOLOv1, OpenPose, DeepSORT）
├── closed/                # 已完成资源
│   ├── README.md          # 已读论文清单
│   └── Attention_Is_All_You_Need/  # Transformer 论文精读（原文/翻译/笔记/对话记录/图表）
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
| `open/README.cv.md` | CV 学习路线图（YOLOv5/v8/v11/v26、PaddleOCR） |
| `closed/README.md` | 已完成论文清单 |
| `more/README.more.open.md` | 待读书籍（12本，含完整元数据） |
| `more/README.more.closed.md` | 已读书籍/播客 |
| `skills/paper-reading/SKILL.md` | 论文精读技能定义（约293行） |
| `skills/interview-baguwen/SKILL.md` | 面试八股文技能定义（约79行） |
| `open/leetcode-top-100-liked/leetcode-top-100-liked.md` | LeetCode 题解 |
| `open/liuxiaoyan-vocab-book/liuxiaoyan-vocab-book.md` | 英语词汇笔记 |
| `open/sword-to-offer/sword-to-offer.md` | 剑指 Offer 题解 |
| `open/claude-skill-guide/The-Complete-Guide-to-Building-Skill-for-Claude.pdf` | Claude Skills 构建教程 |
| `more/mao-selected-works/mao-selected-works.md` | 毛选读书笔记 |

## Claude Code 技能

1. **paper-reading**：吴恩达式论文精读助手，支持逐节引导、提问纠正、自动搜索补充资料、保存/恢复学习进度
2. **interview-baguwen**：读取简历（.docx/.pdf），提取技术技能，生成初/中/高级面试问答

安装方式：将 `skills/` 下的目录复制到 `~/.claude/skills/`

## 组织约定

- `open/` = 待读/进行中，`closed/` = 已完成，`more/` = 书籍播客
- 每个子目录通常包含一个同名 `.md` 笔记文件
- 论文目录通常包含：原文 PDF、中文翻译、学习笔记
- Git 分支策略：单分支 `main`，直接提交

## 最近提交

- `7756f3b` 添加 MIT 6.034 人工智能课程到待读清单
- `470d054` 添加《论持久战》读书笔记，更新 README 目录结构

- `470d054` 添加《论持久战》读书笔记，更新 README 目录结构
- `5c89c8b` 添加刘晓燕考研英语词汇笔记和剑指 Offer 题集
- `4c29b58` 更新根目录 README 目录结构
- `d6c7b4f` 添加 LeetCode 热题100题解和区块链学习项目
- `4161d92` 重命名 bitcoin 笔记目录
