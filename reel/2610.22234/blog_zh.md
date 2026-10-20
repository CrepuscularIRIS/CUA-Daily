# OS-Helix：一个既能点击又能写代码的统一策略，基于可验证的合成桌面任务训练

*CUA Radar 对 arXiv 2610.22234v1（Yang、Jin、Ding、Wu、Li、Liu、Cheng、Xu、Sun、Sun、Qiao）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.22234v1 · 代码：https://github.com/OS-Copilot/OS-Helix*

## 问题：桌面任务很少是纯视觉或纯编程的

大多数 computer-using agent（CUA）感知截图，用鼠标键盘行动。论文列出了它的实际代价：小而模糊的界面元素上 grounding 容易失败，即便批量执行动作，结构化状态的操作也很繁琐。代码智能体则相反：它们能直接通过 shell 查看文件、执行复合操作，却处理不了依赖视觉布局或仅通过界面暴露的应用状态的任务。

一个直接的办法是给 GUI 模型加一个代码工具。作者的初步实验表明这还不够：以 Qwen3-VL-32B-Instruct 在 OSWorld-Verified 上测试，只用 GUI 动作为 34.17%，简单开放代码执行后为 32.68%（Table 14）。他们的结论是，GUI/代码的路由必须通过混合数据训练学到，而不是在提示词层面拼接。

## OS-Helix 是什么

**智能体。** 每一步策略看到当前截图和历史；评测时最多保留 8 张历史截图（1504x832）和完整的文本交互历史。它通过一套工具 schema 行动，包含三类动作：GUI 动作（click、drag、type、key、scroll 等，坐标为 1000x1000 的相对网格）、episode 级的 meta 动作（如终止），以及在操作系统上运行 Python 或 Bash 的 code 动作。每个 code 动作在新进程中执行，其 stdout 和 stderr 被追加到上下文。平台是 Ubuntu（OSWorld）和 Windows（WindowsAgentArena）。在 CUA Radar 板上，它属于子模式 C11（在同一动作空间中混合 GUI 动作与代码），主模式为“Decouple Planning from Grounding and Redesign the Action Interface”。

**新的部分**是四阶段的训练流水线。

1.  **Application–artifact composition（应用–文件组合）。** 作者维护一份 45 个应用的清单（44 个具名桌面应用加 1 个系统级 OS 应用），记录固定版本、启动命令和初始化模板，另有一个真实文件库（.docx、.pptx、.xlsx、.pdf、.png、.mp4、.blend、.dxf、项目文件夹等）。一张兼容图把文件类型与能打开它们的应用连起来；每次合成先采样一个应用及兼容文件，实例化出可复现的 Ubuntu 虚拟机状态。
2.  **Decoupled task synthesis（解耦的任务合成）。** Exploration Agent（Claude Sonnet 4.6）先做一小段非破坏性探索（只允许 open、click、scroll、terminate），并参考一份记录已覆盖功能的全局记忆，提出带成功条件的指令。指令被接受后即冻结，由另一个独立的 Evaluator Agent 编译检查逻辑：能用程序判断时用基于规则的检查（针对虚拟机文件和命令行状态），视觉条件用基于 VLM 的检查，或两者结合。评测器必须能编译且在初始状态得分为零；GPT-5.5 审查智能体评估质量，并去除近似重复。过滤前流水线生成了 8,880 个任务，其中多数仅用规则评测器。
3.  **SFT cold start（监督微调冷启动）。** 教师模型为开启了 Computer Use 和 Bash 的 Claude Sonnet 4.6。轨迹由评测器打分后做拒绝采样和过滤，在 83,701 条未过滤样本中保留约 31K 条成功桌面样本，并按约 1:1 与 40K 条通用多模态样本混合。此阶段的训练信号是用于拒绝采样的评测器分数。
4.  **Online RL with Step-balanced GSPO（在线强化学习）。** rollout 在真实的 Ubuntu 沙箱中运行（跨多台机器、超过一百个），配对的规则评测器分数是唯一的结果奖励；无法解析的工具调用奖励记为 0。作者观察到标准 GSPO 会逐渐偏向大量使用代码，并将其归因于较长的 code 动作主导了按 token 平均的样本级重要性比。Step-balanced GSPO 则先在每个动作步内平均 token 的对数比，再对各步等权加权，不受 token 数影响（GUI 步与 code 步权重均为 1.0）。RL 从稠密 27B 的 SFT 检查点出发，训练 1,000 步，且只使用带规则评测器的任务。

