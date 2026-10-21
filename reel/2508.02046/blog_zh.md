# NaviMaster：用一个 GRPO 策略同时做 GUI 与具身导航

*CUA Radar 对 arXiv 2508.02046v4（Luo、Yan、Gong、Wang、Zhang、Wang、Xie、Tan）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2508.02046 · 项目页（代码、数据、checkpoint）：https://iron-boyy.github.io/navimaster-page/*

## 问题：互不来往的两套导航技术栈

GUI agent 与具身导航 agent 都从第一人称观察出发去 traversing 环境，但论文指出二者“largely evolved in isolation, with disparate datasets and training paradigms”（ largely 各自演化，数据集与训练范式互不相通），并列出四个后果：(1) 一套系统要养两个模型，训练与部署成本翻倍，任务之间没有协同；(2) 在单一任务里堆数据对 out-of-domain（OOD）输入泛化差；(3) RFT 式训练用稀疏二值 reward，RL 优化效率低；(4) 从文本蒸馏出的推理常常“想法对、动作错”。论文的统一论证是形式化的：两个任务都是建立在 egocentric 视觉观察上的 Markov Decision Process（MDP），因此可以共享同一状态表示、同一动作空间和同一条训练流水线。

## NaviMaster 是什么

智能体的基座是 Qwen2.5VL-7B。每一步它看到：指令、当前观察（GUI 截图，或 Habitat 模拟器的第一人称画面）、深度图（纯 2D 截图时取零矩阵）、以及历史的 (thought, action) 对；输出一段思考加一个 JSON 动作。动作分三类：specific action 语义固定（GUI 的 BACK、HOME，具身的 STOP）；view-shifting action 是 GUI 的 SCROLL（上下左右）与具身的 TURN（left/right/around/down）；localization action 是核心设计——GUI 保留 CLICK(x, y)，具身导航把 MOVEFORWARD 改写成 MOVETO(x, y)，于是一次定位动作总是显式给出一个像素目标，这就是让两个动作空间同构的“visual target”。平台：mobile / web / desktop 的 GUI 基准（离线评测）加上模拟具身导航（Habitat 中的 Matterport 3D 场景）。它在 CUA Radar 板上的架构模式是 R01：offline single-step GRPO + 规则校验的 action/grounding reward。

流水线三步。第一，visual-target trajectory collection：GUI 轨迹直接复用 GUI-Odyssey；具身轨迹在 Matterport 3D 里对初始点与目标点跑 A\* 最短路，把下一个路径点投影进当前相机画面，目标出视野或在相机后方时插入 TURN 动作；再用 GPT-4o 为每个动作写约 60 词的第一人称 thought。第二，统一强化学习：不做 SFT（R1-Zero 配方），n 步轨迹的每一步是一个训练样本——“given an n-step trajectory, we take step i as a data sample”——GRPO 每步采样一组 rollout（5 个 generation），advantage 做组内归一化。训练共 20k 样本（10k GUI 来自 GUI-Odyssey，10k 具身来自 Matterport 3D 与 RoboPoint），在 8 张 A800 上训 3 个 epoch，batch size 128，学习率 1×10−6，KL 系数 0.01，框架为 EasyR1。第三，distance-aware reward：R = λ1·RF + λ2·RT + λ3·RG，λ 取 0.1、1、1；RF 检查 think/answer JSON 可解析，RT 检查动作类型与标签一致，RG 是稠密 grounding reward (1 − dj/θd)，按预测点到目标点的像素距离 dj 打分并加深度一致性门控；dense 阈值 θd = 200 像素，sparse 对照为 20 像素。训练信号完全由每一步唯一的标准参考动作经规则计算，环境不进环。

## 论文报告的结果

下面 GUI 与 affordance 全部离线，具身导航在模拟器中。论文称结果为多次试验的平均、推理用 vLLM temperature 0；未给种子数或标准差。

GUI，每步成功率（SR，Table 1；OS-Atlas 协议下的 per-step task success rate，GR grounding 精度另列）：

| 模型                 | AC-High   | AITZ      | GuiAct-W  | OmniAct-W | Odyssey   |
|----------------------|-----------|-----------|-----------|-----------|-----------|
| Qwen2.5VL-7B（基座） | 47.06     | 33.88     | 78.08     | 71.91     | 37.32     |
| GUI-R1-7B            | 51.56     | 49.06     | 74.54     | 68.69     | 36.22     |
| UI-AGILE             | 50.97     | 38.74     | 69.57     | 63.15     | 36.96     |
| Ours w/o Embodied    | 53.47     | 52.56     | 83.68     | 72.63     | 46.38     |
| **NaviMaster**       | **55.89** | **54.00** | **86.17** | **72.99** | **48.35** |

