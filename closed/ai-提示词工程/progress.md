# Prompt Engineering — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-29（上次 2026-04-24）

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现与整理 | ✅ 已完成 | 5 个 Section 全部生成 |
| 2.1 苏格拉底式精读 | ✅ 已完成 | 5/5 Section |
| 2.2 个人笔记 | ✅ 已完成 | prompt-engineering-personal-notes.md |
| 2.3 模拟题测试 | ✅ 已完成 | 8/9 ✅，掌握度 ~90% |
| 3. 知识检验（A4 默写） | ✅ 已完成 | 掌握度 85%，3 个薄弱点待强化 |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: In-Context Learning | ✅ | 良好 — 理解模式匹配机制 |
| Section 2: Few-Shot Prompting | ✅ | 良好 — 理解消除格式歧义 |
| Section 3: Chain-of-Thought | ✅ | 良好 — 理解分步推理+自纠错 |
| Section 4: 结构化输出（JSON） | ✅ | 良好 — 理解三代演进 + FSM 状态追踪 |
| Section 5: System Prompt vs User Prompt | ✅ | 良好 — 理解训练数据是根本原因 |

## 下次从哪里继续

下次回测：月测 2026-05-24。

周测 2026-04-29 已完成（掌握度 85%）。

## 已掌握的关键知识点

### Section 1: In-Context Learning
- ICL vs fine-tuning：改不改权重
- 模式匹配机制：示例触发预训练中已学到的模式识别能力
- ICL 是临时的，对话结束即消失

### Section 2: Few-Shot Prompting
- 核心价值：消除格式歧义（告诉模型要什么形式的答案）
- 3-5 个多样化示例效果最好

### Section 3: Chain-of-Thought
- 分步推理替代一次性跳到答案
- 每生成一个 token = 一次完整前向传播 = 更多计算量
- 中间步骤可自纠错
- 简单任务不适合用 CoT

### Section 4: 结构化输出（JSON）
- 三代演进：Prompt 提示 → JSON Mode → Constrained Decoding
- Constrained Decoding 核心：logit masking + FSM 状态追踪
- FSM 追踪当前走到 Schema 的哪个位置，决定每步哪些 token 合法
- 代价：可能强制模型走预训练中少见的路径，降低质量
- 只能保证格式正确，不能保证内容正确

### Section 5: System Prompt vs User Prompt
- 功能分离：全局规则 vs 具体任务
- 模型区分三机制：特殊 token 标记、注意力权重差异、训练数据结构
- 根本原因是训练数据结构，其余是结果

### 贯穿主线
- 所有 Prompt Engineering 技巧有效的前提：触发 LLM 预训练时已学到的文本模式

## 被纠正过的误区

1. Few-Shot 核心价值表述为"学会新任务"（被纠正 3 次）→ 正确说法："消除歧义 + 激活预训练模式"
2. ICL 定义遗漏"不更新参数"→ ICL = 不改权重 + 提供示例 + 学会新任务
3. System/User Prompt 功能维度不完整 → System=公司制度（持久），User=每天任务（可变）
