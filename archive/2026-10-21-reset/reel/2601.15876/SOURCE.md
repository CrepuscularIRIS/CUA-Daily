# Source notes — 2601.15876

Read from: arXiv 2601.15876v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2601.15876v2 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/meituan/EvoCUA (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 1 lists Step-GUI-8B under closed-weights; the poster and blogs keep the paper's grouping only where it matters and name the model and step budget for every number.
- Table 2 values marked * are sourced by the paper from other public reports; we keep the marker.
- Table 3 and Table 4 report gains only; the base score and the benchmark are not stated in the tables.
- The paper's text says +15.1% over the base model for EvoCUA-32B, while Table 1 lists 41.0 for Qwen3-VL-32B-Thinking (100 steps); the paper does not reconcile the two.
- Numbers marked with a dagger (computed by us): 15.7 = 56.7 - 41.0 (Table 1) and also the sum of the five Table 3 gains (4.84 + 2.62 + 3.13 + 3.21 + 1.90); computed by us, shown only in the blogs. The paper's own text states +15.1.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
