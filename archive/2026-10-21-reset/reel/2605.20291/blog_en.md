# Weasel: choosing the right 10K trajectory steps beats fine-tuning on all 52K, for out-of-domain web agents

*A CUA Radar reading of arXiv 2605.20291v2 (Pesaran Zadeh, Choi, Lù, Reddy, Kim; ICML 2026). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2605.20291v2 · Code: https://github.com/fatemehpesaran310/weasel*

## The problem: two costs of offline training data

Web agents fine-tuned on a fixed set of trajectories and environments tend to break when deployed on unseen websites, layouts, or interaction patterns; the paper also notes that most recent work is trained and evaluated in-benchmark, which hides this drop. Offline interaction data makes things worse twice over. Expert trajectories are noisy and redundant — a single AgentTrek trajectory can hold up to 45 state-action pairs while only a fraction is goal-relevant — and each state is a linearized accessibility tree (AXTree) that can reach 180K tokens, so training on full data is slow and prone to overfitting site-specific artifacts. A further hazard for reasoning-native models: fine-tuning on traces written in another model’s style “can be detrimental” and “may degrade performance, sometimes even falling below the base model before fine-tuning.”

## What Weasel is

Weasel (WEb Agents with trajectory SELection) is not a new agent architecture but a data selection and curation method for offline training. The underlying agent is a text-based web agent in the BrowserGym ecosystem: it observes the goal, the interaction history, and the linearized AXTree of the page, and acts with node-grounded actions that reference an AXTree element by its bid (click, type, scroll) plus non-node actions (goto, noop). Three base policies are studied — Qwen2.5-7B-Instruct, Gemma3-4B-IT, and the reasoning-native Qwen3-8B — each fine-tuned with a LoRA adapter of rank 8. On the CUA Radar board the paper sits under trajectory-level policy training, sub-pattern K25: augment action traces with generated reasoning.

Curation runs once, before training:

1.  **Target-centered pruning.** For each node-grounded action, keep only a window of 2w+1 AXTree nodes centered at the gold target bid (w = 60; a fixed-length prefix for non-node actions). This keeps about 32% of the original tokens and gives a 2x training speed-up on its own.
2.  **Scoring.** Unary importance Phi(t) = BERTScore(goal, state), computed with roberta-large; pairwise diversity D(i, j) = max of the state and the answer pseudo-distances, each 1 − BERTScore. Lambda trades them off at 1.
3.  **Greedy selection.** Seed with the best-scoring pair, then repeatedly add the step with the largest marginal gain until the budget of T0 = 3 steps per trajectory is met. From 52K AgentTrek steps this keeps 12K (16K from NNetNav-Live), uniformly sampled down to 10K for training.
4.  **Self-reasoning synthesis.** Only for reasoning-native Qwen3-8B: the base model itself regenerates the think and memory blocks conditioned on goal, history, pruned state, and the expert action, which is kept verbatim — the paper’s fix for the style mismatch above.

The training signal is therefore plain imitation of expert actions on a curated subset; the selection signal is embedding similarity, and no environment interaction or RL is involved in training.

## Results, as reported

All numbers below are online success rates (SR) collected with the AgentLab framework, judged by GPT-4.1-mini on WebArena-Lite and GPT-4-1106-preview on WebArena. The setting is zero-shot transfer: trained on AgentTrek, evaluated on WebArena-Lite, WebArena, MiniWob, and WorkArena (L1/L2) with no additional fine-tuning. The paper reports aggregate SR over the full evaluation set; no seeds or variance are given. Epochs: 4 for Qwen2.5-7B, 2 for Gemma3-4B and Qwen3-8B.

Qwen3-8B, trained on AgentTrek:

| Variant | WebArena-Lite | WebArena | MiniWob | WorkArena L1 | WorkArena L2 | Training |
|----|----|----|----|----|----|----|
| Qwen3-8B (base) | 16.4 | 18.0 | 61.1 | 35.2 | 1.7 | – |
| Full 52K steps | 17.7 | 18.2 | 59.4 | 33.3 | 2.1 | 88.5 hr, 1.0x |
| Pruning 52K | 17.6 | 12.7 | 40.3 | 15.5 | 2.6 | 44.0 hr, 2.0x |
| Sampling 10K | 16.5 | 17.5 | 61.4 | 33.9 | 3.4 | 7.0 hr, 12.6x |
| LLM-Judge 10K | 19.4 | 16.6 | 61.9 | 35.2 | 3.8 | 7.0 hr, 12.6x |
| **Weasel 10K** | **21.2** | **19.2** | **61.9** | **38.8** | **4.3** | 8.3 hr, 10.7x |

