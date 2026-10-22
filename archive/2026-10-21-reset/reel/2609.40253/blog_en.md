# ComputerSD: a computer-use agent that learns from a step-by-step analyst while it trains

*A CUA Radar reading of arXiv 2609.40253v2 (Du, Chen, Lu, Liu, Chen, Jiang, Xu, Shen). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2609.40253v2 · Code: https://github.com/ZJU-REAL/ComputerSD*

## The problem: a task verdict says little about individual steps

Online reinforcement learning lets a computer-use agent improve by acting in real desktop environments, but the usual reward is a single success-or-failure verdict from the environment verifier. It does not say which of the many actions in an episode were productive, redundant or wrong. On-policy self-distillation (OPSD) offers finer credit: the policy rescores its own sampled response while conditioned on privileged information (a reference trajectory, a hint), and the resulting token-level log-probability shifts say which tokens to reinforce or suppress. The paper argues that this breaks in two ways for computer use. Guidance written before the rollout stops matching the screen once the agent leaves the assumed path, and then it suppresses tokens of steps that were correct on the agent’s own path. And even relevant guidance shifts every token, whether or not the step was right: the authors report that over 80% of tokens at correct steps are suppressed and nearly 20% of tokens at incorrect steps are reinforced during training.

## What ComputerSD is

The agent is a screenshot-based desktop agent. It keeps the three most recent historical screenshots in context and emits a short “Action” sentence followed by a `computer_use` tool call with coordinates or keys (click, type, key presses, terminate). Training and evaluation run on OSWorld-Verified (real desktop applications) and, for transfer, WindowsAgentArena. The CUA Radar board files the method under sub-pattern K19 (dense step-level process signals for multi-turn GUI RL, inside the “learned outcome and process judges” family). Two 8B backbones are used: the general-purpose Qwen3-VL-8B-Thinking and the computer-use model EvoCUA-8B.

The mechanism has four parts:

1.  **GUI analyzer.** After each executed action, an analyzer reads the screenshots before and after it and returns a step-level value score plus “guide” and “avoid” text written for the pre-action state. The analyzer is initialised from Qwen3-VL-8B-Thinking and fine-tuned (LoRA) on step labels from an expert model, Kimi K3, over 1,776 trajectories (34,188 annotated steps) collected on the 222 training tasks. It is then frozen.
2.  **Privileged rescoring.** The same policy scores its sampled response twice, once with the ordinary context and once with the guidance added. The log-probability gap per token is the OPSD signal.
3.  **Value gate.** Each token’s gap is multiplied by the step score, and a sigmoid with sharpness 5 turns that product into a weight, so shifts that agree with the step judgment are kept and conflicting ones are attenuated.
4.  **Joint objective.** The gated OPSD loss (coefficient 0.01) is added to outcome-only GRPO, so the verifier’s task reward still anchors learning. A fully asynchronous pipeline overlaps rollout, analysis, rescoring and optimisation.

The training signal is therefore the verifier’s outcome reward plus step-level feedback from a learned analyzer. At evaluation time, models trained with ComputerSD use only the ordinary context, with no analyzer calls or guidance. Training uses 8 trajectories for each of 4 tasks per batch, 180 policy updates, a 30-step limit; evaluation uses a 50-step limit.

## Results as reported

All results are online success rates from the benchmarks’ official verifiers, averaged over three evaluation runs (the paper reports no standard deviations or intervals). Other models’ rows in the paper’s Table 1 come from their own reports, with different step budgets.

**OSWorld-Verified (Table 1, 50 steps)**

| Model                | Base | Outcome-only GRPO | ComputerSD |
|----------------------|------|-------------------|------------|
| Qwen3-VL-8B-Thinking | 33.8 | 37.9              | 39.8       |
| EvoCUA-8B            | 41.3 | 43.8              | 47.9       |

The paper states gains over GRPO of 1.9 and 4.1 points. It also reports that the EvoCUA-8B result exceeds all listed open-source models and most listed proprietary ones.

