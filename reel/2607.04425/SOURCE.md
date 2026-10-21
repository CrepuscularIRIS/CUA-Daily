# Source notes — 2607.04425

Read from: arXiv 2607.04425v2
Paper figures shown: none

- Paper: https://arxiv.org/abs/2607.04425v2 (license: CC BY 4.0; no paper figure or screenshot is reused).
- Code: https://github.com/EliSpectre/UI-MOPD (link only; not run, no number taken from it).
- Read in full from the PDF, appendix included. The pipeline diagram is our own drawing from the method text; the charts are redrawn by us from the paper's tables.
- Score, band, evidence level and flags in "Our read": `research/scores.jsonl` and `research/judgments/` (version read as recorded there).
- All poster numbers are copied from Tables 1, 2, 3 and 7 and Sections 1, 4.2, 4.6 and Appendix C of arXiv 2607.04425v2; nothing on the poster is computed by us.
- H-Mean and MinGain are the paper's own reported metrics (Sec. 4.2): H-Mean = 2·S_desktop·S_mobile/(S_desktop+S_mobile); MinGain = min(ΔS_desktop, ΔS_mobile) vs Qwen3-VL-8B-Thinking.
- Relative gains of 12.7% (OSWorld) and 55.8% (MobileWorld) are stated in Sec. 1; the +4.3-point gain on both platforms is stated in Sec. 4.6.
- Figure 4's useful-correction percentages are figure-only bar labels absent from the paper text; poster and blogs describe that analysis qualitatively and cite no number from it.
- Offline metrics (AndroidControl⋆, ScreenSpot-Pro/V2, OSWorld-G) appear only in the controls table with an explicit offline label; the results chart is online-only.
- Numbers marked with a dagger (computed by us): none; every decimal on the poster and in both blogs occurs in the paper text.
- The poster header omits institution names and logos; it names the paper version and says the poster is not made or endorsed by the authors.
