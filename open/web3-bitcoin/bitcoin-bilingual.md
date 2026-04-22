# Bitcoin: A Peer-to-Peer Electronic Cash System
# 比特币：一种点对点的电子现金系统

**Satoshi Nakamoto**
**satoshin@gmx.com**
**www.bitcoin.org**

---

## Abstract / 摘要


A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without going through a financial institution. Digital signatures provide part of the solution, but the main benefits are lost if a trusted third party is still required to prevent double-spending. We propose a solution to the double-spending problem using a peer-to-peer network. The network timestamps transactions by hashing them into an ongoing chain of hash-based proof-of-work, forming a record that cannot be changed without redoing the proof-of-work. The longest chain not only serves as proof of the sequence of events witnessed, but proof that it came from the largest pool of CPU power. As long as a majority of CPU power is controlled by nodes that are not cooperating to attack the network, they'll generate the longest chain and outpace attackers. The network itself requires minimal structure. Messages are broadcast on a best effort basis, and nodes can leave and rejoin the network at will, accepting the longest proof-of-work chain as proof of what happened while they were gone.


我们要提出一种纯点对点的电子现金系统，让在线支付可以直接从一方发送给另一方，无需经过任何金融机构。数字签名虽然解决了一部分问题，但若仍需依赖可信第三方来防止双花，就失去了主要价值。本文利用点对点网络来解决双花问题。网络将交易哈希进一条不断延伸的工作量证明链，从而为交易打上时间戳，形成一条无法篡改的记录——除非重新完成工作量证明。最长的链不仅见证了事件发生的顺序，也证明它源自最大的算力池。只要大多数算力掌握在不合谋攻击网络的节点手中，它们就会生成最长的链，从而超越攻击者。网络本身结构极简：消息尽力广播，节点可随时离开或重新加入，并以最长的工作量证明链作为离线期间发生事件的证明。

---

## 1. Introduction / 引言


Commerce on the Internet has come to rely almost exclusively on financial institutions serving as trusted third parties to process electronic payments. Although the system works well enough for most transactions, it still suffers from the inherent weaknesses of the trust based model. Completely non-reversible transactions are not really possible, since financial institutions cannot avoid mediating disputes. The cost of mediation increases transaction costs, limiting the minimum practical transaction size and cutting off the possibility for small casual transactions, and there is a broader cost in the loss of the ability to make non-reversible payments for non-reversible services. With the possibility of reversal, the need for trust spreads. Merchants must be wary of their customers, hassling them for more information than they would otherwise need. A certain percentage of fraud is accepted as unavoidable. These costs and payment uncertainties can be avoided in person by using physical currency, but no mechanism exists to make payments over a communications channel without a trusted party.


互联网上的商业活动几乎完全依赖金融机构作为可信第三方来处理电子支付。这套系统对大部分交易来说运行良好，但信任模型固有的弱点始终存在。交易不可能做到真正完全不可撤销，因为金融机构难免要介入纠纷调解。调解成本推高了交易成本，限制了最小可行交易金额，让小额日常交易难以进行。更广泛的代价在于，对于那些一旦完成就无法撤销的服务，也无法实现真正不可撤销的支付。由于存在撤销的可能，信任的需求便四处蔓延。商家不得不提防客户，索要比本来更多的信息。一定比例的欺诈也被视为无法避免。当面使用现金可以避免这些成本和不确定性，但在通信渠道上进行支付，若没有可信方参与，目前还没有相应的机制。


What is needed is an electronic payment system based on cryptographic proof instead of trust, allowing any two willing parties to transact directly with each other without the need for a trusted third party. Transactions that are computationally impractical to reverse would protect sellers from fraud, and routine escrow mechanisms could easily be implemented to protect buyers. In this paper, we propose a solution to the double-spending problem using a peer-to-peer distributed timestamp server to generate computational proof of the chronological order of transactions. The system is secure as long as honest nodes collectively control more CPU power than any cooperating group of attacker nodes.


