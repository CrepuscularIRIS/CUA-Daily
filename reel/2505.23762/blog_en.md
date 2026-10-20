# ZeroGUI: a GUI agent pipeline that writes its own tasks and grades its own trajectories

*A CUA Radar reading of arXiv 2505.23762v1 (Chenyu Yang, Shiqian Su, Shi Liu, Xuan Dong, Yue Yu, et al.). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2505.23762v1 · Code: https://github.com/OpenGVLab/ZeroGUI*

## The problem: offline training needs hands everywhere

GUI agents built on large vision-language models are usually trained offline, and the paper pins two costs on that: “heavy reliance on high-quality manual annotations for element grounding and action supervision”, and “limited adaptability to dynamic and interactive environments”. Interactive benchmarks such as OSWorld and AndroidLab ship a test set of manually crafted tasks plus script-based verification functions — fine for scoring, useless as a training corpus. Hand-building thousands of diverse training tasks and their success verifiers does not scale, and novel real-world scenarios arrive without ground-truth labels.

## What ZeroGUI is

The agents are pure-vision GUI agents: UI-TARS-7B-DPO and Aguvis-7B, both 7B. They perceive screenshots only (no DOM or a11y tree), and act with coordinate-grounded primitives — click, type, hotkey, terminate — on desktop (OSWorld’s Ubuntu, 1920 x 1080, at most 15 steps) and mobile (AndroidLab, 9 offline-deployable apps). On the CUA Radar board the paper sits in sub-pattern K16: a passive VLM outcome judge under “learned outcome and process judges”.

ZeroGUI automates the two hand-made ingredients:

1.  **Automatic task generation.** GPT-4o is prompted with task exemplars plus the screenshot of a randomly sampled initial state, and returns multiple candidates at once (10 per prompt on OSWorld, 5 on AndroidLab) for diversity. A subset of infeasible tasks is generated on purpose, requiring the agent to answer “FAIL”. Over 4,000 Ubuntu-based and 225 Android-based tasks are generated; 725 and 175 are sampled for training, about twice the size of the respective test sets.
2.  **Automatic reward estimation.** A locally deployed Qwen2.5-VL-32B assigns a binary success reward to a whole trajectory. Design choices target false positives, which the paper argues distort policy improvement more than false negatives: all screenshots of the trajectory are shown (not just the final frame), the agent’s own responses are hidden (they hallucinate success), and the VLM is queried 4 times at temperature 1.0 with unanimous-agreement voting.
3.  **Two-stage online RL.** Stage 1 trains on generated tasks; stage 2 is test-time training on the test set itself, without ground-truth labels, rewarded by the same VLM estimator. GRPO is extended to multi-step trajectories: a group of G = 64 trajectories per task, advantage = the voted reward normalized within the group, DAPO-style dynamic sampling, AdamW at a constant 2e-6, 1 epoch per stage. The k3 KL estimator is swapped for a k2 per-token MSE version, with an appendix derivation arguing it avoids huge gradients and numerical overflow.

So the only training signal is the VLM-voted binary outcome; no human label ever enters the loop.

## Results, as reported

All numbers are online success rates (SR), mean ± std over 4 runs, screenshot-only mode.

| Model | OSWorld all tasks | OSWorld feasible | AndroidLab full | AndroidLab ops subset |
|----|----|----|----|----|
| UI-TARS-7B-DPO | 17.7 ± 1.1 | 11.3 ± 0.6 | 45.7 ± 1.52 | 54.6 ± 1.72 |
| \+ ZeroGUI | 20.2 ± 1.0 | 15.8 ± 0.5 | 47.5 ± 2.12 | 57.4 ± 2.30 |
| Aguvis-7B | 3.0 ± 0.4 | 2.4 ± 0.5 | – | – |
| \+ ZeroGUI | 4.9 ± 0.4 | 4.5 ± 0.4 | – | – |

For UI-TARS-7B-DPO the paper reports +2.5 (14% relative) on all OSWorld tasks and +4.5 (40%) on the feasible subset; for Aguvis-7B, +1.9 (63%) and +2.1 (88%). On AndroidLab: +1.8 SR on the full set, +2.8 on the operation subset, +2.9 sub-goal success rate. pass@4 rises from 25.5 to 28.0 and all-pass@4 from 9.4 to 9.6 (UI-TARS), which the paper reads as capability coverage from generated tasks plus consistency from test-time training. For reference, rows marked \* in the paper’s table, taken from prior papers under different settings: GPT-4o 5.0, Claude Computer-Use 14.9, OpenAI Operator 19.7, UI-TARS-72B-DPO 22.7.

## What the paper’s own controls say

**The judge is checked against human labels.** On manually labeled trajectories, the full estimator reaches precision 61.5 / recall 51.1 with test SR 27.2; judging from the final frame alone drops to 47.5 / 40.4 with SR 23.9; letting the judge read the agent’s response gives the highest recall (74.5) but precision 44.3 and SR 24.0 — the response misleads it into false positives; dropping voting sits between at 53.7 / 61.7 with SR 25.6.

**Task generation ablation.** Without exemplars SR falls to 22.3 (infeasible-task detection 33.8); without multi-candidate generation 24.1; without generated infeasible tasks, success on the infeasible subset collapses from 41.3 to 22.1 — the FAIL tasks keep overconfidence in check.

**Training recipe.** On the OSWorld Daily domain: offline RFT 22.4, online RFT 24.5, online RL 27.2; with GRPO’s k3-KL instead of k2-KL, 26.1, and the training-accuracy curves are less stable. A KL-coefficient sweep (Fig. 6) favors the middle setting; removing KL or over-weighting it both hurt.

**Stage split.** Test-time training alone reaches 18.2 (test-set SR), generated-task training alone 18.2, both stages 20.2 — the two-stage order matters.

## Where the evidence is thinner, in the paper’s words

- The second stage trains on the test set: “the agent performs test-time training on the test set without ground-truth labels, receiving rewards solely from the same VLM-based evaluator.” The evaluation environment is therefore also a training environment; no held-out environment is reported.
- Gains on the full OSWorld set are smaller than on the feasible subset, “indicating a decrease in the detection of infeasibility”; the paper blames the VLM’s lack of software-specific knowledge and reward noise, only partly mitigated by FAIL tasks.
- On AndroidLab, “we fix some code errors in the original task verifiers, and some baseline methods get higher scores after the correction”, and the GPT scoring of query-detecting tasks “is not fully reliable” — hence the operation-subset reporting.
- Ablations run on the Daily domain only (Chrome, Thunderbird, VLC) “to reduce experimental burden”; the judgment record also marks budget matching as partial (15-step cap) and cost reporting as partial.

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **transfer**, sub-pattern K16 (passive VLM outcome judge). The record credits: online evaluation on OSWorld and AndroidLab, mean and std over 4 runs, offline-RFT and online-RFT baselines, component ablations for task generation, judge and KL loss, a precision/recall validation of the learned judge against manually labeled trajectories, and released code. It flags: no held-out environment (test-time training on the test set), and only partial budget and cost matching. The radar did not rerun anything; every number above comes from the paper (version v1).
