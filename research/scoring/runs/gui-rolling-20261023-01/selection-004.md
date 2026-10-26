# selection-004 — gui-rolling-20261023-01（第四期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-10-26，本仓第四期
- 不再入选：前三期 19 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，`reel/README.md`）。本期 6 个候选都不在其中
- 依据：本 run L2 记录，以及**每篇的完整原文**。本地缓存 `research/fulltext/<id>.txt` 只到 core（显式省略、无附录），所以 6 篇都按缓存文件头钉定的版本从 arxiv.org/html 补读了全文（入选 3 篇和 Realtime-Bench、PointerBench 读了正文与全部附录，SolveBind 读了正文与附录 D.1/D.4/D.5/D.10）；转换稿放在 /tmp，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 记录：`batches/inc-l2-02.jsonl`。6 个候选的最新记录都在这个文件里，各自 supersede 对应的 `inc-l1-02` / `inc-l1-03` / `inc-l1-01` 记录
- 候选池：PROBLEM_CORE 第 4 节 `next_action=to_l3` 的 6 篇（P3 + confirmed）。同 run 的 2610.31712（P2 confirmed，park，L2 认为没有足够的编辑理由）不进池
- 日期：2026-10-26。之后新增的 L2 或 correction 不计入本期

## 候选池（6 篇）

| ID（钉定版本） | 标题 | tier | q3 | 族 | 卡 |
|---|---|---|---|---|---|
| 2610.31698 (v1) | Understanding Tool-Mediated Interaction Failures in Agentic GUI Software | P3 | judgment | F1,F2 | structured_screen_observation；agent_loop_context_control |
| 2610.32223 (v1) | Correct Answers, Closed Gates: SolveBind | P3 | capability | F0 | agent_loop_context_control；online_evaluation_methodology |
| 2610.32536 (v1) | IGG: Interactive GUI Grounding under Visibility Constraints | P3 | judgment | F1 | online_evaluation_methodology；high_resolution_target_localisation |
| 2610.22155 (v3) | Realtime-Bench | P3 | judgment | F5,F1 | agent_loop_context_control；online_evaluation_methodology |
| 2610.30792v1 | Trace2World | P3 | judgment | F2,F3 | calibrate_simulator_to_real |
| 2610.31274v1 | PointerBench | P3 | capability | F0 | high_resolution_target_localisation；online_evaluation_methodology |

## 1. 最终入选（3 篇）

三篇都是 P3 confirmed、q3 judgment，问题各不相同。顺序不代表高低。

| # | ID | 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2610.30792 Trace2World | F2,F3 | calibrate_simulator_to_real（**新覆盖**，前三期一直空着） | 问题清楚：从部分轨迹重建 GUI 训练环境时，编码代理在写代码的同时决定语义，再用同一套解读写的测试来验收，错误的状态转移因此能通过。证据直接：自验证对照只换验收证据，其他构建阶段和模型都不变。在 20 个训练 app 的 100 个配对真机任务上（3 个训练 seed），模拟收益留到真机的比例是 94.0%（源回放验收）对 54.7%（自验证）；6.0 pp 差距的主要来源是“模拟里通过、真机上失败”的减少（8.3 pp）。这改变了“能跑、终值对、自写测试通过就能当训练环境”的验收做法。限制：保真度的 200 个工作流在构建时就被源回放检查和修复过；真机只测了训练 app；基线都是重实现 |
| 2 | 2610.31698 Malva | F1,F2 | structured_screen_observation（**新覆盖**）；agent_loop_context_control | 问题清楚：GUI 代理通过工具来观察、执行和接收回报，工具不做核对就把状态交给模型，模型看到的界面于是与真实界面静默脱节。40 个开源应用、99 个确认缺陷，跨应用复现成 335 例，分为 11 种模式；86.6% 的失败造成结果错误，119 例出错却没有任何停止信号。静态检查器在另外 20 个应用上达到 57.3% precision、76.8% recall。这改变了把 GUI 失败默认算到模型推理上的归因习惯（F1），也说明执行回报本身可能是假的（F2）。限制：样本以 issue 为入口，比例描述的是这份缺陷库，不是部署中的出错率；335 不是 335 个独立 issue |
| 3 | 2610.32536 IGG | F1 | high_resolution_target_localisation；online_evaluation_methodology | 问题清楚：目标一开始不可见或不可点时，失败该算在“让目标出现”还是“认出并点中目标”上。受控干预直接回答了这个问题：Qwen3-VL 完整完成 30.8%，告诉它动作类别只到 33.9%，替它把显露动作做完就到 81.9%。失败轨迹里，需要 Drag 的任务一次都没有用 Drag（59/59）。SFT+GRPO 在三种架构上都有提升（同环境 120 题留出）。限制：16 个确定性仿制环境；每题只跑一次；“代执行”同时去掉了位置/参数选择和动作执行，两者没有分开 |

