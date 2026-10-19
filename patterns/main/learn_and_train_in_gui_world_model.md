# Learn GUI Dynamics and Train in Them
_id: `learn_and_train_in_gui_world_model` · sub-patterns: K03, K04, K05, K06, K07, K35 · 5 candidate_pattern · 1 case · domains: cua-agents (6 K / 0 C) · outcome labels: none in this build_

**Definition.** Learn a model of how a GUI or web page changes in response to actions — in text, renderable code, object slots, or as an auxiliary objective inside the policy — from transitions harvested in real environments, and use it as a training substrate: imagined rollouts for policy learning, or transition objectives that shape the policy's representation. The gain is claimed from dynamics knowledge, not from extra task demonstrations.

**Operational signature.** harvest real (s, a, s') transitions (often goal-free) → train a next-state predictor (text diff, HTML, slots) or transition objective → roll out the policy in imagination or pretrain on transitions → fine-tune with real data as anchor

**When to apply.** When real interaction is expensive or non-resettable, transitions are mostly determined by visible state, and a pool of real trajectories exists to anchor training.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K03](../sub/K03.md) | candidate_pattern | Learn a text-space web transition model from real interaction logs | train an LLM on real (o_t, a_t, o_t+1) web transitions to predict the next state in text (an abstracted natural-language change… |
| [K04](../sub/K04.md) | candidate_pattern | Predict the next GUI screen as renderable HTML code | represent the next GUI state as HTML (with placeholders/SVG or diffusion-filled image slots), generate it from (screenshot, action, goal) —… |
| [K05](../sub/K05.md) | candidate_pattern | Train or fine-tune the policy on world-model rollouts, anchored with real data | roll out the policy inside a learned world model (short horizons), score/filter the imagined trajectories (self-assessed reward, rule… |
| [K06](../sub/K06.md) | candidate_pattern | Pretrain the policy backbone on transition-understanding objectives | before agent fine-tuning, train the VLM policy on self-supervised tasks over (s_t, a_t, s_t+1) triples: forward next-state description,… |
| [K07](../sub/K07.md) | candidate_pattern | Harvest a transition corpus by goal-free exploration plus VLM captioning | random-walk or structured-walk real web pages/apps without tasks, deduplicate and filter transitions, and have a large VLM caption each… |
| [K35](../sub/K35.md) | case | Object-centric slot world model for relational dynamics | encode frames into object slots and predict next slots with an action-conditioned transformer separating temporal and relational attention |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Abstracted transition target.** The world model predicts an abstraction of the change (Hungarian-matched element diff rewritten in natural language, or a delta from a retrieved HTML of the same app) rather than the raw full next state; raw-tree targets drop downstream SR 22.0 -> 14.5, and retrieval-grounded delta generation scores 73.51 vs 67.46 without RAG (2410.13232#s1, 2608.05891#s1).
- **Transitions harvested from real execution.** Training transitions come from executing in real pages/apps (goal-free random or structured walks, deduplicated structurally and visually, e.g. MinHash plus pHash) and are captioned by a VLM, not imagined by a teacher (2604.02345#s1, 2411.06559#s2).
- **Short imagination horizon.** Imagined rollouts used for policy training are kept short (best 4-5 steps), with the horizon ablated (2601.22149#s2).
- **Real-data anchor in the training mixture.** Imagined trajectories are mixed with real expert or public trajectories (~40% real gives most of the gain), and the world model is fine-tuned on the target environment family (2601.22149#s2, 2608.05891#s3, 2602.14721#s2).
- **World-model reward is not visual-only.** When the world model is itself RL-trained, its reward combines visual alignment with an action-consequence (transition validity) judge; either alone is worse and visual-only reward is reward-hacked (2602.09856#s1).
- **Transition objective compared under matched data.** A forward-dynamics pretraining objective is compared against inverse/backward variants with identical post-training data (EM 53.9/54.4 vs 51.0 baseline); explicit auxiliary tasks restore verification/reversal ability eroded by regular GUI pretraining (87.56 verification, 93.81 reversal) (2604.02345#s3, 2604.02345#s2, 2506.08012#s3).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Policy trained on imagination alone.** Purely imagined training underperforms SFT or lowers ATP below the base model (2601.22149#s2, 2608.05891#s3).
- **Long dreams or full-page prediction.** Long dreams degrade through compounding hallucination and only ~1/10 world-model rollouts pass quality checks; full-page transitions are much harder (~12% completely wrong) (2601.22149#s2, 2608.05891#s3, 2601.22149#s1).
- **Next state depends on hidden server state.** The model has no access to server-side state, real assets or pixels by construction; counterfactual imagination accounts for 42% of sampled errors (invented products) and visual similarity drops OOD (2410.13232#s1, 2601.22149#s1, 2602.09856#s1).
- **Optimistic, sycophantic predictions.** The world model predicts overly optimistic outcomes that cater to the agent's action, with poor detailed content generation (2602.14721#s1).
- **Fidelity scored by an LLM judge from the training family.** Intrinsic metrics are LLM-judged rather than executed, or the same VLM family serves as RL reward and evaluation judge, which may inflate gains (2601.22149#s1, 2602.14721#s1, 2602.09856#s1).
- **No real-environment synthesis baseline or scaling ceiling.** No comparison against equal-size synthesis in the real environment; gains saturate (~20K rollouts) and taper with data scale; filtering stages and caption quality are not ablated (2602.14721#s2, 2608.05891#s3, 2411.06559#s2, 2604.02345#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E30 (metric, common_practice).** Evaluate a GUI world model by downstream agent success and closed-loop (multi-step, autoregressive) rollouts, not only teacher-forced one-step fidelity — _applies when_ a claim that a GUI/web world model (text, code or image next-state predictor) is accurate or useful.
- **E31 (ablation, common_practice).** Ablate imagination / lookahead horizon, since world-model errors compound beyond 1 (lookahead) or about 5 (training) steps — _applies when_ a method that plans or trains with multi-step rollouts inside a learned GUI world model.
- **E32 (ablation, common_practice).** For training in a world model, include sim-only vs real-anchored vs SFT-only arms — _applies when_ a claim that policy training on world-model or simulated GUI rollouts improves agents.
- **E33 (metric, common_practice).** Back world-model or synthetic-environment fidelity scores with a second independent judge, human validation or executable checks, not a VLM judge from the same family as the training reward — _applies when_ a claim about GUI world-model or simulated-app fidelity measured with LLM/VLM judges.
- **E26 (baseline, single_source).** Compare a synthetic-trajectory recipe against an instruction-first / task-driven synthesis baseline with the same executor and similar data size — _applies when_ a claim that an exploration-first, reverse or world-model data-synthesis method yields better GUI training data.
- **E27 (scale, common_practice).** Show a data-scaling curve (fraction or count of synthetic samples vs downstream score) and say where it saturates — _applies when_ a claim that synthetic GUI grounding, transition or trajectory data improves agents.
- **E28 (other, common_practice).** Separate synthesis/exploration environments from evaluation (held-out apps/sites, filtered test queries) and report out-of-distribution transfer — _applies when_ a claim that self-generated tasks, explored transitions, memory or synthesised environments improve benchmark success.

## Cognitive barriers
- "A better world model directly yields a better policy." Purely imagined training can fall below SFT; the real anchor carries much of the gain (2601.22149#s2, 2608.05891#s3).
- "Theory bounds the imagination gap." The available bound is loose by 1-2 orders of magnitude at the median (2605.06732#s1).

## Related anti-patterns
[AP1](../anti-patterns.md#ap1), [AP2](../anti-patterns.md#ap2), [AP3](../anti-patterns.md#ap3), [AP5](../anti-patterns.md#ap5), [AP8](../anti-patterns.md#ap8), [AP9](../anti-patterns.md#ap9), [AP10](../anti-patterns.md#ap10)
