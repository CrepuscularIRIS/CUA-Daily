# Source notes — 2602.22190

Read from: arXiv 2602.22190v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2602.22190v2 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/GUI-Libra/GUI-Libra (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Online results: Table 5 (AndroidWorld, native models, 20 steps), Table 6 (WebArena-Lite-v2, 15 steps, mean of four runs), Table 7 (Online-Mind2Web, 30 steps, columns o4-mini / WebJudge-7B / average overall).
- The Online-Mind2Web chart group uses the paper's printed average-overall column; GPT-4o + UGround-v1-7B is an agent framework (two modules); its WebArena-Lite-v2 value (23.2) is marked as reported by Liu et al. (2025c) in Table 6.
- Ablation card: Table 9 (Qwen2.5-VL-3B base), AndroidWorld column only (online); offline columns are in the paper.
- Controls: Table 7 (judges), Table 10 (SNGS, 4B), Table 15 (uniform scaling lambda_g = 0.75 / 0.9, 3B), Section 6.4 / Figure 10 (Pearson 0.89 / Spearman 0.83 with KL > 0; 0.63 / 0.53 without), Table 3 (AndroidControl-v2 high-level Pass@1, offline).
- Training cost (Appendix B): SFT about 4 h (Qwen3-VL-4B) and 5.5 h (8B) on 8 B200 GPUs; RL about 16 h (4B) and 20 h (8B) on 8 B200 GPUs.
- No number on the poster is computed by CUA Radar; +15.6% and +9.5 are stated in the paper.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