基座模型为 Qwen3.5-27B 和 Qwen3.5-35B-A3B，所有评测 episode 的步数上限为 50。

## 论文报告的结果

以下均为平均成功率（%），在线、在真实虚拟机上评测。OSWorld-Verified 在排除 8 个 Google Drive 任务后共 361 个任务。论文没有给出主表的种子数或运行次数，但报告了 Pass@1 和 Pass@3（见下）。标注 “repro.” 的行是作者用同一套 harness 复现的；其余基线来自官方排行榜（OSWorld）或引用结果。

**OSWorld-Verified（Table 1），平均成功率**

| 模型                     | 设置   | 平均      |
|--------------------------|--------|-----------|
| Qwen3.5-27B (repro.)     | GUI    | 46.61     |
| Qwen3.5-27B (repro.)     | Hybrid | 46.50     |
| **OS-Helix-27B**         | Hybrid | **62.75** |
| **OS-Helix-27B-RL**      | Hybrid | **66.44** |
| Qwen3.5-35B-A3B (repro.) | GUI    | 39.20     |
| Qwen3.5-35B-A3B (repro.) | Hybrid | 42.84     |
| OS-Helix-35B-A3B         | Hybrid | 57.27     |
| Agent S3 w/ GPT-5        | Hybrid | 62.63     |
| OS-Symphony w/ GPT-5     | Hybrid | 65.84     |
| Kimi K2.6                | GUI    | 73.07     |
| Qwen3.7-Plus             | GUI    | 73.33     |

论文写明，OS-Helix-27B 和 OS-Helix-35B-A3B 相对各自匹配的 Hybrid 基线分别提升 16.25 和 14.43 个绝对点（相对提升 35.0% 和 33.7%），OS-Helix-27B-RL “further improves by 42.9%” 达到 66.44%。分领域看，SFT 增益最大的是 Office（27B 模型 72.60，其 Hybrid 基线 39.26）和多应用的 Work. 类（54.28 对 38.29）。RL 在 SFT 之上又提升了 Professional（+23.10 个点）、OS（+7.61）和 Daily（+6.69），而 Office 与 Work. 没有进一步提高。作者把这描述为 RL 只在特定领域带来增益，而非全基准均匀提升。论文称 OS-Helix-27B-RL 与基于 GPT-5 的框架相当，同时指出更新、规模大得多的通用模型整体仍更强。

**WindowsAgentArena（Table 2，50 步预算，混合动作空间，code 动作限定为 Python）**

| 模型                        | 平均  |
|-----------------------------|-------|
| Qwen3.5-27B GUI (repro.)    | 40.82 |
| Qwen3.5-27B Hybrid (repro.) | 56.41 |
| Agent S3 w/ GPT-5           | 54.10 |
| OS-Symphony w/ GPT-5        | 63.45 |
| OS-Helix-27B                | 57.95 |
| OS-Helix-27B-RL             | 63.87 |

论文报告 RL 模型相对 GUI 基线提升 23.05 个点，相对 Hybrid 基线提升 7.46 个点，且训练中没有任何 Windows 专用数据。

**离线指标。** grounding 基准是离线的，单独列出：基于 Qwen3-VL-32B-Instruct 的 32B SFT 变体在 OSWorld-G 上为 57.21，复现的基座为 61.35；ScreenSpot-V2 上为 93.47 对 95.05（Table 13）。作者认为这一下降在预期之内，因为训练把容量从孤立的 grounding 转向了混合执行。

