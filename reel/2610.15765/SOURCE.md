# Source notes — 2610.15765

Read from: arXiv 2610.15765v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.15765v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/co-evolve-lab/ANIS (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 2 (DeepSeek V4 Flash) is charted; Haiku 4.5 results are in Appendix C Table 4 (native SDK 61.4, ANIS atomic 64.9, with goal-level 67.4).
- Success rates are pass@3: a task counts if any of three independent attempts passes its artifact verifier (Section 4.1).
- The cross-version study (Section 4.2, Figure 2: newest release above oldest in all 12 model-application series, e.g. QGIS 41% to 69% for DeepSeek and 33% to 65% for Haiku) is described in the blogs but not charted; the Figure 2 values are figure-only.
- Held-out goal-level evaluation (Appendix E.2): 258 training and 110 test tasks, 7 goal-level commands synthesized from training trajectories.
- Interface generation time 17.1 to 36.4 hours per application (Appendix F); generation used Claude Code with Claude Opus 4.8 for ANIS and CLI-Anything.
- The poster covers programmatic (SDK / command) interfaces on live desktop applications; no screenshots are used.
- No number on the poster is computed by us.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
