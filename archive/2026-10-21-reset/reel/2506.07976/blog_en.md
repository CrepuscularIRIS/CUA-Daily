# TTI: a web agent that scales test-time interaction instead of per-step thinking

*A CUA Radar reading of arXiv 2506.07976v2 (Shen, Bai, Zhang, Zhou, Setlur, Tong, Caples, Jiang, Zhang, Talwalkar, Kumar). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2506.07976v2 · Code: https://github.com/test-time-interaction/TTI*

## The problem: thinking longer is not the only dial

Test-time scaling today mostly means generating longer reasoning traces before each response. For an agent acting in a web environment, the paper argues this is the wrong (or at least incomplete) dial: longer per-step thinking “does not allow agents to acquire new information from the environment or adapt their behavior over time.” Each extra interaction step, by contrast, returns new observations — listings not yet seen, prices that changed, a pop-up that blocks the path. The paper proposes interaction scaling — increasing the number of steps an agent may take — as a complementary axis of test-time scaling, and asks two questions: does acting longer beat thinking longer under a fixed token budget, and can training (not just prompting) teach an agent to use the extra steps well?

## What TTI is

The agent is a multimodal web agent built on Gemma 3 12B. At each step it observes the task goal, the current URL, the accessibility tree, and a screenshot with a set-of-marks overlay that numbers every clickable element; the observation history is truncated to the most recent three observations, but the agent keeps all of its past actions. Its action space is six discrete primitives: click, type, scroll, go back, search (Google or Bing), and stop with an answer. Platforms are desktop web: WebArena’s self-hosted sites (shopping, CMS, Reddit, GitLab, maps) and WebVoyager’s real websites. On the CUA Radar board the paper sits in the trajectory-level policy training family, sub-pattern K20: online RL on the agent’s own trajectories with sparse terminal reward.

The paper first runs a prompting-only study on a 62-task WebArena subset (3 runs, test-time limit of 30 steps). A “check-again” mechanism — after the agent signals completion, prompt it to reconsider — improves task success from 23% to at least 28% on WebArena, while spending the equivalent compute on budget forcing (“wait and think again”) or per-step best-of-n yields less than a 3% gain. One check-again pass averages 26.14 against a 23.81 chain-of-thought baseline; action-only prompting gets 14.76. But repeated re-checks can confuse the agent into revising correct answers, so prompting alone is insufficient.

TTI (Test-Time Interaction) then trains the horizon. It is online filtered behavior cloning (filtered BC, in the online STaR / REINFORCE family): sample rollouts on synthetic tasks, keep only those the judge marks successful, and maximize the likelihood of their actions. The core design is a curriculum on the rollout horizon, h_i = clip(h_min · i, h_max) with h_min = 10 and h_max = 30 — a multiplicative schedule that the paper’s ablation prefers over an additive one. Successful rollouts go into a replay buffer weighted by recency. Training tasks are synthetic, generated PAE-style by an exploratory agent that browses websites and proposes grounded tasks: 128K tasks across real-world domains for WebVoyager, 11K for WebArena’s self-hosted domains, with a separate agent trained per benchmark. The training signal is binary task success from a prompting-based verifier (Gemma 3 27B) that reads action histories and screenshots; on WebArena it reaches 88.9% agreement with the ground-truth evaluator. Training uses 512 rollouts per iteration (12 iterations for WebVoyager, 10 for WebArena) on NVIDIA H100 GPUs with vLLM sampling and DeepSpeed Zero 3.

## Results, as reported

All numbers are online task success rates (%); evaluation uses the original benchmark evaluators (the judge is used for training only), with an evaluation horizon of 30 steps. The main tables report no seeds or variance. Base model for the bottom four rows is Gemma 3 12B in all cases.

