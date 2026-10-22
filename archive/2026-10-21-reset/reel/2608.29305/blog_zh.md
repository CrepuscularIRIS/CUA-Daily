# TTED：把每个页面拆成子目标和子观察，再从自己的判断中学习的 web agent

*CUA Radar 对 arXiv 2608.29305v1（Li、Liu、Huang、Li、Liu、Yan、Liu）的解读。这是第三方对论文所报告内容的总结，并非作者背书。海报：`poster.png`。论文：https://arxiv.org/abs/2608.29305v1 · 代码：https://github.com/THUNLP-MT/TTED*

## 问题：单个部件简单，放在一个杂乱页面里就不行

真实网站常把多个功能部件放在同一屏：搜索面板、表单字段、内容容器、弹窗。论文的出发点是：一个能单独处理每个部件的 agent，在它们同时出现时仍可能失败。作者在 CompWoB+ 上测了这一点，它是作者用任务生成器对 CompWoB 做的扩展（10 个基础任务，每次组合 3 到 8 个，每种规模 100 个任务，共 600 个）。Qwen3-8B 的成功率从 3 个组件时的 85% 降到 8 个组件时的 19%；GPT-4o-mini 从 97% 降到 46%。论文认为这也会伤害 test-time learning，原因有两个：杂乱页面里探索的成功率更低，agent 的自我评估也更不准。

## TTED 是什么

TTED（Test-Time Environment Decomposition）是一个不需要真值标签的 web agent。每一步，agent 看到任务目标、当前观察（WebArena 和 WorkArena 通过 BrowserGym 用 accessibility tree，CompWoB+ 用原始 DOM）以及按步骤摘要组成的历史；它通过 BrowserGym 动作行动，CompWoB+ 上则用 `clickxpath` / `type`。在 CUA Radar 板上它属于 C13 模式，即 structured screen observation。

新意是一个显式的试探步，分四个小步，全部由同一个 LLM 完成：

1.  **Decompose（分解）。** 根据目标、观察和历史预测一个局部 sub-goal，再抽取与之相关的那部分观察作为 sub-observation。两者合起来是一个“子环境”，保持原来的动作空间和动力学。
2.  **Act（行动）。** 根据 sub-goal、sub-observation 和历史生成动作。
3.  **Self-assess（自评）。** 同一个模型充当生成式奖励模型：给 sub-goal 和 sub-observation 各打 0 到 5 分，并把动作判为 pass 或 reject。通过需要分解得分超过阈值且动作被接受；reject 会触发重试（ICL 设置中最多 3 次）。
4.  **Summarize（摘要）。** 通过的步骤被总结后加入历史。

随后 agent 用两种方式之一从这些经验中学习。在 CompWoB+ 上用 in-context learning（ICL）：只保留通过的步骤作为最终运行的示例；对静态页面，用 Selenium 和模型写的 JavaScript 加强检查。在 WebArena 上用 RL：通过和被拒绝的试探都保留，分数映射成 \[-1, 1\] 的回报，用带批内 advantage 归一化（来自 REINFORCE++）的 off-policy REINFORCE 式更新，同时训练分解和动作策略。评测时去掉自评，agent 在完整环境里直接运行。

## 论文报告的结果

下面都是 Qwen3-8B 的 online 任务成功率（%）。WebArena 数字用的是 812 个任务中的 561 个（Reddit 任务因环境无法稳定运行被去掉），评分用 GPT-5-mini 的模糊匹配替代 GPT-4o-Turbo；这个评分器不用作奖励。WorkArena 不做训练。每个任务最多 15 步。

| 方法             | 子环境数 | WebArena | WorkArena |
|------------------|----------|----------|-----------|
| Qwen3-8B，无适应 | 0        | 12.1     | 18.2      |
| SFT（真值）      | 3200     | 14.1     | 17.9      |
| RL（真值）       | 3200     | 14.8     | 17.3      |
| TTRL             | 3200     | 13.5     | 未报告    |
| TTT (SFT)        | 3200     | 11.2     | 18.2      |
| TTT (RL)         | 3200     | 12.5     | 17.3      |
| TTED (SFT)       | 3200     | 17.6     | 21.8      |
| TTED (RL)        | 800      | 19.4     | 未报告    |
| **TTED (RL)**    | 3200     | **21.0** | **22.7**  |

