# Hierarchical Memory Tree: separating what a web task needs from how one site does it

*A CUA Radar reading of arXiv 2603.07024v1 (Tan, Gao, Wu). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2603.07024v1*

## The problem: remembered steps carry site-specific baggage

Web agents often keep memory as past successful trajectories stored as flat sequences of observations and actions. The paper argues that this mixes two things with different lifetimes: the high-level intent (book a flight), which transfers across websites, and the action details (click button `#btn-123`), which do not. Retrieved on an unseen site, such a trajectory can pair the right intent with elements that do not exist. The authors name this intention-execution entanglement and describe two consequences: workflow mismatch (the retrieved action is right for the source task but wrong for the current stage, for example a checkout click before an item is chosen) and context pollution (long raw trajectories crowd the prompt).

## What HMT is

The Hierarchical Memory Tree (HMT) is a memory structure plus an inference procedure; no model is trained. The agent reads a simplified DOM or accessibility tree and issues operations such as CLICK and TYPE on elements. On the CUA Radar board the paper sits in pattern K27, experience memory retrieval.

**Memory construction.** From successful trajectories only, an LLM builds three levels:

1.  **Intent level.** The raw instruction is rewritten into a normalized intent plus constraints in a fixed JSON format, so different phrasings of the same request share one task node.
2.  **Stage level.** The trajectory is split into contiguous subgoals (“Search flights”, “Filter results”), each with observable pre-conditions and post-conditions (“search results visible”, “price filter applied”). Consistency checks cover coverage, ordering, contiguity and minimum length; if they fail, adjacent segments are merged.
3.  **Action level.** Each step becomes an action pattern paired with a semantic element description (role, label, relative position) instead of the raw element identifier.

Offline, memory is built once from a dataset of successful trajectories (the Mind2Web training split). Online, it starts empty and every successful episode in the evaluation stream is abstracted and added.

**Stage-aware inference.** Retrieval is top-down: task nodes, then subgoals scored by a mix of embedding similarity and lexical overlap with the current page (weight 0.3 on the condition match). A Planner abstracts the current page, matches it against the pre- and post-conditions of the retrieved subgoals and picks a stage with a confidence score. If the margin between the top two subgoals or the confidence is low, it widens the candidate set, and if that also fails it falls back to the base policy without memory. An Actor then receives step exemplars and uses their semantic descriptions to select the matching element on the current page, rather than copying an ID. The backbone is GPT-4 at temperature 0 for every component.

## Results, as reported

**Online: WebArena** task success (%), all domains but with the paper’s weighted total.

| Method | Total | Shopping | CMS | Reddit | GitLab | Maps | Avg steps |
|----|----|----|----|----|----|----|----|
| WebArena baseline | 14.9 | 14.0 | 11.0 | 6.0 | 15.0 | 16.0 | 12.4 |
| SteP | 33.0 | 37.0 | 24.0 | 59.0 | 32.0 | 30.0 | 8.5 |
| AWM | 35.5 | 30.8 | 29.1 | 50.9 | 31.8 | 43.3 | 5.9 |
| Flat Retrieval (authors’ ablation baseline) | 32.1 | 28.5 | 25.8 | 47.0 | 28.5 | 39.0 | 6.5 |
| **HMT** | **38.7** | 33.8 | 34.1 | 52.5 | 37.6 | 42.2 | 5.2 |

HMT is highest in total and in CMS and GitLab; SteP is higher on Reddit and Shopping, and AWM is higher on Maps, which the authors attribute to map interactions relying on spatial coordinates where a text description helps less.

**Offline: Mind2Web** step success rate (%).

| Method               | Cross-task | Cross-website | Cross-domain |
|----------------------|------------|---------------|--------------|
| MindAct              | 36.2       | 30.1          | 26.4         |
| AWM (offline memory) | 45.1       | 33.7          | 32.6         |
| AWM (online memory)  | 43.6       | 33.9          | 35.5         |
| **HMT**              | **48.5**   | **39.7**      | **37.1**     |

On cross-task, where the sites were seen in training, the paper says HMT is comparable to AWM; task-level success is small for every method (HMT 4.6, 3.2 and 1.9 across the three splits, AWM-offline 4.8, 2.3 and 0.7).

## What the paper’s own controls say

**Ablations.** On WebArena total task success: full 38.7; without the confidence fallback 37.8; without pre/post-conditions 36.2; with raw element identifiers 34.5; without the planner 33.5; with a flat memory 32.1. On Mind2Web cross-website step success, raw identifiers drop it from 39.7 to 12.4.

**Mechanism checks.** Recall@5 of the ground-truth step on Mind2Web cross-website is 84.2% for HMT against 65.8% for flat retrieval. Locating the target element succeeds 92.1% of the time with raw identifiers on cross-task but 12.4% on cross-website, against 76.8% with semantic descriptions.

**Efficiency.** Against flat retrieval over raw HTML, average context is 3,120 tokens against 11,450, latency is 3.5 against 5.2 seconds per step, and cost is 0.11 against 0.38 dollars per task, even though inference now has two stages.

## Where the evidence is thinner

- The paper reports single numbers: no seeds, standard deviations or intervals, and one backbone (GPT-4).
- Baseline rows are given as printed in the tables; the paper does not say whether they were re-run under the same settings, and budget matching is not reported.
- The efficiency comparison and the ablation baseline are the authors’ own flat-retrieval variant.
- Mind2Web task-level success is low for every method, and the strongest gains are in step success on the cross-website split.
- Qualitative failures include ambiguous grounding (a generic “more” descriptor matched a distractor button) and a rigid post-condition that expected a URL change on a single-page app and looped.
- The record flags data overlap (anti-pattern AP5); the paper gives no code link.

## CUA Radar’s read

CUA Radar scores this paper **66 (★★)**, evidence level **online**. The record credits online WebArena evaluation, a cross-website split, AWM and flat-retrieval baselines, a component ablation and cost reporting. It flags data overlap (AP5) and records variance, matched budgets and code as unclear. The radar did not rerun any experiment; every number here comes from the paper (version v1).
