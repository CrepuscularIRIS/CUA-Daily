# Source notes — 2610.20107

Read from: arXiv 2610.20107v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.20107v1 (license: arXiv nonexclusive-distrib 1.0; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Thresholds τ = 0.9 and τ = 0.5 were fixed in early MiniWoB++ experiments before the main evaluation (Section 4.3).
- On the standard Mind2Web protocol (Appendix G, Table 17) Aguvis 7B is ahead of all systems in this paper on the three M2W splits.
- The results chart shows online task success only; offline M2W / GUIAct step success appears in the ablation and controls cards.
- Timing is model time per step, one agent per GPU on MiniWoB++ (Appendix F); WebArena runs share a GPU across three agents.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
