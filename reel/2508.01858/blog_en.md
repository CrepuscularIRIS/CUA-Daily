# Web-CogReasoner: a web agent that memorizes, understands, then explores

*A CUA Radar reading of arXiv 2508.01858v3 (Guo et al., ICLR 2026). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2508.01858v3 · Code: https://github.com/Gnonymous/Web-CogReasoner*

## The problem: knowledge before reasoning

General-purpose LVMs give web agents strong priors but, in the paper’s words, “remain limited in specialized tasks, creating performance bottlenecks”, and “prior knowledge-enhancement methods often lack systematic or theoretical grounding”. The proposal: borrow Bloom’s taxonomy from pedagogy and split an agent’s competence into knowledge content learning (Factual and Conceptual knowledge: the “what”) and cognitive processes (Procedural knowledge: the “how”), then train a web agent through that order — Memorizing, Understanding, Exploring.

## What Web-CogReasoner is

**The agent.** A multimodal web agent on desktop websites. At each step it observes a screenshot plus the accessibility tree (AX tree), with elements referenced by id, and emits one action from a fixed space: `click [id]`, `type [id] [content]`, `scroll [id or WINDOW] [up/down]`, `dbclick [id]`, `go_back`, `go_forward`, `stop [content]`, `Restart`, `Wait`. Interaction is modeled as a POMDP P = (S, A, O, K, T, R), with K an internal-knowledge slot.

**The mechanism.** Three things ship with the paper. (1) *Web-CogKnowledge*, the taxonomy: Factual knowledge (element attributes, page-change and next-page prediction), Conceptual knowledge (element, webpage and cross-modal understanding), Procedural knowledge (intent prediction, popup close, single-step and noisy multi-step tasks). (2) *Web-CogDataset*, built by Playwright deep traversal of 14 real websites (layers 1 to 6 of clicking), annotated by Qwen2.5-VL 72B from before/after hover and click screenshots, plus open-source augmentation (MultiUI, Mind2Web, OpenWebVoyager). It totals 81K factual, 62K conceptual and 27K procedural samples over 12 task families; popup-close data is synthesized by overlaying 51 popup components and generating AX trees and closing strategies with Qwen-VL-2.5-32B. (3) *Web-CogBench*, an 876-item evaluation curated from a representative subset of the training dataset, scored by ROUGE-L, accuracy, or a GPT-4o LVM judge on a 1-5 Likert scale normalized to 0-100.

**Training signal.** Supervised fine-tuning (imitation learning) of Qwen2.5-VL-7B in curriculum order S1 Factual → S2 Conceptual → S3 Procedural, on 8 A800 80GB GPUs, max sequence length 8K, batch size 1 with 16 gradient-accumulation steps. At inference the agent runs a Knowledge-driven Chain-of-Thought (KCoT): task recap → webpage layout description → key element analysis → summary → trajectory history review → task decomposition → step-by-step reasoning → final action. On the CUA Radar board this is pattern C21 (synthesize reasoning annotations, then SFT a screenshot policy) under trajectory-level policy training.

## Results, as reported

All online numbers are live-web success rates from single runs; the paper reports no seeds or variance, and UI-TARs-7B-SFT is “omitted due to missing online inference scripts”.

| Method (online) | WebVoyager (643) | Mind2Web cross-task | Mind2Web cross-web |
|----|----|----|----|
| Claude Sonnet 4 | 47.7% | 40.2% | 21.7% |
| Gemini 2.5 Pro | 54.9% | 37.5% | 25.5% |
| Qwen2.5-VL-7B (base) | 2.2% | 1.0% | 1.0% |
| OpenWebVoyagerIL | 18.1% | 6.3% | 6.6% |
| OpenWebVoyagerMax | 26.2% | 20.5% | 11.7% |
| **Web-CogReasoner** | **30.2%** | **17.0%** | **10.1%** |

Web-CogReasoner is the strongest open-source agent on WebVoyager, and its average steps per successful task are the lowest reported (4.73 on WebVoyager, 7.00 final average, vs 6.52 final for OpenWebVoyagerMax and 9.76 for Claude Sonnet 4). On Online-Mind2Web it beats OpenWebVoyagerIL but trails OpenWebVoyagerMax on both splits; the paper notes OpenWebVoyagerMax is “not a strictly comparable zero-shot baseline due to additional sample collection and retraining on high-error sites”.

Offline (kept off the online table): on the paper’s own Web-CogBench the overall score is 84.4 vs 80.2 Gemini 2.5 Pro, 76.8 Claude Sonnet 4, 69.8 Qwen2.5-VL-7B and 46.4 UI-TARs-7B-SFT. On VisualWebBench it averages 86.3, slightly above UI-TARs at 86.0 and Claude Sonnet 4 at 85.9, slightly below Gemini 2.5 Pro at 86.6.

## What the paper’s own controls say

**KCoT ablation (Table 9, four WebVoyager sites).** With identical S1+S2+S3 data, removing the Knowledge-driven CoT drops online success from 42.9% to 25.35% — the paper calls KCoT “a crucial activator” bridging possessing and applying knowledge.

**Curriculum ablations (Tables 7-8).** Adding stages cumulatively lifts Web-CogBench overall 69.8 (base) → 72.1 (+Factual) → 78.3 (+Conceptual) → 84.4 (+Procedural). Single-stage training underperforms (S2 only 61.96, S3 only 60.66 overall vs 84.44 full), and online, S1+S3 reaches 23.47% vs 13.14% for S3 only — “procedural exploration relies on accurate factual grounding”.

**Judge validation (Appendix D).** The GPT-4o judge protocol is checked against two other LVM judges: within-1-point agreement of 98.7% (Element Understanding), 97.0% (WebPage Understanding), 96.0% (User Intent Prediction), with human-proxy correlation at 96.7 / 95.4 / 94.4. Dataset annotations average 97.8% human-verification accuracy and 96.9% cross-model consistency.

**Curriculum vs mixed SFT.** Compared only qualitatively: mixed multi-task training “terminate\[s\] the search within a limited number of attempts”, while curriculum-trained models keep exploring (Fig. 7).

## Where the evidence is thinner, in the paper’s words

- No seeds, runs or variance are reported for any number; every table is a single pass.
- UI-TARs-7B-SFT, arguably the strongest open-source baseline family, is missing from all online tables (“omitted due to missing online inference scripts”).
- Web-CogBench is “curated from a representative subset of Web-CogDataset” — the headline offline benchmark shares task families with the training data, while the online benchmarks do not show the same margin: commercial LVMs stay ahead (54.9% vs 30.2% on WebVoyager) and cross-web transfer (10.1%) trails the retrained OpenWebVoyagerMax (11.7%).
- The online ablation covers only four sites (Amazon, Cambridge, Coursera, GitHub).
- Qwen2.5-VL 72B and Qwen-VL-2.5-32B generate much of the training supervision; annotation quality is sample-checked, but the annotator’s own errors are not ablated.

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **transfer**, pattern C21. The judgment record credits: live online evaluation on WebVoyager and Online-Mind2Web, held-out websites, a component ablation (KCoT, knowledge stages), an inter-rater check of the LVM judge, and open-sourced code and data. It marks variance and budget matching as unclear, notes the partial baseline coverage online, and flags anti-pattern AP5. CUA Radar did not rerun anything; every number above is copied from the paper (version v3).
