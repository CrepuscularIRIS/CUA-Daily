# UI-Mem: a mobile GUI agent trained with online RL while an evolving memory of workflows, skills and failure patterns steers its rollouts

*A CUA Radar reading of arXiv 2602.05832v1 (Xiao, Wang, Wang, Liu, Chai, Pan, Zhou, Chen, Wen, Li). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2602.05832v1 · Project page (listed in the paper): https://ui-mem.github.io/*

## The problem: sparse rewards and the same mistakes, task after task

Online reinforcement learning lets a GUI agent learn from live interaction, usually with GRPO and an outcome reward. The paper names two bottlenecks. Credit assignment: in a long task a single final error gives negative feedback even when intermediate steps were right. Repetition: similar failure modes (the example is a confirmation popup) recur across tasks and the agent cannot carry the lesson forward. A sampled GRPO group is also often all failures, so the advantage has zero variance and gives no gradient. Experience replay and step-level dense rewards address parts of this, but the paper argues neither transfers reusable experience across tasks or apps.

## What UI-Mem is

**The agent.** A multimodal LLM (Qwen3-VL, 4B and 8B) on an Android emulator. The state is the screenshot plus the instruction; actions are atomic GUI operations (Click, Swipe, Type, Home, and open_app in the trajectory figures). The reward is a 0/1 outcome unless shaped as below. On the CUA Radar board this is pattern C19, accumulating reusable knowledge from the agent’s own runs, here inside an RL loop.

**The memory.** Three levels, stored as parameterised templates in a vector database: high-level workflows (ordered subtasks, e.g. open the mail app, select recipients, type, send), mid-level subtask skills (e.g. tap search, type the query, select the top result) and failure patterns (e.g. do not click Save before a filename is entered). Concrete values are replaced by placeholders so one template covers many tasks. At rollout time the instruction is embedded, top-k task templates are retrieved, DeepSeek-V3 picks the match and extracts variable bindings, and the template is instantiated into a plan. Candidate plans are ranked by a UCB score (success count plus an exploration bonus); failure patterns by recency.

**Stratified Group Sampling.** Each GRPO group (G = 4 rollouts per query) is split into strong guidance (workflow, skills and failure patterns), weak guidance (workflow only) and none. The aim is outcome diversity inside the group, so the advantage stays informative, while training the unguided policy towards the guided one. A dynamic dropout curriculum tracks a moving average of each task’s success rate and shifts probability from strong to no guidance as the agent improves. The reward adds a subtask-progress term and a bonus for successes obtained with no guidance.

**Self-evolving loop.** A text-based reward pipeline judges each trajectory: Qwen2.5-VL-72B-Instruct describes screens and actions in text, then DeepSeek-V3 checks which essential task states were reached. Seed1.8 extracts success plans and a diagnosis of the first failed subtask, values become placeholders, and entries are merged with a cosine-similar one or added as new.

**Training setup.** 256 queries from AMEX, AndroidLab and UI-Genie instructions, filtered for emulator apps and augmented with GPT-4o; five epochs, learning rate 1e-6. The main text gives no values for the reward weights, UCB weight or curriculum thresholds, and no compute cost.

## Results, as reported

All results are online, in emulators. ⋆ means memory is also retrieved at inference. No seeds, repeated runs or confidence intervals appear anywhere in the paper.

**AndroidWorld** (116 tasks, 20 apps), success rate in %:

| Model          | Success rate |
|----------------|--------------|
| Qwen3-VL-4B    | 45.3         |
| UI-Mem-4B      | 58.2         |
| UI-Mem-4B⋆     | 62.5         |
| Qwen3-VL-8B    | 47.6         |
| UI-Mem-8B      | 66.8         |
| UI-Mem-8B⋆     | 71.1         |
| Step-GUI-8B    | 67.7         |
| Gemini-2.5-Pro | 69.7         |
| Seed1.8        | 70.7         |

The paper calls UI-Mem-8B⋆ at 71.1 state-of-the-art, ahead of Gemini-2.5-Pro and Seed1.8. That row uses test-time memory; without it the 8B model (66.8) sits just below Step-GUI-8B in the same table.

**AndroidLab** (138 tasks, nine offline apps), Sub-Goal Success Rate (Sub-SR) and success rate (SR):

