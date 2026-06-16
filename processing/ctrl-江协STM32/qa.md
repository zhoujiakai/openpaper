# Q&A

## Q1：ST 是半导体厂商吗，生产芯片吗

> 日期：20260616周二

ST（意法半导体，STMicroelectronics）是全球前十大半导体厂商之一，总部在瑞士日内瓦。

- **IDM 模式**：设计 + 制造 + 封测一体化，有自己的晶圆厂（法国 Crolles、意大利 Agrate 等约 14 座），不是只画图纸的 Fabless
- **主要产品线**：通用 MCU（STM32 全线）、车载 MCU（SPC5）、MPU（STM32MP1）、MEMS 传感器（全球第一）、功率器件（MOSFET/IGBT/SiC）、模拟电源 IC、射频 NFC（ST25）
- **与 ARM 的关系**：ST 购买 ARM Cortex-M 内核的 IP 授权，在此基础上集成自研外设（GPIO、TIM、ADC、I2C 等）、Flash、SRAM，在自家工厂流片，做成完整的 STM32 芯片

## Q2：Keil5 MDK 和 Keil5 C51 有什么区别

> 日期：20260616周二

两者是同一套 µVision IDE 下的两个不同工具链，UI 完全相同，区别在目标架构和工程配置。

C51 完全不支持 ARM 内核，无法编译 STM32 代码。

## Q3：代码里面的 GPIOC 是什么

> 日期：20260616周二

GPIOC 是 STM32 标准外设库中代表 **C 组 GPIO 端口** 的结构体指针（宏），指芯片上 **PC0 ~ PC15** 这 16 个物理引脚。

**硬件层面**

STM32F103 把引脚每 16 个分一组，用字母命名：
- GPIOA → PA0 ~ PA15
- GPIOB → PB0 ~ PB15
- **GPIOC → PC0 ~ PC15**

常见核心板（如 Blue Pill）上 LED 接在 **PC13**，所以 `GPIOC` + `GPIO_Pin_13` 控制的就是板上 LED。

**软件层面（本质）**

GPIOC 是宏定义的指针，指向 GPIOC 的寄存器基地址：

```c
#define PERIPH_BASE       ((uint32_t)0x40000000)
#define APB2PERIPH_BASE   (PERIPH_BASE + 0x10000)
#define GPIOC_BASE        (APB2PERIPH_BASE + 0x1000)
#define GPIOC             ((GPIO_TypeDef *) GPIOC_BASE)
```

单片机通过读写特定内存地址控制硬件，库函数把这串地址包装成可读的 `GPIOC` 名字。

**代码解读**

```c
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);  // 给 GPIOC 通电（开时钟）
GPIO_Init(GPIOC, &GPIO_InitStructure);                  // 用配置参数初始化 GPIOC
GPIO_SetBits(GPIOC, GPIO_Pin_13);                       // PC13 输出高电平
GPIO_ResetBits(GPIOC, GPIO_Pin_13);                     // PC13 输出低电平
```

GPIOC 作为第一个参数传入库函数，指定操作的目标端口。操作哪个引脚由第二个参数指定。

## Q4：STM32F10x 标准外设库（V3.5.0）结构分析

> 日期：20260616周二
> 路径：`STM32F10x_StdPeriph_Lib_V3.5.0/`

**顶层结构**

```
STM32F10x_StdPeriph_Lib_V3.5.0/
├── Libraries/          ← 核心库代码（CMSIS + 外设驱动）
├── Project/            ← 模板工程 + 外设示例
├── Utilities/          ← EVAL 官方评估板支持
├── Release_Notes.html
└── stm32f10x_stdperiph_lib_um.chm   ← 用户手册
```

版本 V3.5.0，发布日期 2011-04-08。

**Libraries — 核心库代码**

```
Libraries/
├── CMSIS/                           ← ARM 提供的内核标准接口
│   └── CM3/
│       ├── CoreSupport/             ← 与芯片无关的 Cortex-M3 内核支持
│       │   ├── core_cm3.c
│       │   └── core_cm3.h           ← NVIC、SysTick、MPU、SCB 寄存器定义
│       └── DeviceSupport/ST/STM32F10x/
│           ├── startup/             ← 启动文件（按工具链 + 器件密度分）
│           │   ├── arm/             ← MDK-ARM（我们用的）
│           │   ├── gcc_ride7/
│           │   ├── iar/
│           │   └── TrueSTUDIO/
│           ├── stm32f10x.h          ← ★ 最核心头文件（619KB）寄存器映射+位定义
│           ├── system_stm32f10x.c   ← 系统时钟初始化（SystemInit）
│           └── system_stm32f10x.h
│
└── STM32F10x_StdPeriph_Driver/      ← ST 提供的外设驱动
    ├── inc/                         ← 24 个头文件
    │   ├── misc.h                   ← NVIC、SysTick 高层封装
    │   ├── stm32f10x_rcc.h          ← 时钟控制
    │   ├── stm32f10x_gpio.h         ← GPIO
    │   ├── stm32f10x_usart.h        ← 串口
    │   ├── stm32f10x_tim.h          ← 定时器（最大，51KB）
    │   ├── stm32f10x_adc.h / dma.h / spi.h / i2c.h / exti.h / ...
    │   └── stm32f10x_wwdg.h
    └── src/                         ← 24 个对应 .c 实现文件
```

