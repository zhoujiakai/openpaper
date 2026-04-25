# Agent 与工作流 — 题库

> 生成时间：2026-04-25
> 题目数量：8
> 关联笔记：agent-ai-notes.md

---

## 题目

### Q1 [选择题] Workflow 和 Agent 的本质区别

以下哪个描述最准确地反映了 Workflow 和 Agent 的本质区别？

A. Workflow 用多个 LLM，Agent 只用一个 LLM
B. Workflow 的路径由代码决定，Agent 的路径由 LLM 决定
C. Workflow 不调用工具，Agent 会调用工具
D. Workflow 是串行的，Agent 是并行的

- **正确答案**：B
- **评分要点**：选择了正确选项即通过
- **知识点**：Workflow vs Agent

### Q2 [选择题] Function Calling 中 LLM 的角色

Function Calling 过程中，LLM 实际执行了什么？

A. 调用了外部函数并返回结果
B. 生成了可执行的代码，由运行时编译执行
C. 输出了一个结构化的调用意图（JSON），由应用层负责执行
D. 通过微调获得了直接执行函数的能力

- **正确答案**：C
- **评分要点**：选择了正确选项即通过
- **知识点**：Function Calling 底层机制

### Q3 [简答题] Prompt Chaining vs Parallelization

Prompt Chaining 和 Parallelization 都是处理多步骤任务的 Workflow，它们的适用条件有什么不同？各举一个实际场景例子。

- **参考答案**：
  1. Prompt Chaining 适合串行步骤有依赖关系的任务，如竞品报告（搜索→整理→分析→写作）
  2. Parallelization 适合子任务独立可并行的任务，如代码审查（安全性+性能+可读性同时检查）
  3. 判断标准：子任务之间有没有依赖关系
- **评分要点**：
  1. 必须提到依赖关系是核心判断标准
  2. 需要给出合理的场景例子
  3. 加分项：提到 Parallelization 的 Voting 用法
- **知识点**：Workflow 模式选型

### Q4 [简答题] ReAct 中 Thought 步骤的作用

ReAct 模式中，Thought 步骤的作用是什么？如果去掉 Thought 只保留 Action，会怎样？

- **参考答案**：
  1. Thought 的作用是在行动之前先推理"为什么要这么做"
  2. 去掉 Thought（Act-only）后准确率明显下降
  3. 没有 Thought，LLM 变成"看到什么就反应什么"，像盲人摸象
- **评分要点**：
  1. 必须提到"推理在前，行动在后"的核心思路
  2. 必须说明去掉 Thought 后准确率下降
  3. 加分项：提到实验证据
- **知识点**：ReAct 设计哲学

### Q5 [简答题] Orchestrator-Worker vs Parallelization

Orchestrator-Worker 模式和 Parallelization 模式都会把任务拆成子任务并行处理，它们的本质区别是什么？

- **参考答案**：
  1. Parallelization 的子任务是代码提前定义好的，固定不变
  2. Orchestrator-Worker 的子任务是编排者 LLM 根据具体输入动态决定的
  3. Orchestrator-Worker 仍然是 Workflow（不是 Agent），它只决定"怎么拆"，不决定后续整体流程
- **评分要点**：
  1. 必须提到"固定 vs 动态"的核心区别
  2. 必须指出 Orchestrator-Worker 是 Workflow 不是 Agent
  3. 加分项：举出具体例子对比
- **知识点**：Workflow 模式辨析

### Q6 [对比题] ReAct vs Plan-and-Execute

两者各自适合什么场景？能否混合使用？

- **参考答案**：
  | 维度 | ReAct | Plan-and-Execute |
  |------|-------|-------------------|
  | 决策方式 | 走一步看一步 | 先想好全部步骤再动手 |
  | 全局视野 | 弱 | 强 |
  | 灵活性 | 高，随时调整 | 中，出错才重新规划 |
  | 适合 | 步骤少、需环境交互 | 步骤多、需全局规划 |
- **评分要点**：至少指出 3 个区别维度，提到混合使用方式
- **知识点**：Agent 模式选型

### Q7 [应用题] GitHub Issue 修复 Agent 架构设计

设计一个自动化 GitHub Issue 修复 Agent：读取 Issue、理解问题、定位代码、修改代码、运行测试、提交 PR。选什么模式？工具怎么设计？

- **参考答案**：
  1. 用 Plan-and-Execute Agent：规划者读取 Issue 制定修复计划，执行者逐步修改
  2. 定位代码和修改代码是路径不可预测的环节，需要 Agent 动态决策
  3. 工具设计：文件操作用绝对路径、代码修改用重写整个文件、测试工具只返回失败信息
- **评分要点**：
  1. 正确选择 Plan-and-Execute
  2. 说明为什么不能用纯 Workflow（路径不可预测）
  3. 提到工具设计原则
- **知识点**：综合应用

### Q8 [应用题] 模拟面试回答

面试官问："你在实际项目中是怎么决定用 Agent 而不是 Workflow 的？给我一个具体例子。"

- **参考答案**：
  1. 先说判断标准：路径不可预测时用 Agent，可预测时用 Workflow
  2. 给具体项目例子（如 Knowledge Mastery Agent）
  3. 解释为什么它是 Agent（路径动态，根据用户回答决策）
  4. 展示选型判断能力
- **评分要点**：
  1. 有清晰的判断标准
  2. 有具体项目经验或合理模拟
  3. 说清 Agent vs Workflow 的边界
- **知识点**：面试表达

---

## 测试记录

### 2026-04-25 初始测试

| 题号 | 结果 | 备注 |
|------|------|------|
| Q1 | ✅ | |
| Q2 | ✅ | |
| Q3 | ✅ | |
| Q4 | ✅ | |
| Q5 | ⚠️ | 把 Orchestrator-Worker 误认为 Agent |
| Q6 | ✅ | |
| Q7 | ⚠️ | 低估了场景对 Agent 的需求，选了纯 Workflow |
| Q8 | ✅ | |

通过率：6/8 完全正确，2/8 部分正确

---

## A4 默写测试记录

### 2026-04-25 A4 默写

| 知识点 | 结果 | 备注 |
|--------|------|------|
| 1. 增强 LLM | 🟢 通过 | |
| 2. Workflow vs Agent | 🟢 通过 | |
| 3. 五种 Workflow 模式 | 🔴 未通过 | 只记住 Orchestrator-Worker，其余四种遗忘 |
| 4. ReAct 模式 | 🟢 通过 | |
| 5. Plan-and-Execute vs ReAct | 🟢 通过 | |
| 6. Function Calling | 🟢 通过 | |
| 7. 工具设计原则 | 🟢 通过 | 用删除文件例子，具体准确 |
| 8. Multi-Agent 三种模式 | 🟢 通过 | |
| 9. Memory 系统 | 🟡 基本通过 | 记住时效性，遗漏相关性和重要性 |
| 10. 选型决策框架 | 🟡 基本通过 | 漏了 Routing、Orchestrator-Worker、Evaluator-Optimizer |

通过率：6/10 完全通过，2/10 基本通过，2/10 需要加强

下次回测：2026-05-02 周测（优先：五种 Workflow 模式、选型决策框架、Memory 检索三因素）
