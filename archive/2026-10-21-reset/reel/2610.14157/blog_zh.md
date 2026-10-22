# OpenMobile-2：开放移动智能体全栈——商业应用复刻、11.6K 轨迹与 app-native 工具

*CUA Radar 对 arXiv 2610.14157v1（Yan、Zhang、Cheng、Sun、Pan、Ma 等；南京大学、商汤、港大、西安交大、新加坡国立大学、华东师大）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.14157v1 · 代码：https://github.com/OpenMobile2/OpenMobile2-Code*

## 问题

移动智能体靠交互经验吃饭，而这份经验大多闭门不出。论文开篇即指出，“high-quality interaction data remains largely proprietary, leaving the open community with limited training resources and open models trailing well behind”。现有两条造数据的路各撞一堵墙：在 Android emulator 上跑真实应用很真实，但”resist clean reset and is costly to parallelize”，大规模 rollout 与强化学习不现实；模拟应用（mock client）重置便宜、易并行，却只覆盖又窄又浅的商业场景。此外，应用开始在 GUI 之外暴露结构化接口，而此前没有任何移动环境允许智能体同时在这两种通道上训练。论文的定性一句话：“reproducing rich workflows and persistent user states at scale has remained a key obstacle”。

## OpenMobile-2 是什么

**智能体。** 一个纯视觉的移动 VLM 智能体：只看屏幕原始像素，没有 accessibility tree，也读不到业务状态。SFT 时上下文保留最近 3 张截图（更早的折叠为文字），RL 时最多保留 32 张（短边 448 px）。每个回合是一段 `Thought:` 加恰好一次工具调用：要么是始终可用的 `mobile_use`（click、long_press、swipe、type、answer、system_button、wait、terminate），坐标在归一化的 999 × 999 空间中预测；要么是一个 **app-native tool**——覆盖 50+ 应用的 300 多个受限函数（如 `taobao__search_items`、`clock__create_alarm`），仅当所属应用在前台时加入动作列表，并且与 GUI 操作同一份持久状态。平台：浏览器托管的 simulator、Android emulator，以及用于评测的真机。

**板上的模式。** CUA Radar 将本文归入模式 C22：“executable benchmark with resettable environments and privileged final-state checkers”（父模式：可执行 checker 中的 ground reward）。每个任务由用户目标、绑定的初始状态、以及对应用业务状态前后 diff 的程序化 checker 构成；checker 不看截图，也不用模型裁判。

**机制。** MobileGym++ 在 MobileGym 仿真框架上新增 35 个高保真商业应用复刻（simulator 共 63 个客户端，加上 62 个新配置的 emulator 应用，构成超过 110 个应用的训练场）。每个复刻从源应用的数据 schema 与交互图出发构建，交付前经过覆盖率检查与核心流程回放。新应用中位数为 37 条路由、166 个可交互动作、86 次页面跳转——相对原先 12 个 MobileGym 商业应用为 1.48× 的动作和 1.91× 的跳转。设备状态完全可序列化，重置确定、并行便宜；剪贴板、跨应用分享、支付跳转、媒体选择让信息跨应用流动。MobileGym++ Bench 提供 215 个长程任务（109 单应用、74 双应用、27 三应用、5 四应用），同一任务、同一 checker 下可分别用纯 GUI 或混合方式求解。

**训练信号。** OpenMobile-Data-v2 含 11.6K 条示教轨迹（其中 1,774 条混入工具调用）和 2K+ 条可执行 RL 任务（2,475 个目标），每条是”指令 + 初始状态 + verifier”三元组。指令与教师轨迹由 Gemini-3.1-Pro-Preview 生成，只有完成并通过运行时 verifier 的 rollout 才保留——simulator 用程序化校验，emulator 用 vision-language judge。训练在两个基座（Qwen3.5-9B、Qwen3.6-27B）上各跑两条 5-epoch SFT 分支（GUI-only 与 hybrid），再从 hybrid 检查点出发做 DAPO 式 RL（group size 8，150 步，512 个采样任务），奖励 r = v · m_tool · ℓ − 0.2 n_fmt − 0.2 f_succ：放宽版状态 verifier、2× 工具加成、长度因子，外加格式错误与”谎报完成”的惩罚。

## 论文报告的结果

以下全部是**在线**成功率——以最终设备/应用状态程序化判定；论文没有离线单步准确率数字。± 为评测种子间的标准差；∗ 表示该基线结果由 OpenMobile-2 作者复现。SFT 为 5 epochs，RL 为 512 个任务上再训 150 步。

