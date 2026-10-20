# Behavior Judge：并行跑多条桌面 agent rollout，给每条写“行为叙述”，再通过比较选出最好的一条

*CUA Radar 对 arXiv 2510.02250v2（Gonzalez-Pumariega、Tu、Lee、Yang、Li、Wang）的解读。这是第三方对论文所报告内容的总结，并非作者背书。海报：`poster.png`。论文：https://arxiv.org/abs/2510.02250v2*

## 问题：多跑几次很容易，知道哪一次做对了很难

computer-use agent 同一个任务可能这次成功、下次失败，因为小错误会在几十步里不断累积。论文认为，在单条 rollout 内部做 scaling（例如逐步的 best-of-N，由 judge 在每一步从候选动作里挑一个）收益有限，因为它会让 agent 一直沿着当前的计划走。论文的替代方案是 wide scaling：并行生成多条完整的 rollout，再从中选一条。作者指出不同 agent 会在不同任务上成功，所以上限确实存在，但瓶颈在评估。用他们的话说，“生成多条 rollout 很直接，\[但\] 可靠地判断哪条长程轨迹是正确的却不然”：轨迹信息密集且多模态，大部分细节与成败无关，许多任务有多种合法解法，脚本式的检查器未必认得出来。

## BJudge 与 Agent S3 是什么

这个 agent 在桌面上工作：输入是截图，动作通过 `agent.click(...)`、`agent.type(...)` 之类的调用执行，或者把某一步交给 coding agent，在沙箱 VM 里运行 Python 或 Bash。coding agent 在 OSWorld 和 WindowsAgentArena 上启用，在 AndroidWorld 上关闭，因为模拟器不允许执行程序。论文基于 Agent S2 做了一个更强的基座 agent **Agent S3**：去掉 manager-worker 层级，改成可以随时重新规划的扁平策略，并加入 coding agent。在 CUA Radar 板上，该方法属于“模拟前瞻与选择”一类，子模式 K02，即 verifier 重排。

**Behavior Judge（BJudge）** 有两个组件。

1.  **行为叙述生成。** 对每一步，VLM 看到动作前的截图、动作本身、以及动作后 3 秒的截图（用来捕捉延迟出现的效果），写出与任务相关的事实。对指针类动作，生成器还会拿到点击位置的标记和结果区域的放大裁剪，因为这类步骤最容易出现幻觉。一条叙述保留首张截图、逐步的事实和最后一张截图。
2.  **比较式评估。** 一个 VLM 在一个多选提示里同时看到所有叙述，被要求引用并对比各条叙述中的事实，最后给出要提交的 rollout 的编号。作者选择单轮而不是锦标赛式比较，原因是 token 成本和速度。

因此监督信号就是 judge 自己的比较；没有训练任何权重。最佳配置使用 GPT-5 和 Claude Opus 4.5 各 5 条 rollout，由 Opus 写事实，GPT-5 负责选择。

## 论文报告的结果

OSWorld，361 个任务，100 步预算，成功率（%）。全部是 online 执行，由基准的脚本评分。

| 方法                         | 模型                   | 成功率   |
|------------------------------|------------------------|----------|
| Agent S2                     | GPT-5                  | 48.8     |
| CoAct-1                      | OAI CUA + o3 + o4-mini | 59.9     |
| Agent S3                     | GPT-5 Mini             | 49.8     |
| Agent S3                     | GPT-5                  | 62.6     |
| GTA1（逐步 scaling）         | GPT-5                  | 63.4     |
| Agent S3 + WebJudge (N=10)   | GPT-5 Mini             | 50.4     |
| Agent S3 + BJudge (N=10)     | GPT-5 Mini             | 60.2     |
| Agent S3 + BJudge (N=10)     | GPT-5                  | 69.9     |
| **Agent S3 + BJudge (N=10)** | GPT-5 + Opus 4.5       | **72.6** |

论文把 72.6 描述为比此前最佳 63.4 高 9.2 个百分点，并高于它引用的人类水平 72.36。Agent S3 的 62.6 是 10 次运行的平均。在其他基准上（N=3）：WindowsAgentArena 100 步为 56.6，Agent S3 为 50.2；AndroidWorld 为 71.6，对比 68.1。Agent S3 本身在 GPT-5 下与 Agent S2 相比，每个任务的 LLM 调用为 35.12 次对 73.62 次，耗时 891.21 秒对 2366.80 秒。

## 论文自带的对照说明了什么

**等 rollout 预算。** WebJudge 基线是作者自己的改写：对每条轨迹独立打 1 到 5 分，取最高分。在 GPT-5 Mini 的 rollout 上，它在 N=4 附近略有提升，然后进入平台期，在 N=10 附近下降，而 BJudge 继续随 N 提升。

**轨迹表示。** 在相同的 10 条 GPT-5 Mini rollout 上：行为叙述 60.2，对每张截图单独写 caption 56.8，只用截图 56.0，轨迹摘要 55.0（比最佳基线高 3.4 个百分点）。

**Judge 的准确率。** 在至少有一条 rollout 正确、一条错误的 159 个任务上，BJudge 选中脚本判定正确的 rollout 的比例是 78.4%；对其余情况做人工核查后是 92.8%；在整个任务集上这两个数字分别是 69.9% 和 76.3%。在核查的 12 个失败里，8 个是叙述生成的幻觉，4 个是代码到 GUI 的交接失败。

**资源与组合。** 总预算较小时，单个 agent 最好。N=4 的 BJudge 在总预算翻倍（200）时比单个 agent 高 4.25 个百分点，最大的提升 6.38 个百分点出现在 N=10、预算 1000 的设置。在混合模型研究里，GPT-5 + Opus 达到 71.6，多样性最高的组合任务覆盖率最高，为 80.5。

**成本。** 使用 GPT-5，每个任务：一次 rollout 0.72 美元，叙述生成 0.11，对 10 条 rollout 的评判 0.03；完整的 N=10 运行耗时 17 小时 33 分钟。

## 证据偏薄之处（用论文自己的话）

- Table 1 的说明写道 72.6 这个组合是“从 Table 5 中选出的”，而 Table 5 本身就是在 OSWorld 上跑的，并且 Table 5 里 GPT-5 + Opus 在 N=4 条 rollout 时是 71.6，所以头条数字既包含了借助基准做出的选择，也用了更大的 N。
- BJudge 的数字没有报告方差；只有 Agent S3 的 62.6 被说明是 10 次运行的平均。
- Judge 是对照 OSWorld 的脚本来检查的，而论文自己说这些脚本“只能严格评估一种预先设定的解法”；92.8% 这个数字依赖作者自己的人工检查。
- 方法“假设存在能从同一初始状态产生多条独立 rollout 的 agent”；在真实桌面或共享的在线状态上，这一假设可能不成立。
- 论文正文没有给出代码仓库链接。

## CUA Radar 的解读

CUA Radar 给这篇论文打 **68 分（★★）**，证据等级 **transfer**。记录认可：online 评测、向 WindowsAgentArena 和 AndroidWorld 的迁移、强基线、等 rollout 预算、成本报告、表示方式消融以及 judge 准确率检查，没有标注任何 flag。BJudge 的方差和代码在记录中没有被报告。CUA Radar 没有重跑任何实验；本文所有数字都来自论文（版本 v2）。
