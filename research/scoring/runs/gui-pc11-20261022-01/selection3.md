# selection3 — gui-pc11-20261022-01(第三期)

- run:`gui-pc11-20261022-01`;规则 `problem-core-v1.1`(PROBLEM_CORE.md / SELECTION.md)
- 选题:Opus 5.5 L3,2026-10-22,第三期
- 输入:`l3_shortlist3.tsv` 共 38 篇(q3:capability 20 / judgment 17 / incremental 1)。每篇取最新记录,38 篇均为 L2;37 篇是 P3 confirmed,1 篇是 P2 confirmed(2607.11185,带编辑理由)。与 `l3_shortlist2.tsv` 相比新进 13 篇:重激活新晋 5 篇(2604.00073、2607.11185、2610.18067、2610.30108、2610.03574)、2604.04918、2608.30038、2606.15034、2510.14969、2402.05930,以及首期已经讨论过的 2410.00467、2504.04716、2605.16024
- 不再入选:前两期 17 篇,以及 README 高分表里的 16 篇(这 16 篇都不在本短名单中)
- 前两期族覆盖(总控口径):F0 2、F1 1、F2 5、F3 2、F4 3、F5 2。本期优先补空白卡和薄弱族,但不为补位降低证据要求
- 依据:L2 记录的字段、facts、biggest_gap 和 subcard_checks。新进候选抽查了缓存 core(`research/fulltext/<id>.txt`)里的关键数字:2604.00073 的 Table 2/3 和标准误说明,2604.04918 的 Table 4 和 GEE 检验,2510.14969 的 Table 2 及有无多 seed,2608.30038 的阈值冻结和 FRR。**没有读完整原文**,不满足 SELECTION「最终制作条件」
- 不用分数、venue、代码或名气;没有改动任何记录字段

## selection_cutoff

- 记录:`batches/` 下全部 L2 文件(`l01–l108.jsonl`,含 `l19–l23-correction.jsonl`),每篇按批次顺序取最后一条。38 篇候选的最新记录都在这些文件里,其中 2607.11185 的最新记录在 `l104`,其余新进篇在 `l34`、`l41`、`l48`、`l74`、`l106`、`l107`、`l108`
- 候选池:只用 `l3_shortlist3.tsv` 的 38 篇,不另扩池
- 日期:2026-10-22。之后新增的 L2 或 correction 不计入本期

## 1. 最终入选(2 篇)

两篇都是 P3 confirmed,q3 都是 judgment,分属两张不同的主卡。顺序不代表高低。

| # | ID | tier | q3 | 族 | 卡 | 入选理由 |
|---|---|---|---|---|---|---|
| 1 | 2604.00073 Terminal Agents Suffice | P3 | judgment | F1,F0 | planner_grounder_interface(**新覆盖**) | 补上空白卡和薄弱的 F1。三个企业平台共 729 个任务,用同一骨干比较 GUI 浏览器(Playwright,a11y+截图)、MCP 工具目录、终端 API 和混合接口,成功与否都按系统终态判定,并报告标准误。Sonnet 4.6:Web 72.2%/$3.29,Terminal 72.7%/$0.56;四个骨干中有三个的 Web 与 Terminal 相差约 1 点,区别主要在成本(2–9×)。混合接口并不必然更好:Sonnet 72.0%/$1.94,Opus 81.4%/$2.22。在 ServiceNow 上 Terminal 与 Web 各有对方做不了的任务(55 对 51),按任务挑选更优方的 oracle 上界是 89.1%,但混合代理远没到这个上界。这改变了"API 可用的企业流程默认用 GUI 代理、多叠一层接口总会更好"的判断。限制:只覆盖 API 可用的短流程;工具目录覆盖不全不是纯粹的接口模态因素;工具调用次数和 wall-clock 只在 Appendix I |
| 2 | 2604.04918 Human Oversight Strategies | P3 | judgment | F0,F2 | agent_initiated_user_interaction;副卡 injection_defense_isolation(**新覆盖**) | 48 名参与者、192 场真实网页会话,比较四种人类监督策略:有审批不等于危险动作能被拦住。问题动作进入执行的有 138 次,用户只拦住 29 次;发生率依策略为 83.3/87.5/56.2/60.4%(p<.001),拦截成功率差异不显著(p=.366);109 次失败中有 61 次是控制权交还时机不对。与首期 2503.19537 同主卡,但那一篇测的是代理"何时该问",这一篇测的是人拿到控制权后能否及时阻止,是另一侧的问题,有独立价值;同时给副卡 injection_defense_isolation"假设有一位专注的人类"这一失效模式提供了真人证据。限制:站点由研究者搭建;计划型策略把获批计划写进 system prompt,所以发生率下降可能部分来自代理行为的变化;p=.366 不能读成"等价";缓存在 §4 截断,呈现顺序和平衡设计没有核到 |

