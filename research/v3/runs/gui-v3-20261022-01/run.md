# run: gui-v3-20261022-01

- profile: `gui-v3`(G 15 / M 25 / X 20 / E 40;`screen_score = (15G+25M+20X+40E)/4`)
- 规则版本:`sol-batch-v3`,单模型 6.1 Sol(claude-kimi `sonnet` 槽,LiteLLM 127.0.0.1:4001),无第二席/无聚合/无校准冻结
- git HEAD at start: `66d493d`(CUA-Daily main)
- 评分规则:`research/v3/SCORE_SPEC.md`(sha256 见 MANIFEST 于草稿包 `/home/lingxufeng/radar-scoring-v3-draft/MANIFEST.tsv`);执行提示词 `research/v3/SOL_BATCH_PROMPT.md`;卡片索引 `research/v3/RESEARCHSTUDIO_INDEX.md` + `research/v3/domains/gui-card-index.md`(原卡正文按需读取,evidence_level 词表用 `docs/EVIDENCE.md`)
- 语料:screen.jsonl 中 A/B 档共 1328 篇(A 701 / B 627;C 档为筛查排除的范围外,不评)。输入清单 `all-papers.tsv`
- 材料:`research/fulltext/<arxiv>.txt`(fetch_fulltext.py 抓取,单篇上限 40k 字符、保结果表 → 一律 `material_level=core`,裁剪文本不冒充 full);无缓存者先补抓,抓不到的按 abstract 评(`needs_material`,分数 null)
- 批次:按总文本长度分批(≤480k 字符/批,10–20 篇),输入映射 `batches/<bid>-inputs.tsv`,输出 `batches/<bid>.jsonl`;机械校验 `research/v3/check_batch.py`
- 并行约定:多批次 Sol subagent 并行;每个 worker 只写自己的 `batches/<bid>.jsonl`;`progress.md` 由总控维护(worker 不写共享文件)
- 后续:SELECTION.md → top15 候选 → Opus 5.5(`fable` 槽)原文核对 + ≤9 篇 Reel(`research/v3/OPUS_REEL_PROMPT.md`)
