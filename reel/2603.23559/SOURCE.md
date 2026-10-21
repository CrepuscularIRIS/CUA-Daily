# Source notes — 2603.23559

Read from: arXiv 2603.23559v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2603.23559v2 (license: Paper under CC BY 4.0. Poster text, diagram and charts are our redraws, not the paper's figures.; no paper figure or screenshot is reused).
- Code: https://github.com/ASTRAL-Group/ReCAP-Agent (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All numbers from 2603.23559v2 text and Tables 1–5, 7–9; no figure-only values. Code URL as announced in paper v2.
- Real-world eval: Halligan protocol, released framework, 100 samples/type, no step limit.
- SFT: ZeRO-2, bf16, lr 1e-5, 1 epoch, ~230k samples (150k sol + 10k corr + 50k Aguvis + 23k AgentNet).
- Table 3 general-GUI results follow offline protocols; kept off the online chart.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
