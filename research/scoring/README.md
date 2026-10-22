# CUA-Daily：问题优先的论文评价

规则版本 `problem-core-v1.1`，三个项目共用同一套规则。旧 v2/v3 结果全部撤下；`sol-domain-v3.1` 的四轴与 `screen_score` 已停用。新规范尚未试点，没有执行任何评价。

- [问题核心](PROBLEM_CORE.md)：两层评价、四个问题、档位／优先级／证据状态、漏斗与预算、试点。三项目共用。
- [问题族映射](PROBLEM_MAP.md)：本项目主卡对应的问题族。
- [领域配置](PROFILE.md)：收录范围与证据等级。
- [领域卡索引](PATTERN_INDEX.md)：只作检索，判断必须读取相关卡原文。
- [CC / Sol 批量提示词](SOL_BATCH_PROMPT.md)：L1／L2 派发，默认 4 并发，滚动补位。三项目共用。
- [候选选择](SELECTION.md)与[Opus Reel 提示词](OPUS_REEL_PROMPT.md)：三项目共用。
- [虚构输出示例](EXAMPLES.md)：只说明格式，不进入任何名单。
- [SCORE_SPEC.md](SCORE_SPEC.md)：已停用的 v3.1 四轴规范，仅作历史。

未来明确执行新版评价时，使用独立 `research/scoring/runs/<run_id>/`；不要复活历史 run 或把旧记录改字段冒充新结果。完整材料保留在原有忽略目录，不能重新批量下载已完整缓存的论文。