我们需要的是一种基于密码学证明而非信任的电子支付系统，让任何两个自愿方都能直接交易，无需可信第三方介入。如果交易在计算上几乎不可能被撤销，卖家就能免受欺诈；而常规的托管机制也可以轻松保护买家。本文提出用点对点的分布式时间戳服务器来解决双花问题，生成交易时间顺序的计算证明。只要诚实节点集体控制的算力超过任何合谋攻击者群体，系统就是安全的。

---

## 2. Transactions / 交易


We define an electronic coin as a chain of digital signatures. Each owner transfers the coin to the next by digitally signing a hash of the previous transaction and the public key of the next owner and adding these to the end of the coin. A payee can verify the signatures to verify the chain of ownership.


我们把电子币定义为一条数字签名链。每个所有者把币转给下一个人时，要对上一笔交易的哈希和下一任所有者的公钥进行数字签名，并将签名附加到币的末尾。收款人可以验证这些签名，从而确认所有权的传递链。


The problem of course is the payee can't verify that one of the owners did not double-spend the coin. A common solution is to introduce a trusted central authority, or mint, that checks every transaction for double spending. After each transaction, the coin must be returned to the mint to issue a new coin, and only coins issued directly from the mint are trusted not to be double-spent. The problem with this solution is that the fate of the entire money system depends on the company running the mint, with every transaction having to go through them, just like a bank.


问题在于，收款人无法确认某个所有者是否已经双花了这枚币。常见的解决方案是引入一个可信的中心机构（铸币厂）来检查每笔交易是否存在双花。每笔交易完成后，币必须返回铸币厂来发行新币，只有直接从铸币厂发行的币才被信任没有双花。这套方案的问题在于，整个货币系统的命运掌握在经营铸币厂的公司手里，每笔交易都必须经他们处理，就像银行一样。


We need a way for the payee to know that the previous owners did not sign any earlier transactions. For our purposes, the earliest transaction is the one that counts, so we don't care about later attempts to double-spend. The only way to confirm the absence of a transaction is to be aware of all transactions. In the mint based model, the mint was aware of all transactions and decided which arrived first. To accomplish this without a trusted party, transactions must be publicly announced [1], and we need a system for participants to agree on a single history of the order in which they were received. The payee needs proof that at the time of each transaction, the majority of nodes agreed it was the first received.


我们需要让收款人能够确认，之前的所有者并没有签署任何更早的交易。对我们来说，只有最早的那笔交易才算数，所以不在乎后续的双花尝试。要确认一笔交易不存在，唯一的办法就是掌握所有交易的信息。在铸币厂模型中，铸币厂知道所有交易，并决定哪笔先到。要在没有可信方的情况下实现这一点，交易必须公开广播 [1]，并且我们需要一个系统，让参与者对接收到的交易顺序达成一致。收款人需要证明，在每笔交易发生时，大多数节点都认可它是先被接收到的。

---

## 3. Timestamp Server / 时间戳服务器


The solution we propose begins with a timestamp server. A timestamp server works by taking a hash of a block of items to be timestamped and widely publishing the hash, such as in a newspaper or Usenet post [2-5]. The timestamp proves that the data must have existed at that time, obviously, in order to get into the hash. Each timestamp includes the previous timestamp in its hash, forming a chain, with each additional timestamp reinforcing the ones before it.


我们要提出的解决方案从时间戳服务器开始。时间戳服务器的工作方式是：取一组要打时间戳的数据，计算其哈希，然后广泛发布这个哈希——比如发布在报纸或 Usenet 帖子上 [2-5]。时间戳证明了这些数据在那个时间点必然已经存在，否则不可能被算进哈希里。每个时间戳的哈希中都包含前一个时间戳，从而形成一条链，每增加一个时间戳就强化了前面的所有时间戳。

---

## 4. Proof-of-Work / 工作量证明


To implement a distributed timestamp server on a peer-to-peer basis, we will need to use a proof-of-work system similar to Adam Back's Hashcash [6], rather than newspaper or Usenet posts. The proof-of-work involves scanning for a value that when hashed, such as with SHA-256, the hash begins with a number of zero bits. The average work required is exponential in the number of zero bits required and can be verified by executing a single hash.


