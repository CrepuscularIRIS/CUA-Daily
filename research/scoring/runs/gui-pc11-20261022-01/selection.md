# selection — gui-pc11-20261022-01

- run:`gui-pc11-20261022-01`;规则 `problem-core-v1.1`(PROBLEM_CORE.md / SELECTION.md)
- 选题:Opus 5.5 L3(2026-10-22,第 2 版,覆盖第 1 版)
- 输入:重建后的 `l3_shortlist.tsv` 共 52 篇,覆盖 16 张主卡(q3:capability 29 / judgment 23;族:F0 22、F2 18、F3 17、F4 17、F5 7、F1 5)。第 1 版短名单只有 capability 29 篇,judgment 与 F1 全部缺席,已由总控修正。每篇取最新记录,52 篇都有 L2,均为 P3 confirmed
- 依据:只看 L1/L2 记录字段、facts 和 biggest_gap,**未读完整原文**。`research/fulltext/<id>.txt` 是 40k 的裁剪 core,达不到 SELECTION「最终制作条件」;制作前须逐篇读完整原文和所需附录
- 不用分数、venue、代码或名气;没有改动任何记录字段

## 1. 最终入选(9 篇)

全部为 P3。capability 与 judgment 并列,各占 5 篇和 4 篇。9 篇分属 9 张不同主卡,表中顺序不代表高低。

| # | ID | tier | q3 | 族 | 主卡 | 入选理由 |
|---|---|---|---|---|---|---|
| 1 | 2412.10840 Attention-driven GUI Grounding | P3 | judgment | F1 | high_resolution_target_localisation | F1 代表,challenges_barrier。在同一预训练骨干、不做 GUI 微调的条件下,用注意力定位胜过直接生成坐标(ScreenSpot 36.0→54.8,OCG 48.1→84.5),把"看不见目标"与"坐标输出接口差"分开。限制:K 和阈值靠性能扫描选定,没有独立调参集;结论只说明骨干里已有可用的空间信号,不等于坐标 SFT 无用 |
| 2 | 2505.15810 GUI-G1 | P3 | judgment | F2,F5 | rule_reward_single_step_rl | challenges_barrier。受控奖励实验显示,只用 hit 奖励和只用 IoU 奖励时框尺寸朝相反方向被投机;推理越长,定位越差。这会改变定位 RL 里默认用长 CoT 和形状奖励的做法。长 CoT 的结论只来自相关/分层分析,只有静态定位实验 |
| 3 | 2307.13854 WebArena | P3 | judgment | F2,F3 | online_evaluation_methodology | 问题最清楚:按参考动作序列匹配会错判合法的替代解法。可复位的功能网站加上终态检查直接回应这个问题;GPT-4 成功率 14.41%,人类 78.24%。must_include/fuzzy_match 的双侧误判还没审计 |
| 4 | 2508.00935 Measuring Harmfulness of CUAs | P3 | judgment | F2,F0 | verifiable_execution_reward | 聊天中拒绝不代表在电脑上不执行有害任务。52 个恶意电脑任务用执行检查器判定终态,GUI 与终端分开报告(GPT-5 终端 42%、GUI 21%)。checker 双侧审计和良性监控的误报还没确认 |
| 5 | 2404.06474 Autonomous Evaluation and Refinement | P3 | capability | F2,F4 | learned_outcome_and_process_judges | 评估器结果与执行 oracle 和人工判定都做了对照(WebArena 82.1%),又实际用于下游改进(Android 15%→26%),并报告了假阴性的副作用。不能证明它能安全地充当无限优化的 reward |
| 6 | 2409.07429 Agent Workflow Memory | P3 | capability | F3,F4 | experience_memory_retrieval | 只用已完成的查询归纳工作流,不访问未来查询;WebArena 15.0→35.5,跨模板 20.5→33.2。边界:规则工作流 35.6 与 LM 工作流 35.5 相当,收益不能只归于语义抽象 |
| 7 | 2406.11896 DigiRL | P3 | capability | F3 | trajectory_level_policy_training | 真实 Android 上,同一骨干的离线→在线 RL 超过静态模仿和在线 FBC(General 71.9 vs 61.5,Shopping 67.2 vs 57.8,数字取 Table 1)。judge 没做双侧/对抗校验,任务都偏短 |
| 8 | 2407.01476 Tree Search for LM Agents | P3 | capability | F0,F5 | simulated_lookahead_selection | 本卡唯一候选。与 GPT-4o 基线匹配时 VWA 18.9→26.4、WA 15.0→19.2,并有近似算力匹配的消融;自评 value 37.0,真值 value 43.5。前提是环境可以重置/重放,不可逆的真实网站不适用 |
| 9 | 2503.19537 Agent-Initiated Interaction | P3 | capability | F2,F4 | agent_initiated_user_interaction | benchmark/负结果:772 个 episodes 截断在首次必要交互处,现有代理判断"何时该问用户"的 precision 只有 0.08–0.19。问题新、测量直接;消息质量只在 true positive 上测 |

