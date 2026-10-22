# CUA-Daily：领域 pattern 评分

规则版本 `sol-domain-v3.1`，profile `gui-v3.1`。旧 v2/v3 结果全部撤下；本次仅统一规则和清理产物，没有执行新版评分。

- [评分规则](SCORE_SPEC.md)与[领域配置](PROFILE.md)
- [领域卡索引](PATTERN_INDEX.md)：只作检索，评分必须读取相关卡的条件与期望。
- [CC / Sol 批量提示词](SOL_BATCH_PROMPT.md)：内置 Subagent，默认 4 并发，每批 10–20 篇，滚动补位。
- [候选选择](SELECTION.md)与[Opus Reel 提示词](OPUS_REEL_PROMPT.md)
- [虚构输出示例](EXAMPLES.md)：只说明格式，不进入榜单。

未来明确执行新版评分时，使用独立 `research/scoring/runs/<run_id>/`；不要复活历史 run 或把旧记录改字段冒充新结果。完整材料保留在原有忽略目录，不能重新批量下载已完整缓存的论文。