在 CompWoB+（ICL，每种规模 100 个任务）上，TTED 把 8 个组件时的成功率从 19% 提高到 61%（Qwen3-8B），从 46% 提高到 88%（GPT-4o-mini）。这些全部是 online 结果；论文没有 offline 的 step accuracy 基准。

## 论文自带的对照说明了什么

**消融。** WebArena 上、相同 RL 预算：完整 TTED 为 21.0，去掉 sub-observation 分解为 15.0，去掉 sub-goal 分解为 12.4，两者都去掉为 12.5（即 TTT 基线）。论文把 sub-goal 下降解读为：没有局部目标，agent 会失去方向。

**基线与预算。** test-time 基线使用相同的子环境预算。TTED 在 800 个子环境时（19.4）已超过 3200 个子环境的真值 RL（14.8）。在扩展实验表中，TTT 停在 13 左右，TTED 随预算上升；作者报告 advantage 归一化很关键：用普通 REINFORCE 时 TTED 为 17.6，用 GRPO 为 17.8。

**评判器。** 在 82 个 WebArena 任务上，与人工奖励标签的一致性（normalized AD）：TTED 为 0.85，TTRL 的自洽标注为 0.68，TTT 的评判器为 0.71。两位标注者之间的 Cohen’s kappa 也是 0.85。

**成本。** 每个任务的平均步数从 4.72（基座）升到 8.29，而每次动作的 prompt token 从 6338.9 降到 3948.2。在 8 张 A100-80GB 上，GPU 小时数为：TTED 14.80，TTT 14.40，真值 RL 8.67；论文自己写道，TTED 是用额外的探索成本换取更有效的适应，并非没有代价。

**另一个模型规模。** Qwen3-14B 在 WebArena 上：基座 19.3，真值 RL 20.0，TTT 18.7，TTED 22.5。论文的单侧检验给出这些提升的 p 值依次为 0.093、0.153 和 0.061，所以提升为正，但在常用水平上不显著。

**重复运行。** WebArena 主结果重复了三次，绝对波动小于 0.5%。TTED 的 95% Wilson 区间为 \[17.9, 24.6\]，基座模型为 \[9.7, 15.1\]。

## 证据偏薄之处（用论文自己的话）

- 适应和评测用的是同一批任务。论文把 RL 描述为在 WebArena 上“适应一次”，并在“同一个基准分布”上评测；只有 WorkArena 是不经进一步训练直接评测。这是 transductive 的无标签设置，不是 held-out。
- 奖励信号来自 agent 自己的判断。论文的 limitations 说这会带来“继承自基座模型本身的偏差和噪声”；上面的人工检查覆盖 82 个任务，报告的是一致性，不是假阳性和假阴性率。
- 在 CompWoB+ 上，目标分解会拿到组成该数据集的基础任务名称（附录 E）。
- WebArena 子集共 561 个任务；论文没有在训练中途用 WebArena 测试 checkpoint，而是取最后一个 checkpoint；剩余失败主要被归因于动作空间不对齐或过度思考。作者称 TTED 是“基础原型，而不是可用于生产的系统”。
- 更大的闭源模型只作为背景列出：GPT-4o 为 23.5，GPT-5.5 在完整 WebArena-Verified 上为 67.3，使用的验证器不同。

## CUA Radar 的解读

CUA Radar 给这篇论文打 **69 分（★★）**，证据等级 **transfer**。记录认可：online 评测、不经进一步训练的 WorkArena 迁移、匹配的训练预算、成本报告、组件消融，以及对奖励标签的人工检查。它同时标注：评判器的假阳性和假阴性没有被检查，且方法在被测试的任务上做适应。记录里 variance 和 code 为 unclear，但论文在附录里报告了重复运行，并给出了代码仓库链接。CUA Radar 没有重跑任何实验；本文所有数字都来自论文（版本 v1）。
