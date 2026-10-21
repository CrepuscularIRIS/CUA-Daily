# ReCAP：用自动生成的推理-动作数据与自我纠错训练，教会原生 GUI 智能体解 CAPTCHA

*CUA Radar 对 arXiv 2603.23559v2（Chen、Zhai、Wang、Yang、Zhang、Wang、Zhang；UIUC）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2603.23559v2 · 代码（论文中声明将开源）：https://github.com/ASTRAL-Group/ReCAP-Agent*

## 问题

现代 CAPTCHA 已从“难以辨认”转向“难以推理”：图片九宫格、滑块对齐、图标匹配、翻页选择，考验的是强噪声下的 OCR、细粒度视觉理解、精确的连续控制与多步交互。论文的出发点有两面。通用原生 GUI 智能体（OpenCUA、UI-TARS、Qwen3-VL）在日常 GUI 任务上很强，但用论文原话说，它们 “tend to underperform on CAPTCHA solving as they lack complementary skills”；论文还指出 “there is a lack of public and systematic research on studying CAPTCHA solving in native GUI agents”。另一边，Halligan、Oedipus 这类专用求解器能处理特定 CAPTCHA 家族，但把 CAPTCHA 当孤立问题，依赖反复模型调用、外部启发式或显式搜索，也不具备通用 GUI 能力。现有 CAPTCHA 资源（Open CaptchaWorld、MCA-Bench）面向评测而非闭环策略训练：没有可执行的 GUI 反馈、没有完整元监督、也没有失败恢复轨迹。

## ReCAP 是什么

**智能体。** ReCAP 是原生视觉-语言 GUI 智能体：在 Qwen3-VL-8B 与 Qwen3-VL-32B 的 Thinking 和 Instruct 两个变体上微调。它感知渲染页面的原始 screenshot，通过 Qwen3-VL 风格的 computer-use 工具调用行动（点击、拖拽、输入、按键、滚动、移动鼠标、等待、终止），坐标在 1000×1000 相对网格上表达，经 Playwright 派发到浏览器。一次回复可以包含多个动作（点输入框、输答案、提交）——在 CAPTCHA 限时下很关键。平台：训练与评测都在 web/浏览器环境。CUA Radar 板上它的架构模式是 C21（trajectory-level policy training：用强 MLLM 为示范轨迹合成推理标注，再 SFT 截图策略）。

**环境。** 一个动态 CAPTCHA 系统，含七种程序化生成的挑战类型——Text、Compact Text、Icon Match、Icon Selection、Paged、Slider、Image Grid——针对论文从部署系统（reCAPTCHA、Geetest、Arkose Labs、hCAPTCHA）中归纳出的四类交互原语：OCR、连续控制（拖拽）、空间定位（点击）、视觉语义理解。Flask 渲染引擎在每次请求时对布局与样式注入随机性，配合图标、图片、背景、扭曲文字素材库，使实例空间实际上无界。meta API 提供完整真值：答案标签、目标坐标、所需交互。

**机制与训练信号。** 两个数据生成器跑在环境之上。(1) 解答轨迹：专家推理模型（Qwen2.5-VL-72B-Instruct）拿到 CAPTCHA 截图、一个“当作不知道答案”的提示词，以及起约束作用的真值解与标注；它写出 observe/infer/plan 的思维链，自动检查确保推理没有直接泄露答案。论文称这一设置类似 STaR 的 rationale bootstrapping。(2) 自我纠错轨迹：学生模型先尝试；失败后，专家拿到完整失败上下文（前后截图与学生的推理-动作轨迹），写出纠错推理，仿佛自己发现了错误，实际隐式地被恢复真值引导。训练把推理与动作 token 交错在同一序列里，用统一损失对两组 token 重加权（λthink = λact = 0.5），避免长推理淹没短动作。

**训练语料。** 约 150,000 条解答轨迹与 10,000 条自我纠错轨迹，另混入约 50,000 条 Aguvis 与 23,000 条 AgentNet 的通用 GUI 轨迹以保持通用能力；约 230,000 个样本上做一轮全参数 SFT（4× B200，bf16，DeepSpeed ZeRO-2，lr 1e-5）。

## 论文报告的结果

以下 CAPTCHA 结果均为**在线、交互式**求解率：模型观察渲染帧、发出 GUI 动作、提交后获得二值成败反馈。动态基准用同一渲染引擎生成的固定 1,000 个留出实例（与训练不相交），5 步预算（Image Grid 与 Paged 为 8 步），论文未报告随机种子或方差。Halligan 因预算限制每类只评 100 个样本，且不设交互步数上限。

