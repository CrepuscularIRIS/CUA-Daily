# ToolCUA：教计算机操作智能体在鼠标动作与 tool call 之间选对路

*CUA Radar 对 arXiv 2605.12481v2（Hu、Zhang、Xu、Qiao、Yang 等；通义实验室、复旦大学、上海人工智能实验室）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2605.12481v2 · 代码：https://github.com/X-PLUG/ToolCUA*

## 问题：路口上的智能体

计算机操作智能体（CUA）既能用原子 GUI 动作（点击、键入、滚动），也能用高层 tool call（基于 API 的操作）。论文开篇给出一组诊断数字：只是把两种动作空间都暴露给模型，往往不升反降。在 OSWorld 与 OSWorld-MCP 匹配的可行任务集上（Table 1），加入工具后 Qwen3VL-235B 从 41.1% 降到 38.1%，EvoCUA-32B 从 52.6% 降到 40.5%，Claude-4-Sonnet 从 47.7% 降到 43.5%，Claude-4.5-Sonnet 从 61.9% 降到 48.4%；Qwen3VL-8B 基本不动（29.0% 到 28.2%），因为它即便在成功的 tool-beneficial 任务上也只发起 0.01 次 tool call。论文把这称为 optimal path confusion：继续 GUI 还是切换工具，是一个 trajectory 级决策，step 级模仿和最终任务奖励都教不会。

## ToolCUA 是什么

这是一个端到端策略，基座为 Qwen3-VL-8B-Instruct。每一步它看到当前桌面 screenshot 和此前 tool call 的文本结果（消息构造保留最近 5 张 screenshot 作为图像历史，更早的步骤压缩为纯文本动作历史）；动作空间是混合的：通过 `computer_use` 函数发出的坐标级 GUI 动作（key、type、click、scroll、wait、terminate），以及以 JSON `tool_call` 块发出的 MCP 工具调用。平台是 Linux 桌面沙箱（OSWorld QEMU 镜像，加入 OSWorld-MCP 与 AutoGLM 的 MCP 工具设计）；对未见 Windows 应用的迁移在 WindowsAgentArena 上测试。在 CUA Radar 板上它属于模式 C11（在同一动作空间里混合 GUI 动作与代码/工具调用），父模式为 planner_grounder_interface。

训练分三段，监督信号主要靠合成：

1.  **Interleaved GUI-Tool trajectory scaling。** 从 10,000 条成功的纯 GUI 轨迹出发（192,000 个原始步；OpenCUA 8,500 条、ScaleCUA 300 条、沙箱采集 1,200 条），先用 MLLM 为每条轨迹合成一个 trajectory 感知的模拟工具库——4,350 个去重工具，分细、中、粗三档粒度（2,000 / 1,900 / 450），平均每条轨迹候选工具池 19.75 个。再用 MLLM 生成功能等价的纯工具轨迹，并用 next-state grounding 把每个模拟 tool call 锚定到原示范轨迹的真实下一帧 screenshot；82.5% 的合成工具步通过该过滤，人工审计发现被接受的步 93.0% 状态对齐，被拒绝的步只有 28.0% 对齐。随机把一部分 tool call 换回对应 GUI 片段，得到 10,000 条 interleaved 轨迹（180k 步）和 5k 个关键 GUI-Tool 切换步。这一阶段不需要真实工具执行。
2.  **Tool-Bootstrapped GUI RFT。** 先在 interleaved 数据上做 3 个 epoch 的 warmup SFT（全参数，8 × 8 GPU），再在 5k 个关键切换步上做单轮 GRPO（group size 32，学习率 1 × 10−6，batch size 128），直接强化边界上的 GUI-或-工具决策。
3.  **Online Agentic RL。** 在真实 GUI-MCP 沙箱中做多轮 GRPO（rollout size 32，batch size 32，约 250 个 Docker 实例，8 × 8 训练 GPU 加 4 × 8 推理 GPU），奖励为 Tool-Efficient Path Reward：R = R_fmt + R_acc + λ·R_tool + β·R_length，λ = 0.4，β = 0.2。R_tool 奖励在标记为 tool-beneficial 的任务上调用工具、在其余任务上克制（标签来自带/不带工具的 pass@32 rollout 并经人工核验，抽样 60 个 tool-beneficial 任务一致率 91.7%，40 个 non-tool-beneficial 任务一致率 80.0%）；R_length 对短于组内平均的轨迹给奖励。两项都只在成功轨迹上生效。

## 论文报告的结果

以下全部是在线评测结果：OSWorld-MCP 可行任务（333 个：238 个 tool-beneficial、95 个 non-tool-beneficial），average@3，步数上限 50。论文没有离线的 step/grounding 准确率。

