# WebAgent-R1：用端到端多轮强化学习训练网页智能体

*CUA Radar 对 arXiv 2505.16421v2（Wei、Yao、Liu、Zhang、Lu、Qiu 等；University of Virginia、Amazon、Georgia Tech）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2505.16421v2 · 代码：https://github.com/weizhepei/WebAgent-R1*

## 问题

强化学习（RL）在 LLM 上最显眼的收益来自单轮任务（如数学）。网页任务不一样：环境随智能体的动作变化，决策链路长，每一步的观察是一页可能几千 token 的 HTML。论文对现有网页智能体 RL 的批评不在算法，而在数据管线：off-policy 与迭代式方法（AWR、DigiRL、WebRL）在旧版本策略生成的轨迹上训练，因此需要 replay buffer、轨迹过滤，或者额外训练的 outcome reward model（WebRL 就训练了一个，用来给 GPT-4 生成的数据打标签）。论文给了一个具体的失败场景：先让智能体登出账号、再让它编辑用户资料时，登出前收集的 off-policy 数据里从来没有“重新登录”这个行为，智能体会一直假设自己仍有权限。on-policy 的端到端 RL 能看到自身动作的后果，但必须先活过多轮上下文膨胀——这正是下面两个工程贡献的由来。

## WebAgent-R1 是什么

这是一个**纯文本**网页智能体，运行在 WebArena 上——一个自托管环境，覆盖五个站点：Reddit（论坛）、GitLab（协作编码）、CMS（内容管理）、Map（开放街图）、OneStopShop（购物）。每一步它观察任务指令加当前页面的 HTML，没有截图、没有 accessibility tree。输出格式为 `<think> ... </think> <answer> ... </answer>`，**每轮只发一个动作**：python 风格的 `do(action, argument, element)`，动作空间固定（Click、Right Click、Type、Search、Hover、Scroll Up/Down、Press Enter、Switch Tab、Select Dropdown Option、Wait、Go Backward/Forward），或者用 `exit(message)` 结束。元素目标用简化 HTML 里的 id。它在 CUA Radar 板上的模式是 **K20**（trajectory-level policy training，父模式“在自身、回放与修正轨迹上训练策略”）——只是这篇论文刻意把“回放”去掉了。

训练分两阶段：

1.  **Behavior cloning（BC）。** 在 WebArena-Lite 公开的 9,460 条轨迹（1,186 个有效训练样本）上做 SFT，模仿专家动作。这个热身阶段决定了后面 RL 能否奏效。
2.  **端到端多轮 RL（M-GRPO）。** 对每个任务，在 **G 个并行浏览器实例**里同时 rollout 一组轨迹——相同起始页、各自独立的 cookies 与上下文——然后用 GRPO 的多轮扩展更新策略：每条轨迹上所有动作 token 的 advantage 都是该轨迹二值奖励的组相对值 (r − mean(r))/std(r)，套进带 KL 正则的 PPO 裁剪目标。loss 只算在动作 token 上。两个机制让它可行：**dynamic context compression**（观察一旦被处理，后续轮次就替换成”Simplified HTML”之类的占位符；动作历史永不丢弃）和基于 vLLM 的并行采样。

**训练信号就是环境自带的规则式二值奖励**（成功为 1，否则 0），来自 WebArena 内置 rubrics：string match、URL match 或对最终页面状态的 program execution。没有 reward model，没有 reward shaping，没有额外数据。

实现：Qwen2.5-3B 与 Llama-3.1-8B 全参数微调，8 张 A100-80GB；SFT 学习率 5e-5、batch 128；RL 学习率 1e-6、batch 16、KL 系数 0.001、clip 比率 0.2、上下文 16,384、新生成 1,024 token。

## 论文报告的结果

以下全部是 WebArena-Lite（165 个人工核验的评测任务；其余 647 个任务作为 RL 训练池）上的**在线**成功率，由规则式 rubrics 判定；论文没有离线的单步指标，也没有报告随机种子与方差。微调基线取论文规则：作者复现值与文献值中的较高者。