族覆盖(本期):F0 ×2(1、2),F1 ×1(1),F2 ×1(2)。
三期合计(按主族):F0 3、F1 2、F2 5、F3 2、F4 3、F5 2。

编辑理由:
- **只选 2 篇**。新进的 13 篇里,能在本卡问题最清楚、证据最直接,且不与已选篇同题的只有这两篇。其余候选的记录与上一期相同(批次文件没变),前两期的排除理由仍然成立。规则允许少于 9 篇,这里不按配额凑数。
- **空白卡**:本期补上 planner_grounder_interface;injection_defense_isolation 以副卡形式补上。environmental_injection_attacks、mine_human_screen_videos、structured_screen_observation、calibrate_simulator_to_real 四张卡仍然空着,池中候选的缺口见第 2 节,能补位的材料见第 3 节。
- **q3 全为 judgment**:capability 一侧的新进候选,2608.30038 与已选的 2609.02154 同题;2510.14969 的效应只差几个任务,且没有多 seed;2610.18067 的 GUI 部分没有单独隔离。三期合计 capability 7 / judgment 12。
- **安全簇**:2604.04918 和 2606.15034 都在问"局部门控通过不等于危险被挡住",前者是人类门控,后者是自动 guardrail。保留真人样本更大、有统计检验的 2604.04918。加上前两期的 2508.00935、2606.12666 和 2609.02154,安全相关累计 4 席,不再加。

### 原文核对状态与制作前必查

两篇均**未核对完整原文**。制作前须读完整原文和支撑结论所需的附录;若发现 L2 判断错误,暂停该篇,写 correction 退回 Sol 单篇修订。

| ID | 必查 |
|---|---|
| 2604.00073 | Appendix A 的多次运行波动(Web/Terminal 差 1.2–1.5 点处于波动之内);Appendix C.1/C.2 可行任务子集和单一通用工具消融(用来区分工具覆盖与接口模态);Appendix I 的工具调用和 wall-clock 成本;Web 代理的观察和动作配置是否算强 GUI 基线;oracle 89.1% 只在 ServiceNow 上测。画报只能写"API 可用的短流程",不能写"GUI 代理没有必要" |
| 2604.04918 | §4 的被试内顺序和平衡设计;四种策略的 system prompt 差异;问题动作的三类来源(隐私、注入、暗模式)各自的拦截率;61/109 时机错配的编码规则和一致性;研究者自建站点的外推范围 |

## 2. 排除记录(36 篇)

"同卡→前期"指该卡已有前期入选,本篇没有足以单独成篇的独立价值。"维持前期判断"指记录没变,沿用 `selection.md` 或 `selection2.md` 的理由。

### 2a. 本期新进(11 篇)

