# Celery 异步任务队列 — AI 笔记

> 来源：Celery 官方文档（docs.celeryq.dev）、Celery Tasks 文档、Celery Canvas 文档、Celery Workers 文档、"Celery and asyncio: A Guide to Bridging"（blog.miguelgrinberg.com）
> 生成时间：2026-05-01
> 学习目标：面试准备，理解 Celery 架构原理、任务生命周期、重试幂等、与 RabbitMQ 集成、Celery vs asyncio 场景选择

---

## 锚点

想象一家连锁餐厅的后厨系统。

你（生产者）把菜单塞进窗口的投单箱（**Broker**）。后厨的厨师们（**Worker**）从投单箱取菜单，各自做各自的菜。做完后，厨师在出菜口的小黑板上写下"第 28 号订单已完成"（**Backend**）。你不用站在窗口等，该干嘛干嘛，回头来看黑板就行。

如果你点了"先做沙拉，再做牛排"，这是一条**链**（chain）。如果你点了四道菜同时做，这是一个**组**（group）。如果你说"四道菜全做完再上甜点"，这是一个**和弦**（chord）。

关键：你不用自己炒菜。菜是别人做的，你只管下单和取餐。

## 核心问题

为什么不能用 asyncio 或 threading 解决一切？因为有些工作太重了——发邮件要等 SMTP 服务器响应、跑机器学习模型要吃满 CPU、生成报表要查十几张表。这些活如果在 Web 请求处理过程中做，用户就盯着转圈等。Celery 解决的问题：**把重活扔到另一个进程甚至另一台机器上做，做完再告诉我结果**。

## 核心概念

### Broker：投单箱

Broker 是生产者和工人之间的中间人。生产者把任务消息发到 Broker，Worker 从 Broker 取任务。

为什么需要它？如果没有 Broker，生产者必须直接把任务交给 Worker。那 Worker 挂了怎么办？Worker 还没启动怎么办？生产者得自己管这些。有了 Broker，生产者只管往里扔，Worker 按自己的节奏来取。两边彻底解耦。

Celery 支持多种 Broker：**RabbitMQ**（最推荐，功能最全）、**Redis**（简单快速，但不保证消息持久化到磁盘）。选哪个？生产环境用 RabbitMQ，开发环境用 Redis 图方便。

### Worker：厨师

Worker 是真正干活的进程。它从 Broker 取任务，执行任务里的函数，把结果存到 Backend（如果配了的话）。

Worker 的并发模式默认是 **prefork**——一个主进程 fork 出多个子进程，每个子进程同时处理一个任务。为什么不用线程？因为 Python 有 GIL，CPU 密集型任务用线程没有真正的并行。fork 出多个进程，每个进程有自己的 GIL，才能真正跑满多核。

也可以切换成 **gevent** 或 **eventlet** 模式——用协程实现并发，适合 I/O 密集型任务（比如同时等 100 个 HTTP 请求返回）。但要注意，协程模式下任务里不能有阻塞操作，否则整个 Worker 卡住。

### Backend：出菜口的小黑板

任务执行完了，结果放哪？默认不存——任务做完就做完，没人知道结果。如果你需要拿结果（比如报表生成的文件路径、邮件发送是否成功），就要配 Backend。

Backend 的选择：**RPC**（通过 Broker 回传结果，简单但不持久）、**Redis**（快，适合临时结果）、**数据库**（持久化，但慢）。用哪个看需求：结果要留多久？查询频繁吗？

### Task：菜单上的一道菜

Task 就是你要 Celery 帮你执行的函数。用 `@app.task` 装饰器标记一个普通函数，它就变成了可以被远程执行的任务。

```python
@app.task
def send_email(to, subject, body):
    # 发邮件的代码
    return f"sent to {to}"
```

