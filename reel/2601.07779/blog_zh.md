# OS-Symphony：会保留里程碑截图、会视觉化搜索教程的计算机使用智能体编排框架

*CUA Radar 对 arXiv 2601.07779v1（Yang、Jin、Wu、Liu、Sun 等）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2601.07779v1 · 代码：https://github.com/OS-Copilot/OS-Symphony*

## 问题

基于 Vision-Language Model 的计算机使用智能体（CUA）在两类场景下退化。其一是长程任务：虽然有记忆模块，但论文认为它们”缺乏对历史视觉信息的细粒度管理与剪裁”，截图要么冗余保留、要么被丢弃，intent drift 和循环行为难以察觉。其二是陌生软件：检索增强（RAG）方案要么只处理文本、丢失截图密集教程中的视觉语义，要么依赖”维护成本高、难以适应新软件”的本地知识库。OS-Symphony 用里程碑记忆和一个视觉参与的浏览器搜索器同时回应这两点。

## OS-Symphony 是什么

这是一个桌面 CUA。感知为截图（上下文最多 8 张 1920x1080 图像），动作是一个精简的跨平台动作空间，映射到 PyAutoGUI 原语：click、type、scroll、drag_and_drop、hotkey、open、wait、done、fail，加上两个专有调用 call_search_agent 和 call_code_agent。平台覆盖 Ubuntu（OSWorld）、Windows（WindowsAgentArena）和 macOS（MacOSArena）。它在 CUA Radar 板上的架构模式是 C18：“用动作前后的观察核验每个动作的结果并把结论反馈回去”，隶属主模式 agent_loop_context_control（结构化 prompted agent loop）。

在 temperature 0.1 下，同一个 VLM（GPT-5、GPT-5-Mini 或 Qwen3-VL 8B/32B 的 Instruct/Thinking 变体）驱动四个角色：

1.  **Orchestrator（编排器）。** 决策核心：读指令、当前截图、最近 K 轮短期记忆、最新 reflection 和已检索的 tutorial，每步输出一个 thought 和一个 action。
2.  **Reflection-Memory Agent（RMA）。** 辅助 VLM 用动作前后截图总结刚完成的动作并判断是否成功；长期记忆只保留里程碑截图和抽象摘要；reflection 走结构化协议：On-track、Completed、Infeasible，或 Off-track 并标注四类错误之一（GUI Error、Lack of Tutorial、Code Error、Other Error）。规则式循环检测（先 perceptual hashing，Hamming 距离 ≤ 1，再 SSIM 0.99，窗口为 3）提供 Lack-of-Tutorial 的提示。
3.  **Multimodal Searcher。** 按需在隔离的浏览器沙箱里从搜索结果页开始浏览，动作空间只有 click、type、scroll，交叉核对多个页面后蒸馏出分步 tutorial，否则返回 fail。单模态消融用 SearXNG 搜索加 Crawl4AI 解析替代。
4.  **Coder 与 Grounders。** Coder 用 shell/Python 改文件，并通过 GUI 状态检查验证；定位用 UI-TARS-1.5-7B 做通用 grounder，另配基于 EasyOCR 的词级 OCR grounder 处理文本密集应用。

框架不含训练：全部是 prompted 的，转向信号来自辅助 VLM 的逐步判定、规则式循环检测和搜索器带回的 tutorial。

## 论文报告的结果

以下均为在线、执行判定的桌面基准成功率（%）。论文没有报告离线的单步或 grounding 准确率数字；主表也没有给出种子数或方差，CUA Radar 的一句话摘要记录为单次运行。OSWorld 指 OSWorld-Verified，去掉 8 个 Google Drive 任务后共 361 个任务。

