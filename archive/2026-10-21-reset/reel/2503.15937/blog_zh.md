# V-Droid：用「验证候选动作」取代「生成动作」的手机 GUI 智能体

*CUA Radar 对 arXiv 2503.15937v5（Dai、Jiang、Cao、Li、Yang、Tan、Li、Qiu；MobiCom ’26）的解读。本文是第三方对论文所报告内容的整理，并非作者背书。海报见 `poster.png`。论文：https://arxiv.org/abs/2503.15937v5 · 代码：https://github.com/V-Droid-Agent/V-Droid*

## 问题：生成又慢又容易错

大多数手机 GUI 智能体把 LLM 当作生成器（generator）：每一步模型读屏后自回归地解码出决策，往往还要叠加 Chain-of-Thought。论文在 AndroidWorld 上报告了两个后果：现有智能体的最高成功率只有 54.3%，“significantly lower than the human performance of 80%”（人类为 80%）；延迟也不理想——由 GPT-4o 和 UI-TARS-72B 驱动的 Agent-S2 “takes over 25 seconds for a single step”（单步超过 25 秒），多数现有智能体每步需要 10 秒以上。提示工程和 GUI 微调能提升指令遵循，但用论文的话说，“fail to adequately address task-specific, multi-step decision-making challenges”（未能解决任务特定的多步决策问题）。

## V-Droid 是什么

**智能体本体。** V-Droid 是一个纯文本（text-only）的 Android 手机 GUI 任务自动化智能体。感知侧：通过 Android Accessibility Service 提取的 XML 界面描述（当前设计不用截图），外加记录历史步骤的 working memory；动作侧：离散操作——click、long-press、scroll、type text、clear text——通过 Android 命令（ADB）执行，并补充界面上不可见的默认动作：open app、wait、navigate home、navigate back、complete task、answer user。它在 CUA Radar 板上的架构模式是 K02：用训练好的 verifier 对枚举出的候选动作重排序（rerank），取最高分执行，不做下一状态仿真。

**机制。** 模型不生成动作，而是由微调过的 Llama-3.1-8B-Instruct（4-bit）verifier 给每个抽取出的候选打分：每个动作包进一个提示（“Is the action X helpful for completing the given user task?”，模型只许回答 Yes 或 No），分数直接读 “Yes” 首 token 的概率。整个过程只做 prefill、不做自回归解码，因此所有候选可以一次批量验证，并配合 vLLM 的 Automatic Prefix Caching 前缀缓存、同类型动作分组来最大化共享前缀。平均每步验证 50.3 个动作，在默认的 2× RTX 4090 服务器上只需 0.44 s。LLM 顶部接一个 MLP，把 token logits 投影为动作分数。

**训练信号。** Pair-wise Process Preference（P³）损失让标注的正确动作在每一步都压过其余候选：从带细粒度标签的轨迹构造正负动作对比对（论文提到 100 条任务轨迹可导出约 55K 个逐步标签；pairwise 构造相当于 50× 的数据放大）。错误状态也被利用：预定义的逆向动作映射（click → navigate back、type → clear、open app → navigate home、scroll → reverse scroll、long-click → navigate back）构造自纠正（self-correcting）训练对，随机采样后约占训练集的 2.5%。数据来自人机联合标注（human-agent joint annotation）：先用当前 verifier 自动标注，用分数分布的熵标记不确定的步骤交给人修正，四轮迭代把数据从 9K（纯人工，约每任务 4 分钟、共 5 小时）扩到 27K、55K、110K，人工修正时间降到约每任务 1 分钟；数据覆盖 7 大类、90 多个应用。最终训练：Q-LoRA rank 16，学习率从 1e-4 衰减到 1e-6，20 个 epoch，在 16× A100 40G 上训练 90 小时。

## 论文报告的结果

以下全部是在真实执行的 Android 环境（在线模拟器）上的任务成功率；论文没有报告离线的 grounding / 单步准确率基准。论文未报告种子、运行次数与方差。verifier 基座为 Llama-3.1-8B（4-bit）加 MLP 打分头。延迟在随机抽样的 20 个任务上测量；默认推理硬件为 2× RTX 4090。

| 基准（在线） | V-Droid | 论文报告的领先幅度 |
|----|----|----|
| AndroidWorld（20 个应用、116 任务，in-domain） | 59.5% | +5.2 个点（此前最佳 54.3%） |
| AndroidLab（138 任务，out-of-domain） | 38.3% | +2.1 个点 |
| MobileAgentBench（100 任务，out-of-domain） | 49% | +9.0 个点 |

