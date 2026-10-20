# VLAA-GUI：说“完成”前先核验、卡住时逐级升级、迷路时去查资料的提示词桌面智能体

*CUA Radar 对 arXiv 2604.21375v3（Han、Tu、Wang、Dai、Zhou、Lau、Cardenas、Xu、Xu、Xiong、Zheng、Yao、Zhou、Xie）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2604.21375v3 · 代码：https://github.com/UCSC-VLAA/VLAA-GUI*

## 问题：过早停止，以及原地打转

论文指出桌面 GUI 智能体有两类失败。其一是过早停止（early stopping）：智能体在“没有可验证证据”的情况下宣布成功，比如切换了某个设置却没确认状态真的变了。现有的 planner 通过生成的子任务来跟踪进度，但“完成计划中的步骤并不保证用户的要求已被满足”。其二是重复循环（repetitive loops）：现有的防循环启发式通常只检测局部重复，当智能体持续卡住时没有办法逐级升级恢复手段。此外，智能体在不熟悉的应用流程上也容易停滞：截图能显示界面，却不显示操作步骤。

## VLAA-GUI 是什么

VLAA-GUI 是围绕一个 **Manager** 智能体搭建的模块化框架，Manager 在 perceive-reason-act 循环中工作。它看到的是截图（1920×1080）加上任务、历史和工具返回结果；动作是通过 `pyautogui` 发出的 GUI 原语（click、type、scroll、hotkey、drag、打开应用），或者调用某个工具，原语和工具在同一个动作空间里。评测平台是 Linux 桌面（OSWorld）和 Windows（WindowsAgentArena，WAA）。在 CUA Radar 板上，这篇论文属于模式 C18：“核验每个动作的结果并把结论反馈回去”。整个系统不做训练：Manager、reflection agent、judge 和 coder 都是被提示词驱动的前沿模型，提示词在附录中完整给出。

机制由五部分组成，两个必选、三个按需：

1.  **Completeness-Aware Planner（CAP，必选）。** 其中的 *Completion Gate* 根据指令推导出 K 条可在界面上观察到的成功标准，并在每一步重新检查证据，使用针对具体动作的规则。只有所有标准都通过且界面稳定，才输出 DONE。gate 输出 DONE 后，一个独立的 *Completeness Model Judge*（温度 0.2）会重新阅读指令、当前屏幕和最近轨迹。终止需要两者一致；若被驳回，缺失证据的反馈会回到 Manager。
2.  **Loop Breaker（必选）。** 每个动作之后都运行。Tier 1：同一目标上的同一动作两次都没有可见变化，必须切换交互方式。Tier 2：同一屏幕状态出现三次，必须整体更换策略。Tier 3：外部 reflection agent 返回 keep 或 switch，switch 时把重复的动作加入黑名单。阈值在所有任务和两个基准上固定不变。
3.  **Search Agent（按需）。** Manager 向带搜索 grounding 的 LLM（Gemini 3 Pro 或 3.1 Pro）发出一次“How to”查询，得到纯文本教程，不必在浏览器里导航。
4.  **Coding Agent（按需）：** 运行 Python 或 Bash，自带 20 个代码执行步的独立预算。
5.  **Grounding Agent（按需）：** 定位屏幕元素（默认 Seed 1.8，一个变体用 MAI-UI）。

## 论文报告的结果

以下均为在线成功率（%），基准为 OSWorld-Verified（361 个任务，Ubuntu）或 WAA（154 个任务，Windows）。论文在主表中没有报告随机种子或置信区间。基线行来自 OSWorld 榜单（OS-Symphony 的 100 步来自其论文），基座各不相同，因此只是参照点，而不是同模型对比。

**OSWorld-Verified，按步数预算（Table 1，平均列）：**

| 方法                       | 15 步 | 50 步 | 100 步 |
|----------------------------|-------|-------|--------|
| VLAA-GUI w/ Gemini 3 Flash | 43.15 | 63.14 | 68.77  |
| VLAA-GUI w/ Sonnet 4.6     | 64.13 | 71.11 | 71.67  |
| VLAA-GUI w/ Opus 4.6       | 64.75 | 73.85 | 77.45  |
| OS-Symphony w/ GPT-5       | –     | 65.77 | 65.84  |
| HIPPO w/ Opus 4.5          | –     | –     | 74.49  |

在 100 步时，论文还报告了 VLAA-GUI 搭配 Gemini 3.1 Pro 为 72.47，搭配 Opus 4.5 为 74.89，搭配 Opus 4.5 加 MAI-UI grounder 为 76.26；对比 Agent S3 w/ Opus 4.5 为 66.00。人类参考水平为 72.4；论文认为有三个基座在 100 步时超过了它。

