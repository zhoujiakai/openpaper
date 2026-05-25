# SQLAlchemy ORM — 题库

> 生成时间：2026-05-04
> 题目数量：7 + 2 补测
> 关联笔记：se-sqlalchemy-ai-notes.md

---

## 模拟题测试

### Q1 [选择题] 下面这段代码执行后，总共发了几条 SQL？

```python
stmt = select(User).options(joinedload(User.addresses))
users = session.execute(stmt).scalars().all()  # 查到 50 个用户
for user in users:
    print(user.addresses)  # 每个用户平均 3 个地址
```

A. 1 条
B. 51 条
C. 150 条
D. 50 条

- **正确答案**：A
- **评分要点**：joinedload 已在一条 SQL 里把用户和地址都查出来，后续访问是读内存
- **知识点**：joinedload 行为

### Q2 [简答题] 异步模式下，为什么 lazy loading 会报错？

- **参考答案**：
  1. lazy loading 的机制是访问属性时偷偷发 SQL
  2. 异步下发 SQL 必须用 await
  3. 属性访问（`user.addresses`）里没有 await 的位置
  4. 所以物理上做不到，直接报错（MissingGreenlet 或 DetachedInstanceError）
- **评分要点**：必须提到"属性访问里没有 await 的位置"
- **知识点**：异步 SQLAlchemy

### Q3 [对比题] joinedload 和 selectinload 的区别？

- **参考答案**：
  - joinedload：在数据库里 JOIN 拼表，一条 SQL。关联数据少时最优
  - selectinload：各查各的，Python 端组装，两条 SQL。关联数据多时避免重复
- **评分要点**：
  1. 需要说出"拼表"和"各查各的"的核心区别
  2. 需要提到 joinedload 有数据重复，selectinload 没有
- **知识点**：Eager Loading 策略

### Q4 [应用题] CV 检测系统每秒写入 200 条检测结果，用哪种插入方式？为什么不用 ORM 逐条 session.add()？

- **参考答案**：
  用 Core 直接插入（`__table__.insert()`）。ORM 逐条插入慢的原因是 Python 端的三个开销：身份映射、变更追踪、自动取自增 ID。Core 跳过这些，快 30 倍。
- **评分要点**：
  1. 必须说出用 Core 插入
  2. 必须提到 ORM 慢的原因是 Python 端的开销（不是数据库访问次数）
- **知识点**：性能陷阱

### Q5 [简答题] expire_on_commit 是什么？默认值是什么？什么时候必须改？

- **参考答案**：
  默认 True，commit 后对象属性被标记过期，再访问会触发 SELECT 刷新。异步模式下必须设 False，因为异步下隐式发 SQL 做不到（属性访问里没有 await）。
- **评分要点**：
  1. 知道默认是 True
  2. 知道异步下必须改
  3. 知道原因跟异步下不能隐式发 SQL 有关
- **知识点**：expire_on_commit

### Q6 [简答题] engine.begin() 和 engine.connect() 有什么区别？

- **参考答案**：
  - engine.begin()：自动事务管理，成功自动 commit，报错自动 rollback
  - engine.connect()：只拿连接，手动管事务
- **评分要点**：说清 begin() 自动管理，connect() 手动管理
- **知识点**：事务管理

### Q7 [应用题] 下面代码有什么问题？怎么改？

```python
stmt = select(User)
users = session.execute(stmt).scalars().all()
for user in users:
    print(len(user.orders))
```

- **参考答案**：
  N+1 问题。遍历时每次访问 user.orders 触发一次查询。改为：
  ```python
  stmt = select(User).options(selectinload(User.orders))
  users = session.execute(stmt).scalars().all()
  ```
- **评分要点**：
  1. 识别出 N+1 问题
  2. 给出正确的修改方案（selectinload 或 joinedload）
- **知识点**：N+1 问题识别与修复

---

## 补测题

### Q8 [简答题] 下面代码在异步模式下运行，会发生什么？

```python
async_session = async_sessionmaker(engine, class_=AsyncSession)  # 没设 expire_on_commit=False

async with async_session() as session:
    result = await session.execute(select(User).where(User.id == 1))
    user = result.scalar_one()
    user.name = "新名字"
    await session.commit()
    print(user.name)  # 这里会怎样？
```

- **正确答案**：B. 报错
- **评分要点**：commit 后属性过期，访问触发刷新，异步下刷新要 await，属性访问里没有 → 报错
- **知识点**：expire_on_commit + 异步

### Q9 [简答题] ORM 逐条插入比 Core 慢 30 倍，慢在哪三个开销？

- **参考答案**：
  1. 身份映射：Session 记住对象 ID，维护 {id: 对象} 映射
  2. 变更追踪：跟踪属性变化，算出要发哪些 SQL
  3. 自动取自增 ID：插入后查回主键，填充到对象上
- **评分要点**：三个点都要说到
- **知识点**：ORM vs Core 性能

---

## 测试记录

### 2026-05-04 模拟题测试

| 题号 | 类型 | 结果 | 备注 |
|------|------|------|------|
| Q1 | 选择 | ✅ | |
| Q2 | 简答 | ✅ | |
| Q3 | 对比 | ⚠️ | joinedload 去重是 Python 端做的，不是数据库端 |
| Q4 | 应用 | ⚠️ | 慢的原因是 Python 端追踪开销，不是数据库访问次数 |
| Q5 | 简答 | ❌ | 没答上来 |
| Q6 | 简答 | ✅ | 语音输入误说，实际理解正确 |
| Q7 | 应用 | ✅ | |

### 2026-05-04 补测（薄弱点）

| 题号 | 类型 | 结果 | 备注 |
|------|------|------|------|
| Q8 | 简答 | ✅ | |
| Q9 | 简答 | ✅ | 重测通过 |

### 2026-05-04 A4 默写测试

| 知识点 | 结果 | 备注 |
|--------|------|------|
| N+1 问题和解决方式 | 🟢 通过 | |
| 异步和同步的关键区别 | 🟢 通过 | |
| joinedload vs selectinload 场景 | 🟡 基本通过 | "为什么"没主动说 |
| ORM 插入 vs Core 插入 | 🔴→🟢 重测通过 | |
| expire_on_commit | 🟢 通过 | |
| 变更追踪的前提条件 | 🔴→🟢 重测通过 | |
| raiseload | 🔴→🟢 重测通过 | |

通过率：7/7（含重测）
下次回测：2026-05-11 周测