调用方式有讲究：
- `send_email("a@b.com", "Hi", "...")` — 普通调用，在当前进程同步执行
- `send_email.delay("a@b.com", "Hi", "...")` — 异步调用，扔给 Worker 执行
- `send_email.apply_async(args=["a@b.com", "Hi", "..."], countdown=60)` — 异步调用，60 秒后执行

`.delay()` 是 `.apply_async()` 的简写。需要更多控制（延迟执行、指定队列、设超时）就用 `apply_async`。

任务有生命周期：**PENDING → STARTED → SUCCESS / FAILURE / RETRY / REVOKED**。PENDING 是默认初始状态（其实不算真正的状态，只是"还没开始"），SUCCESS 是成功，FAILURE 是失败，RETRY 是正在重试，REVOKED 是被撤销。

## 逐节详解

### Section 1: 架构原理（Worker / Broker / Backend）

回到餐厅比喻。三个角色缺一不可：

**Broker（投单箱）**：存储任务消息。RabbitMQ 和 Redis 是最常用的两个。Broker 的选型直接决定了消息可靠性的上限——如果 Broker 丢了消息，任务就没了。

**Worker（厨师）**：消费任务并执行。一个机器可以跑多个 Worker，一个 Worker 可以 fork 出多个子进程（prefork 模式）。Worker 可以通过命令行启动：

```bash
celery -A myapp worker --loglevel=info --concurrency=4
```

`--concurrency=4` 表示 4 个子进程同时处理任务。

**Backend（小黑板）**：可选。不配 Backend，`task.delay()` 返回的 `AsyncResult` 对象就只能查状态（PENDING / STARTED），查不到结果。配了 Backend，才能 `result.get()` 拿到返回值。

三个角色可以在不同机器上。Broker 在机器 A，Worker 在机器 B 和 C，Backend 在机器 D。这就是"分布式"的意思——任务不一定在 Web 服务器上执行。

### Section 2: 任务调度策略

任务不是"扔出去就完事"，有时需要精细控制。

**延迟执行**：`countdown=60` 让任务 60 秒后才开始。或者用 `eta=datetime(2026, 5, 1, 12, 0)` 指定精确时间。区别：countdown 是相对时间，eta 是绝对时间。

**指定队列**：默认所有任务进同一个队列。但有些任务优先级高（发验证码），有些低（发营销邮件）。可以建多个队列，让不同的 Worker 处理不同队列：

```python
# 指定任务路由
@app.task(queue='high_priority')
def send_verification_code(phone):
    ...

# 启动 Worker 时指定监听的队列
# celery -A myapp worker -Q high_priority
```

**限速**：`rate_limit='10/m'` 限制每分钟最多执行 10 次。比如调第三方 API 有频率限制，不能无限调。

**过期**：`expires=300` 表示任务 5 分钟内没被执行就作废。比如"5 分钟内发验证码"这种有时效性的任务。

### Section 3: 结果存储

任务结果存哪？取决于 Backend 的选择。

| Backend | 优点 | 缺点 | 适用场景 |
|---------|------|------|----------|
| RPC | 零配置 | 结果不持久，Broker 重启就丢 | 临时结果 |
| Redis | 快 | 占内存，结果有过期时间 | 短期结果 |
| 数据库（SQLAlchemy/Django ORM） | 持久 | 慢，要清旧数据 | 需要留存的结果 |

**结果过期**：`result_expires=3600` 让结果在 Backend 里 1 小时后自动删除。不设的话，Redis 里会越积越多。

**要不要存结果？** 很多任务不需要结果。发邮件，发了就行，不用知道结果。这时候可以 `@app.task(ignore_result=True)` 跳过 Backend 存储，省资源。

### Section 4: 重试与幂等

这是生产环境最关键的两个概念。

#### 重试

任务执行失败怎么办？直接失败太粗暴。很多时候是临时问题——数据库连接闪断、第三方 API 超时。重试几次就好了。

**手动重试**：

