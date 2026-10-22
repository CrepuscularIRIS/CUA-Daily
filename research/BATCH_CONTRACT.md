# GUI Agents：批次、记录与验收契约 v2.2

这是后续模型执行的格式契约；当前不包含已完成的新评分，也不声称已有 v2 机器 validator。
旧 research/score.py、merge_judgments.py、make_batches.py 继续退役。本文件只写记录和验收要求，不要求先开发调度器或新评分软件。后续由 claude-kimi 使用既有能力及按需的小脚本执行核对。

## 输入固定与目录

```text
research/v2/runs/<run_id>/
  manifest.json                  # 范围、corpus/rubric/cards/expectations hashes、所用 model type
  queue.jsonl                    # 每篇 ID/version/paper_key、状态与有效 attempt 指针
  calibration/                   # 开发/留出计划、两席原件引用、Opus意见、锚点、冻结报告
  batches/<batch_id>/
    manifest.json                # 精确 IDs/版本/材料 hash/输入包 hash；每席完全相同
    seats/sol/attempts/<a>/       # 每篇 JSON + batch-report.json；仅该 worker 写
    seats/son55/attempts/<a>/
    conflicts.json               # 总控产出，不让 worker 互相查看
    aggregate/attempts/<a>/       # Opus final records + resolutions + batch report
  rounds/<round_id>.json         # 总控 checkpoint，引用所有有效 attempts/hashes
  final/index.jsonl              # accepted_final 的唯一有效记录指针与分数
  final/report.md                # 覆盖率、阻塞、分歧、分布、模型和检查边界
  selections/                    # 有阈值时才生成；不是把整个 index 送 Reel
```

状态只能随证据推进：queued → material_ready → dual_reviewed → aggregated → validated。
needs_fulltext / needs_evidence / retryable_error / model_unavailable / out_of_scope 是可追溯 disposition；不等于 scored。
一个 seat 完成不能使论文进入 dual_reviewed；worker 只写自己目录，总控拥有共享状态与 git。
每份文件先临时写入后原子完成；attempt 关闭后不修改，纠错创建新 attempt 并显式 supersedes。
私有原文/日志放已有 gitignored 的 research/fulltext/review-runs/<run_id>/；公开记录可保留 hash 引用但不提交原件，提交前校验 ignore 规则；不要把 secret 写进任何公开 JSON。

## 初评 record 必需字段

| 字段 | 契约 |
|---|---|
| schema_version | radar-review-v2.2 |
| run_id / batch_id / attempt_id / seat | manifest 指定，seat=sol 或 son55 |
| paper | paper_key、paper_id、title、version、claim_type、central_claim（原主张） |
| provenance | input_hash、rubric_version/hash、rs_manifest_hash、domain_cards_hash、expectations_hash、model_type（现有配置）、actual_model/session_id/receipt_ref（现有运行记录可得时保存，否则null+原因）、timestamp |
| materials[] | material_id、版本化 URL、sha256、sections_read、complete、missing_sections |
| evidence[] | evidence_id、material_id/hash、locator、连续原文 quote、support_explanation、kind（author_report / our_inference / reviewer_comment / static_code_check / our_run） |
| signatures[] | sig_id、object、information、operation、output、conditions、feedback、selection_rule/data、persistence、later_use、claimed_effect、failure_boundary、evidence_ids |
| gap | author_gap、checked_gap、lineage/closest_adjacent（含来源版本）、residue、stakes、method_response、remaining_gap、evidence_ids、unresolved |
| rs_pattern | primary、supporting（至多2）、matches[]、outside_taxonomy、reason、executes_pattern、resolves_problem |
| domain_pattern | namespace=gui、matches[]（main/sub/version/fit/condition_checks/evidence_ids）、unassigned、revision_proposals |
| pattern_mapping[] | rs_main、rs_sub或null、domain namespace/main/sub、operation correspondence、必要条件/差异、evidence_ids；不可仅字符串相似 |
| expectations[] | id/version、source_strength、source_refs、applies_when、applicable、status、reason、evidence_ids、score_item |
| claims[] | claim_id/text、setting、baseline/control、selection_vs_test、result/denominator、evidence_ids、counterevidence、allowed_conclusion |
| assessment | evidence_level、claim_support、strongest_supported_claim、unresolved；不得虚称复现 |
| ratings | G、M、X、E.measurement、E.causality、E.holdout、E.statistics、E.cost 八项；结构见下 |
| score | raw、display、lower、upper、coverage、rubric_hash；机械重算，unknown 时 raw/display=null |
| status | reviewed / needs_fulltext / needs_evidence / out_of_scope；理由必填 |

