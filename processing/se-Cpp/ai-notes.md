# C++ 嵌入式自动控制实战 — AI 笔记

> 来源：C++ Primer（精选）、cppreference.com、《Embedded Programming with Modern C++》、Effective Modern C++（精选）
> 生成时间：2026-06-29
> 学习目标：掌握 C++ 核心特性，能独立编写嵌入式自动控制（传感器、驱动、控制算法等）C++ 代码

---

## 锚点

**"C++ 是 C 的增强版 SDK"**

想象你原来用 C 写控制代码的情景：一个 PID 控制器要分别写 float 版和 int 版（因为 C 不支持模板）；一个设备驱动要手动维护状态结构体和函数指针表（因为 C 没有类）；一个串口缓冲区要自己 malloc/free 并确保每个分支都有 free（因为 C 没有 RAII）。

C++ 做的，就是用编译器帮你自动生成这些重复劳动——模板替代手写多份代码，类把数据和函数打包，构造函数和析构函数替你做资源的自动获取和释放。你要做的只是"说清楚规则"，剩下的编译器帮你搞定。

嵌入式场景下 C++ 的黄金法则是：**零开销抽象（Zero Overhead Abstraction）**——用 C++ 的特性不会比手写 C 更低效，但你代码量减半、bug 减半。

## 核心问题

用 C 写嵌入式控制代码，最痛苦的是这三件事：
1. **重复** — 每换一种数据类型（float/int/fixed_point）就要重写一遍控制算法
2. **资源管理** — GPIO 申请了就要释放、DMA 缓冲区用完要归还，C 里全靠纪律
3. **设备扩展** — 一个控制器要支持多种传感器（温度、压力、编码器），C 里靠函数指针表，维护起来像走钢丝

C++ 怎么解决这三件事的？模板干掉重复，RAII 接管资源管理，多态让你轻松扩展设备类型。

---

## 核心概念

### 从 C 到 C++ 的"捷径"（三天上手）

你有 C 基础，这意味着 C++ 的 80% 语法你其实已经会了——if/while/for/switch/数组/指针/位运算和 C 完全一样。你需要学的只是 C++ 新增/改动的部分：

**引用 &：** 指针的语法糖，声明时必须绑定，不能为 nullptr，用起来像值类型。嵌入式里做函数参数传递时，引用比指针更安全（不用检查空指针）。

**函数重载：** 多个同名函数，参数不同，编译器自动选匹配的那个。C 里得写成 `pid_init_f`、`pid_init_i`，C++ 里都叫 `init`。

**命名空间 namespace：** 给代码分组用的文件夹系统，防止你用一个别人的电机库时和你的代码变量名撞车。

#### 引用 vs 指针

这是初学者最容易卡的地方。记住这几个差异就行：

| 维度 | 引用 | 指针 |
|------|------|------|
| 能否为空 | 必须绑定对象 | 可以为 nullptr |
| 能否改绑 | 终生绑定一个对象 | 可以指向不同的对象 |
| 语法 | 像普通变量一样用 | 需要 * 解引用 |
| 内存占用 | 0（编译器优化掉） | 8 字节（64位） |

嵌入式场景记住一句话：**输入参数用 const 引用，输出参数用指针或引用，可选参数用指针（因为能传 nullptr）。**

#### auto 和范围 for

C++11 引入的语法糖。`auto x = sensor.read()` 自动推导类型。`for(auto& val : array)` 代替 `for(int i=0; i<n; i++)`。你写 Python 的应该很熟悉这个感觉。

### 类和对象：把数据和操作打包在一起

C 语言写设备驱动的典型模式：
```c
struct Motor {
    int pin_pwm;
    int pin_dir;
    int speed;
};

void motor_setSpeed(struct Motor* m, int speed) {
    m->speed = speed;
    analog_write(m->pin_pwm, speed);
}
```

C++ 把这个模式升级为语言内置的**封装**：
```cpp
class Motor {
    int pin_pwm;
    int pin_dir;
    int speed;
public:
    Motor(int pwm, int dir) : pin_pwm(pwm), pin_dir(dir), speed(0) {}

    void setSpeed(int s) {
        speed = s;
        analogWrite(pin_pwm, speed);
    }
};
```