| ID | 卡 | q3 | 处理 | 理由 |
|---|---|---|---|---|
| 2608.30038 ActReal | 无主卡 | C | 同题去重 → 2609.02154(第二期);**替补** | 问题与 MFA 篇相同:有系统权限的移动代理能伪造"人在场"的证据(这里是触摸与 IMU 的物理耦合)。证据比 MFA 篇更强:阈值在验证集冻结后测,ASR 77.5%、FRR 5.2%,真机 20 名新参与者的联合 ASR 为 48.1–88.3%。若 2609.02154(WiP)在制作前核查时失败,优先用本篇替换。限制:依赖特权 hook;事件规避率不等于整任务恶意成功 |
| 2606.15034 OSGuard | verifiable_execution_reward | J | 安全簇同题 → 本期 2604.04918;F2 已饱和;备选 | 良性指令下有 37.8% 不安全完成,问题新,也有终态检查(hash、权限)。但只有 45 个任务、单一 executor,加 guardrail 只纠正了约 1 条;终态 checker 的误判率没有给 |
| 2610.18067 WorkRover | verifiable_execution_reward | C | GUI 部分未隔离;F2 已饱和;备选 | 同修复预算下 SRR 60.7→70.3%,任务意图改变 14.3→1.3%,对照清楚。但五个外部 benchmark 的收益不是 GUI 单独的证据,应用交互的占比和 GUI-only 留出评测都没有,checker 的两侧误判率也没有分项 |
| 2510.14969 UI-Simulator | learn_and_train_in_gui_world_model | C | 证据强度不足;备选(F3) | 有同规模真实合成的对照,但差距很小:WebArena 6.28 对 4.31(约 16 个任务),AndroidWorld 8.6 对 4.7(116 题中约 4–5 个);没有多 seed 或方差。绝对水平与首期因此落选的 Synatra 相同。R 版用了测试环境的转移库,不能称零经验。该卡已有 ViMo |
| 2610.03574 HyperBrowseComp | online_evaluation_methodology | J | 同卡→前期(该卡已有 2 篇);GUI 部分弱 | 同一模型在三种 harness 下为 31.68/22.22/17.73%,说明 harness 敏感性;但 OWL 有 93 次 workforce 终止失败,难以归因到视觉浏览;judge 没有人工校准;主体是搜索类任务 |
| 2610.30108 Multimodal Embodied Agents | online_evaluation_methodology | J | 同卡→前期;证据形态弱 | 64 个 benchmark 中只有 5 个显式测 Anticipate、3 个显式测 Verify,这个审计视角有用;但这是综述作者的单方编码,没有标注一致性,也没有逐篇来源复核;三档标签不是性能证据 |
| 2607.11185 SCALECUA | verifiable_execution_reward | incremental | P2 后置;备选(F5) | 编辑晋级理由成立:同骨干分段训练每步 750→265 秒,去分段后 68.7→62.2。但 q3 是 incremental,只有单一训练 seed,checker 专家一致率 82.5% 也没有两侧拆分;本期 P3 候选的排除都出于证据或同题,不是数量不够,所以不提前 P2 |
| 2402.05930 WebLINX | online_evaluation_methodology | J | 证据不够直接(F3) | IID 37.0 对 OOD 25.2 的划分清楚,但只有离线 turn score,"接受替代解"一项子卡为 fails,在线外推一项为 unknown。与第二期排除仅有离线证据的 F3 候选一致 |
| 2410.00467 Dynamic Planning | agent_loop_context_control | J | 维持首期判断;同卡→2310.03720 | 只有 20 个 general 任务,45.45→43.94,离线;47.36% 用到了测试流里的 reference |
| 2504.04716 Grounding Robustness | high_resolution_target_localisation | J | 维持首期判断;同卡已有 2 篇 | ε 没有经过人工可察觉性验证,目标固定在角落;OS-Atlas targeted ASR 只有 0.43%,不同模型效应差别大 |
| 2605.16024 ScreenSearch | exploration_driven_task_synthesis | J | 维持首期判断;同卡→2601.22781 | 配对消融扎实,但只有 3 个应用、50 步,下游是 teacher-forced 离线指标 |

### 2b. 前两期已排除、记录未变(25 篇)

