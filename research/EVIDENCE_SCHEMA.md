# v2.2 证据记录契约

旧 yes/no 九项 schema 已归档。当前规范：[SCORE_SPEC](SCORE_SPEC.md)、[逐篇工作表](REVIEW_WORKSHEET.md)。
状态 draft_uncalibrated；机器 schema、validator、scorer 和 selector 尚未实现，旧 check_evidence.py 不能验证此版。

评审包必须分开保存：identity/material manifest、operation signatures、gap/lineage、pattern applications、
reviewer expectations（含来源强度及适用性）、claim-evidence matrix、G/M/X/E ratings、claim_support、evidence_level、独立审核。
每条事实用 evidence ID 连接固定全文 hash、版本化 URL、节/页/表位置、连续原文与解释；未报告用查找范围作依据。
每个判断保存反证/未解问题；unknown、not_reported、not_applicable 不混用；适用性不能改变已冻结计分分母。
模型/会话、rubric、卡片、期望版本/hash 和 supersedes 明确。审核绑定完整 judgment hash，后续变更使审核失效。

选题独立保存输入集合、有效 judgment hashes、阈值、上限、去重/机制分组、入选与未选原因，见 ../docs/REEL_SELECTION.md。
不得把 selection 当评分记录，不把旧 VERIFIED.json 当语义验证，不自动迁移旧 judgment。

原15+31识别、领域模式命名空间、两席原件与Opus裁决字段以 [BATCH_CONTRACT](BATCH_CONTRACT.md) 为当前执行契约；结构化输出不能仅保留总分。