| Model         | Sub-SR | SR   |
|---------------|--------|------|
| Qwen3-VL-4B   | 48.2   | 37.0 |
| UI-Mem-4B     | 49.5   | 37.7 |
| UI-Mem-4B⋆    | 51.9   | 39.9 |
| Qwen3-VL-8B   | 45.3   | 34.8 |
| UI-Mem-8B     | 52.7   | 43.5 |
| UI-Mem-8B⋆    | 56.0   | 44.9 |
| MobileRL (7B) | –      | 42.5 |

At 4B the SR gain without test-time memory is small (37.7 against 37.0). No offline step-accuracy benchmark is reported.

## What the paper’s own controls say

**RL paradigms, 8B, AndroidWorld.** Baseline 47.6; Vanilla GRPO 53.0; GRPO plus progress reward 57.3; GRPO plus experience replay 56.5; memory as inference-time prompting only 52.6; GRPO plus inference-time prompting 55.2; UI-Mem 66.8. The paper concludes that memory as context alone helps little if the model has not learned to use it. It does not say whether these variants share rollout or step budgets.

**Component ablation (8B, AndroidWorld).** Full 66.8. Only workflows 59.5‡, only skills 61.6‡, only failure patterns 58.6‡. Raw experience instead of templates 58.2. No memory update 62.9. No stratified sampling (full guidance everywhere) 48.3‡, below Vanilla GRPO, which the paper reads as over-reliance on memory.

**Training dynamics.** Figure 7 shows qualitatively that standard GRPO’s success rate fluctuates without a clear upward trend and its intra-group reward variance often collapses near zero; UI-Mem trains more stably. No numeric values are given.

**Held-out apps.** Five AndroidLab apps are absent from training. Success rates as printed in Figure 6 (baseline Qwen3-VL / UI-Mem zero-shot without retrieval / UI-Mem with retrieved memory):

| App       | Baseline | Zero-shot | With memory |
|-----------|----------|-----------|-------------|
| Bluecoins | 33.3‡    | 33.3‡     | 53.3‡       |
| Cantook   | 41.7‡    | 50.0‡     | 66.7‡       |
| Maps.me   | 13.3‡    | 33.3‡     | 33.3‡       |
| Pi-Music  | 16.7     | 25.0‡     | 33.3‡       |
| Zoom      | 40.0‡    | 40.0‡     | 80          |

The paper says zero-shot matches or beats the baseline on all five and that memory adds “particularly substantial improvements on Bluecoins and Maps.me”. In the printed values the Maps.me zero-shot and with-memory bars are equal, and the larger memory-time gains are on Cantook and Zoom. Model size, tasks per app and runs are not stated.

**The reward judge.** Table 4 compares the two-stage text pipeline with MLLM-as-a-judge. Qwen2.5-VL-72B alone: accuracy 0.724 (F1 0.811); Gemini 2.5 Pro alone: 0.776 (F1 0.837); Qwen2.5-VL-72B plus DeepSeek-V3, as used in training: 0.900 (F1 0.902). The size and source of the labelled set are not stated.

## Where the evidence is thinner

- No seeds or confidence intervals; differences of a point or two (37.7 against 37.0 at 4B on AndroidLab) cannot be separated from noise with the paper alone.
- The paper does not say whether AndroidWorld apps overlap with the training apps; training tasks are filtered to “core apps in our emulator environment”. The held-out AndroidLab apps are the only explicit held-out test, and its details are sparse (see above).
- Training depends on several large external models (Qwen2.5-VL-72B, DeepSeek-V3, Seed1.8, GPT-4o); their cost is not reported.
- The impact statement notes live-environment exploration may cause unintended actions such as deleting data or financial transactions, and that screenshots with personal data raise privacy concerns.

## CUA Radar’s read

CUA Radar scores this paper **76 (★★★)**, evidence level **transfer**. The score reflects online evaluation on AndroidWorld and AndroidLab, five held-out apps, strong baselines, a component ablation, a validation of the learned reward judge, and a project page. The judgment record marks seeds and variance, and matched budgets, as not reported, and flags possible overlap between memory or training data and evaluation apps (AP5, recorded as mitigated by the held-out apps). CUA Radar did not rerun any experiment; every number here comes from the paper (version v1).