**Split by training exposure (Table 2).** The evaluation set has 222 in-domain tasks, which are also the online training tasks, and 139 out-of-distribution tasks from the Chrome and Multiple Apps categories that were excluded from training. WindowsAgentArena (154 tasks) was never trained on.

| Model                | In-domain | Held-out apps | WindowsAgentArena |
|----------------------|-----------|---------------|-------------------|
| Qwen3-VL-8B-Thinking | 40.5      | 23.0          | 19.2              |
| \+ GRPO              | 48.2      | 21.6          | 23.3              |
| \+ ComputerSD        | 47.5      | 27.5          | 24.5              |
| EvoCUA-8B            | 47.3      | 31.6          | 24.4              |
| \+ GRPO              | 52.2      | 30.2          | 24.2              |
| \+ ComputerSD        | 55.7      | 35.4          | 27.8              |

On held-out apps the paper states ComputerSD is ahead of GRPO by 5.9 points (Qwen3-VL) and 5.2 (EvoCUA); on WindowsAgentArena by 1.2 and 3.6. Note that on Qwen3-VL-8B-Thinking the in-domain figure is 47.5 for ComputerSD against 48.2 for GRPO. The paper’s reading is that GRPO improves in-domain but mostly degrades held-out performance relative to the base models, while ComputerSD improves both.

## What the paper’s own controls say

**Component ablations** (Qwen3-VL-8B-Thinking, OSWorld-Verified, full method 39.8): using the vanilla model as analyzer gives 38.0; replacing real-time feedback with fixed privileged guidance gives 35.0; removing the value gate gives 36.6. The last two are below outcome-only GRPO at 37.9. The paper reports drops of 1.8, 4.8 and 3.2 points respectively.

**Gate designs** (Table 4): an SDAR-style gate 38.1, a hard binary gate 35.2, a reverse gate 36.0.

**Other baselines on the same base model** (Appendix E): the prompt-only method, which inserts expert guidance into the context without updating the policy, reaches 34.6 from a base of 33.8. GRPO with the analyzer used as a process reward model, summing step scores into the trajectory reward, reaches 37.4.

**OPSD coefficient:** 0.1 gives 35.6, 0.01 gives 39.8, 0.001 gives 37.1.

**Cost and speed.** The asynchronous pipeline is reported to give five times the throughput of a synchronous version. Asynchronous GRPO and ComputerSD stabilise at about 370 and 210 trajectories per hour. ComputerSD reaches GRPO’s final performance after about 100 updates on Qwen3-VL-8B-Thinking and 40 on EvoCUA-8B, using about 56% and 22% of GRPO’s trajectory budget.

**Analyzer quality** (offline, 341 held-out annotated steps): agreement with the expert’s step judgments rises from 29.9% for the base model to 85.3% after fine-tuning, and the valid-output rate from 41.6% to 99.7%.

## Where the evidence is thinner, in the paper’s words

- The paper’s limitations section says ComputerSD “relies on the reliability of the GUI analyzer”, that errors in either output “can distort the OPSD signal”, and that the value gate “cannot fully resolve this issue when both outputs are unreliable”. Systematic analyzer errors “may still bias policy updates”.
- The analyzer is checked against the expert model’s labels, not against a ground-truth step label.
- Results are averaged over three evaluation runs; no variance is given. The ablations and gate comparisons use the Qwen3-VL-8B-Thinking backbone only.
- In-domain evaluation uses the same 222 tasks as online training. Held-out apps and WindowsAgentArena are the generalisation evidence, and the paper evaluates one training benchmark with two backbones.
- Training the analyzer needs an expert model (Kimi K3) for annotation, though not during online RL.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **transfer**. The record credits online evaluation by official verifiers, held-out app categories, same-setting outcome-only GRPO baselines, matched step budgets, cost reporting and a component ablation, plus the WindowsAgentArena transfer test. It lists variance as not reported and the check of the learned analyzer against ground truth as untested, and flags the anti-pattern AP4 (judge used without two-sided reliability validation) as unclear. The radar did not rerun any experiment; every number here comes from the paper (v2). The judgment record itself was made on v1.
