# selection-006 — gui-rolling-20261023-01（第六期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-10-28，本仓第六期
- 不再入选：前五期 25 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`、`selection-005.md`，`reel/README.md`）。本期 7 个候选都不在其中
- 依据：本 run 的 L2 记录和**每篇的完整原文**。本地缓存 `research/fulltext/<id>.txt` 都是抽取或裁剪的 core（无附录，部分段落带 [...]），所以 7 篇都按缓存文件头钉定的版本从 arxiv.org/html 补读了全文和全部附录（2610.35237 本身没有附录；2610.22155 v3 已在前两期读过全文，本期复核 §6、App. B.1–B.2）。转换稿放在 /tmp/sel6，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 记录：`batches/inc-l2-05.jsonl`（35237、34735）、`batches/inc-l2-06.jsonl`（36471、36831、36877、37482）、`batches/inc-l2-02.jsonl`（22155），各自 supersede 对应的 L1 记录
- 候选池：PROBLEM_CORE 第 4 节 `next_action=to_l3` 中、尚未入选也未在前期作出最终处理的 7 篇（全部 P3 + confirmed）
- 同 run 的其他 to_l3：2610.31274 PointerBench 维持 selection-004 的备选身份（见第 1 节同题判断）；2610.32223 SolveBind 维持 selection-004 的编辑排除；2610.33528 SkillShift-Bench 已按 selection-005 的 correction 修订为 P2/pending_experiment/park（`batches/inc-l2-04-rev1-33528.jsonl`），不进池
- 不进池：2610.36874（P2 confirmed，park；L2 没有给出编辑理由）；2610.34959、2610.31712（同上，前期已记）
- 日期：2026-10-28。之后新增的 L2 或 correction 不计入本期

## 候选池（7 篇）

| ID（钉定版本） | 标题 | tier | q3 | 族 | 卡 |
|---|---|---|---|---|---|
| 2610.22155 (v3) | Realtime-Bench | P3 | judgment | F5,F1 | agent_loop_context_control；online_evaluation_methodology |
| 2610.35237 (v1) | Chart the Invisible (Hagasu) | P3 | capability | F0 | structured_screen_observation |
| 2610.34735 (v1) | iPrefBench | P3 | judgment | F4,F2 | agent_initiated_user_interaction |
| 2610.36471 (v1) | When to Intervene? | P3 | judgment | F2,F0 | agent_loop_context_control；learned_outcome_and_process_judges |
| 2610.36831 (v1) | Right Click, Wrong Box | P3 | judgment | F2 | online_evaluation_methodology |
| 2610.36877 (v1) | GUI-JEPA | P3 | judgment（L2 记录字段；派发说明写作 capability，以记录为准） | F0,F1 | structured_screen_observation；learn_and_train_in_gui_world_model |
| 2610.37482 (v1) | Task Advancement Memory (TAM) | P3 | capability | F0,F2 | agent_loop_context_control；experience_memory_retrieval |

## 1. 最终入选（3 篇）

三篇都是 P3 confirmed，问题各不相同。capability 1 篇，judgment 2 篇。顺序不代表高低。

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2610.36831 Right Click, Wrong Box | J / F2 | online_evaluation_methodology | 问题清楚：grounding 基准只认“落在唯一标注框内”，但界面常把同一动作放在多个元素上，强模型之间又只差一点左右。证据是本期最直接的：在自托管的 Gitea 与 Oscar 上逐点执行并拦截写请求，得到结果地图与执行判卷器，仪器有重载一致、框中心复现、重复执行三项自检；三个 7–8B grounder 被框拒掉的点击中 17.6–20.5%（Gitea）与 29.7–38.1%（Oscar）达成同一结果，Δ 的页面重采样区间都不含 0（Tab.3）；ScreenSpot-v2 盲审两评审 κ=0.95，Web 14.4% 对移动/桌面约 1%；三种子训练实验把“结果奖励更好”这一猜测也测掉了（Tab.5）。分析规则有时间戳与修订日志（App. H）。这改变了“grounding 正确”的定义，以及一点之内的模型比较该怎么做。限制写进画报：执行判卷只有两个 Web 应用；拦截请求不检验提交后的服务器效果；顺序反转的三对区间都含 0 |
| 2 | 2610.35237 Chart the Invisible | C / F0 | structured_screen_observation | 问题清楚：有 swipe 原语不等于会在目标不可见时去滑；7 个代理在 192 个滑动步只有 42.9% 选对，失败中 83.73% 是去点可见的错目标（§2.3）。研究动作是只改观察：用部署时可见的截图预测所有可滑动区域并画回截图，代理保留决策。证据：9 个 VLM 离线应滑召回全部上升；3 个骨干在 18 个探索依赖任务上各跑 3 次，成功率 70.37→88.89、74.07→88.89、50.00→70.37（Tab.4），同时把每题多 33–71 秒、点击召回小降都报了出来，还给出了被提示带偏的失败例。本期唯一可确认的 capability，唯一主族 F0。限制写进画报：在线只有 3 个按离线结果选出的骨干、18 个任务、人工判定；没有只加文字提示的对照；真值区域（G）并不比预测区域更好，收益里多少来自“提醒能滑”未分开 |
| 3 | 2610.34735 iPrefBench | J / F4,F2 | agent_initiated_user_interaction | 问题清楚：个人代理面对说不全的请求，要分清哪些值能从历史推断、哪些只能问；只报操作成功会掩盖替用户做错的决定。研究动作是构造时给每个省略值钉死来源（可推断 / 只能问），再用可执行 iOS 环境、经人工核验的评分器（条目 κ0.89、整题 κ0.94、换评分器 κ0.92）和模拟用户（96.6% 合规）同时测完成、个性化与提问 recall/precision。7 个模型动作完成 77.5–91.6，整题成功 26.2–47.7%；只能问的信息 recall 最高 44.2%；执行前澄清把 recall 拉高、precision 拉低（Tab.2）；多给历史提高推断、却让 recall 下降（§4.4）。这改变了“执行熟练 = 个人代理可用”的判断。本期唯一主族 F4。限制写进画报：单一虚构用户、mock app、LLM 模拟用户与评分器（与被测 Claude Sonnet 5 同源）、单次运行 |

族覆盖（本期，主族）：F2 ×1、F0 ×1、F4 ×1；副族 F2。累计在 selection-005 的口径上加：F2 +1、F0 +1、F4 +1。F4 此前只有 2606.12666 一篇主族。

卡覆盖：online_evaluation_methodology 再次覆盖（前有 2307.13854、2610.32536、2610.34384 等；本篇是唯一针对“单步评分规则本身”的）；structured_screen_observation 第二次（第四期 2610.31698 测的是工具层状态报告缺陷；本篇是视口外内容的显露）；agent_initiated_user_interaction 第二次（见下方同题判断）。selection3 列出的空白卡 environmental_injection_attacks、mine_human_screen_videos 仍然空着。

### 同题判断（每组都按原文定）

- **2610.35237 与 2610.37482（都涉及“任务推进 / 能力”）：不同题。** 35237 是单步观察：在当前截图上标出可滑动区域，帮助代理决定此刻要不要先滑（§3.4，干预只改截图与提示）。37482 是跨步与跨任务的记忆：把已核实的进展写成任务状态，并从局部成功中学习可复用操作（§3.1–3.3）。变量、作用时间尺度和证据形态（同骨干 V/H 对照 vs 记忆组件消融与跨方法比较）都不同。37482 本期因 correction 暂停（第 4 节），与去重无关。
- **2610.36831 与 2610.36471（都涉及“动作评价 / 干预”）：不同题。** 36831 评的是固定界面状态下单次点击的对错，ground truth 来自执行结果（§3.1、§3.4）；36471 研究轨迹里已发生的错误是否会在后续执行中自行恢复，以及能否在错误发生时预测（§3.2、§3.3 RQ3），根本不评单步动作。36471 的排除理由在第 2 节，与 36831 无关。
- **2610.36831 与前期 2610.32536 IGG、备选 2610.31274 PointerBench：不同题。** IGG 把 grounding 失败分解到“显露”阶段；PointerBench 测常规基准缺失的细粒度几何原语；36831 测的是评分规则把哪些对的点击记成错。PointerBench 维持备选，不在本期重新讨论。
- **2610.34735 与首期 2503.19537（同卡 agent_initiated_user_interaction）：同卡不同题，保留。** 2503.19537 是离线单步、无用户历史、每段最多一次交互，主要结论是问得太多（12 个配置 precision 0.08–0.19）；34735 在线可执行、带 3,051 条历史，并按来源区分可推断与只能问，主要结论是该问的不问（recall ≤44.2%），且多给历史会让 recall 更低（§4.4）。两篇结论方向相反、变量不同，画报“我们的阅读”写明两者关系。

## 2. 排除记录（4 篇）

| ID | q3 | 处理 | 理由 |
|---|---|---|---|
| 2610.37482 TAM | C | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节。L2 用作能力证据的 “State-only 12.0→28.2” 的基线行没有说明运行方式；同协议下 State-only（28.2）并不高于 ConAct（29.1）；TAM 对最强基线的 +5.1 点全部来自在评测任务序列上积累的持久操作记忆，而终局评测器的成功判定可以进入这份记忆的复盘（§3.3、App. A.5、App. B.3）。MobileWorld 单次运行、无区间 |
| 2610.22155 Realtime-Bench | J | **不转正；结束滚动备选** | 按原文核对：v3 仍是最新版；Paused 与 Token 时钟的全部对比仍是 50 题单次运行，Web（30 题）与游戏（20 题）没有分开报告，selection-004 写明的转正条件（重复运行或 Web 子集）三期都未满足。收窄后的结论仍站得住（Claude Opus 5、Gemini 3.8 Flash 高推理下 Paused 70% → Token 30%/34%，远大于 Wall Clock 三次极差 10–12 点），但本期复核 App. B.2 还看到：Gemini 3.8 Flash 低推理在 B=32/64/128/∞ 下为 56/54/58/60，几乎不受时间成本影响，所以 36–40 点的落差只属于两个模型在高推理强度下的一次运行，结论比 selection-005 写的更窄。本期另有 3 篇证据更直接、族更分散的候选。之后不再列入滚动备选；若出现补了 Web 子集或 Paused/Token 重复运行的新版本，由 Sol 重做 L2 后再进池 |
| 2610.36471 When to Intervene? | J | 编辑排除（证据形态 + 与已选论文重叠） | 问题成立（观测到的 1,403 个错误中 725 个在轨迹内自行恢复，中位 2 步）。但原文给出的都是观察性证据：标注由两个 LLM 先标、三位作者复核，复核时能看到模型标签，没有报告标注者之间的一致性（§3.2）；Web 轨迹没有截图和完整 DOM（§3.1）；“未恢复”只指在已观测轨迹内，存在右删失；RQ2 的“恢复有助于完成任务”是相关关系（Fig.7）；RQ3 只做恢复预测、没有执行任何干预（§4.4），ReCoF 在 238 个测试事件上对 Direct LLM 的 Macro-F1 增益在 Claude Sonnet 4.5 上只有 +1.30。第五期 2610.34384 AndroidFlux 已用受控重放测过“接手出错状态后的恢复”，因果设计更强；本篇的新增信息（自然恢复的比例与速度）适合在限制栏引用，不足以单独成篇 |
| 2610.36877 GUI-JEPA | J | 编辑排除（证据形态：只有离线单步） | L2 已限定确认范围，原文核对与之一致，无 correction。排除原因：结果全部是 AndroidControl 离线单步准确率，给定真值历史（§4.1、Limitations；按 EVIDENCE.md 只到 `offline`）；除 click reranker 外的设计选择都在 test IDD 上做（App. B）；正文报告的是三个种子里最好的 seed 3，比三种子均值高 0.87–0.90 点（App. B.1）；7B 参照只训了 4K 条、1 轮，GUI-JEPA 用 13,594 条、6 轮（§4.3）；参数匹配、无预测器的头在 3 个种子中有 2 个达到同等准确率（Tab.8），所以“latent 通路必要”也没有被单独证明。效率对比有参考价值，但不足以做成画报 |

`later_work`：7 篇记录都是 null，本期没有按 later_work 降级。

**下期备选**（仅供参考，不改字段）：2610.31274（沿用 selection-004）。2610.22155 移出备选（理由见上表）。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2610.36831 | v1 正文 + App. A–I | 同意 P3/confirmed。L2 biggest_gap 中的 ScreenSpot 校正与三种子 GRPO 都已补读：校正 0.2–1.8 点（Tab.S5），三对顺序反转均不显著（Tab.S6），奖励差在三种子下都不稳定（Tab.5、Fig.5a）。“评审都不同意时用评审标签”的规则是看到评审后添加的（App. C），只改了 2 个单元 |
| 2610.35237 | v1 全文（本文无附录） | 同意 P3/confirmed。**补注（不退回）**：Tab.3 的真值区域条件 G（52.64）不比 Hagasu 预测区域 H（53.87）好，L2 没有提到；它让“收益来自区域感知的准确度”这一解释更弱，与 L2 已写的“未以仅文字提示对照隔离”一致。摘要把离线 9 个模型与在线 3 个骨干写进同一句，L2 已指出。画报限制栏两条都写了 |
| 2610.34735 | v1 正文 + App. A–F（App. G 为提示词，只看结构） | 同意 P3/confirmed。补读后：交叉评分器一致（App. E.4），模拟用户 89 对问答人工核验（App. C.4），专用 GUI 代理因上下文或动作格式问题排除（App. F.1）。**补注（不退回）**：模拟用户与评分器都是 Claude Sonnet 5，而它也是被测模型之一，原文未讨论自评偏差；交叉评分一致性高，风险较低。画报限制栏写明 |
| 2610.37482 | v1 正文 + App. A–D 与 Analysis Protocols；对照了本仓缓存的 MobileWorld 2512.19432v3 Tab.6 | **correction**，见第 4 节 |
| 2610.36471 | v1 正文 + App. A | 同意 L2 的收窄口径（只确认“自然恢复是干预研究应区分的信号”）。补读 App. A：任务级划分、验证集上分折拟合融合层与阈值、测试集任务互斥，L2 担心的校准隔离成立。没有判断错误 |
| 2610.36877 | v1 正文 + App. A–J | 同意 L2 的收窄口径。**补注（不退回）**：正文报告最佳种子（App. B.1）；参数匹配的无预测器头 2/3 种子与基线持平（Tab.8）；预训练与测试的近重复审计做了，影响 −0.2 点（App. G.1）。这些都与 L2 “不确认 JEPA 必要性”一致 |
| 2610.22155 | v3 正文 + App. A–D（前两期已读，本期复核 §6、App. B.1、B.2） | 维持 selection-004/005 的补注；新增 App. B.2 中 Gemini 3.8 Flash 低推理几乎不受 Token 时钟影响这一点，见第 2 节 |

## 4. correction / 待补

### correction（退回 Sol 单篇修订，保留旧记录）

**2610.37482v1 Task Advancement Memory**（旧记录：`batches/inc-l2-06.jsonl`，P3 / confirmed / to_l3，q1 measured_own，q3 capability，q4 fits）

- **错误点**：facts[0] 与 q3_loss 把 “state-only 12.0→28.2” 和 “完整 34.2 vs ConAct 29.1” 当作在线能力已确认的依据，biggest_gap 中列为待查的项目在原文里有了答案，而且答案削弱这一判断：
  1. **基线行没有出处**。Tab.1、Tab.4 的 “Qwen3-VL-32B-Instruct / Base agent 12.0” 没有步数、EQA 与 token 数，§4.1、App. B.4、App. C 都没有说明它怎么跑。MobileWorld 原论文（本仓缓存 2512.19432v3，Tab.6）报告 Qwen3-VL-32B 在 GUI-only（116 题）上为 11.9%，所以 12.0 很可能是引用值，协议可能与本文 App. B.2（每个动作后由评测器检查、成功即停）不同——这是我们的推断，原文未说明。结果是 Advancement State 的贡献没有同协议的无记忆基线。
  2. **同协议对照里 State 并不领先**。在相同骨干、50 轮预算、相同停止规则下，State-only 为 28.2，ConAct（每题重置上下文、无跨任务记忆）为 29.1（Tab.1、Tab.4）。
  3. **对最强基线的领先来自评测序列上积累的记忆，而且终局判定参与其中**。加 Operator Graph 后 28.2→32.5、29.1→34.2；这份记忆按评测任务顺序积累（§4.1、App. B.2 “Persistent memory”），并且 “Terminal success can nominate an outcome candidate for review”（§3.3、App. A.5），“The terminal binary verdict can participate in the disclosed task-end review”（App. B.3）；MobileWorld 每个动作后由评测器检查、成功即停（App. B.2）。§4.1 所说 “supplies no intermediate success feedback to the policy” 只对在线策略成立，对持久记忆不成立。L2 曾把这一点列为未知（“不能声称……完全无标签反馈”），原文确认了它。
  4. **规模与不确定性**。MobileWorld 117 题单次运行，34.2 对 29.1 相当于 40 对 34 题，无区间；独立的局部结果审计只有 20 个不含评测器提名的候选（App. D.5）；flat-state 对照是 9 个字段 × 2 个实现版本的 18 个实例；SPA-Bench 上 GUI-explorer 的 53.7 是引用的其他协议结果（Tab.2 注）。
- **请 Sol 复核**：(a) 在只计同协议对照的前提下，q3 的 capability 是否仍成立；(b) evidence_status 是否应改为 pending_experiment——缺基线行出处、MobileWorld 重复运行或区间、以及排除评测器提名候选的 Operator Graph 消融；(c) 证据等级最高 `online`（记忆来自评测序列本身，EVIDENCE.md 规则 2）。问题本身（跨应用已获取的值能否被后续目标使用、失败任务中的局部成功能否保留）仍成立，Q1/Q2 不必然变化。
- 本期不入选，不制作画报。

### 待补清单（priority=high，但未 confirmed；补齐后由 Sol 单篇做 L2，不在本期直接入选）

| ID | 当前 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2610.30181v1 | P3 / pending_material | 沿用 selection-004：只检索不交互的消融、judge 人工校验、Table 4/5 与 App. C | 能否把交互访问造成的损失与总体难度分开，从而 confirmed |
| 2610.30573v1 | P3 / pending_material | 沿用 selection-004：§4.5 干预结果 Table 3(a)、85 个任务的选取与重跑规则、标签与 checker 校验 | 证据选择与偏好触发两类失败能否受控隔离 |
| 2610.31307v1 | P3 / pending_experiment | 沿用：记忆来源与测试的隔离、等预算对比、标签真值、13 个配对任务的不确定性 | 补不齐就 park |
| 2610.35823 | P3 / pending_experiment | 沿用 selection-005：跨站数据隔离、合法替代轨迹、等预算对照、§3.2 与 §4.4 数据生成模型表述不一致 | 能否 confirmed 进入下期池 |
| 2610.34724v1 | P3 / pending_experiment | 见 progress.md 2026-10-28 12:17：WebShop 指标是部分匹配奖励而非成功率；model-only 消融同时去掉了记忆与 replay，缺隔离证据 | 能否确认记忆本身的贡献 |
| 2610.37093 | P3 / pending_experiment | 见 progress.md 2026-10-28 06:17：核心 judge 无人工或独立真值校验；奖励与更新次数、视觉预算未隔离；无训练种子区间 | 能否确认“空间监督带来跨域观察策略迁移” |

缓存都是 core，可按钉定版本从 arxiv.org/html 取完整附录补材料。

## 5. 漏检抽查结果

本期没有新增抽查。progress.md 记录的漏检抽查欠账（累计约 1.7）尚未清零，本期不处理，留给巡检班。

版本复核：2026-10-28 用 arXiv API 查得 22155 最新仍为 v3，37482、36831、35237、34735 仍为 v1，与钉定版本一致。

## 6. Reel 成品路径

均在 `reel/<id>/` 下，含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。每张都实际打开渲染图做了视觉 QA，用 DOM 测量核对无越界、内容底边不压页脚，并把 PDF 栅格化后与 PNG 对照。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2610.36831 | `reel/2610.36831/` | 像素结果地图（示意）+ 被拒点击救回条 + 误差预算标尺 + 平台分布（网格纸底） | ready（第一次渲染：标题孤行、结果点压字、刻度与脚注重叠、CI 标签被裁；重做一次后底部仍空约 165 px；第三次加入作者的两条评测做法后通过，如实记两轮修改） |
| 2610.35237 | `reel/2610.35237/` | 手机视口剖面（示意）+ 预研条 + 九模型 V/H/G 点阵 + 在线收益/耗时对账（深色底） | ready（第一次渲染：右栏越界、对账数字重叠、示意标签压标题栏；第二次：耗时条缺图例、底部空约 125 px；第三次通过，如实记两轮修改） |
| 2610.34735 | `reel/2610.34735/` | 信息来源分拣图（示意）+ 四刻度梯 + P–R 平面迁移箭头 + 2×2 失败象限 | ready（第一次渲染：说明文字被截断、散点标签相撞、重合点重复标注；第二次：重合点标签压纵轴标题、底部空约 250 px；第三次通过，底部留白约 110 px，如实记两轮修改） |

索引：`reel/README.md` 新增第六期一节；`README.md` 头部统计行由 25 改为 28（滚动 run 由 6 改为 9）。三份 poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