要在点对点基础上实现分布式时间戳服务器，我们需要使用类似 Adam Back 的 Hashcash [6] 那样的工作量证明系统，而不是报纸或 Usenet 帖子。工作量证明的过程是：不断寻找一个数值，使得哈希结果（比如用 SHA-256）的开头有若干个零位。所需的工作量平均而言与零位数量呈指数关系，但验证只需执行一次哈希即可。


For our timestamp network, we implement the proof-of-work by incrementing a nonce in the block until a value is found that gives the block's hash the required zero bits. Once the CPU effort has been expended to make it satisfy the proof-of-work, the block cannot be changed without redoing the work. As later blocks are chained after it, the work to change the block would include redoing all the blocks after it.


在我们的时间戳网络中，我们通过不断递增区块中的随机数来实现工作量证明，直到找到让区块哈希具有所需零位的数值。一旦消耗了算力使区块满足工作量证明，想要修改区块就必须重做一遍工作。由于后续区块都链接在这个区块后面，要修改这个区块，就得重做它后面的所有区块。


The proof-of-work also solves the problem of determining representation in majority decision making. If the majority were based on one-IP-address-one-vote, it could be subverted by anyone able to allocate many IPs. Proof-of-work is essentially one-CPU-one-vote. The majority decision is represented by the longest chain, which has the greatest proof-of-work effort invested in it. If a majority of CPU power is controlled by honest nodes, the honest chain will grow the fastest and outpace any competing chains. To modify a past block, an attacker would have to redo the proof-of-work of the block and all blocks after it and then catch up with and surpass the work of the honest nodes. We will show later that the probability of a slower attacker catching up diminishes exponentially as subsequent blocks are added.


工作量证明还解决了多数决策中代表权的问题。如果按"一个 IP 地址一票"来计算多数，任何能分配大量 IP 的人都能操纵结果。工作量证明本质上是"一 CPU 一票"。多数决策体现为最长的链——这条链上投入了最大的工作量证明努力。如果大多数算力由诚实节点控制，诚实链就会增长得最快，超越任何竞争链。要修改过去的区块，攻击者必须重做该区块及其后所有区块的工作量证明，然后追上并超越诚实节点的工作量。我们稍后会证明，随着后续区块不断添加，较慢的攻击者追上来的概率会呈指数下降。


To compensate for increasing hardware speed and varying interest in running nodes over time, the proof-of-work difficulty is determined by a moving average of an estimated number of blocks per hour. If blocks are generated too fast, the difficulty increases.


为了适应硬件速度的提升以及运行节点的兴趣随时间变化，工作量证明的难度由每小时出块数的移动平均值来决定。如果区块生成太快，难度就会提高。

---

## 5. Network / 网络


The steps to run the network are as follows:

1. New transactions are broadcast to all nodes.
2. Each node collects new transactions into a block.
3. Each node works on finding a difficult proof-of-work for its block.
4. When a node finds a proof-of-work, it broadcasts the block to all nodes.
5. Nodes accept the block only if all transactions in it are valid and not already spent.
6. Nodes express their acceptance of the block by working on creating the next block in the chain, using the hash of the accepted block as the previous hash.


网络的运行步骤如下：

1. 新交易广播给所有节点。
2. 每个节点将新交易打包成一个区块。
3. 每个节点努力为自己的区块寻找难度较高的工作量证明。
4. 当某个节点找到工作量证明时，将区块广播给所有节点。
5. 只有当区块中的所有交易都有效且未被花过时，节点才会接受该区块。
6. 节点通过基于所接受区块的哈希来创建链中的下一个区块，来表达对该区块的认可。


Nodes always consider the longest chain to be the correct one and will keep working on extending it. If two nodes broadcast different versions of the next block simultaneously, some nodes may receive one or the other first. In that case, they work on the first one they received, but save the other branch in case it becomes longer. The tie will be broken when the next proof-of-work is found and one branch becomes longer; the nodes that were working on the other branch will then switch to the longer one.


