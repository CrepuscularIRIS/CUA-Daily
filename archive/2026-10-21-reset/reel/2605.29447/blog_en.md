# RoTS: growing a trajectory tree so a GUI agent learns to recover from its own mistakes

*A CUA Radar reading of arXiv 2605.29447v1 (Bu, Liu, Chen, Jiang, Li, Duan, Jiang, Hu, Yang, Zhang; Alibaba Cloud Computing). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2605.29447v1 · Code: https://github.com/AlibabaResearch/RoTS*

## The problem: agents trip over their own errors

GUI agents routinely make what the paper calls policy-induced errors: mistakes produced by the agent’s own actions, such as wrong grounding, a misread screen, or a wrong sub-goal. The agent then sits in an erroneous state and fails. The authors argue that robustness to such errors is under-emphasized in both evaluation and training, and name two gaps. The first is error coverage: benchmarks and training data over-represent low-level, human-made errors, while real failures are often compositional and high-level. The second is error horizon: existing protocols and reflection data are mostly short-horizon (an invalid click), while many real errors only become identifiable after several steps and need long-horizon backtracking. Agent frameworks usually add reflection or backtracking sub-agents rather than training the model itself to detect and recover.

The paper answers with two contributions: a benchmark, GUI-RobustEval, and a data-synthesis pipeline, RoTS (Robustness-driven Trajectory Synthesis).

## What RoTS is

**The agent.** The agent is a vision-language model that sees screenshots (plus its history, with at most 5 images kept) and emits a Thought followed by a PyAutoGUI action, in the AgentNet action space. It runs on real Ubuntu and Windows machines hosted in the cloud. Two models are trained, RoTS-7B and RoTS-32B, by supervised fine-tuning of Qwen2.5-VL-7B and Qwen2.5-VL-32B. On the CUA Radar board the pattern is K26 (trajectory-level policy training).

**Benchmark.** GUI-RobustEval has 1,216 executable test cases covering 11 error types at four error depths (d = 0, 1, 3, 5). Source material is 1.5k failed trajectories from 12 agents on OSWorld. Experts locate the root-cause step, assign an error type, and fix unrelated earlier mistakes so the prefix is clean. At test time the environment is reset to the state after the root-cause action plus d further steps, and the agent takes over. Two metrics are reported: Error-Awareness Rate (does the agent recognize the error at takeover, judged by a VLM) and Post-Error Success Rate (does it recover and finish).

**Synthesis.** For 20k online tasks the pipeline builds a replayable trajectory tree per task and policy. It starts with N = 4 parallel rollouts and then runs 32 rounds of explore-recovery co-expansion, giving 68 trajectories per task and policy. A reward model (WebJudge-style) splits the tree into successful and failed parts, and both are expanded:

- **Fragility-driven exploration (FDE).** A progress critic estimates how likely the policy is to propose a correct action at each node of the successful part. A UCB rule picks the most fragile node; the environment replays the prefix and the policy continues from there, to discover new failure modes.
- **Experience-informed recovery (EIR).** For failed trajectories, a reflector reads the experience extracted from sibling branches, marks candidate error states, and writes recovery advice. A UCB rule selects an error state, the environment replays to it, and a recovery actor continues conditioned on the advice.

Policies used for synthesis are OpenCUA-7B, UI-TARS-1.5-7B and Qwen3-VL-Plus; Qwen3-VL-Plus also serves as reflector and recovery actor.

**Training signal.** Whole trajectories are noisy, so a post-processing step keeps correct steps only: a VLM filter removes inconsistent replays, a progress critic and an action critic drop incorrect steps, and a reflection validator splits the rest into reflection-agnostic and reflection-related sets, followed by MinHash deduplication. Training is teacher-forced SFT on the assistant tokens. The final mixture is 800k samples, 720k reflection-agnostic and 80k reflection-related (a reflection share of 0.1). There is no reinforcement learning stage.

## Results, as reported

All results below are online: live OS environments, no offline step accuracy. OSWorld-Verified has 369 Ubuntu tasks. Models are tested at 15 and 50 maximum steps, averaged over 4 runs; All-Pass@4 is the fraction of tasks solved in all four runs. The dagger marks the authors’ own re-implemented runs.

| OSWorld success (%)   | Max 15    | Max ≥ 50  | All-Pass@4 (50) |
|-----------------------|-----------|-----------|-----------------|
| OpenCUA-32B           | 29.7      | 34.1      | 15.5            |
| Qwen3-VL-32B-Thinking | 28.1†     | 41.0      | 21.1            |
| Qwen3-VL-Plus (API)   | 33.1†     | 35.2†     | 24.5            |
| RoTS-7B               | 31.7†     | 36.3†     | 26.3            |
| **RoTS-32B**          | **42.8†** | **47.4†** | **33.8**        |

