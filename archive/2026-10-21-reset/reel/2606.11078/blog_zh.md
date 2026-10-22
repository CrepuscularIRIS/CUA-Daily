# HiViG：在 computer use agent 动手之前，先检查像素、再回顾历史的 critic

*CUA Radar 对 arXiv 2606.11078v1（Lee、Khan、Prasad、Chen、Chakraborty、Balasubramaniam、Sahu、Stengel-Eskin、Lee、Bansal）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2606.11078v1 · 代码：https://github.com/G-JWLee/HiViG*

## 问题：只读意图、不看屏幕的 critic

Computer Use Agent（CUA）靠看截图、发像素级动作来操作图形界面，也会犯错：点错元素、点击不存在的 UI、反复重探已经查过的文件夹。论文指出，许多 GUI 动作不可逆（发邮件、删文件），出错后再纠正往往不安全，因此需要在执行前介入。现有介入方式有两类：标量 process reward model 给候选动作打分，但当所有候选都差时，分数给不出改进方向；verbal critic 用自然语言解释失败，但正如论文所说，现有 critic “focus primarily on short-sighted decision loops”，且 “lack the visual grounding needed to detect flawed actions”——它们相信策略口述的意图，从不核对动作真正落点的坐标。

## HiViG 是什么

HiViG（History-aware Visually Grounded）是一个 test-time 框架：冻结的策略外面套一个训练出来的小 critic。策略用 Qwen3-VL-32B-Thinking（开源）和 Gemini-3-Flash（前沿闭源）两个；感知只有原始截图，不用 DOM、不用无障碍树；动作是结构化 JSON 像素调用（click、type、scroll、swipe 等），坐标归一化到 1000×1000 网格，覆盖 web、移动、桌面。在 CUA Radar 板上这属于 C18 模式：校验动作结果并把结论反馈回环路——这里把校验挪到了执行之前。

critic 是 HiViG-critic：以 Qwen3-VL-8B-Thinking 初始化，在 52k 样本上微调 1 个 epoch，由 Qwen3-VL-32B-Thinking 标注器从开源 ScaleCUA 轨迹语料蒸馏而来（20k 历史状态跟踪 + 32k 视觉接地错误分析，后者含 16k 专家动作、16k 按 12 类错误 taxonomy 扰动出的动作）。测试时它每步做两件事：

1.  **Macro-action history。** 策略规划前，critic 对前后两张截图做视觉 diff，把已完成和已失败的事项压缩成一份滚动更新的宏观动作历史，供策略参考；训练信号来自源语料中经过验证的真实执行结果，而非标注器的想象。
2.  **Visually grounded error analysis。** 策略提出动作后，在截图上按提议坐标画一个红色 X 标记；critic 识别标记下方的 UI 元素、预测视觉状态转移、对照指令判断对齐，给出 Good（执行）或 Bad（错误维度 + 纠正性解释，策略在执行前改写动作）。

两个训练细节被消融验证很重要：30% 样本遮蔽策略的文字意图以打破文本依赖；标注器拿到的是从真实执行元组导出的真值 state-transition，而不是让它自己想象后果。

## 论文报告的结果

以下均为执行判定的任务成功率（%），在线评测，每格单次运行（论文明确写道所有结果都是单次运行，算力所限；没有种子数和方差）。基准：WebArenaLitev2（154 个 web 任务，15 步上限）、AndroidLab（138 个任务、9 个 Android 应用）、WindowsAgentArena（145 个 Windows 11 任务，30 步上限）。

以 Gemini-3-Flash 为策略（成功率 %）：

| 方法                    | WALv2    | ALab     | WAA      | 平均     |
|-------------------------|----------|----------|----------|----------|
| Base agent              | 30.5     | 58.0     | 35.8     | 41.4     |
| OpenCUA（标量 PRM）     | 29.9     | 57.2     | 35.8     | 41.0     |
| SE-WSM（标量 PRM）      | 30.5     | 57.2     | 35.1     | 40.9     |
| CGI（32B，verbal）      | 29.9     | 55.8     | 37.9     | 41.2     |
| GUI-Critic-R1（verbal） | 22.1     | 53.6     | 32.5     | 36.1     |
| **HiViG**               | **45.5** | **61.6** | **44.2** | **50.4** |

