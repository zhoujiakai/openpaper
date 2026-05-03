# Python 核心机制 — AI 笔记

> 来源：
> - Real Python: [How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)
> - DasRoot: [Python Decorators: A Complete Guide](https://dasroot.io/python-decorators/)
> - UCL Research Computing: [Iterators, Generators, Decorators](https://github.com/UCL-ARC/python-training/blob/main/intermediate/extra_materials/iterators_generators_decorators.ipynb)
> - Python 官方文档: [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
> - Python 官方文档: [contextlib](https://docs.python.org/3/library/contextlib.html)
> 生成时间：2026-05-03
> 学习目标：面试准备

---

## 锚点

Python 核心机制干的是同一件事：**把"什么时候执行"的决定权从解释器手里拿过来，交给你自己**。装饰器决定函数执行的前后要干啥，生成器决定函数执行到一半能不能暂停，上下文管理器决定进入和离开一段代码时自动干啥。它们共享一个底层设计：用协议（一组约好的方法名）让对象获得某种能力，不需要继承任何类。

一句话记住：**协议即能力，鸭子类型即接口**。

## 核心问题

为什么有些 Python 代码你一看就知道是高手写的？因为他们不把逻辑从头到尾堆在函数里，而是用这些机制把"干什么"和"怎么组织"拆开。装饰器管"前后"，生成器管"节奏"，上下文管理器管"开关"。不懂这些，你只能写"能跑"的代码；懂了这些，你写的代码别人愿意读。

## 核心概念

### 闭包（Closure）

函数里面定义的函数，可以记住外面函数的变量，即使外面函数已经执行完了。

```python
def make_multiplier(n):
    def multiply(x):
        return x * n  # 记住了 n
    return multiply

double = make_multiplier(2)
double(5)  # 10，make_multiplier 已经返回了，但 n=2 还活着
```

闭包是装饰器能工作的前提。不懂闭包，装饰器的原理就是黑箱。

### 装饰器（Decorator）

一个函数，接收另一个函数，返回一个新函数。新函数在调用原函数的前后可以做额外的事。就这些。

```python
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时 {time.time() - start:.2f}s")
        return result
    return wrapper

@timer  # 等价于 do_something = timer(do_something)
def do_something():
    time.sleep(1)
```

少了装饰器，每个需要计时的函数都得自己写 start/end 计算逻辑，重复代码堆满项目。

### 迭代器（Iterator）

一个对象只要实现了 `__iter__` 和 `__next__` 两个方法，Python 就认为它是迭代器。`__next__` 每次返回一个值，没值了抛 `StopIteration`。

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for i in Countdown(3):
    print(i)  # 3, 2, 1
```

迭代器是 for 循环的底层协议。你每天用的 `for x in list`，Python 实际上在调用 `iter(list)` 拿到迭代器，然后反复调 `__next__`。

### 生成器（Generator）

用 `yield` 关键字的函数，调用时不会执行函数体，而是返回一个生成器对象。生成器是迭代器的一种——它自动实现了 `__iter__` 和 `__next__`，你不用手写。

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for i in countdown(3):
    print(i)  # 3, 2, 1
```

生成器比手写迭代器简单得多，而且有更大的本事：`send()` 可以从外面往里传值，`throw()` 可以从外面往里抛异常。这使得生成器可以做协程（coroutine 的早期形态）。

### 上下文管理器（Context Manager）

一个对象实现了 `__enter__` 和 `__exit__`，就可以用 `with` 语句。`with` 保证不管中间有没有异常，`__exit__` 一定会执行。

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()  # 不管有没有异常，都会关

with DatabaseConnection() as conn:
    conn.execute("SELECT ...")
# 出了 with 块，连接自动关了
```

少了上下文管理器，你就要在每个可能出错的地方写 `try/finally` 来保证资源释放。文件操作、数据库连接、锁的获取释放，全靠它。

### 推导式（Comprehension）

一行代码从旧集合生成新集合。三种：列表推导式 `[x for x in ...]`，字典推导式 `{k: v for ...}`，集合推导式 `{x for ...}`。把 `[]` 换成 `()` 就是生成器表达式——不立即生成列表，而是按需产出。

```python
squares = [x**2 for x in range(10)]          # 列表推导式
even_squares = {x: x**2 for x in range(5) if x % 2 == 0}  # 字典推导式
total = sum(x**2 for x in range(1000000))     # 生成器表达式，不会撑爆内存
```

推导式和生成器表达式的区别只有一个：`[]` 立即生成所有结果放内存，`()` 按需产出、用完即弃。

## 关键代码模式

### 模式 1：带参数的装饰器

装饰器本身需要参数时（比如指定重试次数），外面再包一层函数。

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    print(f"第 {attempt+1} 次失败，重试...")
        return wrapper
    return decorator

@retry(times=5)  # retry(5) 返回装饰器，再装饰 fetch_data
def fetch_data(url):
    ...
```

解析调用链：`retry(5)` → 返回 `decorator` → `decorator(fetch_data)` → 返回 `wrapper`。三层函数嵌套是带参数装饰器的标志。

### 模式 2：functools.wraps

装饰器必须加 `@functools.wraps(func)`，否则被装饰函数的 `__name__`、`__doc__` 等元信息会变成 `wrapper` 的。

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def important():
    """很重要的函数"""
    pass

important.__name__  # 'wrapper'，丢了原始名字
important.__doc__   # None，丢了文档字符串
```

加了 `@functools.wraps(func)` 后，`__name__` 和 `__doc__` 保持为 `'important'` 和 `'很重要的函数'`。

### 模式 3：生成器管道

多个生成器串联，像流水线一样处理数据，每一步只处理当前元素，不在内存里存全部数据。

```python
def read_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith('#'):
            yield line

def parse_numbers(lines):
    for line in lines:
        yield [int(x) for x in line.split()]

# 三个生成器串起来，读大文件也不撑内存
pipeline = parse_numbers(filter_comments(read_lines('data.txt')))
for numbers in pipeline:
    process(numbers)
```

每个生成器只做一件事，串起来就是完整的数据处理流程。处理 10GB 的日志文件，内存占用可能只有几 KB。

### 模式 4：@contextmanager 装饰器

用生成器来写上下文管理器，不用手写类。`yield` 之前是 `__enter__` 的逻辑，`yield` 的值赋给 `as` 变量，`yield` 之后是 `__exit__` 的逻辑。

```python
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    yield  # yield 前面是进入 with 时做的事
    print(f"{name} 耗时 {time.time() - start:.2f}s")

with timer("数据处理"):
    process_data()
# 自动打印耗时
```

这个模式把装饰器和生成器连在了一起。`@contextmanager` 本身是个装饰器，它把你写的生成器函数变成上下文管理器。

### 模式 5：类作为装饰器

类实现 `__call__` 方法就可以当装饰器用。好处是可以在 `__init__` 里保存状态。

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 第 {self.count} 次调用")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("hello")

say_hello()  # say_hello 第 1 次调用
say_hello()  # say_hello 第 2 次调用
```

## 逐节详解

### Section 1: 闭包 — 装饰器的地基

碰到一个问题：我想在函数内部定义一个辅助函数，但这个辅助函数需要用到外部函数的局部变量。普通的局部变量在外部函数返回后就没了，怎么办？

Python 的做法是：内部函数会"记住"外部函数的变量。不是记住变量的值（拷贝），而是记住变量本身（引用）。所以外部函数返回后，这些变量依然活着——它们被内部函数"背着"。

```python
def make_greeter(greeting):
    def greet(name):
        print(f"{greeting}, {name}!")
    return greet

hello = make_greeter("Hello")
hi = make_greeter("Hi")

hello("Alice")  # Hello, Alice!
hi("Bob")       # Hi, Bob!
```

`hello` 和 `hi` 是两个不同的闭包。它们各自背着自己的 `greeting` 值，互不干扰。

判断闭包的三个条件：
1. 有嵌套函数（函数里定义函数）
2. 内部函数引用了外部函数的变量
3. 外部函数返回了内部函数

面试常问：闭包和类的区别？闭包背的是数据，类背的是数据+方法。闭包适合"一个函数+一些状态"的场景，类适合"多个方法+共享状态"的场景。

### Section 2: 装饰器 — 函数的外套

先说问题：你有 10 个函数，每个都要加计时、加日志、加权限检查。你当然可以在每个函数开头结尾写这些代码。但这意味着同样的逻辑写 10 遍，改一个地方要改 10 处。

装饰器的思路：把"计时/日志/权限"这些跟核心逻辑无关的代码抽出来，包成一个函数。然后告诉 Python：以后调用这个函数时，先走我的包装逻辑。

```python
def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"调用 {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} 返回 {result}")
        return result
    return wrapper
```

`@log_call` 放在任何函数定义上面，这个函数就被包了一层日志。核心逻辑一行不碰。

**装饰器的执行时机**：装饰器在函数定义时就执行了，不是在调用时。也就是说，模块加载时 `@timer` 就把 `do_something` 替换成了 `wrapper`。之后所有对 `do_something` 的调用，实际调用的是 `wrapper`。

**装饰器堆叠**：多个装饰器从下往上执行（靠近函数定义的最后执行，最先包装）。

```python
@decorator_a   # 第二层包装
@decorator_b   # 第一层包装
def func():
    pass
# 等价于 func = decorator_a(decorator_b(func))
```

调用 `func()` 时，请求先走 `decorator_a` 的 wrapper，再走 `decorator_b` 的 wrapper，最后走原函数。就像穿衣服：最后穿的外套最先被看到。

### Section 3: 迭代器 — for 循环的底层协议

你在 Python 里天天写 `for x in something`。Python 解释器收到这行代码时，它做的不是直接遍历 `something`。它先调用 `iter(something)` 拿到一个迭代器，然后反复调用迭代器的 `__next__()`，直到抛出 `StopIteration`。

```python
# for x in [1, 2, 3] 实际做的事：
it = iter([1, 2, 3])   # 调用列表的 __iter__，拿到迭代器
x = next(it)            # 1，调用 __next__
x = next(it)            # 2
x = next(it)            # 3
x = next(it)            # StopIteration，for 循环捕获并停止
```

为什么 Python 要搞这么一层间接？因为解耦。任何对象只要实现了 `__iter__` + `__next__`，就能被 for 循环使用。列表、字典、集合、文件对象、数据库游标，它们内部结构完全不同，但 for 循环不需要知道——它只认迭代器协议。

可迭代对象（Iterable）和迭代器（Iterator）的区别：
- **可迭代对象**：实现了 `__iter__` 方法，返回一个迭代器。列表、字典、字符串都是。
- **迭代器**：同时实现了 `__iter__` 和 `__next__`。`__iter__` 返回自身。

关键区别：可迭代对象可以被多次迭代（每次 `iter()` 返回新的迭代器），迭代器只能用一次（耗尽后 `__next__` 永远抛 `StopIteration`）。

```python
nums = [1, 2, 3]       # 可迭代对象
it1 = iter(nums)        # 第一个迭代器
it2 = iter(nums)        # 第二个迭代器，跟 it1 独立

next(it1)               # 1
next(it1)               # 2
next(it2)               # 1（独立的，从头开始）
```

### Section 4: 生成器 — 按需生产的迭代器

手写迭代器很烦：你要写类、写 `__init__` 维护状态、写 `__iter__`、写 `__next__` 处理边界。生成器用 `yield` 一个关键字把这些全替你做了。

```python
# 手写迭代器
class SquareIterator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        result = self.current ** 2
        self.current += 1
        return result

# 生成器，做同样的事
def squares(limit):
    for i in range(limit):
        yield i ** 2
```

生成器函数被调用时不执行函数体，而是立即返回一个生成器对象。生成器对象是迭代器，每次 `next()` 调用执行到下一个 `yield`，把 `yield` 后面的值交出去，然后暂停。下次 `next()` 从暂停的地方继续。

**生成器 vs 列表的内存差异**：

```python
# 方式1：列表，一次性生成 100 万个数放内存
nums = [x ** 2 for x in range(1000000)]

# 方式2：生成器，每次只算一个，内存占用恒定
nums = (x ** 2 for x in range(1000000))
```

列表占几十 MB 内存。生成器占几十字节——它只保存当前状态，不知道、也不关心下一个值是什么，直到你要的时候才算。

**生成器的高级用法：send()**

`send()` 可以从外部往生成器内部传值。`yield` 表达式本身有返回值，这个值就是 `send()` 传进来的。

```python
def accumulator():
    total = 0
    while True:
        value = yield total   # yield 把 total 交出去，同时接收 send 传进来的 value
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)          # 启动生成器，返回 0（必须先 next 一次"启动"）
gen.send(10)       # 返回 10
gen.send(20)       # 返回 30
gen.send(5)        # 返回 35
```

`send()` 是 Python 协程的早期形态。现在有了 `async/await`，直接用生成器做协程的场景少了，但面试中 `send()` 仍然是区分"用过"和"理解原理"的分水岭。

### Section 5: 上下文管理器 — 自动收拾的协议

数据库连接、文件句柄、网络锁——这些资源用完必须释放。手动写 `try/finally` 可以，但每个地方都写一遍，迟早漏掉。

上下文管理器把"获取"和"释放"绑定在一起，保证不管发生什么，`__exit__` 一定会被调用。

两种写法：

**写法 1：类，实现 `__enter__` 和 `__exit__`**

```python
class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.f = open(self.filename)
        return self.f      # as 变量拿到的是 __enter__ 的返回值

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
        return False        # False 表示异常继续传播，True 表示吞掉异常

with ManagedFile('data.txt') as f:
    data = f.read()
# f 自动关闭
```

**写法 2：`@contextmanager` + 生成器**

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename):
    f = open(filename)     # __enter__ 的逻辑
    try:
        yield f            # yield 的值赋给 as 变量
    finally:
        f.close()          # __exit__ 的逻辑

with managed_file('data.txt') as f:
    data = f.read()
```

`try/finally` 保证即使 with 块里抛了异常，文件也会关闭。

两种写法怎么选？简单场景（开/关、获取/释放）用 `@contextmanager`，代码少。需要复杂初始化或多个方法共享状态时用类。

### Section 6: 推导式与生成器表达式

推导式是 Python 最具辨识度的语法之一。它的本质：把循环 + 条件判断 + 构造新集合压缩成一行。

**列表推导式**：

```python
# 普通写法
results = []
for x in range(20):
    if x % 2 == 0:
        results.append(x ** 2)

# 推导式
results = [x ** 2 for x in range(20) if x % 2 == 0]
```

**字典推导式**：

```python
words = ['hello', 'world', 'python']
word_lengths = {w: len(w) for w in words}
# {'hello': 5, 'world': 5, 'python': 6}
```

**集合推导式**：

```python
unique_lengths = {len(w) for w in words}
# {5, 6}
```

**生成器表达式**：把 `[]` 换成 `()`。不立即构造列表，而是返回生成器。

```python
# 这两个效果一样
sum(x ** 2 for x in range(1000000))
sum((x ** 2 for x in range(1000000)))

# 但列表推导式会撑内存
sum([x ** 2 for x in range(1000000)])  # 先生成 100 万个元素的列表
```

原则：**只要外层函数接受可迭代对象（如 `sum()`、`max()`、`any()`），就用生成器表达式**。只有你需要反复遍历结果、或者需要用列表方法（`append`、`sort`）时，才用列表推导式。

推导式的可读性边界：超过两个 `for` 或超过一个 `if` 时，换回普通循环。没人愿意读一行 200 字符的推导式。

## 与其他语言的对比

Python 的装饰器和 Java 的注解（Annotation）经常被拿来对比，但它们完全不是一回事。

Java 注解是元数据标记，本身不执行任何逻辑。你要配合注解处理器（Annotation Processor）或 AOP 框架（如 Spring）才能让注解"干活"。运行时注解通过反射读取。

Python 装饰器是一个实实在在的函数，在模块加载时就执行，把原函数替换成新函数。不需要框架，不需要反射，不需要配置文件。

```python
# Python：装饰器就是高阶函数，直接执行
@timer
def work():
    pass
# 等价于 work = timer(work)，立即执行

// Java：注解只是标签，需要框架解读
@Timed
public void work() {}
// 注解本身什么也不做，需要 Dropwizard/Micrometer 框架扫描并代理
```

Python 生成器在其他语言里的对应物：

| 语言 | 机制 | 区别 |
|------|------|------|
| Python | 生成器（yield） | 语言级支持，自动实现迭代器协议 |
| JavaScript | Generator 函数（function*） | 语法类似，也有 yield/next |
| C# | yield return | 几乎一样的语法 |
| Java | Stream / Iterator | 没有语言级 yield，Stream 是库级实现 |
| Go | 无对应物 | 用 channel 模拟，但语义不同 |

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| 装饰器原理 | 你是否理解高阶函数和闭包 | 装饰器接收函数返回函数，利用闭包保存原函数引用。`@decorator` 是语法糖，定义时执行替换 | 以为装饰器在调用时才执行；忘记 `functools.wraps` |
| 带参数装饰器 | 你能不能处理三层嵌套 | 外层函数接收装饰器参数，返回真正的装饰器。调用链：`retry(3)(func)` → wrapper | 搞混参数传给哪一层 |
| 生成器 vs 列表 | 你是否理解惰性求值和内存效率 | 生成器按需产出，内存恒定；列表一次性生成，占满内存。生成器只能遍历一次 | 以为生成器可以反复遍历；不知道生成器表达式 |
| yield 的执行流程 | 你是否理解协程的雏形 | yield 暂停函数、交出值；next() 恢复执行到下一个 yield；send() 往里传值 | 不知道 send()；不知道生成器必须先 next() 启动 |
| 迭代器 vs 可迭代对象 | 你是否理解 for 循环的底层 | 可迭代对象有 `__iter__` 返回迭代器；迭代器有 `__next__`；迭代器耗尽不可重用 | 混淆两个概念；以为迭代器可以重置 |
| 上下文管理器 | 你是否会正确管理资源 | `__enter__` 获取资源返回给 as，`__exit__` 保证释放。`@contextmanager` 用生成器简化 | 忘记 `__exit__` 的参数；不知道 `@contextmanager` |
| 推导式 vs 生成器表达式 | 你是否知道何时用哪个 | 需要多次遍历或列表方法用 `[]`；只遍历一次用 `()`。大数组必须用生成器表达式 | 所有地方都用列表推导式；写出过长的推导式 |
| 闭包 | 你是否理解作用域和变量捕获 | 内部函数引用外部变量，外部函数返回后变量不销毁。记住的是引用不是拷贝 | 以为闭包拷贝了值；跟类的作用混淆 |

### 面试加分题：用装饰器实现单例模式

```python
def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connected = True

db1 = Database()
db2 = Database()
db1 is db2  # True，始终返回同一个实例
```

### 面试加分题：yield from

`yield from` 让生成器可以把迭代工作委托给另一个生成器，避免手写内层循环。

```python
def flatten(nested):
    for sublist in nested:
        yield from sublist  # 等价于 for item in sublist: yield item

list(flatten([[1, 2], [3, 4], [5]]))  # [1, 2, 3, 4, 5]
```

`yield from` 在 Python 3.3 引入。它不仅简化了代码，还建立了子生成器和调用者之间的双向通道——`send()` 和 `throw()` 会透明地传递给子生成器。
