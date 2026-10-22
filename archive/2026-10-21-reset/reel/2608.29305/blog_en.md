# TTED: a web agent that splits each page into a sub-goal and a sub-observation, then learns from its own judgments

*A CUA Radar reading of arXiv 2608.29305v1 (Li, Liu, Huang, Li, Liu, Yan, Liu). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.29305v1 · Code: https://github.com/THUNLP-MT/TTED*

## The problem: easy parts, cluttered page

Real websites put several functional pieces on one screen: search panels, form fields, content containers, modal windows. The paper’s starting point is that an agent which handles each piece alone can still fail when they appear together. It measures this on CompWoB+, an extension of CompWoB that the authors built with a task generator (10 base tasks, composed 3 to 8 at a time, 100 tasks per size, 600 in total). With Qwen3-8B the success rate falls from 85% at 3 components to 19% at 8; with GPT-4o-mini it falls from 97% to 46%. The paper names two reasons this also hurts test-time learning: exploration succeeds less often in cluttered pages, and the agent’s self-assessment becomes less accurate.

## What TTED is

TTED (Test-Time Environment Decomposition) is a web agent that learns without ground-truth labels. At each step the agent sees the task goal, the current observation (an accessibility tree on WebArena and WorkArena via BrowserGym, raw DOM on CompWoB+) and a history of step summaries. It acts through BrowserGym actions, or `clickxpath` / `type` actions on CompWoB+. On the CUA Radar board it sits in pattern C13, structured screen observation.

What is new is an explicit trial step with four sub-steps, all done by the same LLM:

1.  **Decompose.** Predict a localized sub-goal from the goal, observation and history, then extract the task-relevant part of the observation as a sub-observation. Together they form a “sub-environment” that keeps the original action space and dynamics.
2.  **Act.** Generate the action from the sub-goal, sub-observation and history.
3.  **Self-assess.** The same model acts as a generative reward model: it scores the sub-goal and sub-observation from 0 to 5 and marks the action pass or reject. A pass needs the decomposition scores above a threshold and an accepted action; a reject triggers a retry (up to 3 attempts in the ICL setup).
4.  **Summarize.** A passed step is summarized and added to the history.

Then the agent learns from this experience in one of two ways. With in-context learning (ICL), used on CompWoB+, only passed steps are kept as demonstrations for the final run; for static pages the check is strengthened with Selenium and model-written JavaScript. With RL, used on WebArena, both passed and rejected trials are kept, the scores are mapped to a return in \[-1, 1\], and an off-policy REINFORCE-style update with batch-level advantage normalization (from REINFORCE++) trains the decomposition and the action policy together. At evaluation the self-assessment is removed and the agent runs in the full environment.

## Results, as reported

All results below are online task success (%) with Qwen3-8B. The WebArena figures use 561 of the 812 tasks (the Reddit tasks were dropped because the environment did not run reliably), graded with GPT-5-mini fuzzy matching instead of GPT-4o-Turbo; the grader is not used as a reward. WorkArena is not trained on. Up to 15 steps per task.

| Method                  | \#Sub-envs | WebArena | WorkArena    |
|-------------------------|------------|----------|--------------|
| Qwen3-8B, no adaptation | 0          | 12.1     | 18.2         |
| SFT with ground truth   | 3200       | 14.1     | 17.9         |
| RL with ground truth    | 3200       | 14.8     | 17.3         |
| TTRL                    | 3200       | 13.5     | not reported |
| TTT (SFT)               | 3200       | 11.2     | 18.2         |
| TTT (RL)                | 3200       | 12.5     | 17.3         |
| TTED (SFT)              | 3200       | 17.6     | 21.8         |
| TTED (RL)               | 800        | 19.4     | not reported |
| **TTED (RL)**           | 3200       | **21.0** | **22.7**     |

On CompWoB+ (ICL, 100 tasks per size), TTED lifts the 8-component success rate from 19% to 61% for Qwen3-8B and from 46% to 88% for GPT-4o-mini. All of these are online; the paper has no offline step-accuracy benchmark.

## What the paper’s own controls say

**Ablation.** On WebArena with the same RL budget: full TTED 21.0, without sub-observation decomposition 15.0, without sub-goal decomposition 12.4, without both 12.5 (which is the TTT baseline). The paper reads the sub-goal drop as agents being disoriented without localized objectives.

**Baselines and budget.** Test-time baselines use the same budget of sub-environments. TTED at 800 sub-environments (19.4) already exceeds RL with ground truth at 3200 (14.8). In the scaling table TTT stays near 13 while TTED rises with budget, and the authors report that advantage normalization matters: with plain REINFORCE TTED gets 17.6, with GRPO 17.8.

**The judge.** On 82 WebArena tasks, agreement with human reward labels (normalized AD) is 0.85 for TTED, 0.68 for TTRL’s self-consistency labeling and 0.71 for TTT’s judge. Two annotators agreed with each other at a Cohen’s kappa of 0.85.

**Cost.** Average steps per task go from 4.72 (base) to 8.29, while prompt tokens per action fall from 6338.9 to 3948.2. GPU hours on 8 A100-80GB are 14.80 for TTED against 14.40 for TTT and 8.67 for RL with ground truth; the paper states TTED “trades additional exploration costs for more effective adaptation rather than being cost-free.”

**Another model size.** With Qwen3-14B on WebArena: base 19.3, RL with ground truth 20.0, TTT 18.7, TTED 22.5. The paper’s one-sided tests give p = 0.093, 0.153 and 0.061 for these gains, so they are positive but not significant at the usual levels.

**Repeats.** The main WebArena results were repeated three times, with absolute variation below 0.5%. The 95% Wilson interval for TTED is \[17.9, 24.6\] against \[9.7, 15.1\] for the base model.

## Where the evidence is thinner, in the paper’s words

- Adaptation and evaluation share the same tasks. The paper describes RL as adapting “once on WebArena” and evaluating “on the same benchmark distribution”; only WorkArena is evaluated without further training. This is a transductive, label-free setup, not a held-out one.
- The reward signal is the agent’s own judgment. The paper’s limitations say it “introduces potential bias and noise inherited from the backbone model itself”; the human check above covers 82 tasks and reports agreement, not false-positive and false-negative rates.
- On CompWoB+ the goal decomposition is given the names of the base tasks that make up the dataset (Appendix E).
- The WebArena subset has 561 tasks, a final checkpoint was taken without mid-training WebArena tests, and the remaining failures are said to come mostly from action-space misalignment or overthinking. The authors call TTED “a foundational prototype rather than a production-ready system”.
- Larger proprietary models are listed for context only: GPT-4o 23.5, and GPT-5.5 67.3 on full WebArena-Verified with different verifiers.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **transfer**. The record credits online evaluation, WorkArena transfer without further training, matched training budgets, cost reporting, a component ablation and a human check of reward labels. It flags that the judge’s false positives and negatives are not checked and that the method adapts on the tasks it is tested on. Variance and code are marked unclear in the record, although the paper reports repeated runs in the appendix and links a repository. The radar did not rerun any experiment; every number here comes from the paper (version v1).
