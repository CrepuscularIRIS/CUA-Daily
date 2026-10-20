# Source notes — 2610.02932

Read from: arXiv 2610.02932v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.02932v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/myl7/computer-use (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- The results chart and the ablation chart use the first (GLM 5.3 Flash, blue) column of Table 3 and of the Logs mean block of Table 4; the paper gives every model separately, with the three columns ordered GLM, DeepSeek, Qwen as stated in the table captions. The all-model means (17.34%, 52.68%) are quoted from the text.
- ToolPro is drawn together with ReAct because the paper states its cost equals ReAct in these conditions (Table 3).
- No online task-success metric exists in the paper: all decision-rule results are simulations on measured cost profiles; the live Calendar study (Appendix D, Tables 17-19) tests a fixed program, not the online algorithm.
- Numbers marked with a dagger (computed by us): none; no number was computed by us.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
