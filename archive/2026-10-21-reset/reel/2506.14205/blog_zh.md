# AgentSynth：让 computer-use 任务”生成容易、求解困难”的可扩展数据管线

*CUA Radar 对 arXiv 2506.14205v2（Jingxu Xie、Dylan Xu、Xuandong Zhao、Dawn Song；UC Berkeley；ICLR 2026）的解读。这是对论文所述内容的第三方总结，不代表作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2506.14205v2 · 代码：https://github.com/sunblaze-ucb/AgentSynth*

## 问题

人工标注无法扩展到通用 computer-use agent。论文自己的核算：OSWorld 用了约 1,800 人时做出 412 个任务（约 4.4 小时/任务；按 \$2–\$25/小时折合 \$8.8–\$110）；TheAgentCompany 报告 3,000 人时做 175 个任务（约 17 小时，\$34–\$425）；τ-bench 约 2 小时，\$4–\$50。合成数据生成已有很多工作，但集中在 web 环境；而让 LLM 一次性”发明一个困难的长程任务并解出它”大多会失败：论文的对照实验里，直接生成式（direct instruction）generator 在 easy（5–10 个动作）目标上只有 64% 能拿到可用的 ground-truth 轨迹，medium 33%，hard 只有 11%（Table 5）。最需要数据难度的任务，恰恰是一次式生成器产不出来的。

## AgentSynth 是什么

**Agent 本体。** 感知输入是 1920×1080 全屏截图（依 tokenizer 约 1k–2k tokens）；动作是 OS 层的 pyautogui 原语，在整个数据集里的分布为 click 59.1%、write 12.1%、press 8.2%、scroll 5.4%、move 5.3%、drag 4.6%、hotkey 3.0%、double-click 1.5%、wait 0.8%。平台是 OSWorld（Gym 兼容的 Ubuntu 桌面虚拟机），同一管线还移植到 InSTA web 环境（61 个任务序列、194 个测试任务）以显示通用性。在 CUA Radar 榜上，这篇归入 K15：依据 agent 的历史与失败来提议新任务。

**机制：information asymmetry（信息不对称）。** 正向逐步解题远比一次性推断完整解法容易。AgentSynth 用六个 LLM 角色利用这一点：

1.  **Task proposer**：从 persona hub 采样人设，提出一个几步内可完成的初始任务（禁止需要登录或发邮件的任务）。
2.  **Executor**：ReAct 风格；GPT-4.1 用自然语言规划下一步，OpenAI 的 computer-use-preview 模型把动作 ground 到像素坐标；每个子任务最多 10 步。
3.  **Verifier**：WebJudge 风格的三段式——抽取任务关键要求、筛出关键截图（降采样），再输出二值成功标签和完成百分比。
4.  **Reviser**：子任务只部分完成时，把任务描述改写成与实际完成动作一致。
5.  **Follow-up proposer**：看全部子任务历史和先前失败的任务，被明确要求提出更简单、且建立在当前状态上的后续任务。
6.  **Summarizer**：把前 n 个已完成的子任务合成一条长程指令——这条摘要就是难度 level n。

**训练/导向信号。** 论文本身不训练模型，产出是一个 benchmark 加轨迹数据集（6,000+ 任务）。塑造数据的信号是 verification：只有验证通过的子任务才被串接，失败任务反馈给下一轮提议。难度是一个旋钮：level 1→6，平均 horizon 从 5 步涨到 45 步，memory span 从 2 到 18，涉及应用数从 1.2 到 3.3，应用切换从 0.5 到 4.3；level-6 任务通常需要 40–60 步，超过 60% 的轨迹涉及两个及以上应用、超过 40% 涉及三个以上。

**成本。** 每条轨迹 \$0.60（典型轨迹为 6 个子任务共约 50 步，每步约 \$0.011；GPT-4.1 每百万 tokens \$2、computer-use-preview \$3、验证用的 GPT-4.1-mini \$0.40）。一条序列可总结出 6 个任务，折合每个任务 \$0.1。论文给的对比：AgentTrek \$0.55、Explorer \$0.28、InSTA \$0.27 每条轨迹。

## 结果（照论文报告）

