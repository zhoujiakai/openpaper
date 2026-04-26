# 消息队列（RabbitMQ / Kafka）— AI 笔记

> 来源：RabbitMQ 官方教程、RabbitMQ Reliability Guide、Confluent Kafka 官方文档
> 生成时间：2026-04-26
> 学习目标：面试准备，理解 RabbitMQ 和 Kafka 架构差异，掌握技术选型依据

---

## 锚点

想象两种快递系统。

**RabbitMQ 是智能分拣中心**——包裹送进来，分拣员看地址（routing key），决定扔进哪个筐（queue）。快递员（consumer）从筐里取走一件，分拣中心就把这件从系统里删掉。包裹不留底，送完即走。

**Kafka 是流水线传送带**——货物放上去，传送带不停，按顺序一直往前走。每个工位（consumer）自己看传送带上哪个位置是新的，自己决定什么时候取。传送带上的货物不会因为被看过就消失，保留一段时间或永远保留。想回头看？往回翻就行。

一个主动推给你，一个你自己来拉。一个送完即焚，一个永久留存。这一个区别，衍生出了后面所有的架构差异。

## 核心问题

为什么微服务之间不能直接 HTTP 调用？因为调用方必须等对方在线、必须等对方处理完、必须处理超时和重试。三个"必须"把两个服务死死绑在一起。消息队列干的事就是：**把你发的消息暂存起来，让接收方在自己方便的时候处理**。发的人不用等，收的人不怕丢。

## 核心概念

### 消息队列解决的基本问题

两个服务要通信，但不要求同时在线。A 发消息，B 随时来取。

举个具体的例子：用户下单后要发短信通知。下单服务不该被短信服务的快慢拖住——短信接口慢了 2 秒，用户就多等 2 秒。中间放个队列，下单服务扔一条消息就完事，短信服务按自己的节奏取出来发。

少了消息队列会怎样？每个服务间调用都变成强依赖，任何一个下游挂了，整条链路全卡住。

### RabbitMQ：Exchange → Queue → Consumer

回到"智能分拣中心"的比喻。

生产者不直接把消息放进队列。它把消息交给 **Exchange**（分拣台）。Exchange 根据规则（routing key + binding），决定消息进哪个 Queue。Consumer 从 Queue 里取消息。

为什么要这么绕？因为解耦。生产者不需要知道消息最终进了哪个队列，它只需要说"这条消息的 routing key 是 order.created"。至于哪个队列接收这条消息，是 Exchange 和 Binding 的事。

**Queue** 是真正存消息的地方。消息进队列后，等着被消费者取走。RabbitMQ 的队列有个核心特性：**默认情况下，消息被消费者确认后就会删除**。送完即走。

**Consumer ACK** 是可靠性的关键一环。消费者取走消息后，必须告诉 RabbitMQ "我处理完了"。如果消费者挂了没发 ACK，RabbitMQ 会把消息重新放回队列，交给另一个消费者。这保证了"消息至少被处理一次"。

### Exchange 的四种类型

Exchange 怎么决定消息进哪个 Queue？看类型：

**Direct Exchange**——精确匹配。routing key 是 `order.created`，就只发给绑定了这个 key 的队列。像快递柜：你的取件码是 A12，只有标了 A12 的柜子会开。

**Fanout Exchange**——广播。不管 routing key 是什么，发给所有绑定的队列。像小区广播：所有住户都收到。

**Topic Exchange**——模式匹配。routing key 支持通配符：`order.*` 匹配 `order.created` 和 `order.cancelled`，`order.#` 匹配 `order.created.paid`。像邮件分类规则：所有以"order"开头的邮件放进同一个文件夹。

**Headers Exchange**——匹配消息头而不是 routing key。实际用得少，知道有这个东西就行。

**各自适合什么场景？**

| 类型 | 场景 |
|------|------|
| Direct | 点对点，一个消息只发给一个队列。如：订单服务只通知库存服务 |
| Fanout | 广播，一个消息发给所有相关方。如：用户注册后同时通知短信、邮件、积分三个服务 |
| Topic | 按主题分类，灵活订阅。如：支付系统发布 `payment.success.alipay`，不同下游按需订阅 |

### prefetch_count：消费者的节流阀

Consumer 从 Queue 取消息，默认情况下 RabbitMQ 会**一股脑推过来**。如果你的消费者处理一条消息要 100ms，RabbitMQ 推了 1000 条过来，消费者内存就爆了。

**prefetch_count** 就是告诉 RabbitMQ："同时推给我的未确认消息，最多 N 条。"比如设成 10，消费者手上有 10 条未处理完的消息时，RabbitMQ 就不再推了，等消费者 ACK 一条，再推一条。

