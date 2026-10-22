# ScaleCUA：先合成可验证的 GUI 任务，再用在线 RL 训练 9B 桌面智能体

*CUA Radar 对 arXiv 2607.11185v1（Lv、Liu、Ren、Lai、Jing、Zhang、Zhao、Yao、Tang、Dong）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2607.11185v1 · 代码：https://github.com/THUDM/SCALE-CUA*

## 问题：没有打分器、浪费 rollout、多轮训练太慢

论文从面向计算机使用智能体（CUA）的在线可验证奖励强化学习（RLVR）出发，认为它被两件事卡住。第一是数据。“可验证的 GUI 任务”是指配有确定性 judge 函数（文件系统检查、浏览器状态检查或一段 Python 代码）的任务，judge 在没有人或 LLM 参与的情况下对最终环境状态打分。与数学或代码不同，GUI 任务天然只有一个在线环境和一条初始指令，judge 需要自己构造。任务难度还要合适：在 GRPO 式训练下，模型总是做对或总是做错的任务，组内优势为零，整组 rollout 都被浪费。

第二是训练效率。均匀采样任务常常产生没有学习信号的批次。多轮 GUI 训练里还要权衡轨迹怎么打包：整条轨迹作为一个训练项会累积所有截图并拖慢 rollout 引擎；每一轮切一个训练项（step-wise）则会让训练项数量随轮数线性增长。

## ScaleCUA 是什么

智能体只看截图；附录明确说明感知阶段不使用 accessibility tree 或特权环境状态。动作走各基准暴露的计算机动作接口：鼠标动作（click、drag、move）以相对 1000×1000 网格上的 (x, y) 为参数，再由环境缩放到 1280×800 屏幕；键盘动作（key、hold_key、type）、scroll，以及 wait 等辅助动作。ScienceBoard 另外提供 done、answer、write_file。平台是 docker 容器里的 Ubuntu 桌面（OSWorld 与 ScienceBoard）。论文把这套方法用在三个基座模型上：GLM-4.6V-Flash、Qwen3-VL-8B-Thinking 和 Qwen3.5-9B。在 CUA Radar 板上它的架构模式是 K13：“从 checker 出发合成任务，使可验证奖励天然存在”。

整体流程分三步：先在 VeriGen 生成的初始任务池上训练；再收集模型的 rollout，让 VeriGen 把它们转成精炼后的 RL 任务池；最后在该任务池上用下面两个组件做在线 RL。

1.  **VeriGen（任务与 judge 合成）。** 三个 LLM 智能体与在线 docker 容器交互。proposer 根据环境知识文档写出任务及其 verifier；judger 做静态语义审查（指令是否无歧义、verifier 逻辑是否成立）；checker 在容器里做一次 dry run，检查目标是否可达、verifier 能否正确给最终状态打分。一个共享的 docker 交互 probe 让 100+ 个智能体 worker 同时对 100+ 个容器工作。在“轨迹引导”模式下，VeriGen 读取训练后模型的 rollout 与各任务通过率：对失败任务，找到模型最早偏离目标的一步，把任务拆成更简单的子任务；对成功任务，把同一应用内相似的任务聚类，串成更难的多目标任务。结果是 24K+ 个可验证任务和近 3K 个高质量 RL 任务。
2.  **Frontier Sampling（前沿采样）。** 每个任务维护成功率的指数滑动平均（alpha = 0.2）。以目标成功率（mu = 0.5，sigma = 0.25）为峰值的高斯权重，把 rollout 分配给接近模型当前能力前沿的任务；每个批次的 20% 从该池之外均匀采样以保持探索。
3.  **Visual Context Segmentation（视觉上下文分段）。** 滑动窗口只保留最近 K 张截图（OSWorld 用 K = 5，ScienceBoard 用 8）。窗口溢出时，把当前 token-ID 流存为一个训练项，丢掉最旧的截图，并把剩余历史以零 loss mask 重新 tokenize，这样之前的助手回复只作为上下文。训练项数量是 O(nT/K)，而 step-wise 是 O(nT)。

训练信号是 Python judge 对最终状态给出的奖励（全有或全无的任务为二值，有子目标时为稠密），用 GRPO、DAPO 式非对称裁剪和 KL 惩罚优化。每个 episode 最多 50 轮；未完成的 episode 会得到 -0.2 的奖励惩罚。

## 论文报告的结果

以下全部是在线评测（OSWorld 与 ScienceBoard 成功率，%），OSWorld 最多 50 步。ScaleCUA 的数字是每个任务 4 次独立 rollout 的均值；论文给出三个模型的标准差，OSWorld 为 0.5 到 1.2，ScienceBoard 为 0.5 到 2.8。没有分项成绩的行取自各自的技术报告。

