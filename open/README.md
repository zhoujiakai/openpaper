# 待看论文

## Web3

### Bitcoin：A Peer-to-Peer Electronic Cash System
- 类型：论文，2008年10月31日发表
- 作者：Satoshi（中本聪）
- 来源：通过密码学邮件列表（metzdowd.com）发布
- 链接：https://bitcoin.org/bitcoin.pdf
- 被引用数：43,585+（Semantic Scholar，截止2026年4月6日）
- 说明：比特币白皮书。中文：《比特币：一种点对点的电子现金系统》

### learn blockchains by building one
- 类型：博客，2017年9月发布
- 作者：Daniel van Flymen
- 链接：https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
- 说明：基于python，写一个区块链应用，非常简单简短的代码，了解区块链。

### 基于公链 + LoRa 的无人机机间安全通信，破解低空交通管理难题
- 类型：论文解读（Sensors 2025），跨 Web3 + CV
- 作者：计算机视觉研究院（公众号解读）
- 来源：微信公众号「计算机视觉研究院」
- 链接：
  - 公众号文章: https://mp.weixin.qq.com/s/76p9ItqouBRPIvTrE-FG3w
  - 原始论文 PDF: https://pmc.ncbi.nlm.nih.gov/articles/PMC12390230/pdf/sensors-25-05087.pdf
- 说明：将 LoRa D2D 通信与以太坊公链 UTM 融合，提出轻量化安全协议解决无人机协同避障。核心亮点：SHA256+异或加密实现 0.01ms 级计算、544~800 位存储开销（行业最低）、AVISPA 形式化验证通过、抵御重放/中间人/追踪四大攻击。跨领域价值：区块链（去中心化 UTM + 智能合约）× CV（无人机视觉感知 + 低空交通管理）。

## AI

### BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- 类型：论文，2018年10月 arXiv 首发
- 作者：Jacob Devlin 等
- 来源：NAACL 2019
- 链接：
  - arXiv: https://arxiv.org/abs/1810.04805
  - GitHub: https://github.com/google-research/bert
- 被引用数：112,481+（Semantic Scholar，截止2026年4月6日）
- 说明：提出了 BERT 模型，使用双向 Transformer 编码器进行预训练，刷新了 11 项 NLP 任务记录

### MIT 6.034: Artificial Intelligence
- 类型：课程（MIT OCW），Fall 2010
- 讲师：Professor Patrick Winston
- 来源：MIT OpenCourseWare
- 链接：
  - OCW: https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/
  - YouTube: https://www.youtube.com/playlist?list=PLUl4u3cNGP63gFHB6xb-kVBiQHYe_4hSi
- 说明：MIT 经典人工智能本科课程，涵盖知识表示、问题求解、搜索算法、约束满足、机器学习、神经网络、概率推理等核心 AI 主题

### The Complete Guide to Building Skills for Claude
- 类型：官方教程（PDF）
- 来源：Anthropic 官方
- 说明：Claude Code Skills 完整构建指南，涵盖技能基础概念（SKILL.md 结构、渐进式加载）、规划与设计（用例识别、三大类别）、测试与迭代、分发与共享、常见模式与问题排查、资源与参考

### 特征工程方法论
- 类型：技术主题学习
- 来源：特征工程方法论系统学习
- 紧急程度：高
- 关键词：特征提取、特征转换、特征编码、特征选择、特征构造、标准化、归一化、Embedding、TF-IDF
- 说明：系统学习特征工程的完整流程（提取→转换→编码→选择→构造），掌握数值型/类别型/文本型/时间序列特征的处理方法，理解特征工程在 AI 应用开发中的实践（RAG 文档分块策略、元数据设计、向量检索中的特征表示）

### 模型服务化部署（vLLM/Triton）
- 类型：技术主题学习
- 来源：模型服务化部署系统学习
- 紧急程度：高
- 关键词：vLLM、Triton Inference Server、模型量化、ONNX、dynamic batching、PagedAttention、推理优化、容器化部署
- 说明：系统学习大模型的线上服务化部署方案，涵盖：① vLLM 推理引擎（PagedAttention、continuous batching）② Triton Inference Server（多框架支持、dynamic batching）③ 模型格式转换（PyTorch→ONNX→TensorRT）④ 量化策略（FP16/INT8）⑤ API 服务封装（FastAPI + 限流 + 监控）⑥ Docker/K8s 容器化部署与自动扩缩容

