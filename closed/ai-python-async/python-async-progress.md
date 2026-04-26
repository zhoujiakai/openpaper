# Python 异步 — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-26

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现 | ✅ 已完成 | Real Python + Python 官方文档 |
| 2. 深度理解 | ✅ 已完成 | Section 6/6 |
| 3. 知识检验 | ⏳ 未开始 | — |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: 并发 vs 并行 | ✅ 已完成 | 理解核心区别，纠正了 3 个点 |
| Section 2: 事件循环内部运作 | ✅ 已完成 | 理解 _ready/_scheduled 和循环步骤 |
| Section 3: gather vs TaskGroup vs create_task | ✅ 已完成 | 会按场景选择，理解 TaskGroup 的适用范围 |
| Section 4: 阻塞——asyncio 最大的敌人 | ✅ 已完成 | 知道阻塞操作的替代方案 |
| Section 5: asyncio vs 多线程 vs 多进程 | ✅ 已完成 | 能组合使用 asyncio + ProcessPoolExecutor |
| Section 6: 异常处理 | ✅ 已完成 | 理解优雅取消和 CancelledError |

## 下次从哪里继续

阶段 3：知识检验（A4 默写测试 → 掌握度报告）

## 已掌握的关键知识点

- asyncio 是单线程协作式多任务，不是多线程
- 并发（任务切换）vs 并行（真正同时执行）
- 协程无竞态条件，但阻塞操作会卡住整个事件循环
- 协程切换靠 `await` 显式标记，不是自动检测 I/O
- 事件循环核心：_ready（马上执行）和 _scheduled（定时执行）两个数据结构
- await 底层：Python 层靠生成器 send/yield 暂停恢复，OS 层靠 epoll/kqueue 通知 I/O 就绪
- asyncio.sleep 不会卡住事件循环，回调进 _scheduled 等到期
- gather + return_exceptions=True：独立任务，允许部分失败
- TaskGroup：有依赖的任务，一个失败取消全部
- create_task：后台任务，不等完成
- 阻塞操作（time.sleep、requests、同步 DB）会拖死事件循环
- 异步替代：aiohttp、asyncpg、aiofiles、asyncio.to_thread()
- ProcessPoolExecutor：进程池，绕过 GIL 做 CPU 并行
- asyncio + ProcessPoolExecutor 组合：I/O 用协程，CPU 用进程池
- 进程间不共享内存，靠 pickle 序列化传数据，只能传原始数据
- asyncio.Semaphore 做并发控制
- task.cancel() 在下一次 await 时抛 CancelledError，需在 except 中做清理并重新抛出
- CancelledError 在 3.9+ 继承 BaseException，except Exception 不会误捕获

## 被纠正过的误区

- 误以为多线程受 CPU 核心数限制 → 线程数量受内存限制，受核心数限制的是多进程
- 混淆了协程自动切换和 await 显式切换 → 协程不会自动识别 I/O，靠代码中的 await
- GIL 限制的理解不够准确 → GIL 阻止多线程同时执行 Python 字节码，I/O 和 C 扩展会释放 GIL

## 需要复习的内容

- GIL 的精确含义和例外情况
- ProcessPoolExecutor 的实际用法（loop.run_in_executor）
