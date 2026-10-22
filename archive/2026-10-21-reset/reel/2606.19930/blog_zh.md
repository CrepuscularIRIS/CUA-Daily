# MobileForge：探索 App、自我批评、带提示训练——一条免标注的移动 GUI 智能体适配流水线

*CUA Radar 对 arXiv 2606.19930v2（Liu、Zhao、Wu、Yin、Li 等；浙江大学、快手、清华大学）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2606.19930v2 · 代码（已宣布开源）：https://github.com/kwai/MobileForge*

## 问题：不靠标注适配目标 App

移动 App 数量多、更新快，用人工任务、示范或奖励标签去覆盖它们成本极高。论文把目标设定为 annotation-free adaptation（免标注适配）：智能体自己探索目标 App、尝试有依据的任务、评估自身行为、从自采经验中学习。论文对现有工作的批评有两点：一是缺少一个把目标 App 探索、课程挖掘、rollout 执行和反馈连起来的统一基底（substrate），生成的任务与评估反馈容易脱离策略学习；二是策略优化常把 rollout 当作孤立经验、只配稀疏的轨迹级奖励——失败轨迹里正确的局部步骤被整段丢弃，诊断出的错误也不会传给下一次尝试。

## MobileForge 是什么

这是一个运行在 Android 上的 MLLM 移动 GUI 智能体。每一步它观察截图与交互历史（适配期间还加上同一任务此前尝试的纠正提示 hint），输出一个结构化动作（click、long_press、swipe、type、answer、system_button、wait、terminate；GUI-Owl 动作空间另有 open 和 key）。论文研究两个 8B 基座：开源通用模型 Qwen3-VL-8B-Instruct 与 GUI 专用模型 GUI-Owl-1.5-8B-Instruct，适配后的模型分别叫 ForgeQwen3-8B 和 ForgeOwl-8B。在 CUA Radar 板上，这篇论文属于 K19 子模式——多轮 GUI RL 的密集步级过程奖励，隶属”learned outcome and process judges”主干。

系统由两部分组成。**MobileGym** 是交互与评估基底。Function-aware exploration（受 GUI-explorer 启发）遍历目标 App：APK 的 activity 锚点和截图引导目标生成，深度优先遍历把可达屏幕与转移记录进证据池 Z。MobileGym-Curriculum 把 Z 转成可执行任务，每个任务带指令、预估步数预算、核心功能、变体类型和前置条件；完整任务池包含来自 20 个 AndroidWorld App、527 条源轨迹的 3,249 个候选任务，训练使用 200/400/900 任务子集。MobileGym-Critic 以可视化动作轨迹审视每次完成的尝试，返回层级反馈：轨迹级结果标签 z、每步的过程标签（合理步标记加理由）、以及纠正提示 h。**HiFPO** 是训练配方。每个任务串行跑 K 次尝试，第 k 次只复用第 1..k−1 次的提示。全部成功的任务被剔除；其余任务选合理步比例最高的一次成功尝试（无成功则选最高的一次），只保留其中被标记为合理的步骤。每个保留步骤加上提示上下文构成 prompt，策略采样 G = 5 个候选动作，按规则奖励打分（动作类型匹配 0.2、参数匹配 0.8），做组内归一化得到相对优势——即 hint-contextualized 的步级 GRPO，并对参考策略加 KL 正则。全程没有人工任务、示范或奖励标签；监督信号完全来自 critic 的结果标签、步级标签与提示（默认终审模型 Gemini-2.5-Pro，步骤描述由 Qwen3-VL-8B 生成）。

## 论文报告的结果

以下全部是在线评测。AndroidWorld（116 任务）为 in-domain：适配数据就在此挖掘。MobileWorld GUI-only（117 任务）为 out-of-domain：适配不使用任何 MobileWorld 的 rollout、任务或反馈。Pass@k 按 116 个 AndroidWorld 任务统计；MobileWorld 报告单次尝试成功率。论文未报告随机种子数与方差。900 任务的 8B 训练在 8×80GB GPU 上约需 80 小时。

