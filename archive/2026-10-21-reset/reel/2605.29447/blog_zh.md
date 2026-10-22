# RoTS：生长轨迹树，让 GUI 智能体学会从自己的错误中恢复

*CUA Radar 对 arXiv 2605.29447v1（Bu、Liu、Chen、Jiang、Li、Duan、Jiang、Hu、Yang、Zhang；阿里云计算）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2605.29447v1 · 代码：https://github.com/AlibabaResearch/RoTS*

## 问题：智能体会被自己的错误绊倒

GUI 智能体经常犯论文所说的 policy-induced errors（策略自身引发的错误）：由智能体自己的动作造成的失误，例如 grounding 错误、误读屏幕状态、子目标选错。之后智能体陷在错误状态里，最终失败。作者认为，无论评测还是训练，对这类错误的鲁棒性都没有得到足够重视，并指出两个缺口。其一是错误覆盖（error coverage）：现有基准和训练数据偏重低层、人工整理的错误，而真实失败往往是组合式、高层的。其二是错误视野（error horizon）：现有评测协议和反思数据大多是短视野（例如一次无效点击），而许多真实错误要过几步才能被识别，需要长视野的回溯与恢复。现有智能体框架通常是外加反思或回溯子智能体，而不是在训练层面让模型自己学会检测和恢复。

论文给出两项贡献：基准 GUI-RobustEval，以及数据合成流水线 RoTS（Robustness-driven Trajectory Synthesis）。

## RoTS 是什么

**智能体。** 智能体是一个视觉语言模型，输入截图（加上历史，最多保留 5 张图像），输出 Thought 加一个 PyAutoGUI 动作，使用 AgentNet 的动作空间。环境是云上托管的真实 Ubuntu 和 Windows 系统。训练出两个模型 RoTS-7B 和 RoTS-32B，分别由 Qwen2.5-VL-7B 和 Qwen2.5-VL-32B 做监督微调（SFT）得到。在 CUA Radar 板上的架构模式是 K26（trajectory-level policy training）。

**基准。** GUI-RobustEval 包含 1,216 个可执行测试用例，覆盖 11 种错误类型和四个错误深度（d = 0、1、3、5）。素材来自 12 个智能体在 OSWorld 上的 1.5k 条失败轨迹。专家定位根因步骤、标注错误类型，并修正更早的无关错误，使前缀保持干净。测试时，环境被重置到根因动作之后再走 d 步的状态，然后由智能体接手。报告两个指标：Error-Awareness Rate（接手时是否识别出错误，由 VLM 判定）和 Post-Error Success Rate（能否恢复并完成任务）。

**合成。** 对 20k 个在线任务，流水线为每个任务和每个策略构建可回放的轨迹树。先做 N = 4 次并行 rollout，再进行 32 轮 explore-recovery co-expansion，每个任务每个策略得到 68 条轨迹。奖励模型（WebJudge 风格）把树分成成功部分和失败部分，两边都扩展：

- **Fragility-driven exploration（FDE，脆弱点驱动探索）。** progress critic 估计策略在成功部分每个节点上提出正确动作的概率；UCB 规则选出最脆弱的节点，环境回放前缀后由策略继续，用来发现新的失败模式。
- **Experience-informed recovery（EIR，经验引导恢复）。** 对失败轨迹，reflector 读取从兄弟分支提取的经验，标出候选错误状态并写出恢复建议。UCB 规则选定一个错误状态，环境回放到该处，recovery actor 在建议的约束下继续执行。

合成用的策略是 OpenCUA-7B、UI-TARS-1.5-7B 和 Qwen3-VL-Plus；Qwen3-VL-Plus 同时充当 reflector 和 recovery actor。

**训练信号。** 整条轨迹噪声较大，因此后处理只保留正确的步骤：VLM 过滤掉状态转移不一致的轨迹，progress critic 和 action critic 剔除错误步骤，再由反思验证器把剩余数据分成 reflection-agnostic 和 reflection-related 两个子集，最后做 MinHash 去重。训练是对 assistant token 的 teacher-forced SFT。最终混合数据为 800k 条样本，其中 720k 为 reflection-agnostic、80k 为 reflection-related（反思占比 0.1）。没有强化学习阶段。

## 论文报告的结果

以下结果全部是在线评测：真实操作系统环境，没有离线步骤准确率。OSWorld-Verified 有 369 个 Ubuntu 任务。模型在最大 15 步和 50 步下测试，取 4 次运行均值；All-Pass@4 指四次运行全部成功的任务比例。† 表示作者自行复现的结果。

| OSWorld 成功率（%）   | 最大 15 步 | 最大 ≥ 50 步 | All-Pass@4（50 步） |
|-----------------------|------------|--------------|---------------------|
| OpenCUA-32B           | 29.7       | 34.1         | 15.5                |
| Qwen3-VL-32B-Thinking | 28.1†      | 41.0         | 21.1                |
| Qwen3-VL-Plus（API）  | 33.1†      | 35.2†        | 24.5                |
| RoTS-7B               | 31.7†      | 36.3†        | 26.3                |
| **RoTS-32B**          | **42.8†**  | **47.4†**    | **33.8**            |

