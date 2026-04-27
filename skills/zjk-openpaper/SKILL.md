---
name: zjk-openpaper
description: >
  个人知识库浏览器与管理工具。浏览、搜索、管理 OpenPaper 仓库中的学习资源（论文、技术主题、书籍、播客），
  查看学习进度、掌握度、笔记内容，添加新资源，归档已完成主题。
  触发场景：(1) 用户想浏览/搜索知识库中的资源 (2) 查看某个主题的学习笔记或进度
  (3) 统计学习进展概览 (4) 添加新学习资源到知识库 (5) 归档已完成的主题
  (6) 管理书籍/播客列表 (7) "openpaper"、"知识库"、"学习进度"、"掌握度"、"归档" 等关键词。
  不触发场景：用户要在知识库内开始学习某个主题——此时应引导用户到仓库内使用 zjk-mastery skill。
---

# OpenPaper 知识库管理

## 定位

OpenPaper 是一个基于 Markdown 的个人学习知识库，按三态组织：`open/`（进行中）→ `closed/`（已完成）→ `more/`（书籍播客）。本 Skill 提供浏览和管理操作。

**注意**：本 Skill 不负责学习工作流。如需开始学习，请到仓库内使用 `zjk-mastery` Skill。

## 配置仓库路径

首次使用时需定位 OpenPaper 仓库。按优先级查找：

1. 用户在对话中指定的路径
2. 当前工作目录下是否存在 `open/`、`closed/`、`more/` 三态结构
3. 搜索常见路径：`~/Downloads/repos/opensource/openpaper`、`~/openpaper`、`~/repos/openpaper`

找到后记住路径，后续操作基于该路径。如果找不到，询问用户仓库位置。

详细目录结构约定见 [references/directory-conventions.md](references/directory-conventions.md)。

## 操作总览

### 浏览操作（只读）

| 操作 | 方法 |
|------|------|
| 列出全部资源 | 读取 `open/README.md` + `closed/README.md` + `more/README.more.open.md` + `more/README.more.closed.md` |
| 按领域筛选 | 从 README 中提取对应分组（AI/CV/Web3/SE/英语/书籍/播客） |
| 按状态筛选 | `open/` = 进行中，`closed/` = 已完成，`more/` = 书籍播客 |
| 查看某主题笔记 | 定位 `{状态目录}/{topic}/` 下的 `.md` 文件，读取内容 |
| 查看学习进度 | 读取 `{topic}-progress.md` |
| 搜索内容 | 在仓库目录下用 Grep 搜索关键词，限定 `.md` 文件 |
| 学习统计 | 汇总：完成数/进行中数/待读数，各领域分布，平均掌握度 |

### 管理操作（写入）

| 操作 | 方法 |
|------|------|
| 添加资源 | 在 `open/` 或 `more/` 下创建目录，更新对应 README |
| 更新进度 | 修改 `{topic}-progress.md` |
| 归档主题 | `mv open/{topic}/ closed/{topic}/`，更新两边 README + MEMORY.md |
| 添加书籍 | 更新 `more/README.more.open.md`，按格式添加条目 |
| 完成书籍 | 从 `more/README.more.open.md` 移到 `more/README.more.closed.md` |

## 操作细则

### 列出全部资源

读取三个索引文件并汇总为表格：

```
| # | 主题 | 领域 | 状态 | 类型 | 备注 |
|---|------|------|------|------|------|
```

备注列填掌握度（closed 主题）或学习阶段（open 主题）。

### 按领域筛选

读取对应 README，提取该分组下的所有条目。领域映射：

- `ai-` → AI/NLP
- `cv-` → 计算机视觉
- `web3-` → Web3/区块链
- `se-` → 软件工程
- `eng-` → 英语
- `more/` → 书籍/播客

### 查看主题笔记

1. 确定主题所在目录（`open/` 或 `closed/`）
2. 用 Glob 扫描 `{目录}/{topic}/` 下所有 `.md` 文件
3. 按用户请求读取对应文件（AI 笔记、个人笔记、模拟题、进度、掌握度报告）

### 添加新资源

1. 确定领域前缀，命名目录为 `{前缀}-{主题名}`
2. 在 `open/` 下创建目录
3. 按索引格式在 `open/README.md` 对应分组下添加条目
4. 如有原始文件（PDF 等），放入该目录

### 归档主题

1. 确认掌握度 ≥ 80%（从 mastery-report 或 progress 中读取）
2. `mv open/{topic}/ closed/{topic}/`
3. 从 `open/README.md` 移除条目
4. 在 `closed/README.md` 添加条目（含掌握度、完成日期、笔记链接）
5. 更新 `MEMORY.md` 对应主题状态

### 学习统计

读取所有索引文件和 progress 文件，汇总：

- 主题总数 / 已完成 / 进行中 / 待读
- 各领域分布
- 已完成主题的平均掌握度
- 下次回测日期（从 closed/README.md 提取周测日期）