| ID | 卡 | q3 | 理由(沿用前期) |
|---|---|---|---|
| 2404.02475 Prompt2Task | agent_initiated_user_interaction | C | 同题 → 2503.19537;90.68/95.24 含用户协助,子卡 1 项 fails |
| 2303.17491 RCI | agent_loop_context_control | C | 同卡 → 2310.03720;没有等调用预算的纯批判对照 |
| 2605.06761 Weblica | calibrate_simulator_to_real | C | 技能由 Online-Mind2Web 测试任务轨迹归纳,24.8→35.6 不能当未见迁移。该卡因此仍空着 |
| 2407.09295 Mobile GUI attacks | environmental_injection_attacks | C | 安全簇;缓存缺 §4 成功规则 |
| 2408.02544 Environmental Distractions | environmental_injection_attacks | J | 安全簇;只有模拟单步,没有成对的无干扰基线 |
| 2306.07863 Synapse | experience_memory_retrieval | C | 同题 → 2409.07429;OOD 增益不能归于记忆 |
| 2509.25140 ReasoningBank | experience_memory_retrieval | J | 同题 → 2409.07429;增量;自判校准只在 Shopping 子集 |
| 2409.14337 MobileViews | exploration_driven_task_synthesis | C | 同卡 → 2601.22781;规模收益不单调 |
| 2401.10935 SeeClick | high_resolution_target_localisation | C | 同卡 → 2412.10840/2312.08914;收益来自混合预训练包 |
| 2410.09006 UI Operation Impacts | injection_defense_isolation | J | 最佳一致率 58.37%,没有标注者间一致性 |
| 2503.09241 In-Context Defense | injection_defense_isolation | C | 只对已知、非自适应攻击;本期该卡由 2604.04918 以副卡覆盖 |
| 2412.09362 Falcon-UI | learn_and_train_in_gui_world_model | J | 同卡 → 2504.13936;只有离线表征收益 |
| 2406.13264 WONDERBREAD | learned_outcome_and_process_judges | J | 同卡 → 2404.06474;负例是合成的,没有下游证据 |
| 2505.21496 UI-Genie | learned_outcome_and_process_judges | C | 同卡 → 2404.06474;AndroidLab 收益混入了搜索和再训练循环;F2 已饱和 |
| 2406.13719 GUI Action Narrator | mine_human_screen_videos | C | 离线描述组件,GPT-4 指标未经人工校准。该卡因此仍空着 |
| 2105.13231 AndroidEnv | online_evaluation_methodology | C | 同卡 → 2311.18751;只有 6 个任务的基线 |
| 1808.09132 NL→Web Elements | planner_grounder_interface | C | 按页面而非站点划分,没有下游任务;该卡本期由 2604.00073 覆盖 |
| 2202.02312 MoTIF | planner_grounder_interface | J | 可行性实验是 oracle 探索上界;同卡 → 2604.00073 |
| 2508.05615 GUI-RCPO | rule_reward_single_step_rl | C | 同卡 → 2505.15810;收益很小 |
| 2502.15760 Digi-Q | simulated_lookahead_selection | C | 同卡已有 2 篇;是 DigiRL 的同谱系后续;备选(F0) |
| 2010.04295 Widget Captioning | structured_screen_observation | C | 可访问性组件,没有 agent 任务收益。该卡因此仍空着 |
| 2201.04100 Denoise UI Layouts | structured_screen_observation | J | 没有下游训练收益 |
| 1802.08802 Workflow-Guided Exploration | trajectory_level_policy_training | C | 同卡 → 2406.11896;只在 MiniWoB 上测 |
| 2406.03679 Data Scale on UI Control | trajectory_level_policy_training | J | 同卡 → 2406.11896;单一骨干,离线代理指标 |
| 2207.01206 WebShop | verifiable_execution_reward | C | 同卡 → 2508.00935;checker 与真实需求是否一致没有量化 |

`later_work`:38 篇记录均为 null,本期没有按 later_work 降级。

**下期备选顺序**(仅供参考,不改字段):2608.30038(若 2609.02154 被替换)、2606.15034、2610.18067、2607.11185、2510.14969。