延迟：整步 4.3 s，比现有智能体快 6.1×；决策延迟 0.74 s（比推理+grounding 分解式智能体快 32.1×；比 UI-TARS 快 25.1×，比带 System-2 reasoning 的 DeepSeek-R1 快 112.2×）。单步分解：验证 0.44 s，动作补全 0.30 s（只有 12.4% 的步骤需要），由 GPT-4 写的 working memory 更新 3.03 s，页面切换平均 0.54 s；动作空间抽取不到 1 ms。显存占用约 16 GB（含 KV cache）。

相对具体基线家族，论文报告：比云端 LLM 智能体在 AndroidWorld / AndroidLab 上高 25.0% / 7.13%；在 AndroidWorld 上比 UI-TARS、Aria-UI、UGround、Aguvis 等分解式高 14.3%；在 AndroidLab 上比微调 SLM 高 14.3%；在三个基准上比 AutoDroid、MobileGPT 等记忆驱动智能体分别高 36.2%、21.0%、18.0% 以上。

## 论文自带的对照实验

**同基座替代方案（Table 3，AndroidWorld，各用 1.1K 任务步训练）。** 同一个 Llama-3.1-8B 微调成 selector（输出正确动作编号）为 35.8%，微调成 T3A 式 generator 为 27.4%，而 V-Droid 的 P³ verifier 为 47.4%。未训练的 judge 直接崩溃：Llama-3.1-8B 做 LLM-as-a-Judge 为 0%，GPT-4 做 judge 为 34.5%（仍高于 GPT-4 做生成器的 29.6%）。验证范式只有在偏好训练之后才有效。

**CoT 开关（Table 2，AndroidWorld）。** GPT-4o：开 CoT 41.3%、决策延迟 6.70 s，关 CoT 39.2%、5.74 s；UI-TARS-7B：33.2%、10.6 s 对 29.3%、0.97 s。没有 CoT 阶段的 V-Droid 为 59.5%、0.74 s，输入 2.6K / 输出 54.3 个 token。

**自纠正与记忆。** 去掉自纠正训练对，AndroidWorld 从 59.5% 降到 52.2%（保留时平均轨迹长度从 10.3 步增至 11.6 步）。把 GPT-4 记忆写作换成规则摘要为 46.1%（延迟近零），只留动作历史为 40.0%。

**规模与标注。** 训练对从 9K → 27K → 55K → 110K，AndroidWorld 成功率 15.0% → 37.5% → 47.4% → 59.5%；MobileAgentBench 从 17.0% 升至 49.0%。Verifier-as-annotator 检验：熵预测逐步正确性的 AUC 从 0.55（第 2 轮）提升到约 0.8；标注准确率从 0.51 升到 0.70 以上，域外数据上预测准确率达 76%。前缀缓存带来 10× 的决策延迟加速。

## 论文自己承认的薄弱处

- 基线数字未复跑：“We directly adopt the SR number reported in the respective baseline papers on the corresponding benchmarks.”（直接采用各基线论文报告的 SR），跨论文对比并非预算对齐。
- AndroidWorld 属于域内：“AndroidWorld is designated as the in-the-domain test set”；只有另外两个基准的应用被从训练数据采集中排除。
- working memory 由 GPT-4 写入并占据主要单步时间（3.03 s）；论文探索了替代方案但未彻底解决该瓶颈。
- 对 300 多个任务的失败分析：幻觉决策仍是 V-Droid 最大的失败类别，且存在 “an incomplete action space caused by inaccurate information from the accessibility service”（无障碍服务信息不准导致的动作空间不完整）——a11y 枚举可能漏动作。纯文本设计带来 “modality limitations”（需要视觉的任务无法完成）。
- 所有成功率均未报告种子与方差。

## CUA Radar 的判断

CUA Radar 给这篇论文打 **65 分（★★）**，证据等级 **transfer**，子模式 K02（verifier 对枚举候选重排序）。分数反映论文所报告的证据：三个公开基准上的在线评测、其中两个基准的应用 held-out、强基线、延迟与成本报告、针对同基座 selector/generator 替代方案的组件消融、verifier-as-annotator 的 AUC 校验，以及已发布的代码。判定记录同时标出：AndroidWorld 为域内、训练数据与其应用存在重叠（AP5）；基线 SR 取自原论文而非匹配预算的复跑；方差未报告；AP14（把动作绑定到可能不完整的结构化元素列表）标记为 unclear。CUA Radar 没有复现任何实验，本文所有数字均来自论文（版本 v5）。
