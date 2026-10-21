# Agent S2：把动作路由给专家 grounder、每完成一个子目标就重规划的 computer-use agent

*CUA Radar 对 arXiv 2504.00906v1（Agashe、Wong、Tu、Yang、Li、Wang，Simular Research）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2504.00906v1 · 代码：https://github.com/simular-ai/Agent-S*

## 问题：一个 generalist 包办一切，在三处掉链子

Computer-use agent 直接操作图形界面来完成桌面或手机任务。论文指出了 monolithic agent（单一 generalist 模型包办一切）的三个限制。其一是 grounding：把界面元素的文字描述映射到精确像素坐标仍然不可靠。其二是长程任务：任务跨越多个应用和屏幕，弹窗、干扰和不断变化的观察会让一开始定死的计划失效。其三是 generalist 瓶颈：让同一个模型同时负责 planning、action 和 grounding，它在特定子任务上”往往不如 specialist 模型”，最终”制约了 computer-use agent 的整体表现”。

## Agent S2 是什么

Agent S2 是一个纯 prompting 的组合式框架，本文中没有任何组件经过训练。感知输入只有 **screenshot 加 action history**——刻意不用早期分层 agent 依赖的 accessibility tree。动作是一个 function-call 风格的动作空间（论文 Table 8）：click、type、scroll、hotkey、hold and press、drag and drop、highlight text span、set cell values、save to knowledge、switch applications、wait、done、fail。平台覆盖桌面 Linux（OSWorld，369 个任务）、Windows（WindowsAgentArena，154 个任务）和 Android（AndroidWorld，116 个任务、20 个应用；因任务较短，采用 worker-only 配置）。它在 CUA Radar 板上的架构模式是 C10：“把描述目标的 generalist planner 与负责定位的 specialist grounder 拆开”。

论文的两个核心机制：

1.  **Mixture of Grounding（MoG）。** generalist 的 Worker 产出一个原子动作和目标的自然语言描述，然后像 gating network 一样把 grounding 路由给三个 specialist 之一：Visual Grounding expert（UI-TARS-72B-DPO）对屏幕上任意一点返回像素坐标；Textual Grounding expert（Tesseract OCR）接收 span 的起始和结束短语，返回词级选区坐标；Structural Grounding expert（UNO 接口）接收 cell:value 字典，以编程方式写入表格单元。Worker 还可以逐步细化描述来自我纠正。
2.  **Proactive Hierarchical Planning（PHP）。** generalist 的 Manager 把指令分解为 subgoal。**每完成一个** subgoal——而不是像 reactive planning 那样只在失败后——Manager 就根据原始指令、已完成的 subgoal 和最新 screenshot 重新生成剩余的 subgoal，让任务随着观察的演变不断被重新语境化。

系统还复用了 Agent S 的知识库（任务级与子目标级交互经验以及网络知识）。Agent S2 本身没有任何训练信号；起作用的是”组合”：Worker 每一步把动作路由给哪个 specialist，以及每次重规划所依据的新观察。

## 论文报告的结果

以下全部是**在线成功率**，由功能性脚本判定；论文没有报告任何离线的单步或 grounding 准确率。步数预算为 15 步和 50 步；在 OSWorld 和 WindowsAgentArena 上，agent 未宣告完成就耗尽步数记为失败。论文未报告随机种子、重复次数或方差。

| 方法                                | OSWorld 15 步 | OSWorld 50 步 |
|-------------------------------------|---------------|---------------|
| CCU w/ Claude-3.5-Sonnet (new)      | 14.9          | 22.0          |
| CCU w/ Claude-3.7-Sonnet            | 15.5          | 26.0          |
| OpenAI CUA (Operator)               | 19.7          | 32.6          |
| UI-TARS-72B-DPO                     | 22.7          | 24.6          |
| Agent S2 w/ Claude-3.5-Sonnet (new) | 24.5          | 33.7          |
| **Agent S2 w/ Claude-3.7-Sonnet**   | **27.0**      | **34.5**      |