```python
@app.task(bind=True, max_retries=3)
def send_email(self, to, subject, body):
    try:
        # 发邮件
    except SMTPException as exc:
        raise self.retry(exc=exc, countdown=60)
```

`bind=True` 让第一个参数是 `self`（任务实例），这样才能调 `self.retry()`。`countdown=60` 表示 60 秒后重试。`max_retries=3` 限制最多重试 3 次，超过就彻底失败。

**自动重试**（更简洁）：

```python
@app.task(autoretry_for=(SMTPException, TimeoutError),
          retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_email(to, subject, body):
    # 发邮件，抛出指定异常时自动重试
```

**指数退避**：重试间隔越来越长，避免雪崩。`retry_backoff=True` 开启，第一次等 1 秒，第二次 2 秒，第三次 4 秒。也可以设 `retry_backoff=60` 从 60 秒开始。

#### 幂等

重试的代价：同一条消息可能被消费两次。Worker 取了任务、执行了一半挂了，Broker 没收到 ACK，把任务重新分配给另一个 Worker。结果同一条任务执行了两次。

如果任务是"给账户加 100 块"，执行两次就加了 200 块。这就是没有幂等性的后果。

**Celery 层面的保障**：

`acks_late=True` — Worker 不是取任务就 ACK，而是执行完才 ACK。配合 `reject_on_worker_lost=True`，如果 Worker 在执行过程中挂了，任务会被重新入队。这保证了"至少执行一次"，但不保证"恰好一次"。

**业务层面的幂等**（必须自己做）：

1. **唯一 ID 去重** — 每个任务带 `task_id`，执行前查这个 ID 有没有处理过
2. **天然幂等操作** — `SET balance = 100` 而非 `ADD balance + 100`
3. **乐观锁/版本号** — 更新时带版本号，版本号不对就跳过
4. **数据库唯一约束** — 用 task_id 做唯一索引，重复插入直接失败

这和消息队列的幂等消费是同一套思路（参考 `se-message-queue` 笔记）。

### Section 5: Canvas — 工作流编排

单个任务不够用。有时需要"先做 A，再做 B，最后做 C"。Celery 用 Canvas 来编排复杂工作流。

**Signature（签名）** — 任务的"处方"，描述怎么调用一个任务但不立即执行：

```python
# 创建签名
s = add.s(2, 3)      # 位置参数
s = add.s(2)          # 部分参数，另一个参数后续填入
s = add.signature((2, 3), countdown=10)
```

**Chain（链）** — 串行执行，前一个的结果传给后一个：

```python
# 先验证，再处理，最后发通知
chain(validate.s(data), process.s(), notify.s())()
```

前一个任务的返回值会作为下一个任务的第一个参数。像流水线：每个工位处理完传给下一个。

**Group（组）** — 并行执行，等所有完成：

```python
# 同时生成 4 份报表
group(generate_report.s(i) for i in range(4))()
```

返回一个 `GroupResult`，可以 `.join()` 等所有结果。

**Chord（和弦）** — 先并行执行一组任务，全部完成后执行一个回调：

```python
# 并行处理所有订单，全部完成后汇总
chord(process_order.s(order) for order in orders)(summarize.s())
```

chord = group + callback。前面所有任务的结果会作为一个列表传给回调函数。

**实际用得最多的是 chain 和 group**。chord 因为有"等全部完成再汇总"的语义，实现上比看起来复杂，调试也麻烦。

### Section 6: Worker 并发与弹性

#### 并发模式

**prefork（默认）**：主进程 fork 出 N 个子进程。每个子进程独立运行，互不影响。适合 CPU 密集型。缺点是内存占用大（每个子进程一份），进程间不能共享内存。

**gevent / eventlet**：用协程实现并发。一个进程里跑几百个协程，每个协程处理一个任务。适合 I/O 密集型（网络请求、数据库查询）。内存占用小，但要求任务不能有阻塞调用。