## 3. 待补清单(priority=high 但未确认)

按全部批次的最新记录重新统计(含 l92–l108 重激活):priority=high 且未 confirmed 的共 347 篇,其中 pending_experiment 295(含 out_of_scope 3)、pending_method 15(含 out_of_scope 1)、缺材料 37(needs_material 14 + assessed pending_material 23)。补齐后由 Sol 单篇做 L2,不在此直接入选。

### 3a. 缺材料、且落在仍空着的卡上(补齐可能改变下期选题)

| ID | 卡 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2406.12814 | environmental_injection_attacks | §5.2–5.3 中 evaluator/value function 与搜索的受控比较 | 注入卡是否有带终态判定的候选;能否确认"加检查/搜索反而放大攻击" |
| 2504.14064 | environmental_injection_attacks | BrowserGym 上的攻击排序与组合攻击主结果 | GUI/Web 专属的攻击测量 |
| 2507.05445 | environmental_injection_attacks | §V 逐案例的攻击入口与终态回执 | counterexample 能否成立 |
| 2609.16732 | environmental_injection_attacks | §5.4 之后的人类显示协议、原 APK 对照、功能回归 | "用户难察觉且功能保持"的新威胁能否 confirmed |
| 2504.13805 | mine_human_screen_videos | §4 DemoParser/KnowSeeker,演示与目标的答案隔离 | 该卡唯一可能 confirmed 的候选(范围限 within-app) |
| 2008.05132 | structured_screen_observation | §3 完整测量、方法和主结果 | null→P3 与否 |
| 2608.06171 | structured_screen_observation | §6 完整 router 结果,§7–8 的 CV 与泄漏校正 | router 的训练与评测是否分离 |
| 2610.09469 | injection_defense_isolation | §4–5 系统与证明主体、执行绑定细节 | 是否有"非自适应攻击"之外的隔离式防御 |

### 3b. 其余缺材料(29)

agent_initiated_user_interaction:2509.11939、2512.22047;agent_loop_context_control:2310.18331、2409.10741、2506.16042、2606.29472、2608.27477;experience_memory_retrieval:2504.06821、2609.36488、2610.24453;high_resolution_target_localisation:2506.15425;learned_outcome_and_process_judges:2509.23263;online_evaluation_methodology:2410.06703、2505.03570、2509.04198、2512.00756、2603.04949、2604.06182、2604.06367、2604.07929、2607.26041、2609.06059、2610.19900;planner_grounder_interface:2402.07456、2609.03438、2610.16720、2610.22200;trajectory_level_policy_training:2501.12326、2602.16855。所缺章节见各条最新 L2 的 `biggest_gap`。其中 2608.27477(F1 的 harness 消融)和 2610.22200(GUI-only/code-only 的同权限对照)与本期 2604.00073 同属 F1 接口问题,补齐后可以检验它的结论。

### 3c. 缺受控实验或方法核对(310)

按主卡:online_evaluation_methodology、agent_loop_context_control、environmental_injection_attacks、experience_memory_retrieval、planner_grounder_interface 最多(合计约 2/3)。缺口主要是等预算或同信息对照、judge 的双侧校准和在线验证,详见各条 L2 的 `biggest_gap`。B 组(80 篇)和 C 组(479 篇)的补核状态同 `progress.md`,本期没有处理。

## 4. 漏检抽查结果

本期没有新增抽查,沿用首期 `selection.md` 第 4 节(26 篇抽查,5 篇改判)。本期新进的 2604.00073、2610.03574、2610.30108、2610.18067 在 L2 推翻了 L1 的范围排除(记录在各自的 biggest_gap 或 facts 中),这属于 L2 重激活的结果,不算 L3 抽查改判。

## 5. Reel 成品路径

本期 2 篇待制作,存入 `reel/<paper-id>/`。先完成第 1 节"制作前必查"和原文核对,做过实际视觉 QA 后才记为 ready。
