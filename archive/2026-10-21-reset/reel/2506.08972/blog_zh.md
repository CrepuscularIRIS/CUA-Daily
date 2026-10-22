# UI-NEXUS 与 AGENT-NEXUS：用 GPT-4o 调度器把移动智能体从原子任务带向组合任务

*CUA Radar 对 arXiv 2506.08972v1（Guo、Miao、Wu、Cheng、Zhou、Zhang；上海交通大学与澜舟科技）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2506.08972v1 · 项目主页：https://ui-nexus.github.io*

## 问题：原子任务刷分很好，真实指令一到就卡住

多数移动智能体（mobile agent）研究评测的是原子任务：短链执行（“查一下评分最高的咖啡机”）或单屏 grounding（“点击提交按钮”）。真实用户指令是组合式的。论文按子任务依赖结构定义了三类组合：**Simple Concatenation**（独立子任务顺序拼接）、**Context Transition**（后续子任务依赖前序子任务的输出状态）、**Deep Dive**（子任务之间需要聚合、摘要等中间推理）。在这类任务上，作者观察到典型失败模式：over-execution（任务已完成仍在操作，或中间信息没拿到就编造内容继续）、under-execution（子任务做一半就切换走）、context confusion（在 App A 上却去满足 App B 的要求）、attention drift（漏掉部分要求甚至整个子任务）。

## 论文交付了什么：一个基准 + 一套调度系统

**UI-NEXUS** 是一个交互式 Android 基准：100 个任务模板，覆盖 50 个 App——20 个本地工具 App 加 30 个在线服务 App，中英双语——人工标注的最优平均步数为 14.05，构建在模块化基础设施上（agent 配置、设备管理、轨迹评测）。可控子集 **UI-NEXUS-ANCHOR** 覆盖 50 个本地工具 App 任务，在 Android 模拟器（Pixel 6，API level 33，AndroidWorld 系统镜像）中运行，采用 AndroidWorld 式的自动奖励信号判定成败。在线服务 App 在真机上运行，用 MLLM-as-a-Judge 加人工核验判定。步数预算约为人工标注最优步数的两倍，所有智能体相同。指标分性能（成功率；终止原因：successful、premature、budget exceeded、deemed impossible、collapse）与效率（每步美元成本、每步秒数）。

**AGENT-NEXUS** 是论文提出的调度系统，在 CUA Radar 板上属于模式 C17：manager 规划子目标、worker 执行。GPT-4o **orchestrator** 把组合指令分解为一系列自包含的原子子任务，每个子任务带类型 `act`（UI 操作）、`think`（不改动环境的推理）或 `tool`（预定义操作；本文实现中唯一的 tool 是 HOME）。**执行模块**含三个角色：Analyst（GPT-4o，界面分析与静态推理）、Navigator（任意现成移动智能体，即插即用；论文试了 M3A 和 UI-TARS-7B-SFT）以及 Tool。每个子任务执行完毕后，其 **return signal**（完成状态、抽取出的信息、执行日志）写入 **process memory**，orchestrator 随即重算计划：π<sub>t+1</sub> = M(s<sub>t+1</sub>, g, P<sub>t+1</sub>)。设计哲学是 context reduction：每个全局步只给执行器一条自包含指令。系统不做任何训练——驱动它的信号就是每个子任务的 return signal。

## 论文报告的结果

基线智能体：三个基于 GPT-4o 的 agentic workflow（M3A、Mobile-Agent-v2、Mobile-Agent-E），两个基于 Qwen2-VL-7B 的 agent-as-a-model（OS-Atlas-7B-Pro、UI-TARS-7B-SFT，用 vLLM 部署在 1 块 A100-SXM4-80GB 上）。backbone 温度设为 0.0，输入上限 4096 token；UI-TARS 保留 N = 5 张历史截图。

离线，ANCHOR 50 个任务（成功率 %，括号内为 budget exceeded %）：