| 模型                                | OSWorld  | ScienceBoard |
|-------------------------------------|----------|--------------|
| Kimi K2.5（OSWorld 上最强开源基线） | 63.3     | 未报告       |
| Claude Sonnet 4.5（闭源）           | 62.9     | 未报告       |
| Claude Opus 4.6（闭源）             | 72.7     | 52.7         |
| Qwen3.5-9B（基座，技术报告）        | 41.8     | 未报告       |
| ScaleCUA-GLM-4.6V-Flash             | 66.5     | 49.4         |
| ScaleCUA-Qwen3-VL-8B                | 67.7     | 51.9         |
| **ScaleCUA-Qwen3.5-9B**             | **68.7** | **54.0**     |

论文称 Qwen3.5-9B 版本在 OSWorld 上超过 Kimi K2.5（63.3）、Claude Sonnet 4.5（62.9）和 Seed-1.8（61.9），在 ScienceBoard 上超过 Claude Opus 4.6（52.7）；在 OSWorld 上，GPT-5.4（75.0）和 Claude Opus 4.6（72.7）排在它之上，人类成绩为 72.4。三个模型都比各自基座有提升，论文举的例子是 Qwen3.5-9B：41.8 到 68.7（论文中写作 +26.9）。论文没有离线的 grounding 或单步准确率数字。

## 论文自带的对照实验

**组件消融（OSWorld，Qwen3.5-9B）。** 完整 ScaleCUA 为 68.7。去掉 Frontier Sampling 为 63.7，去掉 Visual Context Segmentation 为 62.2，去掉 VeriGen 则降到 43.9，论文把它标为基座分数。

**采样器基线。** Frontier Sampling 与均匀采样、DAPO 和课程学习做了比较，但只以训练奖励曲线呈现（图 6a），论文没有给出这组比较的数值表。

**窗口大小。** OSWorld 上 pass@1 在 K = 5 时达到峰值 58.9，K = 1 为 56.4，K = 15 为 56.8。在一个多应用任务的案例分析中（每种设置 8 次 rollout），K = 5 通过 7/8，K = 3 通过 5/8，K = 1、8、15 都是 0/8。

**训练速度。** 在 Qwen3.5-9B、batch size 32、rollout-n = 8、其他超参与算力预算固定的条件下，K = 5 把单步时间从 750 s 降到 265 s（2.83×），其中 actor 阶段从 485 s 到 154 s，reference-policy 阶段从 241 s 到 88 s。这是训练耗时测量，不是评测成绩。

**Judge 质量。** 完整的多智能体循环让生成的 judge 可执行率达到 94.5%；去掉 LLM Judge Agent 为 62.3，去掉 Fix Agent 为 78.1，去掉 Rule Validator 为 86.2。专家对 160 条轨迹（每个应用领域 10 条）的审核显示，可执行 judge 与人类标签一致的比例为 82.5%：OSWorld 78.0%，ScienceBoard 90.0%，共有 11 个假阳性和 17 个假阴性。

**轨迹引导任务的价值。** 把它们加入 RL 任务池后，OSWorld 成绩从 64.6 升到 68.7。

**与评测任务的重叠。** 附录把训练子集与基准任务池做了比对：没有完全相同的指令，目标近重复在 OSWorld 占 0.19%、在 ScienceBoard 占 0.36%，judge 的完全复用在 OSWorld 为 2.10%（通用评估器模板），ScienceBoard 为 0.00%。

**成本。** 合成平均端到端 221.7 秒，每个被接受的任务 0.93 到 1.01 美元。主要的 RL 实验使用 8 个节点，每个节点 8 张 H800。

## 证据较薄之处

- 训练任务是在与评测相同的 OSWorld 与 ScienceBoard 环境里合成的：“生成的任务覆盖全部 10 个 OSWorld 应用领域和全部 6 个 ScienceBoard 科学领域”。重叠审计是论文给出的回应，但这些应用本身并没有被留出。
- 基座分数在消融表里是 43.9，在主 OSWorld 表里 Qwen3.5-9B 是 41.8（标注为取自技术报告）。论文没有解释这两个数字的差别。
- 82.5% 的 judge 与人类一致率意味着仍有一部分 judge 决策与专家不同；表 6 中人类判定为成功的比例总体为 73.1%，ScienceBoard 为 58.3%。
- 采样器比较没有数值表。消融每行只有一个 OSWorld 分数，没有标准差。
- 作者列出三条局限：50 轮上限、仅限 Ubuntu 桌面（Windows 与 macOS 留待未来）、只在 8B 到 9B 模型上验证。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **76 分（★★★）**，证据等级 **online**。分数反映论文所报告的证据：两个基准上的在线评测、4 次 rollout 的标准差、采样器基线、成本报告、组件消融、对 judge 的专家审核，以及已发布的代码。判定记录把留出环境和预算对齐标为“部分”，并标出生成任务覆盖的领域与基准相同。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
