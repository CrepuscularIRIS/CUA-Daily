# Source notes — 2602.08995

Read from: arXiv 2602.08995v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2602.08995v2 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/OSU-NLP-Group/Misaligned-Action-Detection (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Table 3 (offline, MisActBench, 2,264 steps): DeAction F1 70.7 / 80.4 / 79.4 / 82.8 for Qwen3-VL-32B / Claude Sonnet 4.5 / GPT-5.1 Instant / GPT-5.1 Thinking; best prior baseline F1 per backbone 61.6 (InferAct), 66.6, 65.1, 66.9 (Task Shield).
- Table 5 (online): RedTeamCUA uses 50 high-risk end-to-end tasks, 50-step cap; OSWorld uses a 15-step cap and no-defense rows are taken from the OSWorld leaderboard, not rerun (Appendix E.1). Baselines compared only on OpenCUA-72B.
- Table 4 and F.6 (offline ablation) use a 566-step subset (242 misaligned, 324 aligned), GPT-5.1 Thinking (Appendix D.2).
- Appendix F.4 and Table F.7: the cost-efficient configuration (GPT-5 mini for fast check and summarizer) gives ASR 8.0 / 8.0 / 8.0 for Claude Sonnet 4.5 / OpenAI CUA / OpenCUA-72B.
- Poster contains no computed numbers; the blogs mark any computed figure with a dagger.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
