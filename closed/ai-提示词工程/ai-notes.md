# Prompt Engineering — AI 笔记

> 来源：
> - [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
> - [Anthropic Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
> - [Anthropic Interactive Tutorial (GitHub)](https://github.com/anthropics/prompt-eng-interactive-tutorial)
> - [Aidan Cooper: Constrained Decoding Guide](https://www.aidancooper.co.uk/constrained-decoding/)
> - [Zachary Levonian: Why Does In-Context Learning Work?](https://levon003.github.io/2024/04/16/incontext-learning.html)
> - [EMNLP 2024: The Mystery of In-Context Learning Survey](https://aclanthology.org/2024.emnlp-main.795/)
> - [PromptLayer: System Prompt vs User Prompt](https://blog.promptlayer.com/system-prompt-vs-user-prompt-a-comprehensive-guide-for-ai-prompts/)
>
> 生成时间：2026-04-24
> 学习目标：面试准备 — 理解 Prompt Engineering 技巧背后的原理（为什么有效）

---

## 一句话总结

Prompt Engineering 的核心技巧（Few-shot、CoT、结构化输出等）之所以有效，是因为它们利用了 LLM 在预训练时学到的模式匹配能力 — 通过在上下文中提供示例和指令，引导模型的注意力机制和 token 预测走向期望的方向。

---

## 核心概念

| # | 概念 | 定义 | 关键细节 |
|---|------|------|----------|
| 1 | In-Context Learning (ICL) | 不更新模型参数，仅通过 prompt 中的示例让模型学会新任务 | 预训练中学到的模式匹配 + 隐式梯度下降 |
| 2 | Few-Shot Prompting | 在 prompt 中提供几个输入-输出示例，引导模型理解任务格式 | 3-5 个多样化的示例效果最好 |
| 3 | Chain-of-Thought (CoT) | 让模型在给出最终答案前展示推理过程 | 激活了预训练中学到的逐步推理模式 |
| 4 | 结构化输出（JSON） | 确保模型输出符合指定格式（如 JSON Schema） | Constrained Decoding：每步屏蔽非法 token |
| 5 | System Prompt | 定义模型的全局行为、角色和安全边界 | 持久、优先级高，模型对其施加不同的注意力权重 |
| 6 | User Prompt | 用户的具体任务请求和输入数据 | 每轮对话可变 |

---

## Section 1: In-Context Learning（上下文学习）

### 什么是 In-Context Learning？

In-Context Learning (ICL) 是指：**不更新模型任何参数，仅通过在 prompt 中提供示例，让模型学会执行新任务。**

示例：

```
将英文翻译成法语：
English: Hello → French: Bonjour
English: Cat → French: Chat
English: Thank you → French: ?
```

模型从没被专门训练过"英译法"这个任务，但看到示例后就能输出 "Merci"。

### ICL 为什么有效？（机制解释）

这是学术界最热门的问题之一，目前的主流解释：

**解释 1：模式匹配（Pattern Completion）**
- LLM 的预训练目标就是"预测下一个 token"
- Prompt 中的示例形成了一个模式："输入 → 输出，输入 → 输出，输入 → ?"
- 模型在预训练时见过大量类似模式（教程、问答、代码示例等）
- ICL 本质上是**触发模型预训练时已学到的模式识别能力**

**解释 2：隐式梯度下降（Implicit Gradient Descent）**
- 研究发现（[von Oswald et al.](https://www.youtube.com/watch?v=TjwYjlzXgts)），Transformer 的前向传播在执行 ICL 时，内部计算类似于梯度下降
- 可以理解为：示例在 Transformer 内部形成了一个"临时的小模型"，专门处理当前任务
- 但这个"学习"不更新权重，只存在于当前前向传播中

**解释 3：贝叶斯推断（Bayesian Inference）**
- 模型在预训练中见过多种任务的分布
- ICL 中的示例相当于"证据"，帮助模型推断当前任务属于哪个分布
- 然后按照推断出的任务分布来生成输出

### 类比理解

| 类比 | 解释 |
|------|------|
| 开卷考试 | 不需要记住所有知识，给你几道例题就能照着做 |
| 模式补全 | 看到数列 2, 4, 6, 8, ? 你不需要懂公式，识别模式就能填 10 |
| 临时工培训 | 不改写工人的大脑，给个操作手册就能上手 |

---

## Section 2: Few-Shot Prompting（少样本提示）

### 什么是 Few-Shot？

在 prompt 中给出几个"输入 → 输出"的示例，然后让模型处理新的输入。

| 模式 | 示例数量 | 适用场景 |
|------|---------|---------|
| Zero-Shot | 0 个 | 简单任务，模型已有足够能力 |
| One-Shot | 1 个 | 给出格式暗示 |
| Few-Shot | 2-5 个 | 需要明确任务格式和风格 |
| Many-Shot | 6+ 个 | 复杂任务，需要更多模式参考 |

### Few-Shot 为什么有效？

**核心原因：消除了任务歧义。**

同样一句"分析这段话的情感"，模型不知道你要：
- 输出 "positive/negative"？
- 输出 1-5 星评分？
- 输出详细分析段落？

给几个示例后，格式和期望就明确了。这不是"教模型新知识"，而是"告诉模型你想要什么格式"。

**深层原因：激活了预训练模式**

LLM 在预训练时见过大量"示例 → 仿照"的模式：
- 教科书：定义 → 例题 → 习题
- 论坛：Q&A 问答对
- 代码：函数签名 + 文档 → 使用示例

Few-Shot 本质上是模拟了这些预训练中常见的结构。

### 最佳实践

1. **示例多样性**：覆盖不同类型的输入，避免模型学到片面模式
2. **示例数量**：3-5 个通常足够，太多会占用上下文窗口
3. **示例顺序**：相关研究表明示例顺序会影响输出（recency bias，靠后的示例权重更大）
4. **示例格式**：使用一致的格式标记（如 `<input>` → `<output>`）

---

## Section 3: Chain-of-Thought（思维链）

### 什么是 Chain-of-Thought？

让模型在给出最终答案前，先输出推理过程。

**Zero-Shot CoT**：
```
这道题的答案是？
请一步步思考。
```

**Few-Shot CoT**：
```
Q: 餐厅有 23 个苹果，用了 20 个做午餐，又买了 6 个，还剩几个？
A: 开始有 23 个苹果。用了 20 个，所以剩下 23 - 20 = 3 个。又买了 6 个，所以现在有 3 + 6 = 9 个。答案是 9。

Q: 杂货店有 15 个橙子，卖了 8 个，又进货了 12 个，还剩几个？
A:
```

### CoT 为什么能提升推理能力？

**原因 1：逐步计算替代一次性计算**

- 没有 CoT 时，模型要在一次前向传播中从输入直接跳到答案
- 这要求模型在一个"步骤"中完成所有推理，超出了单层注意力的能力
- CoT 把复杂推理拆成多个小步骤，每步只需要做简单的模式匹配

**原因 2：生成中间步骤 = 更多的计算层**

- 每生成一个 token，模型都要做一次完整的前向传播
- CoT 让模型多生成 N 个 token = 多做 N 次前向传播 = 多了 N 轮"思考"
- 类似"给草稿纸"：人做复杂计算也需要写中间步骤

**原因 3：自回归的纠错能力**

- 模型生成的每个中间步骤都成为后续步骤的上下文
- 如果某一步推理有误，后续步骤可能通过注意力机制"纠正"
- 但这不是万无一失的，错误也可能传播

### 类比

| 类比 | 解释 |
|------|------|
| 草稿纸 | 复杂心算 vs 写下来一步步算 |
| 编译器优化 | 不优化时直接输出 → 中间变量帮助推理 |
| 深度网络的层数 | 每个中间 token 相当于多了一层"计算层" |

### CoT 的局限性

- 增加输出 token 数，推理成本上升
- 简单任务用 CoT 反而可能引入错误（过度推理）
- CoT 的推理过程不一定是模型真实的"思考过程"，只是看起来合理的文本

---

## Section 4: 结构化输出（JSON）

### 从 Prompt 到 Constrained Decoding 的演进

| 代际 | 方法 | 可靠性 |
|------|------|--------|
| 第 1 代 | Prompt 中说"请输出 JSON" | ~80-95%，不可靠 |
| 第 2 代 | JSON Mode（模型层面保证合法 JSON） | ~99%，但结构不一定对 |
| 第 3 代 | **Constrained Decoding**（基于 Schema 约束） | ~100% |

### Constrained Decoding 的底层原理

LLM 生成文本的过程：

```
每一步：
1. 模型输出所有 token 的原始概率（logits）
2. logits → softmax → 概率分布
3. 按概率采样下一个 token
```

**Constrained Decoding 在第 2 步和第 3 步之间插入一步**：

```
1. 模型输出 logits
2. 根据 JSON Schema 构建合法 token 集合
3. 将非法 token 的 logit 设为 -∞
4. softmax → 非法 token 概率变为 0
5. 从合法 token 中采样
```

具体例子：

```
Schema 要求输出 {"name": "Alice"}

当前已生成：{"name": "

下一步模型可以选的 token：
  "Alice"  → logit = 3.2  → 保留
  "Bob"    → logit = 2.8  → 保留
  "}\n"    → logit = 1.5  → 设为 -∞（这里需要先有值再关引号）
  123      → logit = 0.5  → 设为 -∞（schema 要求 string，不能是数字）
```

### 核心机制：Logit Masking + 有限状态机

1. **有限状态机（FSM/Grammar）**：将 JSON Schema 编译成状态机，每步确定哪些 token 合法
2. **Logit Masking**：将非法 token 的概率置零
3. **采样**：只从合法 token 中选择

### 代价

- **计算开销**：每步都要构建合法 token 集合
- **质量风险**：有时强行限制 token 选择路径，可能导致模型走一条预训练中很少见的路径，输出质量下降
- **非万能**：只能保证格式正确，不能保证内容正确

---

## Section 5: System Prompt vs User Prompt

### 结构上的区别

在 API 调用中，消息分为不同角色（role）：

```python
messages = [
    {"role": "system", "content": "你是一个专业的 Python 编程助手"},
    {"role": "user", "content": "写一个快速排序函数"},
]
```

### 功能上的区别

| 维度 | System Prompt | User Prompt |
|------|--------------|-------------|
| 目的 | 定义全局行为、角色、安全规则 | 提供具体任务请求 |
| 生命周期 | 持久，贯穿整个对话 | 每轮可变 |
| 优先级 | 高 — 模型倾向于遵循 system 指令 | 中 — 在 system 框架内处理 |
| 内容类型 | 角色设定、输出格式、禁止事项、背景知识 | 问题、数据、具体指令 |
| 修改频率 | 很少修改 | 每次请求可能不同 |

### 底层机制：为什么分开？

**模型内部对不同 role 的 token 有不同的处理方式：**

1. **特殊 Token 标记**：不同 API 在消息之间插入特殊 token（如 `<|im_start|>system`、`<|im_start|>user`），模型通过这些标记区分消息边界和角色

2. **注意力权重差异**：研究表明，模型在训练过程中学会了给 system prompt 的 token 分配**更高的注意力权重**。这意味着 system prompt 中的指令在生成时对输出的影响更大

3. **训练数据的结构**：预训练/微调数据中，system-like 指令（如"你是..."、"不要..."）通常与用户查询有明确分隔，模型学会了区分"全局规则"和"当前任务"

### 类比

| 类比 | 解释 |
|------|------|
| 公司制度 vs 工作任务 | System Prompt = 公司制度（不能改，必须遵守），User Prompt = 具体任务（每天不同） |
| 法律 vs 案例 | System = 法律框架（边界），User = 具体案件（在框架内判决） |

### 实践中的建议

- **System Prompt** 放：角色定义、输出格式要求、安全规则、通用背景知识
- **User Prompt** 放：具体任务描述、输入数据、临时指令
- **边界模糊时**：可以测试把指令在 system 和 user 之间移动，看哪种效果更好（不同模型表现不同）

---

## 面试高频考点

| 考点 | 标准答案要点 | 常见错误 |
|------|-------------|----------|
| Few-Shot 为什么有效 | 消除任务歧义 + 激活预训练模式匹配能力 | 以为是"教模型新知识" |
| In-Context Learning | 不更新参数，仅通过上下文示例学习；机制可能是隐式梯度下降或模式补全 | 混淆 ICL 和 fine-tuning |
| CoT 为什么有效 | 拆分复杂推理为多步 + 增加计算轮次 + 中间步骤自纠错 | 以为是"模型更聪明了"，实际是更多计算 |
| JSON 结构化输出 | Constrained Decoding：每步屏蔽非法 token 的 logit | 以为只是 prompt 里说"输出 JSON" |
| System vs User Prompt | 功能分离（全局规则 vs 具体任务），模型对不同 role 有不同注意力权重 | 以为只是 API 设计，没有模型层面的区别 |