## 论文自带的对照实验

- **同一 harness 与预算。** 所有复现的基线使用相同的 harness 和环境配置；WindowsAgentArena 的所有条目都使用 50 步预算和混合动作空间。
- **去除领域。** 从 SFT 数据中去掉九个与 OSWorld 相关的应用领域（约 31K 减到约 17K 样本），成功率从 62.75% 变为 62.31%。
- **教师模型。** 基于 800 个合成任务采集的轨迹，Kimi K2.5 做教师得 54.03，Claude Sonnet 4.6 做教师得 58.77，均高于未适配的 Hybrid 基座。
- **训练阶段（Table 4）。** Hybrid 基座 46.50，仅 RL 48.20（+1.70），仅 SFT 62.75，SFT 后接 RL 66.44。SFT 提供主要增益。
- **RL 目标。** 在相同的 SFT 初始化、数据、采样、奖励和预算下，标准 GSPO 为 60.47（相对 SFT 为 -2.28），code 动作占比从 27.9% 升到 40.0%；Step-balanced GSPO 为 66.44，code 动作占比 26.1%。
- **代码访问。** 同一个 OS-Helix-27B 检查点，关闭 code 为 52.13，开启为 62.75。在固定 10K 样本 SFT 预算下，纯 GUI 轨迹为 57.56，混合轨迹为 60.61（高 3.05 个点）。
- **重复采样。** 从 SFT 到 RL，Pass@1 从 62.75% 升到 66.44%，Pass@3 从 70.88% 升到 76.44%（+5.56），对 361 个任务做配对 bootstrap 的 95% 区间为 \[2.24, 8.97\]。Pass@1 提升在论文 Table 16 中的区间为 \[0.93, 8.33\]。
- **换基座（仅 SFT）。** 在 Qwen3-VL-32B-Instruct 上，朴素 Hybrid 为 32.68，OS-Helix-32B 为 50.56；Thinking 基座上分别为 42.88 和 51.67。Thinking 变体在 Professional 一个领域出现下降。
- **效率与行为。** OS-Helix-27B 在小步数预算下使用更少交互（Figure 3）。对 30 条 Work. 轨迹的人工审计中，27 条含有有据可依的 GUI/code 交接；论文提醒该子集不一定代表整个基准。

## 论文自己承认的薄弱处

- 自动验证 “remains imperfect”：评测器 “carry intrinsic brittleness”，且基于 VLM 的评分被排除在 RL 奖励之外。论文没有报告对评测器准确率的人工核验。
- RL 只在 “dense 27B model” 上做，超参较保守；35B-A3B 的 MoE 模型没有做 RL，也没有研究 RL 的扩展规律。
- 不可行任务（约占 OSWorld 和 WindowsAgentArena 的 10%）不会由流水线生成，模型可能不会主动停止；去掉它们后平均成功率 “up to 3-5 absolute points” 地提高（论文原话）。
- 在 WindowsAgentArena 上，code 动作通过修改提示限定为 Python，失败轨迹常把 Bash 风格的写法混进 Windows 执行。
- 许多现有基准是为纯 GUI 智能体设计的，评测器可能不接受所有合法的 GUI/code 解法；只用成功率也无法反映代码执行带来的安全风险。
- 论文表示 “will release” 模型、环境和数据；本文未核查代码仓库。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **75 分（★★★）**，证据等级 **transfer**。判定记录认可：OSWorld-Verified 上的在线评测、去除领域的对照、Pass@3 的 bootstrap 区间、同一 harness 和 50 步预算下复现的基线、步数与效率报告，以及组件消融；WindowsAgentArena 提供迁移证据。论文没有报告评测器或判定器的验证，代码是否可用从论文中也无法确定。判定还标出了 AP5：合成数据与被评测的应用有重叠，因此除上述去除领域实验外，增益无法与领域内暴露完全分开。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
