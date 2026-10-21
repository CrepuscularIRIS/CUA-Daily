# NaviMaster: one GRPO policy for GUI and embodied navigation

*A CUA Radar reading of arXiv 2508.02046v4 (Luo, Yan, Gong, Wang, Zhang, Wang, Xie, Tan). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2508.02046 · Project page (code, data, checkpoints): https://iron-boyy.github.io/navimaster-page/*

## The problem: two navigation stacks that never meet

GUI agents and embodied navigation agents both traverse environments from first-person observations, but they have “largely evolved in isolation, with disparate datasets and training paradigms”. The paper lists four persistent consequences: (1) two individual models per system, which raises training and deployment cost and blocks synergy between the tasks; (2) scaling data within one task generalizes poorly to out-of-domain (OOD) inputs; (3) RFT-style training with sparse binary rewards makes reinforcement learning inefficient; (4) reasoning distilled from text yields “correct thoughts but wrong actions”. Its unification argument is formal: both tasks are Markov Decision Processes over egocentric visual observations, so they can share one state representation, one action space and one training pipeline.

## What NaviMaster is

The agent is a multimodal LLM policy with Qwen2.5VL-7B as the base model. At each step it sees the instruction, the current observation (a GUI screenshot or a first-person camera frame from the Habitat simulator), a depth map (set to the zero matrix for pure 2-D screenshots), and a history of previous (thought, action) pairs; it outputs a thought plus one JSON action. Actions come in three classes. Specific actions have fixed semantics: BACK and HOME in GUI, STOP in embodied tasks. View-shifting actions are SCROLL (up/down/left/right) in GUI and TURN (left/right/around/down) in embodied scenes. Localization actions are the core trick: GUI keeps CLICK(x, y), and embodied navigation is reformulated from MOVEFORWARD to MOVETO(x, y), so every localization action names an explicit pixel target — the “visual target” that makes the two action spaces isomorphic. Platforms: mobile, web and desktop GUI benchmarks, evaluated offline, plus simulated embodied navigation (Matterport 3D scenes in Habitat). On the CUA Radar board the architecture pattern is R01: offline single-step GRPO with rule-checked action and grounding rewards.

The pipeline has three parts. First, visual-target trajectory collection: GUI trajectories are reused from GUI-Odyssey; embodied trajectories are built by running A\* between the initial and target positions in Matterport 3D, projecting each next waypoint into the current camera view, and inserting TURN actions whenever the target falls outside the field of view or behind the camera. GPT-4o then writes a roughly 60-word first-person thought for every action. Second, unified reinforcement learning: no SFT stage (an R1-Zero recipe); each step of an n-step trajectory is one training sample, GRPO samples a group of rollouts per step (5 generations), and the advantage is group-normalized. Training uses 20k samples — 10k GUI from GUI-Odyssey and 10k embodied from Matterport 3D and RoboPoint — for 3 epochs on 8 A800 GPUs, batch size 128, learning rate 1×10−6, KL coefficient 0.01, in the EasyR1 framework. Third, the distance-aware reward, R = λ1·RF + λ2·RT + λ3·RG with λ = 0.1, 1, 1: a format reward for a parseable think/answer JSON, a type reward for matching the ground-truth action type, and a dense grounding reward (1 − dj/θd) that scores a rollout by its pixel distance dj to the target point, gated by a depth-disparity check; the dense threshold is θd = 200 pixels, against 20 pixels in the sparse variant. The training signal is thus rule-computed from the single labelled reference action per step — no environment feedback enters the loop.

## Results, as reported

All GUI and affordance numbers below are offline; embodied navigation runs in simulation. The paper states results are averaged over multiple trials with vLLM temperature 0; no seed count or standard deviation is given.

GUI, per-step success rate (SR), Table 1. SR here is the per-step task success rate under the OS-Atlas protocol; grounding accuracy (GR) is reported alongside:

| Model               | AC-High   | AITZ      | GuiAct-W  | OmniAct-W | Odyssey   |
|---------------------|-----------|-----------|-----------|-----------|-----------|
| Qwen2.5VL-7B (base) | 47.06     | 33.88     | 78.08     | 71.91     | 37.32     |
| GUI-R1-7B           | 51.56     | 49.06     | 74.54     | 68.69     | 36.22     |
| UI-AGILE            | 50.97     | 38.74     | 69.57     | 63.15     | 36.96     |
| Ours w/o Embodied   | 53.47     | 52.56     | 83.68     | 72.63     | 46.38     |
| **NaviMaster**      | **55.89** | **54.00** | **86.17** | **72.99** | **48.35** |

