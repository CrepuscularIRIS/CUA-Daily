# Source notes — 2606.27330

Read from: arXiv 2606.27330v1
Paper figures shown: none

- Paper: https://arxiv.org/abs/2606.27330v1 (license: arXiv default; no paper figure or screenshot is reused).
- No code repository is listed on the board.
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Headline numbers: Table 1 (WebVoyager, online, trajectory-level success rate; Overall averages the ID site and 7 unseen sites).
- TDHAF numbers: Table 2 and Sec. 3.3 (offline step metrics on Multimodal-Mind2Web-derived data; 616 train / 684 test samples).
- Exploration: GPT-4o, max 15 steps; the task-setting prompt asks for 50 tasks per site. Training: SFT and GRPO on Qwen2.5-VL-3B/7B-Instruct, 4 A800 GPUs.
- WebVoyager sites excluded for access limits: Cambridge Dictionary, Google Search, Hugging Face (Appendix C).
- 0.1k = about 100 tasks from Allrecipes (ID); 2k = about 2,000 tasks from additional websites, distinct from the 7 held-out test sites.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
