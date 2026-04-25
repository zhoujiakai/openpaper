# Python 异步 — AI 笔记

> 来源：
> - [Real Python: Async IO in Python](https://realpython.com/async-io-python/)
> - [Python 官方文档 asyncio](https://docs.python.org/3/library/asyncio.html)
> 生成时间：2026-04-25
> 学习目标：面试准备，理解事件循环底层机制

---

## 锚点

异步就是一个服务员同时管 24 桌客人。服务员只有一个人（单线程），但客人点完菜要等厨房做（I/O 等待），这时候服务员不用傻站着，去下一桌点单就行。等哪桌菜做好了，再回去上菜。整场下来，24 桌客人几乎同时被服务完——不是服务员变快了，是他把等待时间利用起来了。

这就是 asyncio 的全部核心：**一个线程，靠把 I/O 等待时间让给别人用，实现了"看起来同时"的效果。**

## 核心问题

为什么你的 Python 程序跑 100 个网络请求要等 100 秒？不是因为 CPU 慢，是因为程序在等网络响应的时候啥也没干。asyncio 解决的就是这个问题：**在等 I/O 的时候，干点别的。**

## 核心概念

### 协程（Coroutine）

协程就是一个能"暂停"的函数。普通函数从头跑到尾，中间停不下来。协程跑着跑着可以喊"暂停，我要等一个结果"，把控制权交出去，等结果回来了再继续。

定义方式：在 `def` 前面加 `async`。

```python
async def fetch_data(url):
    print("开始请求")
    response = await aiohttp.get(url)  # 暂停，等网络响应
    print("拿到结果")                    # 响应到了，从这里继续
    return response
```

直接调用 `fetch_data()` 不会执行它——你只会得到一个协程对象。就像菜单上写了道菜，但还没交给厨房。要想真正执行，需要用 `await` 或 `asyncio.run()`。

**为什么重要：** 没有协程，就没有"暂停和恢复"的能力，asyncio 的一切都建立在协程的暂停-恢复机制上。

### 事件循环（Event Loop）

事件循环就是那个在 24 桌之间来回跑的服务员。它是一个无限循环，不停做三件事：

1. 看看哪些 I/O 操作准备好了（用操作系统的 `epoll`/`kqueue` 机制）
2. 把准备好的协程叫醒继续执行
3. 处理定时任务

```python
# 伪代码，展示事件循环的核心逻辑
while running:
    ready = check_io_ready(timeout)     # 1. 检查 I/O
    for callback in ready:
        callback()                       # 2. 执行回调/恢复协程
    run_scheduled_tasks()                # 3. 处理定时任务
```

启动方式：`asyncio.run(main_coroutine)`。这是现代 Python 唯一推荐的启动方式。

**底层实现：** 事件循环依赖操作系统的 I/O 多路复用。Linux 上用 `epoll`，macOS 上用 `kqueue`，Windows 上用 `IOCP`。Python 的 `selectors` 模块封装了这些差异，事件循环在它的基础上工作。两个主要实现：
- `SelectorEventLoop`：Unix 默认，基于 `selectors`
- `ProactorEventLoop`：Windows 默认，基于 `IOCP`

**为什么重要：** 事件循环是整个 asyncio 的发动机。没有它，协程只是一段定义好的代码，不会自己跑起来。

### await 到底做了什么

`await` 是协程暂停的地方，也是控制权交接的地方。当你写 `result = await f()` 时，发生了这些事：

1. 协程在这里暂停执行
2. 控制权还给事件循环
3. 事件循环去执行其他准备好的协程
4. 等 `f()` 的结果就绪，事件循环把协程叫醒
5. 协程从暂停的地方继续，`result` 拿到值

`await` 只能用在 `async def` 函数里。在外面用会报 `SyntaxError`。`await` 后面跟的必须是"可等待对象"（awaitable）：协程、Task、Future，或者实现了 `__await__()` 方法的对象。

**为什么重要：** `await` 不是"等一下"的意思。它的意思是"我把 CPU 让出来，等结果准备好了叫我"。理解这一点，就理解了 asyncio 的调度方式。

### Task 和 Future

协程本身不会自动运行。`Task` 是协程的包装器，把它丢进事件循环的调度队列里，让事件循环来驱动它。

```python
# 创建 Task——协程变成可调度的单元
task = asyncio.create_task(fetch_data("https://example.com"))
# task 立刻开始执行（在事件循环的下一次迭代中）
```

`Future` 是更底层的概念——它代表一个"将来才有结果"的占位符。`Task` 是 `Future` 的子类，专门用来包装协程。

简单记：**协程是菜谱，Task 是订单，Future 是叫号器。**

关键区别：
- `await coro()`：立刻执行，调用者等待结果
- `asyncio.create_task(coro())`：排进调度队列，调用者可以继续干别的

### async for 和 async with

`async for`：异步迭代器，每次迭代之间可以交出控制权。用在异步生成器上。

`async with`：异步上下文管理器，`__aenter__` 和 `__aexit__` 是协程。最常见的场景是网络连接和数据库会话。

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.text()
# 两个 async with 确保连接在退出时正确关闭，不阻塞事件循环
```

## 关键代码模式

### 并发执行多个协程

```python
# 方式 1：gather——等全部完成，按顺序返回结果
results = await asyncio.gather(
    fetch_data(url1),
    fetch_data(url2),
    fetch_data(url3),
)
# results = [result1, result2, result3]，顺序固定

# 方式 2：as_completed——谁先完成谁先返回
for coro in asyncio.as_completed([fetch_data(url1), fetch_data(url2)]):
    result = await coro  # 最先完成的先拿到

# 方式 3：TaskGroup（Python 3.11+）——更安全的 gather
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch_data(url1))
    task2 = tg.create_task(fetch_data(url2))
# 退出 with 块时自动等所有任务完成，任一任务异常会取消其他任务
```

### 生产者-消费者模式

```python
async def producer(queue):
    for item in items:
        data = await fetch_data(item)
        await queue.put(data)
    await queue.put(None)  # 毒丸，通知消费者结束

async def consumer(queue):
    while True:
        data = await queue.get()
        if data is None:
            break
        process(data)

queue = asyncio.Queue()
await asyncio.gather(producer(queue), consumer(queue))
```

## 逐节详解

### Section 1: 并发 vs 并行——asyncio 不是多线程

很多人以为 asyncio 是"多线程的另一个写法"。不是。

- **并行（Parallelism）**：多个 CPU 核心同时干活。 multiprocessing 做的事。
- **并发（Concurrency）**：一个核心在多个任务之间切换，看起来同时在做。asyncio 和 threading 做的事。

asyncio 是**单线程、单进程**的。它靠"协作式多任务"（cooperative multitasking）实现并发——每个协程自己决定什么时候让出控制权（通过 `await`）。这和线程的"抢占式多任务"（操作系统随时可以切换线程）完全不同。

**优缺点：**
- 优点：没有锁、没有竞态条件，因为同一时刻只有一个协程在执行
- 缺点：一个协程如果不 `await`，整个事件循环都会卡住（后面会讲）

### Section 2: 事件循环的内部运作

事件循环的核心数据结构：

- `_ready`：一个双端队列（deque），存着马上要执行的回调
- `_scheduled`：一个最小堆（heapq），存着将来要执行的定时回调，按时间排序

每一轮循环的步骤：
1. 计算下次定时任务还有多久到期
2. 用这个时间作为超时，调用 `selector.select(timeout)` 等待 I/O 就绪
3. 把就绪的 I/O 回调加到 `_ready` 队列
4. 把到期的定时回调从 `_scheduled` 移到 `_ready`
5. 依次执行 `_ready` 里的所有回调
6. 回到第 1 步

**Task 是怎么被驱动的：** `Task` 包装了协程，它的 `__step()` 方法调用 `coro.send(None)` 推进协程。当协程 `await` 一个 Future 时，Task 在那个 Future 上注册一个回调——Future 完成时，回调再次调用 `__step()`，协程从暂停点继续。

```python
# 简化版 Task.__step 逻辑
def __step(self, exc=None):
    try:
        result = self._coro.send(exc)  # 推进协程
    except StopIteration as e:
        self.set_result(e.value)  # 协程结束，设置结果
    else:
        # result 是一个 Future，等它完成后再 __step
        result.add_done_callback(self.__step)
```

### Section 3: gather vs TaskGroup vs create_task——什么时候用什么

| 场景 | 用什么 | 为什么 |
|------|--------|--------|
| 并发跑多个独立任务，等全部完成 | `asyncio.gather()` | 返回结果按顺序排列，简单直接 |
| 并发跑多个任务，任一出错要全部取消 | `asyncio.TaskGroup` | 内置异常传播和取消，3.11+ 推荐 |
| 后台跑一个长期任务，不等它 | `asyncio.create_task()` | 任务立刻开始，你去做别的事 |
| 需要按完成顺序处理结果 | `asyncio.as_completed()` | 谁先完成先处理谁 |

**gather 的坑：** 如果其中一个协程抛异常，gather 会立刻把异常往上抛，其他协程的结果会丢掉。加 `return_exceptions=True` 可以让异常变成返回值，不中断其他任务。

**TaskGroup 的优势：** 它是 `async with` 语法，退出时自动等所有任务完成。如果某个任务异常，会取消其他所有任务，然后把所有异常打包成 `ExceptionGroup` 抛出。比 gather 更安全。

**create_task 的注意事项：** 创建了 Task 但没有 await 它，当 `main()` 协程结束时，这些没等完的 Task 会被取消。必须确保所有你想完成的 Task 都被 await 了。

### Section 4: 阻塞——asyncio 最大的敌人

asyncio 是协作式调度。如果协程里调用了阻塞操作（`time.sleep()`、`requests.get()`、同步文件读写、CPU 密集计算），它不会让出控制权，整个事件循环都会卡住。其他所有协程都等着。

**常见阻塞操作和替代方案：**

| 阻塞操作 | 异步替代 |
|---------|---------|
| `time.sleep()` | `asyncio.sleep()` |
| `requests.get()` | `aiohttp` 或 `httpx`（异步版） |
| 同步数据库驱动 | `asyncpg`、`aiomysql`、`Motor`（MongoDB） |
| 同步文件读写 | `aiofiles` |
| CPU 密集计算 | `asyncio.to_thread()` 或 `ProcessPoolExecutor` |

**`asyncio.to_thread()`（Python 3.9+）：** 如果必须调同步阻塞函数，用它把阻塞函数丢到线程池里，事件循环不会被卡住。

```python
# 阻塞的同步函数
def blocking_io():
    return open('file.txt').read()

# 在异步代码里安全调用
result = await asyncio.to_thread(blocking_io)
```

**为什么数据库要用 AsyncSession：** SQLAlchemy 的同步 Session 执行查询时会阻塞事件循环。异步代码里用同步 Session，所有协程都等着这个查询完成，并发就废了。`AsyncSession` 把查询操作丢到线程池里异步执行，不阻塞事件循环。

### Section 5: asyncio vs 多线程 vs 多进程

| 维度 | asyncio | 多线程 | 多进程 |
|------|---------|--------|--------|
| 并发方式 | 协作式，协程主动让出 | 抢占式，OS 调度 | 真正的并行 |
| 线程/进程数 | 1 个线程 | 多个线程 | 多个进程 |
| 内存开销 | 极小（协程就是函数对象） | 中等（每线程约 8MB 栈） | 大（每进程独立内存） |
| 适合场景 | I/O 密集（网络、数据库） | I/O 密集 + 简单并发 | CPU 密集（计算、图像处理） |
| 并发量 | 轻松上万 | 几百到几千 | 几十（受 CPU 核心数限制） |
| 数据安全 | 无竞态（同一时刻只有一个协程在跑） | 需要锁 | 进程间隔离，天然安全 |
| 调试难度 | 中等 | 高（竞态条件难复现） | 低 |

**选择口诀：** 等网络用 asyncio，等计算用多进程，简单并发用多线程。三种可以组合使用。

### Section 6: 异常处理

```python
# gather 里收集异常
results = await asyncio.gather(
    task1(), task2(), task3(),
    return_exceptions=True
)
# results 里可能有异常对象

# TaskGroup + ExceptionGroup（3.11+）
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(risky_task1())
        tg.create_task(risky_task2())
except ExceptionGroup as eg:
    for exc in eg.exceptions:
        print(f"任务失败: {exc}")
```

**取消任务：**
```python
task = asyncio.create_task(long_running())
task.cancel()  # 请求取消
try:
    await task
except asyncio.CancelledError:
    print("任务已取消")
```

取消不是立刻生效的——它会在协程下一次 `await` 时抛出 `CancelledError`。协程可以捕获这个异常做清理工作。

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| asyncio 是多线程吗 | 你理解并发和并行的区别 | 不是，单线程协作式多任务，靠 await 让出控制权 | 混淆并发和并行 |
| 事件循环做了什么 | 你知道底层调度机制 | 无限循环：检查 I/O 就绪→执行回调→处理定时任务，底层用 epoll/kqueue | 以为是多线程调度 |
| await 的时候发生了什么 | 你理解协程的暂停-恢复 | 暂停当前协程，控制权给事件循环，结果就绪后恢复执行 | 以为是阻塞等待 |
| gather 和 TaskGroup 区别 | 你知道怎么选并发 API | gather 结果有序，TaskGroup 更安全（自动取消+异常分组），3.11+ 推荐 TaskGroup | 不知道 gather 的异常传播问题 |
| 为什么不能用同步数据库驱动 | 你理解阻塞的危害 | 同步驱动会阻塞事件循环，所有协程都等着，并发失效 | 以为加 async def 就够了 |
| 什么时候用多进程而不是 asyncio | 你会做技术选型 | CPU 密集用多进程，I/O 密集用 asyncio，可以组合 | 一刀切只用一种 |
| asyncio.sleep 和 time.sleep 的区别 | 你理解阻塞 vs 非阻塞 | asyncio.sleep 不阻塞事件循环，time.sleep 会卡住一切 | 以为效果一样 |

## 参考

- [Real Python: Async IO in Python](https://realpython.com/async-io-python/)
- [Python 官方文档 asyncio](https://docs.python.org/3/library/asyncio.html)
- PEP 3156 — asyncio 原始提案
- Miguel Grinberg PyCon 演讲（国际象棋类比来源）
