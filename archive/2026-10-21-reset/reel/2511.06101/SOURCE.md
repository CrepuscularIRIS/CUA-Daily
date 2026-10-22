# Source notes — 2511.06101

Read from: arXiv 2511.06101v3
Paper figures shown: none

- Paper: https://arxiv.org/abs/2511.06101v3 (license: arXiv non-exclusive distribution licence; no paper figure or screenshot is reused).
- Code: https://github.com/aiming-lab/SynthAgent (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- WebArena chart values: Table 1 (Qwen2.5-VL-7B and UI-TARS-1.5-7B rows); headline 24.34 is Table 3 (Qwen3-VL-8B); 226 of 812 tasks, one per template (Appendix A.1). The paper itself calls WebArena offline and Online-Mind2Web online (Limitations).
- The ablation chart (Table 10) does not name its backbone; its base and full rows (8.80, 20.80) equal the Qwen2.5-VL-7B rows of Table 1, so it is labelled that way. Its last row is the Table 1 base value.
- Online-Mind2Web values: Table 2 (rows named only 'Qwen' and 'SynthAgent') and Table 4 (Qwen3). The agent trained for them is not named in Table 2.
- The paper's Section 3.2 gives 6.3% over-budget samples for SynthAgent while Table 6 lists 0.0% exceeded; the poster and blogs use Table 6 (completion 96.5%).
- Computed numbers: none; every figure is a table or text value of the paper.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
