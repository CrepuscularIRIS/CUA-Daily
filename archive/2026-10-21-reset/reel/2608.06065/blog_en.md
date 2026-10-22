# The Next Screenshot Knows: hindsight distillation for mobile GUI agents

*A CUA Radar reading of arXiv 2608.06065v1 (Weiwei Li, Junzhuo Liu, Tong Chu, Hengfu Yu, Wen Li; University of Electronic Science and Technology of China). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.06065v1 · Code: announced (“The code and checkpoints will be made available”), not yet released at v1.*

## The problem: the evidence for an action arrives one screen too late

Most GUI agents are trained offline from successful trajectories, decomposed into prefix-action pairs: predict the action from the goal, the interaction history and the current screen, and discard everything that follows. The paper’s argument is that this throws away the rationale. To enable a setting hidden in a submenu, several entries on the current screen look equally plausible; only the next screenshot, where the submenu is open, shows which entry was the right one and why. Standard imitation “teaches the policy which action to take, but not why it is appropriate”, and a scalar RL reward says only whether a rollout was right, not what app knowledge would have justified it. The authors call this future-dependence: actions must be predicted from the past, but the evidence that explains them often appears only in the future.

## What GHD is

The agent is a mobile GUI agent on Android, evaluated on AndroidWorld and AndroidLab. At each step it observes a natural-language goal, the action history, and the current screenshot; it emits a reasoning trace followed by a JSON tool-call action (click, long_press, swipe with coordinates on a normalized 1000×1000 grid; text actions; discrete arguments). Base models are Qwen2.5-VL-7B and Qwen3-VL-8B, each fine-tuned with the OpenMobile recipe (screenshots resized to 420×896, about 3x fewer visual tokens, at the cost of a lower initial SFT score than the published OpenMobile checkpoint). On the CUA Radar board the paper sits in sub-pattern R01: offline single-step GRPO with rule-checked action rewards.

Gated Hindsight Distillation (GHD) adds one training-time device to this stack:

- **Privileged teacher.** A teacher with the same parameters as the student additionally receives the realized next screenshot of the successful demonstration. It never generates its own trajectory; under teacher forcing it re-scores the token distributions along the student’s own rollout (stop-gradient).
- **Gating.** Distillation is kept only when the prefix-only student fails the step verifier (reward below τ = 1.45) and the teacher’s position-wise top-1 decode recovers the demonstrated action (same action name, parseable JSON, coordinates within δ = 20 on the grid). The gate “directly verifies the signal used for distillation”.
- **Transfer.** A generalized Jensen-Shannon divergence (α = 0.5) between teacher and student distributions, evaluated on the student’s top-K = 100 tokens; the joint loss is L = L_GRPO + 0.1 · L_GHD. Dynamic sampling redraws up to three rollout groups per prompt (2.69 attempts per batch on average).
- **Training signal.** A rule-based step verifier — format, action-type match, and value (coordinate, edit-similarity, or exact match) — gives R in \[0, 1.5\], used both as the GRPO reward and as the gate. Training runs 200 steps on a hard subset of OpenMobile trajectories the SFT model fails in one attempt: 6,968 of 27,360 examples at 7B, 5,982 at 8B.

At deployment the teacher, the next screenshot and the gate are all removed: inference is the unchanged prefix-only student, with “no additional inference-time module”.

## Results, as reported

All numbers are task-level online success, Pass@1 (%), mean ± std over three independent runs; same data, same evaluation settings, and GRPO/GHD share the same initialization (Table 3).

| Model         | Method  | AndroidWorld     | AndroidLab       |
|---------------|---------|------------------|------------------|
| Qwen2.5-VL-7B | SFT     | 46.55            | 29.71            |
| Qwen2.5-VL-7B | GRPO    | 47.13 ± 0.65     | 31.93 ± 1.12     |
| Qwen2.5-VL-7B | **GHD** | **52.73 ± 1.51** | **43.10 ± 0.66** |
| Qwen3-VL-8B   | SFT     | 59.05            | 39.13            |
| Qwen3-VL-8B   | GRPO    | 61.35 ± 1.08     | 37.43 ± 0.42     |
| Qwen3-VL-8B   | **GHD** | **66.47 ± 0.68** | **54.11 ± 1.11** |

