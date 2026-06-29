
# PyTorch — AI 笔记

> 来源：PyTorch 官方文档 (pytorch.org/docs/stable)、PyTorch 源代码、d2l.ai (动手学深度学习)、Fast.ai 实战教程
> 生成时间：2026-06-29
> 学习目标：系统掌握 PyTorch 从张量到模型训练部署的完整链路，能独立搭建和训练神经网络

---

## 锚点

**PyTorch 像搭乐高。**

你不是在写模型，你是在一块一块拼计算图。每个 `Tensor` 是一块积木，`nn.Module` 是把积木拼成功能件的模具，Autograd 是个录像机——默默记住你每一步怎么拼的，Optimizer 是最后按一下"自动重拼"按钮的手。

搭乐高的好处是：你能控制每一块。不想用现成的轮子？自己造一块。看别人拼好了不知道怎么改的？拆开看每一步怎么走的。这就是 PyTorch 和 Keras 的最大区别——它给你的不是成品，是零件。

---

## 核心问题

**为什么训练神经网络这么难管理？**

核心矛盾在于：你写的是一堆数学运算，但你要追踪的是"每个参数对最终误差有多大责任"。没有 PyTorch 的话，你得手算每条链上的偏导数。一个 10 层的网络，每层 100 个神经元——人力已经不可能了。

PyTorch 做的事很简单：**你只管往前算，它自动记下来怎么倒回去**。

---

## 核心概念

### Tensor——最底层的积木

`Tensor` 是 PyTorch 的积木块。跟 NumPy 的 `ndarray` 几乎一样——多维数组、切片、广播——但多了两件事：**能搬到 GPU 上**，**能自动记住怎么算出它来的路径**。

比如你创建一个形状是 `(3, 4)` 的随机数矩阵，在 NumPy 里叫 `ndarray`，在 PyTorch 里叫 `Tensor`。你用 `+`、`*`、`@` 做运算的方式也一样。但 PyTorch 的 tensor 可以 `.to('cuda')` 搬到显卡上算，速度翻几十倍。

> 为什么重要：没有 Tensor，PyTorch 就不存在。它是所有运算的基础单位。NumPy 的用户上手 PyTorch，第一件事就是习惯把 `np.array(...)` 换成 `torch.tensor(...)`。

### Autograd——录像机

既然 Tensor 是一块积木，Autograd 就是那个录像机：你每拼一步（做一次运算），它都记下来"谁跟谁拼在一起了"。

具体来说：每个 Tensor 上有个 `.grad_fn` 属性。你做了 `c = a + b`，那 `c.grad_fn` 就指向一个 `AddBackward` 节点，里面存着"c 是由 a 和 b 相加得到的"。你做了 `d = c * w`，那 `d.grad_fn` 就指向 `MulBackward`，里面连着 `c` 和 `w`。

这些 `.grad_fn` 连起来，就形成了一张计算图。你调 `d.backward()` 的时候，Autograd 沿着这张图往回走，给每个需要梯度的 tensor 算偏导数，填到 `.grad` 属性里。

不用 Autograd 的话，你层数一深就要手算链式法则，数学上能算，工程上累死。

### nn.Module——功能件的模具

大部分神经网络层（全连接、卷积、RNN）结构太相似了，每次手写参数矩阵太浪费。`nn.Module` 就是一个基类，帮你把参数注册、forward/backward 的联动、子模块嵌套这些事情封装好。

你写一个自定义层，就继承 `nn.Module`，在 `__init__` 里声明用到的子层和参数，在 `forward` 里写前向计算。剩下的——参数管理、设备迁移、梯度计算——PyTorch 帮你搞定。

```python
class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc(x)
```

> 为什么重要：没有 `nn.Module`，你每次都要手动管理参数列表、手动调 `requires_grad_()`、手动把每个参数搬到 GPU。容易漏、容易错。

### nn.Linear / Conv2d / ...——现成的功能件

PyTorch 在 `torch.nn` 下提供了大多数常见网络层：`Linear`（全连接）、`Conv1d/2d`（卷积）、`LSTM`、`BatchNorm`、`Dropout`、`ReLU` 等激活函数。

它们都是 `nn.Module` 的子类。你不需要自己写参数矩阵的乘法和偏置加法——`nn.Linear(in_features, out_features)` 就是干这个的。它帮你创建了权重矩阵 W 和偏置 b，并且自动标记 `requires_grad=True`。

### 损失函数——偏差尺子

