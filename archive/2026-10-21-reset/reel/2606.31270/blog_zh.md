# Learning from Failure：把计算机使用智能体的失败轨迹变成推理时补丁

*CUA Radar 对 arXiv 2606.31270v1（Sun、Wang、Schmidt、Yeung-Levy、Zhang；Stanford 与清华大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2606.31270v1 · 摘要列出代码仓库 github.com/snow10072740/Learning_from_Failure（radar 判定记录将代码可得性标记为 unclear）。*

## 问题：成功循环把大多数数据扔掉了

构建计算机使用智能体（computer-use agent）的标准做法是自我改进循环：把智能体放进可验证环境，保留验证器判为成功的轨迹去做 SFT。论文开篇指出，这个循环”exploits only successful trajectories and discards the failed ones, even though failures carry rich information about a model’s weaknesses”——而那些被丢弃的失败轨迹，来自本身”require considerable human engineering effort”才建成的环境。论文的问题很直接：能不能在不做任何训练的前提下，在推理时用失败轨迹升级智能体？

## 这个方法是什么

智能体是开源的 72B 多模态模型 OpenCUA-72B，在 OSWorld 里操作真实电脑：观察 screenshot，用底层鼠标键盘动作（click、moveto、dragto、打字）行动；打补丁之后，动作空间还多了终端（Ctrl+Alt+T 热键打开）和搜索工具。在 CUA Radar 板上，它属于 C19（experience memory retrieval 之下）：从智能体自身运行中积累可复用知识——只是这里积累的不是提示词式的 tips，而是由失败轨迹导出的代码补丁。

循环有三个环节：

1.  **失败收集。** 智能体 rollout，环境自带的 verifier 给每条轨迹打分；失败的轨迹连同 instruction、action history 和思考过程一起保留。
2.  **LLM 诊断。** 作为 meta-controller 的 Claude 4.5 Sonnet（在 GPT-5.2、Gemini 3 Flash、Qwen3-VL-32B-Instruct 中以分析更全面、代码实现更强胜出）逐条阅读失败轨迹，命名失败模式，并把改进方案写成代码补丁。
3.  **轻度人工核验。** 人来选择并微调补丁，再注入智能体的推理流程。论文给了量化：“over 97% of LLM-generated refinements are accepted without modification”，人工修改平均只占”less than 3% of the modified lines”。

循环跑 4 轮，每轮按主导失败模式引入一个策略，策略逐轮累积。四类失败对应四个策略：

- **Grounding error → visual search。** 对 click、moveto、dragto 这类定位动作，截取动作点为中心的 400×400 图块，放大 2 倍，画上半径 7 像素的红色圆圈；智能体基于这个视图复核，可以确认或修正坐标——动作后的视觉自检。
- **Competency gap → terminal execution。** 用热键打开 terminal，把繁琐的 GUI 操作换成命令行。
- **Knowledge deficiency → knowledge support。** 一份人工整理的 LibreOffice 快捷键手册，加上由 GPT-5-mini 支持的搜索接口，补上模型缺少的操作性知识。
- **Redundant loop → repetition warning。** 在最近 5 步的滑动窗口里，同一 thought 或 action 模式出现至少 3 次即告警；对屏幕，用无障碍树的哈希表示连续 3 步不变即告警。告警后进入 recovery mode，鼓励换一条路径。

监督信号就是环境 verifier 的成败判定——但驱动改进的是失败而非成功。全程不更新任何权重。

## 论文报告的结果

**在线、OSWorld 全集、100 步预算、成功率（%）。** 主结果为 3 次独立运行的均值 ± 标准差；带 \* 的行是”due to resource constraints”的单次运行。

| 智能体               | 步数 | 成功率         |
|----------------------|------|----------------|
| Claude 3.7 Sonnet    | 100  | 28.0           |
| OpenAI CUA 4o        | 200  | 38.1           |
| UI-TARS-1.5          | 100  | 42.5           |
| OpenAI CUA o3        | 200  | 42.9           |
| GUI-Owl-32B          | 100  | 19.0 \*        |
| \+ Ours              | 100  | 21.3 \*        |
| OpenCUA-32B          | 100  | 34.5 \*        |
| \+ Ours              | 100  | 38.2 \*        |
| OpenCUA-72B          | 100  | 42.3 ± 2.6     |
| **+ Ours（主结果）** | 100  | **48.9 ± 1.2** |

