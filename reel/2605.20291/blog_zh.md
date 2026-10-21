# Weasel：选对 1 万步轨迹数据再做 SFT，零样本泛化胜过全量 5.2 万步训练

*CUA Radar 对 arXiv 2605.20291v2（Pesaran Zadeh、Choi、Lù、Reddy、Kim，ICML 2026）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2605.20291v2 · 代码：https://github.com/fatemehpesaran310/weasel*

## 问题：离线训练数据的两重代价

在固定轨迹和环境上微调的网页智能体，一旦换到没见过的网站、布局或交互模式，性能往往大幅下降；论文还指出，近期工作大多在 in-benchmark 设定里训练加评测，掩盖了这一退化。离线交互数据本身也带来两重代价：专家轨迹噪声大、冗余多——AgentTrek 一条轨迹最多含 45 个状态-动作对，真正与目标相关的只是其中一小部分；每个状态又是线性化的 accessibility tree（AXTree），单条可达 180K token，全量训练既慢又容易过拟合到特定网站的痕迹。对 reasoning-native 模型还有一层风险：用别的模型写法写的轨迹做微调“可能有害”，甚至“有时在微调前就掉到基座模型以下”。

## Weasel 是什么

Weasel（WEb Agents with trajectory SELection）不是新的智能体架构，而是一套面向离线训练的数据选择与整理方法。底层智能体是 BrowserGym 生态里的文本网页智能体：观察目标、交互历史和线性化 AXTree，动作用引用 AXTree 元素 bid 的 node-grounded 动作（click、type、scroll）加上不需要目标的动作（goto、noop）。论文研究了三个基座：Qwen2.5-7B-Instruct、Gemma3-4B-IT 和 reasoning-native 的 Qwen3-8B，均用 rank 8 的 LoRA 微调。在 CUA Radar 板上，论文归属 trajectory-level policy training 主模式下的子模式 K25：为动作轨迹补生成推理（reasoning）。

整理流程在训练前一次性完成：

1.  **Target-centered pruning。** 对每个 node-grounded 动作，只保留以 gold 目标 bid 为中心的 2w+1 个 AXTree 节点窗口（w = 60；非节点动作用固定长度前缀）。这保留约 32% 的 token，单独就能带来 2 倍训练加速。
2.  **打分。** 一元重要性 Phi(t) = BERTScore(goal, state)，编码器用 roberta-large；成对多样性 D(i, j) 取状态伪距离与答案伪距离的最大值，每个伪距离为 1 − BERTScore；权重 lambda 取 1。
3.  **贪心选择。** 先选目标值最高的二元组作种子，再每轮加入边际增益最大的步骤，直到每条轨迹的预算 T0 = 3 步。52K 条 AgentTrek 步骤由此保留 12K（NNetNav-Live 保留 16K），再均匀采样到 10K 用于训练。
4.  **Self-reasoning synthesis。** 仅针对 reasoning-native 的 Qwen3-8B：由基座模型自己根据目标、历史、剪枝后状态和专家动作重新生成 think 与 memory 块，专家动作原样保留——这是论文对上述 style mismatch 的解法。

因此训练信号就是对精选子集上专家动作的纯模仿；选择信号是 embedding 相似度，训练全程没有环境交互，也没有 RL。

## 论文报告的结果

以下均为 AgentLab 框架收集的在线成功率（SR），WebArena-Lite 用 GPT-4.1-mini 判定、WebArena 用 GPT-4-1106-preview 判定。设定为零样本迁移：在 AgentTrek 上训练，在 WebArena-Lite、WebArena、MiniWob、WorkArena（L1/L2）上评测，不做任何额外微调。论文报告的是整个评测集上的聚合 SR，没有给出种子数或方差。Epoch 数：Qwen2.5-7B 为 4，Gemma3-4B 与 Qwen3-8B 为 2。

Qwen3-8B，AgentTrek 训练：

| 变体 | WebArena-Lite | WebArena | MiniWob | WorkArena L1 | WorkArena L2 | 训练 |
|----|----|----|----|----|----|----|
| Qwen3-8B（基座） | 16.4 | 18.0 | 61.1 | 35.2 | 1.7 | – |
| Full 52K steps | 17.7 | 18.2 | 59.4 | 33.3 | 2.1 | 88.5 hr，1.0x |
| Pruning 52K | 17.6 | 12.7 | 40.3 | 15.5 | 2.6 | 44.0 hr，2.0x |
| Sampling 10K | 16.5 | 17.5 | 61.4 | 33.9 | 3.4 | 7.0 hr，12.6x |
| LLM-Judge 10K | 19.4 | 16.6 | 61.9 | 35.2 | 3.8 | 7.0 hr，12.6x |
| **Weasel 10K** | **21.2** | **19.2** | **61.9** | **38.8** | **4.3** | 8.3 hr，10.7x |

