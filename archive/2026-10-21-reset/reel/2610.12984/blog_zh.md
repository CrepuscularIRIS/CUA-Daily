# Work2Skill：把录下来的真人桌面操作变成可复用的智能体技能

*CUA Radar 对 arXiv 2610.12984v1（Huang、Li、Cao、Cai、Xie、Gao、Guo、Zhang、Li、Zheng、Yan、Liao）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.12984v1 · 代码：https://github.com/china-qijizhifeng/Work2Skill*

## 问题：任务指令里没写的流程知识

“帮我提交报销”并不会说明用哪个内部系统、附哪些发票、提交前要检查什么。Computer-use agent 恰恰在这种陌生软件和组织专属流程上失败。人类示范是这类知识的天然来源，因为人和智能体共享同一个 GUI 交互空间。论文指出复用示范的三个障碍：动作坐标只说明点击发生在哪，不说明控件是什么；此前的示范研究在示范来源、任务集和执行协议上各不相同，数字之间不可比；固定的解析流水线预先规定了查看顺序，而一次性把长录像装进上下文会造成压力，预先挑帧又会丢掉后面才需要的细节。

## Work2Skill 是什么

三个组件，各对准一个障碍。

**WorkRecorder** 是采集基础设施。macOS 端录制屏幕区域（H.264 视频）和鼠标键盘活动；对远程 Linux 桌面，目标会话内的 AT-SPI collector 提供 accessibility tree（AX）快照、点查询和目标元素信息（名称、角色、边界），取决于应用的无障碍支持。输入事件被组成语义动作——点击、拖拽、滚动、快捷键——并与关键帧对齐到同一条视频时间轴上，因此每个动作都链接到它的屏幕图像、可用的目标信息和前后视频。论文明确说明：对齐用的是启发式时间容差，“not measured accuracy bounds”。

**WorkDemo-350** 是数据集：350 段人类示范，覆盖全部 64 个 MyPCBench Bounded Action 任务和一个固定的 286 任务 OSWorld-Verified 子集，经过完整性与任务成功筛选——共约 8.48 小时录制经验，平均单集时长 119.11 秒（MyPCBench）与 80.04 秒（OSWorld），平均每集约 32.23 与 34.57 个动作。

**Agentic skill induction** 是方法。一个 NexAU 工具型智能体拿到单个证据包（task.json、动作轨迹、keylog、索引图像、视频）和一份 skill-creator 撰写规范。系统提示刻意保持简短；智能体自己决定查看什么：文件工具（`read_file`、`glob`）、读索引图像的 `read_visual_evidence`、按区间或精确时间戳取帧的 `watch_video` / `extract_video_frames`。查证据和写技能在同一个对话里交替，草稿暴露出缺失约束时可以回到源材料。输出是 SKILL.md 文件（Agent Skills 约定），包含语义化 UI 目标、流程规则、步骤依赖和可见的完成检查——“without the source recording” 也能执行。这里没有训练、没有奖励：归纳期间候选技能不被执行，“downstream evaluation results are not used as revision feedback”；`finalize_extraction` 只校验结构和工具使用，论文明说这些检查 “do not verify skill correctness or task success”。

执行时技能只是纯文本，通过共享的 `<task skills>` 包装追加到执行器的 system prompt 末尾；执行器（基于截图与动作的 VM 循环，经 PyAutoGUI 执行；MyPCBench 上还可用 Bash）看不到录像。在 CUA Radar 板上，它的架构模式是 R03（mine human screen recordings into action knowledge）：人类屏幕录像加输入流，蒸馏成动作智能体可用的操作知识。

## 论文报告的结果

以下全部是在线、基于执行结果的评测，使用各基准官方 evaluator；论文没有报告任何离线单步准确率指标。执行模型：GPT-5.5、Opus-4.8、Qwen3.5-35B-A3B、Qwen3.5-9B；默认每个模型执行自己归纳的技能。每个模型与基准共享同一套设置：temperature 0、high reasoning effort、100 步执行上限、100 轮归纳上限。论文未报告随机种子或重复次数。Score 是 evaluator 输出均值换算到 0–100；SR 是满分任务占比。

MyPCBench Bounded Action（64 任务），Score / SR（%）：

| 方法 | GPT-5.5 | Opus-4.8 | Qwen3.5-35B-A3B | Qwen3.5-9B |
|----|----|----|----|----|
| No Skill | 74.73 / 23.44 | 81.53 / 42.19 | 38.38 / 9.38 | 24.27 / 6.25 |
| Aloha | 77.48 / 37.50 | 79.27 / 34.38 | 37.69 / 12.50 | 26.61 / 3.13 |
| D2T | 75.25 / 37.50 | 81.28 / 42.19 | 40.61 / 9.38 | 27.75 / 6.25 |
| **Work2Skill** | **85.27 / 48.44** | **86.20 / 50.00** | **44.56 / 20.31** | **34.11 / 12.50** |

