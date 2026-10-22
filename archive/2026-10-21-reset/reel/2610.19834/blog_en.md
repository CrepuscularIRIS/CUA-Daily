# WebKD: a black-box teacher that edits a small web agent’s failures — in the student’s own style

*A CUA Radar reading of arXiv 2610.19834v1 (Md Farhan Ishmam and Kenneth Marino, University of Utah). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.19834v1 · Project page: https://web-teach-kd.github.io/ · No public code at v1 (supplementary, to be released upon acceptance).*

## The problem: distilling a teacher you can only talk to

Frontier web agents are competent but costly, and the paper’s motivating question is how much of a black-box frontier teacher’s competence can move into a small open-weight web agent “through text alone.” Closed teachers expose no logits, so token-level knowledge distillation, reverse-KL objectives, and on-policy distillation are all unavailable. The standard fallback, behavior cloning on teacher demonstrations, “trains the student on states it has never visited, and in a style it does not write in.” Classical fixes fall short for structured agents: DAgger relabels only the action, while a teacher that takes over from the failure point produces a suffix that is off-policy in both state and style. The paper’s diagnosis is a *perplexity premium*: a frontier teacher’s corrections are surprising to the student, “at several times the perplexity of the student’s own steps,” rising “by up to an order of magnitude” on the reasoning components while the action stays much closer to the student’s distribution. Under uniform SFT, the loss concentrates on the teacher’s wording rather than its decisions.

## What WebKD is

The agent is a text-based web agent in BrowserGym under the AgentLab harness, acting on desktop websites in a container. It observes the goal, an accessibility-tree (AXTree) serialization of the page, and its own response history (truncated to the most recent observation); history survives only through what the agent writes. Each step it emits a five-component response — think, plan, step, memory, action — and only the action (click, fill, goto, send msg, and other BrowserGym commands) executes; think/plan/memory form a scratchpad that persists across steps. Students are Qwen 3.5 4B and 9B and Gemma 4 E4B; the teacher is GPT-5.5 running under the same harness with no privileged input. On the CUA Radar board the paper sits in pattern K26 — build error-correction training data at the first mistake — under trajectory-level policy training.

WebKD runs one round of four phases:

1.  **P1, BC seed.** Fine-tune the base model on successful teacher rollouts; freeze.
2.  **P2, rollouts.** Run the seed student on the training tasks at temperature 0.01 with a 30-step budget; failed episodes become the edit substrate, solved ones a style pool.
3.  **P3, localize.** One teacher call per failed episode returns the earliest step that doomed the trajectory; the prefix is kept verbatim. (The paper proves such a first fatal step exists and is unique under a finite budget and deterministic transitions.)
4.  **P4, edit in style.** For each suffix step, one teacher call conditioned on exactly the observation the student saw, plus K = 3 verbatim exemplars of the student’s own writing; edits are never executed, and a grounding filter removes 9.9% of edited steps.

The corpus then trains the student from the seed with a premium-aware objective: each rationale span is weighted by Δ_s, its leave-one-out contribution to the corrected action’s probability under the frozen student (computable without teacher logits), and a role-asymmetric KL anchor (γ = 1 on think/plan/memory, ≈ 0 on action/step, β = 0.03) lets the action move to the teacher’s decision while holding the reasoning near the student’s prior. The training signal is thus teacher text plus the student’s own log-probabilities.

## Results, as reported

All numbers are online success rates (no offline step-accuracy metric appears), mean of 3 seeds with standard error; TimeWarp v6 is seen in training, v1–v5 are held out, and v6 has 103 tasks. Qwen 3.5 4B rows from Table 1:

| Method · Qwen 3.5 4B  | v1       | v2       | v3       | v4       | v5       | v6 (seen) |
|-----------------------|----------|----------|----------|----------|----------|-----------|
| Behavior Cloning (TW) | 27.5     | 28.5     | 27.8     | 26.2     | 28.2     | 29.8      |
| m-GRPO                | 30.1     | 27.2     | 26.2     | 28.2     | 30.1     | 30.4      |
| Off-policy takeover   | 24.4     | 24.3     | 25.2     | 23.3     | 27.2     | 25.6      |
| **WebKD**             | **37.9** | **36.3** | **35.3** | **38.8** | **36.9** | **41.1**  |

