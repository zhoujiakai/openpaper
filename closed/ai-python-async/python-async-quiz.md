# Python 异步 — 题库

> 生成时间：2026-04-26
> 题目数量：8
> 关联笔记：python-async-ai-notes.md

---

## 题目

### Q1 [选择题] asyncio 的并发模型

asyncio 使用的是什么并发模型？

A. 多线程抢占式并发
B. 单线程协作式并发
C. 多进程并行
D. 多线程协作式并发

- **正确答案**：B
- **评分要点**：选择了正确选项即通过
- **知识点**：并发 vs 并行

### Q2 [选择题] 阻塞操作的影响

在协程中调用 `time.sleep(5)` 会发生什么？

A. 只阻塞当前协程 5 秒
B. 当前协程暂停，其他协程继续执行
C. 整个事件循环阻塞 5 秒，所有协程都等着
D. 自动转换为 asyncio.sleep

- **正确答案**：C
- **评分要点**：选择了正确选项即通过
- **知识点**：阻塞——asyncio 最大的敌人

### Q3 [简答题] await 底层机制

从 Python 层和操作系统层两个角度，解释 `await aiohttp.get(url)` 时发生了什么。

- **参考答案**：
  1. Python 层：协程在 await 处暂停，控制权还给 Task，Task 在 Future 上注册回调
  2. 操作系统层：socket 设为 non-blocking，注册到 epoll/kqueue
  3. 事件循环继续执行其他协程
  4. 操作系统通知 I/O 就绪，事件循环把回调放进 _ready
  5. 回调触发 Task.__step()，协程从 await 处继续
- **评分要点**：
  1. 必须提到协程暂停和 Future 回调注册
  2. 必须提到 epoll/kqueue 的 I/O 通知机制
  3. 加分项：提到 Task.__step() 驱动协程
- **知识点**：await 底层机制

### Q4 [简答题] gather vs TaskGroup

三种并发 API（gather、TaskGroup、create_task）分别适合什么场景？

- **参考答案**：
  1. gather + return_exceptions=True：独立任务，允许部分失败
  2. TaskGroup：有依赖的任务，一个失败取消全部（3.11+）
  3. create_task：后台长期任务，不等完成
- **评分要点**：三种场景都提到并给出合理理由
- **知识点**：并发 API 选型

### Q5 [对比题] asyncio vs 多线程 vs 多进程

从并发方式、内存开销、适合场景、数据安全四个维度对比。

- **参考答案**：
  | 维度 | asyncio | 多线程 | 多进程 |
  |------|---------|--------|--------|
  | 并发方式 | 协作式 | 抢占式 | 真正并行 |
  | 内存 | 极小 | 中（8MB/线程） | 大（独立内存空间） |
  | 适合 | I/O 密集 | I/O 密集+简单并发 | CPU 密集 |
  | 安全 | 无竞态 | 需要锁 | 进程隔离 |
- **评分要点**：至少正确对比 3 个维度
- **知识点**：技术选型

### Q6 [简答题] GIL 的影响和例外

GIL 是什么？它对多线程有什么影响？哪些情况下 GIL 会被释放？

- **参考答案**：
  1. GIL = Global Interpreter Lock，同一时刻只允许一个线程执行 Python 字节码
  2. 影响：纯 Python 的 CPU 密集型多线程无法利用多核
  3. 例外：I/O 操作（网络、文件、time.sleep）释放 GIL；C 扩展（如 NumPy）可主动释放 GIL
- **评分要点**：必须同时提到定义、影响、两个例外
- **知识点**：GIL

### Q7 [应用题] 大规模爬虫设计

设计一个爬虫：5000 个页面爬取 + CPU 密集 HTML 解析 + 结果存数据库。怎么设计？

- **参考答案**：
  1. asyncio + Semaphore 控制并发（如最多 100 个）
  2. 每个协程负责爬取一个页面
  3. HTML 解析用 ProcessPoolExecutor（进程池），绕过 GIL 做 CPU 并行
  4. 子进程只返回解析结果（纯数据），主进程用异步数据库 Session 存入数据库
  5. 不传数据库连接给子进程（不可 pickle）
- **评分要点**：并发控制 + 进程池 + 数据持久化三层设计
- **知识点**：综合应用

### Q8 [应用题] 优雅取消

写一个异步定时任务，每 5 秒从数据库拉数据。要求能被优雅取消——取消时关闭数据库连接。

- **参考答案**：
  ```python
  async def periodic_task():
      db = await create_db_connection()
      try:
          while True:
              data = await db.fetch("SELECT ...")
              process(data)
              await asyncio.sleep(5)
      except asyncio.CancelledError:
          await db.close()
          raise
  ```
- **评分要点**：try/except CancelledError + 清理 + raise 重新抛出
- **知识点**：异常处理、优雅取消

---

## 测试记录

### 2026-04-26 A4 默写测试

| 知识点 | 结果 | 备注 |
|--------|------|------|
| 1. asyncio 核心机制 | 🟢 通过 | |
| 2. await 底层发生了什么 | 🟡 基本通过 | Future 回调和 _scheduled 混淆 |
| 3. gather/TaskGroup/create_task 场景 | 🟢 通过 | |
| 4. 同步阻塞函数的处理 | 🟢 通过 | |
| 5. asyncio/多线程/多进程场景选择 | 🟢 通过 | |
| 6. task.cancel 工作机制 | 🟢 通过 | |
| 7. GIL 及其影响 | 🟢 通过 | |
| 8. 5000 页面爬虫设计 | 🟢 通过 | |
| 9. asyncio.sleep vs time.sleep | 🟢 通过 | |
| 10. 协程 vs 普通函数 | 🟡 基本通过 | 混淆了协程和事件循环 |

通过率：8/10 完全通过，2/10 基本通过

### 2026-04-30 周测

| 题目 | 结果 | 备注 |
|------|------|------|
| Q1 await 底层机制 | ⚠️ 基本通过 | 链路框架对了，"回调注册在 Future 上"仍然记不住 |
| Q2 协程 vs 普通函数 | ❌ 不正确 | 混淆了协程对象和 Task 对象 |
| Q3 阻塞操作 | ✅ 通过 | |
| Q4 三种并发 API | ⚠️ 基本通过 | gather 的关键特征是"允许部分失败"，不是"同时生效" |
| Q5 爬虫设计 | ✅ 通过 | 三层架构清晰，补充了 pickle 限制 |
| Q6 优雅取消 | ✅ 通过 | |

通过率：3/6 完全通过，2/6 基本通过，1/6 不正确

下次回测：2026-05-03 追加测试（优先：await 底层机制 Future 回调、协程 vs Task 区别）
