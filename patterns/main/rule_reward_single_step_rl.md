# Reinforce Single-Step Actions with Rule-Checked Rewards
_id: `rule_reward_single_step_rl` · sub-patterns: R01 · 1 candidate_pattern · 0 case · domains: board-induced (2026-10-19), from wave-1 weak fits (1 R) · outcome labels: none in this build_

**Definition.** Post-train a GUI grounder or step policy with R1-style group-relative RL on static, labelled states instead of (or after) SFT: sample several responses per state, score each with hand-written rules against the single reference action (format, action-type match, point-in-box / distance / box-size / IoU, argument match), and update with GRPO. No environment rollouts, terminal reward or learned judge are involved; the levers are data filtering by base-model difficulty, reward shaping, the reasoning template and the GRPO objective.

**Operational signature.** pool existing grounding / step-level datasets → sample the base model k times per state and keep informative (hard, not all-correct) samples → sample a response group per state → score with rule rewards against the label → GRPO update (optional SFT warm-up, KL) → evaluate on grounding and offline step benchmarks

**When to apply.** When per-step labels exist but no executable environment or reliable judge does, the base model already gets a fraction of states right (so group rewards vary), and the claim is about single-step grounding or action prediction rather than long-horizon task success.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [R01](../sub/R01.md) | candidate_pattern | Offline single-step GRPO with rule-checked action and grounding rewards | take static states with one labelled action, filter them by base-model sampling, score a response group with rules against the label, and update with GRPO… |

## Success conditions
_Derived from the member card's When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Same-data, same-backbone SFT baseline.** RL is compared with SFT of the same backbone on the same curated samples (3B ScreenSpot 80.08 vs 63.55, ScreenSpot-Pro 25.23 vs 13.80; WorkArena 46.79 vs 30.20), not only with SFT models trained on different, larger data (2504.10458#board, 2505.22942#board, 2503.21620#board).
- **Difficulty filtering by base-model sampling, ablated.** Training states are selected by sampling the base model (drop all-correct / all-wrong, or keep failed hard samples) and the filter is compared with random or unfiltered data (ScreenSpot-Pro 40.0 vs 27.1 unfiltered with sparse reward) (2503.21620#board, 2504.10458#board, 2505.12370#board, 2505.15810#board).
- **Reward components ablated and checked for hacking.** Each reward term (point vs box/IoU, dense vs sparse, box-size constraint, action-type term) is ablated and the paper inspects whether the policy games it (box sizes over training, response lengths, repeated actions) (2505.15810#board, 2505.22942#board, 2503.21620#board, 2505.12370#board).
- **Reasoning template matched to the task and ablated.** Thinking vs direct answering is compared for the target task (grounding: DAST+NOTHINK ScreenSpot-Pro 33.5 vs 17.8 thinking; web navigation: long-reasoning SFT helps) (2503.21620#board, 2505.15810#board, 2505.22942#board).
- **Out-of-domain or online evidence beyond the training distribution.** Gains are shown on platforms or benchmarks outside the training data (mobile-only training tested on desktop/web and ScreenSpot-Pro) or on an online/live benchmark (WorkArena, WebVoyager), not only on in-distribution offline steps (2503.21620#board, 2505.22942#board, 2506.09373#board).
- **SFT warm-up and a second backbone for agent tasks.** For multi-step agent tasks, GRPO starts from an SFT warm-up compared against direct initialisation, and the gain is repeated on another backbone family (Llama-3.1-8B 32.41 vs 20.48 SFT) (2505.22942#board).

## Failure modes
_Derived from the member card's When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Single-reference, single-step evidence for an agent claim.** Rewards and evaluation use exact match to one reference action on static states, multi-step tasks are cut into independent steps, and no online multi-step success is reported (no "aha moment" from single-image non-interactive training) (2505.22942#board, 2504.10458#board, 2503.21620#board).
- **Shaped reward gamed by the policy.** Hit/IoU/text-similarity or piecewise-dense rewards are hacked (boxes shrink or grow, the most common action is repeated, tokens are emitted after the action tag) or GRPO length normalisation favours long wrong answers, and this is not checked or regularised (2505.15810#board, 2505.22942#board).
- **RL gain confounded with data or backbone.** The headline comparison is against SFT models with different backbones and far larger different data (3K vs 13M-14M), so the share due to RL is not isolated (2505.15810#board, 2504.10458#board, 2505.12370#board).
- **Aggregate grounding hides icon and professional-screen weakness.** Only averages are emphasised while icon accuracy on ScreenSpot-Pro stays low (16.8 vs 49.5 text; 21.0 vs 63.5) (2505.15810#board, 2505.12370#board).
- **Small gains on high-level tasks or few model sizes.** On high-level/multi-step offline tasks the gain over the zero-shot base is small (56.13 vs 50.53), or only 3B/7B are tested, so scaling is unknown (2504.10458#board, 2505.12370#board).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_Existing ids from the frozen domain profiles that apply to this pattern._
- **E15 (metric, common_practice).** Do not rest an agent capability claim on offline step accuracy alone; add an online benchmark or show the offline metric predicts online success.
- **core-E06 (other, common_practice).** Offline single-reference matching under-counts alternative valid paths; pair it with online/executable success or show offline-online correlation.
- **core-E01 / core-E02 (baseline / dataset).** Compare grounders against SeeClick, CogAgent, OS-Atlas, UGround on ScreenSpot split by text vs icon, and report ScreenSpot-Pro per group for high-resolution claims.
- **E22 (scale, common_practice).** Report results across backbone sizes, since GUI data/RL recipe gains shrink with model size.
- **E09 (baseline, common_practice).** Compare against an SFT-only model trained on the same data.

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP7](../anti-patterns.md#ap7), [AP9](../anti-patterns.md#ap9), [AP10](../anti-patterns.md#ap10), [AP16](../anti-patterns.md#ap16)
