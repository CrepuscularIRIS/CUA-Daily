# selection2 — gui-pc11-20261022-01(第二期)

- run:`gui-pc11-20261022-01`;规则 `problem-core-v1.1`(PROBLEM_CORE.md / SELECTION.md)
- 选题:Opus 5.5 L3,2026-10-22,第二期
- 输入:`l3_shortlist2.tsv` 共 36 篇,按主卡去重后每卡最多 2 篇(17 张主卡 + 2 篇无主卡);q3 为 capability 19 / judgment 17。每篇取最新 L2 记录(36 篇都只有一条 L2,没有 correction),均为 P3 confirmed
- 首期 9 篇不再入选:2412.10840、2505.15810、2307.13854、2508.00935、2404.06474、2409.07429、2406.11896、2407.01476、2503.19537。首期族覆盖为 F0 1、F1 1、F2 5、F3 2、F4 3、F5 1(总控口径)
- 依据:L2 记录字段、facts、biggest_gap 和 subcard_checks;2602.12276、2310.03720 抽查了缓存 core(`research/fulltext/<id>.txt`,40k 裁剪)中的关键数字。**没有读完整原文**,不满足 SELECTION「最终制作条件」
- 不用分数、venue、代码或名气;没有改动任何记录字段

## selection_cutoff

- 记录:`batches/l01–l18.jsonl`、`l24–l91.jsonl`(L2),以及 `l19–l23-correction.jsonl`;36 篇候选的最新记录都在这些文件里
- 候选池:`l3_shortlist2.tsv` 36 篇,不另行扩池
- 日期:2026-10-22。之后新增的 L2 或 correction 不计入本期

## 1. 最终入选(8 篇)

全部为 P3 confirmed。8 篇分属 7 张不同主卡,另有 1 篇无主卡(2609.02154)。表中顺序不代表高低。

| # | ID | tier | q3 | 族 | 主卡 | 入选理由 |
|---|---|---|---|---|---|---|
| 1 | 2606.12666 CAPED | P3 | capability | F4,F0 | 无主卡(unassigned) | new_bottleneck。上传前按任务需要遮蔽截图里无关的私人内容:28 任务上原图 utility .893、泄漏率(WSLR).766,完整方法 .929/.268;去掉任务提取后为 .321/.028,说明隐私和可用性是耦合的。限制:原型跑在 host/server harness 上,未知应用映射为 Public,不是保守策略 |
| 2 | 2504.13936 ViMo | P3 | capability | F0,F2 | learn_and_train_in_gui_world_model | 生成的未来屏幕保留可读文字,能实际用于选候选动作:M3A step acc 46.01→50.16、T3A 43.13→49.20,AndroidWorld 116 任务 +7.76;rollout 深度 1/2/3 的收益与开销放在一起报告。等算力比较和每个候选约 38 秒的开销有待原文核对 |
| 3 | 2602.12276 Agentic TTS(CATTS) | P3 | judgment | F5,F2 | simulated_lookahead_selection | challenges_barrier。按全部 token 计成本时,每步统一增加采样不保证更可靠:WebArena-Lite 三种子 N=1/5/10/20 为 38.8/42.4/43.2/43.0%;Online-Mind2Web 单次运行 22.6→15.1%;仲裁 K=10→20 从 44.6 回落到 42.0。首期 2407.01476 的"预算越大越好"只测到 c=20,本篇是它的直接反证,所以虽然同卡也保留 |
| 4 | 2310.03720 SteP | P3 | judgment | F5,F0 | agent_loop_context_control | challenges_barrier。同样的示例数下,局部上下文加策略栈的 SteP 约 33%,Flat-4K 约 20%、Flat-8K 约 23%;作者原话是 4K→8K "only marginally",部分 intent 还下降。这改变"把上下文加大就能代替控制结构"的判断。限制:子卡的层间交接一项为 fails(信息不足会导致循环),数字取自图,是约数 |
| 5 | 2601.22781 Learning with Challenges | P3 | judgment | F5 | exploration_driven_task_synthesis | 合成数据不是越难越好:同为 500 条、同一生成骨干,挑战系数 α 在 0–2 之间扫描,0.5 最好(约 +4.3 点),另有随机难度分布和去 rollback 对照。限制:单 seed;GUI-Odyssey 用的是离线 AMS,只有 AndroidWorld 是在线评测 |
| 6 | 2311.18751 Sequential-Task Compositions | P3 | judgment | F3 | online_evaluation_methodology | 基本任务成功率高,组合起来未必能做:50 个组合留出,每个评 100 次,提示式 94.0→24.9%、迁移式 85.4→54.8%;同一组合只改指令顺序,迁移式 54.8→31%。和首期 WebArena 同卡,但问的是组合迁移,不是评测构造,有独立价值。限制:只在 MiniWoB 上测,链长与组合推理没有完全分开 |
| 7 | 2312.08914 CogAgent | P3 | judgment | F0,F1 | high_resolution_target_localisation | 三项子卡全部 holds。同数据、计 FLOPs 的对照:base490 用 29.14 TFLOPs 得 40.7,224+cross756 用 10.08 TFLOPs 同样 40.7;同 Cap+OCR 数据下架构收益只有 40.7→41.4,大头来自数据(54.2)。和首期 2412.10840 同卡,但问的是分辨率与计算的取舍,不是坐标读出。指标是离线的 |
| 8 | 2609.02154 MFA Automation(WiP) | P3 | judgment | F0,F4 | 无主卡(unassigned) | new_bottleneck。设备已解锁、可控 GUI、主凭证有效时,同为 15 步动作预算,三档因素配置下分别完成 3/10、6/10、10/10 个服务(人工核查):MFA 完成不再能证明人在场。只证明了可行性,不是破解;防御只是 4 人、116 会话的 pilot,不作为入选依据 |

