# ReasoningBank：从自己的成功与失败中学习策略的 web agent

*CUA Radar 对 arXiv 2509.25140v2（Ouyang、Yan、Hsu、Chen、Jiang、Wang、Han、Le、Daruki、Tang、Tirumalashetty、Lee、Rofouei、Lin、Han、Lee、Pfister）的解读。这是第三方对论文所报告内容的总结，并非作者背书。海报：`poster.png`。论文：https://arxiv.org/abs/2509.25140v2 · 代码：https://github.com/google-research/reasoning-bank*

## 问题：agent 会忘记刚学到的东西

面对一连串任务的 web agent，通常每个任务都从零开始。确实保存记忆的系统，往往要么存原始轨迹（太长、噪声大，难以直接复用），要么只存从成功中提炼出的例程（让 agent 自己的失败白白浪费）。论文认为，这样的记忆只是被动的记录，而不是能迁移到新任务上的指导。

## ReasoningBank 是什么

ReasoningBank 是为 ReAct 风格的 agent 设计的一个记忆闭环；不训练任何东西。agent 通过 BrowserGym 看到文本形式的 accessibility tree，用 web 操作行动（在 SWE-Bench-Verified 上用 bash）。任务一个接一个到达，记忆从空开始，测试时没有任何真值反馈。在 CUA Radar 板上，这篇论文属于 C19 模式，即从 agent 自身的运行中学习可复用的知识。

对每个任务：

1.  **检索。** 对任务查询做嵌入（gemini-embedding-001），按余弦相似度取最相似的 top-k 条记忆，默认 k = 1；这些条目被放进 agent 的 system prompt。
2.  **行动。** 运行 agent，最多 30 步，得到一条轨迹。
3.  **自评。** 同一个 LLM 以 temperature 0 读取查询、轨迹和最终页面状态，把它标为成功或失败。这是唯一的正确性信号。
4.  **提取。** 从成功中提炼“为什么有效”，从失败中提炼教训和陷阱。每条轨迹最多产生三条记忆，每条由标题、一行描述和一段策略内容组成。
5.  **整合。** 新条目直接追加；不合并也不剪枝。

**MaTTS（memory-aware test-time scaling，记忆感知的测试时扩展）** 为每个任务多花算力，来产生更好的记忆。并行版本中，agent 产生 k 条轨迹并相互对照（self-contrast）来整理记忆；顺序版本中，它对一条轨迹自我改进 k 次，并把中间笔记保留为信号。Best-of-N 的挑选同样由 LLM 完成。

## 论文报告的结果

online 的 WebArena，684 个任务（因为网站问题排除了 Map 领域），总体成功率（%），pass@1。MaTTS 一行使用 k = 5 的并行扩展。

| 方法                | Gemini-2.5-flash | Gemini-2.5-pro | Claude-3.7-sonnet |
|---------------------|------------------|----------------|-------------------|
| No Memory           | 40.5             | 46.7           | 41.7              |
| Synapse（轨迹记忆） | 42.1             | 47.7           | 42.6              |
| AWM（工作流记忆）   | 44.1             | 47.6           | 40.8              |
| **ReasoningBank**   | **48.8**         | **53.9**       | **46.3**          |
| \+ MaTTS, k = 5     | 51.8             | 56.3           | 48.8              |

论文给出的提升是：相对无记忆 agent 分别为 +8.3、+7.2 和 +4.6。在 SWE-Bench-Verified 上，Gemini-2.5-flash 的解决率从 34.2 升到 38.8，Gemini-2.5-pro 从 54.0 升到 57.4。WebArena 上的平均步数相比无记忆最多减少 1.4。Mind2Web 是 offline：用 Gemini-2.5-flash，任务级成功率在 cross-task 从 3.3 升到 4.8，cross-website 从 1.7 升到 2.3，cross-domain 从 1.0 升到 1.6，绝对值很小。

## 论文自带的对照说明了什么

**把失败作为记忆来源**（WebArena-Shopping，Gemini-2.5-flash）。加入失败轨迹后，ReasoningBank 从 46.5 提高到 49.7，而 Synapse 从 40.6 变为 41.7，AWM 则从 44.4 降到 42.2。

**带记忆的扩展。** k 从 1 增加到 5 时，并行 MaTTS 从 49.7 升到 55.1，顺序版本从 49.7 升到 54.5。没有记忆时，扩展的结果在 39.0 到 42.2 之间波动（并行）、在 37.4 到 40.6 之间波动（顺序）。在 k = 5 时，MaTTS（并行）达到 55.1，普通的测试时扩展为 52.4；顺序版本为 54.5 对 51.9。

**成本。** 每个任务的总 token 数：ReasoningBank 为 53054.5，无记忆为 50847.4，Synapse 为 58514.7，AWM 为 59372.8；论文把增加的幅度描述为约 4.3%。

**评判器。** 在 Shopping 子集上，自评判器对照真值标签的准确率是 72.7%。当作者通过翻转标签来模拟准确率更低的评判器时，他们报告在 70% 到 90% 的准确率区间内成功率相近。

**更小的模型。** 在 Shopping 上用 Gemma-3-12B-Instruct，成功率为：ReasoningBank 24.1，无记忆 17.1，Synapse 16.0，AWM 21.4。

## 证据偏薄之处

- 没有报告随机种子、标准差或区间；主表只给出单个数字。
- Table 1 中的 MaTTS 一行每个任务使用五条轨迹（best-of-N），而其他行只用一条，所以它并没有按算力匹配。
- 消融和扩展研究使用的是同一个子集（Shopping，187 个任务）和同一个骨干模型；Multi 子集只有 29 个任务。
- 正确性信号是 agent 自己的评判器，在被检查的地方准确率为 72.7%，CUA Radar 的记录对此打了标记（反模式 AP4）；鲁棒性检查是在一个子集上的模拟。
- 任务按顺序从同一个基准到达；论文没有描述单独的 held-out 任务划分，CUA Radar 的记录把 held-out 评测标为 partial。
- Mind2Web 上的提升在绝对值上很小。

## CUA Radar 的解读

CUA Radar 给这篇论文打 **66 分（★★）**，证据等级 **online**。记录认可：WebArena 的 online 评测、Synapse 和 AWM 基线、步数与 token 的报告、失败样本消融、评判器准确率检查以及已发布的代码。它标注了没有双向验证的自评判器（AP4），并把随机种子、方差和 held-out 任务记为未报告。CUA Radar 没有重跑任何实验；本文所有数字都来自论文（版本 v2）。
