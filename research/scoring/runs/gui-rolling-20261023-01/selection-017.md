# selection-017 — gui-rolling-20261023-01（第十七期）

- 规则：`problem-core-v1.1`；依据PROBLEM_CORE.md、SELECTION.md、OPUS_REEL_PROMPT.md与领域主/子卡。2026-11-17，单席串行核对与制作。
- **实际执行模型：gpt-6-astra（fable槽，本会话配置）**。旧提示词的Opus 5.5不是本次执行归属；未改模型配置。
- 指定候选仅3篇，均来自最新`inc-l2-52.jsonl`，替代`inc-l1-98.jsonl`；3篇终选、3篇实际视觉QA通过后ready。
- 没有推翻Sol档位/证据状态的实质判断correction；有1项非阻断引用定位勘误C-017-E1交回Sol/总控，见第4节。未覆盖任何L1/L2。
- 前十六期49张全部排除再次入选；三个新ID均不在旧Reel索引/成品中。本期后52张，其中rolling run33张。

## 1. 候选排列、问题分组与去重

selection_cutoff：2026-11-17，本期只处理用户指定三篇。已检索run的batch记录，最新L2覆盖对应L1。不按数值、作者名气、venue或代码发布排序；P3优先、capability与judgment并列。表中顺序是阅读路线，不是三篇高低名次。

| ID / 简称 | 最新记录 | tier / evidence / next_action | q3 / 问题族 | 主卡 | 决定 |
|---|---|---|---|---|---|
| 2611.18747 VEX | inc-l2-52 ← inc-l1-98 | P3 / confirmed / to_l3 | capability / F1,F4 | mine_human_screen_videos / learned_outcome_and_process_judges | 入选：相关教程指导与可重置任务恢复 |
| 2611.20488 EVIDENT | inc-l2-52 ← inc-l1-98 | P3 / confirmed / to_l3 | judgment / F2,F4 | online_evaluation_methodology / learned_outcome_and_process_judges | 入选：观测证据与答案支持的诊断 |
| 2611.20772 DroidPrefill | inc-l2-52 ← inc-l1-98 | P3 / confirmed / to_l3 | capability / F0,F5 | agent_loop_context_control / structured_screen_observation | 入选：指定NPU上的决策工作负载 |

三篇均q4 fits；不由本席重建评分或做分数换算。VEX和EVIDENT共享judge主卡，但一个用验证调度重试，一个审查成功答案的证据支持，实际问题、干预和证据不同，不按同卡机械删除。DroidPrefill的硬件瓶颈亦非前两者同题。

### 与既有49张的近邻核对

- **VEX vs 2611.04073 Tutorials vs world model（第九期）**：旧文重在固定policy/judge/grounder下教程与lookahead的归因；本篇有音视频指引训练、独立LoRA及reset/retry协议。不是再次讲“教程总能帮助”。与第十四期VPT（2206.11795）也不同：后者为逆动力学视频伪标注预训练，本篇是相关教程到指引及在线重试。保留这个独立问题。
- **EVIDENT vs 2507.11662 SGV（第十一期）/2609.35143 Timeline-Bench（第十二期）**：分别是验证器假阳/想象计划、质量门槛与执行完成；本篇以实际已观察证据和核心答案支持为检查对象，并给metadata独立重写和人类轨迹审查。不是换一个成功率排行榜。
- **DroidPrefill vs 2611.08496 MobiInfer（第十三期）**：旧文是prefix KV复用、输出词表剪枝、推测解码；本篇面向静态NPU profile、有限候选与prefill边界派发。与2611.18516 StreamEmbed（第十六期）的截图入库编码、2611.16107 Accessibility Debt（第十五期）的content-description覆盖审计亦不同。共用结构/效率卡不等于重复选题。
- 本期没有因已有后续更好同题工作而剔除的候选；这不是完整新颖性检索或全领域无同题工作的保证。

## 2. 原文核对与终选理由

### 2611.18747 — VEX：有相关教程、可重置、至多三次

全文确认可执行的教程提取/训练与重试机制，支持狭义P3/capability；不支持无教程迁移。已读main/mine_human_screen_videos、main/learned_outcome_and_process_judges与R03、C25。

