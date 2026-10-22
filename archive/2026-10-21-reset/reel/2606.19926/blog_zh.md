# MemGUI-Agent：把上下文管理变成动作的端到端移动 GUI 智能体

*CUA Radar 对 arXiv 2606.19926v1（Liu 等，浙江大学与快手科技）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2606.19926v1 · 代码（论文中为”将发布”）：https://github.com/kwai/MemGUI-Agent*

## 问题：长任务击穿被动式上下文

移动 GUI 智能体能做短任务，但任务一长就退化：论文开篇给出 GUI-Owl-1.5-8B 从 AndroidWorld 的 71.6%（平均 8.4 步）掉到 MobileWorld 的 38.2%（平均 27.8 步），再到 MemGUI-Bench 的 11.7%（平均 36.2 步）。作者把这归因于 ReAct 式提示——它”被动累积每步记录，导致 prompt 爆炸、跨应用关键事实被稀释”。价格、编号、复制的文本需要跨屏幕、跨应用存活，但被动策略只会机械地追加、截断或丢弃记录；外挂记忆框架又把内容整理移出了端到端策略。

## MemGUI-Agent 是什么

这是一个端到端的多模态移动 GUI 智能体。感知端是截图加结构化状态 S<sub>t</sub> = (G, H<sub>t</sub>, M<sub>t</sub>, L<sub>t</sub>)：任务目标 G、Folded Action History（压缩后的轨迹摘要）、Folded UI State（持久保留的 UI 事实）、Recent Step Record（最近一步详情）。动作端每步恰好执行一个动作，来自 A<sub>ui</sub> ∪ A<sub>mem</sub>：UI 动作（click、long_press、swipe、type、answer、system_button、wait、terminate，1000×1000 坐标系），或记忆操作（memory_add、memory_update、memory_delete），记忆条目是 (id, description, content) 三元组，存完整内容而非摘要。平台是 Android 风格：快照式的 MemGUI-Bench 环境（26 个应用）和容器化的 MobileWorld（Mattermost、Mastodon、Mall4Uni）。

机制是 **Context-as-Action（ConAct）**：上下文管理成为同一策略的一等输出。每步模型在一次前向中输出五部分——reasoning、folding directive、tool call、带落地细节的 UI observation、action intent。folding directive 指定一个历史区间和生成摘要：step-level distillation 压缩最近一步，span-level abstraction 把完成的子任务总结成一条。在 CUA Radar 板上这是子模式 C16（让智能体自己提名要留存的task-relevant 内容），挂在”结构化 prompted agent loop”主模式之下。

训练信号是 **MemGUI-3K**：把 MemGUI-Bench 的 128 个种子任务经 entity substitution（456 个）、memory-operation augmentation（289 个）、task simplification（6,558 个）扩成 7,303 个任务的池子；其中 5,293 个由 Qwen3-VL-235B-Thinking 教师按完整 ConAct 协议各滚一条轨迹，经 MemGUI-Eval 渐进审查流水线判定，并做轨迹级与步级双重过滤（每步标注 reasonable/unreasonable）。最终得到 26 个应用上的 2,956 条轨迹，平均 28.8 步（论文标注为 GUIOdyssey 15.3 步的 1.9×），75.7% 的步是 reasonable，产出 64,430 个 SFT 样本，并与评测任务验证零重叠。**MemGUI-8B-SFT** 由 Qwen3-VL-8B-Instruct 在 57,951 个训练样本上做 LoRA（rank 8，alpha 32）微调，1 个 epoch，seed 42，8×80GB GPU 上 535 分钟。

## 论文报告的结果

以下头条数字全部为**在线**（真实交互）结果。MemGUI-Bench：128 任务，最多 3 次尝试，步数预算 2.5g + 1（g 为 golden-step 数），由 MemGUI-Eval 判定。MobileWorld GUI-Only：117 任务，单次尝试，50 步上限，由后端验证器判定。

