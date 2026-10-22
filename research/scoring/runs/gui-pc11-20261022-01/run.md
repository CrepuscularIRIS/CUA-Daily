# run: gui-pc11-20261022-01

- 规则:`problem-core-v1.1`(research/scoring/PROBLEM_CORE.md);执行 research/scoring/SOL_BATCH_PROMPT.md;选择 SELECTION.md;Reel OPUS_REEL_PROMPT.md
- git HEAD at start: `47f3cd5`(main)
- 模型:6.1 Sol(claude-kimi `sonnet` 槽,CC 内置 Subagent);总控 claude-kimi
- 卡片:patterns/main 18 主卡 + patterns/sub 子卡,版本=当前 HEAD;PROBLEM_MAP.md v1 映射仅作检索
- 输入:A/B 档全部 1331 篇(screen.jsonl A/B ∩ corpus);L1 材料=摘要+引言(cut_l1.py 从缓存全文切,markdown 标题解析;1311 abstract_intro / 20 abstract),l1_manifest.tsv
- 批次:p000=试点 10 篇(含 1 诊断审计、2 摘要-only、1 综述、随机混合);p001–p067 每批 20 篇
- 并发:默认 4,滚动补位,无限流可升 6–8
- **L2 预算:篇数上限 = 266(L1 的 20%);token 上限不做硬限但按批记录**;其中 10%(26 篇)固定从 P0/P1、F0、needs_material、park 随机抽取(随机种子 run 记录于 L2 排队时)
- 校验:research/scoring/tools/l1_check.py(枚举/封顶/facts 定位/ID 一一对应)
- 旧 v3 run 与 Reel 已撤下(ea587f0;本地备份 ~/GUI/moved-out-2026-10-22/gui-v3-run1/,git 历史至 ba95313);旧数值不作输入