| 模型                   | 总体 SR (%) | 平均步数 |
|------------------------|-------------|----------|
| UI-TARS-1.5-7B         | 33.60       | 2.47     |
| Qwen3-VL-8B-Instruct   | 24.70       | 2.51     |
| Qwen3-VL-32B-Instruct  | 39.30       | 2.31     |
| OpenAI CUA             | 31.80       | 2.33     |
| GPT-5.4                | 56.80       | 2.23     |
| Gemini-3-Flash-Preview | 59.90       | 1.98     |
| Halligan framework     | 25.14       | ≥3–5     |
| ReCAP-8B (Thinking)    | 71.90       | 1.54     |
| ReCAP-32B (Thinking)   | 81.00       | 1.54     |
| ReCAP-8B (Instruct)    | 78.60       | 1.33     |
| ReCAP-32B (Instruct)   | **84.20**   | 1.38     |

ReCAP-32B (Instruct) 相对基座 Qwen3-VL-32B-Instruct 从 39.30% 提到 84.20%，Instruct 变体也优于对应的 Thinking 变体；论文还指出 ReCAP 平均只需 1.33 次模型调用（8B Instruct），低于列出的所有基线。

**真实世界迁移（仍是在线、zero-shot）。** 在 Halligan 基准的 26 类真实 CAPTCHA 上，ReCAP 未在该数据集上训练，而 Halligan 本就是为这些类型设计的：ReCAP-8B (Instruct) 与 ReCAP-32B (Instruct) 分别比对应 Qwen3-VL 基线平均高 14.50 pp 与 11.42 pp，且平均都略超 Halligan；ReCAP-32B (Thinking) 比基线平均高 12.58 pp，并在 26 类中的 25 类上胜出。前沿模型仍有竞争力：Gemini-3-Flash-Preview 在完整对比中平均分最高，Halligan 在部分旋转与模式识别类（如 baidu/rotate、geetest/iconcrush、yandex/kaleidoscope）上明显更强。

**通用 GUI 能力（离线协议，单独列出）。** 在 Android Control、ScreenSpot-V2、Multimodal-Mind2Web、UI-Vision 的官方离线协议下，32B 变体基本保持性能——ReCAP-32B (Instruct) 甚至把 UI-Vision Layout IoU 从 0.4843 提到 0.5566——而 8B 变体在部分 grounding 任务上下降（ScreenSpot-V2：8B Instruct 对 89.54 vs 91.12；UI-Vision Element：22.05 vs 29.72）。

## 论文自带的对照实验

- **CoT 消融**（同基座同数据，仅去掉推理轨迹）：总体 SR 从 71.90 降到 66.40，平均步数基本不变（1.61 → 1.54）。
- **自我纠错消融**：去掉 1 万条纠错轨迹后，总体 SR 从 71.90 降到 62.90；论文报告分类增益为 Text +16.77pp、Slider +21.9pp、Compact Text +7.50pp、Icon Match +8.77pp、Paged +3.65pp、Image Grid +2.19pp。
- **数据规模扫描**：CAPTCHA 数据取 50% / 100% / 150% 时总体 SR 为 62.90 / 71.90 / 72.20——接近最终规模后增益饱和。
- **模型容量**：额外用 Qwen3-VL-4B-Thinking 做的实验在 ScreenSpot-V2 上出现更大的相对下降（相对基线 21.15%），支持论文对 8B 退化的容量解释。
- **留出设计**：动态测试集与训练数据不相交；真实世界基准对 ReCAP 是 zero-shot，而 Halligan 专为其设计，且 Halligan 数字来自其发布框架在同一协议下的运行。

## 论文自己承认的薄弱处

- “Our strongest empirical claim is therefore specific to the held-out dynamic CAPTCHA benchmark, while real-world transfer remains mixed.”
- “There remains a gap between these simulations and the messy, unpredictable real world”（合成训练数据）。
- “Our reasoning traces are answer-conditioned and should be interpreted as scalable training supervision rather than verified faithful explanations.”
- 未模拟行为生物特征（鼠标速度、犹豫等）；与 Oedipus 的对比、完整的延迟分解、推理/动作损失权重扫描留给未来工作。
- 所有评测均未报告种子或方差；与 Halligan 的对比受预算限制（每类 100 样本、无步数上限）。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **64 分（★★）**，证据等级 **transfer**。分数反映论文报告的证据：交互式在线评测、留出环境、包括专用框架在内的强基线、成本报告、两个组件消融，以及声明将开源的代码；判定记录把 variance 标为 unclear、Halligan 的预算对齐标为 partial，并标注 CoT 监督是真值条件的（answer-conditioned）。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v2）。