| 8B 模型                   | AW Pass@1 | AW Pass@3 | MW GUI-only SR |
|---------------------------|-----------|-----------|----------------|
| Qwen3-VL-8B（基座）       | 40.5%     | 55.2%     | 7.7%           |
| ForgeQwen3-8B（900 任务） | 50.9%     | 67.2%     | 10.3%          |
| GUI-Owl-1.5-8B（基座）    | 56.0%     | 69.0%     | 37.6%          |
| ForgeOwl-8B（900 任务）   | 67.2%     | 77.6%     | 41.0%          |

免标注适配让通用模型接近闭源数据训练的 GUI 专用基座（Pass@3 67.2% 对 69.0%），并进一步提升了专用模型（Pass@3 77.6%；困难任务 Pass@1 从 19.3% 升到 29.8%）。MobileWorld 上，ForgeOwl-8B 的 41.0% 领先所有受测的开源数据智能体（OpenMobile-8B 17.7%、ClawGUI-2B 17.1%、OpenMobile-7B 14.8%），接近更大或闭源数据的系统（GUI-Owl-1.5-32B 43.9%、MAI-UI-235B-A22B 39.7%）。ForgeQwen3-8B 的迁移要弱得多，只有 10.3%——论文自己也指出，域外泛化”仍然强烈依赖基座的移动 GUI 能力”。论文没有离线的步级准确率或 grounding 数字，两个基准都在线。

## 论文自带的对照实验

**提示的作用。** 200 任务、Qwen 基座下，给重复 rollout 加纠正提示把整体 rollout 成功率从 52.0% 提到 77.0%，Pass@3 从 49.0% 到 72.5%，平均每步尝试数从 18.4 降到 17.2——提升来自反馈积累而非更多采样。在匹配的 HiFPO 训练下，去掉提示会让两个基座同时退化（Qwen 基座 AW Pass@1 55 → 49；GUI-Owl 基座 75 → 71），MobileWorld 成功数也下降。

**训练目标。** 同一批生成数据上，200 任务的 no-hint SFT 掉到基座之下（Pass@1 34.5% 对 40.5%）；hint SFT 45.7%，hint GRPO 47.4%；900 任务时 GRPO 仍最强，50.9%。

**过滤规则。** 保留全败加混合任务（成功率区间 \[0.0, 0.9)）给出最好的 AndroidWorld（48.3%）加 MobileWorld（15/117）组合——该删的是已掌握的任务，不是失败任务。

**Critic。** 相对参考标签、400 条轨迹上，Gemini 配置达到 89.75% 轨迹、86.53% 步级准确率（F1 91.40% 与 89.35%）；全 Qwen critic 为 77.00% 与 71.37%，仍能让策略提升（AW Pass@1/2/3 52/67/70，MW 11/117），说明增益不依赖闭源评估器。

**课程接地。** 在 Broccoli App 上，仅从落地页生成会把 27.3% 的任务堆在食谱删除上；轨迹接地的课程把覆盖摊到购物清单、烹饪助手、膳食规划、设置等落地页基线完全未触及的功能。

## 论文自己承认的薄弱处

- 未报告种子与方差；每个配置单次运行。
- MobileWorld 的外部对比数字”遵循 GUI-only 报告协议”，并非在匹配预算下重跑；与这些基线的预算对齐未给出。
- 适配数据在 AndroidWorld（即 in-domain 基准）上挖掘，域内增益包含对受测 App 的暴露；MobileWorld 迁移是论文对此的回应。
- “训练仍局限于 AndroidWorld 侧的 App，更广覆盖、长程多 App 工作流、持久用户状态与非常规任务规则仍然困难。”
- 代码、数据与模型为”将发布”（will be released），评审时尚未落地。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **transfer**，子模式 K19（learned outcome and process judges 主干下）。判定记录认可：在线评测、真正留出的环境（MobileWorld）、组件消融、以及与参考标签对照验证过的 critic；同时把方差与预算对齐记为 unclear，外部基线记为 partial，代码记为 announced，并标注反模式 AP5——合成/探索数据与评测环境重叠。CUA Radar 未复现任何实验，本文所有数字均来自论文（版本 v2）。
