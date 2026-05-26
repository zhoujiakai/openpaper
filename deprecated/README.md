# <p align="center">已废弃

## 机器学习

- **LSTM**：[ml-lstm](ml-lstm/)

    - 类型：技术主题学习

    - 说明：长短期记忆网络（Long Short-Term Memory），循环神经网络的改进版本，解决长序列梯度消失问题。

- **机器学习基础**：[ml-机器学习基础](ml-机器学习基础/)

    - 类型：技术主题学习（Mastery 三阶段工作流）

    - 来源：sklearn 官方文档 + MIT 讲义 + GeeksforGeeks 面试题

    - 关键词：决策树、随机森林、SVM、CART、Gini、熵、信息增益、Bagging、Boosting、核函数、RBF、剪枝、OOB、GridSearchCV

    - 说明：从零基础出发，面试+实战两用。核心三件套：① 决策树（分裂准则 Gini/熵、预剪枝 vs 后剪枝、CART 二叉树）② 随机森林（Bootstrap + 随机特征双重随机、Bagging 降方差原理、OOB 误差估计、MDI 特征重要性及其局限）③ SVM（间隔最大化直觉、支持向量定义、Hard/Soft Margin、核技巧、C-γ 调参）

## 计算机视觉

- **YOLOv1**：[cv-yolov1](cv-yolov1/)

    - 类型：论文，2015年 arXiv 首发

    - 作者：Joseph Redmon 等

    - 来源：CVPR 2016

    - 链接：https://arxiv.org/abs/1506.02640

    - 被引用数：44,338+（Semantic Scholar，截止2026年4月6日）

    - 说明：开创性工作，将目标检测视为回归问题，实现实时检测

- **OpenPose**：[cv-openpose](cv-openpose/)

    - 类型：论文，2017年 arXiv 首发

    - 作者：Zhe Cao 等（CMU）

    - 来源：CVPR 2017

    - 链接：https://arxiv.org/abs/1611.08050 | GitHub:

    https://github.com/CMU-Perceptual-Computing-Lab/openpose

    - 被引用数：7,100+（Semantic Scholar，截止2026年4月6日）

    - 说明：实时多人姿态估计里程碑工作

- **DeepSORT**：[cv-deepsort](cv-deepsort/)

    - 类型：论文，2016年 arXiv 首发

    - 作者：Nicolai Wojke 等

    - 来源：2017 IEEE ICIP

    - 链接：https://arxiv.org/abs/1703.07402

    - 被引用数：7,000+（arXiv，截止2026年4月6日）

    - 说明：引入外观特征，显著减少 ID 切换，成为多目标跟踪标配

- **R-CNN**：[cv-rcnn](cv-rcnn/)

    - 类型：论文，2013年 arXiv 首发

    - 作者：Ross Girshick 等

    - 来源：NeurIPS 2014

    - 链接：https://arxiv.org/abs/1311.2524

    - 被引用数：28,000+（Google Scholar，截止2026年4月6日）

    - 说明：两阶段目标检测开山之作，后续发展出 Fast R-CNN、Faster R-CNN、Mask R-CNN

## 人工智能

- **Claude Skill 指南**：[ai-claude-skill-guide](ai-claude-skill-guide/)

    - 类型：官方教程（PDF）

    - 来源：Anthropic 官方

    - 说明：Claude Code Skills 完整构建指南，涵盖技能基础概念（SKILL.md 结构、渐进式加载）、规划与设计（用例识别、三大类别）、测试与迭代、分发与共享、常见模式与问题排查、资源与参考

- **特征工程**：[ai-feature-engineering](ai-feature-engineering/)

    - 类型：技术主题学习

    - 来源：特征工程方法论系统学习

    - 紧急程度：高

    - 关键词：特征提取、特征转换、特征编码、特征选择、特征构造、标准化、归一化、Embedding、TF-IDF

    - 说明：系统学习特征工程的完整流程（提取→转换→编码→选择→构造），掌握数值型/类别型/文本型/时间序列特征的处理方法，理解特征工程在 AI 应用开发中的实践（RAG 文档分块策略、元数据设计、向量检索中的特征表示）

- **模型服务化部署**：[ai-model-serving](ai-model-serving/)

    - 类型：技术主题学习

    - 来源：模型服务化部署系统学习

    - 紧急程度：高

    - 关键词：vLLM、Triton Inference Server、模型量化、ONNX、dynamic batching、PagedAttention、推理优化、容器化部署

    - 说明：系统学习大模型的线上服务化部署方案，涵盖：① vLLM 推理引擎（PagedAttention、continuous batching）② Triton Inference Server（多框架支持、dynamic batching）③ 模型格式转换（PyTorch→ONNX→TensorRT）④ 量化策略（FP16/INT8）⑤ API 服务封装（FastAPI + 限流 + 监控）⑥ Docker/K8s 容器化部署与自动扩缩容

