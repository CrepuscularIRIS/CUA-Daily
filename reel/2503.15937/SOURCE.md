# Source notes — 2503.15937

Read from: arXiv 2503.15937v5
Paper figures shown: none

- Paper: https://arxiv.org/abs/2503.15937v5 (license: Paper licensed CC BY 4.0; poster and blogs are our own redrawn summary, not author-endorsed.; no paper figure or screenshot is reused).
- Code: https://github.com/V-Droid-Agent/V-Droid (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All success rates are online task success on live Android emulators; the paper reports no offline grounding/step-accuracy benchmark.
- Baseline SRs are adopted from the respective baseline papers (§6.1.3); V-Droid latency measured on 20 randomly sampled tasks.
- AndroidWorld is the in-domain test set; AndroidLab and MobileAgentBench are out-of-domain, with their apps excluded from training-data collection.
- Table 3 alternatives are trained on 1.1K task steps; the full system uses 110K pairs over four annotation iterations.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