节点始终认为最长的链是正确的，并继续扩展它。如果两个节点同时广播下一个区块的不同版本，一些节点可能先收到其中一个，另一些节点先收到另一个。这种情况下，节点会先处理自己先收到的那个版本，但保留另一个分支以防它变得更长。当找到下一个工作量证明、某个分支变得更长时，分叉就解决了——原本在另一个分支上工作的节点会切换到更长的链上。


New transaction broadcasts do not necessarily need to reach all nodes. As long as they reach many nodes, they will get into a block before long. Block broadcasts are also tolerant of dropped messages. If a node does not receive a block, it will request it when it receives the next block and realizes it missed one.


新交易的广播不一定需要到达所有节点。只要能到达足够多的节点，交易很快就会被打包进区块。区块广播也容许消息丢失。如果某个节点没有收到某个区块，等它收到下一个区块、发现少了一个区块时，就会请求补发。

---

## 6. Incentive / 激励


By convention, the first transaction in a block is a special transaction that starts a new coin owned by the creator of the block. This adds an incentive for nodes to support the network, and provides a way to initially distribute coins into circulation, since there is no central authority to issue them. The steady addition of a constant of amount of new coins is analogous to gold miners expending resources to add gold to circulation. In our case, it is CPU time and electricity that is expended.


按照约定，每个区块的第一笔交易是一笔特殊交易，用来创建一枚新币，归区块创建者所有。这为节点支持网络提供了激励，也提供了一种初始分发货币的方式——因为没有中央机构来发行它们。稳定地持续增发固定数量的新币，类似于金矿消耗资源将黄金投入流通。在我们这里，消耗的是 CPU 时间和电力。


The incentive can also be funded with transaction fees. If the output value of a transaction is less than its input value, the difference is a transaction fee that is collected by the miner who includes the transaction in a block. The incentive will help encourage nodes to stay honest. If a greedy attacker is able to assemble more CPU power than all the honest nodes, he would have to choose between using it to defraud people by stealing back his payments, or using it to generate new coins. He ought to find it more profitable to play by the rules, such rules that favour him with more new coins than everyone else combined, than to undermine the system and the validity of his own wealth.


激励也可以来自交易手续费。如果一笔交易的输出值小于输入值，差额就是手续费，由将交易打包进区块的矿工收取。这种激励有助于鼓励节点保持诚实。如果一个贪婪的攻击者能够聚集超过所有诚实节点的算力，他面临两种选择：用它来欺骗他人（把自己的支付收回来），或者用它来挖新币。他应该会发现，遵守规则更有利——按照规则，他能获得的新币比其他所有人加起来还多，而不是破坏系统和他自己财富的有效性。

---

## 7. Reclaiming Disk Space / 回收硬盘空间


Once the latest transaction in a coin is buried under enough blocks, the spent transactions before it can be discarded to save disk space. To facilitate this without breaking the block's hash, transactions are hashed in a Merkle Tree [7][2][5], with only the root included in the block's hash. Old blocks can then be compacted by stubbing off branches of the tree. The interior hashes do not need to be stored.


一旦一枚币的最新交易被埋在足够多的区块之下，之前已花费的交易就可以丢弃以节省磁盘空间。为了在不破坏区块哈希的前提下实现这一点，交易用默克尔树 [7][2][5] 进行哈希，只有树根被包含在区块哈希中。旧区块可以通过修剪树的分支来压缩。内部的哈希值无需存储。


A block header with no transactions would be about 80 bytes. If we suppose blocks are generated every 10 minutes, 80 bytes × 6 × 24 × 365 = 4.2MB per year. With computer systems typically selling with 2GB of RAM as of 2008, and Moore's Law predicting current growth of 1.2GB per year, storage should not be a problem even if the block headers must be kept in memory.