Odyssey 是 in-domain（GUI-Odyssey 即训练来源），论文将其余测试集标为 OOD；NaviMaster 的 grounding 为 93.90（AC-Low）、78.15（AC-High）。并非每列都是它最高：AC-Low SR 上 NaviMaster 为 69.46，低于 UI-shift 的 73.38 与 infiGUI-3B 的 92.10，论文用 in-domain/OOD 底色把这类差异区分开。

空间 affordance 预测（离线；预测点落入真值 mask 的平均成功率，Table 2）：

| 模型              | RoboReflt | Where2Place | RoboSpatial | RefSpatial |
|-------------------|-----------|-------------|-------------|------------|
| RoboPoint-13B     | 49.82     | 46.77       | 19.70       | 8.40       |
| Ours w/o Embodied | 67.86     | 35.05       | 14.75       | 16.88      |
| Ours w/o GUI      | 76.23     | 43.02       | 19.83       | 18.19      |
| **NaviMaster**    | **77.34** | **52.97**   | **21.65**   | **19.49**  |

具身导航（模拟；VLMNav 框架下 ObjectNav unseen validation branch，Table 3）：

| 模型              | SR        | SPL       |
|-------------------|-----------|-----------|
| Qwen2.5VL-7B      | 27.23     | 9.68      |
| RoboPoint         | 13.01     | 2.80      |
| SpaceLLaVA        | 14.98     | 2.62      |
| Ours w/o GUI      | 31.10     | 11.20     |
| Ours w/o Embodied | 31.00     | 10.05     |
| **NaviMaster**    | **33.20** | **12.60** |

（正文写 “the highest SR of 33.10%”，Table 3 印的是 33.20；本文取表格值。）

## 论文自带的对照实验

**数据混合。** 去掉任一来源都会掉：ObjectNav SR 从 33.20 降到 31.10（w/o GUI）与 31.00（w/o Embodied）；RoboReflt 从 77.34 降到 67.86（w/o Embodied）。混合比例扫描在 5:5 最优；mix 也优于先 GUI 后具身的两阶段课程（AC-High SR 55.89 对 54.83）。“All the experiments of NaviMaster use the same amount of data for a fair comparison.”

**Reward 设计。** sparse 变体（20 像素阈值）AC-High SR 为 54.07，dense 为 55.89；去掉 format 或 type reward 在各导航基准上掉 1–2 个点（Table 8）。距离阈值 200 像素优于 100/300/400 像素（55.06 / 55.77 / 53.61）；深度项被定位为鲁棒性设计而非性能来源。

**基座与规模。** 混合优势在 Qwen2.5VL-3B 上复现（45.26 对单源 3B 的 28.75，AC-High SR），7k 样本规模也成立（52.66），论文以此说明增益不只是一次强基座或大数据。

**指标警示。** 论文自己演示了 action-Type 指标有偏：一个只会预测 CLICK 的朴素模型能拿 55.9–64.4 的 Type 准确率，因此 Type 照报但不被信任。

## 论文自己承认的薄弱处

- 统一停留在数据层而非回合层：“Our trajectory dataset lacks any single trajectory that interleaves GUI and embodied navigation tasks due to the collection difficulty.”
- 方差只被断言、未被量化：“All reported results are averaged over multiple trials”——没有种子数、没有置信区间。
- 没有真机或在线网页评测：GUI 是离线每步精度，具身证据建立在模拟 ObjectNav 上。
- 基线训练语料各不相同（OS-Atlas、Aguvis 等用了大得多的数据），只有 NaviMaster 自家变体做到了数据量对齐。
- 同期的统一 agent OmniActor 被排除，理由是 “it is evaluated on a subset of benchmarks and its implementation is not publicly available”；推理 thought 依赖 GPT-4o 标注。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **63 分（★★）**，证据等级 **online**，架构模式 **R01**（offline single-step GRPO + 规则校验的 action/grounding reward）。判定记录肯定了：OOD 留出测试集、强 SFT 与 RL 基线、组件与 reward 消融、代码/数据/checkpoint 已发布；同时标注 variance 不明、online 评测为 partial（离线每步指标 + 模拟 ObjectNav）、budget 匹配为 partial（只对齐了数据量，基线语料不同）。判定记录 flagged 的“每步只有一条参考动作”在论文设计里即可看到：“given an n-step trajectory, we take step i as a data sample.” CUA Radar 未复现任何实验，本文所有数字均来自论文（版本 v4）。
