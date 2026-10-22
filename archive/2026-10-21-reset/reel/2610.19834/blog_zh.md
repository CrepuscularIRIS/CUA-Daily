# WebKD：让黑盒教师用学生自己的文风，改写小模型网页智能体的失败轨迹

*CUA Radar 对 arXiv 2610.19834v1（Md Farhan Ishmam、Kenneth Marino，犹他大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.19834v1 · 项目页：https://web-teach-kd.github.io/ · v1 无公开代码（随附补充材料，录用后放出）。*

## 问题：只能”对话”的教师怎么蒸馏

前沿网页智能体能力强但成本高，论文的核心问题是：一个黑盒前沿教师的能力，有多少可以”仅通过文本”（through text alone）蒸馏进一个小型开源权重网页智能体。闭源教师不暴露 logits，因此 token-level knowledge distillation、reverse-KL 目标和 on-policy distillation 全都不可用。标准做法是在教师示范上做 behavior cloning，但它”在学生从未访问过的状态上、用它不会写的文风训练学生”（trains the student on states it has never visited, and in a style it does not write in）。经典修正也不合适：DAgger 只重标 action；让教师从失败点接管，得到的后缀在状态和文风上都是 off-policy。论文把诊断归纳为一个 perplexity premium（困惑率溢价）：教师的修正对学生而言非常意外，是其自身步骤困惑率的数倍，在推理（reasoning）部分”最高可达一个数量级”，而 action 本身离学生分布近得多。在均匀 SFT 下，损失集中在教师的措辞而不是它的决策上。

## WebKD 是什么

智能体是 BrowserGym + AgentLab harness 下的文本网页智能体，运行于容器中的桌面网站。它观察目标（goal）、页面的 accessibility tree（AXTree）序列化结果，以及自己的响应历史（截断到最近一次观察）；历史只有靠 agent 写下来的内容才能延续。每步输出五段式响应：think、plan、step、memory、action；只有 action（click、fill、goto、send msg 等 BrowserGym 命令）会被执行，think/plan/memory 构成跨步持久化的 scratchpad。学生模型为 Qwen 3.5 4B / 9B 与 Gemma 4 E4B；教师是 GPT-5.5，在同一 harness 下运行，没有任何特权输入。在 CUA Radar 板上，本文属于 K26 模式（在第一个错误处构造纠错训练数据），隶属 trajectory-level policy training。

WebKD 只跑一轮，四个阶段：

1.  **P1，BC 种子。** 在成功的教师 rollout 上微调基座模型，然后冻结。
2.  **P2，采样。** 种子学生在训练任务上以 temperature 0.01、30 步预算采样；失败轨迹作为编辑底料，成功轨迹构成文风池。
3.  **P3，定位。** 每条失败轨迹一次教师调用，返回最早把轨迹推向失败的步骤；前缀原样保留。（论文证明：在有限预算和确定性转移下，这样的 first fatal step 存在且唯一。）
4.  **P4，按学生文风改写。** 后缀每步一次教师调用，条件是学生当时看到的那份观察，外加 K = 3 条学生自己写作的逐字示例；编辑从不执行；grounding filter 剔除 9.9% 的被编辑步骤。

得到的语料再从种子出发，用”溢价感知”目标训练：每个 rationale span 按 Δ_s 加权——它对”被纠正 action 概率”的 leave-one-out 贡献，由冻结学生自己打分（不需要教师 logits）；再加一个 role-asymmetric KL 锚（γ = 1 作用于 think/plan/memory，≈ 0 作用于 action/step，β = 0.03），让 action 自由跟随教师的决策，而推理保持在学生先验附近。训练信号因此是：教师的文本 + 学生自身的对数概率。

## 论文报告的结果

以下全部是在线成功率（论文没有离线单步准确率指标），3 个种子的均值，附标准误；TimeWarp v6 在训练中见过，v1–v5 留出，v6 共 103 个任务。Qwen 3.5 4B 一组（表 1）：

| 方法 · Qwen 3.5 4B    | v1       | v2       | v3       | v4       | v5       | v6（见过） |
|-----------------------|----------|----------|----------|----------|----------|------------|
| Behavior Cloning (TW) | 27.5     | 28.5     | 27.8     | 26.2     | 28.2     | 29.8       |
| m-GRPO                | 30.1     | 27.2     | 26.2     | 28.2     | 30.1     | 30.4       |
| Off-policy takeover   | 24.4     | 24.3     | 25.2     | 23.3     | 27.2     | 25.6       |
| **WebKD**             | **37.9** | **36.3** | **35.3** | **38.8** | **36.9** | **41.1**   |

