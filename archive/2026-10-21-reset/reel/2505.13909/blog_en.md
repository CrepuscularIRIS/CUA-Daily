# PC Agent-E: 312 human trajectories, plus nine Claude-sampled actions per step, for a Windows computer-use agent

*A CUA Radar reading of arXiv 2505.13909v2 (He, Jin, Liu; ICLR 2026 version). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2505.13909v2 · Code: https://github.com/GAIR-NLP/PC-Agent-E*

## The problem: trajectory data is scarce

The paper opens with the claim that scaling up high-quality trajectory data has long been a critical bottleneck for human-like computer use agents. Open-source models lag proprietary ones such as Claude 3.7 Sonnet, and real human demonstrations are expensive to collect. The authors ask how far a very small set of human trajectories can go if a frontier model is used to enrich it, rather than to replace it. They compare against two alternatives: training on the human trajectories alone, and directly distilling end-to-end trajectories from Claude.

## What PC Agent-E is

The agent is a native, screenshot-only model: at each step it receives the task description, the current screenshot and a textual log of its previous thoughts and actions (past screenshots are deliberately left out), and it outputs a thought followed by one action in the ReAct style. Actions are coordinate based (click, right click, double click, drag, scroll) plus key presses, hotkeys, typed text, wait, finish and fail, and are executed through PyAutoGUI. The platform is Windows desktop, with 1280 x 720 screenshots. The architecture pattern on the CUA Radar board is C21, trajectory-level policy training. The base model is Qwen2.5-VL-72B.

The training pipeline has four parts:

1.  **Trajectory collection.** Two annotators recorded 312 Windows trajectories in one day with PC Tracker, at roughly 3 minutes each. Tasks were seeded by hand and expanded with LLMs. Rule-based filters removed bad steps and trajectories, and tasks were decontaminated against the evaluation benchmark (zero 13-gram overlap, under 0.7 3-gram overlap, cosine similarity under 0.85). No further verification was done, on the grounds that humans are proficient and could discard or re-describe tasks.
2.  **Thought completion.** Claude 3.7 Sonnet reconstructs the implicit thought behind each human action from the task, the history, the action and the screenshot.
3.  **Trajectory Boost.** Each human step is treated as an environment snapshot (task, observation, human history). Claude 3.7 Sonnet, instantiated in the PC Agent-E scaffold, samples 9 alternative (thought, action) decisions per snapshot. These are not executed in any environment. The result is a “Traj Tree”: the human trajectory is the trunk and the sampled decisions are leaves.
4.  **Agent training.** Every node becomes one training sample, and its history contains only the prior human steps on the trunk. This gives 27K samples from the 312 trajectories. The model is fine-tuned with SFT for 2 epochs on 32 GPUs in about 5 hours.

The training signal is therefore supervised imitation of human and Claude-sampled actions with reconstructed thoughts. There is no reward model, verifier or reinforcement learning. The paper defines a data scaling factor s as the ratio of actions used in training to actions in the human trajectory; s = 1 is human data alone and the final model uses s = 9 + 1 = 10.

## Results, as reported

All evaluations are online, VM-based success rates, with a 30-step limit by default. The paper builds WindowsAgentArena-V2, 141 tasks across 11 Windows applications derived from WindowsAgentArena. The changes include restoring a VM snapshot before each evaluation, fixing evaluation functions, and removing the infeasible tasks, because an agent that always outputs FAIL can score on them. The paper does not state the number of runs or seeds, and reports no standard deviations.

| Model (success %, online)    | WindowsAgentArena-V2 | OSWorld (369 tasks) |
|------------------------------|----------------------|---------------------|
| Qwen2.5-VL-72B (base)        | 14.9                 | 11.1                |
| UI-TARS-72B-DPO              | 26.2                 | n/r                 |
| Claude 3.7 Sonnet            | 32.6                 | n/r                 |
| Claude 3.7 Sonnet (thinking) | 35.4                 | n/r                 |
| **PC Agent-E**               | **36.0**             | **14.9**            |

n/r: not reported in the paper.

The abstract and Section 5.2 state a 141% relative improvement over the base model and 10% in relative terms over the teacher, Claude 3.7 Sonnet. On the original WindowsAgentArena, Appendix B reports 27.9 for PC Agent-E against 19.5 for NAVI, a GPT-4V plus Omniparser framework. A Qwen2.5-VL-7B model trained on the same 27K samples goes from 5.0 to 6.4 on WindowsAgentArena-V2, a smaller gain that the authors tie to the small model’s knowledge and grounding limits.

On OSWorld (Linux), after Windows-only training, the paper reports a 34% relative improvement. The feasible and infeasible subsets tell different stories: PC Agent-E scores 10.9 on 339 feasible tasks against 4.4 for the base model, but 63.3 on 30 infeasible tasks against 86.7 for the base model. The authors read this as the “infeasible hacking” they describe in Section 4.

There are no offline step-accuracy or grounding benchmarks in the paper; everything above is online.

## What the paper’s own controls say

**Human data alone.** Training on the human trajectories only (s = 1) moves the base from 14.9 to 17.2, against 36.0 for the full method.

**Direct distillation at matched count.** The authors sampled 10 end-to-end Claude trajectories for each of the 312 tasks, 3,120 in total, and trained with the identical procedure. That baseline reaches 26.2 (Appendix D). Combining the 312 human trajectories with 9 x 312 distilled trajectories gives 26.9. Both are well under 36.0. The paper’s explanation is that single-step augmentation on real human states avoids the error accumulation of end-to-end distillation.

**Cost.** Collecting the same number of trajectories (3120) took about 900 hours for the distillation baseline, which needs Claude to run in virtual machines, and 3 hours for Trajectory Boost under the same hardware, the “300-fold speedup” the paper states.

**Where the gain comes from.** In a review of 50 trajectories that the base model failed and PC Agent-E solved, the authors find that the improvement comes mainly from planning (longer thoughts, more verification and self-correction), and they saw no significant gains in knowledge or grounding.

**Step budget.** With 15, 30 and 50 steps, PC Agent-E scores 26.9, 36.0 and 31.4, and the base model 11.3, 14.9 and 11.9. Both decline at 50 steps. The paper attributes this to missing termination awareness, since over 90% of the training trajectories have fewer than 15 steps, and describes the method as supporting near-distribution test-time scaling only.

## Where the evidence is thinner, in the paper’s words

- The number of runs is not stated and no variance is reported. The main benchmark has 141 tasks.
- WindowsAgentArena-V2 is a benchmark the authors built from WindowsAgentArena, and infeasible tasks are removed as, in their words, “a temporary solution”.
- The 7B result is a small gain: “the gains are not as significant as those observed with the 72B model”.
- Performance degrades at 50 steps, and the paper leaves longer-horizon training and explicit termination supervision to future work.
- The scaffold deliberately omits past screenshots; the authors believe image history would help but did not test it.
- On OSWorld, the overall gain coexists with a lower score on infeasible tasks.

## CUA Radar’s read

CUA Radar scores this paper **72 (★★★)**, evidence level **transfer**. The score reflects what the paper reports: online evaluation, a held-out operating system (OSWorld on Linux after Windows-only training), strong baselines, a budget-matched distillation comparison, cost reporting, ablations over data source and scale, and released code, models and data. The judgment record marks variance as unclear (no run count or spread reported) and records no anti-pattern flags. The radar did not rerun any experiment; every number here comes from the paper (version v2).
