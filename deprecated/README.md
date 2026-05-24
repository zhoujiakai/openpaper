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
