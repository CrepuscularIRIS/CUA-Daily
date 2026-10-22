# PEEU: a web agent that explores a site, then relabels its own trajectories as high-level tasks

*A CUA Radar reading of arXiv 2606.27330v1 (Men, Jin, Cao, Chen, Liu, Zhao; CASIA / UCAS). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.27330v1 · no code repository is listed in the paper.*

## The problem: what task should train a small web agent?

Small open-source multimodal LLMs are cheap and private, but, in the paper’s words, “they suffer from weak planning and limited cross-website generalization.” Two standard data recipes are criticized. Atomic-task methods extract click / type / scroll skills by comparing screenshots before and after an action; whether mastering those atomic skills composes into task planning is exactly what remains unclear. Coarse-task methods keep the exploration task as the training label and pair it with whatever trajectory came out; the paper’s example is a task requiring recipes over 4.5 stars while the collected trajectory only reaches 4 stars — the label and the trajectory are misaligned, and the constraints are weak because a homepage cannot know what the site actually contains (“such as ingredients and preparation directions”).

## What PEEU is

The agent is a visual web agent running in Chrome on live desktop websites. Each step it sees a Set-of-Mark labeled screenshot plus page text, and acts in the WebVoyager action space: click a numbered element, type into one, scroll, wait, go back, jump to Google, or answer. The architecture pattern on the CUA Radar board is K14, “relabel exploration trajectories with retroactively inferred instructions” — a hindsight (HER-analogue) form of exploration-driven task synthesis.

PEEU (planning experience exploration and utilization) is the data pipeline around that agent, in two stages; the user provides only a URL.

1.  **Planning tree exploration.** An exploration model (GPT-4o) reads the homepage and generates a task list adapted to the site’s function (the task-setting prompt asks for 50 tasks). It then executes each task for at most 15 steps, growing a directed exploration tree of trajectories that share the homepage as root.
2.  **Planning experience utilization.** GPT-4o compares the states before and after each action to extract an atomic experience; a trajectory’s experiences form a sequence, and an aggregation step fuses them into a new PEEU task that the trajectory provably satisfies — aligned with the real outcome and constrained by what exploration actually found (e.g., recipes that include ingredients, cooking directions, and photos over 4 stars).

The relabeled (task, trajectory) pairs train the policy — current state, history, task description in; one action out — on Qwen2.5-VL-3B-Instruct or Qwen2.5-VL-7B-Instruct, with SFT (batch size 16, learning rate 5.0e-6, 5 epochs, llama-factory) and GRPO (batch size 20, learning rate 1.0e-6, rollout size 10, 7 epochs, verl). The GRPO reward is a format reward plus an answer-correctness reward, 1.0 each and 2.0 total. All experiments run on 4 A800 GPUs.

The paper also introduces TDHAF, an analysis framework that cuts tasks into low / mid / high granularity and tests generalization bottom-up, top-down, and out-of-domain, on data derived from Multimodal-Mind2Web with offline step metrics (element id, action type, action value, and full single-step match, “Step SR”; 616 training and 684 test samples).

## Results, as reported

The main table is **online**: WebVoyager, trajectory-level success rate, live websites, one run per cell, no seeds or standard deviations reported, and every trained method given the same trajectory scale. The paper’s headline: at 7B with 2k trajectories, PEEU-SFT reaches 30.6% overall, above Coarse-SFT at 19.0%, Atomic-SFT at 21.7%, and the much larger Qwen2.5-VL-32B Instruct at 22.7%.

| Method (Qwen2.5-VL-7B)                        | 0.1k traj | 2k traj |
|-----------------------------------------------|-----------|---------|
| Vanilla (no training)                         | 7.8       | 7.8     |
| Atomic-Prompt / Trajectory-Prompt (retrieval) | 3.7       | —       |
| Coarse-SFT                                    | 4.8       | 19.0    |
| Atomic-SFT                                    | 12.3      | 21.7    |
| PEEU-SFT                                      | 15.6      | 30.6    |

| Method (Qwen2.5-VL-3B) | 0.1k traj | 2k traj |
|------------------------|-----------|---------|
| Vanilla (no training)  | 0.2       | 0.2     |
| Coarse-SFT             | 2.0       | 13.2    |
| Atomic-SFT             | 4.8       | 16.7    |
| PEEU-SFT               | 5.7       | 19.8    |

With GRPO at 0.1k trajectories, 7B PEEU-GRPO reaches 19.9 against Atomic-GRPO 10.0 and Coarse-GRPO 11.5; at 3B it is 11.1 against 5.5 and 5.6. For context, the same table reports GPT-4o vanilla at 59.0, Claude 3 Opus at 56.1, and Qwen2.5-VL-72B vanilla at 29.3. The 7B / 2k PEEU-SFT row reads 17.7 on the in-domain Allrecipes column and 53.6, 16.2, 25.2, 19.5, 35.7, 48.7, 28.2 on the seven unseen sites (Amazon, Apple, Arxiv, Github, Coursera, Map, Wolfram).

The TDHAF numbers are **offline** and are kept separate here. In-domain, the 7B trained on low-level tasks reaches 89.6 Step SR on low-level tests but 18.8 on high-level ones; trained on high-level tasks it reaches 83.1, 63.6 and 72.1 across low / mid / high tests. Out-of-domain coverage (correct at all three levels) for the 7B is 37.8 when trained on high-level tasks versus 25.7 on low-level; for the 3B, 33.8 versus 18.9.

## What the paper’s own controls say

- **Matched data.** “All methods are controlled to use the same amount of data to ensure a fair comparison”, with identical trajectory scales and the same training parameters. At 7B / 2k, Coarse-SFT 19.0 versus PEEU-SFT 30.6 holds the trajectories fixed and changes only the task label — the cleanest evidence for hindsight relabeling.
- **Held-out environments.** “We test on seven additional websites that were entirely excluded from the training data”, and the 2k supplementary pool also comes from websites distinct from those seven.
- **Retrieval does not substitute for training.** Prompting small models with retrieved experiences scores 3.7 for both prompt baselines at 7B — below the untrained 7.8 — and 0.0 across the 3B prompt methods.
- **The granularity study is the mechanism check.** High-level training transfers down and across sites better than low-level training, which is the paper’s argument for why its relabeled high-level tasks work where atomic tasks do not.

## Where the evidence is thinner, in the paper’s words

- No variance: “Overall is the average accuracy of all websites” — no seeds, no confidence intervals, one run per cell.
- No validation of any learned judge or reward model is described, and no code release is listed.
- Scenario coverage: “we did not include scenarios involving sensitive operations such as user login, CAPTCHA solving, or actual payment transactions.”
- The 2k exploration data is described as “2k trajectories from a previously unseen website” in the main text but “approximately 2,000 tasks collected from additional websites” in the appendix; the sites themselves are never enumerated.
- Exploration, experience extraction and aggregation all use GPT-4o; the paper reports no ablation on the explorer, and no dollar or token cost.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **transfer**, sub-pattern K14 under exploration-driven task synthesis. The record credits online WebVoyager evaluation, seven held-out websites, baselines matched on data scale, a component/granularity ablation, and partial budget and cost reporting (identical trajectory scales, 4 A800 GPUs). It marks variance as not reported, the validator check and code as unclear, and flags the exclusion of sensitive operations. The radar did not rerun any experiment; every number above comes from version v1 of the paper.