不包含交易的区块头大约 80 字节。假设每 10 分钟生成一个区块，80 字节 × 6 × 24 × 365 = 每年 4.2MB。2008 年计算机通常配备 2GB 内存，而摩尔定律预测每年增长 1.2GB，即使必须把所有区块头保存在内存中，存储也不成问题。

---

## 8. Simplified Payment Verification / 简化支付验证


It is possible to verify payments without running a full network node. A user only needs to keep a copy of the block headers of the longest proof-of-work chain, which he can get by querying network nodes until he's convinced he has the longest chain, and obtain the Merkle branch linking the transaction to the block it's timestamped in. He can't check the transaction for himself, but by linking it to a place in the chain, he can see that a network node has accepted it, and blocks added after it further confirm the network has accepted it.


可以不运行完整的网络节点来验证支付。用户只需保留最长工作量证明链的区块头副本——他可以通过查询网络节点来获得，直到确信自己拥有最长的链——并获得将交易与其所在区块链接起来的默克尔分支。他无法亲自验证交易，但通过将交易链接到链上的某个位置，他可以看到某个网络节点已经接受了它，而后续添加的区块进一步证明网络已经接受了它。


As such, the verification is reliable as long as honest nodes control the network, but is more vulnerable if the network is overpowered by an attacker. While network nodes can verify transactions for themselves, the simplified method can be fooled by an attacker's fabricated transactions for as long as the attacker can continue to overpower the network. One strategy to protect against this would be to accept alerts from network nodes when they detect an invalid block, prompting the user's software to download the full block and alerted transactions to confirm the inconsistency. Businesses that receive frequent payments will probably still want to run their own nodes for more independent security and quicker verification.


因此，只要诚实节点控制网络，这种验证就是可靠的；但如果网络被攻击者压倒，就会变得脆弱。网络节点可以自己验证交易，但简化方法可能会被攻击者的伪造交易欺骗——只要攻击者能继续压倒网络。一种防范策略是：当网络节点检测到无效区块时，接受来自它们的警报，提示用户的软件下载完整区块和相关交易以确认不一致。经常收到付款的企业可能仍希望运行自己的节点，以获得更独立的安全性和更快的验证。

---

## 9. Combining and Splitting Value / 合并与分割金额


Although it would be possible to handle coins individually, it would be unwieldy to make a separate transaction for every cent in a transfer. To allow value to be split and combined, transactions contain multiple inputs and outputs. Normally there will be either a single input from a larger previous transaction or multiple inputs combining smaller amounts, and at most two outputs: one for the payment, and one for the change, if any, sent back to the sender.


虽然可以一枚一枚地处理币，但每次转移的每一分钱都单独做一笔交易会非常笨重。为了让价值能够分割和合并，交易包含多个输入和输出。通常要么有一个来自较大前笔交易的单输入，要么有多个小金额的合并输入，而输出最多有两个：一个用于支付，一个用于找零（如果有）发还给发送者。


It should be noted that fan-out, where a transaction depends on several transactions, and those transactions depend on many more transactions, is not a problem here. There is never the need to extract a complete standalone copy of a transaction's history before spending it.


需要注意的是，扇出在这里不是问题——一笔交易依赖几笔交易，而那几笔交易又依赖更多笔交易。花费之前永远不需要提取交易历史的完整独立副本。

---

## 10. Privacy / 隐私


The traditional banking model achieves a level of privacy by limiting access to information to the parties involved and the trusted third party. The necessity to announce all transactions publicly precludes this method, but privacy can still be maintained by breaking the flow of information in another place: by keeping public keys anonymous. The public can see that someone is sending an amount to someone else, but without information linking the transaction to anyone. This is similar to the level of information released by stock exchanges, where the time and size of individual trades, the "tape", is made public, but without telling who the parties were.


传统的银行模式通过只让交易各方和可信第三方访问信息来保护隐私。但我们必须公开所有交易，这种方法就行不通了。不过隐私仍可以通过在另一个环节切断信息流来保持：让公钥保持匿名。公众可以看到有人给某人转了一笔钱，但无法将交易与具体的人关联起来。这类似于股票交易所发布的信息水平：个别交易的时间和规模（行情带）是公开的，但不透露交易双方是谁。


