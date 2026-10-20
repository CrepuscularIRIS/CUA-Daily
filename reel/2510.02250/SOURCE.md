# Source notes — 2510.02250

Read from: arXiv 2510.02250v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2510.02250v2 (license: arXiv default; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Costs ($0.72, $0.11, $0.03 per task) are Table 8 (Appendix B), GPT-5 gpt-5-2025-08-07.
- Chart bars are Table 1; blanks mean the paper does not report that method/model pair. All values are 100-step success on 361 OSWorld tasks.
- Agent S3 62.6 is stated as averaged over 10 runs; the paper does not state runs or seeds for BJudge numbers.
- Table 1 caption says the best ensemble is chosen from Table 5; Table 5 lists GPT-5 + Opus 4.5 at 71.6 (N=4 runs split evenly), while the headline 72.6 uses 5 rollouts each from GPT-5 and Opus 4.5 (N=10).
- The WebJudge baseline is the authors' adaptation (independent 1-5 ranking per trajectory, random tie-break).
- Coding agent is disabled on AndroidWorld in the paper's setup.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
