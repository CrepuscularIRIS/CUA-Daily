# SynthAgent: adapting a web agent to a new site with tasks and trajectories it refines itself

*A CUA Radar reading of arXiv 2511.06101v3 (Wang, Liang, Zhang, Wu, Han, Bastos, Wang, Bansal, Peng, Gao, Rajmohan, Yao). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2511.06101v3 · Code: https://github.com/aiming-lab/SynthAgent*

## The problem: a new website has no training tasks

A web agent often struggles on a new site because there are no task demonstrations and writing them by hand is slow. Synthetic data is the usual answer, but the paper argues that existing pipelines optimise only one side of the task-trajectory pair. OS-Genesis proposes a task from a single observed interaction; the goal can then mention elements or states that do not exist. Explorer starts from a coarse homepage goal and rewrites it at every step; the paper reports 8.6 task changes per trajectory on average, and 68.3% of its trajectories exceed the step budget. The authors name the tension: grounding a task avoids hallucination, but grounding it aggressively during execution adds trajectory noise.

## What SynthAgent is

The agent observes the URL, a textual accessibility tree, a list of candidate interactive elements and a screenshot. It acts through element ids: click, type, hover, press, scroll, goto, go_back, go_forward, plus none (final answer) and stop (give up). The setting is web only, with ReAct-style chain-of-thought and a 30-step budget. The CUA Radar board files it under the pattern “synthesise tasks from exploration and history” (sub-pattern K14). The paper calls it four steps (exploration and task synthesis together are step 1), ending in plain supervised fine-tuning:

1.  **Categorized exploration.** An LLM groups the interactive elements of each visited page by function (for example Account Management, Search and Filters) and samples up to 2 unvisited elements per group, giving (observation, action, next observation) triplets.
2.  **Task synthesis.** For each triplet the LLM imagines a broader, multi-step goal for which the observed action is one grounded step.
3.  **Task refinement during collection.** A GPT-4.1 agent executes the task. A conflict predicate fires if the goal refers to something absent, essential arguments are missing, or progress stalls (three consecutive no-op transitions, or the same loop twice). Only then is the task rewritten, close to its original intent. The paper reports 2.0 refinements per trajectory.
4.  **Trajectory refinement.** After collection, with no further interaction, an LLM sees the final task and the whole trajectory and chooses edits: Remove, Reorder, Drop the trajectory, or Keep it. Table 8 gives 39.3% Remove, 1.7% Reorder, 0.4% Drop and 58.6% Keep; the paper calls the edits conservative.
5.  **Fine-tuning.** Each refined (task, trajectory) pair is split into per-step examples, with a history window of 3. Data from the five WebArena sites is mixed to train one model (learning rate 1e-5, 3 epochs).

The training signal is therefore GPT-4.1’s own task writing, refinement and trajectory editing. No environment reward or learned reward model is used; the LLM’s keep, refine or drop decision is the only filter, and test tasks are not used (except in the SFT reference row below). All baselines are re-implemented with the same GPT-4.1 for synthesis and use up to 500 task-trajectory pairs per website.

## Results, as reported

The two benchmarks are labelled differently by the paper: WebArena (self-hosted, five sites, 226 tasks) is called offline, and Online-Mind2Web (300 tasks on 136 live websites, scored by LLM judges) is called online. Both are task-success rates from running the agent; the paper has no step-accuracy benchmark. No seeds or standard deviations are reported.

WebArena overall success (%), Table 1:

| Method                                  | Qwen2.5-VL-7B | UI-TARS-1.5-7B |
|-----------------------------------------|---------------|----------------|
| Base model                              | 8.80          | 8.85           |
| SFT on test-set tasks (upper reference) | 16.37         | 23.45          |
| Self-Instruct                           | 11.50         | 13.33          |
| OS-Genesis                              | 13.27         | 14.60          |
| Explorer                                | 4.44          | 4.96           |
| **SynthAgent**                          | **20.80**     | **17.26**      |

GPT-4.1 itself scores 25.22. The paper states average absolute gains of +10.2 over the base models and +5.1 over OS-Genesis. By site, SynthAgent is ahead of OS-Genesis on all five sites with Qwen2.5-VL-7B, but with UI-TARS OS-Genesis is higher on Shopping (21.82 against 20.00). With Qwen3-VL-8B the paper reports 15.93 for the base model and 24.34 for SynthAgent (Table 3).

