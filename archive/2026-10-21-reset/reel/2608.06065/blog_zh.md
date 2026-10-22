# The Next Screenshot Knows：用“下一张截图”做事后蒸馏的移动端 GUI 智能体

*CUA Radar 对 arXiv 2608.06065v1（Weiwei Li、Junzhuo Liu、Tong Chu、Hengfu Yu、Wen Li；电子科技大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2608.06065v1 · 代码：仅声明”The code and checkpoints will be made available”，v1 时尚未发布。*

## 问题：证明一个动作正确的证据，晚了一屏才出现

大多数 GUI agent 在离线成功轨迹上训练：把轨迹切成 prefix-action 对，从目标、交互历史和当前截图预测动作，然后丢掉之后的一切。论文的观点是，这一丢丢掉的正是“为什么”。比如打开一个藏在子菜单里的设置项，当前屏幕上多个入口看起来同样合理；只有点击之后的下一张截图（子菜单已展开）才说明哪个入口是对的、为什么对。标准模仿学习只教策略“做什么动作”，不教“为什么合适”；标量 RL 奖励也只告诉 rollout 对不对，不传递支撑它的应用知识。作者称之为 future-dependence：动作必须由过去预测，而解释它的证据常常只在未来出现。

## GHD 是什么

这是一个 Android 移动端 GUI agent，在 AndroidWorld 和 AndroidLab 上评测。每一步观察自然语言目标、动作历史和当前截图，输出一段 reasoning 再给出 JSON tool-call 动作（click、long_press、swipe 带归一化 1000×1000 网格坐标；文本动作；离散参数需精确匹配）。基座是 Qwen2.5-VL-7B 和 Qwen3-VL-8B，各自按 OpenMobile 配方微调（截图缩到 420×896，视觉 token 约 3 倍减少，代价是初始 SFT 分数低于已发布的 OpenMobile checkpoint）。在 CUA Radar 板上它属于子模式 R01：带规则校验动作奖励的离线单步 GRPO。

Gated Hindsight Distillation（GHD）在这一套之上只加了一个训练期装置：

- **特权 teacher。** 与 student 共享全部参数的 teacher 额外看到成功演示里真实出现的下一张截图。它不自回归生成自己的轨迹，而是在 teacher forcing 下、沿 student 自己的 rollout 逐 token 重新打分（stop-gradient）。
- **Gating。** 只有当只看 prefix 的 student 未通过步级验证器（reward 低于 τ = 1.45）、且 teacher 逐位置 top-1 解码恢复了演示动作（动作名相同、JSON 可解析、坐标在网格上相差不超过 δ = 20）时，才保留蒸馏。这个 gate“直接验证了用于蒸馏的信号”。
- **转移方式。** teacher 与 student 分布之间的广义 Jensen-Shannon 散度（α = 0.5），只在 student 的 top-K = 100 token 上计算；联合损失 L = L_GRPO + 0.1 · L_GHD。Dynamic sampling 每个 prompt 最多重采三组 rollout（全程平均 2.69 次）。
- **训练信号。** 规则步级验证器——format、动作类型匹配、value（坐标、编辑相似度或精确匹配）——给出 \[0, 1.5\] 内的 R，同时用作 GRPO 奖励和 gate。训练 200 步，数据是 SFT 模型一次尝试失败的 OpenMobile 硬子集：7B 从 27,360 条过滤到 6,968 条，8B 为 5,982 条。

部署时 teacher、下一张截图和 gate 全部移除：推理就是原来的 prefix-only student，不引入“任何额外的推理期模块”。

## 论文报告的结果

以下均为任务级在线成功率 Pass@1（%），三次独立运行的均值 ± 标准差；数据、评测设置相同，GRPO 与 GHD 共享同一初始化（Table 3）。