族覆盖:F0 ×2(4、8),F1 ×1(1),F2 ×5(2、3、4、5、9),F3 ×3(3、6、7),F4 ×3(5、6、9),F5 ×2(2、8)。

编辑理由:
- F2 占 5 篇,但其中 3 篇的 F2 是第二标签,而且 F2 本来就是候选池第二大族(60/162)。
- F0 在池中占 77/162,这里只入选 2 篇。原因是 F0 的强候选(Synatra、2509.23866、2410.16464、MCPWorld)都在同卡比较中因证据不够直接而落选,并非按类型排除,逐条理由见第 2 节。
- 安全方向只留 1 席,见第 2 节"安全簇"。

原文核对状态:9 篇均**未核对**,4 篇 judgment 的缓存文本都在 `research/fulltext/`。制作前逐篇读完整原文和附录;若发现 L2 判断错误,暂停该篇,写 correction 退回 Sol 单篇修订。

## 2. 排除记录(43 篇)

"安全簇"指 agent 被诱导执行偏离用户或有害动作的问题,横跨 environmental_injection_attacks、injection_defense_isolation、verifiable_execution_reward 三张卡。本期只留 2508.00935:它用执行检查器直接判定终态,其余多以单步匹配或分类一致性代替终态。

| ID | 主卡 | q3 | 处理 | 理由 |
|---|---|---|---|---|
| 2404.02475 Prompt2Task | agent_initiated_user_interaction | C | 同题去重 → 2503.19537 | 自主完成率与用户协助完成率并列(90.68/95.24 不是自主完成),子卡 1 项 fails |
| 2405.11120 Latent State Estimation | agent_loop_context_control | C | 备选 | 独立问题,但证据不够直接:ReAct 的提升 p=.078,出错时错误检测仅 25.9%,额外调用没有隔离 |
| 2406.08451 GUIOdyssey | agent_loop_context_control | C | 同题去重 → 2307.13854 | 离线跨应用 SR 是全参考匹配;"静态指标不能代表完成"由 WebArena 直接测 |
| 2410.00467 Dynamic Planning | agent_loop_context_control | J | 证据不足 | 只有 20 个 general 任务,历史长度效应仅 45.45→43.94;离线评测,含 reference 的结果还用到了测试流 |
| 2503.16788 CoT for Mobile Agents | agent_loop_context_control | J | 备选(F1/F5) | "推理收益非单调"是有价值的判断,但缺等算力和重复试验;67 个错误中 47.8% 是弱评估器的假阴性,混杂较重。F1 已由 2412.10840 代表 |
| 2407.09295 Mobile GUI attacks | environmental_injection_attacks | C | 安全簇 | 缓存缺 §4 成功规则,资产损失与判定可靠性未确认 |
| 2408.02544 Environmental Distractions | environmental_injection_attacks | J | 安全簇 | 只有模拟单步、没有成对的无干扰基线;§5 的对抗扩展只有 8 个目标 |
| 2409.11295 EIA | environmental_injection_attacks | J | 安全簇 | 截图/HTML 双通道问题清楚,但 opacity 0 时 full-request ASR 为 0,ASR 不是已验证的外传 |
| 2410.17401 AdvAgent | environmental_injection_attacks | C | 安全簇(首选备选) | 黑盒可控注入,证据直接;但 ASR 是单步 triplet 匹配,不是终态 |
| 2502.20383 Why Web Agents More Vulnerable | environmental_injection_attacks | J | 安全簇(F1 备选) | 与 2508.00935 同题(拒绝不等于不执行);只有 10 条请求各跑 3 次,逐步消融也不是完整因子设计 |
| 2410.09006 UI Operation Impacts | injection_defense_isolation | J | 安全簇 | 与人类标签的一致率最佳只有 58.37%,没有标注者之间的一致性,高危类别漏报未知 |
| 2503.09241 In-Context Defense | injection_defense_isolation | C | 安全簇 | 只针对已知、非自适应的攻击;零 ASR 推不出零误报 |
| 2507.14293 WebGuard | injection_defense_isolation | C | 安全簇 | 标签计数不一致(4956 vs 4939),没有实际门控试验 |
| 2306.07863 Synapse | experience_memory_retrieval | C | 同题去重 → 2409.07429 | 记忆带来的 OOD 增益弱,56% 不能归于记忆 |
| 2409.14337 MobileViews | exploration_driven_task_synthesis | C | 同卡去重 → 2409.15637 后整卡落选 | 规模收益不单调;VLM 只在 38/86 个应用上无卡住遍历 |
| 2409.15637 Synatra | exploration_driven_task_synthesis | C | 备选(F0) | 问题新(间接知识→示范),但 WebArena 绝对值只到 6.28,两类合成作者都承认有真实性缺口;不如入选篇直接 |
| 2605.16024 ScreenSearch | exploration_driven_task_synthesis | J | 证据范围窄 | 配对消融扎实,但只有 3 个应用、50 步;下游指标是 teacher-forced 离线 |
| 2401.10935 SeeClick | high_resolution_target_localisation | C | 同卡去重 → 2412.10840 | 能力问题清楚,但 L2 指出其收益来自混合预训练包,不能归于 grounding 目标本身;2412.10840 在同骨干上直接检验定位瓶颈在哪 |
| 2501.13896 GUI-Bee | high_resolution_target_localisation | C | 同卡去重 → 2412.10840 | 需要先在目标环境探索;测试去重与等 API 预算未核 |
| 2504.04716 Grounding Robustness | high_resolution_target_localisation | J | 同卡去重 → 2412.10840 | ε 没经过人工可察觉性验证,目标固定在角落;效应因模型而异(OS-Atlas 0.43%) |
| 2506.03143 GUI-Actor | high_resolution_target_localisation | J | 同题去重 → 2412.10840 | 同一问题(感知 vs 坐标解码),对照也受控;但需要训练动作头,冻结骨干只恢复部分(22.9 vs 全量 40.7),归因不如免训练的 2412.10840 干净 |
| 2604.14956 FedGUI(漏检升 P3) | high_resolution_target_localisation | J | 同卡去重 → 2412.10840 | 离线动作指标;OS 效应混入了数据来源差异 |
| 2406.13264 WONDERBREAD | learned_outcome_and_process_judges | J | 同卡去重 → 2404.06474 | SOP 审计缺口很清楚(F1 0.27,完成判定 0.90),但负例是合成的、只覆盖 4 个站点,也没有下游使用证据 |
| 2406.13719 GUI Action Narrator | mine_human_screen_videos | C | 独立性不足 | 离线描述组件;GPT-4 指标未经人工校准,38.6 用的是真值时间定位 |
| 2306.06070 Mind2Web | online_evaluation_methodology | C | 同卡去重 → 2307.13854 | 离线单步、给真值历史;WebArena 直接测功能完成 |
| 2311.18751 Sequential-Task Compositions | online_evaluation_methodology | J | 同卡去重 → 2307.13854(备选) | 组合/顺序留出设计好;但只在 MiniWoB,链长与组合推理没有分离 |
| 2312.13108 ASSISTGUI | online_evaluation_methodology | C | 同卡去重 → 2307.13854 | 100 个任务;检查器双侧误判和 critic 准确率未知 |
| 2506.07672 MCPWorld(漏检升 P3) | online_evaluation_methodology | J | 同卡去重 → 2307.13854 | 用内部状态验证的思路有价值,但 GUI-only 条件允许用 bash;双接口比较 AgentStudio 已做过;新 checker 的误判率未知 |
| 1808.09132 NL Commands to Web Elements | planner_grounder_interface | C | 同题去重 → 2412.10840 定位簇 | 按页面划分而非按站点;未涉及下游任务 |
| 2103.16057 RUSS(漏检升 P3) | planner_grounder_interface | C | 证据规模小 | 5 个任务、12 名参与者,依赖预先给出的逐条说明 |
| 2202.02312 MoTIF | planner_grounder_interface | J | 证据不够直接 | 可行性实验用的是 oracle 探索上界;序列匹配是离线的,还带低层指令 |
| 2410.16464 API-Based Web Agents | planner_grounder_interface | J | 备选(F0) | 混合接口 38.9% 的收益里包含人工补充的端点,文档准备成本未量化 |
| 2508.05615 GUI-RCPO | rule_reward_single_step_rl | C | 同卡去重 → 2505.15810 | 在同一数据集上做无标签适应,专用 point 模型收益很小 |
| 2010.04295 Widget Captioning | structured_screen_observation | C | 独立性不足 | 可访问性组件,没有 agent 任务收益 |
| 2101.04893 Screen Recognition | structured_screen_observation | C | 独立性不足 | 缺口测量扎实,但缓存缺用户研究章节,与 agent 的关系间接 |
| 2201.04100 Denoise UI Layouts | structured_screen_observation | J | 独立性不足 | 证明了原始布局不能直接当标签,但没测下游训练收益 |
| 2405.00516 Navigating WebAI | structured_screen_observation | J | 备选(F1) | 打乱 ref 同时改变了编码分布,只评 40 个 MiniWoB 任务,正文与摘要数字不一致 |
| 1802.08802 Workflow-Guided Exploration | trajectory_level_policy_training | C | 同卡去重 → 2406.11896 | 只在 MiniWoB 上测 |
| 2406.03679 Data Scale on UI Control | trajectory_level_policy_training | J | 同卡去重 → 2406.11896 | 只有一个骨干,用无障碍文本、离线代理指标,百万级预测是对数线性外推 |
| 2503.05143 FedMABench | trajectory_level_policy_training | J | 同卡去重 → 2406.11896 | 应用标签由 GPT-4o 分类,指标是 TF-IDF 匹配 |
| 2509.23866 异步 GUI RL(漏检升 P3) | trajectory_level_policy_training | C | 同卡去重 → 2406.11896 | 崩溃反例只在 45 个训练任务子集上,不是独立测试集 |
| 2207.01206 WebShop | verifiable_execution_reward | C | 同卡去重 → 2508.00935 | 有"reward 升、SR 降"的独立价值,但 checker 与真实需求是否一致没有独立量化 |
| 2501.01149 A3 | verifiable_execution_reward | C | 同卡去重 → 2508.00935 | v3 结果晚于首版,校准集是否互斥划分未核 |