族覆盖（本期）：F1 ×2（2、3），F2 ×2（1、2），F3 ×1（1）。累计按主族在 selection3 的口径上加：F1 +2、F2 +1。
卡覆盖：calibrate_simulator_to_real、structured_screen_observation 首次覆盖。selection3 列出的空白卡里，environmental_injection_attacks、mine_human_screen_videos 仍然空着。

编辑理由：
- **只选 3 篇**。候选只有 6 篇，另外 3 篇分别因同题去重、编辑排除和证据形态排除（第 2 节），不为凑数入选。
- **F0 两篇都没选**。PointerBench 和 SolveBind 都是 F0。按 PROBLEM_CORE，F0 与其他族晋级资格相同，所以这里不是按族排除：两篇各有各的排除理由（第 2 节）。本期因此没有 F0；问题族多样性没有被用作取舍依据。
- **grounding 同题**。IGG 和 PointerBench 都是 grounding benchmark，主卡相同。保留 IGG，理由见第 2 节。high_resolution_target_localisation 已有首期 2412.10840 和第二期 2312.08914；IGG 测的是定位之前让目标出现的那一步，与这两篇不同题，有独立价值，所以在该卡已有 2 篇的情况下仍然入选。

## 2. 排除记录（3 篇）

| ID | q3 | 处理 | 理由 |
|---|---|---|---|
| 2610.31274 PointerBench | C | 同题去重 → 2610.32536（本期）；备选 | 与 IGG 同属 high_resolution_target_localisation 的 grounding benchmark。PointerBench 只测静态单步几何（细边界、字符、caret、区域框）；IGG 测交互中的显露，并用受控干预定位了瓶颈，证据更直接。PointerBench 的总榜还混入了输出协议差异：point-only 专家模型在 134 道区域题上全部记 0；Gemini 3.7 Flash 按 0–1000 坐标统一换算后，从 3.1% 升到 78.1%。字符（27 题）和标点（23 题）分母小；附录里也没有标注错误审计。它的发现（frontier 模型在 caret 和区域上远强于专家模型）仍有价值，下期若 grounding 卡需要补“静态细粒度”一侧，可作为备选 |
| 2610.32223 SolveBind | C | 编辑排除；证据形态不足以单独成篇 | ① **用途**：方法的核心能力是让代理通过 CAPTCHA 和行为式反自动化检测（9 个 HLL 验证族）。作者在 Ethics 中承认可能被滥用；本栏目不以 capability 画报的形式推广绕过人机验证的技术。这一条不涉及 L2 判断是否正确。② **证据**：主表每个骨干只有 90 题（每族 10 题），单次运行；跨 harness 的比较同时改变了工具和接口，作者自己也说收益不能全部归于 supervisor（App. D.5）；唯一干净的对照是 GPT-5.5 单模型上的 binding 消融（185/225 → 161/225）。AndroidWorld 部分证明的是通用工作流收益，不能证明受保护环境的结论。L2 的数字与原文一致，不退回 |
| 2610.22155 Realtime-Bench | J | 证据不够直接；F5 已有 3 篇；下期备选 | 问题成立而且新：冻结环境下的成功率掩盖了思考耗时带来的损失（Claude Opus 5 在 Paused/High 下 70%，Token/High 30%，Wall/High 14%）。但 Paused 和 Token 时钟的全部对比都是 50 题单次运行；同一模型在 Wall Clock 三次运行里能相差 10–12 点（如 GPT-5.6 Sol low 16/14/24，Gemini 3.1 Flash Live low 6/16/18），所以“推理强度在时间压力下效果不一”所依据的 7 题、6 题之差处在噪声范围内。50 题里有 20 题是游戏，Web 子集的结果没有单独报告。F5 前期已有 2602.12276、2310.03720、2601.22781 |

