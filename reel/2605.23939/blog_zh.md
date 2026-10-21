# DRIVE：把网页智能体的经验拆成”推理规则 + 页面程序”两个技能库

*CUA Radar 对 arXiv 2605.23939v1（Liu 等，国防科技大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2605.23939v1 · 论文未给出代码仓库。*

## 问题

网页智能体同时需要两类知识。Reasoning knowledge（订机票要先搜航线）是抽象的、可跨网站迁移的；interaction knowledge（在某个站点上点哪个坐标的搜索按钮）则和具体页面绑定。论文的诊断是：现有方法把历史经验用同一种形式统一存储——自然语言反思保留了意图却在具体页面上不可执行，保留的轨迹和可调用程序能执行却在页面改版后失去迁移性。由此带来第二个缺口：任务失败时，系统里没有任何信号说明错在推理还是错在交互，经验库也就无法在正确的层级上被修复。

## DRIVE 是什么

这是一个基于 DOM 的桌面网页智能体，在 WebArena 上评测（812 个任务、五个自建站点域：Shopping、CMS、Forum、Gitlab、Map）。每一步它读取页面 observation 和当前 URL，在一个预定义的 primitive action space 里动作。主实验的 backbone 全部是 GPT-4.1（解码温度 0.1），每个 episode 上限 20 个 environment step。在 CUA Radar 板上它属于模式 C19——从智能体自身运行中积累可复用知识——挂在父模式 “retrieve past experience and knowledge into context” 下。没有任何微调：所有学习都发生在一个被注入 context 的技能库里。

机制分四块：

1.  **双层技能库 K = (K<sup>r</sup>, K<sup>i</sup>)。** Reasoning skill 是自然语言三元组 ⟨M, B, V⟩：观察到的错误模式 M、修正后的行为准则 B、验证指令 V，注入 context 用于决定”做什么”。Interaction skill 是参数化程序 k<sup>i</sup>(C, X) → (α, e)：给定页面上下文 C 和任务参数 X，执行一个闭环过程（迭代校验 locator、处理动态 UI），返回动作序列 α 和结果 e，负责”怎么做”。
2.  **Scenario descriptor 与单例激活。** 每个技能带描述符 ⟨U, W⟩：适用页面上下文（URL 模式等）与任务语义。在线检索先做结构过滤（U 是否匹配当前 URL / 页面状态），再按 W 做语义排序；每一步最多激活一条 reasoning skill 和一条 interaction skill，否则退回 primitive action。
3.  **成功轨迹归纳 + 失败轨迹的反事实归因。** 成功 episode 被抽象成 interaction skill，任务实体被提升为参数。每个失败 episode 要回答一个反事实问题：如果智能体保持高层意图、只换一套交互流程，任务能否完成？能 → interaction-level error，合成带恢复逻辑的修正版 interaction skill；不能 → reasoning-level error，写一条 ⟨M, B, V⟩ reasoning skill。
4.  **持续维护。** Interaction skill 以操作模板 + 有序 selector 列表（CSS、XPath、DOM identifier、text locator、accessibility 属性）存储：失败 selector 降级或删除、可用者加入，反复失败的技能整个删除。Reasoning skill 按使用次数与任务结果算出的平滑 utility 分数做合并与剪枝。

训练信号因此是二值任务结果加 skill 级执行反馈（selector 是否命中、URL/页面状态是否变化、异常）——没有学习型 reward model，也不更新权重。论文报告：训练轨迹从 42 条增加到 251 条时，多数域上的任务成功率与 interaction skill 调用成功率持续上升。

## 论文报告的结果

以下全部是 WebArena 自动 functional-correctness 评测下的在线成功率（%）。DRIVE 与所有复现 baseline 均用 GPT-4.1、同一环境配置、同一测试任务、同样的 20 步预算。划分是 within-website：每个站点 30% 任务用于训练、70% 用于测试。

