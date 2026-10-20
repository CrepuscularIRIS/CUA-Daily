# ScaleCUA: an open data pipeline and model family for screenshot-only computer use agents

*A CUA Radar reading of arXiv 2509.15221v2 (Liu, Xie, Ding, Li, Yang, Wu et al.). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2509.15221v2 · Code: https://github.com/OpenGVLab/ScaleCUA*

## The problem: GUI trajectories are scarce

The paper starts from a data argument. Image-text pairs are abundant online, but “computer-use data, particularly operation trajectories, are rare, costly to collect”. Trajectories also go stale as software and web pages change, and the GUI corpora behind the strongest agents are often proprietary. The authors add that existing open datasets are limited in coverage and diversity, particularly for desktop. Manual collection gives good trajectories but does not scale; automated exploration scales but is noisy. The paper’s answer is a large cross-platform corpus plus a family of base models trained on it.

## What ScaleCUA is

**The agent.** ScaleCUA models are fine-tuned from Qwen2.5-VL at 3B, 7B and 32B. They perceive screenshots only: the paper states that “our models are evaluated with pure visual observation on all benchmarks”, and argues that this avoids interference from noisy accessibility-tree and DOM data. They act with coordinate-level commands from one unified action space covering desktop, browser and mobile (click, write, scroll, hotkey, dragTo, swipe, open app and so on). The board pattern is C12: normalise heterogeneous trajectories into one declared action schema and train a screenshot policy on it.

**Three inference modes.** Grounding Mode returns a point or bounding box for a described element, so a stronger planner such as GPT-4o can be paired with ScaleCUA as the grounder. Direct Action Mode emits a short operation description plus an executable action. Reasoned Action Mode writes a thought first, then the action.

**The data pipeline.** Two loops feed the corpus. An agent-environment loop runs on Windows, Ubuntu, macOS, Android, iOS and the web, reading element boxes from A11y trees (desktop), the DOM (web) and XML layouts (Android); OmniParser fills in where trees are incomplete or unavailable. An agent-human loop adds expert-recorded goal-directed trajectories, collected in Docker containers. For automatic exploration the authors found VLM-driven agents biased and low-diversity, and used a rule-driven random walk with depth-first search and pruning instead. Raw trajectories are cut into weak-semantic sub-trajectories by screen similarity. GPT-4o and Claude-3.7 annotate appearance, position and function; augmentations include cropping, stitching screenshots and background substitution.

**The corpus.** 471K GUI-understanding examples, 17.1M grounding examples (point, box and action) on 1.6M images, and 19K trajectories (average 9 steps), of which 4K are human-curated goal-directed demonstrations. Training mixes in general multimodal data at 25%, 50% and 75% of the GUI data for the 3B, 7B and 32B models. The training signal is supervised; the paper explicitly leaves RL, reward models, reflection and memory for future work.

## Results as reported

All numbers are copied from the paper’s tables. **Online** success rates (Table 5) come first; offline results follow separately. The 15-step and 50-step columns are step budgets; AndroidWorld uses each task’s own predefined limit.

| Online success (%) | AndroidWorld | OSWorld (50) | WindowsAgentArena (50) | MacOSArena (50) | WebArena-Lite-v2 (50) |
|----|----|----|----|----|----|
| ScaleCUA-3B | 23.7 | 12.4 | 15.2 | 1.4 | 33.1 |
| ScaleCUA-7B | 27.2 | 15.0 | 20.7 | 4.3 | 37.7 |
| **ScaleCUA-32B** | 30.6 | 17.7 | 24.2 | 7.1 | **47.4** |
| UI-TARS-72B-DPO | 46.6 | 25.2 | 17.9 | 8.6 | 21.4 |
| UI-TARS-1.5-7B | 31.6 | 23.9 | 15.9 | 7.1 | 26.0 |
| Qwen2.5-VL-72B | 27.6 | 10.6 | 9.7 | 5.7 | 14.4 |
| GPT-4o + UI-TARS-1.5-7B (grounder) | 37.9 | 19.1 | 26.2 | 0.0 | 28.6 |
| GPT-4o + **ScaleCUA-7B** (grounder) | **48.3** | 28.1 | 36.6 | 8.6 | 35.1 |

