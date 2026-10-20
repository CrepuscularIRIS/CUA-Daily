# Source notes — 2610.22234

Read from: arXiv 2610.22234v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.22234v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/OS-Copilot/OS-Helix (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers are copied from the paper text (main + appendix): Tables 1-5, 12, 13, 14, 16 and Sections 4-5, Appendix D.
- Chart: OSWorld average, Office and Work. columns from Table 1; WindowsAgentArena (WAA) average from Table 2 / Table 12. Both are online success rates; the OS-Symphony row is a cited result (not marked as reproduced); Qwen3.5-27B rows are reproduced by the authors.
- Ablation chart mixes Table 4 (full-data runs) and Table 5(b) (10K-sample SFT runs), labelled as such; all are OSWorld, Qwen3.5-27B.
- The offline grounding row (OSWorld-G, ScreenSpot-V2) is from Table 13 and is for OS-Helix-32B (Qwen3-VL-32B-Instruct backbone, SFT only), not the 27B model.
- The paper states relative improvements of 35.0% and 33.7% (27B, 35B-A3B) over the matched Hybrid baselines and 42.9% for the RL model; the poster does not recompute them.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