| 模型                         | Accuracy (%) | TIR (%) | ACS (步)  |
|------------------------------|--------------|---------|-----------|
| UI-Tars-1.5-7B               | 12.31        | 4.5     | 37.11     |
| Qwen3-VL-8B-Instruct（基座） | 28.23        | 8.41    | 19.34     |
| EvoCUA-32B                   | 40.54        | 22.52   | 26.16     |
| GUI-Owl-1.5-8B               | 43.84        | 36.04   | 21.19     |
| Claude-4-Sonnet              | 43.54        | 35.74   | 19.76     |
| Gemini-3.1-Pro               | 41.14        | 34.23   | 25.40     |
| GUI-Owl-1.5-32B              | 48.05        | 41.14   | 24.19     |
| Claude-4.5-Sonnet            | 48.35        | 40.24   | 19.07     |
| **ToolCUA-8B**               | **46.85**    | 24.32   | **14.93** |

ToolCUA-8B 高于此前同规模最强的 GUI-Owl-1.5-8B（43.84%），落后 Claude-4.5-Sonnet 1.50 个点，且 ACS（14.93，基座为 19.34）是所有被评模型中最低的。相对基座，论文在 Table 2 印出 Δ +18.62，并表述为 “a relative improvement of approximately 66%”。在 tool-beneficial / non-tool-beneficial 两个子集上分别为 45.80 / 49.47。它是 Table 1 里唯一因工具受益的模型：纯 GUI 42.9%，加工具 46.8%（+3.9 个点）；tool call 集中在有用处——成功 tool-beneficial 轨迹平均 2.11 次，失败的 0.12 次，全部 333 个任务合并每任务 0.74 次。

迁移：在从 RL 训练中排除的 multi_apps 领域上，ToolCUA 达到 23.9%（基座 9.8%，online RL 前检查点 18.5%）；在未见 Windows 应用上，全量 GUI-only WindowsAgentArena 达 33.8%，匹配的 107 任务子集上 GUI-only 37.7%、加移植 MCP 工具后 40.5%（1.74 次 tool call），而基座从 28.0% 降到 26.8%。

## 论文自带的对照实验

- **纯 GUI 对照（Table 3）。** 用规模相当的 GUI-only 数据冷启动同一基座，再做纯 GUI agentic RL：29.03% → 34.93%（SFT）→ 42.05%（RL）；混合路径 RFT 后 38.13%，online RL 后 46.85%。两个阶段混合训练都占优，最终差距不能只用 GUI 技能解释。
- **消融：数据（Figure 6）。** 去掉 interleaved 数据、直接从基座做 online RL，accuracy 仍会上升，但 TIR “only reaches around 15% by the end of training”，tool call 全程接近零——奖励本身克服不了 GUI 偏置。
- **消融：奖励（Figure 6）。** 把 path reward 换成 vanilla GRPO（只剩 accuracy + format），训练稳定性变差，“an eventual gap of about 7 percentage points after 20 training steps”，TIR 与轨迹长度都没有一致趋势。
- **留出任务与平台。** 如上：multi_apps 不在 339 个 online RL 任务池内，Windows 评测覆盖训练中未见的应用。
- **效率参照。** 把所有模型合并、每个任务保留最短的成功含工具轨迹，得到覆盖 249 个任务的实证参照 2.65 次 tool call；ToolCUA 的 2.11 接近该参照，论文据此认为其工具使用是有选择而非滥用的。

## 论文自己承认的薄弱处

- 多样性与源数据耦合：“the diversity and quality of the synthesized hybrid trajectories are coupled with the breadth, fidelity, and task distribution of the source demonstrations.”
- 合成依赖强模型：“replacing stronger proprietary models with Qwen3.5-Plus led to noticeably lower generation efficiency and trajectory quality.”
- 合成工具并非可执行实现，“real-world execution still depends on the maturity of available tools and the way tool feedback is organized”。
- 基准覆盖：“our main performance evaluation is primarily conducted on OSWorld-MCP”。
- 方差：结果是应对沙箱随机性的 average@3，但没有报告标准差或置信区间；R_tool 标签虽经抽样人工核验，仍可能有残余噪声（论文以软权重 λ = 0.4 论证它不会压过任务成功信号）。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **transfer**。判定记录肯定论文报告了：在线评测、留出任务与留出平台、强基线、步数成本、组件消融和已发布代码；标记为未报告的有：average@3 之外的方差、跨模型匹配的训练算力、以及对 next-state grounding MLLM 作为判定器的验证（论文本身报告了对 grounding 过滤器的人工审计）。子模式为 C11：单一动作空间内混合 GUI 与工具调用。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
