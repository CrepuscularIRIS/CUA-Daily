# 新版 CC 任务入口

当前旧产物已撤下；这次维护没有启动重评分。需要执行新版时，将下面提示词交给当前 CC 会话，并填明范围：

> 按 research/scoring/SOL_BATCH_PROMPT.md 和本仓库 PROFILE 执行我指定范围的论文评分。直接使用 CC 内置 Subagent，model type 使用已配置的 6.1 Sol，默认 4 批并行、每批 10–20 篇、完成即补派。直接依据本领域已完成的 pattern 卡及其判据评分，不使用原 15＋31 逐篇分类，不启动无头 Claude。保留旧产物撤下状态和原材料，只写新的 research/scoring/runs/<run_id>/。评分任务不自动启动 Reel；当我指定制作范围时再交 Opus 5.5 核对并制作。