摘要强调 Qwen3-8B 在 AgentTrek 到 WebArena-Lite 的零样本迁移上提升 +4.8。其他两个模型次序相同：Qwen2.5-7B-Instruct 用 Weasel 在 12.0 hr（11.3x）内达到 14.5 / 9.5 / 48.0 / 12.4 / 4.7，而全量 52K 步 SFT 用 136.0 hr 达到 10.9 / 8.7 / 44.6 / 12.1 / 0.4；Gemma3-4B-IT 用 6.4 hr（12.5x）达到 11.5 / 5.5 / 30.6 / 4.5 / 3.0，全量为 80.0 hr 的 9.1 / 4.3 / 28.6 / 3.3 / 0.0。把训练集换成 NNetNav-Live（表 2，Qwen2.5-7B）结论不变：Weasel 12.1 / 8.3 / 41.8 / 7.6 / 6.8（9.7x），高于全量 SFT（10.9 / 6.9 / 38.9 / 5.2 / 6.4）和均匀采样（10.3 / 7.4 / 32.3 / 7.0 / 6.0）。总体上论文报告 9.7-12.5 倍的训练加速。

另有一个离线结果，与上面的在线数字分开列：把打分模块换成 SigLIP2 截图 embedding 和 CLIP 目标-图像对齐后，仅选择组件即可迁移到多模态的 Android in the Wild（Qwen2.5-VL-3B-Instruct，留出 500 例测试子集，10K 池中取 3.1K）：基座 4.4、随机选择 5.8、Weasel 6.6 的步骤准确率。论文称这些结果为初步（preliminary）。

## 论文自带的对照实验

- **同样 10K 步预算**（Qwen2.5-7B，WebArena-Lite）：均匀采样 9.1，LLM-as-judge 选择 8.5，按长度过滤 5.5 和 10.9，Weasel 14.5。
- **同 32% token 预算下的剪枝对照**（表 3）：Prune-by-Bid 8.5，Semantic 9.1，Target-centered + Semantic 7.3，Target-centered 10.9，未剪枝 10K 数据为 10.3；所有剪枝变体都是同样的 2.0x 加速。图 5 中把窗口从目标处移开，SR 大致线性下降。
- **目标函数消融**：仅一元重要性 10.9，仅多样性 7.9，两者结合 14.5；仅状态多样性 9.7，仅答案多样性 13.9；goal-state 配对优于 goal-summary（12.7）与 goal-reason（9.1）。
- **选择乘以推理合成**（Qwen3-8B，10K，2 epochs）：随机 SFT 16.5，随机 + 合成 18.2，无合成的 Weasel 17.0，两者兼有 21.2——两个组件互补。
- **贪心质量**：在 1,877 条 NNetNav 轨迹上（T0 = 3，每条最多 7,770 个候选子集），贪心解在超过 96% 的轨迹上与精确最优一致，99.7% 落在全体候选的前 1%，目标值之比为 0.9999 ± 0.0005。
- **稳健性**：把 BERTScore 换成 Qwen3-Embedding-0.6B 得 12.7，Qwen3-Embedding-4B 得 14.5；lambda 0.5 / 2.0 / 4.0 分别为 10.9 / 12.1 / 10.3；窗口 40 / 80 为 12.7 / 12.8；T0 = 0.25T 为 12.1——都低于但接近默认的 14.5。
- **成本**：全量 AgentTrek 的一次性预处理共 7.7 小时（重要性 0.35 h、多样性 0.50 h、贪心不足 0.02 h、推理合成 7.5 h），而一次全量 SFT 需 136 小时。

## 论文自己承认的薄弱处

- 没有方差：“We report aggregate SR over the full evaluation set for each benchmark.”
- 成败由 LLM 判定（GPT-4.1-mini、GPT-4-1106-preview）；判定记录指出论文未对这一 judge 相对真值做验证。
- 剪枝并非处处安全：Qwen3-8B 上仅 Pruning 52K 把 MiniWob 拉到 40.3（全量为 59.4）；NNetNav-Live 上仅剪枝的一行降到 5.5 / 3.2 / 38.4 / 1.8 / 1.3。
- 多模态迁移被论文标注为初步结果，绝对准确率也小（4.4 到 6.6）。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **63 分（★★）**，证据等级 **transfer**，子模式 K25。分数反映论文所报告的证据：在线评测、真正的留出环境（在 AgentTrek 或 NNetNav 上训练、零样本在别处评测）、同 10K 步预算下的 SFT 基线、成本报告、组件消融和已公开的代码。判定记录同时标出缺少种子/方差、未经验证的 LLM judge，以及 self-reasoning synthesis 所针对的推理风格失配不稳定性。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
