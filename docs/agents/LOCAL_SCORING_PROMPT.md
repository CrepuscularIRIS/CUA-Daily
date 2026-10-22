# claude-kimi / Claude Code 总控提示词 — GUI Agents 大规模双席评分 v2.2

你是通过 **claude-kimi** 启动的 Claude Code 总控。用户让你执行本提示词时，在当前仓库完成：领域 pattern 识别、校准、分批独立初评、Opus 聚合、逐轮验收、最后本地提交。
遵循 ResearchStudio Idea 原 15 主卡＋31 子卡，迁移到本领域；评分基于全文、gap、操作、领域模式、审稿期望和证据。
保留既有模式卡，旧分数/旧 Reel/旧 VERIFIED 全部退出输入。不要运行 archive 中的旧 merge/scorer 或旧批次。
本次只编写需求文档，不实现调度器、不运行模型评分；以下动作在用户后续把此文交给 claude-kimi 执行时进行。
当前文件是执行提示词，不代表它已经执行。不要把“写了计划”报成“论文已评完”。

## 0. 必读和当前范围

读 AGENTS.md、docs/MAINTAINING.md、docs/EVIDENCE.md、docs/PIPELINE.md、research/PATTERN_PROTOCOL.md、
research/SCORE_SPEC.md、research/REVIEW_WORKSHEET.md、research/BATCH_CONTRACT.md、docs/REEL_SELECTION.md。
按原 15+31 识别是每篇必经；outside_taxonomy/null 子卡仅按原规则允许，不得省略识别。
本仓库领域 namespace：`gui`。三个仓库各自运行、各自冻结、各自提交，不共用评分榜或研究状态。

用户未指定论文范围时：固定当前 corpus 快照，处理范围内且没有本版有效 judgment 的论文；历史 screen/assignments 只做队列线索，不能直接当新结论。
缺材料、范围外、待证据、重复版本逐篇留 disposition，不能静默丢掉。版本更新采用显式 supersedes。
本轮任务不运行论文代码、训练、机器人或模拟器，不联系作者；全文/私有配置/凭据不提交。

## 1. 使用已经配置好的 model type

用户已经配置好 claude-kimi 环境中的 model type。直接用现有对应类型派发 Subagent，不重新配置、不另建代理、不进行模型探测、不要求用户再次提供模型映射。
本文件只规定职责；不要把下表角色名当成新的配置键或覆盖已有 model type。

| 角色 | 使用现有 model type 对应的模型 | 职责 |
|---|---|---|
| 总控 | claude-kimi | 分批、派发、轮次管理、验收、最终提交 |
| sol | 6.1 Sol | 独立全文初评与原卡/领域卡识别 |
| son55 | Sonnet 5.5 | 相同输入的独立初评 |
| opus55 | Opus 5.5 | 逐篇证据核查、分歧裁决、最终聚合 |
| reel | GLM 5.3 | 仅给选中论文制作画报，见 REEL_PROMPT |

在任务记录中写使用的已配置 model type；现有运行记录提供模型/会话信息时一并保留，不为缺少额外探测凭据阻塞正常流程。
实际调用报错则报告并按重试规则处理，不把一席失败当作双席完成，也不自行替换指定模型。
GLM 失败只影响 Reel，不阻塞已经验收的评分提交。

## 2. 初始化可恢复的运行

创建唯一 run_id，例如 `gui-v22-YYYYMMDD-01`；先记录 git HEAD、已有脏文件路径和 hash，确保不覆盖他人工作。
在 research/v2/runs/<run_id>/ 按 BATCH_CONTRACT 创建 manifest、queue、batches、轮次状态、校准与最终索引。
固定 corpus ID/version 集合、原卡 manifest hash、领域卡/expectations/rubric hash、所用 model type、批大小、并发数和预算范围。
私有全文与调用日志放 research/fulltext/review-runs/<run_id>/（沿用已有 gitignore），公开审核摘要只含来源引用、hash、判定与必要模型信息。

默认 batch_size=5（长文降至 1–3；上限 10），parallel_batches=2；每轮最多 4 个初评 worker，随后最多 2 个 Opus worker。
两个 worker 必须评同一批全部论文；不是把一半论文给 Sol、一半给 Sonnet。
大任务按轮推进而不是一次启动几百子代理。上下文不足拆小批，不摘要全文来节省判断步骤。

## 3. 先校准，再分轮评分

1. 使用 SCORE_SPEC 的 6 篇开发＋12 篇留出；按类型、机制、证据强弱分层，记录选择依据，不能只挑旧高分。
2. 同样由 Sol/Sonnet 独立初评，Opus 聚合。两份初评原件都保留；在 Opus 裁决前测一致性，不能拿裁决后的相同结果算一致性。
3. 校准原 15+31 到领域卡的适用判据及评分锚点；无真实 review 继续按来源分级使用审稿期望。
4. 沿用 SCORE_SPEC 的初始权重作为待检验方案；开发阶段修订锚点要记录，留出集不调权。若需改权重/硬范围而用户尚未授权，提交具体依据。
5. 按 BATCH_CONTRACT 检查覆盖、引用、分歧与算分；使用执行环境已有能力。不要复活旧评分规则，也不要把此需求扩展成先搭建一套调度平台。
6. 校准通过并留下报告后，总控记录冻结的 rubric/profile/card 版本，继续生产，不反复请求已授权的批量操作；未过按 spec 最多两轮修订，仍未过停止批量。

