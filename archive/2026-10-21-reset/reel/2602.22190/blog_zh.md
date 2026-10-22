# GUI-Libra：用精选推理数据、action-aware SFT 与 KL 正则化 RL 训练原生 GUI 智能体

*CUA Radar 对 arXiv 2602.22190v2（Yang、Wu、Wang、Chen、Yang、Cheng、Yao、Peng、Zhang、Gao、Zhang）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2602.22190v2 · 代码：https://github.com/GUI-Libra/GUI-Libra*

## 问题：推理、grounding 与含糊的奖励

这篇论文讨论“原生”（native）GUI 智能体：单个端到端模型，直接把指令和观测映射为可执行动作。作者认为，开源原生智能体在长程导航上仍然落后，并给出两个原因。第一，开源 GUI 轨迹数据集大多没有推理说明，或者只有短而含噪的说明（论文称每步常常不足 100 个 thought token）。第二，通用的后训练配方并不适合 GUI 智能体：带长 chain-of-thought（CoT）的标准 SFT 会损害 grounding；而逐步（step-wise）的可验证奖励 RL 面临论文所说的 partial verifiability（部分可验证性）：同一状态下可能有多个正确动作，但只有演示中的那一个动作被用来验证，于是其他合理动作会被判为失败。

## GUI-Libra 是什么

**智能体。** 每一步模型看到截图、任务指令，以及由自然语言动作描述构成的交互历史。它先在 `<think>` 标签中输出推理，再在 `<answer>` 标签中输出结构化 JSON 动作：动作类型、简短动作描述、可选的目标元素、值（文本、方向、应用名）和 `point_2d` 坐标。共有 13 种动作类型（Click、Write、Terminate、Swipe、Scroll、NavigateHome、Answer、Wait、OpenApp、NavigateBack、KeyboardPress、LongPress、Select），覆盖网页和移动端。在 CUA Radar 板上，它的架构模式是 R01（rule-reward single-step RL）。

**数据。** 作者汇总了公开轨迹数据源（GUI-Odyssey、AMEX、AndroidControl、AitZ、AitW、GUIAct、MM-Mind2Web），清洗后得到 19K 条轨迹、170K 步。他们用 GPT-4.1 生成结构化推理（观察、反思、规划），并把标注动作作为参考。随后有两道过滤：一是 agreement 过滤，用 Qwen3-VL-8B 对每个输入随机预测 10 次，若与标注一致的比例低于 0.3 就丢弃；二是用 Qwen3-VL-32B 做 bounding-box 检查，只有原始点击点落在预测框内才保留。结果是 GUI-Libra-81K：来自 9K 条轨迹的 81K 步，平均每步 210 个 thought token，其中网页数据只占 14.3%。RL 阶段则重新平衡为 40K 步。

**Action-aware SFT（ASFT）。** 训练把“先推理后动作”的样本与“直接动作”（去掉推理）的样本混合，并对 token 重新加权：相对于推理 token，动作 token 的权重为 alpha_a，grounding（坐标）token 的权重为 alpha_g，默认 alpha_a = 2、alpha_g = 4。混合训练也使模型可以在推理时选择不输出推理。

**保守 RL。** 第二阶段是在静态的 40K 步数据上做 step-wise GRPO，训练中不与真实环境交互。奖励是格式奖励（权重 0.1）与准确性奖励的加权和，其中准确性奖励是动作类型是否匹配、值的词级 F1 是否达标、预测点是否落在演示的 bounding box 内三者的乘积。针对 partial verifiability 有两个设计：一是保留 KL 正则（系数 0.001，7B 模型为 0.005），而不少 RLVR 配方会去掉它；二是 success-adaptive negative gradient scaling（SNGS），只对负的 advantage 乘一个系数，该系数随 GRPO 采样组中与演示一致的比例增大。论文还给出了离线逐步匹配与在线成功率之间的一个界，并论证 KL 信任域可以限制策略漂移。

## 论文报告的结果

以下为在线任务成功率（%），原生模型，步数上限为论文所述（AndroidWorld 20 步，WebArena-Lite-v2 15 步，Online-Mind2Web 30 步）。AndroidWorld 使用 115 个任务（另有一个任务无法初始化）。WebArena-Lite-v2（154 个任务，本地部署）取 4 次运行的平均。Online-Mind2Web（300 个任务，真实网站）取两个 judge（o4-mini 与 WebJudge-7B）的 average overall。每一行都与其训练起点的基座模型对比。

