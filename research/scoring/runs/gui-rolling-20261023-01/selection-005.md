# selection-005 — gui-rolling-20261023-01（第五期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-10-27，本仓第五期
- 不再入选：前四期 22 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`，`reel/README.md`）。本期 5 个候选都不在其中
- 依据：本 run 的 L2 记录和**每篇的完整原文**。本地缓存 `research/fulltext/<id>.txt` 只有 core（无附录，部分带 [...] 裁剪），所以 5 篇都按缓存文件头钉定的版本，从 arxiv.org/html 补读了全文和全部附录（33636 本身没有附录；其 Fig. 2 是 SVG，渲染后读数）。转换稿放在 /tmp/sel5，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 记录：`batches/inc-l2-02.jsonl`（2610.22155）和 `batches/inc-l2-04.jsonl`（另 4 篇），各自 supersede 对应的 `inc-l1-02` / `inc-l1-05` 记录
- 候选池：PROBLEM_CORE 第 4 节 `next_action=to_l3` 中、尚未入选也未在上期作同题去重的 5 篇（全部 P3 + confirmed）
- 同 run 的其他 to_l3：2610.31274 PointerBench 上期已按同题去重让给 2610.32536，并列为备选。本期池中没有 grounding 候选，不重新讨论。2610.32223 SolveBind 上期编辑排除，维持原结论
- 不进池：2610.34959（P2 confirmed，park；L2 没有给出编辑理由）、2610.31712（同上，上期已记）
- 日期：2026-10-27。之后新增的 L2 或 correction 不计入本期

## 候选池（5 篇）

| ID（钉定版本） | 标题 | tier | q3 | 族 | 卡 |
|---|---|---|---|---|---|
| 2610.22155 (v3) | Realtime-Bench | P3 | judgment | F5,F1 | agent_loop_context_control；online_evaluation_methodology |
| 2610.33528 (v1) | SkillShift-Bench | P3 | judgment | F3,F1 | experience_memory_retrieval；online_evaluation_methodology |
| 2610.33907 (v1) | OS-Wizard | P3 | capability | F0,F1 | exploration_driven_task_synthesis |
| 2610.34384 (v1) | AndroidFlux | P3 | judgment | F2,F5 | online_evaluation_methodology；learned_outcome_and_process_judges；agent_loop_context_control |
| 2610.33636 (v1) | Build or Adopt? | P3 | judgment | F1,F0 | agent_loop_context_control；online_evaluation_methodology |

## 1. 最终入选（3 篇）

三篇都是 P3 confirmed，问题各不相同。capability 1 篇，judgment 2 篇。顺序不代表高低。

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2610.34384 AndroidFlux | J / F2,F5 | online_evaluation_methodology；learned_outcome_and_process_judges | 问题清楚：从干净起点测出的成功率，分不出代理接手一个已经出错的状态后能否恢复；拿通用 GUI 偏好训练的奖励模型给恢复动作排序也未必可靠。证据直接：把真实代理的第一个错误重放到相同的设备状态，并按各代理自己的格式重渲染同一段历史，再让不同代理接手。同样 80 个人工核验任务，GUI-Owl-32B 从头做 53.75%，接手后 26.25%；Qwen3-VL-30B-A3B 反而从 13.75% 升到 26.25%。4 次重复下的波动只有 2.5–8.75 点。倒带与注入的收益随错误位置交叉，“最晚 − 最早”差 +12.22，episode bootstrap 95% CI [+4.1, +20.8]，18 个代理中 17 个方向一致。UI-Genie 偏好训练的 BT 奖励模型在本基准上为 0.49/0.52。这改变了“干净起点成功率可以代表稳健性”、“注入扰动造出的偏好数据足以训练过程奖励”这两种判断。限制：只覆盖 AndroidWorld 和第一个可恢复错误；奖励基准只有 100 对，一半处在 2/12 的最小差距上 |
| 2 | 2610.33636 Build or Adopt? | J / F1,F0 | agent_loop_context_control；online_evaluation_methodology | 问题清楚：工具层、设备接入和模型都相同时，自建的固定代理循环还有没有优势。证据直接：只换 harness（生产中的四步 ReAct 对 Claude Code / OpenCode），用同一模型，做配对 Wilcoxon，并重复运行测 flaky。66 个逐步车机用例上成功率都在 55–61%（同模型差 −4.5 到 −0.8，p≥0.17），A 的结果更一致；Google Maps 开放任务上 B 高 9–28 点，但它的单步工具正确率更低（0.88–0.89 对 0.93–0.98），故障恢复率更高（0.78–0.83 对 0.24–0.53）。同模型车机推理费高 2.6–10.7 倍。这改变了“专门写的固定循环一定更好”的默认看法，也说明比较 harness 时应同时报告单步正确率和出错后的恢复。限制：单一企业；LLM judge 只在 Booking 的一轮做过人工核对；A 是按 IVI 和 GPT-5.1 调过的；月总成本 −3% 到 −66% 是基于工时估计的账 |
| 3 | 2610.33907 OS-Wizard | C / F0,F1 | exploration_driven_task_synthesis | 问题清楚：专业软件上通用模型不懂用法，GUI 流程又长，线性 rollout 会漏分支，采集器到不了关键工作流，也就没有可训练的轨迹。证据：同一骨干 Qwen3.5-27B 只给 10K 样本时，36.5±0.7（三次评测）对 Task-driven 13.0、Branch-driven 18.9；全量数据把 ScienceBoard 从 5.9 提到 64.1±0.7，超过兼任采样器和验证器的 GPT-5.6-Sol（42.6）。这改变了“专业软件的数据只能靠人工示范或通用 GUI 合成”的判断。本期唯一的 capability、唯一主族 F0。限制写进画报：消融同时改变了应用构成（Lean 只在线性子集，去 code 子集不含 Lean）；保留轨迹没有人工精度审计；Lean 训练题与 ScienceBoard ATP 的去重没有报告；基线的动作空间和教程配置没有写明 |

族覆盖（本期，主族）：F2 ×1、F1 ×1、F0 ×1；副族 F5、F0、F1。累计在 selection-004 的口径上加：F2 +1、F1 +1、F0 +1。

卡覆盖：exploration_driven_task_synthesis 第二次覆盖（第二期 2601.22781 测的是合成难度；本篇测的是专业软件上采集器能否到达，不同题）。learned_outcome_and_process_judges 第二次覆盖（首期 2404.06474 做评估器校准；本篇只测恢复动作排序）。selection3 列出的空白卡 environmental_injection_attacks、mine_human_screen_videos 仍然空着。

### 同题判断：2610.33907 与 2610.33636

两篇都涉及“桌面/移动代理的整套外壳”，但**不同题，不做同题去重**：

- 33907 问的是**训练数据怎么采**：采集器（教程检索、GUI＋原生命令、枢纽快照）能否到达专业软件的工作流，并产出更有用的 SFT 数据。改变的是模型权重，评测时的循环不变。
- 33636 问的是**推理时用哪种代理循环、谁来维护**：工具层和模型固定，只换控制循环和上下文管理。改变的是 harness，不训练模型。
- 两者唯一的交集是“代码/工具通道比纯 GUI 短”，但 33636 两边用的是同一套工具，所以这一点不是它的变量。主卡、族和证据形态（训练前后对比 vs 同模型 harness 替换）都不同。
- 另外核对了 33636 与第三期 2604.00073（同骨干比较 GUI/工具/终端接口）：两篇结论形态相近（成功率接近，成本差数倍），但变量不同（接口模态 vs 控制循环），所以保留，并在 QA 中写明。

## 2. 排除记录（2 篇）

| ID | q3 | 处理 | 理由 |
|---|---|---|---|
| 2610.33528 SkillShift-Bench | J | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节。基准测到的是“装了技能库的代理在同站演化、扰动和模态拦截下变差”，但没有设无技能对照，而且技能调用极少（ASI 每题 0.05–0.29 次），这些下降不能归到“技能变得不可执行”上。L2 的 q1/facts 把它写成本研究自己测到了技能可执行性问题，超出了证据 |
| 2610.22155 Realtime-Bench | J | 上期顾虑**未解除**；再次列为下期备选 | 按原文核对：v3 是最新版（abs 页只有 v1–v3），Paused 与 Token 时钟的全部对比仍是 50 题单次运行；App. B.2 Token-rate 表中 B=64 一列与 Fig. 5 的 TL 数值相同（Claude 44、Kimi 24），B=∞ 就是 PL，都不是独立重复；Web 子集仍然没有单独结果。上期写明的重选条件（补到 Paused/Token 重复运行或 Web 子集）没有满足。不过原文支持把结论收窄后成立：Claude Opus 5 和 Gemini 3.8 Flash 在高推理下从 Paused 70% 跌到 Token 30%/34%，差 36–40 点，远大于 Wall Clock 三次运行的最大极差（10–12 点）；Claude 随 B 增大单调上升（30/44/56/62）。站不住的只是“推理强度在时间压力下效果反转”（44→30、24→36）。本期另有 3 篇证据更直接的候选，AndroidFlux 已带 F5 副族，F5 主族已有 3 篇，所以不入选。下期若选这篇，画报只应以“时间成本造成的损失”为主结论，推理强度反转只能放进限制栏 |

`later_work`：5 篇记录都是 null，本期没有按 later_work 降级。

**下期备选**（仅供参考，不改字段）：2610.22155（按上面的收窄口径）；2610.31274（沿用上期）。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2610.34384 | v1 正文 + App. A–F | 同意 P3/confirmed。补读后 L2 biggest_gap 中的附录项都有了：重复性（App. C.6 Table 17/18）、检测器 P/R（C.9）、配对构造（App. D）、离线 RL 单 seed（E.2）。**补注（不退回）**：“CoT 只在 GUI 领域 RL 后有帮助”混入了从头做时的能力差（Qwen3-VL-32B Thinking 在 Scratch 上也从 36.25 降到 11.25）；5 个单代理打分者恰好就是候选生成者（App. D Table 26）。画报两条都放在限制栏 |
| 2610.33636 | v1 全文（本文无附录）+ Fig. 2 SVG | 同意。L2 facts 与原文一致；judge 只做了部分人工核对，恢复优势的归因没有做消融，L2 都已写明 |
| 2610.33907 | v1 正文 + App. A–F | 同意 P3/confirmed。**补注（不退回）**：三组 20K 消融都改变了应用构成（Lean 每步都是 CODE 编辑，且只用线性采集，所以去 code 和只用树的子集都不含 Lean）。L2 已提到 code/no-code 分布不同，这里只是说得更具体。画报标为混杂项。人类 59.8% 与 SCALECUA 54.0% 引自其他论文、设置不同，画报只作参考 |
| 2610.33528 | v1 正文 + App. A–E（App. C 的证明只看了结构，没有逐行验证） | **correction**，见第 4 节 |
| 2610.22155 | v3 正文 + App. A–D（上期已读，本期复核 §6、App. A.2、B.1、B.2） | 维持 selection-004 的补注；顾虑未解除，理由见第 2 节 |

## 4. correction / 待补

### correction（退回 Sol 单篇修订，保留旧记录）

**2610.33528v1 SkillShift-Bench**（旧记录：`batches/inc-l2-04.jsonl`，P3 / confirmed / to_l3，q1 measured_own，q3 judgment）

- **错误点**：facts[0] 写“本研究自己的测量支持同站演化下技能可执行性问题”；q3_loss 写“将……区分技能获取与执行时适配的贡献”。原文测到的是另一回事：
  1. **没有无技能对照**。六个条件下只评测了 AWM、ASI、SkillWeaver、WALT 四个带技能库的系统（§5.1），没有同栈、只用原子动作的基线，所以分不出下降是因为“技能失效”还是因为“代理本身在版本迁移、DOM 扰动和模态拦截下变差”。
  2. **技能调用极少**。Table 1 中 ASI 的 ASC 是每题 0.05–0.29 次（Tgt-Exec 只有 0.05），WALT 是 0.00–0.21 次；绝大多数任务根本没有调用技能。ASI 从 53.65 降到 15.79，不能归到技能的调用、grounding 或执行上。
  3. **没有可执行技能的 AWM 下降幅度相近**（50.07 → 16.90）。这说明主要压力来自环境变化本身。作者在 §3.4 和 App. B.4 也承认 SFR 在低调用时不稳定；“三种偏移对应三个技能阶段”只有 Magento 上 GPT-5 mini 的 13/10/29 个回归样例，属于定性分析。
  4. **方法证据也比 L2 写得弱**。单次运行、三站汇总的平均提升是 +3.36 点（37.90 → 41.26）；App. D.8.1 中“可行性证据”本身只贡献 +2.14 点（盲重排 37.04 → 完整 39.18，Magento，单次），主要增益来自多一次 LLM 比较（+4.31）。随机对照降到 8.09%，远低于什么都不做的 32.73%，这个结果本身反常，不能用来说明“增益不是来自额外调用”。三 seed 结果中 Tgt 和 Tgt-Perc 的增益落在标准差以内（App. E.5）。
- **请 Sol 复核**：(a) 把 problem_statement 和 Q1 的依据收窄到实际测到的“带技能代理在同站演化下的退化”，单独判断“技能可执行性是瓶颈”是 asserted 还是 measured；(b) Execution Shift 的模态拦截沿用了 Kara et al. (2026)（§3.2 引用），请核对 q2_prior / q2_open；(c) 据此重判 tier。如果技能归因只是 asserted，按封顶规则最高 P2。
- 本期不入选，不制作画报。

### 待补清单（priority=high，但未 confirmed；补齐后由 Sol 单篇做 L2，不在本期直接入选）

| ID | 当前 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2610.30181v1 | P3 / pending_material | 沿用 selection-004：只检索不交互的消融、judge 人工校验、Table 4/5 与 App. C | 能否把交互访问造成的损失与总体难度分开，从而 confirmed |
| 2610.30573v1 | P3 / pending_material | 沿用 selection-004：§4.5 干预结果 Table 3(a)、85 个任务的选取与重跑规则、标签与 checker 校验 | 证据选择与偏好触发两类失败能否受控隔离 |
| 2610.31307v1 | P3 / pending_experiment | 沿用：记忆来源与测试的隔离、等预算对比、标签真值、13 个配对任务的不确定性 | 补不齐就 park |
| 2610.35823 | P3 / pending_experiment | 见 progress.md 2026-10-27 12:17：跨站数据隔离、合法替代轨迹、等预算对照、§3.2 与 §4.4 数据生成模型表述不一致 | 能否 confirmed 进入下期池 |

前两篇仍可按上期建议从 arxiv.org/html 取完整 HTML 补材料。

## 5. 漏检抽查结果

本期没有新增抽查。progress.md 记录的漏检抽查欠账（累计约 0.8，取整为 0）尚未清零，本期不处理。

## 6. Reel 成品路径

均在 `reel/<id>/` 下，含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。每张都实际打开渲染图做了视觉 QA，并用 DOM 测量核对内容底边不压页脚。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2610.34384 | `reel/2610.34384/` | 检查点时间轴 + 斜率重排 + 倒带/注入交叉线 + 奖励模型哑铃（深色底） | ready（第一次渲染：标签裁切、数值重叠、图例截断；第二次：底栏压页脚；第三次通过，如实记两轮修改） |
| 2610.33636 | `reel/2610.33636/` | 建筑剖面（两座楼共用地基）+ 三栏分户账 + 正确率–恢复散点 + 访谈条 | ready（第一次渲染：底部空白、圆内文字溢出；重做一次后通过，同时把标题限定到“开放任务上”） |
| 2610.33907 | `reel/2610.33907/` | 竖向采集树 + 同骨干阶梯 + 领域条 + 带混杂标注的消融 | ready（第一次渲染：右栏越界、树内文字被连线穿过；第二次：新增卡片图例压柱；第三次通过，如实记两轮修改） |

索引：`reel/README.md` 第五期一节；`README.md` 头部统计行由 22 改为 25。三份 poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