| 方法（基座）                                     | 平均 SR            |
|--------------------------------------------------|--------------------|
| Qwen2.5-3B / Llama3.1-8B / Qwen2.5-32B prompting | 6.1 / 8.5 / 16.9   |
| GPT-4o / GPT-4o-Turbo / QwQ-32B prompting        | 13.9 / 17.6 / 22.4 |
| OpenAI o3 / o4-mini prompting                    | 39.4 / 36.9        |
| BC（Qwen2.5-3B）→ **WebAgent-R1**                | 20.0 → **33.9**    |
| BC（Llama3.1-8B）                                | 20.6               |
| Filtered BC / AWR / DigiRL（Llama3.1-8B）        | 23.0 / 28.5 / 30.3 |
| WebRL（Llama3.1-8B）                             | 42.4               |
| **WebAgent-R1（Llama3.1-8B）**                   | **44.8**           |

分站点看（Llama3.1-8B，WebAgent-R1 对 WebRL）：Reddit 47.4 对 63.2，GitLab 56.7 对 46.7，CMS 57.1 对 54.3，Map 23.1 对 36.7，Shopping 44.4 对 31.1——平均值的领先掩盖了两个落后于 WebRL 的站点。

**分布外（OOD）。** 在 WebVoyager 上（每域抽 25 个任务、共 5 个 WebArena 未见过的域，用 Qwen2.5-3B），WebAgent-R1 平均 32%，对比 prompting 的 8.8% 与 SFT 版本的 12%，并且在每个域上都领先（Allrecipes 28%、Amazon 24%、Arxiv 24%、Coursera 44%、Google Map 40%）。

## 论文自带的对照实验

- **初始化消融（Qwen2.5-3B）。** 跳过 BC 的”WebAgent-R1-Zero”从 6.1% 起步，RL 之后反而**掉到 4.8%**——现成模型输出的动作格式残缺，几乎拿不到奖励。用 QwQ-32B 生成的 long-CoT 轨迹做 BC 的”WebAgent-R1-CoT”起点更高（24.5%），但 RL 提升更小（到 30.3%），而普通 BC 是从 20.0% 到 33.9%；作者的解释是确定性的 long-CoT 模式限制了探索。
- **与 WebRL 的公平对比。** WebRL 用了额外的 GPT-4 生成数据，因此在 Llama3.1-8B 上，论文从 WebRL 公开的 checkpoint 初始化自己的 RL，且只用原来的 647 个训练任务。
- **thinking 格式提示。** 仅在提示里加 `<think>` 格式，就把 Qwen2.5-3B 从 3.2% 提到 6.1%、Llama3.1-8B 从 4.8% 提到 8.5%、o4-mini 从 15.9% 提到 36.9%，同时单轮回复长度几乎不变（139 → 142 token），交互轮数上升（3B 从 6 到 17）。论文把这读成一种 test-time scaling 轴：加的是交互轮数而不是单轮长度；另一组分析显示，放宽交互上限后 prompting、SFT 与 RL 方法的成功率都持续上升。

## 论文自己承认的薄弱处

- 纯文本：“our current approach … consider\[s\] only textual input for the web tasks”，而视觉布局与颜色可能有帮助。
- 奖励的可得性：“such reward functions may not be readily available in other interactive scenarios, such as open-ended travel planner agents, where task goals are ambiguous and no clear reference or verifiable outcome is available.”
- 动作空间：模型“trained with a fixed set of predefined actions (e.g. click, type), which can limit its flexibility.”
- 论文自己的清单之外：全文没有种子与方差；RL 探索任务与评测任务是不同任务、但同属五个 WebArena 站点（判定记录把这点标为 AP5，WebVoyager 是对应的 OOD 反证）；训练动态与 test-time scaling 曲线只以图给出、没有印刷数值。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **transfer**，子模式 K20。判定记录肯定了：规则式 rubrics 的在线评测、OOD 基准（WebVoyager）、匹配初始化协议下的强 RL 基线（DigiRL、WebRL）、以及干净隔离 behavior cloning 作用的初始化消融。同时标出：variance 未报告（unclear）、预算匹配 unclear、代码列为 unclear 未核验、以及探索与评测同站点的重叠。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
