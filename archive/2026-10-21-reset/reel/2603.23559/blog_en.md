# ReCAP: teaching a native GUI agent to solve CAPTCHAs with generated reasoning and self-correction data

*A CUA Radar reading of arXiv 2603.23559v2 (Chen, Zhai, Wang, Yang, Zhang, Wang, Zhang; UIUC). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2603.23559v2 · Code (announced in the paper): https://github.com/ASTRAL-Group/ReCAP-Agent*

## The problem

Modern CAPTCHAs have moved from “hard-to-read” to “hard-to-reason”: image grids, sliders, icon matching and paged selection that demand OCR under distortion, fine-grained visual understanding, precise continuous control and multi-step interaction. The paper’s starting observation is two-sided. General native GUI agents (OpenCUA, UI-TARS, Qwen3-VL) are strong at everyday GUI tasks but, in the paper’s words, “tend to underperform on CAPTCHA solving as they lack complementary skills”; the paper also notes “there is a lack of public and systematic research on studying CAPTCHA solving in native GUI agents.” On the other side, specialized solvers such as Halligan and Oedipus handle specific CAPTCHA families but frame CAPTCHA solving as a standalone problem, rely on repeated model calls, external heuristics or explicit search, and do not carry general GUI ability. Existing CAPTCHA resources (Open CaptchaWorld, MCA-Bench) are designed for evaluation, not closed-loop policy training: no executable GUI feedback, no full meta-supervision, no failure-recovery traces.

## What ReCAP is

**The agent.** ReCAP is a native vision-language GUI agent: finetuned Qwen3-VL-8B and Qwen3-VL-32B in both Thinking and Instruct variants. It perceives raw screenshots of a rendered browser page and acts through Qwen3-VL-style computer-use tool calls (clicks, drag, type, key press, scroll, mouse move, wait, terminate), with coordinates on a 1000×1000 relative grid dispatched to the browser via Playwright. One response may contain several actions (click the input, type the answer, submit), which matters under CAPTCHA time limits. Platform: web/browser environments, both in training and evaluation. On the CUA Radar board the architecture pattern is C21 under trajectory-level policy training: synthesize reasoning annotations for demonstrations with a strong MLLM, then SFT a screenshot policy.

**The environment.** A dynamic CAPTCHA system with seven procedurally generated challenge types — Text, Compact Text, Icon Match, Icon Selection, Paged, Slider, Image Grid — built to stress four interaction primitives the paper identifies from deployed systems (reCAPTCHA, Geetest, Arkose Labs, hCAPTCHA): OCR, continuous control (dragging), spatial localization (clicking), and visual semantic comprehension. A Flask rendering engine injects stochasticity into layout and styling at request time, and composed asset banks (icons, categorized images, backgrounds, distorted text) make the instance space effectively unbounded. A meta API exposes complete ground truth: answer label, target coordinates, required interactions.

**The mechanism and its training signal.** Two data generators run on top of the environment. (1) Solution traces: an expert reasoning model (Qwen2.5-VL-72B-Instruct) receives the CAPTCHA screenshot, a prompt to reason as if the ground truth were unknown, and — crucially — the ground-truth solution and annotations, which constrain its final action sequence. It writes observe/infer/plan chain-of-thought; automatic checks verify the reasoning does not cheat by revealing the answer. The paper calls this setup STaR-like rationale bootstrapping. (2) Self-correction traces: a student model attempts the challenge; if the attempt fails, the expert gets the full failure context (before/after screenshots and the student’s reasoning-action trace) and writes a corrective reasoning trace as if it had discovered the mistake itself, implicitly guided by the recovery ground truth. Training interleaves reasoning and action tokens in one sequence, with a unified loss that reweights the two token groups (λthink = λact = 0.5) so long reasoning traces do not dominate short action sequences.

**Training corpus.** Approximately 150,000 solution trajectories and 10,000 self-correction trajectories, plus roughly 50,000 general GUI trajectories from Aguvis and 23,000 from AgentNet mixed in to preserve general GUI ability; one epoch of full-parameter SFT over about 230,000 samples (4× B200, bf16, DeepSpeed ZeRO-2, lr 1e-5).

## Results, as reported

All CAPTCHA results below are **online, interactive** solve rates: the model observes rendered frames, issues GUI actions, and receives binary success feedback on submission. The dynamic-benchmark evaluation uses a fixed set of 1,000 held-out instances from the same rendering engine (disjoint from training), a 5-step budget (8 steps for Image Grid and Paged), and no seeds or variance are reported. Halligan is evaluated on 100 samples per CAPTCHA type due to budget constraints and imposes no interaction-step limit.