网络输出和真实标签之间的差异需要量化。这就是损失函数。

PyTorch 在 `torch.nn` 里提供了 `MSELoss`（回归用）、`CrossEntropyLoss`（分类用）、`BCEWithLogitsLoss`（二分类用）等。用法统一：`loss = loss_fn(pred, target)`，输入输出都是 tensor。

> 选损失函数的关键：看你的任务类型。分类用交叉熵，回归用 MSE。常见错误是分类任务直接用 MSE，收敛慢还容易卡住。

### Optimizer——负责扭螺丝的人

损失算出来了，梯度也算出来了，但怎么更新参数？这就是 Optimizer 的事。

PyTorch 的 `torch.optim` 提供了 `SGD`、`Adam`、`AdamW`、`RMSprop` 等优化器。你给它一组要更新的参数（通常是 `model.parameters()`），然后循环里三步：`optimizer.zero_grad()` 清旧梯度 → `loss.backward()` 算新梯度 → `optimizer.step()` 更新参数。

```python
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
```

Adam 一般是最省心的默认选择。SGD + Momentum 需要更多调参经验，但某些场景泛化更好。

### Dataset + DataLoader——材料输送带

训练的数据通常是成百上千个样本，一次全算内存不够，一个个算又太慢。解决方案是分 batch。

`torch.utils.data.Dataset` 是一个抽象类：你继承它，实现 `__len__`（数据总量）和 `__getitem__`（根据索引取一个样本），PyTorch 就知道怎么取数据了。

`torch.utils.data.DataLoader` 包装 Dataset，帮你做四件事：**分批**（batch_size）、**打乱**（shuffle）、**多进程并行加载**（num_workers）、**自动组装**（collate_fn）。

```python
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

### Training Loop——装配流水线

所有零件拼起来，形成训练循环。每次循环做：

1. 取一个 batch 的数据
2. 前向传播：模型预测 → 算损失
3. 反向传播：`loss.backward()` 算梯度
4. 更新参数：`optimizer.step()`
5. 清梯度：`optimizer.zero_grad()`
6. 记录指标（损失、准确率等）

```python
for epoch in range(num_epochs):
    for x, y in dataloader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### Device Management——在哪搭

训练默认在 CPU 上跑。想用 GPU 需要手动迁移：`tensor.to('cuda')`、`model.to('cuda')`。

PyTorch 的习惯写法是先检测可用设备，再统一迁移：

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
```

Mac 的 M 芯片上可以用 `mps`（Metal Performance Shaders）：
```python
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
```

注意：直接混用 CPU tensor 和 GPU tensor 做运算会报错。模型和数据必须在同一个设备上。

### Save / Load——拍照留存

训练好的模型需要保存。两种做法：

1. **保存整个模型**：`torch.save(model, 'model.pth')`——不推荐，因为 pickle 的序列化方式有兼容问题
2. **保存 state_dict**（推荐）：`torch.save(model.state_dict(), 'model.pth')`——只存参数，不存模型结构定义

```python
# 保存
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pth')

# 加载
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
```

---

## 关键代码模式

### 完整的训练 + 验证循环

```python
def train_one_epoch(model, loader, loss_fn, optimizer, device):
    model.train()
    total_loss = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    return total_loss / len(loader)

def validate(model, loader, loss_fn, device):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            pred = model(x)
            loss = loss_fn(pred, y)
            total_loss += loss.item()
    return total_loss / len(loader)
```

注意：验证时用 `with torch.no_grad()` 关掉梯度追踪，既省显存又提速。

### 自定义 Dataset

```python
class MyDataset(Dataset):
    def __init__(self, data, labels):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
```

### Gradient Accumulation——显存不够时的变通

一个 batch 太大 GPU 放不下？拆成小 batch 累加梯度：

```python
for i, (x, y) in enumerate(loader):
    x, y = x.to(device), y.to(device)
    loss = loss_fn(model(x), y)
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

相当于每个 optimizer.step() 吃进了 accumulation_steps 个 mini-batch 的梯度总和。

---

## 逐节详解

### Section 1: Tensor 基础

你拿到 PyTorch，第一件事肯定是创建 tensor。

但 Tensor 最困惑人的地方不是怎么创建，而是 **它跟 NumPy 到底哪里不一样**。

表面上看——一模一样。`torch.tensor([1, 2, 3])` 和 `np.array([1, 2, 3])`，索引切片广播都一样。连 `torch.randn` 到 `np.random.randn` 的对应关系也没变。

