# Why Generate a Click？用即插式 decision head 从 prefill 里直接读出动作

*CUA Radar 对 arXiv 2610.20107v1（Gan、Liang、Wei、Zhang、Cai、Ni）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2610.20107v1*

## 问题：agent 把已经做过的选择又逐字写了一遍

基于 vision language model 的 web agent 靠”写”来行动：每一步读入目标和带编号框（numbered boxes）的截图，然后生成 `click(6)` 或 `type(5, "chair")` 这样的字符串。论文原话：“Most of this string records a choice from a short list: one of eleven action types and one of a few dozen boxes.” 把这个选择写出来，每个 token 都要付一次顺序解码；真正开放生成的只有 typing / answering 的文本。论文由此提问：generator 写第一个 token 之前，已经读完了目标、历史和所有框——这个决策能否直接从 prefill 的 hidden states 里读出来？agent 能否在读得准的步骤用廉价的 heads、其余步骤交给 generation，而不用两份代价？

## 方法是什么

**Agent 形态。** 桌面网站上的视觉 web agent。感知：Set-of-Mark 截图（N 个候选元素各画一个编号框）、目标、Mind2Web 文本形式的历史动作、以及来自目标和页面的 text options 列表。动作： eleven 种类型的 action grammar（click、type、select、hover、clear、enter、scroll down、scroll up、go back、answer、no operation），由 harness 解析执行。generator 为 Qwen3-VL-4B-Instruct / Qwen3-VL-8B-Instruct 加 rank-16 LoRA。在 CUA Radar 板上属于子模式 C05：frozen backbone 上的 attention action head。

**机制：plug-in decision heads + confidence cascade。** 三个小 head（4B 上 6.0M 参数、8B 上 9.2M，约为主干的 0.1%）读取 generator 36 层中五层（12、18、24、30、36）的可学习 scalar mix，再过 layer normalization。**Type head** 用 attention pooling 汇总整个 prefill，输出动作类型分布（限制为页面允许的类型）；**target head** 对每个编号框内的 visual tokens 取平均（Qwen3-VL 把每个 32 x 32 cell 编成一个 token），与一个可学习 query 打分，因此只需框坐标、不需要元素文本；**argument head** 以 pointer 方式给每个 text option 打分，另有一个可学习的 WRITE 槽。Confidence cascade 取三者的乘积 c = p(type) p(box \| type) p(argument \| type, box)：超过阈值 τ 就立即执行、零解码；若 argument 选了 WRITE，generator 只写文本（至多 24 个 token）；低于 τ 则 generator 从同一份 KV cache 解码整个动作——一次 forward pass 服务两种读出。

**训练信号。** generator 先在 213k 个 web 步骤上训练一个 epoch（成功的 MiniWoB++ episodes、Multimodal-Mind2Web 训练分割、GUIAct 单步与多步任务、UGround grounding、WebLINX demonstrations，全部转成统一格式）。随后冻结 generator，heads 在同一批 demonstrations 上训练一个 epoch，监督是示教的 (type, box, argument) 三元组，外加一个预测该步是否完成任务的辅助二值损失。WebArena 上两者再继续三个 epoch，训练数据来自 GPT-5.5 Set-of-Mark agent 的成功专家轨迹在 115 个训练任务上的 1,298 个重放步骤，与测试任务不相交。两个阈值在早期 MiniWoB++ 实验中固定：τ = 0.9（严格）与 τ = 0.5（宽松）。

## 论文报告的结果

在线任务成功率，均为 3 个训练种子的均值；MiniWoB++ 跑全部 119 个任务、5 个环境种子（12 个任务留出训练，每 episode 至多 10 步）；WebArena 在 6 个站点上跑 174 个测试任务，每任务至多 25 步。

| 方法（Qwen3-VL 基座） | MiniWoB++ 4B | MiniWoB++ 8B | WebArena 4B | WebArena 8B | Tokens/step 4B | Tokens/step 8B |
|----|----|----|----|----|----|----|
| Generator | 53.3 | 55.5 | 12.5 | 13.6 | 7.4 | 7.5 |
| Cascade, τ = 0.5 | 52.5 | 53.6 | 13.8 | 14.6 | 3.1 | 3.3 |
| Joint, generation | 53.3 | 55.0 | 11.5 | 11.1 | 7.3 | 7.4 |
| Joint, heads only | 45.4 | 45.3 | 3.1 | 4.4 | 0 | 0 |

