# SQLAlchemy ORM — 个人笔记

> 学习时间：2026-05-04
> 阶段：Section 1 精读完成，待进 Section 2

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