Zero-shot is 1.0 on v6 and action-only BC is 9.7, so the tasks are out of reach without training. On the seen v6, WebKD improves over the strongest baseline by 10.7 pp (Qwen 3.5 4B, 41.1 vs 30.4), 8.1 pp (Qwen 3.5 9B, 34.6 vs 26.5), and 5.5 pp (Gemma 4 E4B, 39.8 vs 34.3 takeover); on the unseen v1–v5 the margin over the strongest baseline is 3.0–10.6 pp and the seen–unseen gap stays below 5 pp. The teacher itself scores 70.9 on v6. On the live web (Online-Mind2Web), “numbers are low for all methods (below 8%)”; WebKD is the only method that clearly separates, roughly doubling the strongest baseline for the 9B student, and the gains there concentrate on easy, shorter-horizon tasks.

## What the paper’s own controls say

**Who edits, in whose style (Table 2, Qwen 3.5 4B).** Teacher edit + student style (in-context) reaches 41.10, against 33.01 for teacher edit + teacher style, 27.83 when the student proposes and the teacher judges/fixes, 25.89 for a two-pass student re-style, 24.27 for student-only editing, and 17.48 for off-policy teacher takeover. The paper’s read: without an external signal, the student cannot reliably tell which of its own decisions were wrong.

**The objective (Table 3).** WebKD’s weighted loss with the KL anchor scores 41.10, versus 37.43 for uniform cross-entropy with the same anchor, 37.54 for grounding- and consistency-based weightings, and 38.51 for WebKD’s loss without the anchor — a 3.6 pp edge over the other token-weighting schemes. Sweeping the anchor strength, β = 0.03 is best.

**Not just more epochs.** Training the BC (TW) recipe longer plateaus between 0.24 and 0.26 for the 9B student, while adding WebKD keeps improving through the third total epoch.

**Teacher capability matters.** Swapping the editor to Claude Opus 5 or Qwen-3.8 27B (same prompts and style exemplars) trains students to 33.3 and 26.9, versus 41.1 with GPT-5.5.

**Localization audit.** On 200 failed episodes with two blind human annotators, the teacher is never late under the strict budget reading (early on 93%, exact on 7%); under a loop-onset reading it is late on roughly 10%.

**Where the gains come from.** WebKD gets stuck in loops on about 8.7% of trajectories (zero-shot ~97%, BC ~62.5%) and reaches the correct page 202 times where no baseline exceeds 143; its largest remaining failure is right page, wrong answer (~24.3%). By task type: placing an order +25.9 pp (from 0% to 25.9%), counting/listing +9.5 pp (11.9% to 21.4%), lookup +8.7 pp, multi-hop +5.7 pp, verification +4.8 pp. Distillation mostly prunes redundant actions — scrolling −99.7%, key presses −24.5%, send msg +12.3% — with verifying steps/answer +14.6 pp and exiting loops +9.4 pp.

**Cost.** The BC phase makes 4,448 teacher calls (21.8 M prompt tokens); the correction stages (15 localization calls, 403 edit calls) are 17% of the pipeline’s 26.3 M prompt tokens. A fine-tune takes 1.0 GPU-hour on one H200, and the trained 4B student runs at a median 6.10 s per step (38.8 s per episode) against 12.80 s per step (68.1 s per episode) for the teacher in-harness.

## Where the evidence is thinner, in the paper’s words

- “The gains are mostly concentrated on the easy tasks, which have a shorter horizon” (on Online-Mind2Web).
- The per-task-type gains “should be read with caution: only the gains on placing an order and counting/listing have 95% confidence intervals that exclude zero” (categories have 9–29 examples).
- “The student still reaches only about half of the teacher’s success rate, leaving substantial room for improvement.”
- The imitation bound’s teacher term “is an estimate rather than a direct measurement of the term”; it is computed on 15 seed failures, where the teacher solves 14 of 15 takeovers.
- Terminal reward comes from an LLM judge; the paper does not validate the judge against ground truth, and task/judge defects stay roughly constant across methods (8–12 trajectories where labeled).
- No public code at v1; the paper says the source is in supplementary material “and will be released publicly upon acceptance.”

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **transfer**. The score reflects what the paper reports: online evaluation on TimeWarp v1–v6 and the live web, held-out interface versions, three seeds with standard error, strong baselines (BC, outcome-reward RL, and teacher-editing variants), and component ablations over edit source, style, and objective. The judgment record marks budget matching and cost reporting as unclear, code as unclear, and judge validation as untested, and it flags that the gains concentrate on easy, short-horizon tasks. The radar did not rerun anything; every number above comes from the paper (version v1).
