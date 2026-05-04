# SQLAlchemy ORM 深入掌握 — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-05-01

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现 | ✅ 已完成 | — |
| 2. 深度理解 | ⏳ 进行中 | Section 1/5 |
| 3. 知识检验 | ⏳ 未开始 | — |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: Lazy Loading vs Eager Loading | ✅ 已完成 | 需加强：raiseload 机制、selectinload 行数计算 |
| Section 2: 异步 SQLAlchemy | ⏳ | — |
| Section 3: 事务管理 | ⏳ | — |
| Section 4: 性能陷阱和优化 | ⏳ | — |
| Section 5: 2.0 迁移要点 | ⏳ | — |

## 下次从哪里继续

从 Section 2（异步 SQLAlchemy）开始苏格拉底式精读。

## 已掌握的关键知识点

- Lazy loading 是"用到才查"，Eager loading 是"提前一次查完"
- Eager Loading 是总称，joinedload 和 selectinload 是两种具体实现
- joinedload 在数据库里 JOIN 拼表（有数据重复），selectinload 各查各的 Python 端组装（无重复）
- 一对一/一对少用 joinedload，一对多/数据量大用 selectinload
- 加载策略只作用于 relationship 定义的关系属性，普通属性不需要
- raiseload 访问就报错，逼你显式选择策略，防止无意识 N+1

## 被纠正过的误区

1. selectinload 第二条 SQL 返回的是所有关联数据的总行数（如 5000 行地址），不是主表行数
2. raiseload 不是 lazy loading 的变种，是完全不同的策略
3. Eager Loading / joinedload / selectinload 不是三个并列的东西，是总称和具体实现的关系

## 需要复习的内容

- raiseload 的完整工作机制（什么时候报错、怎么解除）
