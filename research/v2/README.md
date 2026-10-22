# v2.2 本地评审工作区

当前 draft_uncalibrated：没有新阅读判定、分数或选题；先读 ../../docs/agents/LOCAL_SCORING_PROMPT.md。
规划分别保存 readings/（材料 manifest、签名、gap）、calibration/（清单/锚点/报告）、judgments/（评分/审核）、selections/（动态阈值选题）。
全文留在 gitignored 本地目录；公共提交只含有意公开的来源引用和结果。
冻结前不建有效排名；selection 未形成前不生成 Reel。旧批次仅在 ../../archive/2026-10-21-reset/。

批量运行采用 runs/<run_id>/，见 ../BATCH_CONTRACT.md；两个独立初评席与 Opus 输出不得互相覆盖，私有原文/日志放已有 gitignored 的 research/fulltext/review-runs/<run_id>/，不提交。当前仅提示词/参考包，未运行批次。