MiniWoB++ 上 τ = 0.9 时 cascade 为 53.1%（4B）与 55.4%（8B），与 generator 相差在 0.2 点以内，heads 单独执行 29% / 33% 的步骤；τ = 0.5 时让出 0.8 与 1.9 点，heads 单独执行 67% / 69%。WebArena 上 heads 单独执行 52%（4B）与 51%（8B）的步骤、另有 17% 与 14% 走 WRITE，生成 token 降到一半以下，episode 从 15.7 步缩到 14.0 步（4B）、16.8 到 16.2（8B）。离线一侧（step success，另一根轴）：τ = 0.9 时 cascade 在全部七个测试集（三个 Multimodal-Mind2Web 留出分割 + 四个 GUIAct 集）上与 generator 相差 0.3 点以下至高出 1.4 点，heads 决定 12 到 64% 的步骤；τ = 0.5 时 Mind2Web 未见网站上的 step success 提高 3.1（4B）与 1.8（8B）点，GUIAct 四个集损失 1.0 到 1.9 点。计时（MiniWoB++）：4B generator 每步 0.234 秒，τ = 0.9 时 0.207 秒（1.13x），τ = 0.5 时 0.168 秒（1.39x）。

## 论文自带的对照实验

**模板切分（最关键的一条）。** WebArena 的全部增益来自意图模板在 115 个重放训练任务中出现过的那 47 个测试任务：4B 从 34.8 到 41.8，8B 从 33.3 到 36.9。其余 127 个新模板任务上两个系统都低于 7%；cascade 比 4B generator 低 0.8 点、与 8B 持平。

**联合训练不免费。** heads 与 generator 同一个 adapter 联合训练，会让 generator 自身在离线集上的 step success 下降 0.5 到 4.9 点（4B 验证损失从 0.214 升到 0.235），尽管 joint heads 本身更强（heads only 提高 0.3 到 1.9 点）；two-model cascade（joint heads + 单独训练的 generator）在 Mind2Web 上最好，标准协议下最多比 generator 高 3.8 点。

**换 target head。** 把 target head 换成 GUI-Actor 的 patch attention head（同样方式训练、GUIAct 留出）：heads only 的 box pooling 在五个测试集中的四个上领先，例如 M2W cross-task 37.3 对 35.3；attention mass 在 M2W 上失效，因为 82% 的测试步骤里存在包住 gold box 的更大候选。

**路由不是随机的。** 在 heads 决定的步骤上（M2W cross-website 的 37%），heads 成功率 68.6，generator 只有 60.3；同样份额随机分配只有 39.8，而 cascade 达到 44.0。M2W 三个分割上 typing 分别提高 9.1、9.1、6.3 点，未见网站上 select 从 14.8 提高到 39.8。

**参照点。** 标准 Mind2Web 协议下，Aguvis 7B 在三个分割上都领先本文所有系统（60.4 / 54.6 / 56.6）。先写 thought 再写动作的 reasoning generator 比普通 generator 低 4.0 点、慢七倍；heads 挂在它上面可在三分之二的步骤上单独执行，把每步时间从 1.56 秒降到 0.70 秒。

## 论文自己承认的薄弱处

- “Our heads choose among numbered boxes, so agents that act through raw screen coordinates would need a different target head.”
- “The heads are tied to one generator; after fine-tuning the generator for WebArena we trained them again.”
- “All experiments use Qwen3-VL backbones and a single action grammar, and the threshold is fixed per experiment.”
- WebArena 成绩”follows the WebArena checkers, with GPT-5.5 judging answers that need fuzzy matching”——判定器本身没有单独验证，判定记录将其标为 untested。
- 板上没有记录代码仓库。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **online**。分数反映论文报告的证据：WebArena 与 MiniWoB++ 的在线评测、所有成功率取 3 个训练种子的均值、预算对齐的对照（所有系统共享同一 generator、prompt 和框）、token 与时间成本、以及成套消融（阈值扫描、联合训练、target head 替换、模板切分）。判定记录把 held-out 环境标为 partial（WebArena 训练任务是重放的专家轨迹，与测试任务不相交但共享意图模板）、judge 验证标为 untested、代码状态标为 unclear；未标记任何 anti-pattern。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