论文报告相对领先基线（脚注注明为 UI-TARS 与 Claude Computer Use）提升 18.9%（15 步）和 32.7%（50 步）。50 步设置下，Claude-3.7 版本在 OS 类任务为 50.00，Daily 为 49.73，Professional 为 57.14，但 Office 只有 25.64、Workflow 只有 18.21——难的类别仍然难。

| 方法         | WindowsAgentArena（15 步） |
|--------------|----------------------------|
| Agent S      | 18.2                       |
| NAVI         | 19.5                       |
| **Agent S2** | **29.8**                   |

| 方法             | AndroidWorld |
|------------------|--------------|
| GPT-4o + UGround | 44.0         |
| GPT-4o + Aria-UI | 44.8         |
| UI-TARS-72B-SFT  | 46.6         |
| **Agent S2**     | **54.3**     |

论文报告在 WindowsAgentArena 上相对 NAVI 提升 52.8%，在 AndroidWorld 上相对 UI-TARS 提升 16.52%。注意输入不对称：WindowsAgentArena 上 Agent S 和 NAVI 还读取 accessibility tree，而 Agent S2 只用 screenshot；OSWorld 上除 Agent S 外所列基线均为 screenshot 输入。

## 论文自带的对照实验

- **步数预算标准化。** 同一批 agent 同时给出 15 步与 50 步成绩；Agent S2 的领先随预算扩大（27.0 到 34.5），而 UI-TARS-72B-DPO 几乎不动（22.7 到 24.6）。
- **更换基座。** Manager 和 Worker 都换成 Claude-3.5-Sonnet (new)，Agent S2 仍有 24.5 / 33.7；论文报告这相当于相对更强基座的 Claude Computer Use 提升 58.1%（15 步）与 29.6%（50 步）——说明增益来自组合而非基座。
- **组件消融（OSWorld 65 任务子集）。** 去掉 MoG，成功率从 30.77 降到 27.69（15 步）、从 38.46 降到 33.85（50 步）；proactive 相对 reactive planning 在 15 步和 50 步分别带来 +4.62 和 +6.15 个点。在路由到对应专家的任务上去掉 Textual expert，子任务成功率从 70.6% 降到 65.2%；去掉 Structural expert 从 73.7% 降到 69.4%。
- **grounding expert 替换。** 在 visual 槽位上，更小的开源模型（UI-TARS-7B-DPO、UGround-V1-7B）在框架内表现超过 Claude-3.7-Sonnet——specialist 不必很大。
- **错误分析。** grounding 被分担后，planning 失败成为最频繁的错误类别，grounding 错误的占比相对此前工作的报告更低。
- **scaling 行为。** 对 15 步失败而 50 步成功的任务，论文把翻转主要归因于 adaptive navigation 与 adaptive interaction，其次是 backward correction 和客观上需要更多步数的任务复杂度。

## 论文自己承认的薄弱处

- 所有 headline 数字都没有种子、重复次数或方差。
- 没有报告成本，而该框架每步要调用多个模型（Manager、Worker、expert）。
- 消融在 OSWorld 的 65 任务分层子集上完成，而非全部 369 个任务。
- 相对提升百分比按基准分别选用不同基线（脚注 1），正文并不总是重申这一点。
- Structural expert 是面向特定应用的 API（LibreOffice 的 UNO）；论文自己的失败分析指出 planning 失败如今占主导，OSWorld 中 Office（25.64）与 Workflow（18.21）仍是最弱的类别。
- AndroidWorld 只用 worker-only 评估，Manager/PHP 机制在该基准上未被检验。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **transfer**，子模式为 planner-grounder-interface 下的 C10。判定记录认可：在线评测、向其他操作系统与应用的泛化（held-out）、强基线（OpenAI CUA、Claude Computer Use、UI-TARS）、对齐的 15/50 步预算、组件消融和已发布的代码；同时标出 variance 与 cost 未报告。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