### 游戏 AI 应用场景
- 类型：技术主题学习
- 来源：AI 技术在行业场景中的落地实践
- 紧急程度：低
- 关键词：游戏 AI、AIGC、智能 NPC、内容生成、推荐系统、反作弊、游戏数据分析
- 说明：了解 AI 技术在游戏行业的主要落地场景，包括：① AIGC 内容生产（美术生成、文案生成、音乐生成）② 智能 NPC 对话系统（RAG + 角色扮演）③ 游戏推荐系统（玩家画像、协同过滤）④ 反作弊系统（异常检测）⑤ 游戏数据分析（玩家行为分析、留存预测）⑥ AI 驱动的游戏玩法优化

## CV

### YOLOv1: You Only Look Once: Unified, Real-Time Object Detection
- 类型：论文，2015年 arXiv 首发
- 作者：Joseph Redmon 等
- 来源：CVPR 2016
- 链接：https://arxiv.org/abs/1506.02640
- 被引用数：44,338+（Semantic Scholar，截止2026年4月6日）
- 说明：开创性工作，将目标检测视为回归问题，实现实时检测

### YOLOv5
- 类型：开源项目，2020年发布
- 作者：Glenn Jocher（Ultralytics）
- 来源：GitHub
- 链接：https://github.com/ultralytics/yolov5
- 说明：无配套论文，以工程实践著称，易于部署，生态最完善

### YOLOv8
- 类型：开源项目，2023年1月发布
- 作者：Ultralytics 团队
- 来源：GitHub
- 链接：https://github.com/ultralytics/ultralytics
- 说明：YOLOv5 的继任者，支持目标检测、分割、分类、姿态估计

### YOLOv11
- 类型：开源项目，2024年9月发布
- 作者：Ultralytics 团队
- 来源：GitHub
- 链接：https://github.com/ultralytics/ultralytics
- 说明：更小更快，精度进一步提升

### YOLO26
- 类型：开源项目 / SOTA 模型，2025年9月首次发布，`https://docs.ultralytics.com/models/yolo26/`，2026年1月14日正式发布
- 作者：Ultralytics 团队
- 来源：https://www.ultralytics.com/news
- 链接：https://docs.ultralytics.com/models/yolo26/ | GitHub:
https://github.com/ultralytics/ultralytics
- 说明：端到端无 NMS 目标检测，优化边缘设备，CPU 推理更快，小目标精度提升，新一代边缘优先视觉 AI 标准

### OpenPose: Realtime Multi-Person 2D Pose Estimation
- 类型：论文，2017年 arXiv 首发
- 作者：Zhe Cao 等（CMU）
- 来源：CVPR 2017
- 链接：https://arxiv.org/abs/1611.08050 | GitHub:
https://github.com/CMU-Perceptual-Computing-Lab/openpose
- 被引用数：7,100+（Semantic Scholar，截止2026年4月6日）
- 说明：实时多人姿态估计里程碑工作

### Simple Online and Realtime Tracking (DeepSORT)
- 类型：论文，2016年 arXiv 首发
- 作者：Nicolai Wojke 等
- 来源：2017 IEEE ICIP
- 链接：https://arxiv.org/abs/1703.07402
- 被引用数：7,000+（arXiv，截止2026年4月6日）
- 说明：引入外观特征，显著减少 ID 切换，成为多目标跟踪标配

### PaddleOCR (PP-OCR)
- 类型：开源项目，2020年发布
- 作者：百度 PaddlePaddle 团队
- 来源：GitHub
- 链接：https://github.com/PaddlePaddle/PaddleOCR
- 说明：超轻量级中英文OCR，支持80+语言，模型小精度高

### RTSP（Real Time Streaming Protocol）
- 类型：协议规范（RFC 2326 / RFC 7826）
- 作者：IETF（互联网工程任务组，制定互联网核心协议标准的国际组织）
- 来源：RFC 2326（1998年）/ RFC 7826（2016年，RTSP 2.0）
- 链接：
  - RTSP 1.0: https://www.rfc-editor.org/rfc/rfc2326
  - RTSP 2.0: https://www.rfc-editor.org/rfc/rfc7826
- 说明：实时流传输协议，用于控制音视频流的传输（播放、暂停、录制等）。理解 RTSP 协议对于视频 surveillance、直播、流媒体开发至关重要。常配合 RTP/RTCP 使用。

