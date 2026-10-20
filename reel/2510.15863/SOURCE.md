# Source notes — 2510.15863

Read from: arXiv 2510.15863v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2510.15863v2 (license: CC BY-NC-SA 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/simonucl/PolySkill (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- WebArena numbers: Table 8 (average column, 812 tasks) with Baseline, SkillWeaver, ASI and PolySkill rows per backbone; no standard deviations are given for WebArena. The Table 8 caption in v2 says experiments marked with a dash are pending completion.
- Mind2Web numbers: Table 6 and Table 2 (GPT-4.1, success rate judged by a GPT-4.1 judge; mean ± std in Table 6); skill counts from Table 2; token counts from Table 10; skill reusability 20.4% from Section 4.2 (WebArena shopping, by task 180).
- Reuse figures in Section 3.2 (under 9% for ASI, under 3% for SkillWeaver on unseen sites) come from Figure 2 text; the introduction states a different threshold (below 18%).
- Paper-internal inconsistencies noticed: WebArena is 812 tasks in the main text and 811 in Appendix E.3; Table 6 delta columns for cross-domain static rows do not match the printed absolute values, so only absolute values are used here; the abstract's 13.9% on unseen websites was not located in a table row.
- Table 3 and Table 9 (task-free exploration) are described by the paper as held-out transfer, but the self-guided rows list the evaluated sites (AMZ, Target, WA; GitHub, GitLab) among the exploration sites, so they are not used as held-out evidence on the poster.
- Mind2Web is scored by a GPT-4.1 judge following the Online-Mind2Web protocol (85% agreement with humans, cited from prior work); the paper does not state whether runs are on live sites.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
