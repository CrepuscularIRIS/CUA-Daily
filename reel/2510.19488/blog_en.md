# VideoAgentTrek: turning 39,000 unlabeled tutorial videos into computer-use training data

*A CUA Radar reading of arXiv 2510.19488v1 (Lu, Xu, Wang, Wu, Wang, Wang, Yang, Su, Chen, Chen, Mao, Zhou, Lin, Hui, Yu). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2510.19488v1 · Code: https://github.com/xlang-ai/VideoAgentTrek*

## The problem: the demonstrations exist, the labels do not

Training a computer-use agent needs screenshots paired with exact actions: click coordinates, typed strings. Manual annotation at that scale is expensive. The internet holds a great many screen-recorded tutorials in which people click and type, but the recordings carry no structured action labels: the cursor is visible but not tracked, the typed text appears on screen but is not extracted, the timing of each action is implicit. The paper asks whether a model can recover those labels, and whether training on them helps an agent.

## What VideoAgentTrek is

VideoAgentTrek is a data pipeline plus a two-stage training recipe. The agent it trains is a Qwen2.5-VL-7B model that sees up to five recent screenshots plus its history of thoughts and actions, and emits a short thought followed by an action (click with coordinates, type, scroll, key press). The paper reports this base scores 4.5% on OSWorld. On the CUA Radar board it sits in pattern R03, mining human screen videos.

The pipeline has three parts:

1.  **Collect and filter.** Seed queries and tags, then channel-level expansion when at least 80% of sampled videos in a channel look good, give 55,000 candidate videos (about 10,000 hours). ScreenFilter, a YOLOv8x cursor detector, keeps segments where at least 80% of frames contain a cursor for 6 seconds or more; 7,377 hours remain.
2.  **Video2Action, an inverse dynamics module.** An event detector (Qwen2.5-VL-7B, fully fine-tuned on 154 hours of screen video with OpenCUA interaction logs) takes a video with no prompt and outputs typed GUI events with start and end times. A second model reads each segment and predicts the parameters (click coordinates, literal text). GPT-5 Medium then writes a short “inner monologue” for each step from the action, the parameters, before/after frames and the surrounding speech transcript.
3.  **Training.** Applied to 39,000 videos at about 39 steps each, this gives 1.52 million steps and about 26 billion tokens. Stage 1 is one epoch of continued pretraining on these video-derived trajectories (with a few grounding pairs). Stage 2 is supervised fine-tuning on 8 billion tokens of human trajectories drawn from OpenCUA and AGUVIS, in a chat format.

The signal that trains the agent is therefore the labels produced by the learned inverse dynamics model, then human demonstrations. Stage 1 used 32 H100 GPUs for about 60 hours.

## Results, as reported

OSWorld-Verified is online: a live desktop, 369 Ubuntu tasks. AgentNetBench is offline: 100 tasks scored per step. Both use the same Qwen2.5-VL-7B base.

| Model | OSWorld-Verified, 20 steps (mean of 3 runs) | OSWorld-Verified, 50 steps (1 run) | AgentNetBench step success (offline) |
|----|----|----|----|
| Base | 4.5 | not reported | 38.5 |
| Stage 2 only (SFT-only) | 9.3 | 9.27 | 64.1 |
| Stage 1 + stage 2 | 14.13 | 15.78 | 69.3 |

The abstract’s headline, 15.8% against 9.3%, a 70% relative improvement, compares the single 50-step run with the SFT-only figure. At 20 steps the paper itself reports 14.13% against 9.3%, a 4.83-point improvement (52% relative). The three 20-step runs are 14.68, 13.57 and 14.13 for stage 1 + 2, and 9.42, 9.13 and 9.42 for SFT-only.

## What the paper’s own controls say

**Data scale.** Training with 0%, 50% and 100% of the stage-1 video tokens, then the same stage 2, gives OSWorld-Verified success at 50 steps of 9.3, 13.3 and 15.7, and AgentNetBench step success of 64.1, 68.1 and 69.3.

**Step budget.** Raising the budget from 20 to 50 steps leaves the SFT-only model flat (9.3 to 9.27), while the model with stage 1 goes from 14.13 to 15.78. The paper attributes this to long video trajectories (42.1% exceed 20 steps; the average is 39.25 steps).

**How good are the labels?** On 23 held-out hours with 20,282 annotated events, the event detector reaches precision 0.88 and recall 0.70, with clicks at F1 0.82 and drags at 0.62; key presses are weak (precision 0.40, recall 0.08). For action parameters there is no automatic ground truth, so the authors manually judged 500 predictions in the wild: overall accuracy 0.658, with click 0.713, scroll 0.735, type 0.671, drag 0.366 and press 0.362.

## Where the evidence is thinner

- The paper does not say which OSWorld applications, if any, were held out from training; the CUA Radar record marks held-out evaluation as unclear.
- Only the three 20-step runs give a spread, with no standard deviation or interval; the 50-step results are single runs.
- The comparison is stage 2 only against stage 1 + stage 2. The paper does not include a control that spends the same stage-1 token budget on other data, so the data-scale curve is the main evidence about the role of the video labels.
- AgentNetBench and the human trajectories used in stage 2 both come from the cited OpenCUA work (Wang et al., 2025b); the paper does not state whether they are disjoint.
- Label quality is uneven: 0.658 of manually checked action parameters were judged correct, and drag and press are much lower. The paper says the parameters are “accurate enough for trajectory construction and downstream training”.
- Compute is reported for training (for example 32 H100 GPUs for about 60 hours in stage 1) and for the filter’s throughput (about 840 hours of video per GPU-day), but the paper gives no total cost for the labeling pipeline.

## CUA Radar’s read

CUA Radar scores this paper **68 (★★)**, evidence level **online**. The record credits online OSWorld-Verified evaluation against a same-base SFT-only baseline, a step-budget control, a data-scale ablation, a check of the event detector on held-out video, and announced open-source tools; it records no flags and marks held-out evaluation as unclear and variance as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v1).
