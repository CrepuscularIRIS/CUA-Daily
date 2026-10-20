# Source notes — 2605.29447

Read from: arXiv 2605.29447v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2605.29447v1 (license: arXiv default; no paper figure or screenshot is reused).
- Code: https://github.com/AlibabaResearch/RoTS (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- GUI-RobustEval is an online benchmark (live environment, replayed erroneous prefix); no offline step-accuracy benchmark is reported in the paper.
- All authors are Alibaba Cloud Computing employees; the paper discloses that the Qwen-VL models and RoTS were developed there. Qwen3-VL-Plus is used as a policy, reflector, recovery actor, critic and CoT generator in the pipeline.
- Table 3 marks values with † as the authors’ own re-implementations averaged over 4 runs; other rows are copied from prior reports. Table 8 gives WebJudge F1 as 77.27% while the appendix text says 77.42%; not used here.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