`later_work`:52 篇记录均为 null,本次没有按 later_work 降级。

## 3. 待补清单(priority=high 但未确认)

截至本 run 共 603 篇:L1 pending_method 497 篇(没进 L2,受 266 篇预算限制)、L2 pending_experiment 66、L2 pending_method 3、缺材料类 37(needs_material 30 + L2 assessed pending_material 7)。补齐后由 Sol 单篇做 L2,不在此直接入选。

### 3a. 缺材料(37)

**先查范围(19 篇)**:现有材料看不出代理是否实际操作 GUI/浏览器。需要补方法里的动作/观测接口和轨迹样例:若只用 API/文件/终端,转 out_of_scope/exclude;若有 GUI 操作面,则为潜在 P3,再核对判定真值和首版前的同条件比较。
2402.07456、2407.19056、2505.14963、2508.04026、2603.11862、2604.01438、2604.02947、2604.05912、2604.13954、2604.28181、2605.03242、2606.03889、2606.20724、2607.19865、2608.06862、2608.23035、2608.26546、2609.06059、2609.29892

**缺具体章节(18 篇)**:

| ID | 主卡 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2008.05132 | structured_screen_observation | §3 主实验、方法与结果表 | 定 null→P3 与否、Q4 |
| 2308.03688 | online_evaluation_methodology | 两项网页任务的交互协议、执行真值、分项结果 | 是否有独立的 GUI 诊断价值 |
| 2310.18331 | agent_loop_context_control | 方法与主实验(只有摘要) | 长度/反馈受控消融,Q4 |
| 2406.12814 | environmental_injection_attacks | §5.2–5.3 干净与受攻击 evaluator/value 条件 | 组件是否放大攻击,能否 confirmed |
| 2409.10741 | agent_loop_context_control | 抽象任务构造、RAG 库时间切分、检查器、基线预算 | Q4 与泄漏排除 |
| 2410.06703 | online_evaluation_methodology | §4 主实验;版本数量冲突 | 策略违规测量结果 |
| 2411.06559 | simulated_lookahead_selection | 与首版前 2410.13232 的同条件比较;v2 主张属于哪次修订 | Q2 是否开放 |
| 2501.12326 | trajectory_level_policy_training | §3–4、§5 后段、OSWorld infeasible 的分母 | 方法归因 |
| 2504.06821 | experience_memory_retrieval | 主要结果、消融、迁移章节 | 程序化技能的验证与迁移收益 |
| 2504.13805 | mine_human_screen_videos | §4 DemoParser/KnowSeeker、示范与目标的关系 | 排除目标答案注入 |
| 2504.14064 | environmental_injection_attacks | BrowserGym 攻击/组合/防御结果表 | GUI 专属的 Q1 |
| 2505.03570 | online_evaluation_methodology | 主实验与 validator 审计 | 检查器双侧误差,能否 confirmed |
| 2506.15425 | high_resolution_target_localisation | §4 余部和 §5 的 PSS 校准与裁剪消融 | Q4 |
| 2506.16042 | agent_loop_context_control | 人类参考轨迹的构建方式、同接口预算 | 效率比较是否成立 |
| 2507.05445 | environmental_injection_attacks | §V 轨迹 | counterexample 是否成立 |
| 2509.04198 | online_evaluation_methodology | 原方法、任务数、同等权限基线、扰动实验 | Q1/Q4 |
| 2509.11939 | agent_initiated_user_interaction | 系统 §4、N14 比较 §5 | 用户控制与负担的效果 |
| 2509.23263 | learned_outcome_and_process_judges | 方法与主实验(只有摘要) | 准则泄漏、等预算消融、真值 |