设大了（比如 1000）——消费者内存压力大，消息分布不均匀（快的消费者拿太多，慢的拿不到）。

设小了（比如 1）——每处理完一条才能拿下一条，吞吐量低，网络开销大。

一般设 **10-50**，在吞吐和公平之间取平衡。

### Kafka：Topic → Partition → Consumer Group

现在切到"传送带"的世界。

**Topic** 是逻辑分类，比如 `order-events`。一个 Topic 被切分成多个 **Partition**（传送带的并行轨道）。每条消息追加到某个 Partition 的末尾，不可修改。

Partition 是 Kafka 并行的核心单位。一个 Topic 有 3 个 Partition，就意味着 3 条传送带同时运转。消息被均匀分配到各 Partition（按 key hash 或轮询）。

**Consumer Group** 是一组消费者，共同消费一个 Topic。规则：**一个 Partition 同一时刻只能被 Group 内的一个 Consumer 消费**。所以如果一个 Topic 有 3 个 Partition，Consumer Group 里有 3 个 Consumer，恰好一人一条传送带。如果 Consumer 比 Partition 多，多出来的消费者闲着。

为什么要这么设计？**保证消费顺序**。一个 Partition 内的消息是严格有序的，因为只有一个消费者在处理它。不用加锁，不用排队，天然有序。

### Offset：消费者的书签

Consumer 不需要 RabbitMQ 那样的 ACK 机制。它自己维护一个 **offset**（偏移量），记录"我读到第几条了"。

Consumer 处理完一批消息，提交 offset。下次重启，从上次提交的位置继续读。想重新处理？把 offset 往回拨就行。这就是 Kafka 天然支持**消息回放**的原因。

RabbitMQ 做不到这一点——消息被确认就删了，想再看？没有了。

### Kafka 为什么吞吐量比 RabbitMQ 高

根本原因：**Kafka 是顺序写磁盘 + 零拷贝**。

1. **顺序写**：Kafka 把消息追加到日志文件末尾。磁盘顺序写速度极快（600MB/s），甚至比内存随机写还快。RabbitMQ 的消息要经过 Exchange 路由、入队、确认等复杂流程，每一步都是随机 IO。

2. **零拷贝（Zero-copy）**：Kafka 用 `sendfile` 系统调用，数据从磁盘直接到网卡，不经过用户态内存。RabbitMQ 要把消息从内核态拷到用户态（Broker 处理），再拷回内核态（发送给 Consumer），两次拷贝。

3. **Pull 模式**：Consumer 自己来拉，Kafka 不用管每个消费者快慢不同。RabbitMQ 是 Push 模式，要为每个消费者维护推送状态、处理背压（prefetch_count），开销大。

4. **批量处理**：Kafka 天然支持批量发送和批量压缩。Producer 把一批消息攒在一起发，Broker 一批一批写磁盘。RabbitMQ 也能批量，但不是默认模式。

**代价**：Kafka 的延迟比 RabbitMQ 高。RabbitMQ 可以做到亚毫秒级延迟（直接推给你），Kafka 通常在毫秒到十毫秒级（攒批 + pull）。吞吐和延迟是一对矛盾。

### 幂等消费：为什么重要，怎么做

**什么是幂等？** 同一条消息被处理多次，结果和只处理一次一样。`f(f(x)) = f(x)`。

为什么在消息队列中特别重要？因为消息队列通常保证"至少一次投递"（at-least-once）。网络抖动、Consumer 重启、ACK 丢失，都可能导致同一条消息被投递两次。

如果你用消息里的金额给账户加余额，同一条消息处理两次，余额就加了两次。这就是没有幂等性的后果。

**实现方式：**

1. **唯一 ID 去重**：每条消息带一个全局唯一 ID（如 `message_id`）。消费者处理前先查这张消息有没有处理过（存 Redis 或数据库）。处理完，把 ID 存下来。下次再遇到同一个 ID，跳过。

   优点：实现简单。缺点：需要额外存储，ID 过期策略要设计。

2. **数据库唯一约束**：把业务操作和去重放在同一个数据库事务里。比如用 `message_id` 做唯一索引，重复插入直接失败，事务回滚。

   优点：天然事务保证。缺点：只适合用数据库的场景。

3. **业务幂等**：把操作设计成天然幂等的。比如"将账户余额设为 100"是幂等的（执行多少次都是 100），"给账户加 50"不是（执行两次变成加 100）。

   优点：不需要额外组件。缺点：不是所有操作都能设计成幂等。

