# Attention Is All You Need — 学习进度

> 学习方式：吴恩达式循循善诱教学
> 论文材料：`papers/Attention_Is_All_You_Need-中文翻译.md`
> 我的特点：基础薄弱并且很没有耐心
> 学习状态：**全部学完**
> 完成日期：2026-04-20

---

## 学习进度总览

| 章节 | 状态 | 掌握程度 |
|------|------|---------|
| 摘要 | 已完成 | 完全掌握 |
| 1 引言 | 已完成 | 完全掌握 |
| 2 背景 | 已完成 | 完全掌握 |
| 3 模型架构 - 整体骨架（编码器-解码器） | 已完成 | 完全掌握 |
| 3 模型架构 - 编码器结构 | 已完成 | 完全掌握 |
| 3 模型架构 - 解码器结构 | 已完成 | 完全掌握 |
| 3.2 注意力 - Q/K/V 概念和缩放点积公式 | 已完成 | 完全掌握 |
| 3.2 注意力 - 多头注意力 | 已完成 | 完全掌握 |
| 3.2 注意力 - 三种注意力用法 | 已完成 | 完全掌握 |
| 3.3 前馈网络 | 已完成 | 掌握 |
| 3.4 嵌入和 Softmax | 已完成 | 了解 |
| 3.5 位置编码 | 已完成 | 掌握 |
| 4 为什么用自注意力 | 已完成 | 掌握 |
| 5 训练 | 已完成 | 掌握 |
| 6 结果 | 已完成 | 掌握 |
| 7 结论 | 已完成 | 掌握 |
| 代码实现 - 缩放点积注意力 | 已完成 | 完全掌握 |
| 代码实现 - 多头注意力 | 已完成 | 掌握 |
| 代码实现 - 编码器/解码器层 | 已完成 | 掌握 |
| 代码实现 - 位置编码 | 已完成 | 已看 |
| 代码实现 - 完整 Transformer | 已完成 | 已看 |

---

## 面试高频考点

| 考点 | 你需要记住的 |
|------|------------|
| Transformer 核心思想 | 纯注意力，不用 RNN/CNN |
| 为什么比 RNN 快 | 注意力可并行，RNN 必须串行 |
| 注意力公式 | softmax(QKᵀ/√d_k)V，四步：分缩软乘 |
| 为什么除以 √d_k | 防止点积过大导致 softmax 饱和 |
| 多头注意力 | 512 维拆 8 头各 64 维，每头看所有 token 的不同切面 |
| 编码器子层 | 自注意力 + FFN |
| 解码器子层 | 掩码自注意力 + 交叉注意力 + FFN |
| Cross-Attention QKV 来源 | Q 来自解码器，K/V 来自编码器 |
| 为什么加 mask | 训练时并行输入完整序列，mask 防止偷看未来位置 |
| 位置编码 | 正弦/余弦函数，加到 embedding 上 |
| 消融实验关键发现 | 头数 8 最好，学习的 vs 正弦位置编码效果几乎一样 |
| 翻译成绩 | 英德 28.4 BLEU，英法 41.8 BLEU |

---

## 摘要

**讨论对象：** 序列转换模型。

**旧方法：** 循环神经网络和卷积神经网络，包含编码器和解码器，最优秀的模型还会使用注意力机制将编码器和解码器连接起来。

**新方法** 论文提出：Transformer，只是用注意力机制，不再使用任何循环神经网络或卷积神经网络。

**效果好**：质量高、训练速度快、成本低。泛化性好。

- 质量高：在 WMT 2014 英德翻译任务上，达到 28.4 BLEU，比最好的模型高 2 BLEU 以上。
- 训练速度快、成本低：在 WMT 2014 英法翻译任务上，使用 8 块 GPU 上花费3.5天，达到 41.8 BLEU，成本仅是最好模型的一小部分。
- 泛化性好：在英语句法成分分析任务上，成功应用，无论训练数据是多是少。

---

## 1 引言

### 核心要点（已掌握）

引言讲了三件事：

| 段落 | 核心信息 |
|------|---------|
| 第1-2段 | RNN 是当时的主流，但它必须串行处理，没法并行，训练慢 |
| 第3段 | 注意力机制已经存在，能建模远距离依赖，但之前一直跟 RNN 搭配使用 |
| 第4段 | Transformer：扔掉 RNN，只用注意力，又快又好 |

### 关键理解

- **RNN 的致命缺点**：必须一个词一个词按顺序处理（串行），没法并行，无法充分利用 GPU
- **注意力机制之前的角色**：是 RNN 的辅助插件，不是主角（注：之前用的是注意力机制，不是"自"注意力）
- **Transformer 的核心改变**：把 RNN 完全扔掉，让注意力成为唯一的机制
- **为什么更快**：注意力机制不需要按顺序计算，所有词对之间的关系可以同时算

