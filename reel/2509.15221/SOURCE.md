# Source notes — 2509.15221

Read from: arXiv 2509.15221v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2509.15221v2 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/OpenGVLab/ScaleCUA (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 5 columns: AndroidWorld (predefined steps), then 15 and 50 steps for OSWorld, WindowsAgentArena, MacOSArena, WebArena-Lite-v2. The chart uses the 50-step columns; rows marked ⋆ (more than 50 steps) or ♣ (steps unknown) are left out of the chart.
- The paper text in Sec. 5.2.3 labels the WindowsAgentArena 24.2 vs 17.9 comparison as the 15-step setting; in Table 5 those values are in the 50-step column. The poster and blogs follow Table 5.
- Chart baselines chosen by us as the strongest same-table native agents on the chart's 50-step columns (UI-TARS-72B-DPO, UI-TARS-1.5-7B); the workflow row GPT-4o+ScaleCUA-7B is shown with its grounder comparison in the blogs; other rows of Table 5 are listed in the blogs where relevant.
- The ablation chart uses Table 6b only (one table, one model, one metric family: online success at 50 steps); other ablations (Table 6a, 6c, 6d) mix offline and online metrics and appear as text in the blogs.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