| 基座模型 | AndroidWorld 基座 / GUI-Libra | WebArena-Lite-v2 基座 / GUI-Libra | Online-Mind2Web 平均 基座 / GUI-Libra |
|----|----|----|----|
| Qwen2.5-VL-3B | 3.5 / 25.2 | 0.8 / 16.7 | 4.8 / 21.3 |
| Qwen2.5-VL-7B | 7.8 / 29.6 | 4.9 / 22.6 | 15.8 / 25.5 |
| Qwen3-VL-4B | 27.0 / 42.6 | 11.9 / 24.4 | 21.7 / 25.7 |
| Qwen3-VL-8B | 30.4 / 42.6 | 15.3 / 26.6 | 19.3 / 28.0 |

摘要给出 4B 与 8B 相对基座的提升：AndroidWorld 为 +15.6% 和 +12.2%，Online-Mind2Web 为 +4.0% 和 +8.7%，WebArena-Lite-v2 为 +12.5% 和 +11.3%。作为对照，原生 Qwen3-VL-32B 在 AndroidWorld 为 34.8，在 Online-Mind2Web 为 26.8。GPT-4o 搭配 UGround-v1-7B（两模块框架）在 AndroidWorld 为 42.6，在 Online-Mind2Web 为 24.3，其 WebArena-Lite-v2 数值 23.2 是论文转引自其他报告的。在 WebArena-Lite-v2 上，GPT-4o 加 ScaleCUA-7B 的框架（28.6）高于 GUI-Libra-8B。

离线逐步准确率是另一条坐标轴，没有放进海报图表。在作者清洗后的 AndroidControl-v2（398 个样本）上，GUI-Libra-8B 在 high-level 任务的 Pass@1 为 64.3，Qwen3-VL-8B 为 54.8；在 MM-Mind2Web-v2 上平均 Pass@1 为 50.5，对比 43.8。

## 论文自带的对照说明了什么

**组件消融（Qwen2.5-VL-3B，AndroidWorld）。** 基座为 3.5；普通 SFT 为 5.2，加混合数据为 11.3，ASFT 为 13.0。再加 KL 系数 0.001 的 RL 得到 25.2；KL 为 0.0 时为 21.7；不做 ASFT 直接 RL（KL 0.001）为 20.9。训练时去掉 CoT，25.2 降到 12.2。论文还报告，更大的 KL 系数往往提高离线 Pass@4，而 Pass@1 可能略降。

**SNGS。** 在 GUI-Libra-4B 上，打开 SNGS 使 AndroidWorld 从 39.1 升到 42.6，WebArena-Lite-v2 从 22.2 升到 24.4，同时 AndroidControl-v2 低层级 Pass@1 略有损失。在 3B 模型上，均匀的负梯度缩放在 AndroidWorld 得到 19.1 和 20.0，自适应版本为 25.2。论文指出 SNGS 对超参数敏感。

**离线与在线的相关性。** 对 3B 与 7B 的中间 checkpoint，使用 KL 正则时离线与在线分数的 Pearson 相关为 0.89、Spearman 为 0.83；不用 KL 时分别为 0.63 和 0.53。没有 KL 时，训练奖励持续上升而评测分数下降。

**长推理下的 grounding。** 在 ScreenSpot-v2 上，7B 模型推理模式下的准确率从 SFT 的 79.0% 升到混合数据的 81.4%，再到 ASFT 的 83.4%；RL 之后推理模式为 89.3%，不推理模式为 88.5%。

**公平比较。** 基线在 GUI-Libra-81K 上训练两个 epoch，混合数据的模型训练一个 epoch。论文还把原生模型与带额外模块的智能体框架分开报告：step-wise summary 模块使 Qwen3-VL-4B 和 8B 分别提高 9.5 和 8.7 个点。

**Judge。** Online-Mind2Web 用两个 judge 打分。o4-mini 下 GUI-Libra-8B 为 19.3，基座为 11.0；WebJudge-7B 下为 36.7，基座为 27.7。

## 证据偏薄的地方

- 论文没有描述留出（held-out）的应用或网站划分，也没有报告 AndroidWorld 与 Online-Mind2Web 的多次运行方差。WebArena-Lite-v2 取 4 次平均，论文称原因是结果方差较大。
- 两个 judge 按已发布方式使用，论文没有对它们本身做验证。
- 作者在 Limitations 中说明，训练数据量相对有限，也没有探索完全在线的训练。SFT 数据以移动端为主，论文提到更多网页数据可能改善网页 Pass@4。
- 成本只部分报告：SFT 在 8 张 B200 上约需 4 小时（Qwen3-VL-4B）到 5.5 小时（8B），RL 约 16 和 20 小时，但数据生成的成本没有给出。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **71 分（★★★）**，证据等级 **transfer**。记录认可：三个基准上的在线评测、较强的基线、对齐的步数预算、组件消融以及已声明的代码发布；成本为部分报告。留出环境与方差记为 unclear，judge 有效性记为 untested，没有记录反模式标记。CUA Radar 没有重跑任何实验，这里所有数字均来自论文（版本 v2）。