---

## 2 背景

### 核心要点（已掌握）

**第一类尝试：用 CNN 替代 RNN（ConvS2S、ByteNet）**
- 解决了并行问题
- 但引入新问题：连接远距离位置的操作数随距离增长（ConvS2S 线性增长，ByteNet 对数增长，都不是指数增长）
- 学习远距离依赖仍然费劲

**Transformer 的优势**：操作数是 O(1) 常数级——不管两个词隔多远，连接它们所需的操作数都一样

**第二类尝试：端到端记忆网络**
- 用了循环注意力，在某些简单任务上表现不错
- 但没有彻底摆脱序列化的限制

**关键结论**：Transformer 是第一个完全依赖自注意力、不使用 RNN 或 CNN 的转换模型

**类比**：CNN 像传话游戏（一层层传），注意力机制像微信群聊（所有人同时在线直接对话）

---

## 3 模型架构

### 3.0 整体骨架（已掌握）

Transformer 采用编码器-解码器结构：

```
输入序列 → 编码器（理解输入）→ 特征向量 z → 解码器（生成输出）→ 输出序列
```

**自回归（autoregressive）**：解码器生成每一步都要看自己之前已生成的词。

**关键区别**：
- 训练时：因为有标准答案（teacher forcing），可以用 mask 模拟"不能看未来"，所有位置并行计算
- 推理时：没有标准答案，解码器必须一个词一个词串行生成
- 编码器：无论训练还是推理，都能一次性并行处理完整个输入
- **Transformer 不是在所有环节都并行，但比 RNN 并行的环节多得多，所以整体快得多**

### 3.1 编码器结构（已掌握）

- 由 N=6 个相同层堆叠
- 每层两个子层：
  1. 多头自注意力（Multi-Head Self-Attention）
  2. 前馈神经网络（Feed-Forward Network）
- 每个子层周围使用残差连接 + 层归一化：`LayerNorm(x + Sublayer(x))`
- 所有子层输出维度统一为 d_model = 512（为了残差连接能相加）
- 残差连接的作用：让梯度更容易流动，训练更稳定（像楼梯+电梯，两条路都能走）

### 解码器结构（已掌握）

- 也由 N=6 个相同层堆叠
- 比编码器多一个子层，每层三个：
  1. **掩码**多头自注意力（Masked Self-Attention）→ 只能看当前位置及之前
  2. 编码器-解码器注意力（Cross-Attention）→ Q 来自解码器，K/V 来自编码器
  3. 前馈神经网络

**掩码（Mask）的作用**：训练时并行计算所有位置，但不让当前位置看到后面的位置。实现方式：把非法位置的注意力分数设为 -∞，softmax 后变 0。

**三种注意力的 Q/K/V 来源对比**：

| 类型 | Q 来自 | K 来自 | V 来自 | 特殊之处 |
|------|--------|--------|--------|---------|
| 编码器自注意力 | 编码器上一层 | 编码器上一层 | 编码器上一层 | 无 |
| 解码器掩码自注意力 | 解码器上一层 | 解码器上一层 | 解码器上一层 | 加了 mask |
| 交叉注意力 | 解码器上一层 | 编码器输出 | 编码器输出 | Q 和 K/V 来自不同地方 |

记忆方法：
- Q/K/V 都来自自己 → 自注意力
- Q 来自解码器，K/V 来自编码器 → 交叉注意力
- 在解码器自注意力上加 mask → 掩码自注意力
- **mask 不是单独的输入，是注意力计算过程中的操作（把分数设为 -∞）**

### 3.2 注意力机制（已掌握）

#### 缩放点积注意力公式

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

四步：**分、缩、软、乘**
1. Q × Kᵀ → 算相似度分数（打分）
2. ÷ √d_k → 缩放，防止数值过大
3. softmax → 归一化变成权重（变概率）
4. × V → 加权求和（乘）

**为什么除以 √d_k**：当 d_k 较大时，点积数值会很大，把 softmax 推入梯度极小的区域（饱和）。Q 和 K 各分量独立、均值为 0、方差为 1 时，点积的方差为 d_k。除以 √d_k 把方差拉回 1，让 softmax 正常工作。

**Q/K/V 的直觉**：
- Q（Query）：你想找什么（"我在找跟深度学习相关的信息"）
- K（Key）：每个位置能提供什么（每本书的标题标签）
- V（Value）：匹配到之后实际拿走的内容（书的具体内容）
- 口诀：Q 是问题，K 是标签，V 是内容

#### 多头注意力（Multi-Head Attention）

做法：把 Q、K、V 各投影成 h=8 个版本，每个独立算注意力，最后 concat + 线性变换。

**关键参数**：h=8 个头，每个头 d_k = d_v = 512/8 = 64