| 方法（步数上限） | OSWorld | WindowsAgentArena（154） | MacOSArena（63） |
|----|----|----|----|
| Qwen3-VL-32B-Instruct（50） | 32.40 | 31.7 | 7.94 |
| UI-TARS-2（100） | 53.10 | 50.6 | 未报告 |
| Agent S3 w/ GPT-5（100） | 62.63 | 56.6 | 未报告 |
| Agent S3 w/ GPT-5-Mini（50，作者复现） | 47.58 | 未报告 | 未报告 |
| OS-Symphony w/ Qwen3-VL-32B-Instruct（50） | 46.86 | 45.3 | 19.05 |
| OS-Symphony w/ GPT-5-Mini（50） | 58.05 | 62.2 | 46.03 |
| OS-Symphony w/ GPT-5（50 / 100） | 63.61 / 65.84 | 63.5 | 未跑（成本原因） |

论文给出的相对提升为：OSWorld 65.8%（↑2.4%）、WindowsAgentArena 63.5%（↑6.9%）、MacOSArena 46.0%（↑38.0%），并称 OSWorld 上 GPT-5 的 100 步成绩超过主要基线（100 步 Agent S3 w/ GPT-5）约 3%。WindowsAgentArena 上，超过 50 步和 100 步 Agent S3 基线 9.4% 和 6.9%，GPT-5-Mini 版本超过 100 步 Agent S3（GPT-5）5.6%。对作者自行复现的 Agent S3，框架在 Qwen3-VL-32B-Instruct 上带来 8% 提升，GPT-5-Mini 上为 10%。

## 论文自带的对照实验

**消融（OSWorld，GPT-5-Mini + UI-TARS-1.5-7B，50 步）。** 同时去掉搜索和反思后平均 51.90；加单模态搜索 54.81；多模态搜索 58.05，在 Daily 域相对无搜索提升 22.1%、相对单模态提升 10.3%。反思方面：无反思 54.38，短期记忆式反思 54.01，完整 RMA 58.05——在 Workflow 域分别相对提升约 20.0% 和 20.7%。值得注意的是，朴素的 last-K 反思低于完全不做反思，且后者 token 还少约 36.5%。去掉 RMA 每任务多花 3.3 步。去掉 Coder，OSWorld 从 63.61 降到 57.42（约 6.2%）。

**成本与规模。** Workflow 域上，Claude-Sonnet-4.5 得 57.21、约 \$500；GPT-5 得 54.86、约 \$150；GPT-5-Mini 得 47.37、约 \$30，论文称 GPT-5-Mini”平均只落后 GPT-5 5%，成本降低约 80%“。换 grounder 对平均值影响很小（UI-TARS-1.5-7B 46.86、GTA1-32B 46.32、ScaleCUA-32B 45.76、Holo2-30B-A3B 43.92）。历史图像上限 8 张是报告的最优值（46.86）。

**反思审计。** 在 RMA 判为 GUI Error 的 100 步中，人工核查发现约 90 步确有错误、约 10 步为幻觉。消息协议统计中 75.0% 的步被判为正常；Searcher 仅被调用 35 次（占动作的 0.6%），人工核查发现其中 85% 的教程有用。

**测试时扩展。** 每次采样把 temperature 提高 0.1，Pass@2 达到 74.14%，超过人类基线 72.4%，Pass@5 达到 79.40%。

## 论文自己承认的薄弱处

- **波动性。**”尽管对 prompt 和 temperature 有严格控制，我们仍观察到显著的任务级波动。“主表没有种子数或置信区间。
- **感知盲区。** 当前 VLM”常常无法分辨高亮、窗口重叠等细粒度线索。这种感知盲区导致 RMA 发出假阳性错误，在视觉复杂的域里，去掉 RMA 的基线反而超过完整框架。”
- **没有留出集。** 三个基准都是标准公开套件；论文没有声称任何留出划分。
- **开销。** 多智能体系统很重：RMA 和 Orchestrator 平均每任务约 270k token（96% 为 prompt，4% 为 completion），“我们的执行速度比人类慢几十倍”。
- **仅限桌面。**”该框架对 Android、iOS 等移动平台的适应性尚未验证。”

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **online**。分数反映论文所报告的证据：三个桌面基准上执行判定的在线评测、同模型复现的 Agent S3 基线、美元成本、以及带步数与 token 记账的组件消融。判定记录同时标出缺失项：没有留出环境、种子/方差未报告（单次运行）、RMA 的判定除 100 步人工审计外未对真值验证、评审时代码链接未核实。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
