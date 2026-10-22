# Source notes — 2604.27151

Read from: arXiv 2604.27151v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2604.27151v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/yale-nlp/StepWise (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Success / cost / latency / step statistics: Tables 1-2; periodic-k comparison: Table 3; detector metrics: Table 4 (Sec 6.3).
- 74.6% / 45.8% / 61.4%: Section 1 contributions and Sec 5.2 text; 2.8× / 2.5×: Section 3 (Figure 2 discussion).
- Ablation intermediate bars (49.7, 53.2, 52.1, 47.6; WebArena 44.9, 54.7, 49.6, 48.9) are the printed labels of Figure 3; they occur in the arXiv HTML text the numbers gate uses and were cross-checked against the PDF figure's bar colors.
- Eval tasks are disjoint from the gold-trajectory tasks used for monitor training (Appendix A.1); the judgment record still marks held-out environments as unclear.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
