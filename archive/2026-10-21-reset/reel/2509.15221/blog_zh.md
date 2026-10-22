# ScaleCUA：面向纯截图电脑操作智能体的开放数据管线与模型家族

*CUA Radar 对 arXiv 2509.15221v2（Liu、Xie、Ding、Li、Yang、Wu 等）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2509.15221v2 · 代码：https://github.com/OpenGVLab/ScaleCUA*

## 问题：GUI 操作轨迹太稀缺

论文从数据问题讲起。图文对在网上随处可得，但“computer-use data, particularly operation trajectories, are rare, costly to collect”。软件和网页不断更新，已有轨迹会过时；强力智能体背后的 GUI 语料往往是闭源的。作者还指出，现有开源数据集在覆盖面和多样性上有限，桌面端尤其如此。人工采集质量高但无法扩展；自动探索可以扩展但噪声大。论文给出的方案是：构建大规模跨平台语料，并用它训练一组基座模型。

## ScaleCUA 是什么

**智能体。** ScaleCUA 由 Qwen2.5-VL 微调而来，有 3B、7B、32B 三个规模。它只看截图：论文写明“our models are evaluated with pure visual observation on all benchmarks”，并认为这样可以避开嘈杂的无障碍树和 DOM 数据的干扰。动作是坐标级命令，来自覆盖桌面、浏览器和移动端的统一动作空间（click、write、scroll、hotkey、dragTo、swipe、open app 等）。它在 CUA Radar 板上的架构模式是 C12：把异构轨迹归一到一个声明好的动作模式里，训练截图策略。

**三种推理模式。** Grounding Mode 针对一段元素描述返回点或边界框，因此可以让 GPT-4o 这样更强的 planner 配合 ScaleCUA 作 grounder。Direct Action Mode 输出一句简短的操作描述加可执行动作。Reasoned Action Mode 先写一段思考，再给出动作。

**数据管线。** 两个循环为语料供数。agent-environment 循环覆盖 Windows、Ubuntu、macOS、Android、iOS 和 Web，元素框来自桌面端的 A11y tree、Web 的 DOM 和 Android 的 XML 布局；树不完整或不可用时用 OmniParser 补足。agent-human 循环加入专家录制的、带明确目标的轨迹，在 Docker 容器中采集。自动探索方面，作者发现 VLM 驱动的智能体有偏差、多样性不足，于是改用规则驱动的随机游走（深度优先搜索加剪枝）。原始轨迹按屏幕相似度切成 weak-semantic（弱语义）子轨迹。GPT-4o 和 Claude-3.7 负责标注外观、位置和功能；增强手段包括裁剪元素、拼接截图和替换背景。

**语料规模。** 471K 条 GUI 理解样本、17.1M 条 grounding 样本（点、框和动作三种形式，基于 1.6M 张图像），以及 19K 条轨迹（平均 9 步），其中 4K 条是人工整理的目标导向演示。训练时按 GUI 数据量的 25%、50%、75% 分别给 3B、7B、32B 混入通用多模态数据。训练信号是监督式的；论文明确把 RL、奖励模型、reflection 和 memory 留给未来工作。

## 论文报告的结果

以下数字均抄自论文表格。先给**在线**成功率（Table 5），离线结果另列。15 步、50 步是步数预算；AndroidWorld 使用每个任务自带的预设上限。

| 在线成功率 (%) | AndroidWorld | OSWorld (50) | WindowsAgentArena (50) | MacOSArena (50) | WebArena-Lite-v2 (50) |
|----|----|----|----|----|----|
| ScaleCUA-3B | 23.7 | 12.4 | 15.2 | 1.4 | 33.1 |
| ScaleCUA-7B | 27.2 | 15.0 | 20.7 | 4.3 | 37.7 |
| **ScaleCUA-32B** | 30.6 | 17.7 | 24.2 | 7.1 | **47.4** |
| UI-TARS-72B-DPO | 46.6 | 25.2 | 17.9 | 8.6 | 21.4 |
| UI-TARS-1.5-7B | 31.6 | 23.9 | 15.9 | 7.1 | 26.0 |
| Qwen2.5-VL-72B | 27.6 | 10.6 | 9.7 | 5.7 | 14.4 |
| GPT-4o + UI-TARS-1.5-7B（grounder） | 37.9 | 19.1 | 26.2 | 0.0 | 28.6 |
| GPT-4o + **ScaleCUA-7B**（grounder） | **48.3** | 28.1 | 36.6 | 8.6 | 35.1 |

