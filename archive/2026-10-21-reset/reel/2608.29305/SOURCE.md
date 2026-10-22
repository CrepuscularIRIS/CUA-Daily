# Source notes — 2608.29305

Read from: arXiv 2608.29305v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2608.29305v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/THUNLP-MT/TTED (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- WebArena results use 561 of 812 tasks (Reddit removed, Table 9), graded with GPT-5-mini fuzzy matching instead of GPT-4o-Turbo (Appendix D.1).
- Table 1 reports TTRL on WebArena only; its WorkArena cell is '-'.
- Table 2 agreement is the paper's 'normalized AD' on 82 WebArena tasks; the separate 0.85 Cohen's kappa is between two annotators.
- Qwen3-14B p-values (0.093, 0.153, 0.061) are listed in the paper in the order base, RL w/ GT, TTT.
- GPT-4o (23.5) and GPT-5.5 (67.3, full WebArena-Verified, different verifiers) appear in Table 5 as context only and are not charted.
- GPU hours (Table 10) are for REINFORCE advantage estimation with 3200 sub-environments on 8 A100-80GB; TTRL (19.20) and TTED with GRPO (21.33) are listed separately.
- No number on the poster is computed by us.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
