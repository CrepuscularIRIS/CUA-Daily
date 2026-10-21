# PEEU：先让网页智能体自主探索，再用 hindsight 把轨迹重新标注成高层任务

*CUA Radar 对 arXiv 2606.27330v1（Men、Jin、Cao、Chen、Liu、Zhao；中科院自动化所 / 国科大）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2606.27330v1 · 论文未列出代码仓库。*

## 问题：小模型该用什么任务来训练？

小型开源多模态 LLM 便宜且利于隐私，但论文原话说 “they suffer from weak planning and limited cross-website generalization”。论文批评了两类常见的数据构造方式。Atomic task 方法通过对比动作前后的截图抽取 click / type / scroll 这类原子技能，但掌握了原子技能是否就能组合出任务规划，恰恰是悬而未决的问题；Coarse task 方法直接把探索任务当作训练标签，与实际采到的轨迹配对——论文的例子是任务要求 4.5 星以上的食谱，轨迹却只到 4 星：标签与轨迹错位，约束也偏弱，因为首页不可能知道网站里到底有什么（“such as ingredients and preparation directions”）。

## PEEU 是什么

这是一个在 Chrome 中运行于真实桌面网站上的视觉网页智能体。每一步它看到带 Set-of-Mark 编号的截图和页面文本，动作空间沿用 WebVoyager：点击编号元素、输入、滚动、等待、后退、跳转 Google、作答。它在 CUA Radar 板上的架构模式是 K14：用 hindsight（事后推断的指令）重新标注探索轨迹，属于 exploration-driven task synthesis 下的 HER 类比。

PEEU（planning experience exploration and utilization）是围绕这个智能体的数据管线，分两个阶段；用户只需要给一个 URL。

1.  **Planning tree exploration。** 探索模型（GPT-4o）读首页，生成贴合网站功能的任务列表（任务设定 prompt 要求 50 个任务），随后以每任务最多 15 步执行，长出一棵以首页为公共根节点的有向探索树。
2.  **Planning experience utilization。** GPT-4o 对比每个动作前后的状态，抽取原子经验；一条轨迹的经验串成序列，再由聚合步骤融合成一个新的 PEEU 任务——该任务被这条轨迹真实满足，与实际结果对齐，并带上只有探索才能发现的约束（例如：食谱需包含食材、做法和 4 星以上的图片）。

重标注后的（任务， 轨迹）对用来训练策略——输入当前状态、历史、任务描述，输出一个动作——基座为 Qwen2.5-VL-3B-Instruct 或 Qwen2.5-VL-7B-Instruct：SFT（batch size 16、学习率 5.0e-6、5 个 epoch、llama-factory）与 GRPO（batch size 20、学习率 1.0e-6、rollout size 10、7 个 epoch、verl）。GRPO 奖励是格式奖励加答案正确性奖励，各 1.0，合计 2.0。所有实验在 4 张 A800 上完成。

论文还提出 TDHAF 分析框架：把任务切成 low / mid / high 三个粒度，考察自底向上、自顶向下和跨域三种泛化，数据来自 Multimodal-Mind2Web，用离线指标衡量（元素编号、动作类型、动作参数，以及单步完全匹配的 Step SR；训练集 616、测试集 684 个样本）。

## 论文报告的结果

主表是**在线**结果：WebVoyager，轨迹级成功率，真实网站，每格一次运行，未报告随机种子或标准差，所有训练方法使用相同轨迹规模。论文的标题结论：7B + 2k 轨迹时，PEEU-SFT 总体达到 30.6%，高于 Coarse-SFT 的 19.0%、Atomic-SFT 的 21.7%，也高于大得多的 Qwen2.5-VL-32B Instruct 的 22.7%。

