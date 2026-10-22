# Source notes — 2506.14205

Read from: arXiv 2506.14205v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2506.14205v2 (license: http://arxiv.org/licenses/nonexclusive-distrib/1.0/; no paper figure or screenshot is reused).
- Code: https://github.com/sunblaze-ucb/AgentSynth (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- Figure 4's bare-LLM curve values are printed only inside the figure; the poster charts Table 6 (in tables) instead, and quotes Figure 4 only via the numbers stated in the text (o4-mini 18% → 4%; GPT-4.1 zero beyond level 3; ~4% for o4-mini and Claude-3.7 at levels 4 and 6; humans 70%).
- Main text says the verifier downsamples screenshots to 960×480 while Appendix E says 960×540; neither number is used on the poster.
- Human-annotation cost rows (τ-bench $4–$50, OSWorld $8.8–$110, TheAgentCompany $34–$425) are the AgentSynth authors' estimates at a $2–$25/hour labor rate.
- Blog decimals $0.55 (AgentTrek), $0.28 (Explorer) and $0.27 (InSTA) are the paper's reported comparison costs, not our computation.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