| Model                  | Overall SR (%) | Avg. steps |
|------------------------|----------------|------------|
| UI-TARS-1.5-7B         | 33.60          | 2.47       |
| Qwen3-VL-8B-Instruct   | 24.70          | 2.51       |
| Qwen3-VL-32B-Instruct  | 39.30          | 2.31       |
| OpenAI CUA             | 31.80          | 2.33       |
| GPT-5.4                | 56.80          | 2.23       |
| Gemini-3-Flash-Preview | 59.90          | 1.98       |
| Halligan framework     | 25.14          | ≥3–5       |
| ReCAP-8B (Thinking)    | 71.90          | 1.54       |
| ReCAP-32B (Thinking)   | 81.00          | 1.54       |
| ReCAP-8B (Instruct)    | 78.60          | 1.33       |
| ReCAP-32B (Instruct)   | **84.20**      | 1.38       |

ReCAP-32B (Instruct) improves over its Qwen3-VL-32B-Instruct base from 39.30% to 84.20%, and the Instruct variants beat their Thinking counterparts; the paper also notes ReCAP solves with fewer model calls (1.33 on average for the 8B Instruct) than every baseline listed.

**Real-world transfer (still online, zero-shot).** On the Halligan benchmark of 26 real-world CAPTCHA types, where ReCAP models are not trained on the dataset and Halligan is explicitly designed for these types, ReCAP-8B (Instruct) and ReCAP-32B (Instruct) improve over their corresponding Qwen3-VL baselines by 14.50 pp and 11.42 pp on average, and both outperform Halligan by a small margin on average; ReCAP-32B (Thinking) improves over its baseline by 12.58 pp and beats it on 25 of 26 types. Frontier models stay competitive: Gemini-3-Flash-Preview obtains the highest average score in the full comparison, and Halligan remains noticeably stronger on some rotation and pattern-recognition types (e.g., baidu/rotate, geetest/iconcrush, yandex/kaleidoscope).

**General GUI ability (offline protocols, kept apart).** On Android Control, ScreenSpot-V2, Multimodal-Mind2Web and UI-Vision under official offline protocols, the 32B variants largely preserve performance — ReCAP-32B (Instruct) even improves UI-Vision Layout IoU from 0.4843 to 0.5566 — while the 8B variants drop on some grounding tasks (ScreenSpot-V2: 89.54 vs 91.12 for the 8B Instruct pair; UI-Vision Element: 22.05 vs 29.72).

## What the paper’s own controls say

- **CoT ablation** (same base, same data, only reasoning traces removed): overall SR falls from 71.90 to 66.40, with average steps essentially unchanged (1.61 → 1.54).
- **Self-correction ablation**: removing the 10k correction traces drops overall SR from 71.90 to 62.90; per type, the paper reports gains of +16.77pp on Text, +21.9pp on Slider, +7.50pp on Compact Text, +8.77pp on Icon Match, +3.65pp on Paged and +2.19pp on Image Grid.
- **Data-scale sweep**: 62.90 / 71.90 / 72.20 overall SR at 50% / 100% / 150% of the CAPTCHA data — gains saturate near the final scale.
- **Capacity**: an extra Qwen3-VL-4B-Thinking run shows an even larger relative drop on ScreenSpot-V2 (21.15% versus its baseline), supporting the paper’s capacity-based reading of the 8B degradation.
- **Held-out design**: the dynamic test set is disjoint from training data; the real-world benchmark is zero-shot for ReCAP while Halligan was built for it, and all Halligan numbers come from its released framework under the same protocol.

## Where the evidence is thinner, in the paper’s words

- “Our strongest empirical claim is therefore specific to the held-out dynamic CAPTCHA benchmark, while real-world transfer remains mixed.”
- “There remains a gap between these simulations and the messy, unpredictable real world” (synthetic training data).
- “Our reasoning traces are answer-conditioned and should be interpreted as scalable training supervision rather than verified faithful explanations.”
- Behavioral biometrics (mouse speed, hesitation) are not simulated; an Oedipus comparison, a full latency decomposition, and a sweep over reasoning/action loss weights are left to future work.
- No seeds or variance are reported for any evaluation, and the Halligan comparison is budget-limited (100 samples per type, no step limit).

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **transfer**. The score reflects what the paper reports: interactive online evaluation, a held-out environment, strong baselines including a specialized framework, cost reporting, two component ablations, and code announced for release; the judgment record marks variance as unclear and the Halligan budget match as partial, and flags that the CoT supervision is answer-conditioned. CUA Radar did not rerun any experiment; every number here comes from the paper (version v2).
