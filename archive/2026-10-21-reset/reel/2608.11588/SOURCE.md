# Source notes — 2608.11588

Read from: arXiv 2608.11588v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2608.11588v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Setting 1 Base Policy (27.10) and Policy-Only TTA (37.50) are reported from Gu et al. 2026 and were not reproduced by the authors (Appendix B.3); the other three rows are the authors' five-run means.
- AndroidWorld Plus (Table 2) reports no standard deviation or run count; the five-run statement (Appendix B.3) is for Setting 1.
- The paper states the nominal 50-update schedule is not an identical gradient or compute budget across methods, and that Context-Only TTA vs CoAdapt-GUI is not a crossed isolation of the LoRA adapter.
- Frozen synthesizer and reflector on AndroidWorld Plus: Claude Opus 4.7 (Table 9).
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
