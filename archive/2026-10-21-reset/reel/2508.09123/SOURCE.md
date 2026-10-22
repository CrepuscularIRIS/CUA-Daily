# Source notes — 2508.09123

Read from: arXiv 2508.09123v3
Paper figures shown: none

- Paper: https://arxiv.org/abs/2508.09123v3 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/xlang-ai/OpenCUA (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 3 prints Claude 4 Sonnet as 31.2 / 43.9 / 41.5 at 15 / 50 / 100 steps, while Section 4.2 text says 43.9% at 100 steps; the poster follows the table.
- Table 3 prints Claude Sonnet 4.5 as 61,4; the text gives 61.4 and the poster uses 61.4.
- Table 3 OpenCUA-72B 15- and 50-step values (39.0, 44.9) match run 1 in Table 11 (39.03, 44.89); only the 100-step setting lists three runs (average 44.99, printed as 45.0).
- Pass@3 for the 72B model: Section 4.2 text says 53.2, Table 11 prints 53.02; the poster cites neither for 72B.
- Chart values are copied from Table 3; the paper prints plus/minus ranges for OpenCUA rows without stating their meaning, so no error bars are drawn.
- Ablation pairs in Table 6 (CoT mixture; reflective long CoT) come from separate runs with different data sizes.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
