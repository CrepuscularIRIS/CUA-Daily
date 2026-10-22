# UI-Mem：在线 RL 训练移动端 GUI 智能体，并用不断演化的工作流、技能与失败模式记忆来引导 rollout

*CUA Radar 对 arXiv 2602.05832v1（Xiao、Wang、Wang、Liu、Chai、Pan、Zhou、Chen、Wen、Li）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2602.05832v1 · 项目主页（论文中给出）：https://ui-mem.github.io/*

## 问题：奖励稀疏，同样的错误一遍遍重犯

在线强化学习让 GUI 智能体通过与真实环境交互来学习，通常使用 GRPO 加结果奖励。论文指出两个瓶颈。其一是 credit assignment：长任务里只要最后一步出错，即使中间步骤正确也得到负反馈。其二是重复犯错：相似的失败模式（例子是确认弹窗）在不同任务中反复出现，智能体无法把教训带到下一个任务。此外，采样出的 GRPO 组常常全部失败，advantage 方差为零，没有梯度。Experience replay 和 step-level dense reward 只解决其中一部分，论文认为它们都不能跨任务、跨应用迁移可复用的经验。

## UI-Mem 是什么

**智能体。** 一个多模态 LLM（Qwen3-VL，4B 和 8B），在 Android 模拟器上操作。状态是截图加用户指令；动作是原子 GUI 操作（Click、Swipe、Type、Home，轨迹图中还有 open_app）。除非按下文做了奖励塑形，奖励就是 0/1 的结果奖励。在 CUA Radar 板上它属于模式 C19：从智能体自身运行中积累可复用知识，这里放在 RL 循环里。

**记忆。** 三个层级，以参数化模板形式存入向量数据库：高层 workflow（有序的子任务，如打开邮件应用、选择收件人、输入内容、发送）、中层 subtask skill（如点搜索、输入查询词、选择第一个结果）和 failure pattern（如在填写文件名之前不要点 Save）。具体取值被替换成占位符，因此一个模板可以覆盖很多任务。rollout 时先对指令做 embedding，检索 top-k 任务模板，由 DeepSeek-V3 判定匹配并抽取变量绑定，再把模板实例化成具体计划。候选计划按 UCB 分数排序（成功次数加探索项）；失败模式按时间新近程度排序。

**Stratified Group Sampling（分层组采样）。** 每个 GRPO 组（每个 query 采样 G = 4 条）被分成强引导（workflow、skill 与 failure pattern 全给）、弱引导（只给 workflow）和无引导三份。目的是让组内结果保持多样，使 advantage 有信息量，同时把无引导策略训练得接近有引导策略。动态 dropout 课程跟踪每个任务成功率的滑动平均，随着智能体变强，把概率从强引导移向无引导。奖励中还加入了子任务进度项，以及对无引导成功的额外奖励。

**Self-Evolving Loop（自演化循环）。** 一个基于文本的奖励流水线评判每条轨迹：Qwen2.5-VL-72B-Instruct 先用文字描述屏幕状态和动作，再由 DeepSeek-V3 检查达成了哪些关键任务状态。Seed1.8 抽取成功计划和对第一个失败子任务的诊断，具体取值变成占位符，然后与余弦相似的已有条目合并，或作为新条目加入。

**训练设置。** 256 条 query，来自 AMEX、AndroidLab 和 UI-Genie 的指令，按模拟器中可用的应用过滤，并用 GPT-4o 扩充；训练五个 epoch，学习率 1e-6。正文没有给出奖励权重、UCB 权重和课程阈值的取值，也没有给出计算成本。

## 论文报告的结果

以下全部是在模拟器中的在线结果。⋆ 表示推理时同样检索记忆。论文全文没有出现随机种子、重复运行或置信区间。

**AndroidWorld**（116 个任务，20 个应用），成功率（%）：

| 模型           | 成功率 |
|----------------|--------|
| Qwen3-VL-4B    | 45.3   |
| UI-Mem-4B      | 58.2   |
| UI-Mem-4B⋆     | 62.5   |
| Qwen3-VL-8B    | 47.6   |
| UI-Mem-8B      | 66.8   |
| UI-Mem-8B⋆     | 71.1   |
| Step-GUI-8B    | 67.7   |
| Gemini-2.5-Pro | 69.7   |
| Seed1.8        | 70.7   |

论文把 71.1 的 UI-Mem-8B⋆ 称为 state-of-the-art，高于 Gemini-2.5-Pro 和 Seed1.8。注意这一行使用了推理时记忆；不带记忆的 8B 模型（66.8）在同一张表里略低于 Step-GUI-8B。

