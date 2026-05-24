# 消息队列（RabbitMQ / Kafka）— 个人笔记

> 基于精读和模拟题复习整理
> 记录时间：2026-04-30

---

## RabbitMQ 消息投递可靠性（模拟题遗忘，重点记忆）

消息经过三段路，每段都有丢的风险，所以每段都有保险：

| 环节 | 丢消息的风险 | 保险机制 |
|------|-------------|---------|
| Producer → Broker | 发了但 Broker 没收到 | **Publisher Confirm** — Broker 回 ACK |
| Broker 内部 | Broker 重启，内存里的消息没了 | **durable=True + delivery_mode=2** — 写到磁盘 |
| Broker → Consumer | Consumer 取了但处理时挂了 | **Consumer ACK** — 没收到 ACK 就重新入队 |

### 我容易忘的点

- **Publisher Confirm** = Producer 发消息后，Broker 收到会回 ACK。默认是"发了就不管"（fire-and-forget），开了 Confirm 才有回执
- **durable 和 delivery_mode 是两回事**：durable 保队列本身活着（仓库还在），delivery_mode=2 保消息写到磁盘（货还在仓库里）。两个必须同时开
- 三道防线全开也不等于"恰好一次"，可能重复消费，所以幂等消费是必需的

### 口诀

三段路 × 三道防线：Confirm（确认收到）+ 持久化（写到磁盘）+ ACK（确认处理完）

---

## RabbitMQ 集群（模拟题遗忘，重点记忆）

- **默认：队列只存在于创建它的那个节点上，不会复制**
- Exchange 的路由规则会同步到所有节点，但队列本身不会
- 那个节点挂了，队列里的消息就不可用
- 解决方案：**Quorum Queue**（仲裁队列），用 Raft 协议复制到多个节点
- 旧方案 Classic Mirrored Queue 已 deprecated

### 口诀

默认只同步路由规则，不同步队列数据。要高可用用 Quorum Queue

---

## Kafka 为什么快（模拟题只想到"磁盘"）

不是"用了磁盘"，是**怎么用磁盘**：

1. **顺序写磁盘** — 追加到文件末尾，600MB/s，比内存随机写还快
2. **零拷贝** — sendfile 系统调用，磁盘直接到网卡，不经过应用层
3. **Pull 模式** — Consumer 自己拉，Kafka 不用管谁快谁慢
4. **批量处理** — 攒一批一起发，一批一批写磁盘

代价：延迟比 RabbitMQ 高（毫秒级 vs 亚毫秒级）。吞吐和延迟是一对矛盾

---

## Kafka Consumer Group 再平衡（模拟题遗忘）

- Consumer 加入或离开 Group 时，重新分配 Partition，叫**再平衡**
- 再平衡期间：**所有消费者暂停消费**，这是消费端主要抖动来源
- 缓解：**CooperativeStickyAssignor**，只移动必须移动的 Partition，不全部停顿

---

## 消息顺序性（模拟题部分遗忘）

**RabbitMQ**：单队列 + **单消费者**才能严格保序。多消费者从同一队列取消息，处理速度不同会导致乱序

**Kafka**：单 Partition 内严格有序。用订单 ID 做 partition key，确保相关消息进同一 Partition

**共同点**：保序思路都是"钉到同一通道"。RabbitMQ 钉到同一 Queue，Kafka 钉到同一 Partition

---

## ISR（模拟题答对）

- In-Sync Replicas = 跟得上 Leader 的副本集合
- 只有 ISR 里的副本才能当 Leader，落后的当 Leader 会丢数据
- `min.insync.replicas` = 最少需要几个同步副本才算写入成功

## 幂等消费（模拟题答对）

1. 天然幂等操作（SET 而非 ADD）
2. 全局唯一 ID 去重
3. 乐观锁/版本号
4. 数据库唯一约束（补充）

## Kafka 存储

- 每个 Partition = 磁盘上一个目录，追加写日志 + 索引
- Follower 从 Leader 拉数据，被踢出 ISR 后继续拉，跟上就回来

## prefetch_count

- 消费者节流阀，控制同时推送的未确认消息数
- 设大（1000）→ 内存压力大，分布不均
- 设小（1）→ 吞吐低
- 一般 10-50

## 技术选型

- RabbitMQ = 消息代理：复杂路由、低延迟、任务队列、消息量不大
- Kafka = 事件流平台：高吞吐、消息回放、流处理、事件驱动
- RocketMQ = 介于两者之间：延迟消息最合适、事务消息成熟