| 智能体                            | 成功率   | Budget exceeded |
|-----------------------------------|----------|-----------------|
| M3A                               | 50.0     | 16.0            |
| Mobile-Agent-v2                   | 30.0     | 34.0            |
| Mobile-Agent-E                    | 26.0     | 8.0             |
| OS-Atlas-7B-Pro                   | 2.0      | 72.0            |
| UI-TARS-7B-SFT                    | 6.0      | 84.0            |
| **AGENT-NEXUS w/ M3A**            | **74.0** | 10.0            |
| **AGENT-NEXUS w/ UI-TARS-7B-SFT** | **46.0** | 44.0            |

摘要将其概括为：在 UI-NEXUS 组合任务上为现有移动智能体带来 24% 到 40% 的任务成功率提升，且不显著牺牲推理开销。效率（Table 3）：AGENT-NEXUS w/ M3A 每步 0.040 美元、18.86 秒，对比 M3A 单独使用为 0.037 美元、14.77 秒；AGENT-NEXUS w/ UI-TARS-7B-SFT 每步 0.0063 美元、6.53 秒，对比 UI-TARS 单独使用为 0.0025 美元、4.35 秒。

在线，30 个服务 App（成功率 %，Table 4）：英文 App——M3A 32.0、Mobile-Agent-E 28.0、AGENT-NEXUS w/ UI-TARS-7B-SFT 28.0、Mobile-Agent-v2 12.0、UI-TARS-7B-SFT 8.0、OS-Atlas-7B-Pro 4.0；中文 App——AGENT-NEXUS w/ UI-TARS-7B-SFT 32.0、Mobile-Agent-E 24.0、Mobile-Agent-v2 12.0、UI-TARS-7B-SFT 8.0、M3A 4.0、OS-Atlas-7B-Pro 4.0。值得注意的是英文在线 App 上，包装 UI-TARS 的配置（28.0）低于 M3A（32.0）：调度器在那里提升的是 7B 执行器，而不是超过 GPT-4o workflow。没有任何智能体在所有子集上成功率超过 50%。

## 论文自带的对照实验

核心对照是**原子-组合泛化差距分析**（Table 5）：在 ANCHOR 的 Simple Concatenation 与 Context Transition 指令上，每个智能体分别以完整组合指令（“弱”）和人工最优分解的原子子任务（“强上限”）运行。人工分解带来大幅提升：M3A 总体从 57.0 到 80.0（↑87%），UI-TARS-7B-SFT 从 11.0 到 60.0（↑452%）；Mobile-Agent-v2 从 34.0 到 46.0（↑33%），Mobile-Agent-E 从 31.0 到 46.0（↑45%），OS-Atlas-7B-Pro 从 3.0 到 6.0（↑100%）。按 Weak-to-Strong 式的 Performance Gap Recovered（PGR）度量，AGENT-NEXUS w/ M3A 总体 77.0、PGR 88.0，AGENT-NEXUS w/ UI-TARS-7B-SFT 总体 49.0、PGR 76.0——不需要人工分解器，调度器就拿到了人工分解收益的大部分。基线对齐程度尚可：三个 workflow 基线同用 GPT-4o backbone，所有智能体面对同样的步数预算和同样的 App 启动约定，两个模型型智能体的成本与延迟也被量化。

## 论文自己承认的薄弱处

- 未报告随机种子与方差；各表读起来是每个智能体在每个子集上各跑一遍。
- 在线判定器是标准做法但未经验证：论文只说 “we follow previous work to apply MLLM-as-a-Judge and human verification for accurate verification”，没有对 judge 本身的检验。
- 在线界面会漂移：“experimental environments on applications such as RedNo and YouTube may slightly differ across time.”
- 仅限 Android：“our experiments are conducted solely on Android devices.”
- 执行模块是简化实现：“the only tool in HOME.”
- 任务模板由 GPT-4o 与 GPT-o1 扩写、人工修订；探索/数据合成所用 App 与评测 App 之间的留出划分未报告（held-out 不明确）。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **online**，架构模式 **C17**（agent-loop context control 下的 manager-worker 层级）。分数反映论文所报告的证据：交互式在线评测、五个主流基线、成本与延迟核算、带 PGR 的原子-组合对照实验，以及附演示、数据集和代码的项目主页。判定记录同时标出缺失项：无种子/方差、held-out 环境不明确、judge 未检验、预算对齐仅为部分（调度器在 navigator 之上叠加 GPT-4o 调用）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