| 智能体（MemGUI-Bench）                       | P@1      | P@3      | IRR      |
|----------------------------------------------|----------|----------|----------|
| M3A（Gemini-2.5-Pro，最强框架）              | 32.8     | 47.7     | 39.3     |
| Qwen3-VL-235B-Thinking                       | 24.2     | 46.9     | 30.0     |
| Qwen3-VL-8B-Instruct                         | 9.4      | 20.3     | 15.1     |
| MemGUI-8B-SFT                                | 23.4     | 35.9     | 30.2     |
| **MemGUI-Agent-235B**（zero-shot，权重不变） | **37.5** | **62.5** | **46.8** |

| 智能体（MobileWorld GUI-Only）           | SR   |
|------------------------------------------|------|
| GUI-Owl-1.5-32B-Instruct（最强开源权重） | 43.9 |
| Qwen3-VL-235B-Thinking                   | 14.5 |
| Qwen3-VL-8B-Instruct                     | 9.4  |
| OpenMobile-8B（open-data）               | 17.7 |
| **MemGUI-8B-SFT**                        | 17.9 |
| **MemGUI-Agent-235B**                    | 29.1 |

论文报告：相对同一 235B 基座在 MemGUI-Bench 上 +13.3 P@1、+16.8 IRR；MobileWorld 上 235B 智能体 +14.6 SR、8B +8.5；并称 MemGUI-8B-SFT 为最好的 open-data 8B 成绩。增益集中在更难的任务（8B-SFT：Medium +19.0、Hard +18.5、Easy +6.2）。**离线**步级技能指标单列：在 MemGUI-3K 测试集、gold context 下，UI 动作匹配从 29.2 升到 36.3，memory trigger F1 从 19.9 升到 48.0，deep-fold 比例从 8.8 升到 26.1（gold 为 23.2），格式合规到 99.9。

## 论文自带的对照实验

**尺度扫描（Table 1）。** Zero-shot ConAct 只在最强基座上有效：MemGUI-Bench-40 的 P@1 变化为 2B 10.0→5.0、4B 20.0→12.5、8B 12.5→7.5、235B-Instruct 23.4→19.5，而 235B-Thinking 是 5.0→40.0（P@3 27.5→62.5，IRR 19.5→51.0）。这正是论文构造监督数据的动机。

**组件消融（Table 5，MemGUI-Bench-40，zero-shot 235B-Thinking）。** 从 ReAct 基线 5.0 P@1 出发：加 UI memory actions 到 17.5，加 history folding 到 22.5，加 self-describing step 到 25.0，完整 ConAct 为 40.0 P@1 / 62.5 P@3；MTPR 0.143→0.429，IRR 19.5→51.0。

**留出迁移。** MobileWorld 的环境、应用、协议都不同，8B 模型仍有 17.9 SR；训练数据与 128 个评测任务验证零重叠。

**成本。** 150 步内 ConAct 的 prompt 增长显著平缓于 ReAct，到第 150 步约省 1.5k 输入 token。

**失败分析。** 总失败从 99 降到 58（−41%），主要来自 process hallucination（−42%）与 output hallucination（−57%）；knowledge deficiency 与 intent misunderstanding 基本不变。

## 论文自己承认的薄弱处

- 尺度依赖：“on smaller open models and Qwen3-VL-235B-Instruct, the added protocol often reduces performance”——zero-shot 增益建立在一个基座之上。
- 范围：“Our experiments focus on Android-style mobile GUI environments. Extending ConAct to iOS, desktop, and web interfaces remains future work.”
- 代码与数据在 v1 中是承诺而非已发布：“Code, data, and trained models will be released”。
- 评测的跨次方差未报告（seed 42 只覆盖 SFT 划分与训练）；MobileWorld 每任务单次尝试。
- MemGUI-Bench 与 MemGUI-Eval 判定器来自作者自己的早期工作，数据教师与最强 zero-shot 智能体同用 Qwen3-VL-235B-Thinking；在 MobileWorld 上两个 MemGUI 智能体仍远低于最强开源权重模型（43.9）。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **62 分（★★）**，证据等级 **transfer**——等级由留出的 MobileWorld 迁移结果支撑。判定记录认可其在线评测、留出环境、同基座差值、组件消融与成本报告；同时把跨次方差、budget-match 记为 unclear，MemGUI-Eval 验证器记为 untested，代码记为 announced，并标记两个 anti-pattern：AP15（脚手架增益只在 frontier 基座上展示）与 AP18（folding 是有损压缩）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
