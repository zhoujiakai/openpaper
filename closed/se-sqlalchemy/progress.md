# SQLAlchemy ORM 深入掌握 — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-05-01
> 完成时间：2026-05-04

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现 | ✅ 已完成 | — |
| 2. 深度理解 | ✅ 已完成 | Section 5/5 |
| 3. 知识检验 | ✅ 已完成 | A4 默写通过，掌握度 82% |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: Lazy Loading vs Eager Loading | ✅ | 🟢 通过 |
| Section 2: 异步 SQLAlchemy | ✅ | 🟢 通过 |
| Section 3: 事务管理 | ✅ | 🟢 通过 |
| Section 4: 性能陷阱和优化 | ✅ | 🟢 通过 |
| Section 5: 2.0 迁移要点 | ✅ | 🟢 通过 |

## 已掌握的关键知识点

- Lazy loading 是"用到才查"，Eager loading 是"提前一次查完"
- Eager Loading 是总称，joinedload 和 selectinload 是两种具体实现
- joinedload 在数据库里 JOIN 拼表（有数据重复），selectinload 各查各的 Python 端组装（无重复）
- 一对一/一对少用 joinedload，一对多/数据量大用 selectinload
- 加载策略只作用于 relationship 定义的关系属性，普通属性不需要
- raiseload 访问就报错，逼你显式选择策略，防止无意识 N+1
- 异步下 lazy loading 物理上不可行（属性访问里没有 await），必须显式预加载
- 异步下 expire_on_commit 必须设 False（commit 后属性过期，异步下刷新不了）
- 变更追踪的前提：对象必须在 Session 管辖范围内，脱离了改了也白改
- ORM 插入的三个开销：身份映射、变更追踪、自动取自增 ID
- 大批量用 Core 直接插入，跳过 ORM 开销
- engine.begin() 自动事务管理，engine.connect() 手动管事务
- 嵌套事务用 begin_nested()，创建 SAVEPOINT

## 被纠正过的误区

1. selectinload 第二条 SQL 返回的是所有关联数据的总行数，不是主表行数
2. raiseload 不是 lazy loading 的变种，是完全不同的策略
3. Eager Loading / joinedload / selectinload 不是三个并列的东西，是总称和具体实现的关系
4. 异步下报错不是为了"保证查询效率"设计的，是物理上做不到
5. ORM 慢的原因是 Python 端的追踪开销，不是数据库访问次数
6. joinedload 的去重还原是 Python 端做的，不是数据库端
7. 身份映射是"记住并维护映射关系"，不是"验证"

## 需要复习的内容

- joinedload 关联多时为什么不好（重复数据浪费带宽和内存）
- raiseload 的完整工作机制（容易和 selectinload 混淆）
- ORM 插入三个开销的具体含义（身份映射、变更追踪、取自增 ID）
