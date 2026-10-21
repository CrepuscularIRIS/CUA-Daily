# Source notes — 2503.03743

Read from: arXiv 2503.03743v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2503.03743v1 (license: Paper under CC BY-NC-ND 4.0 (per CUA Radar record); poster diagrams are our redraws.; no paper figure or screenshot is reused).
- Code: https://github.com/Yuqi-Zhou/CHOP (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 2 reports five metrics (SR, CR, ME, AE, AAC) per language × difficulty; the poster charts SR on CHOP-En and lists CHOP-ZH in the controls card.
- CHOP-ZH has 200 instructions; 30 (3 per app) were run for GPT-4o cost; ablations use CHOP-ZH.
- Subtask-quality scores (Figure 3: BLEU / ROUGE-L / LLM judge) are figure-only and are not reproduced here.
- Error analysis (Table 4) and per-app CR (Figure 4) are reported in the paper; Figure 4/5 bar labels are figure-only.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
