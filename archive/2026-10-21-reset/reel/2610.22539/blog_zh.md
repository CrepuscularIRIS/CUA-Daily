# WebMix：侦察器写网站手册，router 混合 LoRA bank

*CUA Radar 对 arXiv 2610.22539v1（Md Farhan Ishmam、Minh Pham-Dinh、Kenneth Marino；University of Utah）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.22539v1 · 项目页：https://webmix-hyper.github.io/ · 评审时未列出公开代码仓库。*

## 问题：每来一个新界面就要重训一个 adapter

小型开源权重模型只有在演示数据上微调之后才能胜任网页任务，通常是在冻结基座上加一个 LoRA adapter——而“every new site or redesign calls for a new corpus and a new adapter”（每个新网站或改版都需要新的语料和新的 adapter）。论文的动机是：Mind2Web 从 cross-task 划分到 cross-website、cross-domain 划分性能持续下降；TimeWarp（把同一批网站按六个网页设计年代渲染）显示在一个年代上训练的 agent 到下一个年代就退化。演示数据昂贵——每条都要人在真实网站上操作——而且语料还没攒够网站可能就改版了。近期的自适应方法减少了监督量，但按论文的说法“treat each new interface as a separate adaptation problem … none of them learns how to adapt”（把每个新界面当成独立的适配问题，没有一种方法学会“如何适配”这件事）。直接用 hypernetwork 生成 adapter 权重在这里很难：一个界面家族只提供极少 的 conditioning 去回归数百万权重，而且 LoRA 因子不可辨识（not identifiable）。WebMix 的答案是：不生成权重，而是组合权重。

## WebMix 是什么

这是一个基于 BrowserUse harness 的文本网页 agent。它读入自然语言目标、当前页面的 accessibility tree 和历史，每步输出一个浏览器动作（click、输入字符串、scroll）。任务成功当且仅当 verifier 接受网站的最终状态。平台是自托管网站：TimeWarp（三个 domain——Wiki、News、Shop——各六个版本）和 WebArena-Lite-v2（五个 domain：Reddit、GitLab、CMS、Map、OSS）。基座模型为 Qwen-3.5 4B 和 Llama-3.1 8B。在 CUA Radar 板上，它属于模式 C19“从 agent 自身运行中积累可复用知识”（挂在 experience-memory retrieval 主模式下）——只是这里积累的知识是一组按界面训练的 LoRA adapter，而“检索”是一次权重混合。

WebMix 是一个 mixture hypernetwork，四个部件：

1.  **Adapter bank。** 每个源界面一个 LoRA（rank r = 16，scale α = 32，作用于 attention q/k/v/o 和 MLP gate/up/down 投影），用自己界面上的 supervised fine-tuning 训练，并加一个 KL anchor 项（β = 1.0，clip 过的 k3 估计，界为 \[−20, 8\]），惩罚它在**其他**源界面的演示上偏离基座策略。bank 训练一次后冻结。
2.  **Scout（全部冻结、从不训练）。** 分 explorer 和 writer。version transfer 时 explorer 做无任务的广度优先爬取：每站最多 25 页、链接深度 3，外加一次 search probe。domain transfer 时冻结基座策略尝试 n = 1 个来自该站训练集的任务，explorer 回放策略走过的页面。冻结的 writer LLM（Qwen-3.5 9B，temperature 0）把记录压缩成固定七节结构的 manual（domain transfer 再加一节确定性的 worked path）。冻结的句编码器（BGE-large-en-v1.5，d_c = 1024）对 manual 做嵌入。
3.  **Router。** 两层感知机（hidden width 256，SiLU，输出层零初始化，训练从均匀混合出发；约 0.26M 参数），把 manual 嵌入映射成 K 个 softmax 混合系数，每个 bank adapter 一个。组合在 update 空间进行：把 bank 因子沿 rank 维拼接，得到一个 rank 至多 Kr、scale 为 α_out = Kα 的标准 LoRA。未修改的推理栈即可 serving，且任何混合都不会产生比 bank 中最大 adapter 更大的 update。
4.  **训练与适配。** Stage 2 只训 router（500 步 AdamW），在汇总的源语料上做 behavior cloning，梯度穿过组合出的 update 和冻结的基座。适配 = 一次 scout 访问加一次前向：目标界面零演示、零梯度更新。以后新增界面只需加一个 adapter 并重训 router。

训练信号因此只有源界面的专家演示（behavior cloning）、其他源界面上的 KL anchor，以及部署时唯一取自未见界面的信息——scout 写出的 manual。

## 论文报告的结果

以下全部是在线成功率（%）：verifier 接受网站最终状态才算成功。每个数字是 3 次运行的平均，BrowserUse harness，non-rationale tokens、memory 开启。“Unseen”指被评测的 domain 或版本同时不在训练数据和 in-context 示例里。论文没有报告任何离线的 step / grounding 指标。TW = TimeWarp，WAL = WebArena-Lite-v2。