C 靠命名约定（`motor_` 前缀）暗示"这个函数是操作 Motor 的"，C++ 靠 `Motor::setSpeed` 编译器强制保证。调用也从 `motor_setSpeed(&m, 100)` 变成了 `m.setSpeed(100)`——少写一个参数，代码也更自然。

#### 对嵌入式开发者最重要的类特性

**构造/析构函数**是最值钱的。构造是"一创建就自动初始化"，析构是"一销毁就自动清理"。

```cpp
class GpioOutput {
    int pin;
public:
    GpioOutput(int p) : pin(p) {
        pinMode(pin, OUTPUT);      // 构造：自动初始化
    }
    ~GpioOutput() {
        pinMode(pin, INPUT);       // 析构：自动恢复
    }
    void write(bool val) { digitalWrite(pin, val); }
};

// 使用：离开作用域自动调用析构，自动恢复为输入模式
{
    GpioOutput led(13);
    led.write(HIGH);
    delay(1000);
    led.write(LOW);
}
```

这个模式叫 **RAII**，后面有专门一节。

### 继承与多态：写出可扩展的设备框架

自动控制项目中经常遇到：一个控制板，接了温度传感器、压力传感器、编码器，读取方式不同（I2C/SPI/ADC），但上层希望"统一读取接口"。

C 的解决方案：函数指针结构体
```c
struct Sensor {
    int (*read)(void);
    int type;
};
int read_temp() { /* I2C读温度 */ }
int read_pressure() { /* SPI读压力 */ }
struct Sensor s = { .read = read_temp };
s.read();
```

C++ 的方案：虚函数 + 继承
```cpp
class Sensor {
public:
    virtual int read() = 0;  // 纯虚函数 = 接口声明
    virtual ~Sensor() {}
};

class TempSensor : public Sensor {
    int read() override {
        return i2c_read(0x48);
    }
};

class PressureSensor : public Sensor {
    int read() override {
        return spi_read(CS_PIN);
    }
};
```

**虚函数的工作机制**：每个含虚函数的类，编译器生成一个**虚函数表（vtable）**——指向各虚函数实现地址的指针数组。调用 `sensor->read()` 时，运行时根据对象的实际类型去 vtable 里找正确的地址。代价是一次间接寻址，仅此而已。

### 模板：给你的算法加一层"类型参数化"

嵌入式自动控制里最典型的需求：写一个 PID 控制器。

C 里写三份：
```c
typedef struct { float kp, ki, kd, ...; } PidF;
typedef struct { int kp, ki, kd, ...; } PidI;
// 然后分别写 set_param、compute... 各三遍
```

C++ 模板让你写一次：
```cpp
template<typename T>
class Pid {
    T kp, ki, kd;
    T target, integral, last_error;
public:
    Pid(T p, T i, T d) : kp(p), ki(i), kd(d),
        target(0), integral(0), last_error(0) {}

    T compute(T current) {
        T error = target - current;
        integral += error;
        T derivative = error - last_error;
        last_error = error;
        return kp * error + ki * integral + kd * derivative;
    }
};

Pid<float> speed_control(1.5, 0.1, 0.05);  // 浮点版
Pid<int> position_control(10, 2, 1);       // 整数版
```

编译器给你自动生成两份代码，等价于你手写两份，维护成本从两份变成一份。

#### 模板的嵌入式使用原则
- 模板在编译期展开，不产生运行时开销
- 留意模板膨胀——如果每个模板实例化差异很大，体积会涨
- 运行时多态用虚函数，编译期多态用模板，不要互相替代

### RAII：C++ 最值钱的特性

RAII 是 C++ 对资源管理的核心贡献。名字拗口，但本质只有一句话：**构造时获取资源，析构时释放资源。**

嵌入式典型应用：
```cpp
class SpiTransaction {
    int cs_pin;
public:
    SpiTransaction(int cs) : cs_pin(cs) {
        spi_begin();
        digitalWrite(cs, LOW);
    }
    ~SpiTransaction() {
        digitalWrite(cs, HIGH);
        spi_end();
    }
};

// 使用
void readSensor() {
    SpiTransaction t(CS_PIN);  // 自动选中
    uint8_t data = spi_transfer(0x00);
    // 离开作用域 → 自动释放 CS + SPI 总线
}
```