但本质区别有三：

1. **设备感知**：NumPy 的数据永远在 CPU 内存里。Tensor 可以在 CPU、GPU、MPS 上，并且能在它们之间迁移。这个差异决定了 PyTorch 能做的计算规模是 NumPy 打不到的——一张 A100 有 80GB 显存和数千个核，比 CPU 快几十倍。

2. **梯度追踪**：创建 tensor 时设 `requires_grad=True`，PyTorch 就会自动追踪对这个 tensor 的所有运算。NumPy 没有也不可能有这个功能，因为它是数值计算库而不是自动微分框架。

3. **计算图感知**：NumPy 做 `c = a + b`，结果就是一个数组，不记得自己怎么来的。PyTorch 做同样的运算，`c` 的 `.grad_fn` 指向运算的源头。这是 Autograd 能工作的前提。

创建方式有几种：
- `torch.tensor(data)` — 从 Python 列表或 NumPy 数组创建
- `torch.zeros(3, 4)` / `torch.ones(3, 4)` — 全零/全一
- `torch.randn(3, 4)` — 标准正态分布随机
- `torch.arange(10)` — 类似 range
- `torch.eye(3)` — 单位矩阵

形状操作跟 NumPy 一样：`.view()`（resize）、`.reshape()`、`.transpose()`、`.squeeze()`、`.unsqueeze()`。

### Section 2: Autograd 工作原理

你在 `loss.backward()` 之前得搞清楚一件事：**Autograd 到底记了什么**。

核心数据结构是 **计算图** (computational graph)。它是一个 DAG（有向无环图），每个节点是一个 tensor，每条边是运算关系。

假设：
```python
x = torch.tensor([2.0], requires_grad=True)
w = torch.tensor([3.0], requires_grad=True)
b = torch.tensor([1.0], requires_grad=False)
y = w * x + b   # y = 3*2 + 1 = 7
```

计算图长这样：
```
x --\
     -> Mul -> Add -> y
w --/      |
           b
```

当你调 `y.backward()`，Autograd 从 y 开始，沿边反向传播。它做的是链式法则自动求导：
- `dy/dx = w = 3` → `x.grad = 3`
- `dy/dw = x = 2` → `w.grad = 2`
- `dy/db = 1` → b 没有 requires_grad，所以不保存 grad

Autograd 只在 forward 时建图，backward 后默认释放图（`retain_graph=True` 可以保留）。这也是为什么每次循环里都要先 `forward` 再 `backward`——图是每轮重建的。

> 注意：`requires_grad=True` 是有传播性的。你对一个 requires_grad=True 的 tensor 做运算，结果 tensor 也会 requires_grad=True。所以你不需要手动标记每个中间变量。

### Section 3: nn.Module 的工作方式

你肯定写过 `class MyModel(nn.Module)`，但 `nn.Module` 到底帮你做了什么？

三件事：

**参数注册**：你在 `__init__` 里 `self.fc = nn.Linear(10, 5)` 时，`nn.Module` 的 `__setattr__` 会检测到赋值的对象也是一个 `nn.Module`，自动把它注册成子模块。之后调 `model.parameters()` 就可以递归获取所有参数。

**设备迁移**：`model.to(device)` 会把模型的所有参数和缓冲区递归迁移到目标设备。你不需要一个个参数去调 `.to()`。

**训练/评估模式切换**：`model.train()` 和 `model.eval()` 会递归设置所有子模块的模式。Dropout 和 BatchNorm 在两种模式下行为不同，这个切换是它们正常工作需要的前提。

你可能遇到的坑是：在 `__init__` 里直接赋值（不是用 `nn.Parameter` 或 `nn.Module`）的参数，不会自动注册：
```python
class BadNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.W = torch.randn(10, 5)  # 不会被跟踪！
```

正确的做法是用 `nn.Parameter` 或把参数放在 `nn.Module` 子模块里：
```python
class GoodNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.W = nn.Parameter(torch.randn(10, 5))
```

### Section 4: 训练循环的常见陷阱

训练循环写错的地方，90% 集中在这几个问题上：

**1. 忘了 zero_grad()**

梯度的计算是累积的。这本来是个特性（你可以用梯度累积模拟大 batch），但如果你忘了清，每轮的梯度会和前一轮叠加：
```
epoch 1: grad = g1
epoch 2: grad = g1 + g2  ← 错的
epoch 3: grad = g1 + g2 + g3  ← 更错
```

