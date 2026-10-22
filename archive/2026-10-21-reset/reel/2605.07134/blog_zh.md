# Region4Web：让网页智能体按”功能区域”而不是元素清单读页面

*CUA Radar 对 arXiv 2605.07134v1（Donguk Kwon、Dongha Lee，延世大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2605.07134v1 · 代码（论文中声明）：https://github.com/kwondu/region4web*

## 问题：观测空间照抄了动作空间的粒度

网页智能体每一步通过 observation space 感知页面、再从 action space 里选动作。现有工作基本把两者都放在 element 粒度：把 AXTree / DOM 序列化成带编号的元素清单，再做过滤或截断。论文的观点是：这个粒度适合动作（每个动作指向一个元素、执行一种操作），但不适合观测——观测的任务是理解页面状态，关键是元素之间的关系。页面上真正存在的是 functional region：一组元素因共同目的（站点导航、结果筛选等）组织在一起。而且”目的”没法从布局直接读出：商品卡片阵列是多个独立 region，而结构几乎相同的旅行网站目的地展示却是一个 region。

论文用 Mind2Web（2,350 个任务、137 个网站）上的两个测量来支撑 region 作为观测单元：相邻两个动作的 LCA 深度比中位数为 0.48（随机基线 0.22），81.7% 的动作对高于随机中位数——动作集中在很小的子树里，而一个页面在任务中平均只收到 6 个动作（90 分位 13），对比数千个 DOM 节点。另一方面，页面内 52.9% 的步骤 DOM 零变化、74.4% 的变化率低于 5%——每步重建完整观测大部分是浪费。

## Region4Web 是什么

这是一个跑在 BrowserGym 上的桌面 web 文本智能体：观测是页面的 AXTree，动作通过元素编号（bid）从 BrowserGym 的 15 个动作（click、fill、select_option 等）中选择。它在 CUA Radar 板上的架构模式是 C13：在策略看到文本观测之前先做剪枝与重构。

Region4Web 是把 AXTree 变成 region 级观测的两段框架：

1.  **Hierarchical decomposition。** 一个约 536K 参数的小模型（三层 MLP）自底向上一次遍历，把 AXTree 的每条父子边判为 cut 或 merge；由 merge 边连成的子树就是 functional region。切分打分为 EdgeClassifier(x_v, r_c, r̄)，r̄ 是兄弟均值，切分阈值 τ = 0.55。
2.  **Semantic abstraction。** 微调过的 Qwen3-0.6B 读取每个 region 的子树，输出两个正交字段：purpose（这个 region 是干什么的）和 state summary（当前可交互的上下文）。

训练信号来自专有 LLM 标注器 gpt-5-mini-2025-08-27。源页面取自 Tranco top-1M 中按 10 个 IAB 类别抽出的 500 个网站，最终从 253 个网站抽取 21,974 个页面的 AXTree；经过校验阶段后只保留每个 region 都判对的 2,052 个页面、45,147 个 region。分解模型在二值边标签上用 focal loss（α = 0.75，γ = 2.0）加 teacher forcing 训练；抽象模型在 region 标注上做监督微调。

**PageDigest** 是部署管线。进入新页面时，由 actor 自己的 backbone LLM 读 purpose/state summary 列表加上任务与动作历史，选出与任务相关的 region：被选中的以完整 AXTree 子树暴露（保住动作所需的 element 粒度），未选中的只保留 purpose。页面内不再重跑 Region4Web，而是对照进页时的 AXTree 跟踪 added / removed / modified 节点；另有 view_all 兜底动作可展开全部子树。actor 的策略完全不改，推理时不新增大模型。

## 论文报告的结果

以下全部是 WebArena 在线成功率（%）：812 个长程任务、每任务至多 30 步、五个领域，跑在 BrowserGym，Map 域走实时 OpenStreetMap 服务。原评测器（已废弃的 gpt-4-1106-preview）被换成 GPT-4o。论文未报告随机种子或方差。

| 配置                  | 单独 | \+ PageDigest | 观测 token 单独 → 之后 |
|-----------------------|------|---------------|------------------------|
| GPT-5.1               | 45.2 | 47.5          | 6,116 → 4,302（−30%）  |
| Gemini 3.1 Flash-Lite | 39.4 | 41.6          | 6,705 → 3,207（−52%）  |
| DeepSeek-V3.2         | 40.4 | 43.4          | 7,158 → 4,521（−37%）  |
| Qwen3.5-27B           | 38.2 | 39.9          | 5,767 → 2,654（−54%）  |
| SteP（GPT-4o）        | 39.5 | 38.7          | 7,136 → 3,693（−50%）  |
| AgentOccam（GPT-4o）  | 40.6 | 41.3          | 4,025 → 3,365（−16%）  |

四个 backbone 平均：观测长度下降 43%（每步 6,437 → 3,671 token），成功率平均提高 2.3%p。两个既有 agent 方法上观测分别下降 50% 与 16%，成功率相当。论文没有离线单步准确率数字，以上全部是在线结果。

## 论文自带的对照实验

**消融**（WebArena-Lite，165 任务子集，GPT-5.1）：backbone 单独 48.5（5,410 token）；加 Region4Web 单独 50.3（5,922）；去掉 Region4Web、把 region 选择换成 LCoW 式 self-contextualization 的 element 级变体为 46.1（4,013，省 26% 但掉分）；完整 PageDigest 53.9（3,814，省 30%，比 backbone 高 5.4%p）。论文据此认为支撑 actor 的是 region 级观测，而不是单纯的压缩。

**任务级核算。** 步级观测中位数下降 33%（3,077 → 2,066 token），任务总 token 中位数下降 25%（26,707 → 19,944）。任务总量分解为：actor 观测 73.9%、region 选择 19.5%、view_all 6.6%；选择平均每任务触发 4.8 次，view_all 出现在 38.1% 的任务中、平均 0.64 次。

**失败审计。** 抽样 50 条失败轨迹（每域 10 条）：backbone 动作选择占 90.0%，环境错误 16.0%，region 选择 10.0%，语义抽象 2.0%，分解 2.0%，transition 管理为零；多因归因下 82.0% 归于 backbone 能力、8.0% 归于 PageDigest 回退。

**留出关系。** 训练页面来自 Tranco 榜单的真实网站；WebArena 评测站点是自建副本，标注页面与评测页面不重叠。

## 论文自己承认的薄弱处

- 只在 WebArena 上评测：“Our evaluation focuses on WebArena, whose consistent AXTree fidelity supports the controlled comparisons our experiments require. Broader validation on real-world web environments … complements these results.”
- 依赖 AXTree 质量：分解效果取决于 “how completely each page exposes its accessibility semantics”，canvas 渲染或非语义标记的页面结构线索更弱。
- 所有表格都没有种子、标准差或显著性检验。
- 评测器换成 GPT-4o 一事未与原评测器做对照验证。
- 论文声明代码在 github.com/kwondu/region4web；radar 记录中 code 状态为 unclear。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **transfer**，模式为 C13（对文本观测先剪枝再重构）。分数反映论文报告的证据：WebArena 在线评测、训练页面留出、两个既有 agent 基线、对齐的 30 步预算、token 成本报告和组件消融。未报告：运行方差、替换后评测器的验证、可核验的代码。记录同时标记 AP18（有损或状态不一致的上下文管理）——紧凑 digest 可能藏掉任务所需内容的长期风险；论文在基准内的回应是 view_all 兜底，它在 38.1% 的任务中被触发。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