以 Qwen3-VL-32B-Thinking 为策略时，HiViG 为 25.3 / 51.5 / 38.0（平均 38.3），base agent 为 13.0 / 44.2 / 35.7（平均 31.0）。论文的头条数字：Gemini-3-Flash 在 WebArenaLitev2 上从 30.5% 提到 45.5%，提升 15.0 个点；相对最强基线的平均提升为 5.8（Qwen3-VL-32B）和 9.0（Gemini-3-Flash）个点。论文没有离线单步准确率数字，以上全部是在线结果。类目级跳变最大的是：Qwen3-VL-32B 在 WebArenaLitev2 的 Map 类从 3.9% 到 23.1%，Gemini-3-Flash 在 WindowsAgentArena 的 Office 类从 4.7% 到 23.3%。

## 论文自带的对照实验

**组件消融（WebArenaLitev2）。** 两组件都不用：Gemini-3-Flash 30.0、Qwen3-VL-32B 13.5；只用视觉接地错误分析：35.1 和 21.4；只用历史跟踪：42.9 和 23.4；两者都用：45.5 和 25.3。任一组件单独使用即超过全部基线；而且完整流程每步需要两次 critic 推理，单用任一能力的一次推理就已经能带来提升。

**基线对齐。** 标量 PRM 基线（OpenCUA、SE-WSM）用与 critic 相同的 Qwen3-VL-8B-Thinking 骨干，N=2 对齐 verbal 框架的计算成本。标量反馈相对 base agent 没有提升；各基线介入对 Gemini-3-Flash 最好只加 2.1 个点（WindowsAgentArena），最差掉 8.4 个点（WebArenaLitev2）。GUI-Critic-R1 在 AndroidLab 加 5.1，在 WebArenaLitev2 只加 0.6，在 WindowsAgentArena 掉 1.3。

**训练数据消融。** 训练时去掉视觉标记，WebArenaLitev2 从 25.3% 掉到 20.8%（MLLM 很难直接读懂原始数值坐标）；去掉意图遮蔽，AndroidLab 从 51.5% 掉到 47.1%。不给标注器真值 state-transition，WebArenaLitev2 也掉到 20.8%。混合训练的单个 8B critic（25.3）好于两个分开训练的 8B critic（23.4），并与 zero-shot 的 Qwen3-VL-32B 历史提供者打平。任务级重叠分析报告：9 个任务只有历史跟踪能修、7 个只有错误分析能修、6 个两者都能修、4 个只有组合才能修。

**成本。** 训练在 8 张 H100-80GB 上约 4 小时；评测也用 8 张 H100。历史窗口 W：Qwen 策略为 4，Gemini 为 2。

## 论文自己承认的薄弱处

- “All experimental results are from a single run, due to heavy compute costs for long-horizon GUI tasks”——单次运行、无方差，而若干基准间的差距只有几个点。
- critic 自身的准确率从未对照真值测量：论文没有报告 Good/Bad 判定的精确率/召回率，引导信号的质量只能由端到端任务成功率间接推断。
- 评测环境是否与 critic 的训练语料（覆盖 web、移动、桌面的 ScaleCUA 轨迹）保持留出，论文没有明说；WebArenaLitev2 正是 ScaleCUA 同一论文提出的。
- 论文报告的失败案例：critic 分不清 Windows Paint 里 “dark red” 与 “red” 的色差；macro-action history 曾把”仅被隐藏、未删除”的闹钟记成已删除。
- 作者自己的局限说明：12 类错误 taxonomy “remains bounded by the current landscape of digital interfaces”。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **63 分（★★）**，证据等级 **transfer**。分数反映论文所报告的证据：跨 web、移动、桌面的执行判定在线评测、同 8B 骨干且成本对齐的标量与 verbal 基线、组件与训练数据消融、成本报告。判定记录同时标出缺失项：单次运行无方差、评测环境是否留出不清楚、critic 判定未经验证、代码链接未核实。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v1）。