**关键理解**：
- 512 维是每个 token 的向量长度（embedding 维度），不是 token 数量
- 多头切分的是每个 token 的 512 维向量，切为 8 份各 64 维
- 每个头都能看到所有 token，只是看到每个 token 的不同维度"切面"
- 不同头学不同关系模式：语法、指代、位置等
- 总计算量与单头几乎相同（512 维拆成 8×64 维）

### 3.3 前馈网络（已掌握）

每个编码器/解码器层都有一个前馈网络：
- 公式：`FFN(x) = max(0, xW₁ + b₁)W₂ + b₂`（两层全连接 + ReLU）
- 逐位置独立：每个 token 各自过网络，token 之间不交互
- 输入输出维度 512，中间隐藏层维度 2048
- 交互工作已由注意力层完成，FFN 负责对每个 token 做非线性变换

### 3.4 嵌入和 Softmax（已了解）

- 用学习的嵌入将输入/输出 token 转为 d_model=512 维向量
- 输入端 embedding、输出端 embedding、softmax 前的线性变换**共享权重矩阵**
- 权重要乘以 √d_model
- 解码器最后输出经线性变换 + softmax 变成词汇表上的概率分布

### 3.5 位置编码（已掌握）

**为什么需要**：Transformer 没有循环和卷积，没有天然的顺序感，必须手动告诉模型位置信息。

**怎么加**：位置编码向量直接加到 token embedding 上：`最终输入 = token embedding + 位置编码`

**论文用的公式**：正弦/余弦函数
- 偶数维度：PE(pos, 2i) = sin(pos / 10000^(2i/d))
- 奇数维度：PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
- 为什么用这个函数：PE(pos+k) 可以表示为 PE(pos) 的线性函数，方便模型学习相对位置
- 也实验了学习的位置嵌入，两者结果几乎相同，选正弦是因为能外推到更长序列

---

## 4 为什么用自注意力（已掌握）

论文从三个维度对比了自注意力、循环层、卷积层：

| 层类型 | 每层复杂度 | 顺序操作数 | 最大路径长度 |
|--------|-----------|-----------|-------------|
| **自注意力** | O(n² · d) | **O(1)** | **O(1)** |
| **循环** | O(n · d²) | O(n) | O(n) |
| **卷积** | O(k · n · d²) | O(1) | O(n/k) |

**关键结论**：
- 并行性：自注意力 O(1)，RNN O(n) → 自注意力赢
- 长程依赖：自注意力 O(1)，RNN O(n) → 自注意力赢（一步连接任意两个位置）
- 计算量：自注意力 O(n²·d)，RNN O(n·d²)，比值 = n/d
  - n < d 时自注意力更快（机器翻译中通常成立，d=512）
  - n > d 时 RNN 更快（超长序列时自注意力有劣势，这也是 Longformer 等后续工作要解决的问题）

**额外好处**：自注意力能产生更可解释的模型——不同注意力头明显学会了执行不同的任务

---

## 5 训练（已掌握）

### 5.1 训练数据

| 任务 | 数据量 | 分词方式 | 词汇量 |
|------|--------|---------|--------|
| 英→德 | ~450 万句对 | byte-pair encoding | ~37,000 |
| 英→法 | ~3600 万句 | word-piece | 32,000 |

### 5.2 硬件和训练时间

| 模型 | GPU | 训练时间 |
|------|-----|---------|
| Base 模型 | 8 × P100 | 12 小时（100K 步） |
| Big 模型 | 8 × P100 | 3.5 天（300K 步） |

### 5.3 优化器

- **Adam**：β₁=0.9, β₂=0.98, ε=10⁻⁹
- **学习率调度**：warmup + decay
  - 前 4000 步：学习率线性增大到峰值
  - 之后：按步数倒数平方根递减

### 5.4 正则化

1. **Dropout（P=0.1）**：随机丢弃 10% 连接，防止过拟合
   - 加在每个子层输出上（残差连接之前）
   - 加在嵌入 + 位置编码的和上
2. **标签平滑（Label Smoothing，ε=0.1）**：正确答案概率从 1.0 降为 0.9，其余 0.1 分给其他词
   - 损害困惑度，但提升 BLEU 分数
   - 模型变得更"谦虚"、更泛化

---

## 6 结果（已掌握）

### 6.1 翻译成绩

- **英→德**：Big 模型 BLEU = 28.4，比之前最佳（含集成模型）高 2 BLEU 以上，8 块 P100 训练 3.5 天
- **英→法**：Big 模型 BLEU = 41.8，单模型新纪录，训练成本不到之前最佳模型的 1/4

推理设置：beam search（beam size=4），平均最后 5-20 个 checkpoint

### 6.2 消融实验