| 方法 | AndroidWorld Pass@1 | MobileWorld GUI | MobileGym++ GUI | MobileGym++ Hybrid | SPA-Bench L3（真机） |
|----|----|----|----|----|----|
| UI-Venus-1.5-8B | 73.7 | – | 19.5\* | 16.3\* | 29.8\* |
| GUI-Owl-1.5-32B | 69.4 | 43.9 | 18.6\* | 23.3\* | – |
| Gemini-3.1-pro-preview | 70.7 | 58.1 | – | – | 70.2\* |
| Qwen3.5-9B（基座） | 54.3 ± 3.7\* | 12.8\* | 9.3\* | 12.1\* | 25.5\* |
| OpenMobile-2-9B（+RL） | 74.0 ± 2.9 | 38.5 | 40.5 | 46.5 | 48.9 |
| Qwen3.6-27B（基座） | 67.1 ± 4.1\* | 35.9\* | 46.5\* | 50.7\* | 31.9\* |
| OpenMobile-2-27B（+RL） | 79.9 ± 3.0 | 50.4 | 57.2 | 67.0 | 59.6 |

论文报告 9B 在 AndroidWorld 上较基座提升 19.7 个点（54.3 到 74.0），27B 提升 12.8 个点（67.1 到 79.9），并把真机迁移描述为”nearly doubling SPA-Bench performance from 31.9 to 59.6”。MobileGym 上 27B 从基座 37.1 到 +RL 的 51.2。闭源参照：MobileWorld GUI 上 GPT-5.6-Sol 为 70.1、Gemini-3.1-pro-preview 为 58.1；SPA-Bench L3 上 GPT-5.6-Sol 68.1*、Gemini 70.2*，仍高于这些开源模型。

## 论文自带的对照实验

- **重叠审计。** 用 text-embedding-3-large 嵌入后，与 AndroidWorld、MobileWorld、MobileGym、MobileGym++ Bench 相似度超过 0.7 的 SFT 指令分别只有 1.11%、0.39%、0.46%、2.25%，无一超过 0.9；2,475 个 RL 目标中 6.1% 与 MobileGym++ Bench 超过 0.7。
- **覆盖度消融。** 固定骨干、优化器与 2K 轨迹预算，把应用覆盖从 15 提到 53，AndroidWorld 留出应用 Pass@1 从 60.7 升到 67.5，而 InD Pass@1 基本稳定（73.7 到 71.4）。
- **工具需要混合训练。** hybrid SFT 之前，工具调用只出现在 215 个任务中的 20–102 个，Qwen 模型仅提升 2.8–4.2 个点；之后工具出现在 113 与 128 个任务（110 与 115 个不同工具），提升升到 5.6 与 10.3 个点，轨迹缩短 4.8 与 5.8 步。在工具从未见过的 MobileWorld MCP 上，hybrid SFT 对 GUI-only SFT 为 27.5 对 12.5（9B）、45.0 对 35.0（27B）。
- **RL 的边界。** RL 把 MobileGym 成功率从 35.9 提到 38.3（9B）、48.4 提到 51.2（27B），把 27B 的 SPA-Bench 从 57.4 提到 59.6。论文直言：“Gains on other benchmarks remain limited, suggesting that RL benefits depend on the alignment between training environments and evaluation scenarios.”

## 论文自己承认的薄弱处

- emulator 侧的 SFT 轨迹靠 “a vision-language judge” 过滤，论文并未验证该裁判的准确率；“不用模型裁判”的 checker 设计只覆盖 simulator 一侧。
- 留出评测是部分的：覆盖度研究在 AndroidWorld 上固定了 15 个 InD 应用（InD 74 个任务 vs 留出 42 个），主基准的一部分应用与训练应用池重叠。
- RL 阶段在 MobileGym++ 任务上训练与验证（2K+ 池中的 512 个），其测得的增益也主要落在该环境。
- 模拟应用以保真度换 “cheap parallelism, clean reset, and direct state checks”——这是论文对 mock client 一族的描述——simulator 分数衡量的是”商业风格”而非真实商业应用。

## CUA Radar 的判断

CUA Radar 给本文打 **62 分（★★）**，证据等级 **transfer**。判定记录肯定了五个套件上的在线评测、评测种子间的标准差、较强的开源与闭源基线、覆盖度消融、训练/评测重叠审计以及代码开放；同时标记了两个反模式（AP2、AP5）、留出应用状态为 partial、emulator 数据上的 VLM judge 未经验证、RL 比较的预算匹配不明确。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