本文规定结果和验收要求，不要求新建调度器、模型适配器或完整软件框架。算分与结构检查可用已有工具或按需的小脚本，不能声称运行了不存在的 v2 命令。
机械核对只覆盖结构、引用存在和算术；科学语义由两席初评与 Opus 聚合判断。

## 4. 每轮派发：准备 → 双席 → 聚合 → 验收

A. 总控准备不可变的材料包：固定版本完整正文/附录、原卡索引与候选卡、领域卡/期望、rubric、工作表和本批 IDs。
材料包不得预填 gap 结论、模式归属或分数；两席各自分析。共享事实来源允许，共享判断不允许。

B. 对每批并行派两名 worker，使用 JUDGE_BATCH.md。只给它本批输入和自己的输出目录；两个初评 worker 不互看结果。
每个 worker 用新上下文，逐篇写完整记录后再下一篇；已经完成的原子文件可在中断后恢复。
worker 不使用 git、不写全局 score/queue/card，不覆盖他人文件。它们不是独占代码库，必须保留其他人的编辑。

可直接复制的派发词（替换尖括号参数）：

> 你是 <sol|son55> 席，使用已经配置好的 <对应 model type>。仅处理 run=<run_id>、batch=<batch_id>、attempt=<attempt_id>。
> 读 docs/agents/JUDGE_BATCH.md 与本批 inputs/manifest；不得读取另一席、Opus、旧分数或旧 Reel。
> 你仅拥有本批 seats/<seat>/attempts/<attempt_id>/，不是唯一写入者；不得改他人文件、共享索引或 git。
> 逐篇读完整材料，依次做签名、gap/谱系、原15+31识别、领域条件/审稿期望、证据判断和分项评分。
> 输出每篇 JSON 与 readable rationale，完成 batch report；缺材料如实记状态，不靠 unknown 填满伪造完成。

C. 总控校验两席覆盖/版本/所用 model type/引用/hash/算式，生成逐字段差异；不先选边或算平均。
输入版本不同或缺席先修复，不能让 Opus 在不同版本上强行裁决。

D. 每批派 Opus，使用 AGGREGATE_OPUS.md。它检查每篇，而非只看总分差异；同分也可能共享错误。
Opus 对所有实质分歧读原文裁决，记录证据；可以选 A、选 B、两者都错、证据不足，不能靠多数/地位/折中。

E. 总控检查最终结果与裁决覆盖，确定性重算总分，写本轮索引/报告/状态；只对 accepted_final 结果更新当前有效索引。
问题论文可挂 needs_fulltext / needs_evidence，不阻塞同轮其他合格结果，但整个运行报告仍须列待处理数，不宣称全量完成。
然后开启下一轮，直到固定队列都已有明确 disposition，或达到用户预算/时限/停止要求。

## 5. 大语料恢复、失败与质量

- 进度唯一键为 paper_id+version+material_hash+rubric_hash+seat+attempt；不要只看“某文件存在”。
- 断点恢复先校验 hash 和状态；不重跑已验证原件，不将缺席/超时当作 0 分，也不把失败批次标 done。
- 临时服务/格式错误每个任务最多重试两次，保留 attempt；持续错误停该任务并报告。实际调用失败不得记作已完成。
- 每轮总控核论文数、缺失数、冲突数、未解数、outside_taxonomy 比例、每席耗时/实际可得用量，不能估算冒充账单。
- 若一轮出现核心主张语义错误、材料截断误当未报告或伪造调用结果，暂停后续新批；定位受影响范围并重评，不用增加投票掩盖。
- batch-size/concurrency 可为上下文/限流调小；不得为吞吐量减少全文、原卡识别或另一初评席。
- 新论文引出的领域卡 revision 单独积累；生产 rubric 不随轮次漂移。阶段末领域归纳仍按 PATTERN_PROTOCOL。

## 6. 选题、Reel 与最终提交

全量评分和制作数量分开：处理很多论文不等于做很多海报。
审核分数按 docs/REEL_SELECTION.md 的 quality_floor/名额选择，默认一期最多 9；阈值未指定时先交分布，不妨碍完成和提交评分。
选中名单交 GLM 5.3 按 REEL_PROMPT.md 制作；GLM 不能更改评分，发现新证据回退至评审。

只有总控操作 git。每轮写 checkpoint；本次授权队列处理结束/达到明确停止点后汇总，并做一个本地 commit，标题 `review: <domain> <run_id> (<final> final, <blocked> blocked)`。
用显式文件列表暂存本次结果、校准/契约/工具与报告；先检查 diff、secret/fulltext、ignore、已有脏改，不用 git add .，不包含他人工作。
可以提交明确标为未完成的检查点，但提交说明必须写 partial，不能写 all done。不要自动 force push；远端推送只有用户明确授权时进行。
Reel 成品单独验收、单独提交，不因渲染尚未完成拖住已验收的评分。
最终报告：使用的 model type、冻结规则、语料覆盖/缺失、双席/聚合结果、未解分歧、评分分布、入选数、Reel状态、commit与未完成项。
