# InfiGUI-G1：一次前向给出 N 个候选点、按效率打分的 GUI grounding 模型

*CUA Radar 对 arXiv 2508.05731v2（Liu、Liu、Zhu、Li 等；浙江大学、香港理工大学、InfiX.ai、芝加哥大学、Amazon）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2508.05731v2 · 代码：https://github.com/InfiXAI/InfiGUI-G1*

## 问题：RLVR 指得准，但指错对象

GUI grounding 把自然语言指令映射到截图上的一个可交互元素。论文把这件事拆成两个维度：spatial alignment（空间对齐）是”指得准”，semantic alignment（语义对齐）是”指对东西”。RLVR（Reinforcement Learning with Verifiable Rewards）已经显著改善了空间对齐，但作者认为 “inefficient exploration bottlenecks semantic alignment, which prevent models from learning difficult semantic associations”——探索效率低下卡住了语义对齐。标准 RLVR 每个状态只从当前策略采样一个动作，于是不断重复采样自己高置信度的错误：论文的例子是指令 “use the camera to search for an object”，弱模型反复点通用的相机按钮，永远采不到 Google Lens 这个正确的小概率动作，奖励信号也就永远无法纠正它的语义误解。

## InfiGUI-G1 是什么

这是一个单步 grounding 策略，不是交互式智能体。感知：GUI 截图 + 自然语言指令；动作：输出一个点击坐标 (x, y)。回答前先在 `<think>...</think>` 标签里生成推理。基座是开源的 Qwen2.5-VL-3B-Instruct 和 Qwen2.5-VL-7B-Instruct；在 CUA Radar 板上的模式是 R01：离线单步 RL + 规则校验奖励，不需要环境 rollout。方法叫 Adaptive Exploration Policy Optimization（AEPO），三个部件：

1.  **Multi-answer generation（多答案生成）。** 模型一次前向输出 N 个候选点 {p1, …, pN}，而不是一个点，强迫它看自己最高置信预测之外的地方。
2.  **Adaptive Exploration Reward（AER，自适应探索奖励）。** 从效率比值 η = U/C 推出：效用 U 在任一候选点落入真值框 B 时为 +1，否则为 −1；成本 C 取提案成本（N）与验证成本的几何平均。成功时第一个正确点的名次为 k，C = √(N·k)，accuracy 奖励为 1/√(N·k)；失败时 N 个点全要检查，C = N，奖励为 −1/N。高效、确信的命中奖励最高，失败则给递减的惩罚以鼓励更宽的探索。
3.  **Collinear penalty（共线惩罚）。** 若候选点近似共线（任三点构成的三角形面积接近零），奖励直接改写为 −1。这挡住了退化的线性扫描；作者原话说该惩罚 “critical for preventing reward hacking”。

总奖励再加一个 +1/0 的格式奖励，用 RLOO 更新策略。训练数据来自公开 GUI 数据集（Widget Caption、OmniAct、GUICourse 等）约 44k 样本，过滤方式为：温度 1.0 生成 8 个回复，8 个全对的样本视为太简单而丢弃。训练用 16 张 H800，学习率 1e-6，rollout batch 128，RLOO rollout n = 8，训 3 个 epoch。

## 论文报告的结果

以下全部是**离线** grounding top-1 准确率（%）：预测点落入真值框即算对。InfiGUI-G1 只评估第一个生成的答案；论文对自己的模型报告 5 次运行的 σ。论文没有在线或交互式智能体实验。

| 模型（各基准平均） | MMBench-GUI | ScreenSpot-Pro | UI-Vision | UI-I2E-Bench | ScreenSpot-V2 |
|----|----|----|----|----|----|
| Naive RLVR-3B（同数据） | 70.9 | 39.8 | 19.4 | 71.6 | 90.1 |
| Naive RLVR-7B（同数据） | 79.3 | 47.6 | 24.1 | 75.8 | 92.5 |
| InfiGUI-G1-3B | 73.4 | 45.2 | 22.0 | 72.6 | 91.1 |
| InfiGUI-G1-7B | 80.8 | 51.9 | 26.1 | 77.4 | 93.5 |

论文还报告了自家模型的 Exploration Success Rate——N 个候选里**至少一个**正确，这是另一个更容易的指标（如 ScreenSpot-Pro 上 3B 为 52.0、7B 为 58.0，平均约 2 个候选），不应与上表的 top-1 混用。对外部方法：7B 在 ScreenSpot-Pro 上高于 GUI-G2-7B（47.5）和 UI-AGILE-7B（44.0）；在 MMBench-GUI 上高于 UI-TARS-1.5-7B（64.3）、UGround-V1-7B（65.7）和 InternVL3-72B（72.2）；在 UI-Vision 上高于 UI-TARS-72B（25.5）。摘要把内部对比总结为相对 naive RLVR 基线最高 9.0% 的相对提升。

## 论文自带的对照实验

**同数据内部基线。** Naive RLVR 用完全相同的 44k 数据和调好的超参训练，只隔离 AEPO 的改动；InfiGUI-G1 在两个规模、五个基准上全部更高。

**消融（ScreenSpot-Pro，7B）。** 每次去掉一个组件：完整模型 51.9；去掉 multi-answer 46.5；去掉 AER（换 naive 奖励）41.4；去掉 AER 的名次因子 k 为 44.0；去掉共线惩罚 37.0——且每样本答案数从 2.0 涨到 8.2。3B 顺序相同（完整 45.2，去惩罚 35.3，6.6 个答案）。去掉 k 之后模型仍能找到答案（exploration success 47.6）但很少排在第一位（38.1）。

**探索效率。** 即使给 Naive RLVR 四次独立尝试（pass@4：3B 43.5、7B 52.1），仍低于 InfiGUI-G1 单次前向的探索成功率（52.0 与 58.0，约 2 个候选），论文据此认为这是有结构的探索而非暴力多试。

**难样本。** 用基座模型的 16 次采样把 ScreenSpot-Pro 分层：在基座 0/16 全错的 hard 子集上，Naive RLVR 10.8，InfiGUI-G1 17.4（7B），论文报告相对提升 +61.1%；middle 子集增益较小（7B +8.0%，3B +4.0%），easy 子集两者都是 100。

**自适应行为。** 7B 模型在最难的基准上生成最多答案（UI-Vision：26.1% 准确率、2.1 个答案），在最容易的基准上最少（ScreenSpot-V2：93.5%、1.4 个答案）。

## 论文自己承认的薄弱处

- 全部是离线单步 grounding；没有 OSWorld/AndroidWorld 式在线评测，主指标是点是否落入框内。
- 只用了两个基座：“Our InfiGUI-G1 models are built upon the open-source Qwen2.5-VL-3B-Instruct and Qwen2.5-VL-7B-Instruct as backbones.”
- 泛化是论断而非构造：“these benchmarks contain many applications and scenarios not present in our training data, indicating that AEPO fosters a robust understanding rather than overfitting”——训练/测试应用重叠度没有量化。
- 列明的局限：“the computational overhead from multi-answer generation and a performance ceiling imposed by the backbone MLLM’s visual capabilities”。
- 相对同数据基线，平均值上的增益是几个点；较大的相对数字（+61.1%）出现在样本量更小的 hard 子集上。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **offline**，子模式 R01（规则奖励单步 RL）。分数反映论文报告的证据：五个 grounding 基准上的离线评测、包含未见过应用的基准、5 次运行的方差、同数据内部基线、GPU 成本、组件消融和已发布代码。判定记录同时标出：在线评测未报告、基座选择窄（仅 3B/7B）、预算对齐是部分的（pass@4 对比而非算力对齐训练）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
