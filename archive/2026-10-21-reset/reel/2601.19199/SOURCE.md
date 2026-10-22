# Source notes — 2601.19199

Read from: arXiv 2601.19199v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2601.19199v2 (license: arXiv default; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- AndroidWorld Easy split = 61 tasks (Appendix C.1); the online comparison (Table 2) uses all agents with Qwen2.5-VL-32B and the same action budget.
- Online memory preparation (Appendix C.2.2): MAGNET runs three memory-free passes across the 61 tasks and then evaluates; Agent-S runs one round of generic plus official exploration tasks; AppAgent runs one exploration task per app (24 apps).
- Ablation chart is Table 3(a): Amex in-distribution subset, Qwen2.5-VL-32B planner and actor, OFFLINE step success rate. The paper has no online ablation.
- Figure 4 (shift subsets) carries no numbers in the text, so none is charted; only the paper's text statements are used.
- Table 1 labels COAT as Qwen2.5-VL-32B while Appendix C.2.1 says COAT uses Gemini-2.5-Pro; the poster does not use the COAT row.
- No code link is given in the paper text.
- Numbers marked with a dagger (computed by us): ‡ Computed by us, not stated in the paper: with 61 tasks in the Easy split, 42.62% and 40.98% correspond to 26 and 25 tasks, so the headline gap over Agent-S is one task.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