**solo**：单进程单线程，一次只处理一个任务。调试用。

**threads**：用线程池。因为有 GIL，CPU 密集型没有真正并行。但在某些场景（比如任务里有 C 扩展会释放 GIL）可能有用。

#### Autoscaling

Worker 可以动态调整子进程数量：

```bash
celery -A myapp worker --autoscale=10,3
```

最少 3 个进程，最多 10 个。任务多的时候自动扩到 10，闲的时候缩回 3。配合 `-Q` 指定队列，不同队列用不同的 autoscale 策略。

#### 优雅关闭

Worker 关闭不是"拔电源"。分四个阶段：

1. **Warm shutdown**（`SIGTERM`）：不接收新任务，等当前任务完成再退出
2. **Soft shutdown**（`SIGQUIT`，需开启）：等当前任务完成，但设了超时
3. **Cold shutdown**：当前任务立即中断，退回 Broker
4. **Hard shutdown**（`SIGKILL`）：进程直接杀掉，任务状态未知

生产环境用 warm shutdown，确保任务不丢。如果在 warm shutdown 过程中 Worker 被强制杀掉（比如 Kubernetes 的 pod eviction），配合 `acks_late=True` 可以让任务重新入队。

#### 远程控制

Worker 启动后，可以在不重启的情况下动态调整：

```bash
# 查看所有 Worker 状态
celery -A myapp inspect active

# 动态修改某个任务的 rate_limit
celery -A myapp control rate_limit myapp.send_email 100/m

# 撤销一个正在执行的任务
celery -A myapp control revoke <task_id>
```

这些命令通过 Broker 发消息给 Worker，Worker 收到后执行。不需要 SSH 到 Worker 所在的机器。

### Section 7: 与 RabbitMQ 集成

Celery 用 RabbitMQ 做 Broker 时，背后的机制是什么？

**默认 Exchange**：Celery 在 RabbitMQ 里自动创建 `celery` Exchange（direct 类型）和 `celery` 队列。所有没有指定队列的任务，默认进 `celery` 队列。

**自定义队列路由**：可以配置任务路由，让不同任务进不同队列：

```python
# celeryconfig.py
task_routes = {
    'myapp.send_email': {'queue': 'email'},
    'myapp.generate_report': {'queue': 'report'},
}
```

这会在 RabbitMQ 里创建 `email` 和 `report` 两个队列。启动 Worker 时指定监听：

```bash
celery -A myapp worker -Q email    # 只处理邮件任务
celery -A myapp worker -Q report   # 只处理报表任务
celery -A myapp worker -Q email,report  # 两个都处理
```

**消息可靠性**：Celery + RabbitMQ 的可靠性，依赖你之前学的消息队列三道防线（参考 `se-message-queue` 笔记）：

1. **Publisher Confirm** — Celery 的 `publish_retry` 配置控制发送重试
2. **Broker 持久化** — RabbitMQ 队列设 `durable=True`，消息设 `delivery_mode=2`
3. **Consumer ACK** — Celery 的 `acks_late=True` 控制何时 ACK

如果三道都开了，任务消息"几乎不丢"。但"几乎不丢"≠"恰好一次"，所以幂等消费仍然必须。

### Section 8: Celery vs asyncio

面试常问："什么时候用 Celery，什么时候用 asyncio？"

它们解决的不是同一个问题。

**asyncio** 解决的是**单机并发**问题。一个进程里，用事件循环切换协程，实现"等 I/O 的时候去做别的事"。适合：同时调多个 API、同时查多个数据库、WebSocket 长连接。

**Celery** 解决的是**分布式任务**问题。把任务扔到另一个进程（可能在另一台机器上），异步执行，做完通知。适合：发邮件、生成报表、跑模型、定时任务。

