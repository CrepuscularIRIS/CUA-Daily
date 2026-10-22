# ScaleCUA: synthesising verifiable GUI tasks, then training a 9B desktop agent with online RL

*A CUA Radar reading of arXiv 2607.11185v1 (Lv, Liu, Ren, Lai, Jing, Zhang, Zhao, Yao, Tang, Dong). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2607.11185v1 · Code: https://github.com/THUDM/SCALE-CUA*

## The problem: no scorer, wasted rollouts, slow multi-turn training

The paper argues that online reinforcement learning with verifiable rewards (RLVR) for computer use agents is held back by two things. The first is data. A verifiable GUI task is one paired with a deterministic judge function (a filesystem check, a browser-state inspection, a piece of Python) that scores the final environment state without human or LLM judgment. Unlike math or code, a GUI task comes with only a live environment and an instruction, so the judge must be built. Tasks must also be neither trivial nor out of reach: under GRPO, a task the model always solves or always fails gives zero within-group advantage and wastes the rollout group.

The second is training efficiency. Uniform sampling often yields batches with no learning signal, and packaging trajectories is a trade-off: one item per trajectory accumulates all screenshots and slows rollouts, while one item per turn (step-wise) makes the item count grow with the number of turns.

## What ScaleCUA is

The agent works from screenshots only; the appendix states that it uses no accessibility trees or privileged environment state for perception. It acts through the benchmark’s computer-action interface: mouse actions parameterised by (x, y) on a relative 1000×1000 grid rescaled to the screen, keyboard actions, scroll, and wait. ScienceBoard adds done, answer and write_file. The platform is Ubuntu desktops in docker containers. The recipe is applied to GLM-4.6V-Flash, Qwen3-VL-8B-Thinking and Qwen3.5-9B. On the CUA Radar board the architecture pattern is K13, “synthesise tasks from checkers so that verifiable reward exists by construction”.

The pipeline: train on an initial VeriGen pool, collect rollouts and let VeriGen refine them into an RL pool, then run online RL with the two training components below.

1.  **VeriGen (task and judge synthesis).** Three LLM agents interact with live docker containers. A proposer writes a task and its verifier from environment knowledge documents. A judger reviews statically (is the instruction unambiguous, is the verifier sound). A checker does a dry run in the container to test that the goal is reachable and the verifier scores the final state correctly. A shared docker probe lets 100+ workers run against 100+ containers. In trajectory-guided mode, VeriGen reads the trained model’s rollouts and pass rates: for failed tasks it finds the earliest step where the model deviates and splits the task into easier subtasks; for solved tasks it clusters similar tasks in one application and chains them into harder multi-objective ones. The output is 24K+ verifiable tasks and nearly 3K RL tasks.
2.  **Frontier Sampling.** Each task keeps an exponential moving average of its success rate (alpha = 0.2). A Gaussian weight peaks at a target success rate (mu = 0.5, sigma = 0.25), steering rollouts to tasks near the model’s frontier; 20% of each batch is sampled uniformly from outside that pool.
3.  **Visual Context Segmentation.** A sliding window keeps the last K screenshots (K = 5 for OSWorld, 8 for ScienceBoard). On overflow, the current token-ID stream is saved as a training item, the oldest screenshots are dropped and the history is re-tokenized with a zero loss mask, so earlier turns only serve as context. This gives O(nT/K) items rather than O(nT) for step-wise training.

The training signal is the Python judge’s reward on the final state (binary for all-or-nothing tasks, dense when sub-goals exist), optimised with GRPO, DAPO-style clipping and a KL penalty. Episodes are capped at 50 turns.

## Results, as reported

Everything below is online success rate (%), up to 50 steps on OSWorld. ScaleCUA numbers are means over 4 independent rollout passes per task, with standard deviations of 0.5 to 1.2 (OSWorld) and 0.5 to 2.8 (ScienceBoard).