| Agent          | Shopping | CMS  | Forum | Gitlab | Map  | 平均 |
|----------------|----------|------|-------|--------|------|------|
| WebArena agent | 21.4     | 15.4 | 8.1   | 14.1   | 12.7 | 14.3 |
| SteP           | 37.0     | 24.0 | 59.0  | 32.0   | 30.0 | 36.4 |
| Go-Browse      | 41.2     | 38.4 | 51.6  | 41.2   | 38.4 | 42.2 |
| SkillWeaver    | 25.1     | 23.8 | 41.3  | 32.0   | 26.2 | 29.7 |
| AgentOccam     | 37.2     | 41.5 | 60.4  | 41.4   | 46.8 | 45.5 |
| DRIVE          | 45.9     | 46.1 | 66.7  | 50.0   | 55.4 | 52.8 |

DRIVE 平均 52.8%，对比 AgentOccam 的 45.5%：+7.3 个百分点，相对提升 16.0%；相对 Go-Browse、SkillWeaver 分别高 10.6 和 23.1 个点。换用开源 backbone Qwen2.5-7B-Instruct，平均从 8.2 升到 12.5（相对提升 52%；各域 8.4 → 12.3、6.1 → 8.9、9.9 → 16.9、8.7 → 12.7、7.8 → 11.7）。论文没有离线的单步/grounding 准确率，以上全是在线结果。主表没有方差，mean ± std 只出现在下文的 100 任务错误分析里。效率方面（Shopping 测试集，N = 137）：成功率 37.23 → 45.99（+8.76 pp），每任务 input token 61,316 → 69,858（+13.9%），但每次成功的 token 成本 164.7k → 151.9k（−7.8%），每任务步数 9.3 → 9.1，模型调用次数 10.8 → 13.3；在匹配任务子集上，总 input token 下降 10.9%、总交互步数下降 12.9%。

## 论文自带的对照实验

- **组件消融**（WebArena 平均）：无技能 baseline 45.5；加”从成功轨迹蒸馏的 interaction skill”到 49.8（+4.3 pp）；加”从失败轨迹修正的 interaction skill”到 48.5（+3.0）；加”从失败轨迹得到的 reasoning skill”到 47.8（+2.3）；完整 DRIVE 52.8（+7.3）。
- **归因模块经过验证而非假设。** 在 150 任务子集（每域 30 个）上，baseline 产生 81 条失败轨迹，由两位标注者独立标注。LM 归因与人工标注一致率为 69.1%：47 个 reasoning error 认出 36 个（recall 76.6%），34 个 interaction error 认出 20 个（recall 58.8%）；14 个 interaction error 被误判为 reasoning（多为级联 UI 故障），11 个 reasoning error 被误判为 interaction（多为提前终止任务）。
- **路由方向本身有因果证据。** 同一子集上：no-skill 46.0，human attribution 54.0（+8.0），LM attribution 49.3（+3.3），random attribution 46.7（+0.7），reversed attribution 44.7（−1.3）。故意把失败塞进错误的库会掉到无技能 baseline 之下——这是论文自己给出的”两层必须分开”的证据。
- **两种技能各自削减各自的错误。** 100 个抽样任务、三次运行、mean ± std：no-skill 正确 42.3 ± 3.06 / reasoning error 35.7 ± 2.52 / interaction error 22.0 ± 3.57；仅 reasoning skill 48.0 ± 1.81 / 30.3 ± 2.36 / 21.7 ± 2.08；仅 interaction skill 47.7 ± 2.52 / 33.3 ± 0.58 / 19.0 ± 2.17；双层 52.3 ± 2.52 / 30.0 ± 2.03 / 17.7 ± 1.53。

## 论文自己承认的薄弱处

- 划分是 within-website 而非留出站点：“We then use a within-website stratified split, assigning 30% of tasks to training and 70% to testing.” 技能在这五个网站上归纳、也在同一批站点上评测，跨站点迁移未被测量。
- “Our experiments use a DOM-based benchmark and do not fully capture the visual complexity of real websites.”
- “Retrieval may become less precise as the library grows, which calls for more scalable selection mechanisms.”
- 主对比表没有报告方差，也未给出代码仓库。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **online**。判定记录肯定了论文报告的内容：在线 functional-correctness 评测、同 backbone 同预算的 baseline、token 成本报告、组件消融，以及与人工标注对照验证过的归因模块。同时标记：技能数据与评测网站重叠（anti-pattern AP5，未缓解）、主表无方差、无代码。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