### OpenCV 源码阅读：视频接流（VideoCapture）实现
- 类型：开源代码阅读（C++ + Python）
- 项目：OpenCV
- 来源：GitHub
- 链接：
  - C++ 底层: https://github.com/opencv/opencv/tree/master/modules/videoio
  - Python 绑定: https://github.com/opencv/opencv/tree/master/modules/python/src2
- 说明：分两层阅读。Python 层：理解 cv2.VideoCapture 的调用方式、参数配置、常见问题处理；C++ 底层：深入 VideoCapture → FFmpeg backend → avformat/avcodec 的完整调用链路，理解异步解码、缓冲队列等机制。

### R-CNN: Regions with Convolutional Neural Network Features
- 类型：论文，2013年 arXiv 首发
- 作者：Ross Girshick 等
- 来源：NeurIPS 2014
- 链接：https://arxiv.org/abs/1311.2524
- 被引用数：28,000+（Google Scholar，截止2026年4月6日）
- 说明：两阶段目标检测开山之作，后续发展出 Fast R-CNN、Faster R-CNN、Mask R-CNN

## 英语

### 刘晓燕《考研英语你还在背单词吗》
- 类型：词汇学习笔记
- 作者：刘晓燕
- 链接：https://appfb9e4aqm2459.h5.xiaoeknow.com/p/course/column/p_678b5352e4b0694ca04c5f27
- 说明：基于《考研英语你还在背单词吗》整理的词汇笔记，按 Lesson 分组，标注重点词汇

## 软件工程

### 剑指 Offer（50 道）
- 类型：算法题集
- 来源：LeetCode
- 链接：https://leetcode.cn/problem-list/XApvNy3p/
- 说明：《剑指 Offer》经典面试题 50 道

### Redis 深入掌握
- 类型：技术主题学习（Mastery 三阶段工作流）
- 来源：系统学习 Redis 核心原理
- 紧急程度：高
- 关键词：SDS、ziplist、skiplist、hashtable、RDB、AOF、缓存雪崩/穿透/击穿、Redlock、Sentinel
- 说明：系统学习 Redis 核心原理，涵盖 5 大主题：数据结构底层实现、持久化策略、缓存三大问题、分布式锁、哨兵集群
- 进度：[se-redis](se-redis/)

### FastAPI 深入掌握
- 类型：技术主题学习（Mastery 三阶段工作流）
- 来源：FastAPI 核心机制系统学习
- 紧急程度：高
- 关键词：依赖注入、中间件、生命周期、Pydantic、性能优化
- 说明：系统学习 FastAPI 核心机制，涵盖 5 大主题：依赖注入机制、中间件执行顺序、生命周期事件、请求/响应模型设计、性能优化
- 进度：[se-fastapi](se-fastapi/)

### Celery 异步任务队列深入掌握
- 类型：技术主题学习（Mastery 三阶段工作流）
- 来源：Celery 异步任务队列系统学习
- 紧急程度：高
- 关键词：Worker/Broker/Backend、任务调度策略、结果存储、重试与幂等、RabbitMQ 集成、Celery vs asyncio
- 说明：系统学习 Celery 异步任务队列，涵盖：架构原理（Worker/Broker/Backend）、任务调度策略、结果存储、重试与幂等、与 RabbitMQ 集成、Celery vs asyncio 场景选择
- 进度：[se-celery](se-celery/)

### 爬虫反检测与验证码识别技术
- 类型：技术主题学习
- 来源：爬虫工程化方案与反爬虫应对策略
- 关键词：打码平台 API、2Captcha、Playwright stealth、多模态验证码识别、Agentic 浏览器自动化、AI 自愈选择器
- 说明：系统学习爬虫工程化方案与反爬虫应对策略，涵盖：① 打码平台 API（2Captcha、打码兔）原理与集成；② Playwright stealth 插件减少验证码触发；③ 多模态模型（GPT-4o）识别图形验证码；④ Agentic 浏览器自动化工具（Browser Use、Playwright MCP、OpenClaw）；⑤ 网站结构变化时的自愈策略（配置化选择器、AI 视觉降级）

<!-- 格式参考：
### 论文名
- 类型：
- 作者：
- 来源：
- 链接：
- 被引用数：（可选）
- 说明：
-->