以下均为 OSWorld 上的在线任务成功率，由论文的自动 verifier 判定，每个难度级 50 个任务，裸 LLM 直接输出 pyautogui 代码。Table 6（带 Agent S3 scaffold）：

| 设置（eval 模型 + 生成模型）  | L1  | L2  | L3  | L4  | L5  | L6  |
|-------------------------------|-----|-----|-----|-----|-----|-----|
| GPT-4.1 + S3，GPT-4.1 生成    | 36  | 18  | 14  | 14  | 10  | 10  |
| GPT-5.1 + S3，GPT-4.1 生成    | 62  | 32  | 20  | 22  | 16  | 14  |
| GPT-5.1 + S3，GPT-5-mini 生成 | 60  | 34  | 18  | 20  | 18  | 16  |
| GPT-5.1 + S3，GPT-5 生成      | 58  | 28  | 18  | 16  | 14  | 14  |
| GPT-5.1 + S3，GPT-5.1 生成    | 56  | 30  | 16  | 18  | 14  | 12  |

裸 LLM（Figure 4）方面，正文写明：o4-mini 从 level 1 的 18% 跌到 level 5、6 的 4%；GPT-4.1 在 level 3 之后完全失败；level 4 和 6 只有 o4-mini 和 Claude-3.7 非零、约 4%。人类在 20 个采样的 level-6 任务上达到 70%。加 Agent S3 scaffold 后弱模型（o4-mini、GPT-4.1）在 level 1 上成功率约翻倍，且各难度都高于裸模型；中间档的 Agent S2.5 提升幅度类似。InSTA web 移植中，总结式任务明显更难：gpt-4.1 从 40% 降到 12.9%，o4-mini 从 12% 降到 6.45%。论文没有报告任何离线 step/grounding 准确率；以上全部是在线评测。

## 论文自身的对照实验说明什么

**信息不对称 ablation（Table 5）是承重墙。** 生成成功率：direct instruction 64/33/11（easy/medium/hard）对比 AgentSynth 65/57/52（level 1/3/6）——恰好在一次式生成崩溃的难度区间，串接式仍能稳定拿到轨迹。评测成功率（Agent S3，GPT-5.1）：direct 60/51/48 对比 AgentSynth 62/20/14——被留下来的 direct 任务对 eval agent 仍然偏容易，说明只靠过滤一次式产物做不出困难的 benchmark。

**换生成模型（Table 6）。** 用 GPT-5-mini、GPT-5、GPT-5.1 重跑整条管线：结论定性不变；更强的生成器得到的评测成功率略更低，作者解读为任务更难或更多样。

**Verifier 验证。** 100 个样本的人工审计：可行性 91%、子任务连贯性 90%、persona 相关性 94%、verifier 准确率 88%，标注者间一致性 0.74（Cohen’s kappa）。与人工分级完成度的校准曲线单调。对抗压力测试中，near-miss 变体只被错误接受 12%，benign UI 变体被正确接受 94%。

## 证据较薄的地方

- 主结果的 OSWorld 评测没有报告随机种子或重复运行，是单一成功率（2-sigma 误差条只出现在 InSTA 附录图上）。
- 任务生成与评测都在同一个 OSWorld 环境里，没有在生成时排除、评测时才使用的 held-out 应用或网站。
- 成功与否由作者自己的 LLM verifier 判定——虽然做了上面的压力测试，但不是 ground-truth 判定器。
- 裸 LLM 各难度值只存在于 Figure 4 的图内标注；正文只给了上面引用的端点数字。
- 关于生成模型的选择，论文自己说”remains an open and interesting research question”——任务的复杂度与真实性校准可能继承 GPT-4.1 的偏好。

## CUA Radar 的读法

CUA Radar 给本文 **64 分（★★）**，evidence level 为 **online**，子模式 K15（依据历史条件化地提议任务），隶属于 exploration-driven task synthesis。评分对应论文实际报告的内容：在线 OSWorld 评测、单条轨迹成本、信息不对称 ablation 加生成器替换 ablation、经过测试的 validator、scaffold 对照（Agent S3）、以及公开代码。judgment record 同时标注：held-out 环境不明确、方差未报告、各设置之间预算只是部分对齐、在线成功率由论文自己的 verifier 判定。Radar 没有复跑任何实验；本文所有数字均来自论文（版本 v2）。
