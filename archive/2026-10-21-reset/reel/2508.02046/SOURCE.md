# Source notes — 2508.02046

Read from: arXiv 2508.02046v4
Paper figures shown: none

- Paper: https://arxiv.org/abs/2508.02046v4 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://iron-boyy.github.io/navimaster-page/ (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- ObjectNav SR: Table 3 prints 33.20; the running text says 33.10. Poster and blogs use the table value.
- Dense-vs-sparse control: dense threshold theta_d = 200 px vs sparse 20 px; sparse row is Navimaster-hardreward in Table 7 (AC-High SR 54.07).
- Table 7 lists identical values for Navimaster-3B (w/o GUI) and (w/o Embodied); the 3B control compares the mix row (SR 45.26) against that duplicated row (SR 28.75).
- GUI SR is the per-step task success rate under the OS-Atlas protocol (grounding correct within 14% of image size); GR is grounding accuracy - both offline. In-domain GUI testing samples 4800 cases from GUI-Odyssey.
- Chart series values are SR columns of Table 1; ablation values are Table 3; affordance and reward-component numbers are Tables 2 and 8.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