**AndroidLab**（138 个任务，九个离线应用），Sub-Goal Success Rate（Sub-SR）和成功率（SR）：

| 模型          | Sub-SR | SR   |
|---------------|--------|------|
| Qwen3-VL-4B   | 48.2   | 37.0 |
| UI-Mem-4B     | 49.5   | 37.7 |
| UI-Mem-4B⋆    | 51.9   | 39.9 |
| Qwen3-VL-8B   | 45.3   | 34.8 |
| UI-Mem-8B     | 52.7   | 43.5 |
| UI-Mem-8B⋆    | 56.0   | 44.9 |
| MobileRL (7B) | –      | 42.5 |

在 4B 上，不带推理时记忆的 SR 提升很小（37.7 对 37.0）。论文没有报告离线单步准确率基准。

## 论文自带的对照实验

**RL 范式对比（8B，AndroidWorld）。** 基线 47.6；Vanilla GRPO 53.0；GRPO 加 progress reward 57.3；GRPO 加 experience replay 56.5；只在推理时用记忆做提示、不训练 52.6；GRPO 加推理时提示 55.2；UI-Mem 66.8。论文的结论是：只把记忆当上下文提供，若模型没有学会使用，收益有限。论文没有说明这些变体是否使用相同的 rollout 或步数预算。

**组件消融（8B，AndroidWorld）。** 完整系统 66.8。只用 workflow 59.5‡，只用 skill 61.6‡，只用 failure pattern 58.6‡。用原始经验代替抽象模板 58.2。关闭记忆更新 62.9。去掉分层采样（所有 rollout 都给完整引导）48.3‡，低于 Vanilla GRPO；论文将其解读为对记忆的过度依赖。

**训练动态。** 图 7 定性地显示：标准 GRPO 的成功率剧烈波动、没有明显上升趋势，组内奖励方差经常塌缩到接近零；UI-Mem 的训练更稳定。该图没有给出具体数值。

**留出应用。** 五个 AndroidLab 应用不在训练集中。下表为图 6 上印出的成功率（基线 Qwen3-VL / UI-Mem 不检索记忆的 zero-shot / UI-Mem 检索记忆）：

| 应用      | 基线  | Zero-shot | 带记忆 |
|-----------|-------|-----------|--------|
| Bluecoins | 33.3‡ | 33.3‡     | 53.3‡  |
| Cantook   | 41.7‡ | 50.0‡     | 66.7‡  |
| Maps.me   | 13.3‡ | 33.3‡     | 33.3‡  |
| Pi-Music  | 16.7  | 25.0‡     | 33.3‡  |
| Zoom      | 40.0‡ | 40.0‡     | 80     |

论文称 zero-shot 在五个应用上都不低于基线，并称记忆带来“在 Bluecoins 和 Maps.me 上尤其明显的提升”。按图上印出的数值，Maps.me 的 zero-shot 与带记忆两根柱子相等，记忆带来的较大提升出现在 Cantook 和 Zoom。论文没有说明该实验使用的模型规模、每个应用的任务数以及运行次数。

**奖励判定器。** 表 4 将两阶段文本验证流水线与 MLLM-as-a-judge 对比。仅用 Qwen2.5-VL-72B：accuracy 0.724（F1 0.811）；仅用 Gemini 2.5 Pro：0.776（F1 0.837）；训练中使用的 Qwen2.5-VL-72B 加 DeepSeek-V3：0.900（F1 0.902）。带标注的评测集规模和来源未说明。

## 证据较薄弱之处

- 没有随机种子或置信区间；相差一两个点的差异（例如 AndroidLab 4B 上的 37.7 对 37.0）仅凭论文无法与噪声区分。
- 论文没有说明 AndroidWorld 的应用是否与训练应用重叠；训练任务被过滤为“core apps in our emulator environment”。五个留出的 AndroidLab 应用是唯一明确的留出测试，而其细节很少（见上）。
- 训练依赖多个大型外部模型（Qwen2.5-VL-72B、DeepSeek-V3、Seed1.8、GPT-4o），其成本没有报告。
- Impact statement 提到：在真实环境中探索可能产生非预期操作，例如删除数据或金融交易，并且含个人数据的截图会带来隐私问题。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **76 分（★★★）**，证据等级 **transfer**。分数反映论文所报告的证据：AndroidWorld 和 AndroidLab 上的在线评测、五个留出应用、较强的基线、组件消融、对学习到的奖励判定器的验证，以及项目主页。判定记录把随机种子与方差、预算对齐标为未报告，并标出记忆或训练数据与评测应用可能重叠的风险（AP5，记录为已由留出应用缓解）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
