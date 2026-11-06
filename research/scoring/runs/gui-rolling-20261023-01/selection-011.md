# selection-011 — gui-rolling-20261023-01（第十一期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-11-06，本仓第十一期（单席串行）
- 不再入选：前十期 36 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`–`selection-010.md`，`reel/README.md`）。总控清单中的 2610.31274 已在 selection-010 入选，跳过
- 依据：本 run 最新 L2 记录（`batches/inc-l2-21..30.jsonl`，各自 supersede 对应 L1）；短名单逐篇从 arxiv.org/html 按缓存钉定版本补读（第 3 节写明每篇读到的范围）。转换稿在 /tmp/sel11，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 候选池：Awesome-CUA 回填第二波（inc-l2-21..29）46 篇 P3 / confirmed / to_l3 + 近期查新 inc-l2-30 的 2 篇（05620 P3、07765 P2 带编辑理由），共 48 篇；总控清单 49 个 ID 含已入选的 2610.31274
- 同 run 其余 to_l3 维持前期处理（selection-004–010 的编辑排除与同题去重不重开）；inc-l2-21..29 的 49 篇 pending_material / park、17 篇 pending_experiment 不进池
- 日期：2026-11-06。之后新增的 L2 或 correction 不计入本期

## 候选池（48 篇）与处理

按 SELECTION.md：47 篇 P3 在前，1 篇 P2（07765）在后；q3 中 capability 30 篇、judgment 17 篇、incremental 1 篇，capability 与 judgment 不分先后。池子以“老论文回填”为主（2018–2025 年 27 篇），问题族与主卡高度重叠，先按“主卡 × 问题”分组去重，再兼顾本仓已入 Reel 的卡分布（high_resolution_target_localisation 已 4 张、online_evaluation_methodology 与 learned_outcome_and_process_judges 各多张、simulated_lookahead_selection 2 张、trajectory_level_policy_training 1 张、experience_memory_retrieval 1 张）。

标注：C = capability，J = judgment，I = incremental；“读”列 = 本期读到的范围（全文 = 正文 + 附录；正文 = 正文全部；节选 = 列出的节；结构 = 只看了章节结构与相关段；L2 = 只依据 L2 记录与裁剪 core，未声称读过全文）。

| ID | 简称 | tier | q3 | 族 | 主卡 | 读 | 处理 |
|---|---|---|---|---|---|---|---|
| 2507.11662 | SGV / agreement bias | P3 | J | F2,F5 | learned_outcome_and_process_judges | 全文 | **入选** |
| 2505.10978 | GiGPO | P3 | C | F2,F1 | trajectory_level_policy_training | 全文 | **入选** |
| 2604.25235 | VLM Judges Rank not Score | P3 | J | F2 | learned_outcome_and_process_judges | 节选（§1、§3.3、§4、表 3、§5.5、App. D） | **correction C-011-1**，本期暂停 |
| 2607.17136 | Teach it to stop | P3 | J | F1,F3 | trajectory_level_policy_training | 正文（本文无附录） | 编辑排除（证据形态），补注不退回 |
| 1812.09195 | QWeb / MetaQWeb | P3 | C | F0,F4 | exploration_driven_task_synthesis | 正文（本文无附录） | 编辑排除（证据形态） |
| 2602.16165 | HiPER | P3 | C | F0,F1 | trajectory_level_policy_training | L2 | 同题去重 → 2505.10978 |
| 2605.14311 | BBCritic | P3 | J | F2,F5 | learned_outcome_and_process_judges | 结构 | 同卡同侧去重 → 2507.11662 |
| 2511.08325 | AgentPRM | P3 | C | F2 | learned_outcome_and_process_judges | L2 | 同卡去重 → 2507.11662 |
| 2510.04791 | GUISpector | P3 | C | F2,F0 | learned_outcome_and_process_judges | L2 | 同卡去重 → 2507.11662 |
| 2601.04203 | FronTalk | P3 | J | F2 | learned_outcome_and_process_judges | L2 | 同卡去重 → 2507.11662 |
| 2608.06474 | WebGrader | P3 | C | F2,F4 | verifiable_execution_reward | L2 | 同卡去重 → 2507.11662 |
| 2611.05620 | ViBench 2.0 | P3 | J | F2 | online_evaluation_methodology | L2 | 同卡去重 → 2507.11662 |
| 2605.15962 | PersonaFingerprint | P3 | J | F4,F0 | online_evaluation_methodology | 节选（§1–3、§4 开头） | 编辑排除（偏离核心） |
| 2607.13718 | Agent permissions | P3 | J | F4,F0 | injection_defense_isolation | 结构 | 编辑排除（证据形态） |
| 2608.10775 | SkillLens | P3 | C | F3,F4 | experience_memory_retrieval | 节选（摘要、§3.5–§5） | 编辑排除（证据形态） |
| 2611.03930 | Memory utility | P3 | J | F2,F4 | experience_memory_retrieval | 节选（摘要、§1） | 编辑排除（偏离核心） |
| 2608.06704 | WebRider | P3 | J | F2,F0 | online_evaluation_methodology | 正文（附录未读） | 编辑排除（同题已有） |
| 2511.19957 | AppSelectBench | P3 | J | F0,F2 | planner_grounder_interface | 节选（摘要、§1、章节结构） | 编辑排除（证据形态） |
| 2609.02987 | TailRL | P3 | J | F5,F2 | rule_reward_single_step_rl | 结构 | 编辑排除（偏离核心） |
| 2310.04406 | LATS | P3 | C | F0,F4 | simulated_lookahead_selection | L2 | 同卡去重（已入 2407.01476、2611.04073） |
| 2410.02052 | ExACT | P3 | C | F0,F2 | simulated_lookahead_selection | L2 | 同卡去重（同上） |
| 2503.02878 | 自训练状态价值 | P3 | C | F2,F4 | simulated_lookahead_selection | L2 | 同卡去重（同上） |
| 2605.15963 | PAGER | P3 | C | F0,F3 | high_resolution_target_localisation | L2 | 同题去重 → 上期 2610.31274 |
| 2505.17629 | TransBench | P3 | J | F3 | online_evaluation_methodology | L2 | 编辑排除（grounding 卡已 4 张） |
| 2505.23678 | 坐标锚定视觉 RL | P3 | J | F1,F0 | high_resolution_target_localisation | L2 | 编辑排除（同上） |
| 2608.11191 | 测试时自蒸馏 grounding | P3 | C | F2,F4 | learned_outcome_and_process_judges | L2 | 编辑排除（同上） |
| 2611.07765 | BiGrounder | P2 | I | F2,F3 | rule_reward_single_step_rl | L2 | 编辑排除（P2 增量，同上） |
| 2106.00133 | AppBuddy | P3 | C | F0,F3 | trajectory_level_policy_training | L2 | 同卡去重 → 2505.10978 |
| 2310.12823 | AgentTuning | P3 | C | F3,F5 | trajectory_level_policy_training | L2 | 编辑排除（证据形态） |
| 2503.16365 | JARVIS-VLA | P3 | J | F1,F3 | trajectory_level_policy_training | L2 | 编辑排除（证据形态） |
| 2312.10170 | UINav | P3 | C | F0,F2 | planner_grounder_interface | L2 | 编辑排除（证据形态） |
| 2511.03773 | DreamGym | P3 | C | F3,F2 | learn_and_train_in_gui_world_model | L2 | 编辑排除（证据形态），可作后续候选 |
| 2403.08978 | AutoGuide | P3 | C | F3,F5 | experience_memory_retrieval | L2 | 编辑排除（证据形态） |
| 2501.12485 | R2D2 | P3 | C | F3,F0 | experience_memory_retrieval | L2 | 编辑排除（证据形态） |
| 2603.03296 | PlugMem | P3 | C | F3,F5 | experience_memory_retrieval | L2 | 编辑排除（证据形态） |
| 2608.06745 | MemPrism | P3 | C | F5,F3 | experience_memory_retrieval | L2 | 编辑排除（证据形态） |
| 2510.10049 | ALLOY | P3 | C | F0,F3 | experience_memory_retrieval | L2 | 编辑排除（证据形态） |
| 2506.01952 | WebChoreArena | P3 | J | F2,F0 | online_evaluation_methodology | L2 | 编辑排除（同题已有） |
| 2510.00507 | Graph2Eval | P3 | J | F2,F3 | exploration_driven_task_synthesis | L2 | 编辑排除（证据形态） |
| 2504.12682 | WebLists | P3 | C | F0,F3 | planner_grounder_interface | L2 | 编辑排除（证据形态） |
| 2506.14079 | FormGym | P3 | C | F4,F0 | planner_grounder_interface | L2 | 编辑排除（证据形态） |
| 2606.20487 | OctoNest | P3 | C | F0 | agent_loop_context_control | L2 | 编辑排除（证据形态） |
| 2603.05294 | StructuredAgent | P3 | C | F0,F1 | agent_loop_context_control | L2 | 编辑排除（证据形态） |
| 2306.01987 | AdbGPT | P3 | C | F0 | planner_grounder_interface | L2 | 编辑排除（应用面） |
| 2310.02424 | AXNav | P3 | C | F0 | planner_grounder_interface | L2 | 编辑排除（应用面） |
| 2411.17933 | 跨 app 测试迁移 | P3 | C | F3,F4 | experience_memory_retrieval | L2 | 编辑排除（应用面） |
| 2506.00520 | ResTest | P3 | C | F0,F4 | exploration_driven_task_synthesis | L2 | 编辑排除（应用面） |
| 2609.22234 | 跨模态指令层级 | P3 | C | F3,F4 | environmental_injection_attacks | L2 | 编辑排除（偏离卡核心） |

### 粗筛 → 短名单（12 篇）

从 48 篇中按“问题是否直接落在 CUA 回路上、证据是否有完整对照、主卡是否已饱和、老经典与近作兼顾”挑出 12 篇补读原文：2507.11662、2604.25235、2605.14311（判官三篇，同卡同侧，至多保留一篇）；2505.10978、2607.17136（训练信号）；1812.09195（2018 年老经典）；2605.15962、2607.13718（F4 隐私与权限）；2608.10775、2611.03930（经验与记忆）；2608.06704（委托忠实度）；2609.02987（尾部目标，含 GUI grounding）。读完 2611.03930 摘要后另补看 2511.19957（新问题：应用选择）作为替补。

## 1. 最终入选（2 篇）

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2507.11662 SGV | J / F2,F5 | learned_outcome_and_process_judges | 问题清楚，且直接改变本领域一个常用做法：拿 MLLM 当轨迹验证器筛数据、给在线反馈。VWA（Gemini 2.5 Flash ReAct 代理，47%）与 OSWorld（UI-TARS-1.5，22%）约 1,300 条轨迹上，14 个模型的失败侧判对率（TNR）34–78%；加 CoT、二分类、8 次投票、评分细则、最大预算思考都在 36–55（表 2，VWA）；在失败轨迹上反复采样，抽到正确判决的概率只有 48%（表 3B），所以投票与 Platt 校准都救不了（附录 E.3）。机制被隔离：“同一次调用里先写先验”49、“拆成两次调用”67/71（表 18）。下游：同代理同环境 3 次均值，VWA 45.0 → 46.1（常规）/ 54.0（SGV），OSWorld 21.7 → 24.3 / 26.5。补的是本仓判官卡的**失败侧**：2404.06474 讲校准链、2610.34384 讲恢复对、2611.04073 讲“读不懂做完没有”，都不是“整体右偏、不随采样消失”。限制写进画报：标签是脚本判分器（VWA 版经作者修订，表 9 人工一致率 98、未给样本数）、下游 token 2.2× vs 1.5× 不等算力、TPR 除 o1 外降 1–6 点、只一个代理 / 环境 |
| 2 | 2505.10978 GiGPO | C / F2,F1 | trajectory_level_policy_training | 老一些的近作（2025-05），本仓训练卡此前只有 2406.11896（要不要 RL），本篇回答 RL 内“分数记给哪一步”。证据形态是池中训练类最干净的：所有 RL 方法同一套超参、同组大小与环境数（附录 E.1），3 个种子；只改优势计算，rollout 与显存不变。WebShop：1.5B GRPO 56.8±3.8 → 65.0±3.2 / 67.4±4.5，7B 66.1±3.7 → 72.8±3.2 / 75.2±3.8；去掉步骤优势后 WebShop 回到 56.8（图 4，与 GRPO 相同），ω 扫描 0.4–1.2 稳定、1.4 跌回 56.3（表 5）。限制写进画报：WebShop 是 HTML 文本观测的模拟站、非截图；锚点要求逐字相同的观测，同观测异状态未检验；两个归一化变体择优报告；消融与扫描种子数不明；WebShop 上的步骤组覆盖率未报 |

族覆盖（本期）：F2 ×2（主族），副族 F5、F1 各一。卡覆盖：learned_outcome_and_process_judges 第五张；trajectory_level_policy_training 第二张。年代：2025-05、2025-07 两篇回填论文；2026 年近作在短名单内补读了 6 篇、另看了 3 篇的结构，均因证据形态、偏离核心或同题已有而未入选（第 2 节）。

只选 2 篇：短名单其余 10 篇见第 2 节，不为凑 3 篇降低证据要求。

## 2. 排除记录

### 2.1 读过原文（全部或节选）的短名单

| ID | 处理 | 理由 |
|---|---|---|
| 2604.25235 | **correction C-011-1** | 见第 4 节。CUA 相关内容只有 MLLM-as-a-Judge 的 Mind2Web 子集 398 例（单张图 + 问题 + 模型答案的 1–5 分人工评分），不是代理轨迹或动作判定；L2 据此确认的“B 类 CUA 评价组件”超出原文 |
| 2607.17136 Teach it to stop | 编辑排除（证据形态） | 已读正文 §1–9。问题成立（单次 RL 结果被上游方差主导），但支撑主张的几处证据都偏弱：(a) 端到端“LinkedIn 8/20 vs 0/15，p=0.006”是看到非零后才给该格追加 rollout（§5 自述“once LinkedIn showed a non-null effect we spent additional rollouts there”），属可选停止，p 值不能按固定样本解读；(b) 方差分解只有 D=3 个独立数据抽样，“数据占 48%”的区间未报；(c) 双峰 dip 检验 p=0.07，摘要写“bimodal”；(d) 环境与 35B 后端私有、不可复核；(e) 帧级指标由同一 Claude 验证器选帧、给标签、计分（作者自述循环）。L2 已记 (c)、(e)；(a) 为本期补注，不改变问题档位，不退回 |
| 1812.09195 QWeb | 编辑排除（证据形态） | 已读全文 v1（无附录）。2018 年网页 RL 的经典（课程、势函数奖励、由目标状态反推指令），但结果只在柱状图（图 4、5），没有种子数与方差；课程依赖 ORACLE 策略、势函数用目标 DOM 状态；instructor 训练也沿用 ORACLE 采样（§5.1）。画报要求“一个有完整对照条件的结果”，本篇给不出；与 GiGPO 同属稀疏奖励训练，保留后者 |
| 2605.15962 PersonaFingerprint | 编辑排除（偏离核心） | 已读 §1–3 与 §4 开头。CUA 在这里是流量生成器，问题是加密流量元数据能否区分 LLM 合成人设；结论对象是合成人设而非真实用户，也不改变 CUA 的感知—规划—动作—反馈。L2 已收窄为“受控合成人设”；本仓核心问题之外，不做画报 |
| 2607.13718 Agent permissions | 编辑排除（证据形态） | 看了章节结构与 §3 方法。文献分类 + 商用代理走查（2026 年 5–6 月），无受控实验或量化攻击 / 良性测量；作为综述有用，不适合“一个有完整对照的结果” |
| 2608.10775 SkillLens | 编辑排除（证据形态） | 已读摘要与 §3.5–§5。核心结果是离线单步 Mind2Web：2B 学生、512 例、128 步更新，跨 10 个未见网站 119 步，Full-VSC 比紧凑文本教师高 5.04 点（3 seeds，其中一个配对区间跨零）；运行时参考配置把标注的当前动作描述喂给选卡（§4.1 自述）；教师卡由当前标注步构造。L2 已指出部署信息边界；不足以单独成画报 |
| 2611.03930 Memory utility | 编辑排除（偏离核心） | 已读摘要与 §1。测的是单次调用的事实问答（记忆来自网页代理的页面访问），作者自述“no claim about procedural memory, acting agents”；没有 GUI 动作 |
| 2608.06704 WebRider | 编辑排除（同题已有） | 已读正文。“终止 99.2% 而全部合同门控只过 38.8%”与本仓已入 Reel 的 2610.34735（动作完成 91.6 vs 整题 47.7）、2610.39234 同一类判断；门控由 GPT-5.5 / Gemini 判，300 条双专家校准的一致率正文未给；合同由作者预定义 |
| 2511.19957 AppSelectBench | 编辑排除（证据形态） | 已读摘要、§1 与章节结构。纯文本“意图 → 应用”分类，选错应用的下游执行代价没有测量；§1 “显著提升下游执行”一句引用为空。问题新，但证据停在分类准确率 |
| 2609.02987 TailRL | 编辑排除（偏离核心） | 看了章节结构。GUI grounding 只是 4 组实验之一（§6.3，另有 ImageNet、文本迷宫、代码优化）；L2 已指出“128–256 倍”是 oracle 覆盖而非可部署选优 |
| 2605.14311 BBCritic | 同卡同侧去重 → 2507.11662 | 看了章节结构与 L2。同为“判官在难例上分不开”，本篇针对困难负例的排序训练，有 AndroidWorld 在线结果；SGV 的失败侧测量跨 14 模型、多种加算力对照，机制隔离更直接。L2 另记表内增益为跨文献比较 |

### 2.2 依据 L2 与裁剪 core 的编辑处理（未声称读过全文）

- **同卡去重 → 2507.11662（判官 / 奖励信号）**：2511.08325 AgentPRM（WebShop 文本；RL 只在 BabyAI/TextCraft）、2510.04791 GUISpector（5 个生成单页应用、单次运行）、2601.04203 FronTalk、2608.06474 WebGrader、2611.05620 ViBench 2.0（三篇被测主体是写网站的代码模型，CUA 部分是浏览器评分器）
- **同题去重 → 2505.10978（稀疏奖励下的逐步信用）**：2602.16165 HiPER（同为 WebShop/ALFWorld 的分层信用分配；L2 记 WebShop 同预算 HAE 消融与附录证明未见）。**同卡去重**：2106.00133 AppBuddy（12 任务、逐任务奖励脚本、无等预算对照）
- **同卡已饱和 · 搜索**（已入 2407.01476 算力配平、2611.04073）：2310.04406 LATS（需可回退环境、无等算力对照）、2410.02052 ExACT（约 10× 推理开销，EL 不优于更多轨迹的 IL）、2503.02878（WebShop，伪价值未校准）
- **同卡已饱和 · 定位**（已 4 张，含上期 2610.31274）：2605.15963 PAGER 与上期 PointerBench 同为“点精度”，同题去重；2505.17629 TransBench、2505.23678、2608.11191、2611.07765（P2 增量）编辑排除
- **训练类其他**：2310.12823 AgentTuning（L2：小模型 held-out 收益几乎由通用数据解释）、2503.16365 JARVIS-VLA（Minecraft；追加数据与预算未等量）、2312.10170 UINav（离线与内部动态测试混合、缺独立消融）、2511.03773 DreamGym（L2：§5 正文与主表数值冲突、保真度由 GPT-4o 打分；问题重要，补材料后可再议）
- **经验与记忆**：2403.08978 AutoGuide（调用未匹配、指南正确性未测）、2501.12485 R2D2（经验来自重复执行，测试流可见性）、2603.03296 PlugMem（human demo 贡献、同站同模板）、2608.06745 MemPrism（浏览器部分仅离线 Mind2Web）、2510.10049 ALLOY（用户研究设计缺、可疑 SD）
- **评测与系统**：2506.01952 WebChoreArena（同题已有；evaluator 误判率未知）、2510.00507 Graph2Eval（执行 judge 无人工校准）、2504.12682 WebLists（宽松单列匹配、按用例调 prompt）、2506.14079 FormGym（表 2 与 §7 成本差 10 倍等口径冲突）、2606.20487 OctoNest（自建 23 任务族，变体非独立）、2603.05294 StructuredAgent（表 4 计数不一致、成本未配平）
- **应用面（GUI 测试）**：2306.01987 AdbGPT、2310.02424 AXNav、2411.17933、2506.00520 ResTest——问题限定在测试场景，L2 各记了样本或基线缺口；本仓 GUI 测试类已有 2605.29532
- **安全**：2609.22234 是 system–user 指令层级，L2 已改口径为“不等于环境网页注入隔离”，judge 一致率 80%

`later_work`：本期 48 条记录未据 later_work 降级。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2507.11662 | v3（2026-03-08）正文 §1–6 + App. A–F（表 1–24）；App. B 提示词、App. C/G 定性例只读说明；图 3 读正文与 D.3 文字 | 同意 P3/confirmed。L2 待查项：(1) 表 9 人工校验已读（修订判分器 Acc 85.1 → 98，无样本数），C25/K16 的 partial 维持；(2) 下游无等 token 对照（2.2× vs 1.5×），离线有投票与思考对照；(3) 环境修订前后增益方向一致（表 24：41/48 → 47/54）。**补注（不退回）**：表 3A 判分器 57% 与 VWA 47% 不一致；正文“72%”与表 73、引表行号错位；TPR 在 13/14 模型上下降 1–6 点 |
| 2505.10978 | v3（2025-10-28）正文 §1–6 + App. A–F（表 1–5；图 4–6 由原文 SVG 读数，图 4 按多边形坐标换算并以表 1 两行校验） | 同意 P3/confirmed；K20、K30 的 partial 维持。**补注（不退回）**：§5.6“<0.002%”按原文秒数应为约 0.15%；摘要“>9%”取较好变体；WebShop 上的步骤组覆盖率未报 |
| 2607.17136 | v1 正文 §1–9（本文无附录） | 同意问题档位；编辑排除。**补注（不退回）**：LinkedIn 转移结果为可选停止（见 2.1） |
| 2604.25235 | v2 节选：§1、§3.3、§4、表 1 与表 3 相关行、§5.5、App. D.1–D.2 | **correction C-011-1** |
| 1812.09195 | v1 全文（无附录；图 4、5 只读说明与正文） | 同意问题档位；编辑排除 |
| 2605.15962 | v1 §1–3、§4 开头 | 同意 L2 的收窄；编辑排除 |
| 2608.10775 | v2 摘要、§3.5–§5（表 2–7） | 同意 L2；编辑排除 |
| 2608.06704 | v2 正文（附录未读） | 同意 L2；编辑排除 |
| 2611.03930 | v1 摘要、§1 | 同意 L2 的“限于事实召回”；编辑排除 |
| 2511.19957 | v2 摘要、§1、章节结构 | 不改档位（未读实验节）；编辑排除 |
| 2607.13718、2609.02987、2605.14311 | 只看章节结构与相关段 | 依 L2 处理，未声称读过 |

版本复核：2026-11-06 查 export.arxiv.org/abs，2507.11662 与 2505.10978 最新均为 v3，与缓存钉定版本一致。

## 4. correction / 待补

### C-011-1　2604.25235v2 VLM Judges Can Rank but Cannot Score（退回 Sol 单篇修订，保留旧记录）

旧记录：`batches/inc-l2-27.jsonl`（supersedes inc-l1-36#2604.25235），P3 / confirmed / to_l3；q1 measured_own，q2 open_failure，q3 judgment，q4 fits；卡 main/learned_outcome_and_process_judges；facts 第 1 条称 Mind2Web 子集“直接支持 CUA 评分不确定性”，子卡 C25 第 1 问记 holds 并写“有直接 CUA 评价组件依据”。

- **错误点**：
  1. **原文没有评估任何代理行为**。数据只有两套：MLLM-as-a-Judge 的 score 子集（5,717 例，14 类，“每例一张图、一个问题、一个模型生成的答案、一名标注者的 1–5 分”，§4、App. D.1）与 Polaris 图像描述（8,726 例）。Mind2Web 是前者的 14 类之一（398 例），作者把它归入“Knowledge/Web：以文本世界知识为主、图像为上下文”的任务（App. D.1），被评的是 VLM 对静态网页截图问题的回答，不是轨迹、动作或任务完成判定。
  2. 因此 L2 的范围判断“Mind2Web 实测确认 B 类 CUA 评价组件”不成立；q3 写的“误导阈值门控、模型比较和奖励解释”对 CUA 只是外推，原文唯一与网页相关的数字是 Mind2Web 子集上的区间宽度与相关（如 Gemini ρ=0.065，§5.5），没有在任何 CUA 回路中测过。
  3. C25 第 1 问“有直接 CUA 评价组件依据”应为 partial 或 NA（人工分数是对 VQA 答案的，不是对 GUI 代理的）。
- **请 Sol 复核**：(a) 本篇是否在本仓收录范围内：docs/EVIDENCE.md 的 B 类是“可直接用于 CUA 系统的组件或方法学（含 judge / reward model）”，需判断一个从未在任何 CUA 判官、轨迹或动作上测过的通用 VLM 打分保形校准是否算“可直接用于”；若不算，应记 out_of_scope / exclude；(b) 若保留，q3 是否应为 `local`（对 CUA 只影响本文设置），按 PROBLEM_CORE 第 4 节最高 P1；(c) facts 第 1 条与 C25 第 1 问的表述按上文收窄。
- 本期不入选，不制作画报。

### 待补清单

沿用 selection-008 第 4 节与 selection-010 第 4 节，状态未变。回填第二波新增的 49 篇 pending_material / park（老论文缓存缺章为主）由巡检班按 priority 排队补材料，不在此处直接入选。值得优先补的一篇：2511.03773 DreamGym（问题重要；需核对 §5 正文与主表数值冲突、保真度判定口径）。

## 5. 漏检抽查结果

本期没有新增抽查。按 progress.md，inc-l2-21..29 已清偿欠账（抽 19、改判 0），inc-l2-30 欠账约 0.3 滚存，留给巡检班。

## 6. Reel 成品路径

各目录含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。实际打开渲染图做视觉 QA；用 DOM 探针核对无越界、内容底边不压页脚、SVG 文本不越框；PDF 栅格化后与 PNG 并排对照；缩到 580 px 宽检查小屏可读性。渲染沿用 `--disable-lcd-text`。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2507.11662 | `reel/2507.11662/` | 深墨绿竖栏（标题、55→76、判决分布堆叠条、条件、限制、阅读、同卡关系、原文出入）+ 五面板：两泳道调用对比与四格消融条、14 行 TNR 哑铃配 TPR 列、加算力条形与失败侧采样概率、下游柱与介入结果条、验证器×代理矩阵与长度哑铃（浅灰绿底，珊瑚 / 墨绿） | ready（第一次：两栏大量留白、图例越界、侧栏两处数字不准；第二次补 05 面板与分布条、修数字；第三次补侧栏两块；第四次收窄一句措辞；共四次渲染） |
| 2505.10978 | `reel/2505.10978/` | 粗黑线页眉 + 深色票根 + 线路图机制（金色锚点站、回环箭头、右侧公式框、排序条）+ 条件标签行 + 带误差线分组柱 / 消融数字表 / ω 折线 + 计时条 / 组大小条 / 叠加对比条 + 双栏限制与阅读（米色方格底，锈红 / 墨绿 / 蓝灰） | ready（第一次：机制图线路不从同一起点出发、回到锚点画不出、参考线标签被柱遮挡、标签重叠与越框、底部留白；第二次重画机制图并修图；其后四次小改；共六次渲染） |

索引：`reel/README.md` 新增第十一期一节；`README.md` 头部统计行由 36 改为 38（滚动 run 由 17 改为 19）。poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
