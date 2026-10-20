# MAGNET: a mobile GUI agent with two memories that evolve as apps change

*A CUA Radar reading of arXiv 2601.19199v2 (Sun, Zhang, Wang, Wei). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2601.19199v2*

## The problem: apps change, and agents trained on old versions break

App updates redesign icons without changing what they do (the paper’s example is Twitter becoming X) and reorganize workflows without changing the goal (setting a currency through a different navigation path). The paper says agents trained on historical data fail under such drift, and that existing memory systems mostly store text workflows, which say nothing about how a button looks. It observes two things that stay stable across updates: semantic stability (an updated element still supports the same action) and intent stability (the high-level task goal persists even when the steps change).

## What MAGNET is

MAGNET is a planner–actor agent for Android with two memories and no training. The agent sees a screenshot, a short text description of the screen and its action history, and acts with clicks (on a bounding box), scrolls and system keys such as home. On the CUA Radar board the paper sits in pattern K27, experience memory retrieval.

- **Procedural memory (for the planner)** captures intent stability. Each entry is a task category name plus high-level steps with placeholders such as \[AppName\]. The planner retrieves the most similar workflows for a new request and decomposes the goal into subtasks. Entries are built by clustering instructions (MiniCPM-Embedding, maximal cliques in a similarity graph) and prompting the planner to abstract each cluster’s trajectories.
- **Stationary memory (for the actor)** captures semantic stability. Each entry pairs a function description (“click the search icon to start searching”) with a cropped image of the element. The actor retrieves patches by matching the subtask text to function descriptions and receives them as visual exemplars; for a fixed-format grounding model such as OS-Atlas, retrieved patches are template-matched on the screen to draw a hint. Entries are built from screen-action-screen triplets with OmniParserV2 for regions and Qwen2.5-VL-32B for descriptions. Applied to AITZ, GUI-Odyssey and Amex this gives the UI-40K dataset, 41,009 entries across 20,618 unique functional intents.
- **Evolution and ranking.** Only successful trajectories update memory: new workflows are added and new element–function pairs are added or merged, with duplicates discarded. Retrieval first takes the semantically closest candidates, then ranks them by a retention score R = exp(-g/n), where g is the gap since the entry was last used and n its retrieval count, so frequently used entries decay more slowly.

## Results, as reported

**Online, AndroidWorld Easy split (61 tasks).** All agents use Qwen2.5-VL-32B and share the same action budget. Memory-augmented agents first build memory by self-exploration: MAGNET runs three passes over the 61 tasks, Agent-S one round of exploration tasks and AppAgent one exploration task per app.

| Method     | Task completion (%) |
|------------|---------------------|
| M3A        | 32.78               |
| AppAgent   | 34.43               |
| Agent-S    | 40.98               |
| **MAGNET** | **42.62**           |

The paper reports +8.2 points over AppAgent and +1.6 over Agent-S. ‡ With 61 tasks, 42.62% and 40.98% correspond to 26 and 25 completed tasks, so the margin over Agent-S is one task (this count is our arithmetic, not stated in the paper).

**Offline step accuracy** (in-distribution subsets, success rate / grounding accuracy). With Qwen2.5-VL-32B, MAGNET scores 43.50 / 43.78 on AITZ, 50.16 / 51.91 on GUI-Odyssey and 62.84 / 71.53 on Amex, against 41.09 / 39.28, 48.13 / 49.38 and 59.68 / 67.69 for the memory-free COAT. The paper notes that parameter-tuned specialized models reach higher absolute scores, for example 66.64 for Atlas-Pro-7B on AITZ; with Gemini-2.5-Pro, MAGNET reaches 52.77 on AITZ without task-specific training.

## What the paper’s own controls say

**Memory ablation (offline).** On the in-distribution subsets with Qwen2.5-VL-32B, GUI-Odyssey success rises from 48.13 with no memory to 48.62 (stationary only), 49.72 (procedural only) and 50.16 (both); Amex from 59.68 to 60.20, 62.34 and 62.84. The paper reads procedural memory as the larger contributor (+2.66 on Amex against +0.52) and explains the small stationary effect by static offline benchmarks rarely containing icons the model has not seen. There is no online ablation.

**Across architectures.** Over five planner–actor pairings and three datasets, memory adds an average of 2.3 points of success rate and 2.7 points of grounding accuracy, with the largest gain (4.2 points of success rate) for a Qwen planner with an OS-Atlas actor.

**Distribution shift (offline).** On template-, app- and domain-shifted subsets, stationary memory gives modest gains of +0.1 to +0.9 with Qwen, while procedural memory varies from slight degradation under template and app shifts to moderate gains under domain shifts; with Gemini-2.5-Pro the gains are +0.2 to +1.4. The figure’s values are not in the text.

**Continual adaptation (online).** Warm-started from Amex memory, success on AndroidWorld goes from 31.14 to 37.70, 39.34 and 40.98 over three iterations, while the share of retrieved entries still coming from the Amex bank falls from 100% to 26% (procedural) and 18% (stationary).

## Where the evidence is thinner

- The online test is 61 tasks with no seeds or variance, and the headline margin over Agent-S is one task (‡).
- The online memory is built by three passes over the same tasks that are then evaluated, and the baselines get different amounts of exploration; the CUA Radar record flags this overlap (anti-pattern AP5).
- Distribution-shift results are offline only, and the gains there are small.
- There is no online ablation of the two memories.
- Cost is not reported, the paper gives no code link, and its Table 1 labels COAT with Qwen2.5-VL-32B while its appendix says COAT uses Gemini-2.5-Pro.

## CUA Radar’s read

CUA Radar scores this paper **66 (★★)**, evidence level **online**. The record credits online evaluation, same-backbone and same-budget baselines, offline shift splits and a component ablation. It flags memory data overlapping with the evaluation (AP5) and records seeds or variance, cost and code as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v2).
