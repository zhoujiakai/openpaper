# SQLAlchemy ORM — 个人笔记

> 学习时间：2026-05-04
> 阶段：A4 默写完成，掌握度 82%

---

## Section 1: Lazy Loading vs Eager Loading

### 加载策略全景

```
加载策略
├── Lazy Loading  — 用到才查（默认）
├── Eager Loading — 提前一次查完
│   ├── joinedload   — 在数据库里 JOIN 拼表，一条 SQL
│   ├── selectinload — 各查各的，Python 端组装，两条 SQL
│   └── subqueryload — 子查询方式，基本不用了
└── Raiseload     — 访问就报错，逼你显式选择策略
```

Eager Loading 是"提前把关联数据一起查出来"的总称，joinedload 和 selectinload 是实现这个思路的两种具体做法。

### joinedload vs selectinload 的区别

- joinedload：在数据库里 JOIN 拼表，结果是一张宽表，用户信息会重复（一个用户 50 个地址，用户数据就重复 50 次）
- selectinload：分两条 SQL，各查各的，Python 端组装，没有数据重复

场景：100 个用户每个 50 个地址
- joinedload：1 条 SQL，但返回 5000 行宽表，用户信息大量重复
- selectinload：2 条 SQL，第 1 条返回 100 行用户，第 2 条返回 5000 行地址，干净无重复

**决策规则：一对一、一对少用 joinedload；一对多、数据量大用 selectinload。**

### 这些策略只作用于关系属性

普通属性（name、email、id）就在本表里，查的时候已经带出来了，不需要加载策略。只有 `relationship()` 定义的跨表关系属性（addresses、orders）才需要选择加载策略。

### raiseload 的理解

raiseload 不是 lazy loading，它和 lazy loading 是完全不同的策略。lazy 是"用到才查"，raiseload 是"用到就报错"。

raiseload 不会让你完全不能查关联数据。它堵死的是"什么都不写就访问 `user.addresses`"这个默认行为。你只要在查询时用 `.options(selectinload(User.addresses))` 或 `.options(joinedload(User.addresses))` 显式声明策略，就正常工作。

目的：防止无意识触发 lazy loading 导致 N+1。

### 曾模糊/答错的地方

1. **selectinload 的返回行数**：我一开始以为 selectinload 第二条 SQL 返回 100 行，实际是 5000 行（100 用户 × 50 地址 = 5000 条地址记录）
2. **raiseload 和 lazy loading 的关系**：一开始把 raiseload 当成了 lazy loading 的某种限制，实际它们是并列的不同策略
3. **Eager Loading、joinedload、selectinload 的关系**：一开始以为是三个并列的东西，实际 Eager Loading 是总称，后面两个是实现方式

---

## Section 2: 异步 SQLAlchemy

### 核心：异步下不能偷偷发 SQL

异步模式下所有数据库操作必须显式 `await`。lazy loading 机制是"访问属性时偷偷发 SQL"，但属性访问里没有 await 的位置，所以物理上不可行，直接报错。

两个必须做的事：
1. 关系属性必须显式预加载（selectinload / joinedload）
2. `expire_on_commit` 必须设 False（commit 后属性过期，再访问需要刷新，异步下刷新不了）

预加载的原理：在 `await session.execute()` 这一步就把关联数据查好了，后面访问 `user.addresses` 只是读 Python 内存，不涉及 SQL。

异步下的查询思路：不是"查全部再按需访问"，而是"先想好要什么，精确地查"。

### 曾模糊的地方

1. **异步下报错的目的**：我以为是刻意设计来保证查询效率的，实际原因是物理上做不到 lazy loading（属性访问里插不进 await），报错不是"好心提醒"，是"干不了"。但结果确实更好——逼你写出更精确的查询。

---

## Section 3: 事务管理

### 嵌套事务（SAVEPOINT）

`begin_nested()` 在数据库层面创建 SAVEPOINT，相当于存档点。回滚只回到那个点，不影响之前的操作。

适用场景：大事务里有"可能失败的子操作"，失败了只回滚子操作，关键数据保留。

实际例子（鼎鸿电子安全监督系统）：写入检测结果 + 写入告警记录 + 触发设备联动。检测结果是关键数据必须保留，联动可能失败，用 SAVEPOINT 隔离失败部分。

---

## Section 4: 性能陷阱

### 批量插入的三种方式

| 方式 | 速度 | 原理 |
|------|------|------|
| ORM 逐条 add | 最慢（10万行 ~6.9秒） | 每行都做身份映射、变更追踪、取自增 ID |
| bulk_insert_mappings | 中等（~0.47秒） | 跳过部分 ORM 开销 |
| Core 直接插入 | 最快（~0.21秒） | 完全跳过 ORM 层，直接操作表 |