`later_work`：6 篇记录都为 null，本期没有按 later_work 降级。

**下期备选**（仅供参考，不改字段）：2610.22155（若补到 Paused/Token 的重复运行或 Web 子集结果）、2610.31274。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2610.30792 | v1 全文 + App. A–F | 同意 P3/confirmed。**补注（不退回）**：L2 facts[0] 引用 91.1% 对 59.8% 时，没有写明这 200 个工作流是 construction-exposed（App. D.3 Table D5），即构建时就被源回放检查和修复过。档位不变（真机配对证据单独成立），画报限制栏已写明 |
| 2610.31698 | v1 全文（本文无附录）；补读了缓存缺失的 §V-D | 同意。原文 §IV-A 的“4 种模式合计 63.0%”与 Table II 及各节计数反推的结果不一致，属于原文问题，画报不使用（见 `reel/2610.31698/SOURCE.md`） |
| 2610.32536 | v1 全文 + App. A–H | 同意 |
| 2610.22155 | v3 全文 + App. A–D | 同意 P3/confirmed。**补注（不退回）**：子卡 C20 第 1 项 `challenged_with_evidence` 引用的 Token Clock 差异（Claude 44→30、Kimi 24→36）只来自单次运行。更稳的支持在 Wall Clock 的 3 次运行：Sol、Opus 5、Kimi K3、Gemini 3.8 Flash 每次都是 low ≥ high（App. B.1 Table 2），但这些结果混入了服务延迟。下期若选这篇，画报须以此为界 |
| 2610.32223、2610.31274（F0 两篇） | SolveBind v1：正文 + App. D.1/D.4/D.5/D.10；PointerBench v1：全文 + App. A–H | 数字与 L2 一致；没有发现判断错误 |

## 4. correction / 待补

**correction**：无。没有发现需要退回 Sol 单篇修订的 L2 判断错误。上面两条补注只是收窄展示范围，不改变 tier、evidence_status 或 next_action。

**待补清单**（priority=high，但未 confirmed；补齐后由 Sol 单篇做 L2，不在本期直接入选）：

| ID | 当前 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2610.30181v1 | P3 / pending_material | 缓存在 §2 尾部截断、没有附录：只做检索、不做交互访问的消融，judge 的人工校验，task-validity 过滤与 live-drift 处理（Table 4/5、App. C） | 能否把“交互访问”造成的损失与总体难度分开，从而 confirmed |
| 2610.30573v1 | P3 / pending_material | §4.5 在干预结果之前截断：Table 3(a) 原表、85 个任务的选取与重跑规则、标签与 checker 的校验 | 证据选择与偏好触发两类失败的受控隔离能否成立 |
| 2610.31307v1 | P3 / pending_experiment | 记忆来源与测试的隔离、各粒度在相同记忆与上下文预算下的对比、标签真值、13 个配对任务的不确定性 | 是否真的测到了跨任务复用的瓶颈；补不齐就 park |

本期 L3 能从 arxiv.org/html 取到全部 6 个候选的完整 HTML（含附录）。前两篇的截断可以优先走这条路补材料。

## 5. 漏检抽查结果

本期没有新增抽查。progress.md 记录的漏检抽查欠账（每班 10% 取整为 0）尚未清零，本期不处理。

## 6. Reel 成品路径

均在 `reel/<id>/` 下，含 poster.html / poster.png（1400×2000）/ poster.pdf（1 页）/ SOURCE.md / QA.md；每张都在实际打开渲染图后做了视觉 QA。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2610.30792 | `reel/2610.30792/` | 双边界管线 + 哑铃图 + 保留率柱 | ready（第一次渲染有溢出和留白，重做一次后通过） |
| 2610.31698 | `reel/2610.31698/` | 四相位环形缺陷地图 | ready（第一次渲染折行和重叠不过；第二次中心圆文字仍压环，第三次通过，如实记两轮修改） |
| 2610.32536 | `reel/2610.32536/` | 阶段分解 + 逐级干预剥离 | ready（第一次渲染底栏压页脚，重做一次后通过） |

索引：`reel/README.md` 第四期一节；`README.md` 头部统计行 19 → 22。poster.html 若被旧 .gitignore 忽略，保留在本地。本期未操作 git。
