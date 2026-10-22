# GUI-Libra: curated reasoning data, action-aware SFT and KL-regularised RL for a native GUI agent

*A CUA Radar reading of arXiv 2602.22190v2 (Yang, Wu, Wang, Chen, Yang, Cheng, Yao, Peng, Zhang, Gao, Zhang). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2602.22190v2 · Code: https://github.com/GUI-Libra/GUI-Libra*

## The problem: reasoning, grounding and ambiguous rewards

The paper is about “native” GUI agents: a single end-to-end model that maps an instruction and an observation to an executable action. The authors say open-source native agents still lag on long-horizon navigation and point to two causes. First, open GUI trajectory datasets mostly have no rationales or only short, noisy ones (the paper reports often fewer than 100 thought tokens per step). Second, generic post-training recipes do not fit GUI agents. Standard SFT with long chain-of-thought (CoT) can hurt grounding, and step-wise RL from verifiable rewards faces what the paper calls partial verifiability: at a given state several actions can be correct, but only the single demonstrated action is used for verification, so valid alternatives are scored as failures.

## What GUI-Libra is

**The agent.** At each step the model sees a screenshot, the task instruction and an interaction history made of natural-language action descriptions. It outputs a reasoning trace inside `<think>` tags and then a structured JSON action inside `<answer>` tags: an action type, a short action description, an optional target element, a value (text, direction, app name) and a `point_2d` coordinate. There are 13 action types (Click, Write, Terminate, Swipe, Scroll, NavigateHome, Answer, Wait, OpenApp, NavigateBack, KeyboardPress, LongPress, Select), covering web and mobile. On the CUA Radar board the architecture pattern is R01, rule-reward single-step RL.

**The data.** The authors aggregate public trajectory sources (GUI-Odyssey, AMEX, AndroidControl, AitZ, AitW, GUIAct, MM-Mind2Web) and, after cleaning, have 19K trajectories with 170K steps. GPT-4.1 is prompted to write structured reasoning (observation, reflection, planning) with the annotated action as a reference. Two filters follow: an agreement filter that discards steps where Qwen3-VL-8B re-predicts the annotation with accuracy below 0.3 over 10 stochastic runs, and a bounding-box check with Qwen3-VL-32B that keeps a step only if the original click point falls in the predicted box. The result is GUI-Libra-81K: 81K steps from 9K trajectories, with an average of 210 thought tokens per step. Only 14.3% of it is web data. For RL, the set is rebalanced to 40K steps.

**Action-aware SFT (ASFT).** Training mixes reasoning-then-action samples with direct-action samples (reasoning removed), and re-weights tokens: action tokens get weight alpha_a and grounding (coordinate) tokens get alpha_g, relative to reasoning tokens. Defaults are alpha_a = 2 and alpha_g = 4. The mixed training also allows a no-reasoning inference mode.

**Conservative RL.** The second stage is step-wise GRPO on the static 40K-step set, with no live environment interaction during training. The reward is a weighted sum of a format reward (weight 0.1) and an accuracy reward, where accuracy is the product of action-type match, a word-level F1 test on the value, and whether the predicted point lies inside the demonstrated bounding box. Two choices target partial verifiability. The first is KL regularisation, kept in contrast to many RLVR recipes that drop it (coefficient 0.001, and 0.005 for the 7B model). The second is success-adaptive negative gradient scaling (SNGS), which multiplies only the negative advantages by a factor that grows with the fraction of GRPO samples matching the demonstration. The paper also gives a bound relating offline step matching to online success and argues that a KL trust region limits drift.

## Results as reported

Online task success, native models, with the step caps the paper states (20 steps on AndroidWorld, 15 on WebArena-Lite-v2, 30 on Online-Mind2Web). AndroidWorld uses 115 of its tasks (one could not be initialised). WebArena-Lite-v2 (154 tasks, locally deployed) is the mean of four runs. Online-Mind2Web (300 tasks, live websites) is the “average overall” of two judges, o4-mini and WebJudge-7B. Each GUI-Libra row is compared with the base model it was trained from.

| Base model | AndroidWorld base / GUI-Libra | WebArena-Lite-v2 base / GUI-Libra | Online-Mind2Web avg base / GUI-Libra |
|----|----|----|----|
| Qwen2.5-VL-3B | 3.5 / 25.2 | 0.8 / 16.7 | 4.8 / 21.3 |
| Qwen2.5-VL-7B | 7.8 / 29.6 | 4.9 / 22.6 | 15.8 / 25.5 |
| Qwen3-VL-4B | 27.0 / 42.6 | 11.9 / 24.4 | 21.7 / 25.7 |
| Qwen3-VL-8B | 30.4 / 42.6 | 15.3 / 26.6 | 19.3 / 28.0 |

