# SQLAlchemy ORM 深入掌握 — AI 笔记

> 来源：
> - [SQLAlchemy 2.0 Official Unified Tutorial](https://docs.sqlalchemy.org/tutorial/index.html)
> - [SQLAlchemy Performance FAQ](https://docs.sqlalchemy.org/en/latest/faq/performance.html)
> - [Relationship Loading Techniques (官方)](https://docs.sqlalchemy.org/14/orm/loading_relationships.html)
> - [Mastering SQLAlchemy (Medium)](https://medium.com/@ramanbazhanau/mastering-sqlalchemy-a-comprehensive-guide-for-python-developers-ddb3d9f2e829)
> - [Async SQLAlchemy 2 Guide (Dev.to)](https://dev.to/amverum/asynchronous-sqlalchemy-2-a-simple-step-by-step-guide-to-configuration-models-relationships-and-3ob3)
> - [OneUptime - SQLAlchemy 2.0 Patterns](https://oneuptime.com/blog/post/2026-01-27-work-with-sqlalchemy-orm-python/view)
> 生成时间：2026-05-01
> 学习目标：面试准备（项目中大量使用但未系统掌握）

---

## 锚点

SQLAlchemy 就是一个**翻译官团队**。你在 Python 这边用对象说话（`user.addresses`），它在数据库那边用 SQL 说话（`SELECT ... JOIN ...`）。这个团队里每个人负责一件事：Engine 管连接数据库，Session 管跟踪你的修改，ORM 负责把对象翻译成表、把属性翻译成列。性能问题的关键永远是：你让翻译官跑了几趟数据库？

## 核心问题

为什么直接写 SQL 不够用？因为 SQL 是给数据库看的，不是给 Python 程序员看的。你在 Python 里写 `cursor.execute("SELECT ...")`，拿到的是一堆元组，不是对象。你得手动把每一列映射到属性上，手动拼 INSERT/UPDATE 语句，手动处理外键关系。项目一大，这些手动的活儿又容易出错又难维护。SQLAlchemy 就是来干这些脏活的——但干得太自动化了，你不理解它背后的机制，就会踩坑（N+1 查询、Session 泄漏、异步下的坑）。

## 核心概念

### Engine — 连接大门

Engine 是你和数据库之间的第一道门。你给它一个连接字符串，它帮你管理连接池。你不用自己处理连接的创建和回收。

```python
from sqlalchemy import create_engine

# 同步
engine = create_engine("postgresql://user:pass@localhost/dbname", pool_size=10, max_overflow=20)

# 异步
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/dbname")
```

为什么重要：没有 Engine，后面所有东西都连不上数据库。它是整个 SQLAlchemy 的地基。

### Session — 改动追踪器

Session 是 SQLAlchemy 最核心的概念。它做的事就三件：

1. **Identity Map（身份映射）**：同一行数据在 Session 里只有一个对象。你查两次 `user_id=1`，拿到的同一个 Python 对象。这避免了内存里出现两个不一致的副本。
2. **Unit of Work（工作单元）**：你改了对象的属性，Session 偷偷记下了。调 `commit()` 的时候，它自动算出要发哪些 SQL。你不用手动写 UPDATE。
3. **Transaction（事务）**：一个 Session 就是一个事务范围。commit 提交，rollback 回滚。

```python
from sqlalchemy.orm import Session

# 同步用法
with Session(engine) as session:
    user = session.execute(select(User).where(User.id == 1)).scalar_one()
    user.name = "新名字"  # 改属性，Session 自动追踪
    session.commit()  # 自动发 UPDATE users SET name='新名字' WHERE id=1

# 异步用法
from sqlalchemy.ext.asyncio import AsyncSession
async with AsyncSession(engine) as session:
    result = await session.execute(select(User).where(User.id == 1))
    user = result.scalar_one()
    user.name = "新名字"
    await session.commit()
```

为什么重要：不理解 Session 生命周期，就会遇到 "DetachedInstanceError"（对象脱离了 Session，访问延迟加载的属性就报错）、Session 泄漏（没关 Session，连接池被耗尽）这些坑。

### 模型定义 — 对象和表的映射规则

SQLAlchemy 2.0 推荐用 `Mapped` + `mapped_column` 的方式定义模型。比老式的 `Column()` 更类型安全，IDE 也能自动补全。

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    # 关系定义
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")
```

既然模型定义好了，那两个表之间的关系怎么映射？这就是 relationship 出场的原因。

### relationship — 对象间的导航

`relationship()` 让你用 `user.addresses` 直接拿到关联对象，不用手写 JOIN。它背后做的事是：看 ForeignKey，知道要 JOIN 哪张表，帮你生成 SQL。

```python
# 一对多：一个 User 有多个 Address
# User 那边：addresses = relationship("Address", back_populates="user")
# Address 那边：user = relationship("User", back_populates="addresses")

# 多对多：需要关联表
from sqlalchemy import Table, Column, Integer, ForeignKey

student_course = Table("student_course", Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    courses: Mapped[List["Course"]] = relationship(secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    students: Mapped[List["Student"]] = relationship(secondary=student_course, back_populates="courses")
```

`back_populates` 是双向绑定的关键。两边必须互相指，否则一边改了另一边不知道。

### 查询（2.0 风格）— select() 统一一切

SQLAlchemy 2.0 用 `select()` 取代了老的 `session.query()`。ORM 和 Core 现在用同一种写法。

```python
from sqlalchemy import select

# 查所有
stmt = select(User)
users = session.execute(stmt).scalars().all()

# 条件查询
stmt = select(User).where(User.name == "Alice")
user = session.execute(stmt).scalar_one_or_none()

# JOIN
stmt = select(User, Address).join(Address).where(User.name == "Alice")
results = session.execute(stmt).all()

# 聚合
from sqlalchemy import func
stmt = select(func.count(User.id))
count = session.execute(stmt).scalar_one()
```

`scalars()` 从结果里提取 ORM 对象（去掉 Row 包装），`all()` 变成列表，`scalar_one_or_none()` 拿单个结果或 None。

## 关键代码模式

### 模式 1：连接字符串

```python
# SQLite（开发/测试用）
"sqlite:///./app.db"          # 文件数据库
"sqlite+aiosqlite:///:memory:"  # 异步内存数据库

# PostgreSQL
"postgresql://user:pass@localhost:5432/dbname"          # 同步
"postgresql+asyncpg://user:pass@localhost:5432/dbname"   # 异步

# MySQL
"mysql+pymysql://user:pass@localhost/dbname"
```

### 模式 2：Session 工厂

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

# 同步
SyncSession = sessionmaker(engine, expire_on_commit=False)

# 异步
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

`expire_on_commit=False` 很关键。默认 commit 后，对象所有属性都过期了，再访问会触发一次查询。设成 False 可以避免这个问题，特别是在异步模式下（异步不支持延迟加载，过期属性直接报错）。

### 模式 3：上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def session_scope():
    session = SyncSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# 使用
with session_scope() as session:
    user = session.execute(select(User).where(User.id == 1)).scalar_one()
    user.name = "新名字"
```

这是最安全的 Session 管理方式。自动 commit，出错自动 rollback，最后一定 close。

## 逐节详解

### Section 1: Lazy Loading vs Eager Loading — 性能最大的坑

这是 SQLAlchemy 面试最常问的问题。核心矛盾：默认情况下，关系属性是"用到才查"（lazy loading）。你查 100 个用户，然后遍历每个用户的 addresses，就发 101 条 SQL（1 查用户 + 100 查地址）。这就是 **N+1 问题**。

解决方式是 **Eager Loading（预加载）**，一次查询把关联数据全拿出来。SQLAlchemy 提供三种策略：

| 策略 | 函数 | 生成的 SQL | 适用场景 |
|------|------|-----------|----------|
| Joined Loading | `joinedload()` | LEFT OUTER JOIN | 关联数据量小，一对一或一对少 |
| Select IN Loading | `selectinload()` | SELECT ... WHERE id IN (...) | 一对多，关联数据量大 |
| Subquery Loading | `subqueryload()` | 子查询方式加载 | 旧项目兼容，一般用 selectinload 替代 |

```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# joinedload — 一条 SQL 搞定（JOIN）
stmt = select(User).options(joinedload(User.addresses))
# 生成：SELECT users.*, addresses.* FROM users LEFT OUTER JOIN addresses ON ...

# selectinload — 两条 SQL（先查用户，再 IN 查地址）
stmt = select(User).options(selectinload(User.addresses))
# 生成：
# 1. SELECT users.* FROM users
# 2. SELECT addresses.* FROM addresses WHERE addresses.user_id IN (1, 2, 3, ...)

# 还可以 raiseload — 访问就报错（强制你必须显式选择加载策略）
from sqlalchemy.orm import raiseload
stmt = select(User).options(raiseload(User.addresses))
# 访问 user.addresses → 抛异常，逼你思考要不要加载
```

什么时候用哪个？简单说：关联数据少用 `joinedload`（一次查询，效率高），关联数据多用 `selectinload`（避免 JOIN 产生巨大的笛卡尔积）。生产环境推荐在模型上设置 `lazy="selectin"`，全局避免 N+1。

### Section 2: 异步 SQLAlchemy — 和同步的关键区别

异步 SQLAlchemy 不是"把同步代码加个 async/await 就行"。有几个本质区别：

**1. 不能用延迟加载**

异步下，`user.addresses` 不会偷偷发查询（因为那是同步 IO）。你必须在查询时用 `selectinload` 或 `joinedload` 显式加载。

```python
# 错误 — 异步下访问未加载的关系会报错
async with AsyncSessionLocal() as session:
    result = await session.execute(select(User))
    user = result.scalar_one()
    print(user.addresses)  # ❌ MissingGreenlet 或 DetachedInstanceError

# 正确 — 显式预加载
async with AsyncSessionLocal() as session:
    stmt = select(User).options(selectinload(User.addresses))
    result = await session.execute(stmt)
    user = result.scalar_one()
    print(user.addresses)  # ✅ 已经加载好了
```

**2. expire_on_commit 必须设 False**

原因同上。commit 后如果属性过期，再访问需要重新查询，但异步下做不到自动重查。

**3. 用 async_sessionmaker 而不是手动创建**

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_user(user_id: int):
    async with async_session() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

# 关闭时
async def shutdown():
    await engine.dispose()
```

**4. 异步驱动选择**

| 数据库 | 同步驱动 | 异步驱动 |
|--------|---------|---------|
| PostgreSQL | psycopg2 | asyncpg |
| MySQL | pymysql / mysqlclient | aiomysql |
| SQLite | 内置 sqlite3 | aiosqlite |

### Section 3: 事务管理 — commit、rollback、嵌套事务

SQLAlchemy 的事务模型：一个 Session 对应一个事务。`commit()` 提交当前事务并自动开启新事务。`rollback()` 回滚当前事务。

```python
# 基本事务
with Session(engine) as session:
    session.add(User(name="Alice"))
    session.commit()   # 提交
    # 如果出错 → session.rollback() 自动回滚（with 语句保证）

# 嵌套事务（SAVEPOINT）
with Session(engine) as session:
    session.add(User(name="Alice"))

    nested = session.begin_nested()  # 创建 SAVEPOINT
    try:
        session.add(User(name="Bob"))
        # 这里有问题
        raise Exception("出错了")
    except:
        nested.rollback()  # 只回滚到 SAVEPOINT，Alice 还在
    # Bob 被回滚了，Alice 还在

    session.commit()  # 提交 Alice
```

嵌套事务用 `begin_nested()`。它创建数据库的 SAVEPOINT，只回滚到那个点，不影响外层事务。适合在一个大事务里做"可能失败的子操作"。

**隔离级别**设置：

```python
# 全局设置
engine = create_engine(url, isolation_level="READ COMMITTED")

# 单个连接设置
with engine.connect() as conn:
    conn = conn.execution_options(isolation_level="SERIALIZABLE")
    # 用这个连接的查询都是 SERIALIZABLE 级别
```

四种隔离级别从低到高：READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE。级别越高，一致性越强，并发性能越差。大多数 Web 应用用 READ COMMITTED 就够了。

### Section 4: 性能陷阱和优化

**陷阱 1：N+1 查询**

最常见的性能杀手。解决方案就是用 `selectinload` / `joinedload`。

怎么发现？开 SQL 日志：`create_engine(url, echo=True)`，看到同一个模式的查询重复出现，就是 N+1。

**陷阱 2：大批量 ORM 插入太慢**

ORM 插入 10 万行需要 6.9 秒，用 Core 只需要 0.21 秒——差 30 倍。因为 ORM 要做身份映射、变更追踪、自动取自增 ID 这些事。

```python
# 慢 — ORM 逐条插入
for i in range(100000):
    session.add(Customer(name=f"NAME {i}"))
    if i % 1000 == 0:
        session.flush()
session.commit()  # ~6.9 秒

# 快 — bulk 操作
session.bulk_insert_mappings(Customer, [
    {"name": f"NAME {i}"} for i in range(100000)
])
session.commit()  # ~0.47 秒

# 最快 — Core 直接插入
with engine.connect() as conn:
    conn.execute(Customer.__table__.insert(), [
        {"name": f"NAME {i}"} for i in range(100000)
    ])
    conn.commit()  # ~0.21 秒
```

**陷阱 3：连接池耗尽**

```python
# 好的配置
engine = create_engine(url,
    pool_size=10,        # 常驻连接数
    max_overflow=20,     # 高峰时额外开 20 个
    pool_recycle=1800,   # 30 分钟回收一次（防止数据库关掉空闲连接）
    pool_timeout=30,     # 等连接最多等 30 秒
)
```

**陷阱 4：expire_on_commit 导致的隐式查询**

默认 commit 后所有对象属性过期。你再访问 `user.name`，SQLAlchemy 会自动发一条 SELECT 刷新对象。如果在循环里 commit 后又访问属性，就会多出一堆查询。设 `expire_on_commit=False` 可以避免。

**陷阱 5：在 async 下忘记预加载**

前面说过，异步下延迟加载直接报错。解决方案：要么查询时 `options(selectinload(...))`，要么在模型上设 `lazy="selectin"`。

### Section 5: 2.0 迁移要点

如果你之前用的 1.x 风格，这几个变化最重要：

| 1.x 写法 | 2.0 写法 | 变化说明 |
|---------|---------|---------|
| `session.query(User).filter(...)` | `session.execute(select(User).where(...))` | select() 统一了 ORM 和 Core |
| `declarative_base()` | `class Base(DeclarativeBase): pass` | 新的类型声明方式 |
| `Column(Integer, primary_key=True)` | `mapped_column(primary_key=True)` 类型用 `Mapped[int]` | 类型安全 |
| `Query.all()` | `session.execute(stmt).scalars().all()` | 两步走：execute + scalars |
| `Query.first()` | `session.execute(stmt).scalar_one_or_none()` | 更明确的语义 |

## 与其他方案的对比

SQLAlchemy 和其他 ORM/数据库方案要解决的是同一个问题吗？不完全相同。SQLAlchemy 既有 ORM 层（高层抽象），也有 Core 层（底层控制）。它是"全栈"数据库工具，不是纯 ORM。

| 维度 | SQLAlchemy ORM | SQLAlchemy Core | Django ORM | 原生 SQL |
|------|---------------|-----------------|------------|---------|
| 抽象层级 | 高（对象操作） | 中（SQL 构建器） | 高（对象操作） | 低（手写 SQL） |
| 查询灵活性 | 高（可混用 Core） | 最高 | 中（复杂查询受限） | 最高 |
| 性能控制 | 中（需注意 N+1 等） | 高 | 中 | 最高 |
| 学习曲线 | 陡 | 更陡 | 平缓 | 取决于 SQL 功底 |
| 数据库迁移 | Alembic | Alembic | 内置 | 手动 |
| 异步支持 | 2.0 原生支持 | 2.0 原生支持 | Django 5.0+ | 取决于驱动 |

关键区别：Django ORM 和模型绑死在 Django 框架里，SQLAlchemy 是独立的，可以配 Flask、FastAPI 或任何框架。而且 SQLAlchemy 的 Core 层让你在 ORM 不够用时，随时降级到 SQL 级别的控制。

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| 什么是 N+1 问题？怎么解决？ | 你有没有实际处理过 ORM 性能问题 | 用 `selectinload` 或 `joinedload` 预加载。前者发 SELECT IN（适合一对多），后者发 JOIN（适合一对一/一对少） | 只说"用 eager loading"但说不出三种策略的区别 |
| Session 的生命周期？ | 你会不会在项目里搞出 Session 泄漏 | 创建→操作→commit/rollback→close。用上下文管理器。不要跨请求复用 Session | 认为 Session 是线程安全的（不是，每个线程要自己的 Session） |
| lazy loading 和 eager loading 区别？ | 你理不理解 ORM 的查询机制 | Lazy：访问时才查，默认行为。Eager：查询时一次加载。异步下 lazy 不可用 | 不知道异步下 lazy loading 会报错 |
| bulk 操作和普通 ORM 操作的区别？ | 你知道 ORM 的性能代价在哪 | ORM 有身份映射、变更追踪、自动取 ID 的开销。大批量用 `bulk_insert_mappings` 或 Core 的 insert | 以为 ORM 插入性能和原生 SQL 差不多 |
| SQLAlchemy 2.0 有什么变化？ | 你有没有跟进最新实践 | `select()` 统一查询、`Mapped` 类型声明、异步原生支持、`Query` 对象移除 | 没听说过 2.0 的变化，还在用 `session.query()` |
| 怎么做事务管理？ | 你能不能保证数据一致性 | commit 提交、rollback 回滚、`begin_nested()` 嵌套事务（SAVEPOINT）。用上下文管理器保证不出错 | 不知道嵌套事务怎么用 |
| `expire_on_commit=False` 什么时候用？ | 你有没有踩过这个坑 | commit 后对象属性过期，再访问会触发查询。异步模式下必须设 False，因为异步不支持隐式查询 | 不知道默认是 True，不理解为什么异步下必须改 |
| 连接池怎么配置？ | 你能不能支撑生产环境的并发 | `pool_size`（常驻连接数）、`max_overflow`（额外连接数）、`pool_recycle`（回收时间，防止数据库关掉空闲连接） | 不配置连接池参数，用默认值上线 |