### 3b. 已读全文核心但缺受控实验(L2 pending_experiment 66 / pending_method 3)

这些论文保留潜在 P3,缺口多为等预算/同信息对照、judge 双侧校准和在线验证,详见各条 L2 的 `biggest_gap`。按主卡列出:

- online_evaluation_methodology:2403.07718、2403.11905、2404.09992、2406.01623、2406.10227、2406.12373、2410.23252、2412.18426、2501.07572、2502.17903、2503.07919、2505.11891、2505.21279、2506.01616、2506.14477、2507.19478(method)、2508.09057、2508.09241、2509.01619、2509.21782、2608.08392
- planner_grounder_interface:2311.07562、2402.07945、2403.03186、2409.01927、2502.18525、2504.10127、2505.12842、2505.14141、2509.20729、2512.24965
- environmental_injection_attacks:2502.13053、2503.20279、2504.11281、2505.12981、2505.14289、2505.14418、2509.10723
- trajectory_level_policy_training:2202.08137、2408.07199、2505.12493、2506.20332、2507.04103
- experience_memory_retrieval:2308.15272、2404.05902、2505.21964、2506.10387、2507.21071(method)
- high_resolution_target_localisation:2503.00401、2506.11127、2507.23779、2509.11548
- injection_defense_isolation:2503.18492、2503.22738、2507.10610
- agent_initiated_user_interaction:1909.00031、2501.16609、2508.19679
- structured_screen_observation:2402.17553、2409.10811、2507.12844
- exploration_driven_task_synthesis:2410.19609、2505.19095、2508.04700
- mine_human_screen_videos:2406.10819、2410.19100
- 其他:2410.13232(learn_and_train_in_gui_world_model)、2507.03730(agent_loop_context_control)、2508.04389(rule_reward_single_step_rl,method)