C 里你需要记得在每个 return 分支手动释放资源。C++ 里，对象出作用域，析构函数自动执行。

### 智能指针（嵌入式场景谨慎使用）

- `unique_ptr<T>`：独占所有权，拷贝禁止，移动转移。开销 = 裸指针
- `shared_ptr<T>`：共享所有权，引用计数。开销 = 裸指针 + 原子计数

嵌入式建议：**优先 unique_ptr（零额外开销）。shared_ptr 在资源受限时慎用。**

单片机上大多数时候直接用栈分配——`Sensor s;` 就够了，new/delete 少用。

### Modern C++ 实用特性（C++11~17）

| 特性 | 作用 | 嵌入式推荐 |
|------|------|-----------|
| `auto` | 自动类型推导 | ✅ 随便用 |
| `nullptr` | 代替 NULL（类型安全） | ✅ 随便用 |
| `constexpr` | 编译期计算，零运行时开销 | ✅ 大力用 |
| `enum class` | 强类型枚举，不会隐式转 int | ✅ 值得用 |
| `range-for` | `for(int x : arr)` 简化遍历 | ✅ 随便用 |
| `override` | 明确表示覆盖虚函数 | ✅ 值得用 |
| `static_assert` | 编译期断言 | ✅ 值得用 |
| `std::array` | 固定数组，替代 C 数组 | ✅ 推荐用 |
| `std::vector` | 动态数组 | ⚠️ 看内存情况 |
| 异常（try/catch） | 运行时异常处理 | ❌ 一般关掉 |
| RTTI（typeid） | 运行时类型识别 | ❌ 一般关掉 |

嵌入式编译加 `-fno-exceptions -fno-rtti` 关掉异常和 RTTI，节省代码体积。

---

## 关键代码模式

### 模式 1：硬件外设封装

```cpp
class AdcReader {
    uint8_t channel;
public:
    explicit AdcReader(uint8_t ch) : channel(ch) {
        adc_init(channel);
    }
    uint16_t read() { return adc_read(channel); }
    float readVoltage(float ref = 3.3) {
        return read() * ref / 4095.0;
    }
};
```

### 模式 2：模板化控制算法

```cpp
template<typename T>
class LowPassFilter {
    T alpha;
    T previous;
    bool first;
public:
    explicit LowPassFilter(T a) : alpha(a), previous(0), first(true) {}
    T filter(T input) {
        if(first) { first = false; previous = input; }
        previous = alpha * input + (1 - alpha) * previous;
        return previous;
    }
};
```

### 模式 3：设备继承体系

```cpp
class Actuator {
public:
    virtual void setOutput(float value) = 0;
    virtual void calibrate() {}
    virtual ~Actuator() = default;
};

class ServoMotor : public Actuator {
    uint8_t pin;
public:
    explicit ServoMotor(uint8_t p) : pin(p) { attach(pin); }
    void setOutput(float angle) override {
        pwm_set(pin, angle / 180.0 * 2500 + 500);
    }
};

class StepperMotor : public Actuator {
public:
    void setOutput(float steps) override { /* 步进逻辑 */ }
};
```

### 模式 4：RAII 管理硬件

```cpp
class LedIndicator {
    int pin;
public:
    LedIndicator(int p) : pin(p) {
        pinMode(pin, OUTPUT); digitalWrite(pin, LOW);
    }
    ~LedIndicator() { digitalWrite(pin, LOW); }
    void on() { digitalWrite(pin, HIGH); }
    void off() { digitalWrite(pin, LOW); }
};
```

### 模式 5：编译期配置

```cpp
namespace Config {
    constexpr float CONTROL_FREQ = 100.0;
    constexpr float DT = 1.0 / CONTROL_FREQ;
    constexpr uint32_t BAUD_RATE = 115200;
    constexpr uint8_t NUM_SENSORS = 4;
    constexpr float PID_LIMIT = 100.0;

    constexpr uint8_t pinForSensor(uint8_t idx) {
        return idx + A0;
    }

    static_assert(NUM_SENSORS <= 8, "Too many sensors");
}
```

---

## 逐节详解

### Section 1: C++ 关键差异点

你已经会 C 了，所以这里只说"C 没有的"。

#### 1.1 引用（再一次强调）