As an additional firewall, a new key pair should be used for each transaction to keep them from being linked to a common owner. Some linking is still unavoidable with multi-input transactions, which necessarily reveal that their inputs were owned by the same owner. The risk is that if the owner of a key is revealed, the linking could reveal other transactions that belonged to the same owner.


作为额外的防火墙，每笔交易应该使用新的密钥对，防止交易被关联到同一个所有者。但对于多输入交易，一些关联仍然无法避免——这类交易必然暴露其输入属于同一个所有者。风险在于：如果某个密钥的所有者被曝光，这种关联可能会暴露属于同一所有者的其他交易。

---

## 11. Calculations / 计算


We consider the scenario of an attacker trying to generate an alternate chain faster than the honest chain. Even if this is accomplished, it does not throw the system open to sudden changes, such as creating value out of thin air or taking money that never belonged to the attacker. Nodes are not going to accept an invalid transaction as payment, and honest nodes will never accept a block containing them. An attacker can only try to change one of his own transactions to take back money he recently spent.


我们来考虑这样一个场景：攻击者试图比诚实链更快地生成一条替代链。即使成功了，也不会让系统突然变得可以任意修改，比如无中生有地创造价值或拿走不属于他的钱。节点不会接受无效交易作为支付，诚实节点也永远不会接受包含无效交易的区块。攻击者只能尝试修改自己的一笔交易，把最近花出去的钱收回来。


The race between the honest chain and an attacker chain can be characterized as a Binomial Random Walk. The success event is the honest chain being extended by one block, increasing its lead by +1, and the failure event is the attacker's chain being extended by one block, reducing the gap by -1.


诚实链与攻击者链之间的竞争可以看作一个二项随机游走。成功事件是诚实链延长一个区块，领先 +1；失败事件是攻击者链延长一个区块，差距缩小 -1。


The probability of an attacker catching up from a given deficit is analogous to a Gambler's Ruin problem. Suppose a gambler with unlimited credit starts at a deficit and plays potentially an infinite number of trials to try to reach breakeven. We can calculate the probability he ever reaches breakeven, or that an attacker ever catches up with the honest chain, as follows:


攻击者从给定落后差距追上来的概率，类似于赌徒破产问题。假设一个有无限信用的赌徒从落后开始，可能进行无限次试验试图达到收支平衡。我们可以计算他最终达到收支平衡的概率，或者说攻击者最终追上诚实链的概率，如下：


- p = probability an honest node finds the next block
- q = probability the attacker finds the next block
- q<sub>z</sub> = probability the attacker will ever catch up from z blocks behind

