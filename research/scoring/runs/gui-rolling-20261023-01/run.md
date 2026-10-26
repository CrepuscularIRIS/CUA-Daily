# Rolling run gui-rolling-20261023-01（CUA-Daily 增量轮）

- 规则：problem-core-v1.1（PROBLEM_CORE / SOL_BATCH_PROMPT，2026-10-22 版）。
- 启动：2026-10-23 巡检班开档（当时无可评新增）；首批评分于 2026-10-24 巡检班执行。Git HEAD（首批评分时）08e53b458afe0481fe0d63fe04e4cc5c1b7633e6；patterns 卡片版本 87e745d。
- 输入：queue/2026-10-24-0450.txt 7 篇（inbox/2026-10-23-0356 → ingest.py，corpus 1331→1338），L1 材料见本 run l1_material/（6 abstract_intro + 1 abstract）。
- 模型：6.1 Sol（claude-kimi `sonnet` 槽 → gpt-6.1-sol），CC 内置 Subagent，单初评席。
- 批大小：增量小批（7 篇）；并发 ≤4（本班 1 批）。
- L2 预算（2026-10-27 增量轮声明修订，替代原 max(2, 20%×累计 L1) 上限）：每班 = 本班 L1 产生的 to_l2 全部 + 上班遗留 high 队列最多 5 篇；漏检抽查名额 = 每班预算 10% 取整（0 则累计欠账，攒够 1 立即补抽）。token 不设硬额，逐批记录用量。
- 授权：用户 2026-10-23 会话授权的 6 小时巡检管线。
