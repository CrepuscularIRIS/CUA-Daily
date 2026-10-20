# UI-TARS-2：用数据飞轮和稳定化的多轮 RL 训练的原生 GUI agent

*CUA Radar 对 arXiv 2509.02544v2（ByteDance Seed）的解读。这是第三方对论文所报告内容的总结，并非作者背书。海报：`poster.png`。论文：https://arxiv.org/abs/2509.02544v2 · 代码：https://github.com/bytedance/ui-tars*

## 问题：通用 computer-use agent 的四个未解难题

这份技术报告点出了数据可扩展性、多轮强化学习、仅用 GUI 操作的局限以及环境稳定性方面的未解问题。带推理的长程 GUI 轨迹收集成本很高；多轮 RL 面临稀疏奖励和长序列上的 credit assignment；真实工作流除了屏幕还涉及文件和终端；而大规模训练需要能在数百万次 rollout 中保持稳定的沙箱。

## UI-TARS-2 是什么

UI-TARS-2 是一个“原生”模型：一个 Mixture-of-Experts LLM，激活参数 23B（总计 230B），加上 532M 参数的视觉编码器，初始化自 Seed-thinking-1.6。它遵循“思考、动作、观察”的 ReAct 循环。它看到截图，通过 GUI 原语（点击、输入、滚动）行动，或在扩展的动作空间里调用 SDK 函数：终端命令和 MCP 工具调用。工作记忆保留最近 N 步，情景记忆保存更早 episode 的压缩摘要。在 CUA Radar 板上，这篇论文属于 C11 模式，即 planner 与 grounder 的接口。

论文的方法有四个部分：

1.  **一体化沙箱。** Windows、Ubuntu 和 Android 的云端虚拟机（PyAutoGUI 与 ADB），共享文件系统（在浏览器里下载的文件可以直接在 shell 里处理），以及用于 HTML5 小游戏的硬件加速浏览器沙箱。
2.  **数据飞轮。** 每一轮由当前模型通过 rejection sampling 或交互式标注产生轨迹。验证函数 V(s) ∈ {0, 1} 把通过的样本送入 SFT 集合，把未通过的送入继续预训练（CT）集合，然后模型依次经过 CT、SFT 和 RL 重新训练。标注包括边做边说（think-aloud）的录音，以及 on-policy 的交互式模式：标注员接受或改写模型提出的下一步。
3.  **多轮 RL（PPO）。** 带有状态保持环境的异步服务器式 rollout 和流式 rollout 池，外加 reward shaping、解耦且随长度自适应的 GAE、value 预训练和 DAPO 风格的 “clip higher”。奖励有三个来源：脚本检查（游戏）、对照参考答案的 LLM judge（GUI-Browsing），以及对覆盖 690 个网站的开放式 GUI-General 任务，由 UI-TARS-2 自己充当生成式 outcome reward model。
4.  **合并。** 各个领域专门化的 RL 模型（浏览、通用网页、游戏、SDK）通过参数插值合并。

## 论文报告的结果

online 成功率（%）。“-” 表示论文 Table 1 没有给出数值。在这些基准上，UI-TARS-2 可以使用 GUI 操作或 GUI SDK 两种方式之一。

| 模型 | OSWorld (369) | WindowsAgentArena (150+) | AndroidWorld (116) | Online-Mind2Web (300) |
|----|----|----|----|----|
| Claude-4-Sonnet | 43.9 | \- | \- | \- |
| OpenAI CUA-o3 | 42.9 | \- | 52.5 | 71.0 |
| UI-TARS-1.5 | 42.5 | 42.1 | 64.2 | 75.8 |
| **UI-TARS-2** | **47.5** | **50.6** | **73.3** | **88.2** |

论文称 UI-TARS-2 在所有报告的基准上都超过了 UI-TARS-1.5。Table 1 没有说明这些行的步数预算和运行次数。

在 SDK 扩展下，论文报告 Terminal Bench 为 45.3，SWE-Bench Verified 为 68.7，BrowseComp-zh 为 50.5，BrowseComp-en 为 29.6。在一套另外的 15 个浏览器游戏的内部测试集上，按人类水平归一化的平均分，RL 模型为 59.77，其 SFT 模型为 44.27，OpenAI CUA 为 24.73，Claude Computer Use 为 21.61。这些游戏数字来自作者自己的测试集，与上面的 GUI 表格不可比。

## 论文自带的对照说明了什么

**RL 与 SFT。** 在 Online-Mind2Web 上，RL 把准确率从 83.7（最后一轮迭代的 SFT 基线）提高到 88.2。论文强调了在训练重点之外的迁移：OSWorld 从 43.0 到 47.5，AndroidWorld 从 64.6 到 73.3。训练任务（GUI-Browsing、GUI-General）大多是基于浏览器的。

**仅 GUI 与 SDK。** 限制在仅 GUI 操作时，BrowseComp-zh 和 BrowseComp-en 分别为 32.1 和 7.0；有 SDK 时为 50.5 和 29.6。

**量化。** 使用 W4A8 量化后，OSWorld 从 47.5 降到 44.4，同时解码速度从每秒 29.6 个 token 提高到 47 个，每轮延迟从 4.0 秒降到 2.5 秒。

**步数预算。** 另一项推理时 scaling 分析（Figure 11）显示，随着最大允许步数从 20 增加到 100，OSWorld 分数持续上升，尽管 RL 训练缩短了轨迹；具体数值只出现在图中。

**PPO 与 GRPO。** 在初步评测中，论文发现 PPO 稳定地明显优于 GRPO；它给出的是训练奖励曲线，而不是基准数字。

**奖励模型。** 内部的 outcome reward model 在 300 条人工标注的轨迹上 F1 为 83.8；论文指出其假阳性率相对较高，同时认为正确的中间步骤仍会获得合适的奖励，并报告人工检查没有发现明显的 reward hacking。

## 证据偏薄之处

- GUI 基准上没有报告随机种子、标准差或区间，基线的步数预算在正文中也没有说明。
- RL 与 SFT 的比较发生在作者自己的流程内（最后一轮迭代的 SFT 基线）。论文把 OSWorld 和 AndroidWorld 描述为并非主要训练重点，但没有说明它们的任务是否与训练任务重叠。
- 论文把 OSWorld 的提升写成“nearly 10.5%”（43.0 到 47.5，是相对值），把 AndroidWorld 的提升写成“over 8.7%”（64.6 到 73.3，是绝对差）；我们引用的是原始数字。
- GUI-General 任务的训练信号一部分来自模型自己的 judge，论文承认它存在假阳性。
- 训练的成本和算力没有报告。

## CUA Radar 的解读

CUA Radar 给这篇论文打 **67 分（★★）**，证据等级 **transfer**。记录认可：四个 GUI 基准上的 online 评测、强的闭源基线、RL 与 SFT 的比较、GUI 与 SDK 的比较，以及在 300 条标注轨迹上对学习到的奖励模型的检验。它标注了学习到的 judge（反模式 AP4），把 held-out 评测标为 partial，并把方差、匹配的预算和成本记为未说明或 unclear，把代码记为 unclear，尽管标题页给出了项目仓库链接。CUA Radar 没有重跑任何实验；本文所有数字都来自论文（版本 v2）。
