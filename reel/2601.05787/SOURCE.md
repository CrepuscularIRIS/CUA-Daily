# Source notes — 2601.05787

Read from: arXiv 2601.05787v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2601.05787v2 (license: arXiv non-exclusive distribution license; no paper figure or screenshot is reused).
- Code: https://github.com/LEON-gittech/Verl_GUI.git (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Chart and Table 1 numbers: Table 1 (overall = mean +/- std over 3 runs; Dexpert_only/Dtrain/Dheld_out columns without std). The poster chart draws error bars on the Overall group only, as the paper gives no std for the splits.
- Table 7 (per-domain, 'best single-run') lists UITARS1.5-7B 23.66, GRPO 24.50, ARPO 22.97, differing from the Table 1 means (22.87, 23.60, 23.86). We use Table 1 for the headline and Tables 7/10 only for the extensibility chips, labelled single run.
- Online-Mind2Web 28.52 / 23.28 / 24.81 are from Table 11 (WebJudge with o4-mini as judge); MMBench-GUI L1 easy from Table 8 (offline); group size and update rule from Table 12.
- Token tail mass and JS values quoted from the paper text for Figure 3 (19-task subset Dupd); no figure-only values are used.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
