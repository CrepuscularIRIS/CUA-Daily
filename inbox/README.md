# 候选收集 inbox

Grok 只写本目录。使用 [GROK_PROMPT](../docs/agents/GROK_PROMPT.md) 的字段与高质量线索门槛。
每次一份 `YYYY-MM-DD-<run-id>.jsonl`，每行一个候选；另附 `-run.md` 记录覆盖、排除和失败来源。
保留既有历史候选，不因新字段要求删除旧输入。

兼容本地入库的最小字段：arxiv（无则 null）、url、title、source、github、why、found。
新记录额外保留 version、published、discovered_at、primary_url、source_urls、candidate_status、update_of、
mechanism、evaluation_signal、evidence_locator、retrieval_notes。全文未读则明确写 needs_fulltext。

去重以去版本 ID/DOI/官方 URL 与标题为线索，最终需核对来源。版本更新单独标 update_of。
本地 `research/ingest.py` 只接收新 arXiv ID，更新/无 arXiv 记录仍留待处理。
必须逐行记录处理结果后才移动到 processed，不能因部分成功丢掉未处理候选。

## 统一 JSONL 模板

下面是字段模板，不是真实候选；替换占位内容后每个候选写成单独一行。

```json
{"arxiv":null,"url":"<官方论文或报告 URL>","title":"<核实后的标题>","source":"arxiv-listing|hf-daily|github|official-report","github":null,"why":"<具体机制与本项目的关系>","found":"YYYY-MM-DD","version":null,"published":null,"discovered_at":"<UTC ISO timestamp>","primary_url":"<已打开的一手来源 URL>","source_urls":["<发现来源 URL>"],"candidate_status":"needs_fulltext","update_of":null,"mechanism":"<改变的具体环节>","evaluation_signal":"<作者报告的实验设计，未看到则 null>","evidence_locator":"<摘要/章节/表/页>","retrieval_notes":"<实际读取范围与缺失项>"}
```

`arxiv` 使用不含 vN 的真实 ID；`version` 单列 vN；`update_of` 指向该论文已有 ID 与旧版本。
`candidate_status=ready` 仅指候选来源与范围可交接，不表示质量审查通过。
