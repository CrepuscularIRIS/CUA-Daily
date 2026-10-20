# OpenMobile: open task and trajectory synthesis for mobile agents, and what its numbers do and do not show

*A CUA Radar reading of arXiv 2604.15093v1 (Cheng, Li, Ma, Chen, Cao, Sun, Ding, Xu, Yan, Chen, Tuan, Zhang, Lu, Lin). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2604.15093v1 · Code: https://github.com/njucckevin/OpenMobile-Code*

## The problem: strong mobile agents, closed recipes

The paper starts from a gap. Recent industry systems (Step-GUI, MAI-UI, UI-Venus-1.5, MobileAgent-v3.5) are described as approaching 70% on AndroidWorld, but their data and synthesis recipes are not released. Open-source agents, which mostly train on human-annotated sets such as AndroidControl and AMEX, are reported at around 30% on the same benchmark (the paper cites ScaleCUA and UI-S1 as examples). The authors argue that without the recipe, the community cannot study which data properties matter.

They name two difficulties. Existing interaction-driven task synthesis couples exploration with generation, so each instruction is bounded by one trajectory. And expert distillation never shows the learner recovering from its own mistakes, while self-evolution does but converges slowly and is capped by the learner.

## What OpenMobile is

OpenMobile is a data synthesis framework plus a released dataset, not a new agent architecture. The agent being trained is a vision-language model that receives the current screen, the instruction and the history, and emits actions in the Qwen3-VL action space and response format (terminal actions `complete` and `answer`). The platform is Android, using the emulator provided by AndroidWorld. On the CUA Radar board the paper sits under the pattern family “exploration-driven task synthesis” (sub-pattern K15).

The pipeline has five steps.

1.  **Exploration.** A random walk: each session runs 10 steps, clicking or typing on a random interactable element from the accessibility tree. The authors say the framework is agnostic to the exploration strategy.
2.  **Global environment memory.** Screens are clustered by perceptual hash (similarity threshold 0.95) into N unique screens. Transitions define each screen’s neighbours; Gemini-3.1-Pro-Preview extracts functionality descriptions per screen, and a per-app embedding index supports retrieval.
3.  **Memory-augmented task synthesis.** For each screen the prompt contains the screen itself, short-term memory (1 predecessor and up to 3 successor screens) and long-term memory (30 semantically related functionalities from other screens of the same app, filtered so that pairwise similarity stays below 0.8). Gemini-3.1-Pro-Preview writes instructions. They are scored by an LLM on a 1 to 5 scale (clarity or reasonableness below 4 is discarded), deduplicated at cosine similarity 0.8 and capped per app.
4.  **Policy-switching rollout.** At each step the action comes from the expert or the learner, controlled by a switch variable. In the error-intervention variant the learner starts; a monitor (Gemini-3.1-Pro-Preview) looks at the recent actions and the last two screenshots and, when it sees deviation from progress, hands control to the expert. This happens at most twice per rollout, and the expert acts for at least 3 steps before control returns.
5.  **Training.** Only the expert’s steps are kept as targets, but the full history, including the learner’s errors, stays in the context. The expert rewrites each step’s chain of thought. Supervised fine-tuning with LLaMA-Factory, batch size 32, learning rate 1e-5, 3 epochs.

The resulting dataset has about 2,800 instructions and 34K action steps across 20 Android apps, with an average trajectory length of 12.2 steps and 129 words of reasoning per step. The training signal is expert (Gemini) actions on LLM-synthesised, LLM-filtered tasks; the SFT recipe has no reward model or verifier.

## Results as reported

All benchmarks below are online (agents act in a live emulator). Pass@1 is the mean of three runs; the plus-minus values in the paper are half-ranges (max minus min over 2), not standard deviations. MobileWorld is evaluated on its GUI-only subset. The models are Qwen2.5-VL-7B and Qwen3-VL-8B fine-tuned on the OpenMobile data.

| Method (base)              | AndroidWorld | AndroidLab   | MobileWorld |
|----------------------------|--------------|--------------|-------------|
| Qwen2.5-VL-7B (no tuning)  | 25.5         | 10.6         | 7.7         |
| ScaleCUA-7B (Qwen2.5-VL)   | 27.2         | 30.0         | 7.7         |
| **Ours-7B** (Qwen2.5-VL)   | **51.7**     | 22.7         | 14.8        |
| Qwen3-VL-8B (no tuning)    | 47.6         | 43.5         | 9.4         |
| UI-Venus-1.5-8B (Qwen3-VL) | 73.7         | 55.1         | 17.1        |
| MAI-UI-8B (Qwen3-VL)       | 70.7         | not reported | 27.5        |
| **Ours-8B** (Qwen3-VL)     | **64.7**     | 51.5         | 17.7        |

