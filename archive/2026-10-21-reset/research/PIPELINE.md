# CUA Radar build log (started 2026-10-19)

Goal: a quote-backed, pattern-card-based board for computer-use / GUI / browser agents, built on the pipeline cloned
from HarnessRSI Daily. This file is the log of **this** build: what was done, with counts, and what remains. The
general, repeatable procedure is [`docs/PIPELINE.md`](../docs/PIPELINE.md).

Each wake-up: check background tasks/agents → do the first unchecked step whose inputs exist → tick it here → commit.
Never re-launch work that is still running.

## Done
- [x] 1 **Corpus**: 2,707 arXiv papers harvested by `research/build_corpus.py` from the 7 lists in `refs/lists/`
  (OSU-NLP-Group/GUI-Agents-Paper-List, reacher-z/Awesome-CUA, showlab/Awesome-GUI-Agent, trycua/acu,
  ranpox/awesome-computer-use, ZJU-REAL/Awesome-GUI-Agents, steel-dev/awesome-web-agents) → `research/corpus.jsonl`.
- [x] 2 **Screening** per `research/SCREEN_RUBRIC.md` → `research/screen.jsonl`: **A 689 / B 616 / C 1,402**. 165 of the
  C rows are automatic, because the primary arXiv category lies outside cs / stat.ML / eess (`research/screen/auto_c.jsonl`). A/B ids:
  `research/ab_ids.txt` (1,305).
