# OpenPaper 目录约定

## 顶层结构

```
openpaper/
├── README.md              # 主索引：目录树 + 领域导航 + 工具推荐
├── MEMORY.md              # AI 上下文记忆文件
├── skills/                # Claude Code Skills
├── open/                  # 待读/进行中
├── closed/                # 已完成
└── more/                  # 书籍与播客
```

## 三态目录

| 目录 | 含义 | 索引文件 |
|------|------|----------|
| `open/` | 待读或学习中 | `open/README.md` |
| `closed/` | 已完成（掌握度 ≥ 80%） | `closed/README.md` |
| `more/` | 书籍与播客 | `more/README.more.open.md`（待读）、`more/README.more.closed.md`（已读） |

## 主题目录命名

格式：`{领域前缀}-{主题名}`

领域前缀：`ai-`、`cv-`、`web3-`、`se-`、`eng-`

示例：`ai-transformer`、`cv-yolov1`、`se-message-queue`

## 主题目录内文件

### 论文/资源目录

```
open/cv-yolov1/
├── yolov1-paper.pdf           # 原文
├── yolov1-paper-zh.md         # 中文翻译
└── README.cv.md               # 相关路线图
```

### 知识精通目录（zjk-mastery 工作流产出）

```
open/se-message-queue/
├── se-message-queue-ai-notes.md       # 阶段1：AI 笔记
├── se-message-queue-notes.md          # 阶段2：个人笔记
├── se-message-quiz.md                 # 阶段2：模拟题
├── se-message-queue-progress.md       # 学习进度
└── se-message-queue-mastery-report.md # 阶段3：掌握度报告
```

## 索引文件格式

### open/README.md

按领域分组（Web3、AI、CV、英语、软件工程），每个资源包含：

```markdown
### 资源名
- 类型：论文/博客/课程/开源项目
- 作者：
- 来源：
- 链接：
- 被引用数：（可选）
- 说明：
```

### closed/README.md

分"AI 论文"和"AI 知识精通"等组。知识精通条目额外包含：

```markdown
**主题名**
- 掌握度：XX%
- 完成日期：
- 笔记：[目录链接]
- 周测：下次回测日期
```

### more/README.more.open.md

按"书籍"和"播客"分组。书籍条目：

```markdown
**书名**
- 分类：
- 作者：[国籍] 作者名
- 作者介绍：
- 译者：（如有）
- 出版年份：
- 出版社：
- ISBN：（可选）
- 来源：
- 说明：
```

## 进度文件格式

`{topic}-progress.md` 包含：

- 当前进度表（阶段1/2/3 的状态）
- 逐节进度表（Section × 状态 × 掌握程度）
- "下次从哪里继续"
- 已掌握的关键知识点
- 被纠正过的误区
- 需要复习的内容

## 归档流程

当主题掌握度 ≥ 80%，将目录从 `open/` 移到 `closed/`：
1. `mv open/{topic}/ closed/{topic}/`
2. 从 `open/README.md` 移除条目
3. 在 `closed/README.md` 添加条目（含掌握度、完成日期、笔记链接、下次回测日期）
4. 更新 `MEMORY.md` 中对应主题的状态