引用就是给变量取了个"外号"。`int a = 5; int& b = a; b = 10;` 之后 a 也变成 10。函数参数用 `const T&` 避免拷贝又不担心空指针。

#### 1.2 函数重载

```cpp
void write(uint8_t data);
void write(const uint8_t* buf, size_t len);
```

编译器根据参数选。C 里你要叫 `write_byte` 和 `write_buf`，C++ 都叫 `write`。

#### 1.3 默认参数 & 命名空间

```cpp
void setPwm(int freq, int duty = 50);
setPwm(1000);      // 等价于 setPwm(1000, 50)

namespace motor { void init(); }
namespace sensor { void init(); }
// 用 motor::init() 和 sensor::init() 区分
```

#### 1.4 const 的增强

C++ 的 const 成员函数承诺不修改对象状态：
```cpp
class Sensor {
    int raw;
public:
    int getRaw() const { return raw; }  // 承诺不改对象
};
```

### Section 2: 类 —— 嵌入式最常用的 C++ 特性

class 和 struct 的唯一区别：class 默认 private，struct 默认 public。

#### 构造函数初始化列表

这是 C++ 的关键语法：
```cpp
class PwmOut {
    const int pin;
    int frequency;
public:
    PwmOut(int p, int f) : pin(p), frequency(f) {
        pinMode(pin, OUTPUT);
    }
};
```

初始化列表在对象构造的**初始化阶段**就完成了赋值。如果写成 `pin = p`，那 pin 先被默认初始化（const 变量不允许），再赋值——编译器报错。

#### this 指针

每个成员函数内部有个隐含的 `this`，指向调用它的对象。变量重名时用：
```cpp
void setSpeed(int speed) {
    this->speed = speed;  // this->speed 是成员，speed 是参数
}
```

### Section 3: 构造与析构详解

一个 C++ 对象的生命周期：
```
分配内存 → 构造函数 → 使用 → 析构函数 → 释放内存
```

#### 拷贝构造函数

```cpp
Motor m1(100);
Motor m2 = m1;  // 拷贝构造
```

默认拷贝是"逐成员拷贝"（浅拷贝）。如果类有指针成员指向动态内存，浅拷贝会导致两个对象共享同一块内存——析构时 double free。

嵌入式推荐：一律禁止拷贝值类型：
```cpp
Motor(const Motor&) = delete;
Motor& operator=(const Motor&) = delete;
```

#### 移动语义（C++11）

解决"临时对象的昂贵拷贝"：
```cpp
class Buffer {
    uint8_t* data;
public:
    Buffer(Buffer&& other) noexcept : data(other.data) {
        other.data = nullptr;  // "偷"走资源
    }
};
```

### Section 4: 继承与多态

#### 纯虚函数和抽象类（接口）

```cpp
class TemperatureSensor {
public:
    virtual float readCelsius() = 0;         // 纯虚函数
    virtual float readFahrenheit() {
        return readCelsius() * 1.8 + 32;     // 带默认实现
    }
    virtual ~TemperatureSensor() = default;
};
```

`= 0` 表示"我没实现，派生类必须自己实现"。含纯虚函数的类不能实例化——它就是接口声明。

#### virtual 析构函数

基类必须有虚析构函数。否则通过基类指针 delete 派生类对象时，只有基类析构被调用，派生类资源不会释放。

### Section 5: 操作符重载

让自定义类型表现得像原生类型：
```cpp
struct Vector2 {
    float x, y;
    Vector2 operator+(const Vector2& rhs) const {
        return {x + rhs.x, y + rhs.y};
    }
};
```

嵌入式场景不多，但控制系统的向量运算（角度/位置/速度）用起来很顺手。

### Section 6: 模板 —— 编译期代码生成

工作原理：
1. 你写一个模板定义
2. 编译器看到具体类型实例化时，生成该类型的代码
3. 生成的代码和你手写完全一样 = 零开销抽象

#### 模板特化

```cpp
template<typename T>
T clamp(T val, T min, T max) {
    return (val < min) ? min : (val > max) ? max : val;
}

// 特化 float 版本
template<>
float clamp(float val, float min, float max) {
    // 更精确的 float 实现
}
```

### Section 7: STL 容器的嵌入式策略

STL 容器的问题：隐式使用堆内存。