论文将其表述为绝对提升 +6.6 个点（相对 +15.6%），运行时间”about an 8% increase”，交互步数减少”by roughly 15%“，且没有额外训练开销。两个 32B 基座上报告了稳定的 +10–12% 相对提升。

**消融，OSWorld small set（用于快速迭代的轻量子集），30 步上限，在线。**

| 配置                      | 成功率 |
|---------------------------|--------|
| 基线 OpenCUA-72B（30 步） | 41.67  |
| \+ Visual search          | 47.22  |
| \+ Terminal execution     | 47.19  |
| \+ Knowledge support      | 44.44  |
| \+ Repetition detection   | 44.40  |
| \+ 全部组合               | 52.74  |

正文写明 terminal execution 在该子集上提升 5.52 个点、repetition detection 提升 2.73 个点。

**OSWorld 挖出的补丁跨基准迁移**（Qwen3-VL-32B-Instruct 基座，除 WebVoyager 外均重复 3 次）。论文本身没有区分在线/离线；按 radar 的分类，WebVoyager 是在线基准，AndroidControl 和 ScreenSpotPro 是离线基准，因此不与上面的在线数字同轴比较。

| 基准                     | Base         | Ours         |
|--------------------------|--------------|--------------|
| OmniACT                  | 4.77 ± 0.02  | 6.90 ± 0.10  |
| AndroidControl（离线）   | 28.37 ± 0.13 | 36.23 ± 0.22 |
| ScreenSpotPro（离线）    | 27.50 ± 0.35 | 30.74 ± 0.27 |
| WebVoyager（在线，单次） | 23.80        | 27.90        |

论文特别指出 WebVoyager（+4.10 个点）和 AndroidControl（+7.86 个点）提升最大。

## 论文自带的对照实验

- **公平比较。** 改进后的框架”retains exactly the same tool access, environment configurations, and action spaces as the baseline agents”。
- **组件消融。** 每个策略单独都有效，四者组合（52.74，基线 41.67）高于任何单项；论文据此认为四次叠加的改进可以 constructive 地组合。
- **失败模式迁移。** 按 LLM 分类，action loop 从占失败的 43% 降到 24%，坐标精度错误初始占 24%；剩余失败以 multi-step planning（28%）、UI recognition（24%）、CAPTCHA（12%）、task misinterpretation（12%）为主。论文的解读：低层瓶颈被解决，剩下的属于更高层的认知能力。
- **人工介入被量化。** 超过 97% 的补丁原样采纳，人工改动平均不足 3% 的行。
- **关键处报告方差。** 主结果与四个迁移基准中的三个给出 3 次运行的均值 ± 标准差；32B 跨模型行与 WebVoyager 为单次运行，论文明确标注。

## 证据较薄的地方

- 补丁在 OSWorld 上挖出，头条增益也在 OSWorld 上测得；跨基准表是论文自己的迁移证据，radar 记录也因此把 held-out 评价标为 partial（anti-pattern AP5：合成或记忆数据与评测重叠）。
- 榜单上部分基线的步数是 15、50 或 200 而非 100，这些对比不是预算对齐的。
- meta-controller 的选择（Claude 4.5 Sonnet 对 GPT-5.2、Gemini 3 Flash、Qwen3-VL-32B-Instruct）是定性描述，没有数字表。
- 判定记录将代码可得性标为 unclear，尽管摘要宣告了仓库。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **transfer**，子模式 C19（从智能体自身运行积累可复用知识）。分数反映论文报告了什么——在线 OSWorld 评测、主结果 3 次运行带标准差、成本报告、逐策略消融、跨模型与跨基准迁移——也反映它没报告什么：代码核验，以及榜单上的完全预算对齐。记录同时标出 AP5。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