The abstract states the gains over base models for the 4B and 8B variants as +15.6% and +12.2% on AndroidWorld, +4.0% and +8.7% on Online-Mind2Web, and +12.5% and +11.3% on WebArena-Lite-v2. Native Qwen3-VL-32B scores 34.8 on AndroidWorld and 26.8 on Online-Mind2Web. GPT-4o paired with UGround-v1-7B, a two-module framework, scores 42.6 on AndroidWorld and 24.3 on Online-Mind2Web, and a value of 23.2 on WebArena-Lite-v2 that the paper copies from another report. On WebArena-Lite-v2 a GPT-4o plus ScaleCUA-7B framework (28.6) is above GUI-Libra-8B.

Offline step accuracy is a separate axis and is not on the poster chart. On the authors’ cleaned AndroidControl-v2 (398 samples), GUI-Libra-8B reaches 64.3 Pass@1 on high-level tasks against 54.8 for Qwen3-VL-8B. On MM-Mind2Web-v2 the average Pass@1 is 50.5 against 43.8.

## What the paper’s own controls say

**Component ablation (Qwen2.5-VL-3B, AndroidWorld).** The base model scores 3.5. Plain SFT gives 5.2, SFT with mixed data 11.3, and ASFT 13.0. Adding RL with KL coefficient 0.001 gives 25.2; with KL 0.0 it gives 21.7; RL without ASFT (KL 0.001) gives 20.9. Training without CoT lowers the 25.2 to 12.2. The paper also reports that larger KL coefficients tend to raise offline Pass@4 while Pass@1 may drop slightly.

**SNGS.** On GUI-Libra-4B, switching SNGS on moves AndroidWorld from 39.1 to 42.6 and WebArena-Lite-v2 from 22.2 to 24.4, with a small trade-off on AndroidControl-v2 low-level Pass@1. Uniform negative scaling on the 3B model gives 19.1 and 20.0 on AndroidWorld, against 25.2 for the adaptive version. The paper notes SNGS is sensitive to hyperparameters.

**Offline versus online.** Over intermediate 3B and 7B checkpoints, the paper reports a Pearson correlation of 0.89 and Spearman 0.83 between offline and online scores with KL regularisation, and 0.63 and 0.53 without it. Without KL, evaluation scores fall while training reward keeps rising.

**Grounding under long reasoning.** On ScreenSpot-v2, 7B accuracy in reasoning mode goes from 79.0% (SFT) to 81.4% (mixed data) to 83.4% (ASFT), and after RL reaches 89.3% against 88.5% without reasoning.

**Fair comparison.** Baselines are trained on GUI-Libra-81K for two epochs, and the mixed-data models for one epoch. The paper also separates native models from agent frameworks with extra modules: a step-wise summary module adds 9.5 and 8.7 points to Qwen3-VL-4B and 8B.

**Judges.** Online-Mind2Web is scored with two judges. With o4-mini, GUI-Libra-8B gets 19.3 against 11.0 for its base; with WebJudge-7B, 36.7 against 27.7.

## Where the evidence is thinner

- The paper does not describe a held-out apps or sites split, and it does not report run-to-run variance for AndroidWorld or Online-Mind2Web. WebArena-Lite-v2 results are averaged over four runs, which the paper attributes to high variance.
- The judges are used as published and are not themselves validated in the paper.
- The authors say in their Limitations that they train on a relatively limited amount of data and do not explore fully online training. The SFT data is mostly mobile, and the paper notes that web Pass@4 may benefit from more web data.
- The cost is stated only partly: SFT takes about 4 hours (Qwen3-VL-4B) to 5.5 hours (8B) and RL about 16 and 20 hours on 8 B200 GPUs, but the paper reports no cost for data generation.

## CUA Radar’s read

CUA Radar scores this paper **71 (★★★)**, evidence level **transfer**. The record credits online evaluation on three benchmarks, strong baselines, matched step budgets, a component ablation and an announced code release; cost is partial. Held-out environments and variance are recorded as unclear, and judge validity as untested. No anti-pattern flags are recorded. The radar did not rerun any experiment; every number here comes from the paper (version v2).
