# CoAdapt-GUI: a mobile agent that adapts both its workflow notes and its LoRA weights on a new app

*A CUA Radar reading of arXiv 2608.11588v1 (Guo, Gu, Jiang, Chi, Reid, Wang, Yu, Liu, Wang, Chen). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.11588v1 · No code repository is listed on the board.*

## The problem: a new app is more than new tasks

Mobile GUI agents do well on benchmarks whose apps and workflows were seen in training. The paper starts from the observation that success on new tasks inside a familiar interface does not imply effective behavior in an unfamiliar application. It cites an earlier study (AndroidWorld-Generalization) in which source-side online RL improves a 7B policy by 26.1 percentage points on unseen task instances, but only 8.3 points on unseen apps.

An unseen app can expose two kinds of gap. The agent may understand the goal but fail to ground actions to unfamiliar interface elements, or it may execute individual actions correctly and still lack the workflow and completion conditions needed to finish. Updating only the policy or only the context may leave one of these unresolved. The setting is test-time adaptation (TTA): a limited interaction budget on the target app, no target demonstrations, and a frozen result before held-out evaluation.

## What CoAdapt-GUI is

**The agent.** It is a mobile GUI agent: a vision-language policy that receives the task, the current observation, the interaction history and a rendered block of workflow text (the paper’s appendix lists the screenshot and a UI-element list among the inputs) and emits actions that the Android emulator executes. Two backbones are used: the released step-500 UI-TARS-7B checkpoint in one setting and Qwen3-VL-8B-Instruct in the other. The platform is Android. On the CUA Radar board the architecture pattern is C19, experience memory and retrieval.

**Two adaptive states.** An explicit workflow state M and a parametric state theta (a LoRA adapter on a frozen VLM). Each transferable workflow entry has four typed fields: when it applies, an abstract procedure, failure or recovery conditions, and completion checks.

**The transfer boundary.** For each source app the system builds a screen-transition finite-state machine (concrete screens, transitions, visible cues). That app-bound part never leaves the source app. Only an abstracted entry is eligible to cross to another app, and a schema validator and linter reject entries that contain app names, package or resource identifiers, concrete widget labels, coordinates or task-instance values. Eligible entries are grouped by Google Play category into a frozen source library. A target app retrieves only its own category; if its category is absent from the source pool, retrieval returns an empty prior.

**Reward-guided context update.** During adaptation the controller keeps a population of context variants rated with TrueSkill. Each round it samples up to two variants, runs four matched rollouts per task-context pair and updates ratings from the executable task rewards. A frozen reflector (Claude Opus 4.7 in the AndroidWorld Plus configuration) contrasts successful and failed traces and proposes a typed diff to a high-rated parent. The child enters the population only after schema, provenance and lint checks, and it inherits no reward: it earns a rating only when sampled in later rounds. The highest-rated validated state is kept at the end.

**Task-context-matched policy update.** The same rollouts feed an online group-relative objective (Shao et al. 2024). Because the context changes the policy’s input, advantages are computed only among rollouts that share both task and context variant. Groups with a single member or constant reward give no gradient; the buffer is on-policy and cleared after each update attempt.

**Training signal.** Executable task reward from the benchmark’s programmatic evaluator, on the agent’s own target-app rollouts. After the budget is spent, context and adapter are frozen and held-out tasks are run. The two channels are coupled through interaction, not through gradients: the context shapes the trajectories the policy learns from, and the policy produces the successes and failures the reflector reads.

## Results as reported

All numbers are success rate (SR) from online emulator episodes scored by the benchmark’s programmatic evaluator. The paper reports no offline step-accuracy numbers.

**Setting 1: AndroidWorld-Generalization, UI-TARS-7B, five target apps, 48 held-out instances.** Adaptation and evaluation use the same 16 task templates with non-overlapping seeds, so this tests new instances of task types seen during adaptation. Base Policy and Policy-Only TTA are reported values from the earlier AndroidWorld-Generalization paper; the other three rows are the authors’ mean ± standard deviation over five runs.

