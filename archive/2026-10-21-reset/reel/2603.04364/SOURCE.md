# Source notes — 2603.04364

Read from: arXiv 2603.04364v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2603.04364v2 (license: Paper licence: CC BY-NC-SA 4.0; poster and blogs are our own redraw and text, no figure of the paper is reproduced.; no paper figure or screenshot is reused).
- Code: https://github.com/huajianduzhuo-code/DMAST_official (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All values are copied from Table 1, Table 2, Table 4, Table 6 and Table 7 of arXiv 2603.04364v2; no value on the poster or in the blogs is computed by us.
- Chart: ASR (attacker success rate) and TSR (task success rate) share one percent axis; both are interactive-episode metrics, there is no offline metric in the paper. Error bars are the standard errors printed in Table 2.
- Prompt Defense, SPAG, ART and Online SFT are the authors' own reproductions as baselines on the Gemma-3-12B-IT student; Online SFT is in the blogs but not in the chart.
- The evaluation attacker is the fixed Gemma-3-27B-IT model, which the paper also uses as the Stage 1-2 teacher (Appendix B.1).
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
