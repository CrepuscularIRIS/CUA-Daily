# Source notes — 2508.05731

Read from: arXiv 2508.05731v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2508.05731v2 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/InfiXAI/InfiGUI-G1 (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All results are offline grounding accuracy (top-1, point inside the ground-truth box); the paper reports no online or interactive evaluation.
- The 'w/ Expl. Success' rows in the paper's tables are exploration success rate (any of the N candidates correct) — a different metric from top-1 accuracy; only top-1 rows are charted here.
- Internal baseline Naive RLVR uses the same 44k samples and optimized hyperparameters; training data from public GUI datasets (Widget Caption, OmniAct, GUICourse, etc.), filtered by dropping samples where all 8 of 8 sampled responses are correct.
- Numbers from Tables 1–8 of v2; abstract states relative improvements of up to 9.0% over the naive RLVR baseline.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