OSWorld-Verified 子集（286 任务），Score / SR（%）：

| 方法 | GPT-5.5 | Opus-4.8 | Qwen3.5-35B-A3B | Qwen3.5-9B |
|----|----|----|----|----|
| No Skill | 74.47 / 70.98 | 79.23 / 77.97 | 32.52 / 32.17 | 27.48 / 26.92 |
| Aloha | 72.57 / 69.93 | 78.91 / 76.57 | 31.08 / 30.42 | 24.81 / 24.13 |
| D2T | 80.32 / 76.22 | 80.66 / 78.67 | 33.93 / 32.52 | 26.45 / 25.52 |
| **Work2Skill** | **81.97 / 78.67** | **82.34 / 79.37** | **36.36 / 36.01** | **33.41 / 32.52** |

Work2Skill 在每个”模型 × 基准”单元里都拿到最高 Score 和 SR。相对 No Skill，MyPCBench 平均分提升 4.67–10.54（SR 提升 6.25 到 25.00 个百分点），OSWorld 子集提升 3.11–7.50（SR 提升 1.40 到 7.69）。成本依模型而异：相对 No Skill，Opus-4.8 和两个 Qwen 模型执行步数更少、GPT-5.5 更多；归纳 token 用量（GPT-5.5 在 MyPCBench 为 334.52 k、OSWorld 为 185.19 k）相对基线 “not consistently lower”。

## 论文自带的对照实验

**换任务实例复用（MyPCBench Jitter）。** 64 个任务各配一个变体，在同一应用内改变实体、参数或约束；原技能不做重新归纳直接复用。四个执行器上 Work2Skill 相对 No Skill Score 提升 3.93–8.64、SR 提升 6.25–9.38 个百分点（GPT-5.5：81.75 对 73.45；Opus-4.8：87.23 对 83.30；Qwen3.5-35B-A3B：51.58 对 42.94；Qwen3.5-9B：36.25 对 27.80），步数减少 2.49–5.44，对每个执行器上更强的示范基线优势为 4.28–6.25 分。

**跨模型迁移。** 冻结归纳出的技能、交换执行器（GPT-5.5 × Qwen3.5-9B），四种归纳/执行组合都超过同一执行器的 No Skill 基线；GPT-5.5 归纳的技能在两个执行器下都优于 Qwen3.5-9B 归纳的，在 GPT-5.5 执行下优势 “reaching 9.46 score points and 9.38 percentage points”——但无论谁来归纳，Qwen3.5-9B 执行的绝对水平仍然低得多。

**证据消融（64 任务，GPT-5.5）。** 归纳时去掉索引图像、UI 注释或 KeyLogs，Score 下降 5.02–10.63、SR 下降 14.06–21.88 个百分点；Score 最大损失来自去掉索引图像，SR 最大损失来自去掉 KeyLogs。只用带 UI 语义的动作文本仍优于只用视频且步数最少，但两者都落后于全量证据。

**提示设计。** 与规定归纳阶段的 Pipeline Prompt 相比，简短的自由探索提示 Score 高 3.97、SR 高 6.25 个百分点，步数从 48.98 降到 47.38，代价是归纳 token 用量高 12.7%。

**对齐比较。** Aloha 与 D2T 被文本化适配进同一包装、来自同一批源示范、在同一执行器/步数上限/evaluator 下运行——比较隔离的是指导文本本身，而不是执行框架。

## 论文自己承认的薄弱处

- 示范直接采自基准任务，RQ1 就在这些被示范的任务上评测；泛化只通过”within the same application context”的 Jitter 变体和一个双模型迁移矩阵探测。
- OSWorld 集是筛选过的：“we first exclude infeasible tasks for which a valid human demonstration cannot be completed”，且 “OSWorld results apply to this curated subset”。
- 未报告种子或重复运行，运行间方差未知。
- AX 覆盖 “depends on the recording configuration and the application’s accessibility support”，时间对齐窗口是 “implementation tolerances, not measured accuracy bounds”。
- Jitter 变体由 GPT-5.6-sol 协助起草、再经人工核验。
- 案例研究（带后备餐厅的 TableFind 订位）是单个示例：两个基线在八项 rubric 上得 55/100，Work2Skill 得 100/100。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **online**。分数反映论文所报告的证据：两个基准上的在线评测（官方 evaluator）、同示范同设置的强基线对比（适配后的 ShowUI-Aloha、Demo2Tutorial）、归纳 token 成本、证据模态消融与提示对比，以及公开的代码和数据。判定记录把 held-out 环境标为 partial（Jitter 变体留在同一应用内），未报告项包括 variance（无种子）与 budget match；同时标记反模式 AP5——用于归纳的经验数据与评测集重叠，因为示范就采自评测任务。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