族覆盖(本期):F0 ×5(1、2、4、7、8),F1 ×1(7),F2 ×2(2、3),F3 ×1(6),F4 ×2(1、8),F5 ×3(3、4、5)。
两期合计:F0 7、F1 2、F2 7、F3 4、F4 5、F5 5。首期按 `selection.md` 的族标签计(F0 2、F5 2),与总控口径(F0 1、F5 1)差在次标签,结论不受影响。

编辑理由:
- **族多样性**:首期 F2 占 5 篇,本期没有以 F2 为主族的入选。2605.19769 OpenComputer 证据很强,但因 F2 已饱和,且与首期 2508.00935 同卡,只列为首选备选。
- **F5 三篇**:它们分属 3 张卡,检验的是三个不同的"越多越好"——候选采样(3)、prompt 上下文(4)、数据难度(5)。按问题不同处理,不视为同题。
- **F3 只增加 1 篇**:其余 F3 候选要么只有离线证据(2412.09362、2406.03679、2202.02312),要么与首期同题(2509.25140、2306.07863),要么与 2311.18751 同卡且证据更弱(2105.13231)。见第 2 节。
- **q3 偏 judgment(6:2)**:capability 一侧,未覆盖卡上的候选或有测试流泄漏(2605.06761),或缺等预算消融(2303.17491),或在首期已因证据被排除(2404.02475、2409.14337、2306.07863、2401.10935、1802.08802 等)。这里不按配额补位。两期合计 capability 7 / judgment 10。
- **安全簇两席**:1 和 8 都是无主卡的移动端隐私/认证问题,和首期 2508.00935 的"有害执行"不同题。注入攻防卡(2407.09295、2408.02544、2410.09006、2503.09241)维持首期的排除理由。
- **新覆盖的卡**:本期补上 agent_loop_context_control、exploration_driven_task_synthesis、learn_and_train_in_gui_world_model 三张。3、6、7 落在首期已覆盖的卡上,各自写明了独立价值。
- 本期只选 8 篇,没有凑满 9 篇:剩下的 capability 候选都达不到"问题最清楚、证据最直接"。

### 原文核对状态与制作前必查

8 篇均**未核对完整原文**。制作前须逐篇读完整原文和支撑结论的附录;若发现 L2 判断错误,暂停该篇,写 correction 退回 Sol 单篇修订。各篇重点:

| ID | 必查 |
|---|---|
| 2606.12666 | 泄漏按不同成功子集比较是否公平;未知应用映射 Public 对隐私结论的影响;连接评测只有 9 个任务 |
| 2504.13936 | 在线协议全文;前瞻与基线是否等算力;70 人图像评估不能当作打分器校准 |
| 2602.12276 | 缓存 core 在 §4.1 开头截断:CATTS 动态阈值主表、附录 C 的 judge 可靠性、附录 E(Plan-and-Act)。只把"统一加采样不保证更好"写成确认结论 |
| 2310.03720 | Flat/SteP 的确切数值与方差;同示例数 few-shot 对照;额外模型调用的成本 |
| 2601.22781 | semantic 难度标签的来源;合成数据与测试是否隔离;等合成计算;是否报告多 seed |
| 2311.18751 | 链长与组合推理怎么拆;不同代理之间的模型、检索示例和预算差异 |
| 2312.08914 | Table 5/6 是否同数据、同步数;离线坐标精度的边界 |
| 2609.02154 | 10 个服务的选取和人工核查规则;权限模型的假设边界;正文是否混入防御 pilot 的结论 |