- [x] 3 **Pattern induction** with Open Scientist: two domain builds, `.forge/domains/cua-agents/v1` and
  `.forge/domains/cua-agents-core/v1`, each from 40 full-text readings → sub-patterns K01–K35 and C01–C37 (the core
  domain's K01–K37 renumbered). Merged into 15 main patterns.
- [x] 4 **Cards and standards**: `patterns/main/*.md`, `patterns/sub/*.md`, `patterns/overview.md`,
  `patterns/anti-patterns.md` (AP1–AP22); `research/patterns/taxonomy.json` / `taxonomy_view.json`;
  `research/patterns/conditions.json` (S/F ids, via `build_conditions.py`); `research/EVIDENCE_SCHEMA.md` (9 items,
  from `.forge/domains/cua-agents/v1/profile/expectations.json`); `research/SCORE_SPEC.md`; `docs/agents/JUDGE_BATCH.md`.
- [x] 5 **Trial**: 5 anchor papers assigned, judged and scored end to end (`research/trial/`).
- [x] 6 **Wave 1**: the first 100 papers (`research/trial/wave1.txt`, batches b00–b09). 32 weak fits →
  sub-patterns **R01–R03** induced from them (domain `board-induced`), each opening a new main pattern. The success
  conditions and failure modes of the 15 existing mains are unchanged. Result: **18 main patterns / 75 sub-patterns**.
  Re-assignments: `research/patterns/reassign_wave1.jsonl`.
- [x] 7 **First board selected**: tier A, published 2025 or later → **568 papers** (`research/board1_ids.txt`). The other
  **737** A/B papers → `research/queue/2026-10-19-backlog.txt`.
- [x] 8 **Docs rewritten for CUA Radar** (README, AGENTS, docs/, agent prompts, config, CI). The CI workflow now runs
  only the checks that work here.

## Done (2026-10-20)
- [x] 9 **Board scoring**: all 568 board-1 papers assigned and judged in 57 batches (`research/judgments/b00`–`b57`;
  wave-1 papers moved to R01–R03 were re-judged in `b10`); every batch passes `score.py check`; `score.py build`
  scored 568 (0 skipped); `build_board.py` wrote `papers/README.md` and the README top-30. 5 papers have no HTML
  full text and are listed as "not ranked". Result: median 47, max 86; ★★★ 25 · ★★ 208 · ★ 273 · — 57; evidence level
  online 309 · offline 144 · transfer 94 · unclear 21; `weak` fits 160/568 (28%).
- [x] 10 **HF code metadata**: `research/hf_meta.jsonl` (GitHub links for 157 board papers); 231 papers get the Code
  part from some source.
- [x] Calibration run 1 (blind re-judge of 3 gold papers): PASS — see `research/calibration/README.md`.
- [x] Bot prompts: `docs/agents/GROK_PROMPT.md` and `docs/agents/DOTS_PROMPT.md` (superseded 2026-10-21, see below).
- [x] 11 **Publish**: public repo `CrepuscularIRIS/cua-architecture-radar`.

## Done (2026-10-21)
- [x] 12 **Architecture change: scoring went local, multi-model.** Dots (cloud scorer) never started (0 commits);
  Grok is collect-only now (`GROK_PROMPT.md` shrunk, ingest/maintenance moved local). Judging is two blind seats
  (`gpt-6.1-sol` + `claude-sonnet-5-5`, each following `docs/agents/JUDGE_BATCH.md`) merged deterministically by
  `research/merge_judgments.py` (agreement kept, disagreement FLAGged), with one `claude-opus-5-5` arbitrator per
  batch resolving FLAGs with verbatim quotes. Procedure: `docs/agents/JUDGE_LOCAL.md`; roles/monitor updated.
  Motivation: the 568-paper board was single-model judged; board-1 will be re-judged dual-seat (later batch wins).

## Known issues (open)
- **Taxonomy ageing.** Weak fits run ~15–20% for 2025 papers but 30–60% for some 2026 batches (bundled multi-stage
  training recipes, guardrail/corrector models, edge–cloud routing, KV-cache compression, model routing). Per the
  monthly rule, propose (do not silently apply) a revision from the `fit_note`s of weak rows; existing mains' S/F ids
  must stay stable or the affected papers must be re-judged.
- **Condensed full text.** Long technical reports (e.g. GUI-Owl-1.5, UI-Venus-2, Xiaomi-GUI-0) exceed the 40k-char
  extract, so their RL/ablation sections are partly `[...]` and those items are `unclear`. A section-aware extract
  that always keeps result tables would fix this.
- **Wave-1 texts (100 papers, `research/trial/wave1.txt`)** were extracted before MathML numbers were kept, so some
  table numbers were missing when they were judged. Re-judge them in a new batch when convenient (the later batch wins).
- 2505.13887 is an abstract-only duplicate of 2502.17110.

## Remaining
- [ ] 12 Backlog queue (737 A/B: tier B + tier A before 2025), daily collection (Grok), weekly diagnosis cards,
  Reel posters (inherited scripts not yet adapted), Repo Score (separate, planned).

## Inherited, not yet adapted
These HarnessRSI Daily scripts and specs stay in the tree but have no CUA use yet. Do not rely on them.
- `research/openreview_pull.py`: pulls ICLR submissions matching harness-RSI terms from OpenReview (incl. rejected/withdrawn).
- `research/openreview_labels.py`: attaches OpenReview accept/reject labels to corpus papers.
- `research/fetch_reviews.py`: fetches ICLR reviews for the outcome-contrast set (rate-limited, needs credentials).
- `research/fetch_openreview_pdf.py`: downloads OpenReview PDFs as full text for non-arXiv submissions.
- `research/or_to_arxiv.py`: maps OpenReview forums to arXiv ids by fuzzy title.
- `research/contrast.py`: accept-rate statistics per pattern; there are no outcome labels in this build.
- `research/build_bundles.py`: builds per-pattern reading bundles for card writing from signatures.
- `research/check_patterns.py`: checks HarnessRSI card counts against `contrast.json`; there is no contrast data here.
- `research/calibrate.py`: compares re-judgments with a gold set `research/judgments/pilot.jsonl`, which does not exist yet.
- `research/reel_candidates.py`, `research/check_reel.py`, `research/setup_reel.sh`: Reel poster pipeline
  (ResearchStudio); no `reel/` directory yet. The README keeps the empty `REEL` block for `build_board.py`.
- `research/check_signatures.py` + `research/SIGNATURE_SCHEMA.md`: signature extraction for HarnessRSI pattern
  induction; here Open Scientist readings replaced signatures.
- `research/monitor.py`: hourly repo health check. It still expects Reel and signature files, and its repo name is assumed.
- `research/build_corpus.py` is adapted and used (step 1). `research/ingest.py` and `research/fetch_hf_meta.py` are used as is.

## Notes / decisions
- No outcome labels (venue, acceptance) are used anywhere in this build, so cards hold no accept rates.
- The score measures reported evidence and execution against the pattern card, not idea value. Repo Score is separate.
- Full texts stay local (`research/fulltext/` is gitignored).
