# Q-Reflector：先生成前置/后置条件、再判断移动端 GUI 步骤的 8B 训练型 reflector

*CUA Radar 对 arXiv 2608.05587v2（Guo、Liu、Gu、Wang、Chen）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2608.05587v2 · 代码：https://github.com/pockyitachi/Q-Reflector*

## 问题：反思要么放过太多，要么拒绝太多

移动端 GUI agent 每执行一个动作，都要决定继续、重试、恢复还是停止，依据是一步 reflection：这个动作是否执行成功，结果是否是朝任务目标迈出的有效一步？有效的一步不必完成任务。打开时间选择器是设置闹钟的有益准备，而一次让设置列表纹丝不动的滑动则是失败。接受无效的转移，会让 agent 在动作失败或无关之后继续往下走；拒绝有效的转移，则会引发不必要的恢复。

作者报告：在同一个提示词下作为独立 reflector 使用时，前沿 VLM 和专门的 GUI 模型都明显偏向一边。在他们人工核验的 1,082 个 AndroidWorld 转移上，GPT-5.2 对负例的准确率为 95.10%，对正例只有 51.39%；GUI-Owl-1.5-8B 则相反（正例 92.33%，负例 57.78%）。此外，每个动作后单独调用一次 reflection，在长任务中会累积推理成本。

## Q-Reflector 是什么

场景是 Android（移动端）。reflector 是基于 Qwen3-VL-8B 的独立模块，生成动作的模型保持不变。每个动作执行后，它接收任务目标、动作（类型、参数和意图描述）、最近至多五个动作，以及 BEFORE 和 AFTER 两张截图。它在一次调用中按顺序输出四个 JSON 字段：precondition、postcondition、三段式 rationale（前置检查、后置检查、任务进展）和二值 Yes/No 判定。precondition 说明动作需要什么；postcondition 说明它预期的局部效果。两者应当只依据任务、动作、历史和 BEFORE 截图写出，而不是迎合结果去改写。论文指出，这只是对模型的指令，而不是运行时的隔离，因为两张图是一起提供的。只有预期效果确实发生、且该步对任务有效时，判定才是 Yes。在 CUA Radar 的分类里这是 C18 模式：用前后观察验证每个动作的结果，并把判定反馈回去。

反馈刻意收得很窄。只有 No 判定才会产生提示，并追加到动作模型的下一次观察中：上一个动作、后置检查、任务进展判断，以及“不要重复相同坐标或文本”的指令。生成的条件本身留在 reflector 内部，不传给动作模型。

训练分三个阶段，使用 880 个人工审核的转移（512 正例、368 负例），由 Agent-SAMA 在 Mobile-Eval-E 和 SPA-Bench 上运行收集。第一阶段是对四字段响应做监督微调（LoRA，rank 16），条件目标由 GPT-5.2 起草、人工审核。第二阶段是用 GPT-5.2 响应做 teacher-student distillation。第三阶段是带不对称判定奖励的 GRPO（判对 Yes 为 +2.5，判对 No 为 +2.0，两种错误分别为 -2.0 和 -2.5，另有 0.1 的格式奖励），随后用 559 个“正确/错误采样响应”配对做 DPO。训练信号是经过审核的判定标签；论文明确说明，奖励并不评估条件本身的质量。

## 论文报告的结果

**离线（AndroidWorld，1,082 个转移：613 正例、469 负例）。** 二值判定的准确率，所有 reflector 使用相同的提示词和输入。

| Reflector        | Overall   | Balanced  | Positive | Negative |
|------------------|-----------|-----------|----------|----------|
| GPT-5.2          | 70.33     | 73.24     | 51.39    | 95.10    |
| Claude Haiku 4.5 | 76.89     | 78.96     | 63.46    | 94.46    |
| GUI-Owl-1.5-8B   | 77.36     | 75.06     | 92.33    | 57.78    |
| **Q-Reflector**  | **82.16** | **81.45** | 86.79    | 76.12    |

Balanced accuracy 是正负两类准确率的等权平均；Claude Haiku 4.5 是该指标上最强的基线。GUI-Reflection-8B（使用其 Action Verification 预训练检查点）总体为 60.72，此处未列出。

**在线（MobileWorld，每个动作模型 117 个任务）。** 带条件生成时的任务成功率（%），由 MobileWorld 自带评估器判定，每次尝试最多 50 个动作决策步。这与上面的离线数字是两回事，不能放在一起比较。