## 2. 排除记录(28 篇)

"同卡→首期"指该卡已有首期入选,本篇没有足以单独成篇的独立价值。

| ID | 主卡 | q3 | 处理 | 理由 |
|---|---|---|---|---|
| 2404.02475 Prompt2Task | agent_initiated_user_interaction | C | 同题去重 → 2503.19537(首期) | 维持首期判断:90.68/95.24 含用户协助,不是自主完成率,子卡 1 项 fails |
| 2602.11750 AmbiBench | agent_initiated_user_interaction | J | 同题去重 → 2503.19537(首期);备选 | 真机加 κ=.91 的人工验证都较强,但仍是"何时该问用户"同题;用户由 GPT-5 模拟,ambiguous 档 TSR=0 是按设计构造的;关闭 ASK 的实验只抽本已成功的样本 |
| 2303.17491 RCI | agent_loop_context_control | C | 同卡去重 → 2310.03720 | 没有等调用预算的纯批判对照,critic 准确率未测;SteP 的同示例对照更直接 |
| 2605.06761 Weblica | calibrate_simulator_to_real | C | 证据不够直接(本卡唯一) | 技能组由 Online-Mind2Web **测试任务**的轨迹归纳而来,24.8→35.6 不能当作未见任务迁移(F4 信息访问问题);pass@k 含多次尝试的预算。若改用非测试流归纳技能并重做,可重新审 |
| 2407.09295 Mobile GUI attacks | environmental_injection_attacks | C | 安全簇,维持首期判断 | 缓存缺 §4 成功规则,资产损失与判定可靠性都未确认 |
| 2408.02544 Environmental Distractions | environmental_injection_attacks | J | 安全簇,维持首期判断 | 只有模拟单步,没有成对的无干扰基线;§5 对抗扩展只有 8 个目标 |
| 2306.07863 Synapse | experience_memory_retrieval | C | 同题去重 → 2409.07429(首期) | 记忆带来的 OOD 增益弱,56% 是组合指标,不能归于记忆 |
| 2509.25140 ReasoningBank | experience_memory_retrieval | J | 同题去重 → 2409.07429(首期) | 同为 WebArena 同环境流式记忆;失败记忆 46.5→49.7 是增量;自判校准只在 Shopping 子集(72.7%) |
| 2409.14337 MobileViews | exploration_driven_task_synthesis | C | 同卡去重 → 2601.22781 | 维持首期:VLM 只在 38/86 个应用上无卡住遍历,规模收益不单调 |
| 2401.10935 SeeClick | high_resolution_target_localisation | C | 同卡→首期 2412.10840;本期该卡给了 2312.08914 | 收益来自混合预训练包,不能归于 grounding 目标本身 |
| 2410.09006 UI Operation Impacts | injection_defense_isolation | J | 安全簇,维持首期判断 | 最佳一致率 58.37%,没有标注者之间一致性,高危类别漏报未知 |
| 2503.09241 In-Context Defense | injection_defense_isolation | C | 安全簇,维持首期判断(备选) | 只对已知、非自适应攻击;EIA 把拒绝计为成功;零 ASR 推不出零误报。安全簇本期两席给了问题更新、证据更直接的 1、8 |
| 2412.09362 Falcon-UI | learn_and_train_in_gui_world_model | J | 同卡去重 → 2504.13936 | 只有离线表征收益,没有在线验证;ViMo 有 AndroidWorld 在线结果 |
| 2406.13264 WONDERBREAD | learned_outcome_and_process_judges | J | 同卡→首期 2404.06474;维持首期判断 | SOP 审计缺口清楚,但负例是合成的、只覆盖 4 个站点,也没有下游使用证据 |
| 2505.21496 UI-Genie | learned_outcome_and_process_judges | C | 同卡→首期 2404.06474;F2 已饱和 | 去掉历史后 F1 79.6→61.3 是直接证据;但 AndroidLab 18.1→38.7 混入了同一 RM 驱动的搜索、筛选和再训练循环,不能归于奖励可信度 |
| 2406.13719 GUI Action Narrator | mine_human_screen_videos | C | 独立性不足,维持首期判断 | 离线描述组件;GPT-4 指标未经人工校准 |
| 2105.13231 AndroidEnv | online_evaluation_methodology | C | 同卡去重 → 2311.18751 | 平台约束(异步时钟、可组合触屏)成立,但只有 6 个任务的基线,奖励没有双侧验证 |
| 1808.09132 NL→Web Elements | planner_grounder_interface | C | 维持首期判断 | 按页面而非站点划分;没有下游任务 |
| 2202.02312 MoTIF | planner_grounder_interface | J | 维持首期判断 | 可行性实验是 oracle 探索上界;离线严格序列匹配,还带低层指令 |
| 2508.05615 GUI-RCPO | rule_reward_single_step_rl | C | 同卡→首期 2505.15810 | 在同一数据集上做无标签适应,专用 point 模型收益很小 |
| 2606.05597 AsyncWebRL | rule_reward_single_step_rl | J | 同卡→首期 2505.15810;备选(F1/F5) | 长度归一化削弱失败惩罚是清楚的机制问题,但单 seed,+2.5pp,系统提速混入了其他工程变化,文中两处提速数字不一致 |
| 2502.15760 Digi-Q | simulated_lookahead_selection | C | 同卡去重 → 2602.12276;备选(F0) | 消融与 3 次重复都扎实,但它是首期 DigiRL 的同谱系后续(对照离线 DigiRL 59.0→71.2),作为第二期独立一席的价值较弱;自动成功评估器没有校准 |
| 2010.04295 Widget Captioning | structured_screen_observation | C | 独立性不足,维持首期判断 | 可访问性组件,没有 agent 任务收益 |
| 2201.04100 Denoise UI Layouts | structured_screen_observation | J | 独立性不足,维持首期判断 | 证明了原始布局不能直接当标签,但没测下游训练收益 |
| 1802.08802 Workflow-Guided Exploration | trajectory_level_policy_training | C | 同卡→首期 2406.11896 | 只在 MiniWoB 上测 |
| 2406.03679 Data Scale on UI Control | trajectory_level_policy_training | J | 同卡→首期 2406.11896,维持首期判断 | ID/OOD 扩展差距是有用的 F3/F5 判断,但只有一个骨干、无障碍文本、离线代理指标,百万级预测是外推 |
| 2207.01206 WebShop | verifiable_execution_reward | C | 同卡→首期 2508.00935 | checker 与真实需求是否一致没有独立量化 |
| 2605.19769 OpenComputer | verifiable_execution_reward | J | 同卡→首期 2508.00935;F2 已饱和;**首选备选** | verifier 113/120 对 LLM judge 95/120,修复 checker 后 85.2→94.1%,证据直接;但前后用的是同一批 120 条样本,可能乐观,也没有误接受/误拒绝的双侧率。若下期 F2 有空位,优先考虑 |

