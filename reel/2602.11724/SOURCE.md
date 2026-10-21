# Source notes — 2602.11724

Read from: arXiv 2602.11724v3
Paper figures shown: none

- Paper: https://arxiv.org/abs/2602.11724v3 (license: Paper text © 2026 authors, CC BY 4.0 (ACM PACMSE); arXiv non-exclusive-distrib 1.0. Poster diagram and charts are our own redraws, not the paper's figures.; no paper figure or screenshot is reused).
- Code: https://github.com/code-philia/WebTestPilot (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers from arXiv 2602.11724v3 (Proc. ACM Softw. Eng. 3, FSE, Article FSE087): Tables 3-5, Sections 5.2-5.6, and the Figure 1 study.
- TC = every scripted assertion satisfied by the trace; CT = fraction of the script correct before the first failure (Sec. 5.2.2).
- Evaluation is online: four live web apps (BookStack, Indico, InvoiceNinja, PrestaShop) in Docker Compose, fresh instance + restored DB per test, sequential runs; no offline benchmarks are charted.
- Termination is budget-matched: a test stops when executed steps reach the scripted step count. Retry budget n = 1 (Sec. 4.3.3).
- The +70 precision / +27 recall and +54.7% TC / +28.6% CT gains are the paper's own reported deltas (abstract, Secs. 5.2.4, 5.3.4).
- No component ablation, no seeds/variance, and no held-out apps are reported; RQ3/RQ4 vary input transformations and the base model (GPT-4.1, Qwen2.5-VL 72B/32B/7B/3B) instead.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
