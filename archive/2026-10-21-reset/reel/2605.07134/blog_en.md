# Region4Web: a web agent that reads pages as functional regions, not element lists

*A CUA Radar reading of arXiv 2605.07134v1 (Donguk Kwon and Dongha Lee, Yonsei University). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2605.07134v1 · Code (stated in the paper): https://github.com/kwondu/region4web*

## The problem: the observation space inherits the action space’s granularity

A web agent perceives each page through an observation space and selects from an action space. Existing work mostly runs both at element-level granularity: the AXTree or DOM serialized as a list of indexed elements, sometimes filtered or truncated. The paper’s argument is that this granularity is right for actions (each action targets one element with one operation) but wrong for observation, whose job is page-state understanding, where what matters is how elements relate. Pages are organized into functional regions — groups of elements whose relations serve a shared purpose, such as site traversal or result narrowing. And purpose cannot be read off layout: a grid of product cards is many independent regions, while a structurally similar grid on a travel site can be one destination showcase.

Two measurements on Mind2Web (2,350 tasks, 137 websites) motivate the region as the observation unit. Consecutive actions have a median lowest-common-ancestor depth ratio of 0.48 against 0.22 for a random baseline, with 81.7% of pairs above that baseline — actions concentrate in tight subtrees, while a page receives a median of only 6 actions (90th percentile 13) against thousands of DOM nodes. And within a page, 52.9% of steps change nothing in the DOM and 74.4% stay below a 5% change ratio — so re-serializing the full observation at every step is largely redundant.

## What Region4Web is

The agent is a text-based web agent running in BrowserGym on desktop web: it perceives the page’s AXTree and acts by element id (bid) using the 15 BrowserGym actions (click, fill, select_option, …). On the CUA Radar board its architecture pattern is C13, “prune and restructure the text observation before the policy sees it”.

Region4Web is a two-stage framework that turns the AXTree into region-level observation:

1.  **Hierarchical decomposition.** A small model (about 536K parameters, three-layer MLPs) classifies every parent-child edge of the AXTree as cut or merge in a single bottom-up traversal; the subtrees held together by merged edges are the functional regions. The cut score is EdgeClassifier(x_v, r_c, r̄), where r_c is the child’s region representation and r̄ the sibling mean; the cut threshold is τ = 0.55.
2.  **Semantic abstraction.** A fine-tuned Qwen3-0.6B reads each region’s subtree and writes two orthogonal fields: a purpose (what the region is for) and a state summary (its current actionable context).

The training signal is annotations from a proprietary LLM, gpt-5-mini-2025-08-27. Source pages come from 500 websites sampled from the Tranco top-1M across 10 IAB categories, yielding 21,974 pages with extracted AXTrees from 253 websites. A verification stage keeps only pages where every region passes: 2,052 pages and 45,147 regions. Decomposition trains on binary edge labels with focal loss (α = 0.75, γ = 2.0) under teacher forcing; abstraction is supervised fine-tuning on the region annotations.

**PageDigest** is the deployment pipeline. On entering a page, the actor agent’s own backbone LLM reads the purposes and state summaries together with the task and action history, and selects task-relevant regions; selected regions are exposed as full AXTree subtrees (element granularity is preserved for acting), non-selected regions appear as purposes only. Within a page, PageDigest does not re-run Region4Web: it tracks added, removed and modified nodes against the page-entry AXTree. A view_all fallback action re-exposes every region’s full subtree. The actor’s policy is unmodified and no extra large model is added at inference.

## Results, as reported

All numbers below are WebArena online success rate (%): 812 long-horizon tasks, up to 30 steps each, five domains, run in BrowserGym with the Map domain routed to the live OpenStreetMap service. The original evaluator (deprecated gpt-4-1106-preview) was replaced with GPT-4o. No seeds or variance are reported.

| Configuration         | Alone | \+ PageDigest | Obs. tokens alone → with |
|-----------------------|-------|---------------|--------------------------|
| GPT-5.1               | 45.2  | 47.5          | 6,116 → 4,302 (−30%)     |
| Gemini 3.1 Flash-Lite | 39.4  | 41.6          | 6,705 → 3,207 (−52%)     |
| DeepSeek-V3.2         | 40.4  | 43.4          | 7,158 → 4,521 (−37%)     |
| Qwen3.5-27B           | 38.2  | 39.9          | 5,767 → 2,654 (−54%)     |
| SteP (GPT-4o)         | 39.5  | 38.7          | 7,136 → 3,693 (−50%)     |
| AgentOccam (GPT-4o)   | 40.6  | 41.3          | 4,025 → 3,365 (−16%)     |

Across the four backbones, observation length falls by 43% on average (6,437 → 3,671 tokens per step) while success rises by 2.3%p on average. On the two established agent methods, observation falls by 50% and 16% with comparable success. There are no offline step-accuracy numbers in the paper; everything above is online.

## What the paper’s own controls say

**Ablation** (WebArena-Lite, a 165-task subset, GPT-5.1): the backbone alone scores 48.5 at 5,410 tokens; adding Region4Web alone lifts success to 50.3 at 5,922 tokens; an element-level variant that drops Region4Web and replaces region selection with LCoW-style self-contextualization (keeping the same transition management) scores 46.1 at 4,013 tokens — a 26% cut that costs success; full PageDigest reaches 53.9 at 3,814 tokens — a 30% cut and 5.4%p above the backbone. The paper reads this as region-level observation supporting the actor where element-level compression hinders it.

**Task-scale accounting.** The median step observation drops 33% (3,077 → 2,066 tokens) and the median per-task total 25% (26,707 → 19,944 tokens). The task total decomposes into actor observation 73.9%, region selection 19.5%, and view_all 6.6%; selection is invoked 4.8 times per task on average, view_all in 38.1% of tasks with 0.64 calls on average.

**Failure audit.** Of 50 sampled failed trajectories (10 per domain), the backbone’s action selection accounts for 90.0%, environment errors 16.0%, region selection 10.0%, semantic abstraction 2.0%, decomposition 2.0%, and transition management none; under multi-cause attribution, 82.0% backbone capacity against 8.0% PageDigest regression.

**Held-out status.** Training pages come from Tranco-listed real-world websites; WebArena’s evaluation sites are self-hosted replicas, so the annotation pages and evaluation pages do not overlap.

## Where the evidence is thinner, in the paper’s words

- WebArena only: “Our evaluation focuses on WebArena, whose consistent AXTree fidelity supports the controlled comparisons our experiments require. Broader validation on real-world web environments … complements these results.”
- AXTree dependence: decomposition quality depends on “how completely each page exposes its accessibility semantics, with pages that render through canvas or rely on non-semantic markup providing weaker structural cues.”
- No seeds, standard deviations or significance tests accompany any table.
- The evaluator swap to GPT-4o is described but not validated against the original judge.
- The paper states code is available at github.com/kwondu/region4web; the radar record lists code as unclear.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **transfer**, under pattern C13 (prune and restructure the text observation). The score reflects what the paper reports: online WebArena evaluation, held-out training pages, two established agent baselines, a matched 30-step budget, token-cost reporting and a component ablation. Not reported: run variance, validation of the swapped evaluator, and verifiable code. The record flags AP18, lossy or state-inconsistent context management — the standing risk that a compact digest hides content the task needs; the paper’s in-benchmark answer is the view_all fallback, which fires in 38.1% of tasks. The radar did not rerun any experiment; every number here comes from the paper (version v1).