| Reflector         | GUI-Owl-1.5-8B-Instruct | MAI-UI-8B |
|-------------------|-------------------------|-----------|
| No reflection     | 29.06                   | 21.37     |
| Self-reflection   | 41.88                   | 27.35     |
| GPT-5.2           | 42.74                   | 29.06     |
| Claude Haiku 4.5  | 39.32                   | 29.91     |
| GUI-Reflection-8B | 39.32                   | 29.06     |
| **Q-Reflector**   | **46.15**               | **35.90** |

论文给出的相对无外部反思的提升是 17.09 和 14.53 个百分点（分别多完成 20 和 17 个任务），相对最强基线 reflector（GPT-5.2 和 Claude Haiku 4.5）则分别是 3.42 和 5.98 个百分点。对同一个动作模型，所有 reflector 的输入信息和反馈接口保持一致。

## 论文自带的对照实验

**条件生成。** 论文单独训练了一个 Q-Reflector 变体：同一基座、同样的 880 个转移、阶段和超参数，只有提示词和响应结构不同（只有 rationale 和判定，没有条件）。它在 MobileWorld 上的成功率为：GUI-Owl 41.88%、MAI-UI 29.91%，完整模型则为 46.15% 和 35.90%。论文给出的差距是 4.27 个百分点，以及 MAI-UI 多完成七个任务。对检查点固定的其他 reflector，用提示词加入条件生成时，GUI-Owl 上有提升，MAI-UI 上则好坏不一（self-reflection 和 Claude Haiku 4.5 分别少完成四个和两个任务）。用论文的话说，条件生成的收益取决于动作模型与 reflector 的组合。

**不带条件时，MAI-UI 上 Q-Reflector 并非最优。** 在 Table 2 的无条件列中，MAI-UI 下 Claude Haiku 4.5 为 31.62%，self-reflection 为 30.77%，而 Q-Reflector 变体为 29.91%。GUI-Owl 下该变体（41.88%）领先 GPT-5.2（40.17%）。论文关于“成功率最高”的结论限定在统一的条件生成设置之下。

**Token 成本。** 带条件时，相对该消融变体，每任务平均输入 token 在 GUI-Owl 上增加 41.1%，在 MAI-UI 上增加 76.0%；输出 token 在 GUI-Owl 上减少 5.6%，在 MAI-UI 上增加 50.8%。对 GUI-Owl，带条件时每任务输入 token 为 236,132，无反思时为 143,649。论文提醒，这些计数依赖各自的 tokenizer 和视觉编码器，并不直接衡量延迟或硬件成本。

**训练阶段与顺序。** distillation 并不能稳定保持独立分类准确率：对 Qwen3-VL-8B，总体准确率从 73.11%（基座）升到 SFT 后的 80.87%，distillation 后降到 78.37%。先 GRPO 后 DPO 得到 82.16%，先 DPO 后 GRPO 为 80.41%；颠倒顺序会把负例准确率提高到 87.42%，但会拒绝更多有效转移。

## 证据偏薄之处（用论文自己的话）

- 评估规模是 1,082 个转移和 117 个任务。两个在线动作模型都是 8B；“transfer to other sizes remains untested”。验证集中在移动端，web 和桌面场景同样“remains untested”。
- 每个配置每个任务只保留一个最终得分，解码固定（temperature 0 或 greedy）。论文没有报告随机种子、标准差或置信区间。
- “Evaluation measures verdict accuracy and downstream task success, without independently scoring the semantic correctness of generated conditions.”
- 标签由 GPT-5.2 辅助并经作者审核；这种人工投入“limits scalability”。有限的历史可能会掩盖准备性或恢复性步骤的目的。
- 截图缩放（最长边 1,024 像素）、解码设置和输出预算都没有系统性地变化。
- 附录 D.5 有一个 MobileWorld 定性例子：无反思时连续七次无效滑动，有 Q-Reflector 时下一步即恢复；两次运行最终都成功。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **81 分（★★★）**，证据等级 **transfer**，子模式 C18。判定记录中视为论文已报告的项目有：MobileWorld 上的在线评估、与训练基准分离的测试基准、较强的基线、成本报告、条件生成的消融，以及在带标注转移上对学得的判定器的检验。预算对齐被记为部分满足，方差被记为未报告，没有触发任何反模式标记。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
