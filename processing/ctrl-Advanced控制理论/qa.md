# 困惑点的问答记录

 ### Q1: App Engineer 和 Proposal Engineer 是什么？

 > 时间：20260622周一
 >
 > 位置：通识问答 — 职业方向调研

 学习 Advanced 控制理论过程中，顺便了解设备控制 / 工业自动化方向相关的职业角色。App Engineer 和 Proposal Engineer 这两个 title 在招聘中常被一起提及，想知道各自做什么、合在一起是什么定位。

 **App Engineer（应用工程师）**

 不是写手机 App 的。更多是理解客户需求、做系统方案设计、设备选型、配置软件/硬件、甚至现场调试。是技术与客户之间的连接器。

 **Proposal Engineer（方案工程师）**

 负责技术投标和方案建议书。包括读懂招标文件、算成本、写技术方案、做报价、评审风险。本质上是用工程师的思维去回答"客户为什么该选我们的方案"。

 **合在一起**

 两者合在一起，就是一个人既懂技术方案，又能把方案写成能赢标的提案。

 **中文译名**

 - **App Engineer** → **应用工程师**
 - **Proposal Engineer** → **方案工程师**
 - 合称：**应用与方案工程师**

 在 PCB 设计工具、测试测量、工业控制、智能制造等领域很常见。如果走**设备控制 / 工业自动化**方向，这个角色对标得比较准——这类项目本质上是非标定制，需要先把客户的生产需求翻译成控制方案，再把方案写成投标文件去落地。

---

 ### Q2: 电力系统 — 建立状态空间方程的推导步骤

 > 时间：20260623
 >
 > 位置：DR_CAN [2] 状态空间 State Space
 >
 > 电路：串联 RLC 电路，电压源 $v_s(t)$，串联电阻 $R$、电感 $L$、电容 $C$

 **1. 选择状态变量**

 选电容电压 $v_C$ 和电感电流 $i_L$ 作为状态变量（因为能量储存在电容和电感里）：

 $$z = \begin{bmatrix} v_C \\ i_L \end{bmatrix}$$

 **2. 写基尔霍夫方程**

 KVL（沿回路绕一圈）：

 $$v_R + v_L + v_C = v_s$$

 **3. 代入元件特性**

 | 元件 | 特性关系 |
 |---|---|
 | 电阻 | $v_R = R \cdot i_L$ |
 | 电感 | $v_L = L \cdot \frac{di_L}{dt}$ |
 | 电容 | $i_C = C \cdot \frac{dv_C}{dt}$，串联电路中 $i_C = i_L$ |

 代入 KVL：

 $$R i_L + L \frac{di_L}{dt} + v_C = v_s$$

 **4. 整理成状态变量的导数表达式**

 电容：
 $$\dot{v}_C = \frac{1}{C} i_L$$

 电感（从 KVL 解出 $\frac{di_L}{dt}$）：
 $$\dot{i}_L = -\frac{1}{L} v_C - \frac{R}{L} i_L + \frac{1}{L} v_s$$

 **5. 写成矩阵形式 $\dot{z} = Az + Bu$**

$$
 \begin{bmatrix} \dot{v}_C \\ \dot{i}_L \end{bmatrix}
 = \begin{bmatrix} 0 & \frac{1}{C} \\ -\frac{1}{L} & -\frac{R}{L} \end{bmatrix}
 \begin{bmatrix} v_C \\ i_L \end{bmatrix}
 + \begin{bmatrix} 0 \\ \frac{1}{L} \end{bmatrix} v_s
$$

 所以：

 $$A = \begin{bmatrix} 0 & \frac{1}{C} \\ -\frac{1}{L} & -\frac{R}{L} \end{bmatrix}, \quad
 B = \begin{bmatrix} 0 \\ \frac{1}{L} \end{bmatrix}$$

 **6. 输出方程**

 如果输出 $y = v_C$（比如测电容两端电压）：

 $$y = \begin{bmatrix} 1 & 0 \end{bmatrix} \begin{bmatrix} v_C \\ i_L \end{bmatrix} + [0] v_s$$

 即 $C = [1 \; 0], \; D = 0$。

