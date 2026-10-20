# Behavior Judge: run many desktop-agent rollouts, narrate each one, pick the best by comparison

*A CUA Radar reading of arXiv 2510.02250v2 (Gonzalez-Pumariega, Tu, Lee, Yang, Li, Wang). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2510.02250v2*

## The problem: running many attempts is easy, knowing which one worked is not

A computer-use agent can succeed on one attempt at a task and fail on the next, because small errors compound over dozens of steps. The paper calls scaling inside a single rollout (for example step-wise best-of-N, where a judge picks among candidate actions at each step) limited, since it commits to the agent’s current plan. Its alternative is wide scaling: generate several full rollouts in parallel and select one. The authors point out that different agents succeed on different tasks, so the upside is real, but the bottleneck is evaluation. In their words, “generating multiple rollouts is straightforward, \[but\] reliably determining which long-horizon trajectory is correct is not”: trajectories are dense and multimodal, most detail is irrelevant to success, and many tasks admit several valid solutions that scripted checkers may not recognise.

## What BJudge and Agent S3 are

The agent works on desktops. It sees screenshots and acts through calls such as `agent.click(...)` and `agent.type(...)`, or hands a step to a coding agent that runs Python or Bash in a sandboxed VM. The coding agent is enabled on OSWorld and WindowsAgentArena and disabled on AndroidWorld, where the emulator does not allow program execution. The paper builds a stronger base agent, **Agent S3**, from Agent S2 by removing the manager-worker hierarchy (a flat policy that can replan at any step) and adding the coding agent. On the CUA Radar board the method sits in the “simulated lookahead and selection” family, sub-pattern K02, verifier reranking.

**Behavior Judge (BJudge)** has two components.

1.  **Behavior narrative generation.** For every step, a VLM sees the screenshot before the action, the action, and the screenshot after it (taken 3 seconds later to catch delayed effects) and writes the task-relevant facts. For pointer actions the generator gets a marker at the click point and a zoomed crop of the result, because those steps are where hallucination is most likely. A narrative keeps the first screenshot, the per-step facts and the last screenshot.
2.  **Comparative evaluation.** A VLM receives all narratives in one multiple-choice prompt that asks it to cite and contrast facts, and answers with the index of the rollout to submit. The authors chose a single round over tournament-style comparison for token cost and speed.

The supervision signal is therefore the judge’s own comparison; no weights are trained. The best configuration uses 5 rollouts each from GPT-5 and Claude Opus 4.5, with Opus writing the facts and GPT-5 selecting.

## Results, as reported

OSWorld, 361 tasks, 100-step budget, success rate (%). All numbers are online execution scored by the benchmark’s scripts.

| Method                       | Model                  | Success  |
|------------------------------|------------------------|----------|
| Agent S2                     | GPT-5                  | 48.8     |
| CoAct-1                      | OAI CUA + o3 + o4-mini | 59.9     |
| Agent S3                     | GPT-5 Mini             | 49.8     |
| Agent S3                     | GPT-5                  | 62.6     |
| GTA1 (step-wise scaling)     | GPT-5                  | 63.4     |
| Agent S3 + WebJudge (N=10)   | GPT-5 Mini             | 50.4     |
| Agent S3 + BJudge (N=10)     | GPT-5 Mini             | 60.2     |
| Agent S3 + BJudge (N=10)     | GPT-5                  | 69.9     |
| **Agent S3 + BJudge (N=10)** | GPT-5 + Opus 4.5       | **72.6** |

The paper reports 72.6 as a 9.2-point absolute gain over the previous best of 63.4, and above the human level it cites, 72.36. Agent S3’s 62.6 is averaged over 10 runs. On other benchmarks with N=3: WindowsAgentArena 56.6 at 100 steps against 50.2 for Agent S3, and AndroidWorld 71.6 against 68.1. Agent S3 itself, compared with Agent S2 under GPT-5, uses 35.12 LLM calls per task against 73.62 and 891.21 seconds against 2366.80.

## What the paper’s own controls say

**Equal rollout budgets.** The WebJudge baseline is the authors’ adaptation: it scores each trajectory independently from 1 to 5 and takes the highest. With GPT-5 Mini rollouts it improves slightly near N=4, then plateaus and drops around N=10, while BJudge keeps scaling.

**Representation.** With the same 10 GPT-5 Mini rollouts: behavior narratives 60.2, naive per-screenshot captions 56.8, screenshots only 56.0, trajectory summary 55.0 (a 3.4-point improvement over the best baseline).

**Judge accuracy.** On the 159 tasks where at least one rollout is right and one is wrong, BJudge picks the script-correct rollout 78.4% of the time, and 92.8% when the remaining cases are checked by a human; over the full set the figures are 69.9% and 76.3%. Of the 12 failures reviewed, 8 were narrative hallucinations and 4 were code-to-GUI handoff failures.

**Resources and ensembles.** At small total budgets a single agent is best. BJudge with N=4 beats a single agent by 4.25 points at twice the budget (200), and the largest gain, 6.38 points, appears at N=10 with a budget of 1000. In the mixture study, GPT-5 + Opus reaches 71.6, and the most diverse mixture has the highest task coverage, 80.5.

**Cost.** Per task with GPT-5: 0.72 USD for a rollout, 0.11 for narrative generation and 0.03 for judging over 10 rollouts; the full N=10 run took 17 hours 33 minutes.

## Where the evidence is thinner, in the paper’s words

- Table 1’s caption says the 72.6 ensemble was “chosen from Table 5”, a comparison run on OSWorld itself, and Table 5 lists GPT-5 + Opus at 71.6 for N=4 rollouts, so the headline combines a benchmark-informed choice with a larger N.
- Variance for the BJudge numbers is not reported; only Agent S3’s 62.6 is stated as an average over 10 runs.
- The judge is checked against OSWorld scripts, which the paper says “can only strictly evaluate one pre-defined solution”; the 92.8% figure rests on the authors’ own manual inspection.
- The method “assumes access to an agent capable of producing multiple independent rollouts from the same initial state”; live desktops or shared online state can break that assumption.
- The paper text contains no link to a code repository.

## CUA Radar’s read

CUA Radar scores this paper **68 (★★)**, evidence level **transfer**. The record credits online evaluation, transfer to WindowsAgentArena and AndroidWorld, strong baselines, equal rollout budgets, cost reporting, a representation ablation and a judge accuracy check, with no flags. Variance for BJudge and code are not recorded as reported. The radar did not rerun any experiment; every number here comes from the paper (version v2).