CV 检测结果批量写入场景：攒一批，用 Core 直接插入，跳过 ORM 追踪开销。

### 身份映射和变更追踪

**身份映射**：Session 维护一个 `{id: 对象}` 的字典，同一个 ID 查两次，拿到的是同一个 Python 对象，不是两个副本。避免内存里出现不一致的数据。

**变更追踪**：在 Session 管辖范围内修改对象属性，Session 会记住改了什么，`commit()` 时自动生成对应的 UPDATE SQL。

关键前提：对象必须在 Session 的管辖范围内。Session 关了或对象脱离了 Session，改属性不会影响数据库。

### Core 直接插入也支持异步

Core 不是只能同步的。跳过的是 ORM 的追踪开销，不是异步能力。异步下加 `await` 用异步引擎就行。

### engine.begin() vs engine.connect()

- `engine.begin()`：自动事务管理，成功自动 commit，报错自动 rollback
- `engine.connect()`：只拿连接，手动管事务

大部分情况用 `begin()` 就够。

### 连接池配置

```python
engine = create_engine(url,
    pool_size=10,        # 常驻连接数
    max_overflow=20,     # 高峰时额外开 20 个
    pool_recycle=1800,   # 30 分钟回收，防止数据库关掉空闲连接
    pool_timeout=30,     # 等连接最多 30 秒
)
```

### 曾模糊/答错的地方

1. **Core 直接插入的方法名**：知道要用批量插入、知道要跳过 ORM 开销，但说不出具体方法（`__table__.insert()`）
2. **Core 是否支持异步**：一开始以为 Core 只能同步，实际 Core 和异步是两个维度，Core 跳过 ORM 追踪，异步跳过阻塞 IO，互不冲突
3. **ORM 慢的原因**：一开始以为是"访问数据库次数多"，实际主要是 Python 端的开销（身份映射、变更追踪、自动取自增 ID），数据库访问次数可以通过攒批 commit 控制
4. **joinedload 的去重在哪里做**：以为是数据库端做聚合，实际数据库只负责 JOIN 产生平铺宽表，去重还原成 ORM 对象是 Python 端做的

### eager loading 的代价

selectinload / joinedload 解决了查询次数的问题，但会把所有关联数据加载到内存。100 万用户 × 100 个订单 = 1 亿对象全在内存里。

如果只要统计数量，不要用 eager loading 加载全部对象，直接用 SQL 的 `COUNT` + `GROUP BY`，数据库端算好，不加载对象：

```python
stmt = select(User.name, func.count(Order.id)) \
    .join(Order, User.id == Order.user_id) \
    .group_by(User.id)
```

原则：eager loading 用于"你需要关联对象本身"的场景；只要聚合统计，直接用 SQL。

---

## Section 5: 2.0 迁移要点

核心变化：从"ORM 自己搞一套"变成"ORM 和 Core 用同一套 API"。

| 1.x | 2.0 | 变化 |
|-----|-----|------|
| `session.query(User).filter(...)` | `select(User).where(...)` | select() 统一查询 |
| `Column(Integer, primary_key=True)` | `Mapped[int] = mapped_column(primary_key=True)` | 类型安全 |
| `Query.all()` / `Query.first()` | `scalars().all()` / `scalar_one_or_none()` | 两步走：execute 再提取 |

没有 1.x 旧习惯，直接用 2.0。

---

## A4 默写：薄弱点记录

### 1. joinedload 关联多时为什么不好

100 个用户每个 100 个地址，joinedload 的 JOIN 结果是 1 万行，每个用户信息重复 100 遍。这些重复数据要从数据库传到 Python 端，浪费网络带宽和内存，SQLAlchemy 还要在 Python 端去重还原。selectinload 各查各的，没有重复。

### 2. ORM 插入的三个开销

1. **身份映射**：Session 记住对象 ID，维护 `{id: 对象}` 映射，保证同一 ID 只对应一个 Python 对象
2. **变更追踪**：跟踪属性变化，算出最终要发哪些 SQL
3. **自动取自增 ID**：插入后查回主键，填充到对象上

第一个容易记成"验证"，实际是"记住并维护映射关系"。

### 3. raiseload

模型上设 `lazy="raise"`，访问关系属性直接报错。不是延迟查，不是预加载，就是炸。目的是堵死后门，你不显式声明加载策略就不让访问，防止无意识 N+1。解除方式：查询时加 `.options(selectinload(...))` 或 `.options(joinedload(...))`。

容易和 selectinload 混淆，raiseload 和 lazy loading 是并列的不同策略，不是 eager loading 的一种。