| 方法（Qwen2.5-VL-7B）                     | 0.1k 轨迹 | 2k 轨迹 |
|-------------------------------------------|-----------|---------|
| Vanilla（不训练）                         | 7.8       | 7.8     |
| Atomic-Prompt / Trajectory-Prompt（检索） | 3.7       | —       |
| Coarse-SFT                                | 4.8       | 19.0    |
| Atomic-SFT                                | 12.3      | 21.7    |
| PEEU-SFT                                  | 15.6      | 30.6    |

| 方法（Qwen2.5-VL-3B） | 0.1k 轨迹 | 2k 轨迹 |
|-----------------------|-----------|---------|
| Vanilla（不训练）     | 0.2       | 0.2     |
| Coarse-SFT            | 2.0       | 13.2    |
| Atomic-SFT            | 4.8       | 16.7    |
| PEEU-SFT              | 5.7       | 19.8    |

0.1k 轨迹下用 GRPO：7B 的 PEEU-GRPO 为 19.9，对比 Atomic-GRPO 10.0、Coarse-GRPO 11.5；3B 为 11.1，对比 5.5 与 5.6。同一张表还给出参照：GPT-4o vanilla 59.0，Claude 3 Opus 56.1，Qwen2.5-VL-72B vanilla 29.3。7B / 2k 的 PEEU-SFT 在域内 Allrecipes 一列为 17.7，在七个未见网站上依次为 53.6、16.2、25.2、19.5、35.7、48.7、28.2（Amazon、Apple、Arxiv、Github、Coursera、Map、Wolfram）。

TDHAF 的数字是**离线**的，这里单独列出。域内：7B 用 low 级任务训练后在 low 级测试 Step SR 为 89.6，在 high 级只有 18.8；用 high 级训练则在 low / mid / high 上分别为 83.1、63.6、72.1。跨域 coverage（三个粒度全对）7B 高粒度训练为 37.8、低粒度 25.7；3B 为 33.8 对 18.9。

## 论文自带的对照实验

- **数据规模对齐。**”All methods are controlled to use the same amount of data to ensure a fair comparison”，轨迹规模与训练参数一致。7B / 2k 下 Coarse-SFT 19.0 对 PEEU-SFT 30.6：轨迹固定，只改任务标签——这是支持 hindsight 重标注最干净的一组证据。
- **留出环境。**”We test on seven additional websites that were entirely excluded from the training data”，且 2k 补充池的网站也与这七个测试站不同。
- **检索替代不了训练。** 给小模型提示检索到的经验，7B 上两个 prompt 基线都只有 3.7，低于不训练的 7.8；3B 的 prompt 方法全为 0.0。
- **粒度研究本身是机制检验。** 高粒度训练向下、跨站的泛化都好于低粒度训练，这正是论文解释”为什么重标注的高层任务有效、原子任务无效”的依据。

## 论文自己承认的薄弱处

- 没有方差报告：“Overall is the average accuracy of all websites”——无种子、无置信区间、每格一次运行。
- 未描述对任何学习到的 judge / reward model 的验证，也未列出代码发布。
- 场景覆盖：“we did not include scenarios involving sensitive operations such as user login, CAPTCHA solving, or actual payment transactions.”
- 2k 探索数据在正文里是 “2k trajectories from a previously unseen website”（单数），附录里则是 “approximately 2,000 tasks collected from additional websites”（复数），具体网站从未列出。
- 探索、经验抽取与聚合全部依赖 GPT-4o；论文没有对探索器做消融，也没有报告美元或 token 成本。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **61 分（★★）**，证据等级 **transfer**，子模式 K14（exploration-driven task synthesis 下的 hindsight 重标注）。判定记录认可的：WebVoyager 在线评测、七个留出网站、数据规模对齐的基线、粒度消融，以及部分预算与成本报告（相同轨迹规模、4 张 A800）。标记为缺失的：variance（未报告）、validator 检查与代码（unclear），并标出未覆盖敏感操作场景。CUA Radar 没有复现任何实验；本文所有数字均来自论文 v1 版。