Zero-shot 在 v6 上为 1.0，只克隆 action 的 BC 为 9.7，说明不训练根本做不了这些任务。在见过的 v6 上，WebKD 相对最强基线提升 10.7 pp（Qwen 3.5 4B，41.1 对 30.4）、8.1 pp（Qwen 3.5 9B，34.6 对 26.5）、5.5 pp（Gemma 4 E4B，39.8 对 34.3 的 takeover）；在未见过的 v1–v5 上领先最强基线 3.0–10.6 pp，见过与未见版本之间的差距保持在 5 pp 以内。教师本人在 v6 上为 70.9。在真实网络上（Online-Mind2Web），“所有方法的数字都很低（低于 8%）”；WebKD 是唯一明显拉开差距的方法，对 9B 学生大约把最强基线翻倍，但增益集中在较简单、步数更短的任务上。

## 论文自带的对照实验

**谁来编辑、用什么文风（表 2，Qwen 3.5 4B）。** 教师编辑 + 学生文风（in-context）达到 41.10；教师编辑 + 教师文风 33.01；学生提出、教师判定/修复 27.83；两遍式的学生重写文风 25.89；学生自编辑 24.27；off-policy 教师接管 17.48。论文的解读：没有外部信号，学生无法可靠判断自己哪一步错了。

**目标函数（表 3）。** WebKD 加权损失 + KL 锚为 41.10，同锚下均匀 cross-entropy 为 37.43，grounding 与 consistency 加权均为 37.54，去掉锚的 WebKD 损失为 38.51——相对其他 token 加权方案领先 3.6 pp。扫描锚强度，β = 0.03 最好。

**不是多训几轮就行。** 把 BC (TW) 训得更久，9B 学生在 0.24 到 0.26 之间平台化；加上 WebKD 则持续上升，到第 3 个总 epoch 最佳。

**教师能力重要。** 换 Claude Opus 5 或 Qwen-3.8 27B 做编辑（相同提示与文风示例），学生分别只有 33.3 和 26.9，而 GPT-5.5 为 41.1。

**定位审计。** 200 条失败轨迹、两位互盲的人工标注者：按严格预算口径，教师从不迟到（93% 偏早、7% 精确）；按”进入死循环”口径，约 10% 偏晚。

**增益从哪来。** WebKD 约 8.7% 的轨迹陷入循环（zero-shot 约 97%、BC 约 62.5%），到达正确页面 202 次，没有任何基线超过 143；它最大的剩余失败是”页面对了、答案错了”（约 24.3%）。按任务类型：下单 +25.9 pp（从 0% 到 25.9%）、计数/列举 +9.5 pp（11.9% 到 21.4%）、lookup +8.7 pp、multi-hop +5.7 pp、verification +4.8 pp。蒸馏主要剪掉冗余动作——滚动 −99.7%、按键 −24.5%、send msg +12.3%——其中验证步骤与答案 +14.6 pp，走出循环 +9.4 pp。

**成本。** BC 阶段 4,448 次教师调用（21.8 M prompt tokens）；纠正阶段（15 次定位 + 403 次编辑）占整个流水线 26.3 M prompt tokens 的 17%。一次微调在单张 H200 上用 1.0 GPU 小时；训练后的 4B 学生每步中位数 6.10 s（每 episode 38.8 s），而教师作为 agent 是每步 12.80 s（每 episode 68.1 s）。

## 论文自己承认的薄弱处

- （关于 Online-Mind2Web）“The gains are mostly concentrated on the easy tasks, which have a shorter horizon”（增益主要集中在较简单、步数更短的任务上）。
- 按任务类型的拆解”应当谨慎解读：只有下单和计数/列举两项的 95% 置信区间不包含零”（每类只有 9–29 个样本）。
- “The student still reaches only about half of the teacher’s success rate”（学生仍只达到教师成功率的大约一半），改进空间很大。
- 模仿学习界里的教师项”是一个估计，而非对该项的直接测量”；它基于 15 条种子失败轨迹计算，教师接管能解出其中 14 条。
- 终局奖励由 LLM judge 给出；论文没有把 judge 与真值做对照验证，任务/judge 缺陷在各方法间大致恒定（标注出的为 8–12 条轨迹）。
- v1 没有公开代码；论文称源码在补充材料中、“录用后公开发布”。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **62 分（★★）**，证据等级 **transfer**。分数反映论文报告的证据：TimeWarp v1–v6 与真实网络的在线评测、留出的界面版本、3 个种子附标准误、强基线（BC、outcome-reward RL、多种教师编辑变体），以及覆盖编辑来源、文风和目标函数的组件消融。判定记录将预算对齐与成本报告记为 unclear、代码记为 unclear、judge 验证记为 untested，并标出增益集中在较简单、步数较短的任务上。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
