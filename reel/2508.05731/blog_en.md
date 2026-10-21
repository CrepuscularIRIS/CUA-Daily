# InfiGUI-G1: a grounding model that points N times per pass and is rewarded by efficiency

*A CUA Radar reading of arXiv 2508.05731v2 (Liu, Liu, Zhu, Li, et al.; Zhejiang University, HK PolyU, InfiX.ai, UChicago, Amazon). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2508.05731v2 · Code: https://github.com/InfiXAI/InfiGUI-G1*

## The problem: RLVR points precisely, but at the wrong thing

GUI grounding maps a natural-language instruction to one interactive element on a screenshot. The paper splits this into two dimensions. Spatial alignment is pointing accurately at a location; semantic alignment is pointing at the *right* element. Reinforcement Learning with Verifiable Rewards (RLVR) has improved spatial alignment, but the authors argue that “inefficient exploration bottlenecks semantic alignment, which prevent models from learning difficult semantic associations”. Standard RLVR samples one action per state from the current policy, so it keeps re-sampling its own high-confidence errors — the paper’s example is an instruction “use the camera to search for an object”, where a weak model repeatedly picks the generic Camera button and never stumbles on Google Lens. The correct tail action is never sampled, so no reward ever corrects the misunderstanding.

## What InfiGUI-G1 is

The agent is a single-step grounding policy, not an interactive agent. It perceives a GUI screenshot plus a natural-language instruction; it acts by emitting a click coordinate (x, y). Reasoning is generated inside `<think>...</think>` tags before the answer. The backbones are the open-source Qwen2.5-VL-3B-Instruct and Qwen2.5-VL-7B-Instruct, and the board pattern on the CUA Radar is R01: offline single-step RL with rule-checked rewards, no environment rollout. The method is called Adaptive Exploration Policy Optimization (AEPO) and has three parts:

1.  **Multi-answer generation.** Instead of one point, the model emits a set of N candidate points {p1, …, pN} in a single forward pass, forcing it to look beyond its most confident prediction.
2.  **Adaptive Exploration Reward (AER).** Derived from a first-principles efficiency ratio η = U/C. Utility U is +1 if any candidate falls inside the ground-truth box B and −1 otherwise. Cost C is the geometric mean of a proposal cost (N) and a verification cost: on success the first correct point has some rank k, so C = √(N·k) and the accuracy reward is 1/√(N·k); on failure all N points must be checked, C = N, and the reward is −1/N. Efficient, confident hits are rewarded most; failures get a diminishing penalty that encourages wider exploration.
3.  **Collinear penalty.** If the generated points are approximately collinear (the triangle area of any three points is close to zero), the reward is overridden to −1. This blocks degenerate linear scanning and, in the authors’ words, is “critical for preventing reward hacking”.

The total reward adds a +1/0 format reward, and the policy is updated with RLOO. Training data is a mixture of public GUI datasets (Widget Caption, OmniAct, GUICourse, etc.), about 44k samples, filtered by generating 8 responses at temperature 1.0 and dropping samples where all 8 are correct. Training used 16 H800 GPUs, learning rate 1e-6, rollout batch 128, RLOO rollout n = 8, for 3 epochs.

## Results, as reported

All numbers below are **offline** top-1 grounding accuracy (%): a prediction counts if the point falls inside the ground-truth bounding box. For the InfiGUI-G1 models only the first generated answer is evaluated; the paper reports standard deviation σ over 5 runs for its models. There are no online or interactive agent results in the paper.

| Model (avg per benchmark) | MMBench-GUI | ScreenSpot-Pro | UI-Vision | UI-I2E-Bench | ScreenSpot-V2 |
|----|----|----|----|----|----|
| Naive RLVR-3B (same data) | 70.9 | 39.8 | 19.4 | 71.6 | 90.1 |
| Naive RLVR-7B (same data) | 79.3 | 47.6 | 24.1 | 75.8 | 92.5 |
| InfiGUI-G1-3B | 73.4 | 45.2 | 22.0 | 72.6 | 91.1 |
| InfiGUI-G1-7B | 80.8 | 51.9 | 26.1 | 77.4 | 93.5 |

