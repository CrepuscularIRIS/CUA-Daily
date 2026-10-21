# Source notes — 2504.00906

Read from: arXiv 2504.00906v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2504.00906v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/simular-ai/Agent-S (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All success rates are online, functional-check evaluations as reported in Tables 1-4 and Appendix A-B; the paper reports no offline step-accuracy metric.
- Ablation values (Figure 5 text): MoG 27.69 → 30.77 (15 steps) and 33.85 → 38.46 (50 steps); Proactive Hierarchical Planning +4.62 / +6.15 over reactive planning; measured on a 65-task OSWorld subset.
- Relative improvements 18.9 / 32.7 (OSWorld), 52.8 (WAA), 16.52 (AndroidWorld) are the paper's own numbers; footnote 1 names the baselines they refer to.
- Figure-only values (grounding-model swap bars in Figure 6; pie shares in Figures 7-8) are not used on the poster or in the blogs.
- OSWorld category breakdown (50 steps, Claude-3.7-Sonnet): OS 50.00, Daily 49.73, Office 25.64, Professional 57.14, Workflow 18.21, overall 34.47 (Table 2).
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
