# Source notes — 2606.19930

Read from: arXiv 2606.19930v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2606.19930v2 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/kwai/MobileForge (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers from 2606.19930v2 main text and appendices (Tables 1–12); no figure-only values used.
- AndroidWorld scaling (Table 1): Qwen3-VL-8B Pass@3 55.2 / 61.2 / 62.9 / 67.2 at 0 / 200 / 400 / 900 tasks; GUI-Owl-1.5-8B 69.0 / 74.1 / 77.6 / 77.6.
- MobileWorld (Table 2): external rows follow the GUI-only reporting protocol; ForgeQwen3-8B is 10.3% (12/117), rel. gain +33.8% over Qwen3-VL-8B; ForgeOwl-8B rel. gain +9.0%.
- Hint ablation downstream (Table 7): without/with hints — Qwen3-VL-8B AW Pass@1/3 49/68 vs 55/71, MW 12/117 vs 15/117; GUI-Owl-1.5-8B 71/83 vs 75/86, MW 43/117 vs 46/117.
- 900-task 8B run (Table 14): 8×80GB GPUs, ~80 h, 4 epochs, 5 responses per step prompt, KL coefficient 1e-2, lr 1e-6.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