- **游戏 AI 应用**：[ai-game-applications](ai-game-applications/)

    - 类型：技术主题学习

    - 来源：AI 技术在行业场景中的落地实践

    - 紧急程度：低

    - 关键词：游戏 AI、AIGC、智能 NPC、内容生成、推荐系统、反作弊、游戏数据分析

    - 说明：了解 AI 技术在游戏行业的主要落地场景，包括：① AIGC 内容生产（美术生成、文案生成、音乐生成）② 智能 NPC 对话系统（RAG + 角色扮演）③ 游戏推荐系统（玩家画像、协同过滤）④ 反作弊系统（异常检测）⑤ 游戏数据分析（玩家行为分析、留存预测）⑥ AI 驱动的游戏玩法优化

## 软件工程

- **Harness 工程**：[se-harness-engineering](se-harness-engineering/)

- **Web 抓取反检测**：[se-web-scraping-anti-detection](se-web-scraping-anti-detection/)

    - 类型：技术主题学习

    - 来源：爬虫工程化方案与反爬虫应对策略

    - 关键词：打码平台 API、2Captcha、Playwright stealth、多模态验证码识别、Agentic 浏览器自动化、AI 自愈选择器

    - 说明：系统学习爬虫工程化方案与反爬虫应对策略，涵盖：① 打码平台 API（2Captcha、打码兔）原理与集成；② Playwright stealth 插件减少验证码触发；③ 多模态模型（GPT-4o）识别图形验证码；④ Agentic 浏览器自动化工具（Browser Use、Playwright MCP、OpenClaw）；⑤ 网站结构变化时的自愈策略（配置化选择器、AI 视觉降级）

## 控制理论

- **控制理论**：[control-theory](control-theory/)

## 其他

- **Web3 无人机 LoRa UTM**：[web3-drone-lora-utm](web3-drone-lora-utm/)

    - 类型：论文解读（Sensors 2025），跨 Web3 + CV

    - 作者：计算机视觉研究院（公众号解读）

    - 来源：微信公众号「计算机视觉研究院」

    - 链接：

      - 公众号文章: https://mp.weixin.qq.com/s/76p9ItqouBRPIvTrE-FG3w

      - 原始论文 PDF: https://pmc.ncbi.nlm.nih.gov/articles/PMC12390230/pdf/sensors-25-05087.pdf

    - 说明：将 LoRa D2D 通信与以太坊公链 UTM 融合，提出轻量化安全协议解决无人机协同避障。核心亮点：SHA256+异或加密实现 0.01ms 级计算、544~800 位存储开销（行业最低）、AVISPA 形式化验证通过、抵御重放/中间人/追踪四大攻击。跨领域价值：区块链（去中心化 UTM + 智能合约）× CV（无人机视觉感知 + 低空交通管理）。

# <p align="center">待看

## ML

- **周志华机器学习**：

    - 类型：书，16 章
    - 作者：周志华（南京大学计算机系教授，欧洲科学院外籍院士，ACM Fellow，IEEE Fellow，AAAI Fellow，主要从事人工智能、机器学习、数据挖掘等领域研究，是中国最具影响力的机器学习学者之一）
    - 出版年份：2016年，清华大学出版社
    - 来源：经典教材，素有"西瓜书"之称
    - 说明：中国机器学习领域经典入门教材，因封面为西瓜图案而俗称"西瓜书"。全书 16 章分三部分：基础（1-3 章）、经典方法（4-10 章）、进阶知识（11-16 章），覆盖监督学习、无监督学习、集成学习、深度学习等核心主题。适合初学者建立系统的机器学习认知框架。

- **白话机器学习的数学**：

    - 类型：书
    - 作者：立石贤吾（日本，SmartNews 公司机器学习工程师），译者：郑明智
    - 出版年份：2020年，人民邮电出版社
    - 来源：李宏毅（台湾大学）推荐
    - 说明：以对话形式展开，通过程序员"绫乃"和朋友"美绪"的交流，结合回归与分类的具体问题，逐步讲解机器学习中实用的数学基础知识，重点攻克容易成为学习绊脚石的数学公式和符号，并通过实际的 Python 编程加深理解。与西瓜书互补——西瓜书侧重算法原理认知框架，本书侧重底层数学推导。

## 算法

