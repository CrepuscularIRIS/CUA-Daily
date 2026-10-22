# Source notes — 2501.12326

Read from: arXiv 2501.12326v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2501.12326v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/bytedance/UI-TARS (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers are copied from the paper text and tables (Tables 3-9, Sec. 4-5); no figure-only value is used.
- Chart (Table 9): rows without a step label (Aguvis-72B 10.3, Aria-UI + GPT-4o 15.2) are placed in the 15-step group because the Table 9 caption says OSWorld was run with a maximum of 15 steps; the 50-step rows are labelled in the table.
- UI-TARS-72B-DPO was not evaluated on AndroidWorld in Table 9 ('-'); the AndroidWorld bar is the 72B-SFT model (46.6).
- Offline benchmarks (Tables 5-8) and the system-1 / system-2 comparison (Figure 8, values not in the text) are not charted; Figure 8 numbers are not used.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