| 模型 | 方法 | TW domains (unseen) | TW versions (unseen) | WAL overall (unseen) |
|----|----|----|----|----|
| Qwen-3.5 4B | Zero-shot | 22.92 | 18.28 | 21.86 |
| Qwen-3.5 4B | In-context learning | 25.42 | 20.06 | 24.89 |
| Qwen-3.5 4B | LoRA | 25.42 | 24.27 | 29.22 |
| Qwen-3.5 4B | **WebMix** | **33.75** | **27.51** | **34.42** |
| Qwen-3.5 4B | LoRA (in)，seen 专家 | 33.75 | 25.40 | 37.23 |
| Llama-3.1 8B | Zero-shot | 7.50 | 6.63 | 6.28 |
| Llama-3.1 8B | In-context learning | 7.08 | 6.15 | 4.98 |
| Llama-3.1 8B | LoRA | 8.33 | 16.99 | 12.12 |
| Llama-3.1 8B | **WebMix** | **15.83** | **18.77** | **16.67** |
| Llama-3.1 8B | LoRA (in)，seen 专家 | 15.83 | 17.64 | 22.29 |

论文自己给出的要点：Qwen-3.5 4B 在未见 News domain 上成功率 56.1%（表中为 56.06，对比迁移 LoRA 的 45.45），“exceeding transferred LoRA by 10.6 percentage points”；TimeWarp 未见 domain 平均增益 Qwen 8.3 个点、Llama-3.1 8B 7.5 个点，几乎让 Llama 的成功率翻倍，且两个模型都追平了目标界面专家的平均表现（33.75 与 15.83，与上表 LoRA (in) 行完全一致）。version transfer 增益较小，为 1.8–3.2pp；WebArena-Lite-v2 的增益论文写为 3.3–4.6pp。迁移在与训练 domain 相近的 domain 上最强：Qwen 的 News 比 zero-shot 高 26pp，而 Wiki 和 Shop 约 5pp；WAL 上 OSS 增益最大（两个模型 14–15pp）。论文把 Llama-3.1 上的 Map 列为未见迁移的唯一失败案例；表 2 中该列所有未见基线都是 0.00，WebMix 为 7.69。seen 设定下 WebMix 在每一列都是最好或并列最好；把目标 domain 计入训练后，Qwen 在 WAL overall 达 42.4%，论文报告比在所有 domain 上训练的 LoRA 高 4.3 个点。

## 论文自带的对照实验

- **对齐比较。** 所有方法都在同样两个基座上运行，对比 zero-shot、in-context learning、LoRA；seen 设定再加分目标界面专家 LoRA (in) 和全界面训练的 LoRA (all)。每个数字是 3 次运行的平均。
- **真 held-out。** 未见 domain 或版本同时从训练数据和 in-context 示例中剔除。
- **设计消融**（表 3，Qwen，未见 TW domains，pooled 平均）：用 Text-to-LoRA 回归存储 adapter（T2L-Recons）为 16.25；同一生成器经策略端到端训练（T2L-SFT）加 9.17pp；把权重生成换成 mixture hypernetwork 再加 3.75pp；router 再以 scout 的 manual 为条件再加 4.58pp——相对最强 T2L 变体共 8.33pp（33.75）。
- **Scout 预算。** n = 1 个 scouted task 最好；n = 3 在 News 上 +1.5pp，但在 Wiki 上损失 6–8 个点，因此全文用 n = 1。
- **KL anchor。** β = 1.0 在所有 domain 和平均上都是测试值中最好；去掉该项（β = 0）平均下降超过 7pp；更强的惩罚（β = 3.0）同样有害。
- **保持性（retention）。** 迁移增益不以 seen 界面为代价：相对 LoRA (all)，TW domains +4.6–6.3pp，TW versions +1.8–2.4pp，WAL +2.6–4.3pp。而在所有 domain 上训练 LoRA 只比 in-domain LoRA 高 0.2–1.3pp，说明 WebMix 的增益不只是更多训练数据。
- **分析。** bank 的 domain adapter 接近正交——update 的所有两两 cosine 相似度低于 0.16；没有 KL anchor 时约高出两倍。router 系数反映界面相似度：held-out 的 v1 主要由 v2（81%）和 v3（17%）组成；v6 进 bank 时 96% 权重落在 v6 上。
- **理论。** 附录 D 把 held-out imitation risk 分解为近似项（由目标 oracle 到 bank 凸包的距离界定）与 routing 项，并证明理想化的直接生成器等价于系数未归一化的 routing。全部证明用 Lean 4 形式化。

## 论文自己承认的薄弱处

- version transfer 是较弱的一条轴：增益 1.8–3.2pp，且“LoRA is a strong baseline there”。
- 理论的可检验预测没有落地：“The experiments of §4 do not include the transfer matrix, the uniform mixture, or the hull-distance panel, so these three predictions remain untested”；bank 增长方面，“The experiments of §4 include neither sequential arrival nor this curve。”
- 没有报告标准差或置信区间；每个数字是 3 次运行的平均。
- 代码：“The complete source code is included in the supplementary material and will be released publicly upon acceptance”——评审时没有公开仓库。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **transfer**，子模式 C19（“从 agent 自身运行中积累可复用知识”），挂在 experience-memory retrieval 主模式下。判定记录认可：在线 verifier 判定评测、真正的 held-out domain 与版本、同基座的强基线、组件消融；同时标出：方差未报告（只有 3 次运行平均）、budget 匹配不清楚、计算成本不清楚、代码可得性不清楚（待接收后公开）。CUA Radar 没有复现任何实验；本文所有数字均来自论文（版本 v1）。