- **算法导论**：

    - 类型：书，35 章
    - 作者：Thomas H. Cormen、Charles E. Leiserson、Ronald L. Rivest、Clifford Stein
    - 译者：殷建平、徐云、刘晓光、苏明、邹恒明、王宏志
    - 出版社：机械工业出版社（原书第3版）
    - 来源：经典教材，素有"CLRS"之称
    - 说明：算法领域公认的权威教材，覆盖排序、数据结构、图算法、动态规划、贪心算法、NP 完全性等核心主题，全书 35 章分为七部分。适合系统建立算法知识体系与刷题前打好理论基础。



## 英语



## 软件工程

- **Claude Code 源码**：[se-ClaudeCode源码/](se-ClaudeCode源码/)

    - 类型：开源项目源码学习
    - 来源：https://github.com/shareAI-lab/learn-claude-code
    - 进度：已完成 5/12 章，第 6 章待学习
    - 说明：从零实现自己的 Claude Code（Anthropic 推出的终端 AI 编程助手，可直接编辑文件、执行命令、管理 Git 等工作流），包含 claw0 等模块。

- **OpenClaw 源码**：[se-OpenClaw源码/](se-OpenClaw源码/)

    - 类型：开源项目源码学习
    - 来源：https://github.com/shareAI-lab/claw0
    - 主语言：Python（教学实现）
    - 说明：通过 claw0 教学仓库学习 OpenClaw 架构。claw0 从零开始，每节一个可运行的 Python 文件（~7000 行），10 个 section 逐步构建 AI Agent Gateway：Agent Loop → Tool Use → Sessions → Channels → Gateway → Intelligence → Heartbeat → Delivery → Resilience → Concurrency。学完即可阅读 OpenClaw 生产代码。

# <p align="center">待看论文

## Web3

- **Bitcoin: A Peer-to-Peer Electronic Cash System**：

    - 类型：论文，2008年10月31日发表
    - 作者：Satoshi（中本聪）
    - 来源：通过密码学邮件列表（metzdowd.com）发布
    - 链接：https://bitcoin.org/bitcoin.pdf
    - 被引用数：43,585+（Semantic Scholar，截止2026年4月6日）
    - 说明：比特币白皮书。中文：《比特币：一种点对点的电子现金系统》

- **Learn Blockchains by Building One**：

    - 类型：博客，2017年9月发布
    - 作者：Daniel van Flymen
    - 链接：https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
    - 说明：基于 Python，写一个区块链应用，非常简单简短的代码，了解区块链。

## AI

- **BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**：

    - 类型：论文，2018年10月 arXiv 首发
    - 作者：Jacob Devlin 等
    - 来源：NAACL 2019
    - 链接：
        - arXiv: https://arxiv.org/abs/1810.04805
        - GitHub: https://github.com/google-research/bert
    - 被引用数：112,481+（Semantic Scholar，截止2026年4月6日）
    - 说明：提出了 BERT 模型，使用双向 Transformer 编码器进行预训练，刷新了 11 项 NLP 任务记录。

- **MIT 6.034: Artificial Intelligence**：

    - 类型：课程（MIT OCW），Fall 2010
    - 讲师：Professor Patrick Winston
    - 来源：MIT OpenCourseWare
    - 链接：
        - OCW: https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/
        - YouTube: https://www.youtube.com/playlist?list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi
    - 说明：MIT 经典人工智能本科课程，涵盖知识表示、问题求解、搜索算法、约束满足、机器学习、神经网络、概率推理等核心 AI 主题。

## CV

- **YOLOv5**：

    - 类型：开源项目，2020年发布
    - 作者：Glenn Jocher（Ultralytics）
    - 来源：GitHub
    - 链接：https://github.com/ultralytics/yolov5
    - 说明：无配套论文，以工程实践著称，易于部署，生态最完善。

- **YOLOv8**：

    - 类型：开源项目，2023年1月发布
    - 作者：Ultralytics 团队
    - 来源：GitHub
    - 链接：https://github.com/ultralytics/ultralytics
    - 说明：YOLOv5 的继任者，支持目标检测、分割、分类、姿态估计。

- **YOLOv11**：

    - 类型：开源项目，2024年9月发布
    - 作者：Ultralytics 团队
    - 来源：GitHub
    - 链接：https://github.com/ultralytics/ultralytics
    - 说明：更小更快，精度进一步提升。

- **YOLO26**：

    - 类型：开源项目 / SOTA 模型，2025年9月首次发布，2026年1月14日正式发布
    - 作者：Ultralytics 团队
    - 来源：https://www.ultralytics.com/news
    - 链接：
        - 文档: https://docs.ultralytics.com/models/yolo26/
        - GitHub: https://github.com/ultralytics/ultralytics
    - 说明：端到端无 NMS 目标检测，优化边缘设备，CPU 推理更快，小目标精度提升，新一代边缘优先视觉 AI 标准。

