# TTI：把 test-time scaling 从”多想”转向”多做”的网页智能体

*CUA Radar 对 arXiv 2506.07976v2（Shen、Bai、Zhang、Zhou、Setlur、Tong、Caples、Jiang、Zhang、Talwalkar、Kumar）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2506.07976v2 · 代码：https://github.com/test-time-interaction/TTI*

## 问题：想得更久不是唯一的旋钮

当前的 test-time scaling 主要是在给出动作前生成更长的推理链。论文认为，对需要在环境中交互的智能体来说，这至少是不完整的旋钮：更长的单步思考”does not allow agents to acquire new information from the environment or adapt their behavior over time”。而每多一步交互都会带回新的观察——没看过的商品列表、变化中的价格、挡住去路的弹窗。论文因此提出 interaction scaling：增加允许交互的步数，作为与”加深单步推理”互补的一条 test-time scaling 轴线，并回答两个问题：在相同 token 预算下，多做是否胜过多想；以及能否靠训练（而不只是 prompting）让智能体把多出来的步数用好。

## TTI 是什么

智能体是基于 Gemma 3 12B 的多模态网页智能体。每一步观察任务目标、当前 URL、accessibility tree，以及带 set-of-marks 编号标注的截图；观察历史截断为最近 3 步，但保留全部历史动作。动作空间是 6 个离散原语：click、type、scroll、go back、search（Google 或 Bing）、stop 并给答案。平台是桌面网页：WebArena 的自建站点（shopping、CMS、Reddit、GitLab、maps）和 WebVoyager 的真实网站。在 CUA Radar 板上，论文属于 trajectory-level policy training 主模式、子模式 K20：在自身轨迹上做稀疏终局奖励的 online RL。

论文先做了一组纯 prompting 实验（WebArena 的 62 个任务子集，3 次运行，测试上限 30 步）。“check-again”机制——智能体宣布完成后追加提示让它复查——把任务成功率从 23% 提到至少 28%；而把同等算力花在 budget forcing（“wait and think again”）或逐步 best-of-n 上，提升不足 3%。一次 check-again 的均值是 26.14，对比 CoT 基线 23.81，仅输出动作是 14.76。但反复 re-check 会让智能体把对的答案改错，所以只靠 prompting 不够。

TTI（Test-Time Interaction）转而训练这个视野（horizon）。它是 online filtered behavior cloning（filtered BC，属 online STaR / REINFORCE 一族）：在合成任务上采样 rollout，只保留 judge 判成功的轨迹，最大化其动作似然。核心设计是对 rollout horizon 的课程：h_i = clip(h_min · i, h_max)，h_min = 10、h_max = 30，消融显示乘性调度优于加性。成功轨迹进入按新旧加权的 replay buffer。训练任务由一个自由浏览网站、提出接地任务的探索型智能体按 PAE 方式合成：WebVoyager 用 128K 个真实网站域任务，WebArena 自建域用 11K 个，两个基准各训一个智能体。训练信号是 prompting 式 verifier（Gemma 3 27B，读动作历史和截图）给出的二值成败；它在 WebArena 上与 ground-truth evaluator 的一致率是 88.9%。每轮迭代采样 512 个任务（WebVoyager 12 轮、WebArena 10 轮），在 NVIDIA H100 上用 vLLM 采样、DeepSpeed Zero 3 训练。

## 论文报告的结果

以下全部是在线任务成功率（%）；评测用原始 benchmark evaluator（judge 只用于训练），评测 horizon 为 30 步。主表未报告随机种子与方差。表中后四行的基座一律是 Gemma 3 12B。

| 方法（WebVoyager，427 个任务） | 平均 SR  |
|--------------------------------|----------|
| PAE-LLaVa-34B（open data）     | 33.0     |
| Gemma 3 12B zero-shot          | 55.8     |
| Fixed h = 10（同基座）         | 59.1     |
| Fixed h = 30（同基座）         | 45.2     |
| **TTI（Gemma 3 12B）**         | **64.8** |
| UI-TARS-1.5（私有标注数据）    | 84.8     |
| Claude 3.7                     | 84.1     |
| OpenAI CUA                     | 87.0     |

| 方法（完整 WebArena，812 个任务）              | 平均 SR  |
|------------------------------------------------|----------|
| NNetnav（Llama 3.1 8B）                        | 7.2      |
| AutoWebGLM（ChatGLM3 6B）                      | 18.2     |
| Gemma 3 12B zero-shot                          | 18.3     |
| Fixed h = 30（同基座）                         | 19.0     |
| AgentTrek / Learn-by-Interact（Codestral 22B） | 22.4     |
| Fixed h = 10（同基座）                         | 23.8     |
| **TTI（Gemma 3 12B）**                         | **26.1** |
| IBM CUGA（闭源）                               | 61.7     |

论文表述：TTI 相对未微调智能体在 WebVoyager 上提升 9%、WebArena 上提升 8%（第 6.3 节写为 7.8）；在 WebVoyager 上比 fixed h = 10 高 5.7、比 fixed h = 30 高 19.6；在 13 个域中的 8 个取得最高分。论文没有离线的单步准确率数字。

## 论文自带的对照实验

**同基座固定视野。** 上述对比全部固定基座；固定短视野（h = 10）限制探索，固定长视野学习缓慢——h = 5 的智能体过拟合后提前终止，h = 20 的智能体早期把”乱点链接”与高奖励错误关联，多轮之后才恢复。

**预算对齐比较。** 以每条轨迹的 token 总数衡量算力，interaction scaling 的成功率曲线最陡；budget forcing 在 0.26 附近进入平台期，best-of-n 成本最高却提升最小。

**课程消融。** WebArena 子集训练 10 轮后：加性课程 29.50，乘性课程 32.25。TTI 还以少 40% 的训练步数比 fixed h = 20 高出近 3%。

**Verifier 校验。** 27B prompting verifier 与 WebArena ground-truth evaluator 的一致率为 88.9%，且只用于训练；评测一律用 benchmark 原生判定。

**训练动态。** TTI 下轨迹长度先降后升；GoBack 与 Bing 搜索占比上升；每步 token 数下降——智能体用更短的单步推理换来更多步交互，论文读作自适应探索。

## 论文自己承认的薄弱处

- 主表未报告种子与方差；prompting 与消融数字是 62 任务子集上 3 次运行的均值。
- 留出环境只是部分成立：radar 记录指出合成任务覆盖的”diverse real-world domains”包含了 WebVoyager 的基准网站本身。
- WebArena 增益更小，“possibly because: (1) WebArena tasks are more complex… (2) Agents occasionally attempt actions that are valid in real-world domains but invalid in WebArena counterparts.”
- 部分域出现回退：在 Amazon 和 GitHub 上，“TTI can engage in exploration behaviors such as initiating Bing searches or consulting external sites”，反而”exposes the agent to noisy or distracting information”。
- 失败模式：对 reset 的过度依赖（把 Bing 当万能退路），以及有限的自我验证——智能体能识别条件不符却仍然提交错误答案。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **online**。分数反映论文所报告的证据：在完整 WebVoyager 和 WebArena 上用原生 evaluator 的在线评测、同基座固定视野基线、token 预算对齐比较、成本报告、课程消融、88.9% 一致率的 verifier 校验，以及随数据一同发布的代码。记录同时标出方差未报告、留出环境仅部分成立，未标记任何 anti-pattern（AP5、AP8 已检查）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
