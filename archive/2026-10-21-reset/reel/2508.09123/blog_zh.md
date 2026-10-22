# OpenCUA：从人类桌面演示到基于截图的电脑使用智能体的开放流水线

*CUA Radar 对 arXiv 2508.09123v3（Wang、Wang、Lu、Yang、Xie、Wang 等，XLANG Lab 与 Moonshot AI）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2508.09123v3 · 代码：https://github.com/xlang-ai/OpenCUA*

## 问题：最强的 CUA 配方是封闭的

论文的出发点是：最强的 computer-use agent 背后的数据、架构和训练过程都是专有的，而开放的 GUI 数据集范围很窄，要么只做 grounding、移动端或网页，要么缺乏通用桌面使用所需的多样性。论文报告的第一个结果对最直接的基线是负面的：直接在 27K 条 state-action 轨迹上微调视觉-语言-动作模型，OSWorld 上只有 4.4% 的成功率。全文讨论的就是怎样越过这个起点。

## OpenCUA 是什么

OpenCUA 是一个框架而不是单一算法：包括标注工具、数据集、数据处理与推理合成流水线、训练配方，以及一个离线基准。

**智能体。** 这是纯视觉的桌面智能体。观测是屏幕截图（默认用最近三张截图作为视觉历史）。动作空间是 PyAutoGUI 动作的子集：坐标类动作（click、doubleClick、dragTo、scroll），内容类动作（write、press、hotkey），以及报告成功或失败的 terminate。平台为 Windows、macOS 和 Ubuntu。在 CUA Radar 板上它属于 C21，即轨迹级策略训练：对完整轨迹做监督微调。

**数据采集。** AgentNetTool 运行在标注者自己的电脑上，记录屏幕视频、鼠标键盘信号和 accessibility tree。原始的高频信号由规则压缩成有意义的动作，每个动作配上动作发生前的一帧关键帧；关键帧的选取避免了“鼠标已经悬停在按钮上”这类未来信息泄漏。得到的 AgentNet 数据集有 22,625 个任务（Windows 12K、macOS 5K、Ubuntu 5K），平均 18.6 步。论文不要求标注者给出完美示范，只要错误能被识别，就保留下来。

**机制：reflective long chain-of-thought。** 每个 state-action 对都被合成三个层级的推理：L3（observation、thought、action）、L2（thought、action）、L1（仅 action）。reflector 通过对比动作前后的截图检查每一步；被判为错误或冗余的步骤不参与训练，正确的步骤则会得到对状态变化的解释。generator 再根据完整上下文写出结构化推理，并在点击位置加红色标记和放大图块以帮助坐标 grounding；summarizer 负责改写含糊的任务目标。三个角色都使用 Claude 3.7 Sonnet。训练信号完全是监督式的：每一步的人类动作加上这些合成的推理。训练混合三个层级，加入 grounding 数据以及通用文本和视觉 SFT 数据，历史采用 L1 文本加三张截图；推理时使用 L2 格式。

论文采用三种训练策略：只做 stage 2（OpenCUA-Qwen2-7B 基于 Qwen2-VL，OpenCUA-A3B 基于 Kimi-VL-A3B）、stage 1 加 stage 2（OpenCUA-32B 和 72B，基于 Qwen2.5-VL）、联合训练（OpenCUA-7B，基于 Qwen2.5-VL，200B token，128 张 A100 训练八天）。72B 模型还使用了 8k 条在 Ubuntu 环境中用 o3 和 Jedi 采集的轨迹。

## 论文报告的结果

下表是 OSWorld-Verified 成功率（%），由 OSWorld 团队在 AWS 上评测，步数预算为 15、50 和 100（论文 Table 3，竞品行照该表原样列出）。

| 模型            | 15 步    | 50 步    | 100 步   |
|-----------------|----------|----------|----------|
| OpenAI CUA      | 26.0     | 31.3     | 31.4     |
| Claude 4 Sonnet | 31.2     | 43.9     | 41.5     |
| UI-TARS-72B-DPO | 24.0     | 25.8     | 27.1     |
| OpenCUA-7B      | 24.3     | 28.1     | 26.6     |
| OpenCUA-32B     | 29.7     | 34.1     | 34.8     |
| **OpenCUA-72B** | **39.0** | **44.9** | **45.0** |