The paper also reports an “Exploration Success Rate” for its models — whether *at least one* of the N candidates is correct — which is a different, easier metric (e.g. 52.0 on ScreenSpot-Pro at 3B, 58.0 at 7B, with about 2 candidates per sample); it should not be compared with the top-1 rows above. Against external methods, the 7B model is above GUI-G2-7B (47.5) and UI-AGILE-7B (44.0) on ScreenSpot-Pro, above UI-TARS-1.5-7B (64.3), UGround-V1-7B (65.7) and InternVL3-72B (72.2) on MMBench-GUI, and above UI-TARS-72B (25.5) on UI-Vision. The abstract summarizes the internal comparison as relative improvements of up to 9.0% over the naive RLVR baseline.

## What the paper’s own controls say

**Matched internal baseline.** The Naive RLVR models are trained on the exact same 44k dataset with the same optimized hyperparameters, isolating the AEPO changes; InfiGUI-G1 beats them on every benchmark at both sizes.

**Ablations (ScreenSpot-Pro, 7B).** Removing one component at a time: full model 51.9; without multi-answer generation 46.5; without AER (naive reward) 41.4; without AER’s rank factor k 44.0; without the collinear penalty 37.0 — and answers per sample explode from 2.0 to 8.2. The 3B model shows the same order (45.2 full, 35.3 without the penalty, 6.6 answers). Removing k leaves a model that still finds answers (exploration success 47.6) but ranks them first too rarely (38.1 accuracy).

**Exploration efficiency.** Even when Naive RLVR gets four independent attempts (pass@4: 43.5 at 3B, 52.1 at 7B), its success rate stays below InfiGUI-G1’s single-pass exploration success (52.0 and 58.0 at about 2 candidates), which the paper reads as structured rather than brute-force exploration.

**Hard samples.** ScreenSpot-Pro was split by the base model’s 16-sample success: on the “hard” subset (base model 0/16), Naive RLVR reaches 10.8 and InfiGUI-G1 17.4 at 7B, a relative improvement the paper reports as +61.1%; middle-subset gains are smaller (+8.0% at 7B, +4.0% at 3B), and easy samples are 100 for both.

**Adaptive behavior.** The 7B model generates the most answers on the hardest benchmark (UI-Vision: 26.1% accuracy, 2.1 answers) and the fewest on the easiest (ScreenSpot-V2: 93.5% accuracy, 1.4 answers).

## Where the evidence is thinner, in the paper’s words

- Everything is offline single-step grounding; no OSWorld/AndroidWorld-style online evaluation appears, and the paper’s primary metric is point-in-box accuracy.
- Only two backbones are used: “Our InfiGUI-G1 models are built upon the open-source Qwen2.5-VL-3B-Instruct and Qwen2.5-VL-7B-Instruct as backbones.”
- Generalization is argued, not constructed: “these benchmarks contain many applications and scenarios not present in our training data, indicating that AEPO fosters a robust understanding rather than overfitting” — the training/test app overlap is not quantified.
- Stated limitations: “the computational overhead from multi-answer generation and a performance ceiling imposed by the backbone MLLM’s visual capabilities”.
- Gains over the same-data baseline are a few points on the averages; the larger relative numbers (+61.1%) are on the small hard subset.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **offline**, sub-pattern R01 (rule-reward single-step RL). The score reflects what the paper reports: offline evaluation on five grounding benchmarks, benchmarks containing unseen applications, variance over 5 runs, a same-data internal baseline, GPU cost, a component ablation, and released code. The judgment record flags that online evaluation is not reported, that the backbone choice is narrow (3B/7B only), and that budget matching is partial (the pass@4 comparison rather than compute-matched training). CUA Radar did not rerun any experiment; every number here comes from the paper (version v2).
