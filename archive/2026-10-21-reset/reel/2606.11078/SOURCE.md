# Source notes — 2606.11078

Read from: arXiv 2606.11078v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2606.11078v1 (license: Paper license: arXiv nonexclusive-distrib 1.0. Figure reuse not granted; every visual on this poster is our redraw.; no paper figure or screenshot is reused).
- Code: https://github.com/G-JWLee/HiViG (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Benchmarks: WebArenaLitev2 (154 tasks, 15-step horizon), AndroidLab (138 tasks, 9 apps), WindowsAgentArena (145 tasks, 30-step horizon); setup follows ScaleCUA (Liu et al., 2026).
- Critic training: Qwen3-VL-8B-Thinking init, 1 epoch on 52k mixed SFT samples (20k history tracking; 32k error analysis = 16k expert + 16k perturbed), annotated by Qwen3-VL-32B-Thinking over ScaleCUA; 8×H100-80GB, about 4 hours; eval on 8 H100s.
- Paper, App. A: 'All experimental results are from a single run, due to heavy compute costs for long-horizon GUI tasks.'
- History window W = 4 (Qwen3-VL-32B-Thinking) and W = 2 (Gemini-3-Flash); observations normalized to a 1000×1000 grid.
- Further ablations: mixed training 25.3 vs separate critics 23.4 (WALv2); without ground-truth state-transitions 25.3 → 20.8; intent-masking ratio table (0/30/50%); task-overlap analysis (Fig. 5: 9 tasks unique to HisTrack, 7 to VisAnalysis, 6 both, 4 only combined).
- Reported failure cases (App. D.7): misses 'red' vs 'dark red' color variants in Paint; macro-history once recorded a hidden (not deleted) alarm as deleted.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
