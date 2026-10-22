# Source notes — 2610.14157

Read from: arXiv 2610.14157v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.14157v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/OpenMobile2/OpenMobile2-Code (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Results chart and ablation come from Table 2; values marked ∗ there were reproduced by the OpenMobile-2 authors, not by the original benchmark papers.
- Overlap audit (App. A.4): 1.11% / 0.39% / 0.46% / 2.25% of SFT goals exceed 0.7 cosine with AndroidWorld / MobileWorld / MobileGym / MobileGym++ Bench; 6.1% of the 2,475 RL goals exceed 0.7 with MobileGym++ Bench; none exceeds 0.9.
- Coverage ablation (Sec 5.3): 15→53 train apps at a fixed 2K-trajectory budget; held-out AndroidWorld Pass@1 60.7→67.5, InD 73.7→71.4.
- Tool-use stats (Sec 5.3, Table 4): before hybrid SFT, tool calls in 20–102 of 215 tasks (Qwen gains 2.8–4.2 pts); after, 113 / 128 tasks, 110 / 115 distinct tools, gains 5.6 / 10.3 pts, trajectories 4.8 / 5.8 steps shorter.
- Environment stats (Sec 3.2): median 37 routes, 166 interactive actions, 86 page transitions per new app; 1.48× actions and 1.91× transitions vs the 12 prior MobileGym business apps.
- SPA-Bench numbers are the L3 split on physical Android devices; AndroidWorld numbers are Pass@1.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