`later_work`:36 篇记录均为 null,本期没有按 later_work 降级。2502.15760 与首期 2406.11896 的谱系关系是编辑判断,不改字段。

## 3. 待补清单(priority=high 但未确认)

按 L2 最新记录统计:priority=high 且未 confirmed 的共 347 篇。其中缺材料 38 篇(needs_material 16 + assessed pending_material 22);pending_experiment 292(含 3 篇 out_of_scope);pending_method 14。补齐后由 Sol 单篇做 L2,不在此直接入选。

### 3a. 缺材料(38),按与本期空缺的关系排列

**未覆盖或薄弱卡/族上的(补齐可能改变下期选题)**:

| ID | 主卡 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2406.12814 | environmental_injection_attacks | §5.2–5.3 干净与受攻击的 evaluator/value 条件 | 注入簇是否终于有终态判定的候选 |
| 2504.14064 | environmental_injection_attacks | BrowserGym 攻击、组合攻击与防御结果表 | GUI 专属 Q1 |
| 2507.05445 | environmental_injection_attacks | §V 轨迹 | counterexample 是否成立 |
| 2609.16732 | environmental_injection_attacks | 功能保持/不可察觉的操作与人类实验段、原 APK 对照 | 新威胁能否 confirmed |
| 2610.09469 | injection_defense_isolation | §5、证明与执行绑定细节 | 有没有"非自适应"以外的隔离式防御 |
| 2504.13805 | mine_human_screen_videos | §4 DemoParser/KnowSeeker,示范与目标的关系 | 该卡唯一可能的 confirmed 候选 |
| 2008.05132 | structured_screen_observation | §3 主实验 | 定 null→P3 与否 |
| 2608.06171 | structured_screen_observation | §6 余部、§8 CV/泄漏校正 | router 训练与评测是否分离 |
| 2504.06821 | experience_memory_retrieval | 主要结果、消融、迁移章节 | F3 未见站点迁移 |
| 2609.36488、2610.24453 | experience_memory_retrieval | 方法与主实验 | F3/F4 经验流与测试流是否隔离 |
| 2608.27477 | agent_loop_context_control | §5 跨骨干 harness 消融 | F1 归因 |
| 2506.15425 | high_resolution_target_localisation | §4 余部、§5 PSS 校准与裁剪消融 | Q4 |