所以 `optimizer.zero_grad()` 必须在 `backward()` 前执行。常见的放法是每个 batch 循环的开头。

**2. 忘了 model.eval() 和 torch.no_grad()**

验证/测试时，Dropout 应该关闭，BatchNorm 应该用运行均值和方差，而且不需要算梯度。`model.eval()` 管前三者，`torch.no_grad()` 管最后一个。

少了哪个都不会报错，但验证结果会偏低或者不一致。这是最难排查的 bug 之一。

**3. 在 .item() 和 .detach() 之间选错**

- `.item()`：把一个单元素 tensor 转成 Python 数字。用于记录 loss 值。
- `.detach()`：返回一个和原 tensor 共享数据但不追踪梯度的新 tensor。用于在需要 tensor 值但不需要梯度时切断计算图。

如果你在验证循环里忘了用 `.detach()` 或 `torch.no_grad()`，计算图会在验证时继续建——通常不会报错，但显存会爆炸，因为图永远不会释放。

### Section 5: 数据处理与 DataLoader 深入

`DataLoader` 是容易低估复杂度的组件。你写 `for x, y in loader` 一行，背后发生了这些事：

1. **采样**（Sampler）：决定每轮取哪些索引。`shuffle=True` 时用 `RandomSampler`，否则用 `SequentialSampler`。你也可以自定义 Sampler 实现加权采样。

2. **分批**：把一批索引传递给 Dataset，获取样本。

3. **自动组装**（collate_fn）：默认行为是把一组样本堆叠成 batch。但如果样本形状不同（比如变长文本），默认的堆叠会报错，这时需要自定义 `collate_fn`，比如 padding 到相同长度。

4. **多进程加载**（num_workers）：`num_workers > 0` 时启动子进程预加载数据。不是越多越好——太大了会因进程切换开销反而变慢。

一个典型陷阱：在 `__getitem__` 里做了昂贵的计算（如图像解码），而且没有缓存。那每个 epoch 都要重算一遍，训练慢得离谱。解决方案是预处理后存成 tensor 文件，或者用 `torchdata` 的缓存机制。

---

## 与其他框架的对比

讨论框架对比前得先把问题分清楚。TensorFlow、PyTorch、JAX 要解决的是同一个问题吗？是，但切入角度不一样。

**TensorFlow 1.x** 的思路是"你先建好一个静态图，然后喂数据进去跑"。好处是部署高效，缺点是你没法在运行中途调试代码，因为图是建好了再跑的。你在 `tf.Session().run(...)` 里打 `print` 打印不出来，需要 `tf.Print` 这种特殊 op。

**PyTorch** 的思路是"你正常写 Python 代码，每一步都真实执行了"。你在 forward 里加个 `print(x.shape)`，它就真的打印了。这种模式叫"动态图"或"define-by-run"——边跑边建图。

**TensorFlow 2.x** 后来也学了 PyTorch 的 eager execution（默认动态），但它骨子里的静态图 DNA（通过 tf.function）还在。你加个 `@tf.function`，它就编译成静态图提速。好处是兼顾了调试体验和运行效率，坏处是两套模式之间的微妙差异容易踩坑。

**JAX** 的路线更激进：函数式编程风格，数据不可变，没有状态。你用 `jax.grad` 自动求导，用 `jax.jit` 即时编译。好处是性能极致（XLA 编译），坏处是调试复杂、学习曲线陡。

| 维度 | PyTorch | TensorFlow 2.x | JAX |
|------|---------|---------------|-----|
| 执行模式 | 动态图（define-by-run） | 动态 + 静态（@tf.function） | 函数式 + JIT 编译 |
| 学习曲线 | 平缓（像写普通 Python） | 中等 | 陡峭（函数式思维） |
| 调试友好度 | ⭐⭐⭐⭐⭐（能用 pdb） | ⭐⭐⭐（静态图段需 tf.function） | ⭐⭐（函数式栈更难追踪） |
| 部署生态 | TorchServe、ONNX、torch.jit | TF Serve、TFLite、TF.js | 弱（社区方案为主） |
| 研究使用率 | 极高（CV、NLP、RL 主流） | 中（工业部署为主） | 上升中（特别是 LLM 训练） |
| 自动微分 | Autograd（动态图追踪） | GradientTape（类似） | grad（函数式变换） |
| 分布式训练 | DDP（成熟）、FSDP | MirroredStrategy、TPU 生态 | pmap、顶级大模型训练 |
| 社区生态 | HuggingFace 默认、Lightning | Keras、TF Hub | 较小但增长快 |