![公式](https://latex.codecogs.com/png.latex?%5C%7B%20q_z%20%3D%20%5Cbegin%7Bcases%7D%201%20%26%20%5Ctext%7Bif%20%7D%20p%20%5Cleq%20q%20%5C%5C%20%5Cleft%28%5Cfrac%7Bq%7D%7Bp%7D%5Cright%29%5Ez%20%26%20%5Ctext%7Bif%20%7D%20p%20%3E%20q%20%5Cend%7Bcases%7D%20%7D)


- p = 诚实节点挖到下一个区块的概率
- q = 攻击者挖到下一个区块的概率
- q<sub>z</sub> = 攻击者从落后 z 个区块追上来的概率


Given our assumption that p > q, the probability drops exponentially as the number of blocks the attacker has to catch up with increases. With the odds against him, if he doesn't make a lucky lunge forward early on, his chances become vanishingly small as he falls further behind.


假设 p > q，随着攻击者需要追赶的区块数量增加，概率呈指数下降。由于形势对他不利，如果他不能在早期幸运地冲刺一把，随着他越来越落后，他的机会就会变得微乎其微。


We now consider how long the recipient of a new transaction needs to wait before being sufficiently certain the sender can't change the transaction. We assume the sender is an attacker who wants to make the recipient believe he paid him for a while, then switch it to pay back to himself after some time has passed. The receiver will be alerted when that happens, but the sender hopes it will be too late.


现在我们来考虑，新交易的收款人需要等待多久，才能充分确定发送者无法更改交易。我们假设发送者是攻击者，他想让收款人相信自己已经付款，过了一段时间后再把交易改成付回给自己。收款人到时候会收到警报，但发送者希望那时已经太晚了。


The receiver generates a new key pair and gives the public key to the sender shortly before signing. This prevents the sender from preparing a chain of blocks ahead of time by working on it continuously until he is lucky enough to get far enough ahead, then executing the transaction at that moment. Once the transaction is sent, the dishonest sender starts working in secret on a parallel chain containing an alternate version of his transaction.


收款人生成新的密钥对，并在签名前不久把公钥给发送者。这防止了发送者提前准备一条区块链——通过持续工作直到幸运地领先足够多，然后在那个时刻执行交易。一旦交易发送出去，不诚实的发送者就开始秘密地在一条包含其交易替代版本的平行链上工作。


The recipient waits until the transaction has been added to a block and z blocks have been linked after it. He doesn't know the exact amount of progress the attacker has made, but assuming the honest blocks took the average expected time per block, the attacker's potential progress will be a Poisson distribution with expected value:

λ = z × (q / p)


收款人会等待，直到交易被打包进区块，并且后面又链接了 z 个区块。他不知道攻击者取得了多少进展，但假设诚实区块花费了每个区块的平均预期时间，攻击者的潜在进展将服从泊松分布，期望值为：

λ = z × (q / p)


To get the probability the attacker could still catch up now, we multiply the Poisson density for each amount of progress he could have made by the probability he could catch up from that point:

![公式2](https://latex.codecogs.com/png.latex?%5Csum_%7Bk%3D0%7D%5E%7B%5Cinfty%7D%20%5Cfrac%7B%5Clambda%5Ek%20e%5E%7B-%5Clambda%7D%7D%7Bk%21%7D%20%5Ccdot%20%5Cbegin%7Bcases%7D%20%28q%2Fp%29%5E%7Bz-k%7D%20%26%20%5Ctext%7Bif%20%7D%20k%20%5Cleq%20z%20%5C%5C%201%20%26%20%5Ctext%7Bif%20%7D%20k%20%3E%20z%20%5Cend%7Bcases%7D)


要计算攻击者现在仍能追上的概率，我们将他可能取得的每个进展量的泊松密度，乘以他从那个进展量追上来的概率：


Rearranging to avoid summing the infinite tail of the distribution...

![公式3](https://latex.codecogs.com/png.latex?1%20-%20%5Csum_%7Bk%3D0%7D%5E%7Bz%7D%20%5Cfrac%7B%5Clambda%5Ek%20e%5E%7B-%5Clambda%7D%7D%7Bk%21%7D%20%5Cleft%28%201%20-%20%5Cleft%28%5Cfrac%7Bq%7D%7Bp%7D%5Cright%29%5E%7Bz-k%7D%20%5Cright%29)


重新排列以避免对分布的无限尾部求和...


Converting to C code...

```c
#include <math.h>
double AttackerSuccessProbability(double q, int z)
{
    double p = 1.0 - q;
    double lambda = z * (q / p);
    double sum = 1.0;
    int i, k;
    for (k = 0; k <= z; k++)
    {
        double poisson = exp(-lambda);
        for (i = 1; i <= k; i++)
            poisson *= lambda / i;
        sum -= poisson * (1 - pow(q / p, z - k));
    }
    return sum;
}
```

转换成 C 代码...


Running some results, we can see the probability drop off exponentially with z.

```
q = 0.1
z = 0  P = 1.0000000
z = 1  P = 0.2045873
z = 2  P = 0.0509779
z = 3  P = 0.0131722
z = 4  P = 0.0034552
z = 5  P = 0.0009137
z = 6  P = 0.0002428
z = 7  P = 0.0000647
z = 8  P = 0.0000173
z = 9  P = 0.0000046
z = 10 P = 0.0000012
```


运行一些结果，可以看到概率随着 z 呈指数下降。


```
q = 0.3
z = 0  P = 1.0000000
z = 5  P = 0.1773523
z = 10 P = 0.0416605
z = 15 P = 0.0101008
z = 20 P = 0.0024804
z = 25 P = 0.0006132
z = 30 P = 0.0001522
z = 35 P = 0.0000379
z = 40 P = 0.0000095
z = 45 P = 0.0000024
z = 50 P = 0.0000006
```


Solving for P less than 0.1%...

```
P < 0.001
q = 0.10 z = 5
q = 0.15 z = 8
q = 0.20 z = 11
q = 0.25 z = 15
q = 0.30 z = 24
q = 0.35 z = 41
q = 0.40 z = 89
q = 0.45 z = 340
```

求解 P 小于 0.1% 的情况...

---

## 12. Conclusion / 结论


We have proposed a system for electronic transactions without relying on trust. We started with the usual framework of coins made from digital signatures, which provides strong control of ownership, but is incomplete without a way to prevent double-spending. To solve this, we proposed a peer-to-peer network using proof-of-work to record a public history of transactions that quickly becomes computationally impractical for an attacker to change if honest nodes control a majority of CPU power. The network is robust in its unstructured simplicity. Nodes work all at once with little coordination. They do not need to be identified, since messages are not routed to any particular place and only need to be delivered on a best effort basis. Nodes can leave and rejoin the network at will, accepting the proof-of-work chain as proof of what happened while they were gone. They vote with their CPU power, expressing their acceptance of valid blocks by working on extending them and rejecting invalid blocks by refusing to work on them. Any needed rules and incentives can be enforced with this consensus mechanism.


我们提出了一个不依赖信任的电子交易系统。我们从数字签名构成的币这一常规框架出发——它提供了强大的所有权控制，但若没有防止双花的机制，就不完整。为此，我们提出了一个使用工作量证明的点对点网络，来记录交易的公共历史。只要诚实节点控制大多数算力，攻击者想要篡改历史在计算上很快变得不可行。网络以其非结构化的简单性展现出鲁棒性：节点几乎无需协调就能同时工作；节点无需身份标识，因为消息不路由到特定地点，只需尽力传递；节点可随时离开和重新加入网络，并以工作量证明链作为离线期间发生事件的证明。它们用算力投票——通过扩展有效区块来表达认可，通过拒绝在无效区块上工作来表达拒绝。任何必要的规则和激励都可以通过这种共识机制来执行。

---

## References / 参考文献


[1] W. Dai, "b-money," http://www.weidai.com/bmoney.txt, 1998.

[2] H. Massias, J.-J. Quisquater, "Design of a secure timestamping service with minimal trust requirements," In 20th Symposium on Information Theory in the Benelux, May 1999.

[3] S. Haber, W.S. Stornetta, "How to time-stamp a digital document," In Journal of Cryptology, Vol 3, No 2, pages 99-111, 1991.

[4] D. Bayer, S. Haber, W.S. Stornetta, "Improving the efficiency and reliability of digital time-stamping," In Proceedings of the Second Conference on Computational Number Theory, pages 329-334, 1992.

[5] S. Haber, W.S. Stornetta, "Secure names for bit-strings," In Proceedings of the 4th ACM Conference on Computer and Communications Security, pages 28-35, April 1997.

[6] A. Back, "Hashcash - a denial of service counter-measure," http://www.hashcash.org/papers/hashcash.pdf, 2002.

[7] R.C. Merkle, "Protocols for public key cryptosystems," In Proc. 1980 Symposium on Security and Privacy, IEEE Computer Society, pages 122-133, April 1980.

[8] W. Feller, "An introduction to probability theory and its applications," Vol. I, John Wiley & Sons, New York, 1950.


---

*This translation is for educational purposes only. The original Bitcoin whitepaper was written by Satoshi Nakamoto in 2008.*

*本翻译仅供教育用途。比特币原始白皮书由中本聪于 2008 年撰写。*