### 3c. L1 pending_method 未进 L2(497)

按主卡:online_evaluation_methodology 103、agent_loop_context_control 56、environmental_injection_attacks 52、experience_memory_retrieval 42、learned_outcome_and_process_judges 37、injection_defense_isolation 36、planner_grounder_interface 34、structured_screen_observation 21、high_resolution_target_localisation 21、verifiable_execution_reward 17、trajectory_level_policy_training 16、agent_initiated_user_interaction 14、exploration_driven_task_synthesis 11、learn_and_train_in_gui_world_model 11、rule_reward_single_step_rl 7、simulated_lookahead_selection 6、calibrate_simulator_to_real 6、mine_human_screen_videos 3、无主卡 4。都还缺方法/实验核对,按 PROBLEM_CORE 第 5 节留到下一期,或等预算放宽后再做 L2。

## 4. 漏检抽查结果

26 篇抽查(seed 20261022,取自 P0/P1、F0、needs_material、park)中 5 篇改判,漏检率约 15%,集中在缺材料类:

| ID | 原判(L1) | 新判(L2) | 本期去向 |
|---|---|---|---|
| 2103.16057 | P2 | P3 confirmed(capability,F0) | 进短名单;因证据规模小未入选 |
| 2604.14956 | needs_material / null | P3 confirmed(judgment,F3) | 进短名单;同卡去重 → 2412.10840 |
| 2509.23866 | P2 | P3 confirmed(capability,F0/F2) | 进短名单;同卡去重 → 2406.11896 |
| 2506.07672 | P2 | P3 confirmed(judgment,F2/F0) | 进短名单;同卡去重 → 2307.13854 |
| 2503.13843 | needs_material / null | P1,park | — |

