# Web-CogReasoner：先记忆、再理解、后探索的网页智能体

*CUA Radar 对 arXiv 2508.01858v3（Guo 等，ICLR 2026）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2508.01858v3 · 代码：https://github.com/Gnonymous/Web-CogReasoner*

## 问题：先有知识，再谈推理

通用 LVM 给了网页智能体很强的先验，但按论文的原话，它们”remain limited in specialized tasks, creating performance bottlenecks”，而且”prior knowledge-enhancement methods often lack systematic or theoretical grounding”。论文的提案来自教育学：引入 Bloom’s taxonomy，把智能体的能力拆成知识内容学习（Factual 与 Conceptual knowledge，即”学什么”）和认知过程（Procedural knowledge，即”怎么做”），并按这个顺序训练——Memorizing、Understanding、Exploring。

## Web-CogReasoner 是什么

**智能体。** 桌面网站上的多模态网页智能体。每步观察截图加 accessibility tree（AX tree），元素以 id 引用；动作空间固定：`click [id]`、`type [id] [content]`、`scroll [id or WINDOW] [up/down]`、`dbclick [id]`、`go_back`、`go_forward`、`stop [content]`、`Restart`、`Wait`。交互被建模为 POMDP P = (S, A, O, K, T, R)，其中 K 是内部知识槽。

**机制。** 论文交付三件东西。(1) *Web-CogKnowledge* 分类法：Factual（元素属性、页面变化与下一页预测）、Conceptual（元素级/页面级/跨模态理解）、Procedural（意图预测、popup close、单步与带噪声多步任务）。(2) *Web-CogDataset*：用 Playwright 对 14 个真实网站做逐层点击遍历（第 1 到第 6 层），由 Qwen2.5-VL 72B 基于 hover/点击前后的截图生成标注，再叠加开源数据（MultiUI、Mind2Web、OpenWebVoyager）扩充；共 81K 条 Factual、62K 条 Conceptual、27K 条 Procedural，覆盖 12 个任务族；popup close 数据由 51 个弹窗组件合成，AX tree 与关闭策略由 Qwen-VL-2.5-32B 生成。(3) *Web-CogBench*：876 条评测样本，“curated from a representative subset of Web-CogDataset”，指标为 ROUGE-L、accuracy，或 GPT-4o LVM judge（1-5 Likert，归一化到 0-100）。

**训练信号。** 对 Qwen2.5-VL-7B 做 supervised fine-tuning（imitation learning），按 S1 Factual → S2 Conceptual → S3 Procedural 的课程顺序，8 张 A800 80GB，最大序列长度 8K，batch size 1 加 16 步梯度累积。推理时执行 Knowledge-driven Chain-of-Thought（KCoT）：task recap → 网页布局描述 → 关键元素分析 → 总结 → 轨迹回顾 → 任务分解 → 逐步推理 → 最终动作。它在 CUA Radar 板上的模式是 C21（用强 MLLM 合成推理标注后 SFT 截图策略），隶属 trajectory-level policy training。

## 论文报告的结果

在线数字全部来自真实网站的在线评测、单次运行；论文未报告种子或方差，UI-TARs-7B-SFT “omitted due to missing online inference scripts”。

| 方法（在线） | WebVoyager (643) | Mind2Web cross-task | Mind2Web cross-web |
|----|----|----|----|
| Claude Sonnet 4 | 47.7% | 40.2% | 21.7% |
| Gemini 2.5 Pro | 54.9% | 37.5% | 25.5% |
| Qwen2.5-VL-7B（基座） | 2.2% | 1.0% | 1.0% |
| OpenWebVoyagerIL | 18.1% | 6.3% | 6.6% |
| OpenWebVoyagerMax | 26.2% | 20.5% | 11.7% |
| **Web-CogReasoner** | **30.2%** | **17.0%** | **10.1%** |

Web-CogReasoner 是表中最好的开源智能体（WebVoyager 30.2%），且每个成功任务的平均步数最低（WebVoyager 4.73，总平均 7.00；OpenWebVoyagerMax 为 6.52，Claude Sonnet 4 为 9.76）。在 Online-Mind2Web 上它超过 OpenWebVoyagerIL，但两个 split 都低于 OpenWebVoyagerMax；论文注明后者”not a strictly comparable zero-shot baseline due to additional sample collection and retraining on high-error sites”。

离线数字（与在线分开列）：在论文自建的 Web-CogBench 上 overall 84.4，对比 Gemini 2.5 Pro 80.2、Claude Sonnet 4 76.8、Qwen2.5-VL-7B 69.8、UI-TARs-7B-SFT 46.4；在 VisualWebBench 上平均 86.3，略高于 UI-TARs 的 86.0 和 Claude Sonnet 4 的 85.9，略低于 Gemini 2.5 Pro 的 86.6。

## 论文自带的对照实验

**KCoT 消融（表 9，WebVoyager 四个网站）。** 数据相同（S1+S2+S3）时，去掉 Knowledge-driven CoT，在线成功率从 42.9% 掉到 25.35%——论文称 KCoT 是连接”拥有知识”与”运用知识”的”a crucial activator”。

**课程消融（表 7-8）。** 逐阶段累加使 Web-CogBench overall 从 69.8（基座）→ 72.1（+Factual）→ 78.3（+Conceptual）→ 84.4（+Procedural）。单阶段训练明显更差（S2 only 61.96、S3 only 60.66，完整为 84.44）；在线上 S1+S3 达 23.47%，而 S3 only 仅 13.14%——“procedural exploration relies on accurate factual grounding”。

**Judge 校验（附录 D）。** GPT-4o 评分协议与另外两个 LVM judge 对比：within-1-point agreement 为 98.7%（Element Understanding）、97.0%（WebPage Understanding）、96.0%（User Intent Prediction），human proxy 相关为 96.7 / 95.4 / 94.4。数据集标注的人工核验平均准确率 97.8%，跨模型一致性 96.9%。

**课程 vs 混合训练。** 只有定性对比：mixed multi-task training 会”terminate the search within a limited number of attempts”，课程训练的模型则持续探索（图 7）。

## 论文自己承认的薄弱处

- 所有数字均为单次运行，未报告种子、重复次数或方差。
- 在线表格里缺少 UI-TARs-7B-SFT——最强开源基线家族之一（“omitted due to missing online inference scripts”）。
- Web-CogBench “curated from a representative subset of Web-CogDataset”：主打离线基准与训练数据共享任务族，而在线基准并未显现同样优势——商业 LVM 仍领先（WebVoyager 54.9% 对 30.2%），cross-web 迁移（10.1%）也低于经过重训练的 OpenWebVoyagerMax（11.7%）。
- 在线消融只覆盖四个网站（Amazon、Cambridge、Coursera、GitHub）。
- 训练监督大量来自 Qwen2.5-VL 72B 与 Qwen-VL-2.5-32B；标注质量做了抽样核验，但没有对标注者自身误差做消融。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **62 分（★★）**，证据等级 **transfer**，模式 C21。判定记录认可：WebVoyager 与 Online-Mind2Web 的真实在线评测、留出网站、组件级消融（KCoT 与知识阶段）、对 LVM judge 的评分者间信度检验、以及代码与数据开源。同时把 variance 与 budget matching 标为 unclear，指出在线基线覆盖不完整，并标记了 anti-pattern AP5。CUA Radar 没有复现任何实验，本文所有数字均抄自论文（版本 v3）。
