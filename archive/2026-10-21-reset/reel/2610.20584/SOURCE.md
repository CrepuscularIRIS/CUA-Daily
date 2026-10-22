# Source notes — 2610.20584

Read from: arXiv 2610.20584v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2610.20584v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/TencentARC/Player-1 (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers are copied from the paper text and tables (main text, Tables 2-4, Appendix D-E). Nothing was rerun.
- Chart: Table 2 (MineDojo-300 success rate; Combat, Harvest, Overall) for GameWAM, Qwen3.5-9B, Player-1-9B-SFT, Player-1-9B, Player-1-35B-A3B-SFT and Player-1-35B-A3B. The paper's 95% bootstrap CIs exist only for the overall column and are not drawn.
- Ablation card: Section 5.1 text (SFT->RL 17.67 to 51.67 and Base->RL 12.67 to 16.67 over 100 RL steps on the Minecraft development tasks; 9B). Fig. 7 (environment scaling at a fixed 25,600 episodes over 2, 4, 8, 16 environments) is described only qualitatively because its bar labels are not in the paper text.
- Controls table: Table 3 (ViZDoom-10 scaled return) and Table 4 (GameWorld success and progress). The paper gives no confidence intervals for these two tables.
- Minecraft demonstrations are part of the SFT data (1,236 of 6,044 trajectories, Fig. 9b); the RL suite contains no Minecraft environment.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