| Method (WebVoyager, 427 tasks)             | Average SR |
|--------------------------------------------|------------|
| PAE-LLaVa-34B (open data)                  | 33.0       |
| Gemma 3 12B zero-shot                      | 55.8       |
| Fixed h = 10 (same base)                   | 59.1       |
| Fixed h = 30 (same base)                   | 45.2       |
| **TTI (Gemma 3 12B)**                      | **64.8**   |
| UI-TARS-1.5 (private human-annotated data) | 84.8       |
| Claude 3.7                                 | 84.1       |
| OpenAI CUA                                 | 87.0       |

| Method (full WebArena, 812 tasks)             | Average SR |
|-----------------------------------------------|------------|
| NNetnav (Llama 3.1 8B)                        | 7.2        |
| AutoWebGLM (ChatGLM3 6B)                      | 18.2       |
| Gemma 3 12B zero-shot                         | 18.3       |
| Fixed h = 30 (same base)                      | 19.0       |
| AgentTrek / Learn-by-Interact (Codestral 22B) | 22.4       |
| Fixed h = 10 (same base)                      | 23.8       |
| **TTI (Gemma 3 12B)**                         | **26.1**   |
| IBM CUGA (proprietary)                        | 61.7       |

The paper states TTI improves over the non-fine-tuned agent by 9% (WebVoyager) and 8% (WebArena; 7.8 in Section 6.3), beats fixed h = 10 by 5.7 and fixed h = 30 by 19.6 on WebVoyager, and takes the best score in 8 of 13 WebVoyager domains. There are no offline step-accuracy numbers in the paper.

## What the paper’s own controls say

**Same-base fixed horizons.** Every TTI comparison above holds the base model fixed; training at a fixed short horizon (h = 10) caps exploration, while fixed long horizons learn slowly — the h = 5 agent overfits and terminates prematurely, and the h = 20 agent initially rewards aimless exploration before recovering.

**Budget-matched comparison.** Plotting success against total tokens per trajectory, interaction scaling shows the steepest trend; budget forcing plateaus around 0.26 and best-of-n brings the least improvement despite the highest cost.

**Curriculum ablation.** On the WebArena subset after 10 iterations: additive curriculum 29.50, multiplicative 32.25. TTI also beats the fixed h = 20 run by nearly 3% with 40% fewer training steps.

**Judge validation.** The 27B prompting-based verifier agrees with WebArena’s ground-truth evaluator on 88.9% of cases, and is used only for training; evaluation uses the benchmark’s own evaluators.

**Learning dynamics.** Under TTI the trajectory length first shrinks, then grows as the horizon expands; GoBack and Bing-search actions increase; and tokens per step decrease — the agent trades per-step reasoning for more steps, which the paper reads as adaptive exploration.

## Where the evidence is thinner, in the paper’s words

- No seeds or variance are reported for the main tables; the prompting and ablation numbers are averages over 3 runs on a 62-task subset.
- Held-out environments are partial: the radar record notes the synthetic tasks span “diverse real-world domains” that include the benchmark’s own websites for WebVoyager.
- WebArena gains are smaller, “possibly because: (1) WebArena tasks are more complex… (2) Agents occasionally attempt actions that are valid in real-world domains but invalid in WebArena counterparts.”
- Some domains regress: on Amazon and GitHub, “TTI can engage in exploration behaviors such as initiating Bing searches or consulting external sites,” which “exposes the agent to noisy or distracting information.”
- Failure modes: “over-reliance on resets” (Bing as a universal fallback) and “limited self-verification” — the agent can acknowledge a criterion mismatch and still submit the wrong answer.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**. The score reflects what the paper reports: online evaluation on full WebVoyager and WebArena with original evaluators, same-base fixed-horizon baselines, a token-budget-matched comparison, cost reporting, curriculum ablations, a judge validated at 88.9%, and code announced with the data. The record marks variance as not reported and held-out environments as partial, and flags no anti-patterns (AP5 and AP8 checked). The radar did not rerun any experiment; every number here comes from the paper (version v2).
