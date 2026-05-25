# Python 异步 — 个人笔记

> 基于精读和周测复习整理
> 记录时间：2026-04-30

---

## await 底层机制（反复薄弱，重点记忆）

执行 `await aiohttp.get(url)` 时的完整链路：

1. **协程暂停** — 执行到 await，协程停下来，控制权交给外层的 Task
2. **注册回调** — Task 在 Future 上注册回调（Future = 占位符，"结果到了叫我"）
3. **注册到 OS** — socket 设为 non-blocking，注册到 epoll（Linux）/ kqueue（macOS）
4. **事件循环去干别的** — 执行其他排队的协程
5. **OS 通知就绪** — 回调进 `_ready` 队列
6. **协程恢复** — 回调触发 `Task.__step()`，协程从 await 处继续

### 我容易忘的点

- **回调注册在 Future 上**，不是 _scheduled，不是 _ready。Future 是连接"等的人"和"到的人"的桥梁。
- `Task.__step()` 就是"从书签那页继续读"——内部调用 `coro.send(value)`，把协程往下推一步。
- 核心思想：等 I/O 的时间不浪费，交给别人用。epoll/kqueue 是 OS 提供的"帮你盯着"的能力。

### 口诀

暂停 → Future 注册回调 → epoll 盯着 → 就绪 → _ready → 恢复

---

## 协程 vs 普通函数（反复薄弱，重点记忆）

- `def` 函数：调用就执行，直接拿到返回值
- `async def` 函数：调用**不执行**，返回一个 **coroutine 对象**
- Task 不是调用 async 函数产生的，是 `asyncio.create_task()` 包出来的

```python
def foo():       return 42    # foo() → 42
async def bar(): return 42    # bar() → <coroutine object>，还没执行
                               # await bar() → 42，这才执行
                               # create_task(bar()) → Task 对象
```

### 口诀

协程是"要做的事"，Task 是"事件循环给你排上了"。调 async 函数只是拿到一张任务单，await 或 create_task 才是真正开工。

---

## 并发 vs 并行

- 并发：任务交替执行，看起来同时（asyncio 单线程）
- 并行：真正同时执行，需要多核（多进程）

## 事件循环

- 两个核心数据结构：`_ready`（马上执行）、`_scheduled`（定时执行）
- 每轮循环：处理 _ready 里的回调 → 检查 _scheduled 到期的移到 _ready → epoll/kqueue 检查 I/O

## 三种并发 API（周测模糊点）

- `gather + return_exceptions=True`：独立任务，**允许部分失败**——某个挂了不影响其他
- `TaskGroup`：一荣俱荣一损俱损，一个失败自动取消全部（3.11+）
- `create_task`：后台任务，扔出去不等它完成，继续干自己的事

### 判断标准

一个任务失败了，其他还要不要继续？要 → gather，不要 → TaskGroup，根本不关心结果 → create_task

**注意**：gather 的关键不是"同时生效"，是"允许部分失败"——这是周测时说错的地方。

## 阻塞操作

- `time.sleep`、`requests`、同步 DB 驱动会卡死整个事件循环
- 替代：`asyncio.sleep`、`aiohttp`、`asyncpg`、`asyncio.to_thread()`

## asyncio vs 多线程 vs 多进程

| 维度 | asyncio | 多线程 | 多进程 |
|------|---------|--------|--------|
| 并发方式 | 协作式 | 抢占式 | 真正并行 |
| 内存 | 极小 | 中（8MB/线程） | 大 |
| 适合 | I/O 密集 | I/O + 简单并发 | CPU 密集 |
| 安全 | 无竞态 | 需要锁 | 进程隔离 |

## GIL

- 同一时刻只允许一个线程执行 Python 字节码
- I/O 操作释放 GIL，C 扩展（NumPy）可主动释放
- 纯 CPU 密集多线程无法利用多核，要用多进程

## 异常处理

- `task.cancel()` 在下一次 await 时抛 CancelledError
- 在 except 中做清理，然后 raise 重新抛出
- CancelledError 在 3.9+ 继承 BaseException，except Exception 不会误捕获