**验证**：检查 A 的维数 — 2 个状态变量，A 是 2×2 矩阵，和弹簧-质量-阻尼系统是一致的。

---

 ### Q3: 拉普拉斯变换是什么 + 怎么用它解状态空间方程

 > 时间：20260623
 >
 > 位置：DR_CAN [2] 状态空间 State Space — 推导 $G(s) = C(sI-A)^{-1}B + D$

**定义**

 $$F(s) = \int_{0}^{\infty} f(t) e^{-st} dt$$

 它是把时域函数 $f(t)$ 映射到复频域 $F(s)$ 的变换，其中 $s = \sigma + j\omega$。

**为什么用**

 控制系统的核心是微分方程。拉普拉斯变换把**时域的微分方程**转成**s 域的代数方程**，解完再做逆变换回到时域。

**常用的变换对**

 | 时域 $f(t)$ | s 域 $F(s)$ | 说明 |
 |---|---|---|
 | $\dot{x}(t)$ | $sX(s) - x(0)$ | 一阶导数 |
 | $\ddot{x}(t)$ | $s^2X(s) - sx(0) - \dot{x}(0)$ | 二阶导数 |
 | $\int f(t) dt$ | $F(s)/s$ | 积分 |
 | 单位阶跃 $1(t)$ | $1/s$ | 从 0 跳变到 1 |
 | $e^{at}$ | $1/(s-a)$ | 指数函数 |
 | $\sin(\omega t)$ | $\omega/(s^2+\omega^2)$ | 正弦信号 |

 **核心规律**：时域求导 → s 域乘以 $s$（并减去初值）；时域积分 → s 域除以 $s$。

 <br>

**从状态空间推导 $G(s)$**

 **Step 1：对状态方程 $\dot{z} = Az + Bu$ 做拉普拉斯变换**

 左边 $\dot{z}$ 变换后是 $sZ(s) - z(0)$，右边 $Az$ 变换后是 $AZ(s)$，$Bu$ 变换后是 $BU(s)$：

 $$sZ(s) - z(0) = AZ(s) + BU(s)$$

 **Step 2：解出 $Z(s)$**

 把 $Z(s)$ 项移到左边：

 $$sZ(s) - AZ(s) = z(0) + BU(s)$$
 $$(sI - A)Z(s) = z(0) + BU(s)$$

 左乘 $(sI - A)^{-1}$：

 $$Z(s) = (sI - A)^{-1}z(0) + (sI - A)^{-1}BU(s)$$

 **Step 3：解出输出 $Y(s)$**

 对输出方程 $y = Cz + Du$ 做拉普拉斯变换：

 $$Y(s) = CZ(s) + DU(s)$$

 代入 $Z(s)$：

 $$Y(s) = C(sI - A)^{-1}z(0) + \bigl[C(sI - A)^{-1}B + D\bigr]U(s)$$

 **Step 4：提取传递函数**

 $G(s) = C(sI - A)^{-1}B + D$ 就是系统的**传递函数**。它描述的是零初始状态下、输入到输出的关系。

 其中：

 | 项 | 名称 | 含义 |
 |---|---|---|
 | $C(sI - A)^{-1}z(0)$ | **零输入响应** | 靠初始状态 $z(0)$ 自己演变，不加输入 |
 | $[C(sI - A)^{-1}B + D]U(s)$ | **零状态响应** | 初始为零，全靠输入 $u(t)$ 驱动 |

 **Step 5：做拉普拉斯逆变换回到时域**

 $$z(t) = \mathcal{L}^{-1}\{Z(s)\}, \quad y(t) = \mathcal{L}^{-1}\{Y(s)\}$$

 常用的逆变换通过查表配合部分分式展开（partial fraction expansion）完成。
