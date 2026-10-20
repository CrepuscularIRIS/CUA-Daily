# Source notes — 2505.23762

Read from: arXiv 2505.23762v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2505.23762v1 (license: arXiv nonexclusive-distrib 1.0; no paper figure or screenshot is reused).
- Code: https://github.com/OpenGVLab/ZeroGUI (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Tables 1-2: online SR, mean±std over 4 runs, screenshot-only, 15-step cap (OSWorld 369 tasks incl. 30 infeasible; AndroidLab 138 tasks); * rows are numbers as reported in prior papers.
- Table 3: ablations on the OSWorld Daily domain (Chrome, Thunderbird, VLC); judge precision/recall measured on manually labeled UI-TARS-7B-DPO trajectories (Table 3b).
- Table 4: training-method ablation (offline RFT / online RFT / online RL, k3- vs k2-KL); Fig. 6 sweeps the KL coefficient.
- Task generation: GPT-4o, over 4,000 Ubuntu + 225 Android tasks generated, 725 + 175 sampled for training (about twice the test-set size). Reward: Qwen2.5-VL-32B, 4 queries at temperature 1.0, unanimous voting.
- Test-time training runs on the test set without ground-truth labels (Sec. 3, Fig. 2); the judgment record marks held-out environment as not reported.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
