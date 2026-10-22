# Source notes — 2605.20291

Read from: arXiv 2605.20291v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2605.20291v2 (license: Paper distributed under the arXiv nonexclusive-distrib 1.0 license; poster text and figures are ours.; no paper figure or screenshot is reused).
- Code: https://github.com/fatemehpesaran310/weasel (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Speed-ups and training hours are the paper's Table 1; one-time preprocessing is 7.7 h (Table 13: importance 0.35 h, diversity 0.50 h, greedy < 0.02 h, reasoning synthesis 7.5 h).
- Evaluation judges: GPT-4.1-mini on WebArena-Lite, GPT-4-1106-preview on WebArena, AgentLab default configuration.
- AITW numbers (Table 8) are offline step accuracy on a held-out 500-example subset; every other number on the poster is online success rate.
- Greedy quality: exact optimum in more than 96% of 1,877 NNetNav trajectories (T0 = 3, up to 7,770 candidate subsets), objective ratio 0.9999 ± 0.0005.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
