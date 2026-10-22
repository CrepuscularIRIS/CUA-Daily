# Source notes — 2603.10505

Read from: arXiv 2603.10505v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2603.10505v1 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/kyle8581/VeriEnv (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Chart and headline values: Table 4 (WebArena-Lite) and Table 5 (Mind2Web-Online); the Δ column is the paper's own.
- The paper's text states +9.09 for LLaMA-3.2-3B on WebArena (Sec. 4.1 and Introduction), while Table 4 lists +9.70 (12.73 vs 3.03). The poster shows only table totals and omits both deltas for LLaMA.
- Website counts as printed in the paper: 149 sites in Table 1; error analysis covers 136 candidate sites, 39 failed, and Figure 9 gives 97 validated sites used for training.
- Figure 4 (site-specific training vs PAE), Figure 5 (environment scaling) and Figure 7 carry no numbers in the text; they are described qualitatively only.
- Baselines marked * in the paper (GPT-4o-mini, GPT-4o, Claude-3.5-Sonnet, Browser-Use) use numbers reported by other papers, not same-setup runs.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