The same table lists proprietary Claude 4.5 Sonnet at 58.1 (max ≥ 50 steps), so the “state-of-the-art” in the abstract is best understood among open-weights models. Other rows: Qwen2.5-VL-32B 3.0 and 3.9, UI-TARS-72B-DPO 24.0 and 25.8, Qwen3-VL-8B-Thinking 29.2† and 33.9, GUI-OWL-7B 27.1 and 29.4. For RoTS-7B, the paper notes that raising the step budget from 15 to 50 adds 4.6%.

On WindowsAgentArena (154 Windows 11 tasks, max 50 steps) RoTS-7B reaches 28.2† and RoTS-32B 39.1†; Jedi-7B with GPT4-o is listed at 32.9, ScaleCUA-32B at 24.2 and UI-TARS-72B-DPO at 17.9.

On GUI-RobustEval (3 runs, up to 50 steps), RoTS-32B scores 49.7, 41.8, 36.5 and 33.2 post-error success at depths 0, 1, 3, 5, with 58.8% error awareness; RoTS-7B scores 43.5, 36.6, 30.1 and 26.7 with 51.9%. OpenCUA-32B scores 45.5, 37.2, 28.6 and 25.9 with 50.3%; Qwen3-VL-Plus 55.1, 46.1, 36.9 and 33.5 with 65.4%. The paper reports that RoTS shows the smallest drop from depth 0 to depth 5 among the open-source models (38% for 7B, 33% for 32B).

## What the paper’s own controls say

**Rollout strategy at equal budget.** On 5k online tasks with 100k SFT samples on Qwen2.5-VL-7B, all variants use a similar rollout budget. OSWorld success and All-Pass@4: parallel sampling only 18.1 and 8.6; plus FDE 19.6 and 9.1; plus EIR 19.5 and 12.1; both 21.4 and 14.1. The paper reads this as FDE mainly helping success and EIR mainly helping robustness.

**Data quality at equal size.** With 100k samples, human AgentNet data (reflection-agnostic only) gives 15.3 success and 7.8 All-Pass@4 on OSWorld; adding human reflection samples gives 16.1 and 8.4; swapping in RoTS reflection data gives 18.8 and 11.6; fully RoTS data gives 21.4 and 14.1.

**Reflection ratio, depth and scale.** The best reflection share is 0.1 (21.4 and 14.1); at 0.3 performance falls below the no-reflection setting, which the authors attribute to too much reflective data producing ineffective reflections. Capping recovery depth in the reflection data, the largest gain comes from moderate depth (≤ 5), where post-error success on GUI-RobustEval rises from 12.1 to 20.7; gains beyond depth 7 are small. Scaling the dataset from 50k to 1000k plateaus at 36.4 success, which the authors attribute to the current expansion setting (N = 4, 32 iterations).

**Judges.** The reward model WebJudge is reported at 90% agreement with humans, against 76.60% for a ZeroGUI-style voting judge; the progress and action critics reach 88.7% and 90.6% on 200 sampled steps; the error-awareness judge reaches at least 96% on 200 samples.

**Held-out tasks.** The 20k synthesis tasks are disjoint from all evaluation benchmarks at task and asset level; only base OS snapshots are shared.

**Cost.** Benchmark construction is about \$400; data synthesis on 20k tasks is about \$48,100 and about 16 days wall-clock.

## Where the evidence is thinner, in the paper’s words

- The paper reports means over 3 or 4 runs but no standard deviations or confidence intervals for the headline tables.
- Rows marked † are the authors’ re-implemented runs; the table does not mark the other rows that way, so evaluation setups may differ across rows.
- The pipeline relies on Qwen models: Qwen3-VL-Plus is a policy, reflector, recovery actor, critic and CoT generator. All authors work at Alibaba Cloud, and the paper discloses that the Qwen-VL series and RoTS were developed there.
- Failure cases include “over-reflection”: in one OSWorld example the agent misreads an incompletely rendered page and goes back twice unnecessarily. Per-type results show remaining bottlenecks in Fail to Terminate (17.4%) and Misunderstand Task Objective (24.1%) for RoTS-32B.
- Scaling saturates at the current expansion setting.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **online**. The score reflects what the paper reports: online evaluation on three benchmarks, task-level held-out synthesis data, matched rollout budgets for the rollout-strategy ablation, cost reporting, component ablations, a human-agreement check of the LLM-as-judge components, and released code. Variance across runs is not reported, and the judgment record flags no anti-patterns. The radar did not rerun any experiment; every number here comes from the paper (version v1).