Pass@3 (solved if any of three runs succeeds) is 68.1 and 78.0 on AndroidWorld for the 7B and 8B models. The paper uses Pass@3 as an upper-bound indicator.

Read directly, the table shows the following. Both fine-tuned models improve on their own base everywhere. Against the open-data baselines the picture is mixed: Ours-7B is far above ScaleCUA-7B and UI-S1-7B (34.0) on AndroidWorld but below ScaleCUA-7B on AndroidLab (22.7 against 30.0). The closed-data 8B systems in the table are higher on AndroidWorld than Ours-8B (UI-Venus-1.5-8B 73.7, MAI-UI-8B 70.7), so “competitive” in the paper’s wording is about the gap, not parity. The introduction gives MobileWorld for Ours-8B as 17.4 while Table 1 says 17.7; the table value is used here.

The appendix also reports Qwen2.5-VL-72B fine-tuned on the same data at 59.3 on AndroidWorld, and a table against other synthesis methods that the authors call an imperfect comparison, since base models and settings differ.

## What the paper’s own controls say

**Task synthesis.** With a fixed budget of 1.5K trajectories on AndroidWorld, OpenMobile instructions give 48.3, a coupled baseline (same prompt, but a single trajectory’s screenshots as context) gives 45.3 and OS-Genesis gives 34.1. In a pairwise human study of 50 comparisons (win / tie / loss), complexity is 0.68 / 0.22 / 0.10 against OS-Genesis and 0.26 / 0.62 / 0.12 against the coupled baseline; soundness is 0.44 / 0.48 / 0.08 and 0.06 / 0.90 / 0.04. The authors read this as harder instructions of comparable soundness.

**Rollout strategy.** Also at 1.5K trajectories and with Qwen2.5-VL-7B as the learner: expert distillation 44.8, self-evolution 33.8, random switching 45.1, error-intervention switching 48.3. The average number of error-recovery instances per trajectory, counted by hand on 50 trajectories, is 0.42, 0.10, 0.64 and 1.56 respectively. The recovery counts rank the strategies in the same order as the scores.

**Overlap with the benchmark.** Because the data is synthesised in the AndroidWorld environment, the authors check for leakage. Using text-embedding-3-large, only 3.5% of synthetic instructions exceed a cosine similarity of 0.7 to an AndroidWorld test instruction; the appendix lists the nearest synthetic instruction for every test task (similarities up to 0.831). Removing the most test-similar instructions costs little at 10% and notably more at 40%, which the paper attributes to losing core app functionality. A coverage analysis shows that the share of test-required functionalities covered grows with instruction count and is higher for OpenMobile than for the coupled pipeline.

**Reinforcement learning.** Step-level GRPO and trajectory-level agentic RL did not beat SFT: the RL variant of Ours-8B reaches 64.1 on AndroidWorld against 64.7 for SFT, with 53.9 against 51.5 on AndroidLab and 16.8 against 17.7 on MobileWorld.

## Where the evidence is thinner

- **Environment overlap.** The training data comes from the same emulator and the same 20 apps as AndroidWorld. The similarity and removal analyses address this, but AndroidWorld is not held out. AndroidLab (novel apps) and MobileWorld (long-horizon, cross-app) are the generalisation evidence, and there the 7B model is mixed against the open-data baseline.
- **Closed components.** Annotation, task writing, monitoring and the expert policy all use Gemini-3.1-Pro-Preview. No validation of the LLM quality filter is reported, and cost is described only by dataset size.
- **Small hand-counted samples.** Error-recovery counts rest on 50 inspected trajectories per strategy, the quality study on 50 pairs.
- **Variance.** Three runs per benchmark; the half-range for Ours-8B on AndroidWorld is 3.2. Some baseline numbers come from prior work or leaderboards.

## CUA Radar’s read

CUA Radar scores this paper **73 (★★★)**, evidence level **transfer**. The judgment record credits online evaluation on three benchmarks, repeated runs, open-data baselines, component ablations and released data and code, and marks held-out environments, matched budget and cost as partial. It flags the overlap between the synthesis environment and the AndroidWorld benchmark (anti-pattern AP5), and records that no validation of the LLM quality filter was found. The radar did not rerun any experiment; every number here comes from the paper (version v1).