Odyssey is in-domain (GUI-Odyssey is the training source); the paper highlights the other test sets as OOD, and reports grounding of 93.90 (AC-Low) and 78.15 (AC-High) for NaviMaster. NaviMaster is not the top number in every column: on AC-Low SR it reports 69.46 against 73.38 for UI-shift and 92.10 for infiGUI-3B, which the paper’s in-domain/OOD colouring treats separately.

Spatial affordance prediction (offline; average success of predicted points inside the ground-truth mask), Table 2:

| Model             | RoboReflt | Where2Place | RoboSpatial | RefSpatial |
|-------------------|-----------|-------------|-------------|------------|
| RoboPoint-13B     | 49.82     | 46.77       | 19.70       | 8.40       |
| Ours w/o Embodied | 67.86     | 35.05       | 14.75       | 16.88      |
| Ours w/o GUI      | 76.23     | 43.02       | 19.83       | 18.19      |
| **NaviMaster**    | **77.34** | **52.97**   | **21.65**   | **19.49**  |

Embodied navigation (simulated; ObjectNav unseen validation branch under the VLMNav framework), Table 3:

| Model             | SR        | SPL       |
|-------------------|-----------|-----------|
| Qwen2.5VL-7B      | 27.23     | 9.68      |
| RoboPoint         | 13.01     | 2.80      |
| SpaceLLaVA        | 14.98     | 2.62      |
| Ours w/o GUI      | 31.10     | 11.20     |
| Ours w/o Embodied | 31.00     | 10.05     |
| **NaviMaster**    | **33.20** | **12.60** |

(The running text says “the highest SR of 33.10%”; Table 3 prints 33.20. We quote the table.)

## What the paper’s own controls say

**Data mixing.** Removing either data source lowers every task family: ObjectNav SR falls from 33.20 to 31.10 (w/o GUI) and 31.00 (w/o Embodied); RoboReflt falls from 77.34 to 67.86 (w/o Embodied). A ratio sweep peaks at the 5:5 mix, and mix training also beats a two-stage GUI-then-embodied schedule (55.89 vs 54.83 AC-High SR). “All the experiments of NaviMaster use the same amount of data for a fair comparison.”

**Reward design.** The sparse-reward variant (20-pixel threshold) reaches 54.07 AC-High SR against 55.89 dense; removing the format or type reward costs 1–2 points across navigation benchmarks (Table 8). The 200-pixel distance threshold beats 100/300/400-pixel variants (55.06 / 55.77 / 53.61), and the depth term is presented as robustness, not a performance source.

**Base model and scale.** The mix advantage reproduces on Qwen2.5VL-3B (45.26 vs 28.75 AC-High SR for a single-source 3B run) and at 7k samples (52.66), which the paper reads as evidence the gain is not just a strong 7B base or large-data effect.

**Metric caution.** The paper itself shows the action-Type metric is biased: a naive model predicting only CLICK scores 55.9–64.4 across the GUI test sets, so Type is reported but not trusted.

## Where the evidence is thinner, in the paper’s words

- The unification is at the data level, not the episode level: “Our trajectory dataset lacks any single trajectory that interleaves GUI and embodied navigation tasks due to the collection difficulty.”
- Variance is asserted, not quantified: “All reported results are averaged over multiple trials” — no seeds, no confidence intervals.
- No live-device or online evaluation appears: GUI results are offline per-step accuracy, and the embodied evidence level rests on simulated ObjectNav.
- Baselines come from different training corpora (OS-Atlas, Aguvis, UI-Tars-style pipelines use much larger data); only NaviMaster’s own variants are data-matched.
- The concurrent unified agent OmniActor is excluded because “it is evaluated on a subset of benchmarks and its implementation is not publicly available”, and reasoning thoughts depend on GPT-4o.

## CUA Radar’s read

CUA Radar scores this paper **63 (★★)**, evidence level **online**, architecture pattern **R01** (offline single-step GRPO with rule-checked action and grounding rewards). The judgment record credits OOD held-out test sets, strong SFT and RL baselines, component and reward ablations, and released code, data and checkpoints; it marks variance unclear, the online evaluation partial (per-step offline metrics plus simulated ObjectNav), and budget matching partial (same data amount, different baselines’ corpora). Its flag that the RL signal is one reference action per step is visible in the paper’s own design: “given an n-step trajectory, we take step i as a data sample.” CUA Radar did not rerun anything; every number here comes from the paper (version v4).