4. **乐观锁/版本号**：更新时带版本号，`UPDATE account SET balance = balance + 50, version = version + 1 WHERE id = 1 AND version = 10`。版本号不对就说明重复了。

   优点：不需要额外存储去重表。缺点：要改业务表结构。

## 逐节详解

### Section 1: RabbitMQ 消息投递可靠性

消息从 Producer 到 Consumer，经过三步：Producer → Broker（RabbitMQ）→ Consumer。每一步都可能丢消息，每一步都有对应的保障机制。

**Producer 到 Broker：Publisher Confirm**

Producer 发消息给 RabbitMQ，默认是"发了就不管了"（fire-and-forget）。开启 Publisher Confirm 后，RabbitMQ 收到消息并持久化后会回一个 ACK 给 Producer。Producer 收不到 ACK 就知道消息丢了，可以重发。

**Broker 内部：队列持久化**

消息进了 RabbitMQ，但 RabbitMQ 重启了怎么办？两个设置要同时开启：
1. Queue 声明为 `durable=True`（队列本身持久化）
2. 消息设置 `delivery_mode=2`（消息内容持久化）

只开一个不够。队列不持久化，重启后队列都没了，消息往哪放？消息不持久化，队列在但消息没了。

**Broker 到 Consumer：Consumer ACK**

Consumer 处理完消息，发 ACK。如果 Consumer 挂了（连接断开或 channel 关闭），RabbitMQ 没收到 ACK，会把消息重新入队。

三道防线全开，消息才能做到"不丢"。但注意，这不等于"恰好一次"——Producer 重发可能导致重复，Consumer 重启也可能重复消费。所以幂等消费是必需的。

### Section 2: RabbitMQ 集群与高可用

单节点 RabbitMQ 挂了怎么办？加集群。但 RabbitMQ 集群有个容易混淆的点：**默认情况下，队列只存在于一个节点上**。

什么意思？Exchange 的元数据（路由规则）会同步到所有节点——你在任意节点发消息都能到达 Exchange。但队列本身不会复制。如果队列所在的节点挂了，这个队列里的消息就不可用了，直到节点恢复。

怎么解决？**Quorum Queue**（仲裁队列）。RabbitMQ 3.8+ 引入，用 Raft 协议把队列数据复制到多个节点。一个节点挂了，其他节点有完整副本，消费者照常取消息。

之前的方案是 **Classic Mirrored Queue**（镜像队列），但已经被官方标记为deprecated，新项目用 Quorum Queue。

### Section 3: Kafka 存储与副本机制

**日志段（Log Segment）**：每个 Partition 在磁盘上是一个目录，里面是一组日志段文件。消息追加写，写到一定大小（默认 1GB）就切一个新文件。每个日志段有一个索引文件，支持按 offset 快速定位。

**副本（Replication）**：每个 Partition 有多个副本分布在不同 Broker 上。一个是 **Leader**，其余是 **Follower**。所有读写都走 Leader，Follower 只是被动从 Leader 拉数据保持同步。

如果 Leader 挂了，Controller（Kafka 集群管理者）会从 ISR（In-Sync Replicas，与 Leader 保持同步的副本集合）中选一个 Follower 提升为 Leader。

**ISR 的意义**：只有跟得上 Leader 的副本才有资格被选为 Leader。如果你允许落后太多的副本当 Leader，会丢数据。配置 `min.insync.replicas` 可以设置最少需要几个同步副本才能写入——设成 2，意味着至少 Leader 和一个 Follower 都确认了才算写入成功。

### Section 4: Kafka Consumer Group 再平衡

Consumer Group 里，Partition 和 Consumer 的对应关系不是固定的。Consumer 加入或离开 Group 时，会触发**再平衡（Rebalance）**，重新分配 Partition。

举个例子：3 个 Partition，3 个 Consumer，一人一个。Consumer 2 挂了，再平衡把 Consumer 2 的 Partition 分给 Consumer 1 或 3。

再平衡期间，所有消费者暂停消费。这是 Kafka 消费端的主要抖动来源。频繁再平衡 = 频繁停顿。

**CooperativeStickyAssignor**（Kafka 2.4+）可以减少再平衡影响——它尽量保持现有分配不变，只移动必须移动的 Partition，不用全部停顿。

**Consumer 的心跳机制**：Consumer 定期向 Group Coordinator 发心跳。心跳超时（`session.timeout.ms`）没收到，就认为 Consumer 挂了，触发再平衡。心跳间隔（`heartbeat.interval.ms`）一般设为 session timeout 的 1/3。

### Section 5: 消息顺序性

面试常问：消息队列能保证消息顺序吗？答案是"看情况"。

