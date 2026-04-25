# Agent 与工作流 — 掌握度报告

> 测试时间：2026-04-25
> 测试类型：A4 默写 + 模拟题测试

---

## 总评

掌握度：75%
等级：入门

## 知识点掌握明细

| 知识点 | 掌握度 | 状态 | 备注 |
|--------|--------|------|------|
| 增强 LLM（Augmented LLM） | 100% | 🟢 | 三样装备、基础单元 |
| Workflow vs Agent 本质区别 | 100% | 🟢 | 路径固定 vs 路径动态 |
| 五种 Workflow 模式 | 30% | 🔴 | 只记住 Orchestrator-Worker，其余四种遗忘 |
| ReAct 模式 | 100% | 🟢 | Think-Act-Observe 循环、Thought 作用 |
| Plan-and-Execute vs ReAct | 90% | 🟢 | 区别、混合使用方式 |
| Function Calling 底层机制 | 95% | 🟢 | LLM 只输出 JSON，不执行代码 |
| 工具设计原则 | 90% | 🟢 | 防呆设计、适应模型习惯 |
| Multi-Agent 三种模式 | 85% | 🟢 | Supervisor/Hierarchical/Swarm |
| Memory 系统 | 60% | 🟡 | 短期/长期记忆正确，检索三因素遗漏两个 |
| 选型决策框架 | 55% | 🟡 | 核心思路正确，漏了三个中间步骤 |

## 薄弱知识点强化建议

### 五种 Workflow 模式（🔴）

- 遗漏点：Prompt Chaining、Routing、Parallelization、Evaluator-Optimizer 四种模式名称和核心思路遗忘
- 建议记忆方法：按路径复杂度递增记忆——串行（Chaining）→ 分支（Routing）→ 并行（Parallelization）→ 动态拆分（Orchestrator-Worker）→ 循环（Evaluator-Optimizer）
- 口诀："串路并编评"——串行、路由、并行、编排、评估

### 选型决策框架（🟡）

- 遗漏点：漏了 Routing、Orchestrator-Worker、Evaluator-Optimizer 三个中间步骤
- 建议：把五种 Workflow 和选型路径一起记，它们是一一对应的
- 完整路径：单次调用 → Chaining → Routing → Parallelization → Orchestrator-Worker → Evaluator-Optimizer → Agent → Multi-Agent

### Memory 检索三因素（🟡）

- 遗漏点：遗漏了相关性和重要性
- 建议记忆方法：类比人回忆事情——"跟我现在在干嘛有没有关系（相关性）、最近发生的还是很久以前的（时效性）、这事重不重要（重要性）"

## 被纠正过的误区

1. 把 Orchestrator-Worker 误认为 Agent 模式——它仍然是 Workflow，只决定"怎么拆"，不决定后续整体流程
2. 低估了 GitHub Issue 修复场景对 Agent 的需求——定位代码和修改代码的路径不可预测，纯 Workflow 不够
3. 演进顺序混淆——ReAct 不是在 Workflow 之前出现的，它们是两种平行的编排风格

## 下一步

当前掌握度 75%，未达到 80% 归档标准。建议：
1. 重点强化五种 Workflow 模式的记忆
2. 背诵选型决策框架完整路径
3. 记住 Memory 检索三因素
4. 完成强化后重新默写薄弱知识点

## 回测计划

| 类型 | 计划日期 | 题目范围 |
|------|---------|---------|
| 周测 | 2026-05-02 | 全部核心知识点，优先五种 Workflow + 选型框架 + Memory 三因素 |
| 月测 | 2026-05-25 | 全部 + 延伸题 |
| 年测 | 2027-04-25 | 全部 + 跨主题关联题 |