| 维度 | Celery | asyncio |
|------|--------|---------|
| 执行位置 | 独立进程，可以跨机器 | 当前进程内 |
| 重启存活 | Worker 重启不影响任务 | 进程重启，协程全没 |
| 重试 | 内置重试 + 指数退避 | 要自己写 |
| 任务编排 | Canvas（chain/group/chord） | 需手动编排 |
| 水平扩展 | 加 Worker 就行 | 扩不了（单进程） |
| 延迟 | 毫秒到秒级（经过 Broker） | 微秒级（内存） |
| 复杂度 | Broker + Worker + Backend | 只需要 Python |

**能不能一起用？** Celery Worker 默认是同步的，不支持直接 `await`。但可以通过桥接模式在 Worker 里跑 asyncio 代码：

```python
import asyncio

@app.task
def async_task():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(my_async_function())
```

或者用信号初始化事件循环：

```python
from celery.signals import worker_process_init

loop = None

@worker_process_init.connect
def init_loop(**kwargs):
    global loop
    loop = asyncio.new_event_loop()

@app.task
def async_task():
    return loop.run_until_complete(my_async_function())
```

这不是 Celery 原生支持，是 workaround。如果你的任务本身是 async 的，可以考虑用 Celery 的 gevent/eventlet 模式，或者干脆不用 Celery，直接用 asyncio + 任务队列（比如 arq）。

**选型口诀**：单机 I/O 并发用 asyncio，分布式重活用 Celery。不是二选一，可以都用在同一个项目里——Web 请求里用 asyncio 并发调 API，重活扔给 Celery Worker。

## 与其他方法的对比

| 维度 | Celery | asyncio | threading |
|------|--------|---------|-----------|
| 执行位置 | 独立进程/远程机器 | 当前进程 | 当前进程 |
| 并发模型 | 多进程（prefork） | 单线程协程 | 多线程 |
| GIL 影响 | 无（多进程） | 无（单线程） | 有（CPU 密集型受限） |
| 任务持久化 | 支持（Broker 存储） | 不支持 | 不支持 |
| 重试机制 | 内置 | 需自己实现 | 需自己实现 |
| 水平扩展 | 加 Worker 机器 | 不支持 | 不支持 |
| 适用场景 | 重 CPU/重 I/O/定时/分布式 | I/O 密集/单机并发 | 简单并发/兼容阻塞库 |
| 依赖 | Broker + 可选 Backend | 只需 Python | 只需 Python |

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| Celery 架构 | 你理不理解分布式任务队列的模型 | 说清 Broker/Worker/Backend 三角色，用比喻也行 | 只说"Celery 是异步任务队列"没有展开 |
| 任务重试 | 你做过生产级的异步任务吗 | 说 `autoretry_for` + `retry_backoff`，提到指数退避 | 不知道有自动重试，以为只能 try/catch |
| 幂等消费 | 你处理过重复执行的问题吗 | 说至少两种实现方式，强调重试会导致重复 | 不知道 Worker 挂了任务会重新入队 |
| Celery vs asyncio | 你有技术选型的判断力 | 先说解决的不同问题（分布式 vs 单机），再给场景 | 只说"Celery 更好"没有场景分析 |
| Worker 并发模式 | 你理解 prefork 和 gevent 的区别 | prefork 多进程绕 GIL、gevent 协程省内存，各适合什么场景 | 不知道 gevent 模式下不能有阻塞调用 |
| Canvas 工作流 | 你用过复杂任务编排吗 | 说 chain（串行）和 group（并行），chord 看情况提 | 没听说过 Canvas |
| acks_late | 你理解 Consumer ACK 的时机 | 说清"执行完再 ACK"vs"取到就 ACK"的区别和场景 | 不知道 acks_late 的作用 |
| Broker 选型 | 你知道 RabbitMQ 和 Redis 的区别 | RabbitMQ 消息可靠、Redis 快但不保证持久化，生产用 RabbitMQ | 以为 Redis 和 RabbitMQ 完全等价 |