rs_pattern.matches 每项包含 main_id、sub_id或null、role、fit、tactic_steps_checked、success/failure_checks、evidence_ids、reason。
sub_id 必须在固定父类下；outside_taxonomy=true 时 primary=null 且 matches/supporting 为空，但 reason 非空。
无子卡适用时填 null，不创造 C31。一个匹配条目对应一张主卡及其最贴切子卡；不要重复主卡来凑 supporting。
fields 内的未适用项可带 not_applicable+reason；评分八项不能通过 N/A 改分母，按预先冻结的 claim_type 解释判断。

每个 rating：

```json
{"status":"resolved","rating":2,"reason":"逐项解释，不能只填中等",
 "evidence_ids":["E001"],"counterevidence_ids":[],"search_scope":[]}
```

rating 只能整数 0..4 或 null；status=unknown 则 rating=null；status=not_reported 则 rating=0 且 search_scope 非空。
对 negative/unknown 事实不要伪造 quote。引文只保留判断必需的短连续片段，完整材料在上述本地全文目录中。
rs/domain 条件的 status=not_applicable 不意味着 rating 自动4；score 按 SCORE_SPEC 固定权重计算。
缺完整材料仍输出 paper/provenance/materials/status/reason，其他分析字段可空且八项均 unknown；score=null，L=0、U=100、coverage=0。
范围外行保留 manifest 身份、来源与排除理由，score=null，不把排除算作完成评分。

## 聚合 record 与分歧

最终文件增加 input_seat_hashes（必须两席）、aggregate_model/session/receipt_ref、resolutions[]、shared_error_corrections[]、aggregate_status、final_record_hash。
final_record_hash 的规范：对移除 final_record_hash 字段后的完整 record 使用 UTF-8、sort_keys=true、紧凑 JSON、ensure_ascii=false 编码取 SHA-256；审核只绑定此内容。

每条 resolution：field_path、sol_value、son55_value、decision（sol/son55/revised/unresolved/same_supported_fact）、
final_value、reason、evidence_ids、score_impact；不能只写“采纳 Opus”。未解的评分/核心主张分歧不得 accepted_final。
机械 conflicts 比较主张类型/范围、模式/父子关系/适用条件、expectations 回答、evidence_level、claim_support、八项 status/rating、材料/规则 hashes。
措辞/引用片段不同不必等于事实冲突，但都留下差异让 Opus判断；任何整数档位差异都列出，不设总分差阈值忽略。

## 总控须完成的验收检查

1. 双席集合与 batch manifest 完全相等；禁止缺行、额外 ID、重复记录、同版本静默覆盖。
2. 记录使用的已配置 model type；两席和聚合职责对应正确。使用现有调用信息，不额外探测，不因缺少额外凭据阻塞；失败调用不能伪造为完成。
3. 同一输入 hash；全文/卡片/期望/rubric 绑定有效；引用 material_id/hash/locator 存在且连续原文能匹配。机械匹配不能代替语义检查。
4. 原卡 15 个 ID、C00–C30 父类、domain namespace 合法；不允许裸 C15 同时表示两套卡。
5. 八项档位、状态与引用/查找范围一致；unknown 不产生点分；E 五项权重和等于 E 总权重，总和100。
6. 确定性计算 score raw/display/L/U/coverage，不平均两席总分，不重复计入 E 总权重；筛选用 raw。
7. 所有实质冲突有 resolution；Opus 逐篇核过核心证据；resolved 的理由/证据不空。无冲突也要有 Opus 每篇审核结果。
8. 修改 final 内容使旧 final_record_hash 和审核失效；当前 index 只引用有效 accepted_final，不引用 pending 文件。
9. 断点恢复只信当前 hash/模型/版本；同一完成 attempt 不重复算，旧版分数不得自动继承。
10. 队列总数 = 所有互斥 disposition 之和，另列 scored 与 blocked；显示分数与未四舍五入阈值比较不混用。

使用合成 fixture 验证以上失败例：缺一席、额外/重复 ID、错误父卡、混 namespace、截断全文、unknown、引用不存在、实际派错席位、未解分歧、hash变更、恢复重复、阈值边界。
这些测试是结构/算术验收，不是模型评分质量的证明；语义可靠性仍看全文复核和开发/留出校准。
