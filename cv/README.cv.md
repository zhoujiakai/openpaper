# CV 学习资源

## YOLOv5/v8/v11/v26 学习途径

这些版本没有正式论文，有以下学习途径：

### 1. 官方文档（最推荐）

- https://docs.ultralytics.com/ - 架构说明、配置详解
- https://docs.ultralytics.com/models/yolo11/ - 每个版本的模块说明

### 2. 阅读源码（最直接）

```bash
git clone https://github.com/ultralytics/ultralytics.git
```

核心文件路径：

```
ultralytics/
├── models/
│   ├── yolo/
│   │   ├── detect/
│   │   │   └── __init__.py          # 检测头
│   │   ├── common.py                 # 基础模块（Conv、C2f等）
│   │   └── __init__.py               # 模型构建入口
│   └── yaml                          # YAML配置文件（架构定义）
```

### 3. YAML 配置文件（架构说明书）

```yaml
# ultralytics/cfg/models/11/yolo11.yaml
nc: 80  # 类别数
scales: # 模型缩放参数（n/s/m/l/x）

backbone:
  - [-1, 1, Conv, [64, 3, 2]]         # Conv模块
  - [-1, 1, Conv, [128, 3, 2]]
  - [-1, 1, C2f, [128, True]]         # C2f模块
  ...
```

### 4. 社区文章

- 知乎/CSDN：搜索 "YOLOv5源码解析"、"YOLOv8架构详解"
- Medium：英文技术博客
- B站/YouTube：视频教程，直观讲解

### 5. 对比学习

参考有论文的版本：

| 版本 | 年份 | 引用数 | 链接 | 关键点 |
|------|------|--------|------|--------|
| YOLOv4 | 2020 | ~25,700+ | [arXiv](https://arxiv.org/abs/2004.10934) | CSPDarknet、PANet |
| YOLOv7 | 2022 | ~4,500+ | [arXiv](https://arxiv.org/abs/2207.02696) | E-ELAN、模型重参数化 |
| YOLOv10 | 2024 | ~370+ | [arXiv](https://arxiv.org/abs/2405.14458) | NMS-free 设计 |

> *注：引用数统计自 Google Scholar/arXiv，数据截至 2026年04月06日*

### 6. 调试工具

```python
from ultralytics import YOLO

model = YOLO('yolo11n.pt')
print(model.model)  # 打印完整模型结构
```

---

## 推荐学习顺序

| 步骤 | 内容 |
|:----:|------|
| 1 | 先看 YOLOv1/v3/v4 论文，理解基础原理 |
| 2 | 阅读 YOLOv5 源码（代码结构最清晰） |
| 3 | 对照 YAML 配置，理解模块组装逻辑 |
| 4 | 用 model.model 打印结构，逐层分析 |
| 5 | 参考社区博客单读重点模块（C2f、SPPF等） |
