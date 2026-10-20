# Source notes — 2509.25140

Read from: arXiv 2509.25140v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2509.25140v2 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/google-research/reasoning-bank (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- WebArena excludes the Map domain (684 tasks), following the paper; Mind2Web has 1341 test instances (252 cross-task, 177 cross-website, 912 cross-domain).
- Table 1 rows are pass@1; the +MaTTS row uses parallel scaling with k = 5 trajectories per task, the other rows use one.
- Chart values are the Overall SR column of Table 1 (means as printed; the paper reports no std, CI or seed count).
- Ablation values are quoted in Section 5 and Appendix C.1 text; the per-method success-only and with-failure bars are Figure 7 of the paper.
- Controls table: Mind2Web columns are cross-task / cross-website / cross-domain task-level SR (offline, Gemini-2.5-flash, Table 3); SWE-Bench-Verified is Table 2 (resolve rate, flash / pro); Gemma-3-12B is Table 6; tokens are Table 5; judge accuracy is Section 5.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