选择建议：做研究、快速验证想法 → PyTorch。做工业级部署、已有 TF 生态 → TensorFlow。做大模型训练、追求极致性能 → JAX。

---

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| autograd 机制 | 你真的理解反向传播怎么实现 | 动态计算图、DAG、每个 tensor 有 grad_fn、backward() 走图反向传播 | 只背了"自动求导"四个字，讲不清计算图 |
| 什么时候 .backward() 会报错 | grad 是否匹配 | scalar loss 可以无参数调用；非标量需要传 grad_output，形状和输出一致 | 不知道非标量 loss 需要 grad_output |
| model.eval() vs torch.no_grad() 区别 | 了解训练和推理的不同行为 | eval() 关 Dropout、固定 BatchNorm；no_grad() 关梯度追踪。验证时两个都用 | 以为 eval() 已经关了梯度 |
| DataLoader num_workers 设多快 | 理解多进程加载的代价 | 不是越大越好，超过 CPU 核数反而变慢；GPU 训练时瓶颈常在数据加载 | 以为 num_workers=0 最好 |
| nn.Parameter vs 普通 tensor | Module 的参数注册机制 | nn.Parameter 默认 requires_grad=True，自动注册为模块参数 | 在 __init__ 里直接赋值 tensor 不被跟踪 |
| .detach() 和作用 | 切断计算图的时机 | 返回不追踪梯度的新 tensor，共享内存 | 跟 .item() 和 .data() 混淆 |
| DDP (DistributedDataParallel) 原理 | 分布式训练的理解 | 每个 GPU 一份模型，各算各的梯度，all-reduce 同步 | 错以为 DataParallel 更好（GIL 瓶颈） |
| 梯度累积为何要 optimizer.zero_grad() | Python 内存管理的坑 | 梯度累积本身不会导致显存泄漏，但计算图不释放会 | 不知道有这个问题 |

---

## 深入话题

### 1. 混合精度训练 (AMP)

`torch.cuda.amp` 在训练中用 FP16 做计算、FP32 存参数。这样能从两个方面加速：FP16 计算更快、显存占用减半意味着可以塞更大的 batch。

但直接全 FP16 会导致梯度下溢（underflow）——梯度过小变成 0。所以 AMP 用梯度缩放（Gradient Scaling）：先放大 loss，反向传播出放大的梯度，再缩小回去。

```python
scaler = torch.cuda.amp.GradScaler()
with torch.cuda.amp.autocast():
    pred = model(x)
    loss = loss_fn(pred, y)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### 2. torch.compile——编译加速

PyTorch 2.0 引入的 `torch.compile` 可以把模型编译成更高效的 kernel，无代码修改就能提速 30%-100%。

用法一行：`model = torch.compile(model)`。它会分析模型的计算图，做算子融合和内存优化。

```python
model = MyModel().to(device)
model = torch.compile(model)  # 一行加速
```

### 3. FSDP (Fully Sharded Data Parallel)

当模型大到单张显卡放不下（比如 7B 参数的大语言模型），DDP 不行了——每个 GPU 都存一份完整模型，显存不够。

FSDP 的做法是把模型参数分片到各 GPU 上。每个 GPU 只存一部分参数，计算时再取回需要的参数。这样可以训练单卡放不下的模型，代价是通信开销增加。

---

## 常见误区自查清单

- ❌ 在 `__init__` 里直接赋值 tensor 而不是用 `nn.Parameter` → ✅ 用 `nn.Parameter` 或 `nn.Module` 子模块
- ❌ 验证/测试时忘了 `model.eval()` 和 `torch.no_grad()` → ✅ 两个都加上
- ❌ `loss.backward()` 后忘了 `optimizer.zero_grad()` → ✅ 梯度累加记得确认是故意的
- ❌ CPU tensor 和 GPU tensor 混着做运算 → ✅ 检查 device 一致性
- ❌ `DataLoader(num_workers=0)` 导致 CPU 成瓶颈 → ✅ 根据 CPU 核数设 `num_workers`
- ❌ 保存模型用 `torch.save(model, ...)` → ✅ 用 `model.state_dict()` 保存
- ❌ 使用 `.data` 属性代替 `.detach()` → ✅ `.data` 已废弃，用 `.detach()`
- ❌ `CrossEntropyLoss` 忘了它内部包含 softmax → ✅ 模型最后一层不加 softmax