Claude Sonnet 4.5 在 100 步下列为 61.4，论文也明确说专有模型仍然领先。OpenCUA-72B 被表述为开源模型中的最好结果。所有解码温度为 0，OSWorld-Verified 的结果称为 3 次运行的平均。附录 Table 11 给出逐次细节：100 步时平均值为 26.67（7B）、34.88（32B）和 44.99（72B preview），Pass@3 分别为 36.48、45.10 和 53.02。72B 在 Table 11 中的 15 步和 50 步行只列出一次运行。

离线结果是另一种度量，不能与上表比较。在 AgentNetBench（来自作者自有数据的 100 个留出 Windows 和 macOS 任务，按步匹配）上，OpenCUA-7B 的平均步成功率为 75.2，OpenCUA-32B 为 79.1，对比 OpenAI CUA 的 73.1 和 Qwen2.5-VL-72B 的 67.0。在 grounding 基准上，OpenCUA-72B 在 ScreenSpot-Pro 上为 60.8，在 UI-Vision 上为 37.3；OpenCUA-32B 在 OSWorld-G 上为 59.6，在 ScreenSpot-V2 上为 93.4。

## 论文自带的对照实验

**Reflective CoT。** 在 Qwen2-VL-7B、14K Windows/macOS 加 3K Ubuntu 轨迹上，把 Aguvis 式的短 CoT 换成 reflective long CoT，OSWorld 成功率从 11.5 升到 15.3。作者推测增益来自更好的自我纠错，但没有直接检验。

**CoT 混合与推理格式。** 只用 L2 数据训练得到 13.1，混合 L1、L2、L3 则为 18.5。推理时 L2 为 18.5，L3 为 17.6，L1 为 16.9（15 步预算）。论文指出这与早先工作中 L1 优于 L2 的结论不同，并把差异归因于自己的 L2 推理质量更高。

**数据规模。** 在 7K Ubuntu 轨迹上加入 14K Windows/macOS 轨迹，OSWorld 从 9.8 升到 18.5，作者据此认为存在正向的跨平台迁移。Ubuntu 数据从 3K 增至 10K，平均性能提升 72%；Windows/macOS 数据从 3K 增至 14K，提升 125%。

**Pass@n 与方差。** 对 OpenCUA-Qwen2-7B 在温度 0.1 下采样 16 次，15 步时成功率从 16.9（Pass@1）升到 34.6（Pass@16），50 步时从 18.4 升到 39.2。温度为 0 时，系统日期等微小差异使 Pass@16 为 38.60 而 Pass@1 为 20.10；作者认为这说明智能体对环境的小变化不够鲁棒。

**成本。** 标注历时约六个月、约 20,000 美元；合成 CoT 平均每个任务 0.6 美元，总成本约 32,000 美元。

## 论文自己承认或未覆盖的薄弱处

- 留出评测只是部分成立。作者按操作系统划分数据，并写明“no overlap with OSWorld tasks to prevent data leakage”，但论文没有说明 72B 使用的 8k 条 Ubuntu rollout 是否避开了 OSWorld 的环境或任务。AgentNetBench 来自与训练数据相同的采集；零样本基线没有在其上训练，作者也承认 OpenCUA 得分更高部分是“due to the alignment of the domain and action space”。
- reflector 和 generator 是 LLM 调用（Claude 3.7 Sonnet），由它们决定哪些步骤被丢弃；论文没有报告对其判断的验证。
- 消融实验都是小规模的 Qwen2-VL-7B 运行，72B 没有做消融。Table 6 的两组对比来自不同的运行。
- 论文正文与表格在个别处不一致：Section 4.2 写 Claude 4 Sonnet 在 100 步为 43.9，而 Table 3 在该处为 41.5（43.9 是 50 步的数值）；72B 的 Pass@3 在正文中是 53.2，在 Table 11 中是 53.02。Table 11 中 72B 一行标注为 “preview”。
- 作者列出的局限：数据规模受限于人工标注，标注者未必使用最高效的方法，知情同意带来选择偏差。错误分析列出了任务知识不足、高精度 grounding、动作重复、终止误判、长程任务失败和错误恢复能力弱。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **69 分（★★）**，证据等级 **online**。判定记录认可：OSWorld 团队的在线评测、3 次运行、15/50/100 步预算下的同基准基线、已报告的训练与标注成本，以及组件消融。记录同时把留出环境标为部分成立，把学习得到的 reflector 标为未检验，把代码标为已宣布而非已核实。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v3）。