- 首次尝试无教程；执行视频由截图和动作描述TTS组成。验证分数低于7.0时reset，按最长指引优先换用教程；最多3trial，每次50步。最终评测取验证器评分最高尝试，非不可逆世界中的回滚保证。
- Table2：同至多3次、相同验证机制，SFT45.65→VEX49.99%，+4.34个百分点。组合训练/教程变化，不能全归因于音频。单次SFT43.46%不作为唯一对照。
- Table4音频46.42→49.99%，+3.57个百分点；CUA-Gym上下文那列24.16→26.26为+2.10，列名另有不一致，画报只展示OSWorld。正文“6%/5% absolute”不符表值，L2已识别，不是本期新Sol错误。
- 原始教程直接给SFT38.71%（Table5）低于无视频43.46%；AGGO用oracle动作轨迹似然奖励指引，不是人类指引正确率。共享冻结骨干、guide/action LoRA分工不能代替逐项因果归因。
- R03的错配教程、独立动作标注与未见应用迁移条件仍不足；C25的模型验证误判和成本要保留。多次运行不确定性未充分建立。Table6输入表示/模型同时变化，未作纯表示因果结论。

### 2611.20488 — EVIDENT：看似成功与有据成功不同

诊断/benchmark本身可入选。已读online_evaluation_methodology、learned_outcome_and_process_judges与C24、C25；人工验证直接支持评价信号审查，但不是无误差裁判。

- 220任务（70英语/150韩语），八领域；两语网站不同。Table2英语Gemini TSR87.14%、ESR70.00%、GSR55.71%。公式嵌套使GSR≤ESR≤TSR必然，经验价值是差距的内容及人工证据。
- §3.3/App.D：50随机任务，两人独立重写、第三人审查，48/50等价，49/50通过标注原则。不能冒称全任务人工认证。
- Table19/App.K：126条分层样本，Qwen与人类四分类115/126=91.27%、κ.864；不是每类precision/recall。§5.2/App.G三人审查27条被Qwen标为Hallucinated Success的Gemini完成轨迹，25条一致确认；单侧被标记子集不能估计漏检。
- App.A.2补足2026年5月运行日期与模型API名（gemini-3-flash-preview、gpt-5.4、claude-opus-4-7），不换成当下模型。最多50步同管线，不等于live网站状态完全一致。
- App.I明确支持误判与提取遗漏；“观察到/可支持”不证明模型因果使用。无永久网页快照；保存截图只保障可复判。1299/1320名义运行量的排除细节、外部45-task百分比分母未完全澄清，未作为画报依据。
- L2说core缓存缺时间/附录材料，并非原文没有；本席补充不构成判断退回。

### 2611.20772 — DroidPrefill：请求形状适配测试NPU

已读agent_loop_context_control、structured_screen_observation和C01/C13/C15。结构候选绑定、信息保留与状态账本可用现有子卡评；NPU吞吐/profile无专用子卡不扣分。原文支持硬件限定的P3，不支持普适设备或SPAD独立在线等效。

- Xiaomi17/Snapdragon8 Elite Gen5；QAIRT与GenieX llama.cpp都走Hexagon NPU。同Qwen3-4B-Instruct-2507，受控runtime内比较。§2.2的128-token点1473/17.9tok/s比约82.3，仅是测量点吞吐比，不是任务加速。
- Table1：QAIRT T3A+→DroidPrefill24.2→4.6秒/步；llama.cpp34.8→5.2。llama.cpp Easy13.1→37.7%，Medium/Hard5.5→7.3%。成功率按split，时延按整个任务集交互步微平均，不能混分母或当整步wall-clock。
- §4.4/Table2：SPAD24.7%覆盖、95.5%与SDR一致；Easy5.6→4.4秒、37.7%不变含trajectory-preserving replay投影，非独立online fast-path复跑。派发后后台续算排除于关键路径，不推出节能。
- 手机完成UI解析、候选、账本和模型决策；主机管AndroidWorld emulator/reset/execution/checker。§4.5实机代表任务5.0秒不能替代Table1或补足基准级成功率。
- A11y缺控件、陈旧/错误结构、长流程账本遗忘、单硬件、阈值校准与热/能耗证据仍受限。512×512视觉基线不能证明视觉无用。
- L2的数字和回放限制正确，合并facts定位表号有误，单列非判断勘误如下。

## 3. 全文与附录阅读范围