Reading the table as printed: ScaleCUA-32B has the highest WebArena-Lite-v2 score in the native block (47.4 at 50 steps, 44.2 at 15 steps against 23.4 for UI-TARS-72B-DPO) and the highest WindowsAgentArena 50-step score among the native rows shown (24.2). On OSWorld its 17.7 is below UI-TARS-72B-DPO (25.2) and UI-TARS-1.5-7B (23.9), and the table also lists OpenCUA-32B at 34.1, Seed1.5-VL at 39.6 and COMPUTERRL at 47.3, with step counts marked as above 50 or unknown for the last two. MacOSArena scores stay low for every model; the paper reads this as OS-specific affordance gaps. With GPT-4o as planner, ScaleCUA-7B as grounder reaches 48.3 on AndroidWorld, 28.1 and 36.6 on OSWorld and WindowsAgentArena, and 35.1 on WebArena-Lite-v2, above the other grounders in the table that report those columns. The paper’s text says scaling 3B to 7B to 32B gives monotonic gains on Windows and Web.

**WebArena-Lite-v2** is the authors’ own upgrade of WebArena-Lite: 154 tasks (11 multi-tab tasks removed from 165), local Docker websites, pure-vision compatible, with revised instructions and answer checkers.

**Offline results** (kept apart from the table above). MMBench-GUI L1, GUI understanding as multiple choice: ScaleCUA-32B scores 92.5 (easy), 92.5 (medium) and 94.4 (hard), against 92.8, 91.7 and 94.2 for GUI-Owl-32B. Grounding: ScreenSpot-v2 94.7 (Table 3 also lists Seed-1.5-VL at 95.2 and UI-TARS-1.5 at 94.2), ScreenSpot-Pro 59.2 (GUI-Owl-32B 58.0), OSWorld-G 60.6 (Table 8 lists Seed1.5-VL at 62.9). On AndroidControl-High, ScaleCUA-32B reaches 75.9 step success against 74.7 for UI-TARS-72B; on AndroidControl-Low its 85.7 is below UI-TARS-72B (91.3) and Qwen2.5-VL-72B (93.7). On ScienceBoard, ScaleCUA-32B scores 5.9, below Qwen2.5-VL-72B (12.9) and Claude-3.7-Sonnet (10.5).

## What the paper’s own controls say

All ablations in Table 6 use the **3B** model.

- **Augmentation** (GUI data only, ScreenSpot-Pro, offline): 37.8 without, 41.3 with element cropping and screenshot concatenation.
- **Weak-semantic trajectories** (public data only, online, 50 steps): OSWorld 7.9 to 8.5; WebArena-Lite-v2 8.4 to 14.3.
- **Coordinates**: raw 42.3 vs normalised 37.9 on ScreenSpot-Pro.
- **Training resolution**: 2K gives 45.5 on ScreenSpot-Pro against 42.3 at 1080P, but online AndroidWorld falls from 23.3 to 13.4 and OSWorld from 12.4 to 11.2.
- **Direct vs Reasoned Action**: reasoning gains +1.4% to +8.2% absolute across benchmarks, described as particularly pronounced on WebArena-Lite-v2, at higher latency.
- **Data scaling**: gains look logarithmic, mostly saturating beyond 75% of the data; WebArena-Lite-v2 is nearly linear.
- **General multimodal data**: GUI benchmarks decline gradually as its share grows while general benchmarks improve, peaking around 75%. ScaleCUA-32B (75%) scores 69.8 on MathVista and 61.9 on MMMU, below Qwen2.5-VL-32B (74.7 and 70.0).

## Where the evidence is thinner

- **Held-out status is not stated.** The paper lists WebArena Forum, GitLab, Shopping and CMS among its web data sources (Table 14), and the online web benchmark is built on WebArena. It does not say how, or whether, training and evaluation sites were separated.
- **No seeds, standard deviations or confidence intervals** accompany any table.
- **Step budgets are only partly matched**: Table 5 marks rows with unknown step counts or more than 50 steps.
- The text of Sec. 5.2.3 attributes the WindowsAgentArena comparison (24.2 vs 17.9) to the 15-step setting, while Table 5 places those values in the 50-step column; this summary follows the table. The text also calls UI-TARS-72B-DPO the best native web baseline at 50 steps, although Table 5 lists UI-TARS-1.5-7B at 26.0 versus 21.4.
- In the authors’ words: “the quality of agent-collected data still lags behind expert crowdsourcing”, memory is “rudimentary”, and “reflection, memory-based decision-making, or hierarchical planning” are not included. The error analysis shows the model repeating an action when the screen does not change.

## CUA Radar’s read

CUA Radar scores this paper **71 (★★★)**, evidence level **transfer**. The record credits online evaluation on five live benchmarks, strong baselines, data ablations and released code, and marks step-budget matching and cost reporting as partial. Held-out environments and seed variance are not reported. No anti-pattern flag is recorded; the judgment notes that AndroidWorld favors planner-grounder workflows, narrowing but not closing the gap with mobile-focused native models. The radar did not rerun any experiment; every number here comes from the paper (version v2).
