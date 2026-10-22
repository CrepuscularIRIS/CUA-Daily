# Source notes — 2610.19834

Read from: arXiv 2610.19834v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.19834v1 (license: Paper license: CC BY 4.0.; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 1 (TimeWarp): success rate, mean of 3 seeds, standard error as subscript; v6 seen in training, v1–v5 held out.
- Online-Mind2Web (Fig. 4) and the β sweep (Fig. 5) are figure-only; the text states all OM2W methods sit below 8% and WebKD roughly doubles the strongest baseline for the 9B student, and that β = 0.03 is best.
- Ablation Tables 2 and 3 use Qwen-3.5 4B with the KL anchor at β = 0.03.
- No public code at v1: the paper says the source is in supplementary material and will be released upon acceptance; project page https://web-teach-kd.github.io/.
- Model sizes are as named by the paper: Qwen-3.5 4B / 9B and Gemma 4 E4B; the teacher is GPT-5.5.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