The abstract highlights a +4.8 zero-shot gain on AgentTrek-to-WebArena-Lite with Qwen3-8B. The same ordering holds for the other models: Qwen2.5-7B-Instruct reaches 14.5 / 9.5 / 48.0 / 12.4 / 4.7 with Weasel in 12.0 hr (11.3x) versus 10.9 / 8.7 / 44.6 / 12.1 / 0.4 for full 52K-step SFT in 136.0 hr; Gemma3-4B-IT reaches 11.5 / 5.5 / 30.6 / 4.5 / 3.0 in 6.4 hr (12.5x) versus 9.1 / 4.3 / 28.6 / 3.3 / 0.0 in 80.0 hr. Replacing the training set with NNetNav-Live (Table 2, Qwen2.5-7B) keeps the conclusion: Weasel 12.1 / 8.3 / 41.8 / 7.6 / 6.8 at 9.7x, above full SFT (10.9 / 6.9 / 38.9 / 5.2 / 6.4) and uniform sampling (10.3 / 7.4 / 32.3 / 7.0 / 6.0). Overall the paper claims 9.7-12.5x training speed-ups.

One offline result, kept separate from the online numbers above: with scoring swapped to SigLIP2 screenshot embeddings and CLIP goal-image alignment, the selection alone transfers to the multimodal Android in the Wild setting (Qwen2.5-VL-3B-Instruct, held-out 500-example subset, 3.1K of a 10K pool): base 4.4, random selection 5.8, Weasel 6.6 step accuracy. The paper calls these results preliminary.

## What the paper’s own controls say

- **Matched 10K-step budget** (Qwen2.5-7B, WebArena-Lite): uniform sampling 9.1, LLM-as-judge selection 8.5, length-sorted filtering 5.5 and 10.9, versus Weasel 14.5.
- **Pruning controls at the same 32% token budget** (Table 3): Prune-by-Bid 8.5, Semantic 9.1, Target-centered + Semantic 7.3, Target-centered 10.9, against 10.3 for unpruned 10K data; every variant gives the same 2.0x speed-up. Shifting the window away from the target in Figure 5 lowers SR roughly linearly.
- **Objective ablations**: unary importance alone 10.9, diversity alone 7.9, both 14.5; state-only diversity 9.7 and answer-only 13.9; goal-state importance beats goal-summary (12.7) and goal-reason (9.1) pairings.
- **Selection times reasoning synthesis** (Qwen3-8B, 10K, 2 epochs): random SFT 16.5, random + synthesis 18.2, Weasel without synthesis 17.0, both 21.2 — the two components are complementary.
- **Greedy quality**: on 1,877 NNetNav trajectories with T0 = 3 (up to 7,770 candidate subsets each), the greedy pick matches the exact optimum in more than 96% of trajectories, lands in the top 1% in 99.7%, and its objective ratio is 0.9999 ± 0.0005.
- **Robustness knobs**: swapping BERTScore for Qwen3-Embedding-0.6B gives 12.7 and Qwen3-Embedding-4B gives 14.5; lambda 0.5 / 2.0 / 4.0 give 10.9 / 12.1 / 10.3; window 40 / 80 give 12.7 / 12.8; T0 = 0.25T gives 12.1 — all below but near the 14.5 default.
- **Cost**: one-time preprocessing of full AgentTrek costs 7.7 h (importance 0.35 h, diversity 0.50 h, greedy under 0.02 h, reasoning synthesis 7.5 h), against 136 h for one full-data SFT run.

## Where the evidence is thinner, in the paper’s words

- No variance: “We report aggregate SR over the full evaluation set for each benchmark.”
- Success is judged by LLMs (GPT-4.1-mini, GPT-4-1106-preview); the judgment record marks this judge as not validated against ground truth in the paper.
- Pruning is not universally safe: for Qwen3-8B, Pruning 52K drops MiniWob to 40.3 (full data: 59.4), and on NNetNav-Live the pruning-only row falls to 5.5 / 3.2 / 38.4 / 1.8 / 1.3.
- The multimodal transfer is labelled preliminary, with small absolute accuracies (4.4 to 6.6).

## CUA Radar’s read

CUA Radar scores this paper **63 (★★)**, evidence level **transfer**, sub-pattern K25. The score reflects what the paper reports: online evaluation, genuinely held-out environments (trained on AgentTrek or NNetNav, evaluated zero-shot elsewhere), SFT baselines under the same 10K-step budget, cost reporting, component ablations, and released code. The judgment record flags the missing variance/seeds, the unvalidated LLM judge, and the reasoning-style-mismatch instability that self-reasoning synthesis is designed to fix. The radar did not rerun anything; every number here comes from the paper (version v2).