按表中所印读数：在原生（native）模型一栏里，ScaleCUA-32B 的 WebArena-Lite-v2 最高（50 步 47.4；15 步 44.2，UI-TARS-72B-DPO 为 23.4），所列原生行中 WindowsAgentArena 的 50 步成绩也最高（24.2）。在 OSWorld 上，它的 17.7 低于 UI-TARS-72B-DPO（25.2）和 UI-TARS-1.5-7B（23.9）；表中还列出 OpenCUA-32B 的 34.1、Seed1.5-VL 的 39.6 和 COMPUTERRL 的 47.3，后两者的步数标注为超过 50 或未知。所有模型在 MacOSArena 上得分都很低，论文将其解读为特定操作系统的 affordance 缺口。以 GPT-4o 作 planner、ScaleCUA-7B 作 grounder 时，AndroidWorld 为 48.3，OSWorld 和 WindowsAgentArena 分别为 28.1 和 36.6，WebArena-Lite-v2 为 35.1，高于表中其他给出相应列数据的 grounder。论文正文称，从 3B 到 7B 再到 32B，Windows 和 Web 上收益单调上升。

**WebArena-Lite-v2** 是作者对 WebArena-Lite 的升级版：共 154 个任务（从 165 个中去掉 11 个多标签页任务），使用本地 Docker 网站，适配纯视觉评测，并修订了指令和答案判定。

**离线结果**（与上表分开）。MMBench-GUI L1（GUI 理解，选择题）：ScaleCUA-32B 在 easy、medium、hard 上分别为 92.5、92.5 和 94.4，GUI-Owl-32B 为 92.8、91.7 和 94.2。Grounding：ScreenSpot-v2 为 94.7（Table 3 同时列出 Seed-1.5-VL 的 95.2 和 UI-TARS-1.5 的 94.2），ScreenSpot-Pro 为 59.2（GUI-Owl-32B 为 58.0），OSWorld-G 为 60.6（Table 8 列出 Seed1.5-VL 为 62.9）。AndroidControl-High 上，ScaleCUA-32B 的步成功率为 75.9，UI-TARS-72B 为 74.7；AndroidControl-Low 上它的 85.7 低于 UI-TARS-72B（91.3）和 Qwen2.5-VL-72B（93.7）。ScienceBoard 上 ScaleCUA-32B 为 5.9，低于 Qwen2.5-VL-72B（12.9）和 Claude-3.7-Sonnet（10.5）。

## 论文自带的对照实验

Table 6 的所有消融都使用 **3B** 模型。

- **数据增强**（仅 GUI 数据，ScreenSpot-Pro，离线）：无增强 37.8，加入元素裁剪和截图拼接后 41.3。
- **Weak-semantic 轨迹**（仅公开数据，在线，50 步）：OSWorld 从 7.9 升到 8.5；WebArena-Lite-v2 从 8.4 升到 14.3。
- **坐标形式**：ScreenSpot-Pro 上原始坐标 42.3，归一化坐标 37.9。
- **训练分辨率**：2K 在 ScreenSpot-Pro 上为 45.5（1080P 为 42.3），但在线的 AndroidWorld 从 23.3 降到 13.4，OSWorld 从 12.4 降到 11.2。
- **Direct 与 Reasoned Action**：推理模式带来 +1.4% 到 +8.2% 的绝对提升，论文称在 WebArena-Lite-v2 上尤其明显，代价是延迟更高。
- **数据规模**：增益大致呈对数趋势，多数在 75% 数据之后趋于饱和；WebArena-Lite-v2 近乎线性。
- **通用多模态数据**：占比上升时，GUI 基准逐步下降而通用基准上升，约在 75% 达到峰值。ScaleCUA-32B (75%) 在 MathVista 和 MMMU 上为 69.8 和 61.9，低于 Qwen2.5-VL-32B 的 74.7 和 70.0。

## 证据偏薄之处

- **没有说明是否留出。** 论文在 Table 14 中把 WebArena 的 Forum、GitLab、Shopping 和 CMS 列为网页数据来源，而在线网页基准正是基于 WebArena。论文没有说明训练与评测的网站是否、如何分开。
- **所有表格都没有随机种子、标准差或置信区间。**
- **步数预算只部分对齐**：Table 5 标出了步数未知或超过 50 步的行。
- 第 5.2.3 节正文把 WindowsAgentArena 的对比（24.2 对 17.9）说成 15 步设置，而 Table 5 中这两个数在 50 步列；本文以表格为准。正文还称 UI-TARS-72B-DPO 是 50 步下最强的原生网页基线，但 Table 5 里 UI-TARS-1.5-7B 为 26.0，高于 21.4。
- 用作者自己的话说：“the quality of agent-collected data still lags behind expert crowdsourcing”，记忆机制“rudimentary”，并且没有加入“reflection, memory-based decision-making, or hierarchical planning”。错误分析显示，当屏幕没有变化时，模型会重复同一动作。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **71 分（★★★）**，证据等级 **transfer**。记录认可在五个在线基准上的评测、较强的基线、数据消融和已发布的代码，并将步数预算对齐和成本报告标为部分满足；留出环境和种子方差论文未报告。记录中没有反模式标记；判断中注明 AndroidWorld 偏向 planner-grounder 工作流，缩小但没有消除与面向移动端的原生模型之间的差距。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