- **PaddleOCR (PP-OCR)**：

    - 类型：开源项目，2020年发布
    - 作者：百度 PaddlePaddle 团队
    - 来源：GitHub
    - 链接：https://github.com/PaddlePaddle/PaddleOCR
    - 说明：超轻量级中英文OCR，支持80+语言，模型小精度高。

- **RTSP（Real Time Streaming Protocol）**：

    - 类型：协议规范（RFC 2326 / RFC 7826）
    - 作者：IETF（互联网工程任务组，制定互联网核心协议标准的国际组织）
    - 来源：RFC 2326（1998年）/ RFC 7826（2016年，RTSP 2.0）
    - 链接：
        - RTSP 1.0: https://www.rfc-editor.org/rfc/rfc2326
        - RTSP 2.0: https://www.rfc-editor.org/rfc/rfc7826
    - 说明：实时流传输协议，用于控制音视频流的传输（播放、暂停、录制等）。理解 RTSP 协议对于视频 surveillance、直播、流媒体开发至关重要。常配合 RTP/RTCP 使用。

- **OpenCV 源码阅读：视频接流（VideoCapture）实现**：

    - 类型：开源代码阅读（C++ + Python）
    - 项目：OpenCV
    - 来源：GitHub
    - 链接：
        - C++ 底层: https://github.com/opencv/opencv/tree/master/modules/videoio
        - Python 绑定: https://github.com/opencv/opencv/tree/master/modules/python/src2
    - 说明：分两层阅读。Python 层：理解 cv2.VideoCapture 的调用方式、参数配置、常见问题处理；C++ 底层：深入 VideoCapture → FFmpeg backend → avformat/avcodec 的完整调用链路，理解异步解码、缓冲队列等机制。

## 软件工程

- **剑指 Offer（50 道）**：

    - 类型：算法题集
    - 来源：LeetCode
    - 链接：https://leetcode.cn/problem-list/XApvNy3p/
    - 说明：《剑指 Offer》经典面试题 50 道。

- **Redis 深入掌握**：[se-redis](se-redis/)

    - 类型：技术主题学习（Mastery 三阶段工作流）
    - 来源：系统学习 Redis 核心原理
    - 紧急程度：高
    - 关键词：SDS、ziplist、skiplist、hashtable、RDB、AOF、缓存雪崩/穿透/击穿、Redlock、Sentinel
    - 说明：系统学习 Redis 核心原理，涵盖 5 大主题：数据结构底层实现、持久化策略、缓存三大问题、分布式锁、哨兵集群。

- **FastAPI 深入掌握**：[se-fastapi](se-fastapi/)

    - 类型：技术主题学习（Mastery 三阶段工作流）
    - 来源：FastAPI 核心机制系统学习
    - 紧急程度：高
    - 关键词：依赖注入、中间件、生命周期、Pydantic、性能优化
    - 说明：系统学习 FastAPI 核心机制，涵盖 5 大主题：依赖注入机制、中间件执行顺序、生命周期事件、请求/响应模型设计、性能优化。

- **Celery 异步任务队列深入掌握**：[se-celery](se-celery/)

    - 类型：技术主题学习（Mastery 三阶段工作流）
    - 来源：Celery 异步任务队列系统学习
    - 紧急程度：高
    - 关键词：Worker/Broker/Backend、任务调度策略、结果存储、重试与幂等、RabbitMQ 集成、Celery vs asyncio
    - 说明：系统学习 Celery 异步任务队列，涵盖：架构原理（Worker/Broker/Backend）、任务调度策略、结果存储、重试与幂等、与 RabbitMQ 集成、Celery vs asyncio 场景选择。

# <p align="center">Collection

- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — 一个优质开源合集，收集了"通过从零亲手构建技术来理解其原理"的教程，涵盖数据库、编译器、操作系统、Web 服务器、区块链等方向，适合在阅读论文之余通过动手实践加深理解。
- [ljg-skills](https://github.com/lijigang/ljg-skills) — 李继刚维护的 Claude Code Skills 合集，包含概念解剖、白话引擎、写作引擎、内容铸卡、论文阅读等 15 个技能，设计思路独特，适合扩展 Claude Code 的能力边界。
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic 官方 Agent Skills 仓库，提供经过验证的 Claude Code 技能，可通过 `/plugin marketplace add anthropics/skills` 安装。
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — 社区最热门的 Claude Code 资源精选合集（38.8k stars），涵盖 Skills、Hooks、Slash Commands 等，适合发现和探索社区产出的优质技能。
