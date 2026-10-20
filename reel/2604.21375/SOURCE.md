# Source notes — 2604.21375

Read from: arXiv 2604.21375v3
Paper figures shown: none

- Paper: https://arxiv.org/abs/2604.21375v3 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/UCSC-VLAA/VLAA-GUI (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 1 (OSWorld-Verified, 15/50/100 steps), Table 2 (ablation), Table 3 (WindowsAgentArena), Tables 6, 10 and 11 and Figures 3 and 4 were read; the chart uses Table 1 rows only (HIPPO w/ Opus 4.5, OS-Symphony w/ GPT-5, and three VLAA-GUI backbones).
- Baseline rows are taken by the paper from the OSWorld leaderboard (except OS-Symphony at 100 steps); backbones, tools and step budgets differ between rows, so rows are not same-model comparisons.
- The paper states that the Sonnet 4.6 base scaffold (69.19) and the full framework (71.67) share backbone, grounding, action interface and budget; this is the paper's configuration-controlled comparison.
- Table 1 also lists Kimi K2.6 (73.07) and HIPPO w/ Opus 4.5 (74.49) above the 72.4 human reference at 100 steps, while the text calls VLAA-GUI the first GUI framework to exceed it; the poster states only the paper's own numbers.
- The 60-task subset results (Figure 4, Table 6) are point estimates on a fixed, non-random subset with no confidence intervals, as the paper states; Table 6 costs are lower bounds.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
