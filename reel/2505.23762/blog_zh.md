# ZeroGUI：让 GUI agent 自己出题、自己判分的零人工成本在线训练

*CUA Radar 对 arXiv 2505.23762v1（Chenyu Yang、Shiqian Su、Shi Liu、Xuan Dong、Yue Yu 等）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2505.23762v1 · 代码：https://github.com/OpenGVLab/ZeroGUI*

## 问题：离线训练处处要人

基于大型 vision-language model 的 GUI agent 通常离线训练，论文指出两个代价：一是”heavy reliance on high-quality manual annotations for element grounding and action supervision”（对 grounding 标注和动作监督的人工标注高度依赖），二是”limited adaptability to dynamic and interactive environments”（对动态交互环境适应性有限）。OSWorld、AndroidLab 这类交互式基准只提供人工设计的测试任务和脚本验证函数，可以直接拿来打分，却不能当训练集。手工构造上千个多样训练任务并为每个任务写验证脚本无法扩展，真实场景的新任务更不会自带真值标签。

## ZeroGUI 是什么

被训练的是纯视觉 GUI agent：UI-TARS-7B-DPO 和 Aguvis-7B，均为 7B。感知只用 screenshot（不用 DOM 或 a11y tree），动作用坐标定位的原语——click、type、hotkey、terminate——运行在桌面（OSWorld 的 Ubuntu，1920 x 1080，最多 15 步）和手机（AndroidLab，9 个离线部署 app）上。在 CUA Radar 板上，本文属于子模式 K16：“learned outcome and process judges” 下的被动 VLM outcome judge。

ZeroGUI 把两件手工活自动化：

1.  **Automatic task generation。** 用 GPT-4o，输入任务范例（exemplars）加一张随机采样初始状态的 screenshot，一次生成多个候选（OSWorld 每条 prompt 10 个，AndroidLab 5 个）以保证多样性；还刻意生成一部分不可行任务，要求 agent 明确输出 “FAIL”。共生成 4,000 多个 Ubuntu 任务和 225 个 Android 任务，从中采样 725 和 175 个用于训练，约为各自测试集的两倍。
2.  **Automatic reward estimation。** 本地部署的 Qwen2.5-VL-32B 对整条轨迹给二值 reward。设计针对 false positive——论文认为它比 false negative 更会带偏策略：给 judge 看轨迹的全部 screenshot（而不是只看最后一帧）；不给看 agent 自己的回复（回复会幻觉成功）；以 temperature 1.0 查询 4 次并要求 unanimous agreement 投票。
3.  **Two-stage online RL。** 第一阶段在生成任务上训练；第二阶段直接在测试集上做 test-time training，不用真值标签，reward 同样来自这个 VLM 估计器。GRPO 被扩展到多步轨迹：每个任务一组 G = 64 条轨迹，advantage 是组内归一化的投票 reward，配合 DAPO 式 dynamic sampling、AdamW 常数学习率 2e-6，每阶段 1 个 epoch。KL 项从 k3 估计器换成 k2 的 per-token MSE 版本，附录推导认为它避免巨大梯度和数值溢出。

训练信号只有 VLM 投票的二值结果，全程没有人工标签。

## 论文报告的结果

以下全部是在线成功率（SR），4 次运行的 mean ± std，screenshot-only 模式。

| 模型 | OSWorld 全部任务 | OSWorld 可行子集 | AndroidLab 全集 | AndroidLab 操作子集 |
|----|----|----|----|----|
| UI-TARS-7B-DPO | 17.7 ± 1.1 | 11.3 ± 0.6 | 45.7 ± 1.52 | 54.6 ± 1.72 |
| \+ ZeroGUI | 20.2 ± 1.0 | 15.8 ± 0.5 | 47.5 ± 2.12 | 57.4 ± 2.30 |
| Aguvis-7B | 3.0 ± 0.4 | 2.4 ± 0.5 | – | – |
| \+ ZeroGUI | 4.9 ± 0.4 | 4.5 ± 0.4 | – | – |

论文报告：UI-TARS-7B-DPO 在 OSWorld 全部任务上 +2.5（相对 14%），可行子集上 +4.5（40%）；Aguvis-7B 上 +1.9（63%）和 +2.1（88%）。AndroidLab 上全集 SR +1.8，操作子集 +2.8，sub-goal 成功率 +2.9。pass@4 从 25.5 升到 28.0，all-pass@4 从 9.4 到 9.6（UI-TARS），论文解读为生成任务扩展能力覆盖、test-time training 提升一致性。作为参照，论文表中带 \* 的行取自先前论文、设置不同：GPT-4o 5.0，Claude Computer-Use 14.9，OpenAI Operator 19.7，UI-TARS-72B-DPO 22.7。

## 论文自带的对照实验

**Judge 对照人工标注检验。** 在人工标注的轨迹上，完整估计器 precision 61.5 / recall 51.1，测试 SR 27.2；只看最后一帧降到 47.5 / 40.4，SR 23.9；让 judge 读 agent 回复，recall 最高（74.5）但 precision 44.3、SR 24.0——回复会把它带向 false positive；去掉投票居中，53.7 / 61.7，SR 25.6。

**任务生成消融。** 去掉 exemplar，SR 降到 22.3（不可行任务检测 33.8）；去掉多候选生成 24.1；去掉生成的不可行任务，不可行子集从 41.3 跌到 22.1——FAIL 任务能抑制过度自信。

**训练配方。** OSWorld Daily 域上：offline RFT 22.4、online RFT 24.5、online RL 27.2；把 k2-KL 换回 GRPO 的 k3-KL 则是 26.1，且训练准确率曲线更不稳。KL 系数扫描（图 6）支持中间取值，去掉 KL 或系数过大都变差。

**两阶段拆分。** 只做 test-time training 到 18.2（测试集 SR），只做生成任务训练也是 18.2，两阶段 20.2——阶段顺序有用。

## 论文自己承认的薄弱处

- 第二阶段在测试集上训练：“the agent performs test-time training on the test set without ground-truth labels, receiving rewards solely from the same VLM-based evaluator”。评测环境同时是训练环境，论文没有报告 held-out 环境。
- OSWorld 全集上的增益小于可行子集，“indicating a decrease in the detection of infeasibility”；论文归因于 VLM 缺乏具体软件知识、reward 有噪声，FAIL 任务只是部分缓解。
- AndroidLab 上”we fix some code errors in the original task verifiers, and some baseline methods get higher scores after the correction”，query-detecting 任务的 GPT 评分”is not fully reliable”，所以另外报操作子集。
- 消融只在 Daily 域（Chrome、Thunderbird、VLC）上做，“to reduce experimental burden”；判定记录还把预算对齐标为 partial（15 步上限）、成本报告标为 partial。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **transfer**，子模式 K16（被动 VLM outcome judge）。判定记录认可：OSWorld 与 AndroidLab 的在线评测、4 次运行的 mean±std、offline/online-RFT 基线、任务生成与 judge 与 KL 的组件消融、judge 对人工标注轨迹的 precision/recall 检验、已发布代码。同时标出：没有 held-out 环境（test-time training 直接用测试集）、预算与成本对齐只算 partial。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