另:2503.02950 的状态由 needs_material 变为 assessed,但档位仍为 null(to_l2),不算改判。

## 5. Reel 成品路径

待制作。按 OPUS_REEL_PROMPT.md 存入 `reel/<paper-id>/`(9 个目录对应第 1 节的 ID)。每篇先完成原文核对,做过实际视觉 QA 后才记为 ready。

## 画报核对后的修订与编辑取舍(总控记录)

- **2307.13854 WebArena(P3→P2,保留入 Reel)**:Opus 核对发现论文未实测"动作序列匹配误判率",q1 修正为 asserted,按封顶规则降 P2(revision: batches/l19-correction.jsonl)。**编辑理由保留**:可复位自托管环境+终态检查器成为领域标准评测构造,贡献独立于该未测主张;画报已按收窄口径制作,QA 记 ready。
- **2404.06474(facts 单位修正,档位不变)**:Android 数字是 96 题中任务数(15→26 个=15.6%→27.1%),非百分比;"15.4%→26.9%"对应 iOS 8/52→14/52。两套对照分属 WebArena(执行判定,805 条)与 Android(人工,480 条),不可互传;WebArena 一致率 82.1% 低于全判失败基线 88.3%,判"成功"精确率 28–35%(revision: batches/l20-correction.jsonl)。
- **2508.00935(范围收窄,档位不变)**:聊天 vs CUA 对照仅在 52 条常见恶意提示上做过,52 个恶意电脑任务无聊天基线;反例 Gemini 2.5 Pro(聊天合规 28.8% > CUA 执行 17.3%)画报已同屏标出;聊天侧可能经过平台安全层(非严格同条件);CMP 判定细则论文未写明。
- **2412.10840(措辞修正,档位不变)**:同骨干"只换读出"对比收窄为 Table 4 行 2 / OCG 口径;ScreenSpot 36.0→54.8 的提示词不同构。
- **2406.11896(措辞修正,档位不变)**:"真实 Android 设备"应为"并行 Android 模拟器+实时网站";第二→三级增量混合算法与在线两因素;一→二级预算未配平。
- **2407.01476(收窄,档位不变)**:算力配平仅一组 200 题比较(c=5 32.0% vs 重排 n=5 约30%,单次无方差);主结果未配平算力;"预算越大越好"仅测到 c=20 且作者用词 generally。
- **2503.19537(范围收窄,档位不变)**:基线为 Gemini 1.5 的 12 种 prompting 配置在人类演示轨迹上离线逐步分类,非运行中代理(revision: l23-correction.jsonl)。
