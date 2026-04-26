# 消息队列 — 学习进度

> 学习方式：知识精通三阶段工作流
> 记录时间：2026-04-26

---

## 当前进度

| 阶段 | 状态 | 进度 |
|------|------|------|
| 1. 内容发现 | ✅ 已完成 | — |
| 2. 深度理解 | ✅ 已完成 | Section 6/6，精读 + 苏格拉底问答全部完成 |
| 3. 知识检验 | ⏳ 未开始 | 下一步：模拟题测试（2.3） |

### 逐节进度

| Section | 状态 | 掌握程度 |
|---------|------|---------|
| Section 1: RabbitMQ 消息投递可靠性 | ✅ | durable+delivery_mode ✅，ISR 原理 ✅，"至少一次"与幂等关系 ✅ |
| Section 2: RabbitMQ 集群与高可用 | ✅ | 默认不复制 ✅，Quorum Queue + Raft 过半确认 ✅，3副本容1台 ✅ |
| Section 3: Kafka 存储与副本机制 | ✅ | 追加写日志+索引 ✅，Follower vs Consumer 拉数据区别 ✅，ISR 踢出后恢复 ✅ |
| Section 4: Kafka Consumer Group 再平衡 | ✅ | 再平衡触发+代价 ✅，CooperativeStickyAssignor ✅，心跳 vs poll 间隔区分 ✅，假死处理方案 ✅ |
| Section 5: 消息顺序性 | ✅ | 单队列/单Partition有序 ✅，保序思路一致（钉到同一通道） ✅ |
| Section 6: 技术选型 | ✅ | 选型依据 ✅，延迟消息场景（RocketMQ 最合适） ✅，延迟消息业务实现方式 ✅ |

## 下次从哪里继续

阶段 2 精读已完成，下一步：生成模拟题测试（2.3）。

## 已掌握的关键知识点

- RabbitMQ 三道防线：Publisher Confirm + 持久化（durable + delivery_mode=2）+ Consumer ACK
- Kafka 不丢消息：多副本 + ISR + min.insync.replicas
- ISR 的意义：只有跟得上 Leader 的副本才有资格接班，否则落后副本当 Leader 会丢数据
- Quorum Queue 用 Raft 协议，过半数确认，副本数决定容忍度（3副本容1台）
- Kafka 存储 = 追加写日志 + 索引，Follower 被踢出 ISR 后继续拉数据，跟上就回来
- 再平衡：所有消费者暂停消费，用 CooperativeStickyAssignor 缓解
- 心跳 vs poll 间隔：两套独立机制，处理慢导致的是 max.poll.interval.ms 超时
- 消息顺序：RabbitMQ 钉到同一 Queue，Kafka 钉到同一 Partition，思路一致
- 技术选型：消息代理 vs 事件流平台，延迟消息场景 RocketMQ 最合适
- 延迟消息业务实现：数据库轮询（朴素）/ 延迟消息（优雅）/ Redis 过期通知（不可靠）
- Kafka 为什么快：顺序写磁盘 + 零拷贝 + 批量处理 + Pull 模式
- 幂等消费：唯一 ID 去重 / 数据库唯一约束 / 业务幂等 / 乐观锁版本号
- Exchange 四种类型：Direct（精确）、Fanout（广播）、Topic（模式匹配）、Headers（少用）
- prefetch_count：消费者节流阀，一般设 10-50

## 被纠正过的误区

- ❌ "处理太慢导致心跳来不及发"→ ✅ 新版客户端心跳由后台线程发送，不受消息处理影响。处理慢导致的是 max.poll.interval.ms 超时，不是心跳超时。两套机制独立：心跳检测进程存活，poll 间隔检测消费是否正常。

## 需要复习的内容

（暂无）