| Model                                            | OSWorld  | ScienceBoard |
|--------------------------------------------------|----------|--------------|
| Kimi K2.5 (best open-source baseline on OSWorld) | 63.3     | not reported |
| Claude Sonnet 4.5 (proprietary)                  | 62.9     | not reported |
| Claude Opus 4.6 (proprietary)                    | 72.7     | 52.7         |
| Qwen3.5-9B (base, technical report)              | 41.8     | not reported |
| ScaleCUA-GLM-4.6V-Flash                          | 66.5     | 49.4         |
| ScaleCUA-Qwen3-VL-8B                             | 67.7     | 51.9         |
| **ScaleCUA-Qwen3.5-9B**                          | **68.7** | **54.0**     |

The paper states that the Qwen3.5-9B model surpasses Kimi K2.5, Claude Sonnet 4.5 (62.9) and Seed-1.8 (61.9) on OSWorld and Claude Opus 4.6 on ScienceBoard; GPT-5.4 (75.0) and Claude Opus 4.6 (72.7) are listed above it on OSWorld, and the human figure is 72.4. All three models improve over their bases; the example given is Qwen3.5-9B, 41.8 to 68.7 (+26.9 as printed). The paper has no offline numbers.

## What the paper’s own controls say

**Component ablation (OSWorld, Qwen3.5-9B).** Full ScaleCUA scores 68.7; without Frontier Sampling 63.7, without Visual Context Segmentation 62.2, and without VeriGen 43.9, which the paper labels the base score.

**Sampler baselines.** Frontier Sampling is compared with uniform sampling, DAPO and curriculum learning only as training-reward curves (Figure 6a), with no table of numbers.

**Window size.** Pass@1 on OSWorld peaks at 58.9 for K = 5 (56.4 for K = 1, 56.8 for K = 15). In a one-task case study with 8 rollouts per setting, K = 5 passes 7 of 8, K = 3 passes 5 of 8, and K = 1, 8 and 15 pass none.

**Training speed.** On Qwen3.5-9B with batch size 32 and rollout-n = 8, other hyperparameters and compute fixed, K = 5 cuts the per-step time from 750 s to 265 s (2.83x; actor phase 485 s to 154 s). This is a training-time measurement, not an evaluation score.

**Judge quality.** The full multi-agent loop gives a 94.5% executable rate for generated judges; removing the LLM Judge Agent gives 62.3, the Fix Agent 78.1, and the Rule Validator 86.2. An expert audit of 160 trajectories (10 per application domain) finds that the executable judge agrees with human labels in 82.5% of cases: 78.0% on OSWorld and 90.0% on ScienceBoard, with 11 false positives and 17 false negatives.

**Trajectory-guided tasks.** Adding them to the RL pool raises the OSWorld score from 64.6 to 68.7.

**Overlap with evaluation tasks.** The appendix audit of training subsets against benchmark pools finds no exact instruction duplicates, near-duplicate objectives in 0.19% (OSWorld) and 0.36% (ScienceBoard) of tasks, and exact judge reuse of 2.10% on OSWorld (generic templates) and 0.00% on ScienceBoard.

**Cost.** Synthesis averages 221.7 seconds end to end and 0.93 to 1.01 USD per accepted task; the main RL runs use 8 nodes of 8 H800 GPUs.

## Where the evidence is thinner

- The tasks are synthesised in the same OSWorld and ScienceBoard environments that are used for evaluation: “The generated tasks span all 10 OSWorld application domains and all 6 ScienceBoard scientific domains”. The overlap audit is the paper’s answer; the apps themselves are not held out.
- The base score is 43.9 in the ablation table and 41.8 for Qwen3.5-9B in the main OSWorld table (marked as taken from a technical report). The paper does not reconcile the two.
- Judge-human agreement is 82.5%, so some decisions differ from experts; the human-valid rate in Table 6 is 73.1% overall and 58.3% on ScienceBoard.
- The sampler comparison has no numeric table, and each ablation row is a single OSWorld score without a standard deviation.
- The authors list three limitations: the 50-turn cap, Ubuntu-only desktops, and validation on 8B to 9B models only.

## CUA Radar’s read

CUA Radar scores this paper **76 (★★★)**, evidence level **online**. The score reflects online evaluation on two benchmarks, 4-pass standard deviations, sampler baselines, cost reporting, a component ablation, an expert judge audit and released code. The judgment record marks held-out environments and budget matching as partial, and flags that the generated tasks span the same domains that the benchmarks cover. The radar did not rerun any experiment; every number here comes from the paper (version v1).
