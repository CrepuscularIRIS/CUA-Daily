# CHOP：把规划器约束在十个人类高频“基子任务”里的手机操作助手

*CUA Radar 对 arXiv 2503.03743v1（Zhou、Wang、Dai、Jia、Du、Dong、Xu；中国人民大学高瓴人工智能学院与华为诺亚方舟实验室）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2503.03743v1 · 代码：https://github.com/Yuqi-Zhou/CHOP*

## 问题：VLM 自己发明的子任务靠不住

基于视觉语言模型（VLM）的手机操作助手通常是分层的：一个任务（“播放 Bob 的歌”）被分解成子任务（“搜索 Bob”），再落地为底层动作（click、type）。论文认为中间这一层最薄弱，并给出两种失败模式。*Ineffective subtasks（不可执行）*：规划器提出动作代理无法执行的子任务——面对“Ask Bob to attend the meeting”，它可能给出“Go to Bob’s office”，而可行的做法是“Send Bob an email”。*Inefficient subtasks（低效）*：不推动任务进展的步骤，比如“Wait for Bob’s feedback”。作者认为两者都源于“the VLM’s lack of experience in decomposing subtasks within GUI scenarios in multi-agent frameworks”。

## CHOP 是什么

**智能体。** CHOP 运行在真实 Android 设备上，且是 image-only：第 t 步的状态只有当前截图，不用 XML 或 view hierarchy。动作空间共六类——CLICK（屏幕坐标）、SCROLL、TYPE、BACK、EXIT、WAIT——策略为 a<sub>t</sub> = f(s<sub>t</sub>, H<sub>t</sub>)，输入截图与累积历史。三个模块协作：**plan agent** 负责任务分解；**action agent** 以 observation / thought / summary 的叙述方式产出动作；**Aria-UI** grounding 模型把 CLICK(Search Bar) 这类符号指称映射为 CLICK(200, 300) 这样的坐标。平台：mobile（Android），在英文和中文应用环境下分别评测。

**板块模式。** 在 CUA Radar 板上这是 C17 模式：“分解为一个规划子目标的 manager 和执行它们的 workers”（主模式：agent loop context control）。CHOP 是一个干净的实例：plan agent 是 manager，action agent + grounding 是 worker，子任务之间传递 summary memory。

**机制。** 核心想法是 *basis subtask（基子任务）*，类比“基向量”：任何任务都应能分解为人类真正高频执行的子任务的组合。基子任务离线从 AITZ 数据集（AITW 的子集，覆盖四个 app）中挖掘，分四步：用 spaCy 做词性标注提取动词（verb extraction）；用 WordNet synsets 做同义聚类（synonym clustering）；用 GPT-4 把每簇动作序列总结成带边界条件的标准化流程（summarization）；按频率过滤只保留 top 10（Search Item、Send Text Message、Open Section、View Content、Interact、Manage Collections、Share Content、Check Notifications、Modify Settings、Create or Edit Entry）。运行时 plan agent 必须从这个集合里选子任务，并为每个子任务给出目的与停止条件；缺少必要子任务时用 placeholder 让模型自定义。每个基子任务附带 documentation，因此对搜索这类固定流程，action agent 一次前向就能输出整段动作序列。

**训练信号。** 没有——全流程不做任何 fine-tuning，所有约束都在提示词里：受限制的子任务词表和文档。GPT-4o 驱动两个 agent；Aria-UI、spaCy、WordNet 和一次 GPT-4 总结作为固定工具使用。

## 论文报告的结果

以下全部是在线评测：agent 在真实手机上操作，以人类执行轨迹为 ground truth。所有方法（含基线）都用 GPT-4o（规模未说明）、temperature 0.0、最大输出 4096；任务须在 20 个动作内完成才算成功。测试集：CHOP-En，30 条英文指令、10 个 app（easy / medium / hard）；CHOP-ZH，由 10 名标注者构建的 200 条中文指令、10 个 app，因 GPT-4o 成本只运行了其中 30 条（每 app 3 条）。随机种子 / 方差：未报告。成功率（SR）：

| SR               | 英 easy  | 英 med   | 英 hard  | 中 easy  | 中 med   | 中 hard |
|------------------|----------|----------|----------|----------|----------|---------|
| AppAgent         | 0.50     | 0.40     | 0.10     | 0.40     | 0.30     | 0.20    |
| Mobile Agent(v2) | 0.50     | 0.50     | 0.40     | 0.80     | 0.20     | 0.30    |
| Moba             | 0.50     | 0.30     | 0.20     | 0.40     | 0.30     | 0.10    |
| **CHOP**         | **0.80** | **0.70** | **0.60** | **1.00** | **0.80** | 0.10    |

效率方面，论文提出的新指标都偏向 CHOP：Average API Cost（AAC，越低越好）在英文 easy / medium / hard 上为 0.76 / 0.85 / 0.93，而 Mobile Agent(v2) 为 3.62 / 3.65 / 4.42；Mapping Efficiency（ME）大于 1（英文为 1.36 / 1.20 / 1.10），因为固定流程子任务一次调用生成多个动作。英文 Completion Rate（CR）为 0.90 / 0.89 / 0.59。论文没有离线单步准确率基准，上表全部是在线结果。

## 论文自带的对照实验

**消融（CHOP-ZH，Table 3）。** 去掉 documentation，10 个 app 上的 SR 从 0.67 降到 0.47；再去掉基子任务约束，降到 0.33。在 6 个 out-of-domain app 上（基子任务来自 AITZ 的四类 app），从 0.61 降到 0.44 再到 0.22——这是论文“基子任务可泛化而非记忆”的证据。In-domain SR 从 0.75 降到 0.50。

**子任务质量。** 以标注者的计划为参照，加了基子任务约束后，BLEU、ROUGE-L 与 LLM-as-evaluator 三种评估都高于不加约束的同一规划器（Figure 3；论文只以图内标签给出数值）。

**错误分析（Table 4）。** CHOP 的 hallucination、解析错误和超迭代失败均为 0.0%；AppAgent 的失败中 57.1% 是 XML / 输出解析错误，Moba 的失败中 63.6% 是任务上下文误解。CHOP 最大的错误类别是 poor graphical recognition，占 54.6%。

**诚实的负结果。** 在中文 hard 拆分上 Mobile Agent(v2) 胜过 CHOP（SR 0.30 对 0.10），论文将其归因于 CHOP 的 documentation 是英文的。

## 论文自己承认的薄弱处

- 规模与评分：“the current evaluation process relies on manual assessments, which results in a relatively small dataset”——实际只执行了 30 + 30 条指令，未报告种子与方差。
- LLM 子任务评估器没有对照任何外部标准做过验证。
- Moba “requiring additional tools to open the app, which are not available in our dataset”，作者为它改用 Aria-UI 负责启动 app。
- 只研究了 plan/action 之间的接口，“challenges between the action agent and the grounding model” 留给未来工作。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **transfer**。分数反映论文所报告的证据：真实设备上的在线评测、in-domain / out-of-domain app 划分、全部基线使用 GPT-4o、20 动作成功预算、API 成本报告、组件消融，以及公开的代码与数据集。判定记录同时标出未报告项：方差、LLM judge 的验证；并指出循环只是“直到动作为 EXIT 或达到最大轮数”为止。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
