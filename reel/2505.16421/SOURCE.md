# Source notes — 2505.16421

Read from: arXiv 2505.16421v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2505.16421v2 (license: Paper license: http://arxiv.org/licenses/nonexclusive-distrib/1.0/ (no figure reuse).; no paper figure or screenshot is reused).
- Code: https://github.com/weizhepei/WebAgent-R1 (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Read in full from the PDF (v2, 8 Oct 2025), appendices A–E included; the pipeline diagram is our own drawing from the method text and the charts are redrawn from Table 2 and the §3.4 text.
- Baseline numbers follow the paper's rule: the higher of the authors' reproduced result and the literature value (Qi et al., 2025).
- For the Llama-3.1-8B comparison the paper initializes RL from WebRL's public checkpoint and uses only the original 647 training tasks, without extra data.
- Figure 3 (training dynamics) and Figure 5 (test-time scaling) carry values only inside the figures; the poster quotes neither, only the qualitative claims stated in the text.
- Interaction counts (6 → 17 for Qwen2.5-3B with the thinking format) come from Table 3.
- WebVoyager OOD: 25 tasks sampled per domain × 5 domains, evaluated with Qwen2.5-3B against prompting and SFT baselines without further training.
- Score, band, evidence level and flags in "Our read" come from research/scores.jsonl and research/judgments/ (version read as recorded there).
- No paper figure or screenshot is reused; license: arXiv nonexclusive-distrib 1.0.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
