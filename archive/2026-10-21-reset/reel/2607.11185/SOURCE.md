# Source notes — 2607.11185

Read from: arXiv 2607.11185v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2607.11185v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/THUDM/SCALE-CUA (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 2 (OSWorld): ScaleCUA-GLM-4.6V-Flash 66.5±0.5, ScaleCUA-Qwen3-VL-8B 67.7±1.2, ScaleCUA-Qwen3.5-9B 68.7±0.7 (std over 4 passes); Kimi K2.5 63.3; Claude Opus 4.6 72.7; Qwen3.5-9B 41.8 (technical-report figure, marked § in the paper).
- Table 3 (ScienceBoard): ScaleCUA 49.4±2.8, 51.9±1.5, 54.0±0.5; Claude Opus 4.6 52.7. Kimi K2.5 has no ScienceBoard entry, so its bar appears on OSWorld only.
- Table 4 ablation base score is 43.9 for 'w/o VeriGen (Base)', while Table 2 lists Qwen3.5-9B at 41.8 (technical report); the paper does not reconcile the two. Both are shown as printed.
- Table 6 audit: 160 trajectories (10 per domain), agreement 82.5% overall, 78.0% OSWorld, 90.0% ScienceBoard; human-valid rate 73.1% overall; 11 false positives and 17 false negatives.
- Table 8 overlap audit: OSWorld 1049 training tasks, 0.19% near-duplicates, 2.10% judge reuse (generic evaluator templates); ScienceBoard 825 tasks, 0.36% near-duplicates, 0.00% judge reuse.
- Sampler comparison (uniform, DAPO, curriculum learning) is Figure 6(a) curves only; the paper gives no table of numbers for it.
- Speedup 2.83× (750 s to 265 s per step, actor 485 s to 154 s, ref 241 s to 88 s) is a training-time measurement on Qwen3.5-9B, batch 32, rollout-n 8; not an evaluation score.
- Limitations stated by the paper: 50-turn cap, Ubuntu desktops only, 8B to 9B models only.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