Online-Mind2Web success (%), Table 2, under three judges. The table’s backbone rows are labelled only “Qwen”:

| Method         | GPT-4.1 judge | GPT-5.1 judge | WebJudge  | Average   |
|----------------|---------------|---------------|-----------|-----------|
| GPT-4.1        | 28.00         | 18.67         | 27.00     | 24.56     |
| Qwen           | 16.90         | 6.49          | 19.48     | 14.29     |
| Self-Instruct  | 17.67         | 13.00         | 19.67     | 16.78     |
| OS-Genesis     | 19.53         | 11.00         | 19.33     | 16.62     |
| Explorer       | 8.33          | 3.67          | 13.33     | 8.44      |
| **SynthAgent** | **31.67**     | **15.67**     | **23.33** | **23.56** |

The authors call this competitive with GPT-4.1 “though the absolute success rates are modest”. For Qwen3-VL-8B (Table 4) the averages are 18.67 for the base and 24.11 for SynthAgent; under the GPT-5.1 judge the two values are 14.67 and 15.00.

## What the paper’s own controls say

**Ablation (Table 10, WebArena; its base and full rows equal the Qwen2.5-VL-7B rows of Table 1).** Full SynthAgent scores 20.80. Without categorized exploration it is 17.26, without trajectory refinement 16.81, without task refinement 15.93, and without both refinements 15.93. The paper reads the drops as 3.54, 3.99 and 4.87 points respectively and calls task refinement the largest. Per site, the both-removed row equals the full model on Shopping (20.00) and drops to 12.50 on Maps; the authors conclude that the two refinements are synergistic.

**Data quality (Table 5, GPT-5.1 as rater, 0 to 100).** Trajectory quality is 82.6 for SynthAgent against 36.4 for Explorer, 52.0 for OS-Genesis and 41.7 for Self-Instruct; diversity is 82 against 46, 65 and 69. Appendix tables with two other raters keep the ranking.

**Completion and cost (Table 6, judged by GPT-4.1).** SynthAgent completes 96.5% of trajectories against 30.5% for Explorer, whose 68.3% exceed the step budget. Average API cost per trajectory is 0.13 against 0.22.

**Data scaling.** Average success rises from about 10.6 at 4% of the data to 20.8 at 100% (500 tasks per site).

## Where the evidence is thinner, in the paper’s words

- Task and trajectory synthesis rely solely on GPT-4.1 without hyperparameter tuning, and execution parameters such as the step limit are not optimised (Limitations). Only standard SFT is used.
- The WebArena sites are the same sites explored for synthesis, so that benchmark is not a held-out-site test (the CUA Radar record flags this overlap). The held-out evidence is Online-Mind2Web, “without any synthesis for targeted websites”.
- The Online-Mind2Web gains are smaller and depend on the judge: under GPT-5.1 SynthAgent (15.67) is above OS-Genesis (11.00) but below the GPT-4.1 agent (18.67). All three judges are automated, and the paper reports no human check. GPT-4.1 is both the synthesis model and one of the judges.
- For Qwen3-VL-8B the paper notes a smaller relative gain and suggests stronger models may already have internalised part of what synthetic demonstrations teach.
- The baselines were re-implemented by the authors; Explorer, with authentication support added, falls below the base model, which the paper says “matches the algorithmic design rather than an implementation error”.
- The text of Section 3.2 gives 6.3% of SynthAgent samples over budget, while Table 6 lists 0.0% exceeded; this summary uses the table.

## CUA Radar’s read

CUA Radar scores this paper **71 (★★★)**, evidence level **transfer**. The judgment record credits online evaluation, held-out sites (Online-Mind2Web), baselines re-run on the same GPT-4.1, a matched budget of up to 500 pairs per site, a component ablation, and released code; cost reporting counts as partial. Variance is recorded as not reported and a check of the judges as untested. It also flags anti-pattern AP5, exploration or synthesis sites overlapping the WebArena evaluation sites. The radar did not rerun any experiment; every number here comes from the paper (version v3).
