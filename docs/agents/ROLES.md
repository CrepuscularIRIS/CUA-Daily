# 分工（v2.2）

| 角色 | 模型/执行者 | 所有权与任务 |
|---|---|---|
| 收集 | Grok | 只写 inbox，不评分 |
| 总控 | claude-kimi / Claude Code | 固定范围/材料/规则、派子代理、检查、断点恢复、轮次索引、最终 git 提交 |
| 独立初评1 | 6.1 Sol | 每个批次的完整论文集，原15+31识别＋领域判断＋评分；只写本席 attempt |
| 独立初评2 | Sonnet 5.5 | 同批同材料独立评，不看初评1；只写本席 attempt |
| 聚合 | Opus 5.5 | 每篇核查，裁决所有实质分歧和共有错误；只写 aggregate attempt |
| 画报 | GLM 5.3 | 只处理已评分并经阈值选中的论文；只写分配的 Reel 目录 |

入口：[LOCAL_SCORING_PROMPT](LOCAL_SCORING_PROMPT.md)、[JUDGE_BATCH](JUDGE_BATCH.md)、[AGGREGATE_OPUS](AGGREGATE_OPUS.md)、[REEL_PROMPT](REEL_PROMPT.md)。
恢复的是用户指定的双席＋Opus角色分工，不恢复旧分数、旧证据规则或旧批次入口。
用户已配置 model type，直接沿用 claude-kimi 的对应类型，不增加配置或探测步骤。任何 worker 都不是唯一写入者，不可撤销他人编辑，不得操作 git。
