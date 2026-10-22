# Reel — posters and interpretations of top papers

Made locally by the maintainers (an Opus session following [docs/agents/REEL_PROMPT.md](../docs/agents/REEL_PROMPT.md)),
not by Dots or the collector, with the [ResearchStudio-Reel](https://github.com/microsoft/ResearchStudio) skills.
Shown in the README poster gallery. Setup: `bash research/setup_reel.sh`. Gate: `python3 research/check_reel.py`.

- **Candidates:** [candidates.md](candidates.md) — every ranked board paper scoring ≥ 60 (abstract-only papers
  excluded), with its arXiv license. Refresh after the board changes: `python3 research/reel_candidates.py` (keeps `status`).
- **Figures:** `reuse` = CC BY / BY-SA / CC0 — the paper's figures may be shown, each credited. `redraw` = arXiv
  default or NC/ND license — no figure or screenshot from the paper; a diagram we draw ourselves, or none.
- **Order:** highest score first.

## Output (one directory per paper, committed)

```
reel/<arxiv_id>/
  poster.png     # ≤ 3 MB, gallery thumbnail
  poster.pdf     # print version
  blog_zh.md     # Chinese interpretation
  blog_en.md     # English interpretation
  SOURCE.md      # see below
```
Never committed: `poster.html`, `.pptx`, `.mp3`, `.docx`, videos, the `paper2assets` bundle, `research/paper_text/`.

`SOURCE.md` must contain these exact lines (checked):
- `Read from: arXiv <version>` — the version in `candidates.jsonl`, read from the PDF or arXiv HTML. No PDF → no poster.
- `Paper figures shown: none` — required when `figure_reuse` is false; otherwise a table of each figure shown and its credit.
- A note for every number marked `‡` (computed by us from paper numbers, e.g. a difference), saying how it was computed.

## Content standard
1. **The agent:** what it perceives (screenshots, accessibility tree, DOM, video), how it acts (coordinates, element
   ids, API/tool calls), and which platforms (desktop, mobile, web). Name the architecture pattern from the board.
2. **The mechanism:** what is new (grounding, planning, reflection, memory, data synthesis, RL recipe, world model, …),
   and what signal trains or steers it.
3. **Results exactly as reported:** model and size, benchmark, online vs offline, step budget, seeds/runs. Every
   decimal number must occur in the paper — the checker verifies this against the full text, tables included. Never
   recompute from a code repository or leaderboard.
4. **The paper's own controls** that decide whether the gain is real: ablations, the same base model or budget for
   baselines, held-out apps/sites (apps used for exploration or data synthesis are not held-out), live vs offline
   evaluation, validation of any learned judge or reward model. The takeaway follows from these, not from the headline.
5. Where gains are absent, small or only offline, say so with the paper's numbers; do not invent weaknesses or strengths.
6. **"Our read" box:** CUA Radar score, band, evidence level, and what evidence the paper does and does not report —
   taken from `research/scores.jsonl` and `research/judgments/`. Neutral wording, no hype.