| 变体 | 改了什么 | 结论 |
|------|---------|------|
| (A) 注意力头数量 | 1/4/8/16/32 | 8 头最好，太少不行，太多也降 |
| (B) 键维度 d_k | 减小 d_k | 维度越小质量越差 |
| (C) 模型大小 | 层数/维度 | 越大越好 |
| (D) Dropout | 0.0/0.1/0.2 | 有 dropout 比没有好 |
| (E) 位置编码 | 学习的 vs 正弦 | **结果几乎一样**，选正弦因能外推 |

### 6.3 泛化实验

4 层 Transformer 在英语成分句法分析（WSJ）上 F1 = 91.3，超过了专门的 BerkeleyParser（90.4）

---

## 7 结论（已掌握）

Transformer 是第一个完全基于注意力的序列转换模型，训练快、效果好。在翻译任务上刷新 SOTA。未来可扩展到文本以外的模态。

---

## 代码实现（已掌握核心组件）

### 缩放点积注意力

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    # 第1步：分 — Q × Kᵀ
    scores = torch.matmul(Q, K.transpose(-2, -1))
    # 第2步：缩 — ÷ √d_k
    d_k = Q.size(-1)
    scores = scores / math.sqrt(d_k)
    # mask：把不该看的位置设为 -1e9（近似 -∞）
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    # 第3步：软 — softmax
    weights = F.softmax(scores, dim=-1)
    # 第4步：乘 — × V
    output = torch.matmul(weights, V)
    return output
```

### 多头注意力

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, h=8):
        self.d_k = d_model // h  # 64
        self.h = h               # 8
        self.W_q = nn.Linear(d_model, d_model)  # 线性投影（可学习）
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)  # 输出融合

    def forward(self, Q, K, V, mask=None):
        # 线性投影 + 拆成 8 头：(batch, seq, 512) → (batch, 8, seq, 64)
        Q = self.W_q(Q).view(batch, -1, h, d_k).transpose(1, 2)
        K = self.W_k(K).view(batch, -1, h, d_k).transpose(1, 2)
        V = self.W_v(V).view(batch, -1, h, d_k).transpose(1, 2)
        # 每个头独立算注意力
        attn = scaled_dot_product_attention(Q, K, V, mask)
        # 拼回来：(batch, 8, seq, 64) → (batch, seq, 512)
        attn = attn.transpose(1, 2).contiguous().view(batch, -1, h * d_k)
        # 输出投影（融合 8 个头的信息）
        return self.W_o(attn)
```

**代码要点**：
- W_q/W_k/W_v 是可学习的线性投影，不是直接拆分。投影让模型能主动选择每个头关注什么
- contiguous() 是 transpose 后 view 前的固定搭配（内存连续性要求）
- W_o 让 8 个头的信息混合融合，不只是简单拼接

### 编码器层 + 解码器层

```python
class EncoderLayer(nn.Module):
    def forward(self, x, mask=None):
        x = self.norm1(x + self.self_attn(x, x, x, mask))  # 自注意力 + 残差 + LN
        x = self.norm2(x + self.ffn(x))                     # FFN + 残差 + LN
        return x

class DecoderLayer(nn.Module):
    def forward(self, x, enc_output, src_mask=None, tgt_mask=None):
        x = self.norm1(x + self.self_attn(x, x, x, tgt_mask))                    # 掩码自注意力
        x = self.norm2(x + self.cross_attn(x, enc_output, enc_output, src_mask))  # 交叉注意力
        x = self.norm3(x + self.ffn(x))                                           # FFN
        return x
```

**代码要点**：
- 残差连接：`x + self_attn(...)`（输入直接加到子层输出上）
- 交叉注意力：`cross_attn(x, enc_output, enc_output)` → Q=x（解码器），K=V=enc_output（编码器）

### 完整 Transformer

```python
class Transformer(nn.Module):
    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        # 编码器：embedding + 位置编码 → 6 层编码
        enc = self.pos_enc(self.src_embed(src))
        for layer in self.encoder_layers:
            enc = layer(enc, src_mask)
        # 解码器：embedding + 位置编码 → 6 层解码
        dec = self.pos_enc(self.tgt_embed(tgt))
        for layer in self.decoder_layers:
            dec = layer(dec, enc, src_mask, tgt_mask)
        # 输出：线性变换 → 概率分布
        return self.output_proj(dec)
```

---

## PyTorch 语法笔记

| 语法 | 含义 |
|------|------|
| `K.transpose(-2, -1)` | 交换最后两个维度，用于矩阵乘法 |
| `masked_fill(mask == 0, -1e9)` | mask 中值为 0 的位置填充 -1e9（近似 -∞） |
| `-1e9` | -1×10⁹，用来近似负无穷（softmax 后变 0） |
| `view(batch, -1, h, d_k)` | reshape，-1 表示自动推断该维度大小 |
| `contiguous()` | transpose 后重新排列内存，使 view 可用 |
| `register_buffer` | 不参与梯度更新，但随模型保存/加载的 tensor |