| 模型          | 方法    | AndroidWorld     | AndroidLab       |
|---------------|---------|------------------|------------------|
| Qwen2.5-VL-7B | SFT     | 46.55            | 29.71            |
| Qwen2.5-VL-7B | GRPO    | 47.13 ± 0.65     | 31.93 ± 1.12     |
| Qwen2.5-VL-7B | **GHD** | **52.73 ± 1.51** | **43.10 ± 0.66** |
| Qwen3-VL-8B   | SFT     | 59.05            | 39.13            |
| Qwen3-VL-8B   | GRPO    | 61.35 ± 1.08     | 37.43 ± 0.42     |
| Qwen3-VL-8B   | **GHD** | **66.47 ± 0.68** | **54.11 ± 1.11** |

与已报告系统的对比（Table 1，各系统“按其原始实验设置”）中，Ours-7B 平均 Pass@1 为 47.9（AndroidWorld 52.7、AndroidLab 43.1），Ours-8B 为 60.3（66.5、54.1）；论文称这是两个规模上 open-data 模型中最好的平均 Pass@1；OpenMobile-8B 为 58.1，UI-Venus-1.5-8B 在 AndroidWorld 上达到 73.7。同一张表里也有诚实的细节：8B 的 Pass@3 上，AndroidWorld 为 73.3，低于 OpenMobile-8B 的 78.0，而 AndroidLab Pass@3 为 65.2 对 62.3。论文没有离线单步准确率数字，以上全部是在线结果。

## 论文自带的对照实验

**组件消融（Table 2，AndroidWorld，7B）。** 从 GRPO 的 47.13 起：加 gate 但 teacher 无特权信息为 47.84（+0.71）；再加 dynamic sampling（仍无未来信息）为 49.56（+2.43）；完整 GHD 加上下一张截图到 52.73（+5.60）。论文明确说下一张截图带来进一步的 3.17 点，是“最大的增量”。

**预算对照（Table 5，8B）。** 不用 dynamic sampling 的 GHD 与 GRPO 用同一“每次一个 rollout-group”的生成预算，仍达到 AndroidWorld 63.64 ± 2.04、AndroidLab 51.93 ± 0.84（论文写明提升为 2.29 和 14.50 点）；dynamic sampling 再加 2.83 和 2.18。

**特权信息对照（Table 4，AndroidWorld，8B）。** 流程不变，只换 teacher 的提示：只给参考动作为 58.62（相对 SFT −0.43），加参考 reasoning 为 60.34（+1.29），换成下一张观测为 64.67（+5.62）；带 GRPO 的完整方法为 66.47（+7.42）。只给答案没用，未来屏幕有用。

**转移机制对照。** 在试过的每种特权信号下，distillation 都优于 STaR 式离策自训练（Figure 3）；在 GRPO 上加 GUI-Shift 式逆动力学辅助任务只 +0.28（47.41），而 GHD 为 +5.60（Table 6），两者从同一 SFT checkpoint 出发。

**分应用（Table 7）。** 一次代表性 8B 运行、138 个 AndroidLab 任务上，GHD 在九个应用中的七个上胜过 GRPO（总体 55.07 对 37.68），Bluecoins（26.67 到 60.00）和 Contacts 提升最大；例外是 Calendar 和只有五个任务的 Zoom。

## 论文自己承认的薄弱处

- 对比表“旨在说明整体竞争力，而非隔离 GHD 的贡献”：各系统在“模型家族、训练数据、图像分辨率和算法”上不同，且复现的 SFT 起点用 420×896 截图，低于已发布 OpenMobile checkpoint 的分数。
- 未讨论 held-out 应用：论文没有说明 AndroidWorld/AndroidLab 的应用与训练所用 OpenMobile 轨迹是否不相交。
- 成本报告不完整：给了数据量和 GPU 型号（4 卡），但 wall-clock 对比只是“指示性的而非受控的系统对比，因为实验在非独占的租用实例上进行”。
- 代码与 checkpoint 仅声明将发布；分应用结果是单次代表性运行。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **62 分（★★）**，证据等级 **online**，子模式 R01（规则奖励的离线单步 GRPO）。判定记录肯定了：两个基准上的在线评测、三次运行的均值与标准差、同初始化/同数据/同 rollout 预算的受控对比，以及覆盖 gate、dynamic sampling、特权信息和转移机制的消融。同时标注：held-out 环境问题不清楚（unclear）、成本报告为 partial、代码尚未发布、只测了 7B/8B 开源基座。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
