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

<!-- 格式参考：
### 论文名
- 类型：
- 作者：
- 来源：
- 链接：
- 被引用数：（可选）
- 说明：
-->
