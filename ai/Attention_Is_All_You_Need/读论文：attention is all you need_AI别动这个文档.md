# Attention Is All You Need

- 类型：论文，2017年6月 arXiv 首发
- 作者：Ashish Vaswani、Illia Polosukhin（Google Brain 团队）等
- 来源：NeurIPS 2017 (Conference on Neural Information Processing Systems)
- 链接：
    - arXiv: https://arxiv.org/abs/1706.03762
    - NeurIPS: https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
- 被引用数：171,777+（Semantic Scholar，截止2026年4月6日）



## 摘要

讨论对象：序列转换模型。

旧方法：循环神经网络和卷积神经网络，包含编码器和解码器，最优秀的模型还会使用注意力机制将编码器和解码器连接起来。

新方法：论文提出：Transformer，只使用注意力机制，不再使用任何循环神经网络或卷积神经网络。

效果好：质量高、训练速度快、成本低。泛化性好。

- 质量高：在 WMT 2014 英德翻译任务上，达到 28.4 BLEU，比最好的模型高 2 BLEU 以上。
- 训练速度快、成本低：在 WMT 2014 英法翻译任务上，使用 8 块 GPU 上花费3.5天，达到 41.8 BLEU，成本仅是最好模型的一小部分。
- 泛化性好：在英语句法成分分析任务上，成功应用，无论训练数据是多是少。



## 1 引言

（铺垫）拔高RNN：RNN 是王者

（诊断）打倒RNN：RNN 天生串行，没法并行

（验证）验证：别人试过优化，无法根本解决

（转机）引出关键角色：注意力很强，却一直在RNN主导的模型中打辅助

（亮相）拿出最终解决方案：Transformer 让注意力当主角，完全摒弃RNN

（亮相）验证：8 块 P100 GPU 上训练 12 小时就达到翻译任务的 SOTA

## 2 背景



## 3 模型架构



## 4 为什么用自注意力



## 5 训练



## 6 结果



## 7 结论