**关键文件的角色**

| 文件 | 项目中作用 |
|------|-----------|
| **stm32f10x.h** | 单一总头文件。根据 `STM32F10X_MD` 等宏选择芯片密度；定义所有外设寄存器地址和位定义；开启 `USE_STDPERIPH_DRIVER` 后引入外设驱动 API |
| **stm32f10x_conf.h** | 外设驱动选择器。通过注释/取消注释切换各 `stm32f10x_ppp.h` 的包含；配置断言 `assert_param()` |
| **system_stm32f10x.c** | 启动后调用 `SystemInit()`，配置 HSI/HSE/PLL、AHB/APB 预分频、Flash 等待周期 |
| **core_cm3.h** | CMSIS 内核层，提供 NVIC 中断管理、SysTick 内联函数，被 stm32f10x.h 间接包含 |

**启动文件（startup）**

8 个启动文件，按芯片密度分：`ld`（低密度 16-32KB）、`md`（中密度 64-128KB）、`hd`（高密度 256-512KB）、`xl`（XL 密度）、`cl`（互联型）及对应 Value Line 版本。

STM32F103C8T6（64KB Flash）用 **startup_stm32f10x_md.s**。

启动文件做的事：设置栈指针 → 初始化向量表 → 调用 `SystemInit()` → 跳转 `main()`。

**常用外设驱动模块速查**

| 模块 | 头文件 | 用途 |
|------|--------|------|
| RCC | stm32f10x_rcc.h | 复位和时钟控制 |
| GPIO | stm32f10x_gpio.h | 引脚输入输出配置 |
| EXTI | stm32f10x_exti.h | 外部中断 |
| USART | stm32f10x_usart.h | 串口通信 |
| TIM | stm32f10x_tim.h | 通用/高级/基本定时器（最大模块） |
| ADC | stm32f10x_adc.h | 1-3 个 12 位 ADC |
| DMA | stm32f10x_dma.h | 7/12 通道 DMA |
| I2C | stm32f10x_i2c.h | I2C 通信 |
| SPI | stm32f10x_spi.h | SPI / I2S |

**Project — 模板与示例**

- **Template**（`STM32F10x_StdPeriph_Template/`）：工程骨架，包含 main.c、stm32f10x_conf.h、stm32f10x_it.c，新建工程时复制
- **Examples**（`STM32F10x_StdPeriph_Examples/`）：每个外设配有若干独立示例（GPIO 3 个、USART 12 个、TIM 22 个等），可直接参考

**开机启动流程**

```
复位 → 启动文件（startup_stm32f10x_md.s）
      → SystemInit()（配置时钟，默认 HSI 8MHz）
      → 初始化 .data / .bss
      → main()
      → 用户代码（开外设时钟 → 初始化 → 工作）
```

## Q5：寄存器方式点灯的代码在做什么

> 日期：20260617周三

```c
#include "stm32f10x.h"                  // Device header
int main(void){
    RCC->APB2ENR = 0x00000010;
    GPIOC->CRH = 0x00300000;
    GPIOC->ODR = 0x00000000;
    while(1){}
}
```

**RCC->APB2ENR = 0x00000010**：打开 GPIOC 的时钟。

- `APB2ENR`（APB2 外设时钟使能寄存器，地址 0x40021018）
- `0x00000010` = bit 4 置 1，查手册：bit 4 对应 **IOPCEN**（I/O Port C clock enable）
- 不开这行，后面操作 GPIOC 的寄存器全部无效

**GPIOC->CRH = 0x00300000**：把 PC13 配置为推挽输出。

- `CRH`（端口配置高寄存器，地址 0x40011004），管 PC8 ~ PC15
- `0x00300000` → bit[23:20] = `0011`
- MODE13 = `11`（输出模式，50MHz），CNF13 = `00`（通用推挽输出）

**GPIOC->ODR = 0x00000000**：把 PC0 ~ PC15 全部拉低（灯亮）。

- `ODR`（端口输出数据寄存器，地址 0x4001100C）
- 写 0 让 PC13 输出低电平 → LED 亮
- 若写成 `0x00002000`（bit 13 = 1），PC13 输出 3.3V → LED 灭

**三个寄存器全貌**

| 代码 | 寄存器 | 地址 | 干了什么 |
|------|--------|------|----------|
| `RCC->APB2ENR = 0x00000010` | APB2ENR | 0x40021018 | 给 GPIOC 通电 |
| `GPIOC->CRH = 0x00300000` | CRH | 0x40011004 | PC13 设为推挽输出 |
| `GPIOC->ODR = 0x00000000` | ODR | 0x4001100C | PC13 输出低电平 |

标准外设库里 `RCC_APB2PeriphClockCmd` + `GPIO_Init` + `GPIO_ResetBits` 底层最终也是写同样的寄存器。