**RabbitMQ**：单个队列内的消息，按投递顺序发给消费者。如果只有一个消费者，严格有序。如果有多个消费者，不同消费者处理速度不同，消息的实际完成顺序可能乱掉。比如消息 1、2、3 分别发给 Consumer A、B、C，C 可能先处理完 3，A 还在处理 1。

**Kafka**：单个 Partition 内严格有序。但不同 Partition 之间的消息没有顺序保证。所以如果你需要"同一个订单的所有事件按顺序处理"，就要确保这个订单的事件都发到同一个 Partition——用订单 ID 做 partition key。

### Section 6: 技术选型——RabbitMQ 还是 Kafka

核心判断：你要的是**消息代理**（Message Broker）还是**事件流平台**（Event Streaming Platform）？

**选 RabbitMQ 的场景：**
- 需要复杂的消息路由（多种 Exchange 类型）
- 消息消费完就删，不需要保留历史
- 对延迟敏感（亚毫秒级）
- 任务队列模式：消费者处理完就 ACK，处理失败重新入队
- 消息量不大（每秒几千到几万条）

**选 Kafka 的场景：**
- 高吞吐（每秒几十万到上百万条）
- 需要消息回放（重新消费历史数据）
- 事件驱动架构，多个消费者独立消费同一个 Topic
- 大数据和流处理（对接 Flink、Spark 等生态）
- 需要严格的消息顺序（Partition 内有序）

**RocketMQ 在哪？** 它介于两者之间。比 RabbitMQ 吞吐高，比 Kafka 延迟低。有事务消息、延迟消息等高级特性。阿里系生态完善。国内公司用得多，国际社区不如 Kafka 活跃。

## 与其他方法的对比

| 维度 | RabbitMQ | Kafka | RocketMQ |
|------|----------|-------|----------|
| 模型 | 消息代理 | 事件流平台 | 消息代理 + 流 |
| 消息保留 | 消费完即删 | 按时间/大小保留 | 按时间保留 |
| 消费模式 | Push（推） | Pull（拉） | Push + Pull |
| 吞吐量 | 1-5 万/秒 | 100 万+/秒 | 10-20 万/秒 |
| 延迟 | 亚毫秒 | 毫秒级 | 毫秒级 |
| 路由 | Exchange（4种） | Topic + Partition | Topic + Queue |
| 消息回放 | 不支持 | 天然支持 | 支持 |
| 顺序保证 | 单队列有序 | 单 Partition 有序 | 单 Queue 有序 |
| 事务消息 | 不支持 | 支持（Exactly-once） | 支持（更成熟） |
| 延迟消息 | 插件支持 | 不原生支持 | 原生支持 |
| 协议 | AMQP | 自定义协议 | 自定义协议 |
| 适用场景 | 复杂路由、任务队列 | 高吞吐、流处理、事件驱动 | 电商、金融、事务消息 |

## 面试高频考点

| 考点 | 他真正想知道的 | 回答要点 | 常见错误 |
|------|---------------|----------|----------|
| RabbitMQ Exchange 类型 | 你理不理解消息路由的灵活性 | 说出 direct/fanout/topic 三种及各自场景，用具体例子 | 只背定义不说场景 |
| prefetch_count | 你知不知道消费者可能被压垮 | 解释推模式的背压问题，说清楚设大设小的影响 | 不知道这是干什么的 |
| Kafka 为什么快 | 你是只背结论还是理解原理 | 顺序写磁盘 + 零拷贝 + 批量处理 + Pull 模式 | 只说"因为 Kafka 用磁盘" |
| Kafka 的 Partition 和 Consumer Group | 你懂不懂 Kafka 并行消费的模型 | 说清楚"一个 Partition 只能被一个 Consumer 消费"这条规则，解释为什么这样设计 | 不知道 Consumer Group 内消费者数不能超过 Partition 数 |
| RabbitMQ 和 Kafka 怎么选 | 你有没有实际选型的判断力 | 先说区别（消息代理 vs 事件流），再说场景匹配 | 只说"Kafka 更好"没有场景分析 |
| 幂等消费 | 你做过生产级的消费者吗 | 说至少两种实现方式，强调"至少一次投递"是前提 | 不知道消息会重复投递 |
| 消息丢了怎么办 | 你处理过消息可靠性问题吗 | RabbitMQ 三道防线（Publisher Confirm + 持久化 + Consumer ACK），Kafka 副本 + ISR + min.insync.replicas | 只说了其中一个环节 |
| Kafka 再平衡 | 你踩过 Consumer Group 的坑吗 | 解释触发原因和影响（消费暂停），提 CooperativeStickyAssignor | 不知道再平衡会导致消费暂停 |