Against previously reported systems, each “under its original experimental setting” (Table 1), Ours-7B averages 47.9 Pass@1 (AndroidWorld 52.7, AndroidLab 43.1) and Ours-8B averages 60.3 (66.5, 54.1), which the paper describes as the best average Pass@1 among open-data models at both scales; OpenMobile-8B is 58.1 and UI-Venus-1.5-8B reaches 73.7 on AndroidWorld. One honest wrinkle in the same table: on Pass@3 at 8B, AndroidWorld is 73.3 for Ours against 78.0 for OpenMobile-8B, while AndroidLab Pass@3 is 65.2 against 62.3. There are no offline step-accuracy numbers; everything above is online.

## What the paper’s own controls say

**Component ablation (Table 2, AndroidWorld, 7B).** From GRPO at 47.13: adding the gate with an unprivileged teacher gives 47.84 (+0.71); adding dynamic sampling (still no future) gives 49.56 (+2.43); full GHD with the next screenshot reaches 52.73 (+5.60). The paper states the next screenshot adds a further 3.17 points, “the largest incremental gain”.

**Budget control (Table 5, 8B).** GHD without dynamic sampling uses the same one-attempt rollout budget as GRPO and still reaches 63.64 ± 2.04 on AndroidWorld and 51.93 ± 0.84 on AndroidLab (improvements the paper states as 2.29 and 14.50 points); dynamic sampling adds a further 2.83 and 2.18.

**Privileged-input control (Table 4, AndroidWorld, 8B).** Same pipeline, only the teacher’s hint changes: the reference action alone gives 58.62 (−0.43 vs SFT), adding reference reasoning 60.34 (+1.29), and the next observation 64.67 (+5.62); the full method with GRPO reaches 66.47 (+7.42). Giving the answer alone does not help; the future screen does.

**Transfer-mechanism controls.** Distillation beats a STaR-style off-policy self-training target under every privileged signal tried (Figure 3), and a GUI-Shift-style inverse-dynamics auxiliary task added to GRPO gives only +0.28 (47.41) versus +5.60 for GHD (Table 6), both from the same SFT checkpoint.

**Per-application (Table 7).** On a representative 8B run over 138 AndroidLab tasks, GHD beats GRPO on seven of nine apps (overall 55.07 vs 37.68), with the largest gains on Bluecoins (26.67 to 60.00) and Contacts; the exceptions are Calendar and Zoom, the latter with five tasks.

## Where the evidence is thinner, in the paper’s words

- The comparison table is explicitly “intended to establish overall competitiveness rather than to isolate the contribution of GHD”: systems differ in “model family, training data, image resolution, and algorithms”, and the reproduced SFT start uses 420×896 screenshots, below the published OpenMobile checkpoint’s score.
- Held-out apps are not discussed: the paper does not state whether the AndroidWorld/AndroidLab apps are disjoint from the OpenMobile trajectories used for training.
- Cost reporting is partial: data counts and GPU types (4 GPUs) are given, but the wall-clock comparison is “indicative rather than a controlled systems comparison because the experiments were conducted on non-dedicated rented instances”.
- Code and checkpoints are only announced, and the per-application breakdown is a single representative run.

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **online**, sub-pattern R01 (offline single-step GRPO with rule-checked rewards). The judgment credits the online evaluation on two benchmarks, three-run means with standard deviations, controlled comparisons under the same initialization, data and rollout budget, and ablations covering the gate, dynamic sampling, the privileged input, and the transfer mechanism. It marks the held-out-environment question as unclear, cost reporting as partial, and notes the code is not yet released and that only 7B/8B open bases are tested. CUA Radar did not rerun anything; every number here comes from the paper (version v1).
