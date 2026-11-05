# selection-009 — gui-rolling-20261023-01（第九期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-11-04，本仓第九期（单席串行）
- 不再入选：前八期 32 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`–`selection-008.md`，`reel/README.md`）。本期 21 个候选都不在其中
- 依据：本 run 最新 L2 记录；入选、退回与需要定夺的 6 篇按缓存钉定的 v1 从 arxiv.org/html 补读了全文与附录（见第 3 节）；其余 15 篇只读了 L2 记录与本地裁剪 core，按编辑理由排除，**未声称读过全文**。转换稿在 /tmp/sel9，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 记录：`batches/inc-l2-12.jsonl`（2610.41181）、`inc-l2-13.jsonl`–`inc-l2-15.jsonl`（Awesome-CUA 回填 17 篇）、`inc-l2-17.jsonl`（3 篇），各自 supersede 对应 L1
- 候选池：PROBLEM_CORE 第 4 节 `next_action=to_l3` 中、selection-008 之后新增的 21 篇（全部 P3 + confirmed）
- **关于 2610.41181**：派发说明称它“上期已入选制作”。核对后并非如此——selection-008 入选的是 2610.41272（`reel/2610.41272/`），41181 在 2026-11-04 18:17 巡检班（inc-l2-12）才进池，`reel/` 下没有它。因此按本期正常候选处理，见第 2 节
- 同 run 的其他 to_l3 维持前期处理：2610.31274 PointerBench 仍为 selection-004 起的备选；2610.32223、2610.36471、2610.36877 维持编辑排除；C-007-1（40133）、C-008-1（41397）、C-008-2（40798）的修订记录均已转 park，不进池
- 日期：2026-11-04。之后新增的 L2 或 correction 不计入本期

## 候选池（21 篇）

| ID（缓存版本） | 简称 | tier | q3 | 族 | 主卡 |
|---|---|---|---|---|---|
| 2610.41181v1 | AgentShield | P3 | J | F4,F0 | environmental_injection_attacks |
| 2508.18040v1 | PerPilot | P3 | C | F4,F0 | experience_memory_retrieval |
| 2607.05804v2 | TurnOPD | P3 | J | F5,F0 | trajectory_level_policy_training |
| 2608.07775v1 | AndroidReality | P3 | J | F3,F0 | online_evaluation_methodology |
| 2609.33102v1 | ORBIT | P3 | J | F3,F4 | injection_defense_isolation |
| 2610.02542v1 | FT vs RAG world model | P3 | J | F1,F2 | learn_and_train_in_gui_world_model |
| 2610.02617v1 | WebUIProof | P3 | J | F2,F0 | verifiable_execution_reward |
| 2610.06898v1 | DIBench | P3 | J | F2,F4 | environmental_injection_attacks |
| 2610.09944v2 | AgentTime | P3 | J | F2,F0 | online_evaluation_methodology |
| 2610.11963v1 | No-code fix verification | P3 | J | F1,F2 | online_evaluation_methodology |
| 2610.13092v1 | Jev in agent workflows | P3 | J | F1,F5 | agent_loop_context_control |
| 2610.19384v1 | MMA-SafetyBench | P3 | J | F2,F4 | environmental_injection_attacks |
| 2610.22686v2 | MFM memory | P3 | C | F0,F3 | experience_memory_retrieval |
| 2610.28679v2 | VerifierBench | P3 | J | F2 | verifiable_execution_reward |
| 2610.31162v1 | HiSTEVE | P3 | C | F4,F1 | planner_grounder_interface |
| 2611.02472v1 | MAGAR | P3 | C | F2,F0 | planner_grounder_interface |
| 2611.02644v1 | Coati | P3 | C | F2,F4 | agent_loop_context_control |
| 2611.03238v1 | ScienceCUA | P3 | C | F3,F4 | experience_memory_retrieval |
| 2611.04879v1 | ScamWorld | P3 | C | F4,F2 | environmental_injection_attacks |
| 2611.05263v1 | JHiMA-WebRL | P3 | C | F1,F0 | agent_loop_context_control |
| 2611.04073v1 | Tutorials vs world model | P3 | J | F1,F2 | simulated_lookahead_selection |

按 SELECTION.md 排列：全部 P3；capability 9 篇、judgment 12 篇，不分先后。池内按问题族与卡分组后做同题去重与编辑排除：
- **安全/注入一带（5 篇）**：41181、06898、19384、04879、33102。上期刚入选同卡 41272（自适应注入攻击）。本期只保留一篇，选问题与上期最不同、测量最直接的 04879（不是注入，而是“照用户请求办事时接受网站附加条款”）
- **世界模型/前瞻与教程知识（3 篇）**：04073、02542、03238。04073 是唯一在视觉 CUA 上做受控归因、且把世界模型换成真实截图上界的一篇；02542 是文本 WebShop，03238 与 04073 同用 ScienceBoard、同问“文档知识怎样帮科学软件 CUA”，记同题去重
- **评测方法（4 篇）**：08775、09944、11963、02617——与已入 Reel 的评测类卡片重复度高或偏离核心（见第 2 节）
- **规划/执行接口与系统（5 篇）**：05263（correction）、31162、02472、02644、13092
- **记忆/训练（3 篇）**：18040、22686、05804

## 1. 最终入选（2 篇）

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2611.04073 Tutorials vs world model | J / F1,F2 | simulated_lookahead_selection；learned_outcome_and_process_judges | 问题清楚：R-WoM 一类方法把“检索教程 + MLLM 判官 + 世界模型前瞻”捆在一起，只和无教程基线比。本文固定 policy/judge/grounder、harness、K=3，只换判官看到的未来（无 / 文本预测 / 真实截图），并用 VM 快照让每个候选真实执行 1–3 步作为保真度上界。OSWorld 360 题、Qwen3-VL-32B：无教程时真实未来 43.8→48.0（表 2），有教程时 51.7→51.6（表 6）；ScienceBoard 32B 40.2→42.4（p=0.32）。收益的大头是教程（OSWorld +5.3、ScienceBoard +15~21），判官再 +4。改变“提高下一屏保真度就能改善前瞻选择”的判断，并补上本仓 2504.13936 ViMo 画报记下的空缺对照。限制写进画报：单一 Qwen 家族零样本判官；教程是测试时强信息（生成器还搜过任务文件，但 110 题人工教程子集结论相同）；27B 上名义 +0.8~+1.6、不显著≠等价；无候选覆盖率；代价未配平；v1 HTML 缺 OSWorld 主表 |
| 2 | 2611.04879 ScamWorld | C / F4,F2 | environmental_injection_attacks；online_evaluation_methodology | 问题清楚：网页代理照用户请求办事时，会不会接受诈骗网站附加的条件——不需要注入，也不偏离任务。377 个依据真实举报重建的诈骗任务 + 53 个同流程合法站，用网站事件日志判定是否完成付款/提交凭据：6 个骨干受骗 11%–35%，合法完成 94%–100%；492 次受骗里 220 次在最终动作前已点名风险；付款 28% vs 凭据类 2%；单独问“是不是诈骗”能认出 88%–100%；一句警告使受骗 −24 点、合法完成 −3 点。它改变“看最终答复/检测率即可评估安全”“用户请求即授权”的做法。与上期同卡的 41272 不同题（41272 是攻击者注入与自适应搜索）。限制写进画报：从站内起步、红旗约半数由作者补入；检测口径宽（严格 58%–80%）；合法对照不配对；每任务一次运行；结果集中在少数网站 |

族覆盖（本期主族）：F1 ×1、F4 ×1；副族 F2 ×2。卡覆盖：simulated_lookahead_selection 自首期 2407.01476 后第二次入 Reel；environmental_injection_attacks 连续两期各一篇，但问题不同。

只选 2 篇：池内其余 P3 都有同题去重、偏离 GUI 核心、证据形态或卡片重复的理由（第 2 节）；不为凑 3 篇把 DIBench 或 Coati 做成画报，二者列为下期备选。

## 2. 排除记录（19 篇）

| ID | q3 | 处理 | 理由 |
|---|---|---|---|
| 2611.05263 JHiMA-WebRL | C | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节 C-009-1。核心比较的差距都在 1.7–3.8 点，无方差、单训练种子；主表“37.2 vs 24.0”的大部分来自 SFT 数据与配方差异，不是联合训练 |
| 2610.06898 DIBench | J | 编辑排除（同卡近题，**下期备选**） | 移动端决策完整性：注入可见内容操纵候选选择，完成率反而上升。问题成立且与 04879 不同，但同属“网站内容误导代理做用户要求的事”，与上期 41272、本期 04879 同卡；本期保留测量更直接的 04879。只读 L2 与 core |
| 2611.02644 Coati | C | 编辑排除（证据形态，**下期备选**） | 已读全文。同 Gemini 3.8 Flash、仅可访问性 API 下 86.5% vs Artemis 77.6%（3 次）可信；但核心机制 VerifyLoop 的消融是 C1 单次（8.0% 假完成）对 C2 三次均值（5.4%），不是配对；快速执行器与 AppMemory 为 3–5 次运行的小样本。系统论文，机制贡献无法逐项归因 |
| 2610.13092 Jev | J | 编辑排除（偏离核心 / 证据边界） | 已读全文。仅文本观测（AndroidWorld 可访问性文本、ALFWorld），针对一个厂商决策模型。“每次成功成本上升”只在 T3A 一家、+7.7% 且 95% 区间跨零（表 10）；稳健的是每次成功耗时上升（T3A +59.6 s、FastAgent +138 s）与成功率 −13/−18 点。“按交付成功计成本”的评价原则已由 Kapoor et al. 提出（本文引用）。补注见第 3 节 |
| 2610.11963 No-code fix | J | 编辑排除（偏离核心） | 已读结构与结果节。主题是软件工程的无代码修复生成，CUA 只作执行器；可运行的 issue 只有 51 个候选中的 9 个（17.6%），执行器间 46.9% 一致、换执行器平均变 38.8% 的发现有价值，但样本面太窄 |
| 2611.03238 ScienceCUA | C | 同题去重 | 与 04073 同用 ScienceBoard、同问“文档/教程知识如何帮科学软件 CUA”；04073 给出更干净的受控归因。L2 列出的缺口（App. I 回归认证、双侧 checker、信息匹配组织消融）未补。RSI 仓已入选，三仓不共享，本仓按 CUA 卡独立判断。只读 L2 与 core |
| 2610.02542 FT vs RAG WM | J | 同题去重 / 偏离 GUI | 文本 WebShop 世界模型构造方式；与 04073 同属“世界模型对选择的价值”，但非视觉 GUI。只读 L2 与 core |
| 2610.41181 AgentShield | J | 编辑排除（同卡 + 视角） | 已确认部分是“传统反机器人信号挡不住代理”（站点防御视角）；EPD 攻击的对照与重试预算在缓存中截断，L2 不以其作晋级依据。同卡上期、本期已各有一篇。只读 L2 与 core |
| 2610.19384 MMA-SafetyBench | J | 编辑排除（证据形态 + 同卡） | 冻结观察上的输出级劫持信号，不是闭环执行后果；同卡。只读 L2 与 core |
| 2609.33102 ORBIT | J | 编辑排除（偏离核心） | 多代理安全框架，GUI 部分仅浏览器拓扑一项，桌面分项与良性效用缺。只读 L2 与 core |
| 2608.07775 AndroidReality | J | 编辑排除（与既有画报重复） | 弹窗/延迟/掉动作扰动下的鲁棒性，与已入 Reel 的 39282（加载时序）、39234（资源阻断与恢复）、34384（出错状态接手）问题高度重叠；L2 注明只有本地 GUI-Owl 严格配对、TTIR 主表未缓存。只读 L2 与 core |
| 2610.09944 AgentTime | J | 编辑排除（偏离核心） | 222 个任务主要是编码/研究型 harness；GUI 只是 OSWorld 子集，L2 注明缺 GUI 分层率。只读 L2 与 core |
| 2610.02617 WebUIProof | J | 编辑排除（偏离核心） | 主题是 WebUI 代码生成评测，UI 代理只作交互测试 harness。只读 L2 与 core |
| 2610.28679 VerifierBench | J | 编辑排除（偏离核心） | 工具调用/状态/代码验证器，L2 自述不能用其数值预测 GUI checker 错误率。只读 L2 与 core |
| 2610.31162 HiSTEVE | C | 编辑排除（偏离核心） | Minecraft 原生键鼠 VLA；L2 注明角色与预算归因 partial。只读 L2 与 core |
| 2611.02472 MAGAR | C | 编辑排除（证据形态） | 录制状态上的离线选择性修正（37.50→41.39；209 次介入中 70 次修对、22 次改错），没有闭环装配。只读 L2 与 core |
| 2610.22686 MFM | C | 编辑排除（证据形态） | Minecraft 为主，KiCad 一项；L2 注明缺等预算的视觉保留消融与错误记忆审计。只读 L2 与 core |
| 2508.18040 PerPilot | C | 编辑排除（同卡近题 + 规模） | 个性化指令补全，75 条指令；与已入 Reel 的 2610.34735 iPrefBench（只能问的信息与提问）同卡近题。只读 L2 与 core |
| 2607.05804 TurnOPD | J | 编辑排除（偏离核心） | 长程 OPD 训练预算，诊断主要在 ALFWorld，WebShop 为文本网页；标准差来自 4 个检查点而非独立种子。只读 L2 与 core |

`later_work`：21 篇记录都是 null，本期没有按 later_work 降级。

**下期备选**（仅供参考，不改字段）：2610.31274（沿用 selection-004）、2610.06898 DIBench、2611.02644 Coati。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2611.04073 | v1 正文 §1–8 + App. A–U（表 1–14；提示词附录只看结构） | 同意 P3/confirmed。**补注（不退回）**：(a) 子卡 K02 的 paper_evidence 写“失败类别由 Gemini 标注无人工复核”，App. R 实有 30 题人工定类、主因一致率 90%、另抽 20 条复看，仍以模型标注为主，partial 不变；(b) App. E 图 9 显示教程生成器曾搜索任务文件 ID 与 OSWorld 仓库，教程收益可能含基准信息，但 110 题人工教程子集上主结论不变（表 4）；(c) v1 HTML 缺 OSWorld 主表、正文把 ScienceBoard 表称“表 9”，L2 facts 的“缓存标 Table 1、正文称 Table 9”即此 |
| 2611.04879 | v1 正文 §1–6 + App. A（表 1–6，图说明全部） | 同意 P3/confirmed。L2 facts 的 430 vs 416 口径疑问已解：377 个诈骗任务建在 363 个站上，377+53=430。**补注（不退回）**：q3 更接近 judgment（评测与授权判断），capability 亦可辩护，同属 P3 条件 |
| 2611.05263 | v1 正文 §1–6 + App. A–C | **correction**，见第 4 节 C-009-1 |
| 2611.02644 | v1 正文 §1–6 + App. A–D | 同意档位；排除为编辑理由（VerifyLoop 消融非配对），不退回 |
| 2610.13092 | v1 正文 §1–7 + App. A–C | 同意档位。**补注（不退回）**：L2 problem_statement 与 q3_loss 以“每个成功交付的成本更高”为核心损失；表 10 中唯一的成本上升（T3A +5.27 mUSD/成功）95% 区间 [−3.83, +17.34] 跨零，作者也写明。稳健的是每次成功耗时上升与成功率下降。不改档位 |
| 2610.11963 | v1 摘要、§3–4 结构与结果表 | 只核对排除理由（9/51 issue、执行器一致率），未逐节核对 L2 |
| 其余 15 篇 | 仅 L2 记录 + 本地裁剪 core | 未读全文；按第 2 节编辑理由排除，不对其 L2 判断作结论 |

版本复核：2026-11-04 查 export.arxiv.org/abs，读过全文的 6 篇均只有 v1，与缓存钉定版本一致。

## 4. correction / 待补

### C-009-1　2611.05263v1 JHiMA-WebRL（退回 Sol 单篇修订，保留旧记录）

旧记录：`batches/inc-l2-17.jsonl`，P3 / confirmed / to_l3；q1 measured_own，q2 open_failure，q3 capability，q4 fits。

- **错误点**：
  1. **“冻结分解器使 actor RL 与计划失配”这一问题本身没有被测出**。依据是表 2 的 33.4%（冻结分解器、只训 actor）低于 35.1%（双模块 SFT），差 1.7 点；154 题上一题约 0.65 点，即约 3 题。表 1/2 只报 4 次评测的均值，**没有任何标准差或区间**，训练只有一个种子。作者在 §5(v) 自述“消融差值 2.0–3.8 点的量级正是运行方差起作用的范围”。q1 的 measured_own 因此缺少可区分的测量。
  2. **联合更新的增益同样落在未报告的方差内**。联合 37.2% 对 actor-only RL（无分解器）35.2%/34.9%、对 SFT 双模块 35.1%，差 2.0–2.3 点。
  3. **主表“同协议 37.2 vs 24.0”不能归因到层级联合训练**。同为 7B、同一 RL 任务的无分解器 actor-only RL 已达 35.2%，比 ScaleCUA-32B RL（24.0%，7 次 rollout）高 11.2 点；13.2 点差距的大部分来自 actor 的 SFT 数据（ScaleCUA 轨迹 + 2,535,552 条含 grounding 的样本）与训练配方，而不是联合训练。L2 已在 biggest_gap 中说“不表示差距全归因联合训练”，但仍据此给 fits/confirmed。
  4. 其他已由 L2 列出、仍未解决：计划 open-loop；教师子任务标签未经人工核验；训练/评测共享站点与意图模板；评测用 LLM fuzzy match。
- **请 Sol 复核**：(a) q4 是否应为 `partial`、evidence_status 是否应为 `pending_experiment`（缺：多种子训练与评测方差、显著性检验、交替训练对照、同 SFT 数据下的单体基线）；(b) q1 是否仍可记 measured_own——若 33.4 vs 35.1 不足以区分，“冻结计划失配”应视为未测出；(c) q3 是否应收窄为 `incremental`（在已有 planner–actor 分离上加联合 GRPO，已证增益在噪声量级）。若 (a)(c) 成立，按 PROBLEM_CORE 第 4 节应为 P2 / pending_experiment / park。
- 本期不入选，不制作画报。

### 待补清单

沿用 selection-008 第 4 节（selection-007 的 9 篇 + 2610.40747），状态未变。本期没有新增 needs_material 的 high 项。

## 5. 漏检抽查结果

本期没有新增抽查。按 progress.md，inc-l2-13..16 的 6 篇抽查与 inc-l2-12 的 4 篇抽查改判均为 0；inc-l2-17 欠账约 0.4 滚存，留给巡检班。

## 6. Reel 成品路径

各目录含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。实际打开渲染图做视觉 QA；用 DOM 探针核对无越界、内容底边不压页脚、SVG 文本不越框；PDF 栅格化后与 PNG 并排对照；缩到 580 px 宽检查小屏可读性。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2611.04073 | `reel/2611.04073/` | 因子开关机制图 + 有/无教程分带点图 + 三组收益阶梯 + Celestia 三分支案例 + 双栏失败类型（浅色网格底、墨绿/梅红/蓝） | ready（第一次：限制栏压页脚、阶梯卡越出右缘、机制图多处文字越框；第二次修掉主要问题；第三次处理贴边与回环箭头后通过） |
| 2611.04879 | `reel/2611.04879/` | 四段结账路径 + 停法分布条 + 知道/做到三点图 + 钱/秘密对比 + 自述计数块 + 收据式样例 + 干预表 + 来源漏斗（米色纸底、深棕锯齿页眉） | ready（第一次：底部空约 170 px、表头折行；第二次加大字号与图高；第三次补第二个样例填满样例卡后通过） |

索引：`reel/README.md` 新增第九期一节；`README.md` 头部统计行由 32 改为 34（滚动 run 由 13 改为 15）。poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