同一张表还列出了闭源的 Claude 4.5 Sonnet（最大 ≥ 50 步为 58.1），所以摘要里的 “state-of-the-art” 应理解为开放权重模型之间的比较。其他行：Qwen2.5-VL-32B 为 3.0 和 3.9，UI-TARS-72B-DPO 为 24.0 和 25.8，Qwen3-VL-8B-Thinking 为 29.2† 和 33.9，GUI-OWL-7B 为 27.1 和 29.4。论文指出，对 RoTS-7B，把步数预算从 15 提高到 50 可再增加 4.6%。

在 WindowsAgentArena（154 个 Windows 11 任务，最大 50 步）上，RoTS-7B 为 28.2†，RoTS-32B 为 39.1†；表中 Jedi-7B w/ GPT4-o 为 32.9，ScaleCUA-32B 为 24.2，UI-TARS-72B-DPO 为 17.9。

在 GUI-RobustEval 上（3 次运行，最多 50 步），RoTS-32B 在深度 0、1、3、5 的 post-error success 分别为 49.7、41.8、36.5、33.2，error awareness 为 58.8%；RoTS-7B 分别为 43.5、36.6、30.1、26.7，awareness 为 51.9%。OpenCUA-32B 为 45.5、37.2、28.6、25.9，awareness 50.3%；Qwen3-VL-Plus 为 55.1、46.1、36.9、33.5，awareness 65.4%。论文指出，在开源模型中 RoTS 从深度 0 到深度 5 的下降最小（7B 为 38%，32B 为 33%）。

## 论文自带的对照实验说明了什么

**等预算的 rollout 策略。** 在 5k 个在线任务上，用 100k 条样本对 Qwen2.5-VL-7B 做 SFT，各变体使用相近的 rollout 预算。OSWorld 成功率和 All-Pass@4 分别为：仅并行采样 18.1 和 8.6；加 FDE 为 19.6 和 9.1；加 EIR 为 19.5 和 12.1；两者都用为 21.4 和 14.1。论文的解读是：FDE 主要提升成功率，EIR 主要提升鲁棒性。

**等规模的数据质量。** 在 100k 条样本下，人类演示数据 AgentNet（仅 reflection-agnostic）在 OSWorld 上得到 15.3 成功率和 7.8 All-Pass@4；加入人类反思样本为 16.1 和 8.4；换成 RoTS 的反思数据为 18.8 和 11.6；完全使用 RoTS 数据为 21.4 和 14.1。

**反思比例、恢复深度与规模。** 最佳反思占比为 0.1（21.4 和 14.1）；提高到 0.3 时性能降到无反思设置之下，作者归因于过多的反思数据造成无效反思。限制反思数据的恢复深度时，最大增益来自中等深度（≤ 5），GUI-RobustEval 上 post-error success 从 12.1 升到 20.7；深度 7 以上的增益很小。数据量从 50k 扩到 1000k 后在 36.4 的成功率处趋于饱和，作者认为这是当前扩展设置（N = 4，32 轮）所限。

**评判模型。** 奖励模型 WebJudge 与人工的一致率报告为 90%，对照的 ZeroGUI 式投票评判为 76.60%；progress critic 和 action critic 在 200 个抽样步骤上分别为 88.7% 和 90.6%；error-awareness 评判在 200 个样本上各智能体均不低于 96%。

**留出任务。** 20k 个合成任务在任务和资产层面与所有评测基准不相交，只共享基础操作系统快照。

**成本。** 基准构建约 400 美元；20k 个任务的数据合成约 48,100 美元，墙钟时间约 16 天。

## 证据偏薄的地方

- 论文报告的是 3 次或 4 次运行的均值，主表没有标准差或置信区间。
- 带 † 的行是作者自行复现的运行；表中没有这样标注其余行，因此各行的评测设置可能不同。
- 流水线依赖 Qwen 系列模型：Qwen3-VL-Plus 同时是策略、reflector、recovery actor、critic 和 CoT 生成器。所有作者均来自阿里云，论文声明 Qwen-VL 系列和 RoTS 均由其开发。
- 失败案例包括 “over-reflection”：在一个 OSWorld 例子中，智能体把未完全渲染的页面当成错误页面，连续两次不必要地返回。分错误类型的结果显示，RoTS-32B 在 Fail to Terminate（17.4%）和 Misunderstand Task Objective（24.1%）上仍有瓶颈。
- 扩展在当前扩展设置下趋于饱和。

## CUA Radar 的评估

CUA Radar 给这篇论文打分 **69（★★）**，证据等级 **online**。该分数反映论文所报告的内容：三个基准上的在线评测、任务级留出的合成数据、rollout 策略消融中匹配的 rollout 预算、成本报告、组件消融、对 LLM-as-judge 组件的人工一致性检验，以及开源代码。论文没有报告多次运行之间的方差，判断记录也没有标记反模式。CUA Radar 没有复现任何实验，文中所有数字均来自论文（版本 v1）。