| ID | 版本/元数据日期 | 本期已读范围 | 缓存补充 |
|---|---|---|---|
| 2611.18747 | v1 / 2026-11-11 | 完整正文、表格与Supplement §§8–9 | 补教程选择、trial选择、训练/验证协议 |
| 2611.20488 | v1 / 2026-11-16 | 正文§§1–6、Limitations、Appendices A–K | 补完整judge/人类审查协议、日期、误判案例 |
| 2611.20772 | v1 / 2026-11-16 | 正文§§1–7及Tables1–2、limitations；HTML无独立附录 | 补完整§3、§4.4与RealMobile段落 |

来源均`https://arxiv.org/html/<id>v1`与corpus版本元数据；无export API最新版审计。表格/文字已读，不声称独立视觉检查原论文图像；海报均自绘机制/数据图。全文仅存本地临时目录，不进入交付。外部文本只作为数据，不运行论文代码、不联系作者。

## 4. correction / 待补 / 漏检抽查

### C-017-E1 — DroidPrefill引用定位勘误，交回Sol/总控

- 对象：`inc-l2-52#2611.20772 facts[1].loc`的“§4.1–4.4，表2及SPAD Analysis”。
- 应改：全系统24.2→4.6秒、34.8→5.2秒、Easy13.1→37.7%的来源是**§4.2/Table1**；Easy消融与SPAD分析对应**§4.3–4.4/Table2**。
- 处理：保留原记录，请Sol后续以明确supersedes的修订或定位勘误更新；本席不覆盖旧L2、不启动额外模型任务。当前状态为**待Sol/总控处理**，不是已修订。
- 性质：数字、P3/confirmed和回放边界未变，属于引用定位erratum，不是SELECTION.md要求暂停该篇的实质L2判断错误，因此不阻断本期终选。画报/SOURCE已使用正确表号。

**实质判断退回0篇；非阻断定位勘误1项。** 三篇均无阻断性待补；更多迁移、独立SPAD在线、方差/能耗或裁判分类可靠性是待研究边界，不能把“未报告”当成实验失败。历史待补/correction不在本期复审范围。本期未做新增漏检抽查，不推断池外论文状态。

## 5. 成品与实际视觉QA

| ID | 成品目录 | 版式 | 最终尺寸 / QA |
|---|---|---|---|
| 2611.18747 | `reel/2611.18747/` | 暖米色三步重试流＋预算/音频双证据栏＋训练说明带 | PNG1600×2300；PDF1页1200×1725pt；ready |
| 2611.20488 | `reel/2611.20488/` | 紫灰纵向三层审计账单＋两张人工验证卡＋证据链 | PNG1400×2700；PDF1页1050×2025pt；ready |
| 2611.20772 | `reel/2611.20772/` | 蓝色硬件双栏板＋主系统表＋独立橙色虚线回放框 | PNG1800×2200；PDF1页1350×1650pt；ready |

三包均含poster.png、poster.pdf、SOURCE.md、QA.md、可编辑poster.html；assets仅含本地字体/渲染测量。实际执行顺序为逐篇全文核对、终选，再制作。

首版三张均实际打开PNG预览：文字/布局无明显缺陷，但画布高度不足，PDF各2页，均判失败。每张只重做一次，扩大画布（2100→2300、2300→2700、1900→2200px）。最终实际打开三张poster.png和三份PDF的栅格图，核对中文、数据、限制框、来源与页尾；DOM横向文字溢出为空、字体加载成功、PDF均1页。PDF/PNG同版，页脚下余量约97/127/128px。详见各QA.md，未将结构检查冒称视觉检查或科学验证。

缩略图可辨标题/主数字，细脚注需放大，不宣称手机原宽全文可读。自定义HTML由本地Chrome渲染，HTTP(S)阻断；仅参考paper2assets溯源原则，不声称完整paper2poster/PPTX流程。未对外托管或上传。

## 6. 索引维护与任务边界

- `reel/README.md`追加第十七期，52张/rolling33；`README.md`头部仅49→52、30→33，保留原19张featured wall的历史说明。
- poster.html与assets沿用既有忽略规则，仅本地；不修改.gitignore。
- 不写共享progress.md，由总控接手。未改评分batch、领域卡、配置、插件或其他任务文件。
- 未操作git、未派子代理、未启动无头Claude/模型调用框架；无实验复现。