**其余(25)**:2310.18331、2409.10741、2506.16042、2606.29472(agent_loop_context_control);2402.07456、2609.03438、2610.16720、2610.22200(planner_grounder_interface);2410.06703、2505.03570、2509.04198、2512.00756、2603.04949、2604.06182、2604.06367、2604.07929、2607.26041、2609.06059、2610.19900(online_evaluation_methodology);2501.12326、2602.16855(trajectory_level_policy_training);2509.11939、2512.22047(agent_initiated_user_interaction);2509.23263、2512.15431(learned_outcome_and_process_judges)。所缺章节见各条 L2 的 `biggest_gap`。

### 3b. 缺受控实验或方法核对(306)

pending_experiment/pending_method 按主卡:online_evaluation_methodology 63、agent_loop_context_control 38、environmental_injection_attacks 32、experience_memory_retrieval 27、planner_grounder_interface 25、injection_defense_isolation 17、learned_outcome_and_process_judges 17、trajectory_level_policy_training 15、exploration_driven_task_synthesis 14、agent_initiated_user_interaction 12、high_resolution_target_localisation 11、structured_screen_observation 9、learn_and_train_in_gui_world_model 7、verifiable_execution_reward 6、mine_human_screen_videos 4、simulated_lookahead_selection 4、rule_reward_single_step_rl 3、calibrate_simulator_to_real 2、无主卡 3。缺口多为等预算/同信息对照、judge 双侧校准和在线验证,详见各条 L2 的 `biggest_gap`。

### 3c. progress.md 记录的补核组

B 组(同材料下仍为 to_l2,80 篇)和 C 组(pending_* 状态,479 篇)仍待新材料或新实验后补核,本期没有处理。

## 4. 漏检抽查结果

本期没有新增抽查,沿用首期 `selection.md` 第 4 节(26 篇抽查,5 篇改判)。改判升到 P3 的 4 篇都不在 `l3_shortlist2.tsv` 中。

## 5. Reel 成品路径

本期 8 篇待制作,存入 `reel/<paper-id>/`。每篇先完成第 1 节"制作前必查"和原文核对,做过实际视觉 QA 后才记为 ready。

## 画报核对后补充勘误(总控)

- **2310.03720 SteP(口径修正,档位不变)**:原写"同样示例数下策略栈约 33%,扁平约 20-23%"混淆了两张表——WebArena 的 33%/20%/23% 来自表 1,Flat 是同一批策略拼接后截断到 4K/8K,示例数未对齐;真正的同示例数对照在图 7(MiniWoB++,≤7 示例,差距 5-11pp)。画报已分开呈现。
- **2602.12276 CATTS(非直接反证,档位不变)**:与首期 Tree Search 并非"直接反证"——首期加搜索预算 c(可回溯、可重置环境、程序判定),本文加候选数 N(不可回溯、真实网站、LLM 判定);两者是互补的边界证据。画报天平已按此口径绘制。
- **2504.13936 ViMo(子卡修订建议)**:L2 子卡第 4 项(预测深度/收益/开销联合检查)建议从 holds 改为 partial——原文深度消融只有准确率,开销未量化。待 Sol 修订。
- **2312.08914 CogAgent(范围收窄)**:"架构和数据分开"是沿表 6 逐步拆,非 2×2 对照;消融预训练步数未报告;"等算力"不准确(交叉分支两档都更省 0.35×/0.43×)。