| Method                  | Adapt. instances | SR (%)       | Source        |
|-------------------------|------------------|--------------|---------------|
| Base Policy             | 0                | 27.10        | Reported      |
| Static Context Transfer | 0                | 28.75 ± 2.28 | Ours (5 runs) |
| Policy-Only TTA         | 40               | 37.50        | Reported      |
| Context-Only TTA        | 40               | 35.00 ± 1.74 | Ours (5 runs) |
| CoAdapt-GUI             | 40               | 45.00 ± 1.86 | Ours (5 runs) |

The paper states that CoAdapt-GUI is 7.5 points above the reported Policy-Only TTA, and 10.00 points above Context-Only TTA under the same adaptation instances and rollout budget.

**Setting 2: AndroidWorld Plus, Qwen3-VL-8B-Instruct, 105 held-out episodes with templates disjoint from adaptation.** The authors extended AndroidWorld with three apps from B-MoCA and three from AndroidLab (25 apps, 191 templates). Twelve apps are source and 13 are target. Within each target app, adaptation and evaluation use disjoint templates. Each adaptive configuration runs 20 rounds per app.

| Method                  | Category-Shared | Category-Novel | Overall SR (%) |
|-------------------------|-----------------|----------------|----------------|
| Base Policy             | 47.2            | 29.4           | 38.6           |
| Static Context Transfer | 56.5            | 29.4           | 43.3           |
| Policy-Only TTA         | 53.7            | 25.5           | 40.0           |
| Context-Only TTA        | 63.9            | 31.4           | 48.1           |
| CoAdapt-GUI             | 70.4            | 34.3           | 52.9           |

The paper reports a gain of 14.3 points over the Base Policy. One 20-round adaptation run took about 9–10 GPU-hours on NVIDIA H200 GPUs.

## What the paper’s own controls say

- **Component path (Table 2, Appendix E).** The cumulative context path (Static Context Transfer, then Context-Only TTA) reaches 48.1, which the paper states is 9.5 points above the Base Policy; Policy-Only TTA gains 1.4. CoAdapt-GUI is a further 4.8 points above Context-Only TTA. The incremental table also shows Policy-Only TTA decreasing Category-Novel performance (a change of -3.9), while target-side context construction improves both groups.
- **A built-in source-transfer control.** In Category-Novel apps source retrieval is empty, so Static Context Transfer equals the Base Policy exactly (29.4). Context-Only TTA and CoAdapt-GUI still improve there (31.4 and 34.3), which the paper reads as target-side adaptation working without category-matched source experience.
- **Held-out design.** Source and target app pools are disjoint, all updates and checkpoint selection use only the adaptation split, and both states are frozen before the held-out manifest is opened. The held-out panel covers 12 of the 13 target apps (one has a single template and is used only for adaptation).

## Where the evidence is thinner, in the paper’s words

- Context-Only TTA and CoAdapt-GUI “are run independently and can therefore collect different policy-dependent trajectories; their difference reflects the complete joint procedure, not a controlled estimate of the LoRA update alone.”
- The nominal 50-update schedule in Setting 1 “should not be interpreted as an identical gradient or compute budget across methods”, because context revision and policy optimization use different update operators.
- The Setting 1 Base Policy and Policy-Only TTA values were “not reproduced in our environment”.
- Table 2 gives no standard deviation, and the five-run statement in the appendix is for Setting 1. Evaluation sets are small: 48 instances over five apps, and 105 episodes.
- In Setting 1 the evaluation templates are the same as the adaptation templates (new instances only), and in Setting 2 the target apps are used for adaptation; “held out” refers to instances or templates, not to the app.

## CUA Radar’s read

CUA Radar scores this paper **80 (three stars)**, evidence level **transfer**. The record credits online evaluation with a programmatic evaluator, held-out apps and templates, variance over five runs (Setting 1), baselines with the same adaptation tasks and rollout budget, cost reporting (9–10 GPU-hours per adaptation run), and a component ablation. No judgment flags are recorded, and no code link is stated. The radar did not rerun any experiment; every number here comes from the paper (version v1).