| 容器 | 内存分配 | 嵌入式推荐 |
|------|---------|-----------|
| `std::array` | 栈/静态 | ✅ 随便用 |
| `std::vector` | 堆 | ⚠️ 视情况 |
| `std::map` | 堆（树结构） | ❌ 少用 |

推荐优先用 `std::array<T, N>` 替代 C 数组，带边界检查、自带大小、支持 STL 算法。

### Section 8: 嵌入式 C++ 实战架构

```
应用层：ControlLoop, StateMachine
    ↓
设备层：Motor, Sensor, Display（纯虚基类）
    ↓
驱动层：GpioPin, SpiBus, TimerChannel（RAII 封装）
    ↓
硬件层：寄存器 / HAL
```

#### 模板化运动控制

```cpp
template<typename T, typename Config>
class MotionController {
    Pid<T> pid;
    LowPassFilter<T> filter;
public:
    MotionController() : pid(Config::KP, Config::KI, Config::KD),
                         filter(Config::FILTER_ALPHA) {}
    T update(T setpoint, T feedback) {
        T filtered = filter.filter(feedback);
        return pid.compute(setpoint, filtered);
    }
};
```

---

## 与其他语言的对比

### C++ vs C（嵌入式场景）

| 维度 | C | C++ |
|------|---|-----|
| 封装 | 结构体+函数 | 类（public/private 强制） |
| 多态 | 函数指针表（手动） | 虚函数（编译器维护） |
| 算法复用 | 宏/拷贝 | 模板 |
| 资源管理 | 手动 malloc/free | RAII（自动） |
| 代码体积 | 最小 | 稍大（vtable） |
| 执行效率 | 相同 | 相同（零开销原则） |

**结论**：C++ 不是"更好的 C"，而是"用 C 的思维写嵌入式 C++"——栈上分配、关异常、关 RTTI、谨慎用堆、有选择地用模板和虚函数。得到的代码比 C 更安全、更可维护，零或极少的性能损失。

### C++ vs Python（从你的 Python 经验看）

- Python 变量都是引用，C++ 需要显式写 `&`
- Python GC 自动管理内存，C++ RAII 自动管理（但你要写代码）
- Python 鸭子类型靠运行时，C++ 靠模板（编译期）和虚函数（运行时）

---

## 面试高频考点（嵌入式方向）

| 考点 | 他在问什么 | 回答要点 | 常见错误 |
|------|-----------|----------|---------|
| 虚函数机制 | 知不知道 vtable | 每类一张 vtable，对象里有 vptr 指向它 | 说虚函数和普通函数一样快（实际差一次间接寻址） |
| 为什么要虚析构 | 知不知道多态删除 | 基类指针 delete 派生类对象时，非虚析构只调基类版本 | 说"析构函数本来就该虚"（只有多态场景需要） |
| RAII 是什么 | 知不知道资源的 C++ 方式 | 构造获取、析构释放，利用栈对象确定性析构 | 说成"智能指针"（智能指针只是 RAII 的一种应用） |
| 模板 vs 宏 | 知不知道编译期 vs 预处理 | 模板有类型检查，宏是文本替换 | 说"模板比宏快"（运行时一样，但模板更安全） |
| 嵌入式不用异常 | 知不知道异常开销 | 需要 RTTI、栈展开表、代码体积增大 10-30% | 说"嵌入式编译器不支持"（其实可以关掉） |

---

## 两周学习路线

### 第 1 周：核心基础

- **Day 1**：引用、函数重载、命名空间、const 增强 —— 从 C 到 C++ 的"语言升级包"
- **Day 2**：类和对象 —— struct 的进化版，封装硬件外设
- **Day 3**：构造函数详解 —— 初始化列表、拷贝控制、移动语义
- **Day 4**：运算符重载 —— 控制向量计算、状态更新
- **Day 5**：继承 + 多态 —— 标准统一的设备抽象接口

### 第 2 周：嵌入式实战

- **Day 6**：模板 —— PID、低通滤波器、通用控制算法
- **Day 7**：RAII —— 管理 SPI 总线、GPIO、DMA 缓冲区
- **Day 8**：STL + 智能指针 —— array、vector 的嵌入式用法
- **Day 9**：Modern C++ 实用特性 —— constexpr、auto、enum class、static_assert
- **Day 10**：综合实战 —— 编写完整的嵌入式控制框架