**WindowsAgentArena（Table 3，Overall）：**

| 方法                                  | 50 步 | 100 步 |
|---------------------------------------|-------|--------|
| VLAA-GUI（Gemini 3 Flash 作 Manager） | 60.4  | 61.0   |
| Agent S3 w/ GPT-5                     | 54.1  | 56.6   |
| GTA1-32B w/ o3                        | –     | 51.2   |

## 论文自带的对照实验

**同基座对照。** 在作者自己的 harness 下，Sonnet 4.6 的基础脚手架（含 coder 和 grounder）得分 69.19，完整框架为 71.67，二者的基座、grounding、动作接口和预算都相同。论文把它表述为 2.48 的提升。

**OSWorld 上的组件消融（Table 2）。** Sonnet 4.6、100 步：完整 71.67，去掉 CAP 为 68.81，去掉 Search 为 70.04，去掉 Loop Breaker 为 71.63。论文的读法是：CAP -2.86，Search -1.63，Loop Breaker -0.04。Gemini 3 Flash、100 步：完整 68.77，去掉 CAP 为 67.34，去掉 Loop Breaker 为 66.95，去掉 Search 为 65.82。论文自己说，结果“支持的是依赖配置的收益，而不是每个模块总能提升性能”。

**并非总是正收益。** 50 步时 Gemini 3 Flash 去掉 CAP 为 66.00，带 CAP 为 63.14。附录中，在 15 步时 CAP 和 Search 会拉低 Flash 的得分（论文给出 -11.3 和 -9.7），Loop Breaker 则把它从 49.30 拉到 43.15，原因是在很小的预算下，工具调用和升级动作会占用步数。Sonnet 4.6 在各个预算下都从 CAP 和 Search 获益。

**WAA 消融（Table 3）。** 100 步时完整系统为 61.0；去掉 CAP 为 51.3，去掉 Loop Breaker 为 55.8，去掉 Search 为 53.9。

**错误完成。** Sonnet 4.6、100 步：CAP 把 false DONE 的数量从 105 降到 91，把失败任务中以错误完成告终的比例从 95.5 降到 91.9。Gemini 3 Flash 的数量从 102 降到 100（91.9 降到 86.2）。论文的总结是：“大多数失败任务仍然以错误的完成声明结束”，因此 CAP “只是部分解决了错误完成”。

**循环。** 对 Gemini 3 Flash，Loop Breaker 把浪费步数比例从 4.9 降到 2.8，失败任务中的循环占比从 20.7 降到 16.2。Flash 的循环频率约为 Sonnet 的两倍（占全部任务的 10.6 对 5.0）。

**迁移到 CoAct-1。** 在固定的 60 任务 OSWorld 子集上（Gemini 3 Flash，100 步），CoAct-1 为 65.13。加 CAP 为 68.91，加 Loop Breaker 为 66.06，加 Search 为 65.96，三者全加为 70.34。

## 论文自己承认的薄弱处

- 60 任务子集是“非随机”的，只提供“受控的点估计，而不是总体层面或统计显著的结论”；没有给出置信区间。
- Loop 的阈值是“手工设计”的，“尚未做敏感性扫描”；Sonnet 在 100 步时只有 0.04 的收益，说明恢复机制对容易循环的智能体帮助最大。
- 所有被评测的 Manager 基座都是闭源模型，附加实验的 coder 和 searcher 也是闭源的 Gemini 3.1 Pro。搜索结果和模型版本会随时间变化。
- 追踪到的成本只是“下界”；CAP 把每个任务的平均动作数从 16.80 提高到 27.32，固定动作预算下的得分不等于成本效率。
- Table 1 中 HIPPO w/ Opus 4.5（74.49）和 Kimi K2.6（73.07）在 100 步时也高于 72.4 的人类参考水平，而正文称 VLAA-GUI 是首个超过它的 GUI 框架。各基线的基座和工具不同，比较时应谨慎。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **73 分（★★★）**，证据等级 **transfer**，模式 C18。判定记录把在线评测、第二个环境（WAA）、同基座对照、三档步数预算、组件消融以及对错误完成判定器的检验列为已有；随机种子或方差、成本和代码则记录为未确认。（作为参考：论文附录确实给出了 60 任务子集的追踪成本下界，首页也链接了代码仓库。）判定记录标出了一个失败案例：在 50 步时验证模块降低了 Gemini 3 Flash 的得分。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v3）。
