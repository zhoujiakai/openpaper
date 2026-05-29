# Agent 与工作流 — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-29（上次 2026-04-25）

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现与整理 | ✅ 已完成 | 3 个来源，AI 笔记已生成 |
| 2. 深度理解与互动 | ✅ 已完成 | 5/5 Section 全部完成 |
| 3. 知识检验 | ✅ 已完成 | 掌握度 75% → 82%（周测），已达归档标准 |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: 为什么不能只用裸 LLM | ✅ | 完全掌握 |
| Section 2: 从 Workflow 到 Agent 的渐进路径 | ✅ | 完全掌握 |
| Section 3: ReAct 的设计哲学 | ✅ | 完全掌握 |
| Section 4: 工具设计为什么比 Prompt 更重要 | ✅ | 完全掌握 |
| Section 5: Multi-Agent 的实际取舍 | ✅ | 完全掌握 |

## 已掌握的关键知识点

### Section 1: 增强 LLM
- 裸 LLM 只能输出文本，装上工具/记忆/检索后变成增强 LLM
- 增强 LLM 是所有 Agent 系统的基本单元

### Section 2: 五种 Workflow 模式
- Prompt Chaining（串行）、Routing（分类分发）、Parallelization（并行/投票）、Orchestrator-Worker（动态拆分）、Evaluator-Optimizer（循环改进）

### Section 3: ReAct 与 Plan-and-Execute
- ReAct：Think-Act-Observe 循环，边想边做
- Plan-and-Execute：先规划再执行，有全局视野
- 两者可混合使用

### Section 4: 工具设计与 Function Calling
- 工具设计比 Prompt 更重要：描述清晰、防呆设计、格式友好
- Function Calling：LLM 只输出 JSON 调用意图，应用层执行

### Section 5: Multi-Agent 与 Memory
- 三种模式：Supervisor（最常用）、Hierarchical、Swarm/Handoff
- Memory：短期=上下文窗口，长期=向量数据库

## 被纠正过的误区

1. 把 Orchestrator-Workflow 误认为 Agent——它只决定"怎么拆"，仍是 Workflow
2. 低估 GitHub Issue 修复对 Agent 的需求——定位和修改代码路径不可预测
3. 演进顺序混淆——ReAct 和 Workflow 是平行的两种编排风格，不是先后关系

## 需要复习的内容

- **五种 Workflow 模式**：名称和核心思路（按路径复杂度递增记忆）
- **选型决策框架**：完整 8 步路径
- **Memory 检索三因素**：相关性、时效性、重要性

## 文件清单

| 文件 | 状态 |
|------|------|
| `agent-ai-notes.md` | ✅ 已生成 |
| `agent-progress.md` | ✅ 本文件 |
| `agent-quiz.md` | ✅ 已生成（8 道题 + A4 默写记录） |
| `agent-mastery-report.md` | ✅ 已更新（掌握度 75% → 82%） |
| `agent-personal-notes.md` | ✅ 已创建（周测复习记录） |

## 回测计划

| 类型 | 计划日期 | 状态 |
|------|---------|------|
| 周测 | 2026-04-29 | ✅ 已完成（掌握度 82%） |
| 月测 | 2026-05-25 | ⏳ 待执行 |
