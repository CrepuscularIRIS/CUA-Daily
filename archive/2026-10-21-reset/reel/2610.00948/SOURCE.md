# Source notes — 2610.00948

Read from: arXiv 2610.00948v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.00948v1 (license: arXiv nonexclusive-distrib license; no paper figure or screenshot is reused).
- Code: https://github.com/GaryYang12345/GUI-HARVEST (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Optimizer comparison (Table 2): Self-Harness and Meta-Harness were adapted by the authors to GUI execution and run from the same Agent S3 commit with Claude Sonnet 5 and a ten-round cap (Appendix G.8). LFF was not re-optimized: the authors applied its released OpenCUA patches under their own protocol.
- Cost comparison (Section 4.4, Appendix F) is source-reported and not a shared-budget experiment: GUI-HARVEST GPT-5 uses 15 steps, Agent S3 / GPT-5 uses 100 steps; published totals are reconstructed by the authors from per-task costs. Optimization-process cost is excluded.
- Splits (Section 4.1, Appendix G.7): 361 OSWorld-Verified tasks (eight Google Drive tasks excluded), domain-stratified into Search 80, Validation 80, sealed Test 201. Test tasks are disjoint from optimization tasks but come from the same benchmark; WindowsAgentArena transfer uses only platform adapters and no WAA trajectories.
- Scores are means of K = 3 runs per task (Eq. 1). The paper reports one optimization run per backbone and no seeds across optimization runs; Appendix C gives a standard error of 0.93 points for the K = 3 Full mean.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
