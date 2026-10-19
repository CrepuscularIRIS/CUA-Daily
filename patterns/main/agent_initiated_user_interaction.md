# Let the Agent Decide When to Involve the User
_id: `agent_initiated_user_interaction` · sub-patterns: R02 · 1 candidate_pattern · 0 case · domains: board-induced (2026-10-19), from wave-1 weak fits (1 R) · outcome labels: none in this build_

**Definition.** Replace full autonomy with mixed initiative: the agent itself decides, step by step, whether to act, to ask the user a follow-up question (ASK action), to defer to a human when its predicted confidence is low, or to propose an action the user can veto and take over from. The move is the agent-side decision and its evaluation (timing, precision, human effort), not a safety gate on sensitive actions.

**Operational signature.** add an ASK / intervention channel to the action space (or a per-step confidence head) → build need-to-ask labels (human annotators, ambiguous-task synthesis by deleting instruction content, or critic-scored probing) → train or prompt the decision → insert the user's answer or actions into the history → score task success together with ask timing/precision and human step share, against autonomous and always-human baselines

**When to apply.** When instructions are often underspecified, personal preferences matter, or the policy fails on identifiable steps, and a human is available at a cost that can be counted.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [R02](../sub/R02.md) | candidate_pattern | Let the agent decide when to ask, defer to or hand control to the user | give the agent an explicit channel to the user (ASK action, confidence-thresholded intervention, suggest-then-execute with take-over), feed the answer back… |

## Success conditions
_Derived from the member card's When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Explicit, trained ask decision.** Asking is an explicit output (ASK action or confidence score) that is trained or fine-tuned and compared with prompt-only asking (HSR 86.87 vs 0.00 prompted; ASK timing precision up to 0.947) (2503.16465#board, 2503.24180#board).
- **Over-asking and under-asking both measured.** Ask/intervention precision or false-positive rate is reported next to recall and task success, not success alone (FPR ≤ 0.005; precision 0.08-0.19 for prompted detectors) (2503.24180#board, 2503.19537#board, 2503.16465#board).
- **Human effort reported with success.** Human step counts, intervention counts/rates or relative efficiency are reported (humans take 1.14 of 7.50 steps; ~19% intervention) (2501.16609#board, 2503.16465#board).
- **Autonomous and human-only (or always-ask) baselines.** The mixed-initiative mode is compared with the same agent fully autonomous and with humans alone or help at every step (0.95 vs 0.48 vs 0.89; 62% TSR with help at each step) (2501.16609#board, 2503.16465#board).
- **Sensitivity of the ask threshold swept.** The decision threshold or interaction sensitivity is varied and success vs intervention rate reported across settings (2503.16465#board).
- **Need-to-ask labels validated.** Labels for when interaction is needed are checked by inter-annotator agreement or human verification (kappa 0.64; 90% pass) (2503.19537#board, 2503.24180#board).

## Failure modes
_Derived from the member card's When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Oracle or simulated user answers.** Requested help is answered by the ground-truth action or by generated QA pairs instead of real users, so success with help credits the oracle (2503.16465#board, 2503.24180#board).
- **Asking cost not counted.** Success is reported without how often the agent asked or how many asks were unnecessary (prompted detectors over-ask with precision 0.08-0.19) (2503.19537#board).
- **Confidence or need labels from an unvalidated proprietary critic.** Confidence labels come from a strong model whose choice changes the result (HSR 86.87 vs 57.63 for another critic) without validation against humans (2503.16465#board).
- **Offline or tiny evaluation of interaction.** Asking is scored on static single-reference trajectories (early ASKs mis-scored) or on a few tasks with the authors as the humans (27 tasks, three authors) (2503.24180#board, 2501.16609#board).
- **Single-interaction scope.** At most one interaction or one omitted step per episode is modelled, and some kinds of asking are excluded by assumption (2503.19537#board, 2503.24180#board).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_Existing ids from the frozen domain profiles that apply to this pattern._
- **E15 (metric, common_practice).** Do not rest an agent capability claim on offline step accuracy alone; add an online benchmark or show the offline metric predicts online success.
- **E10 (metric, common_practice).** Validate an LLM/VLM judge used to label trajectories (here: confidence/need labels) against human labels.
- **E16 (reproducibility, common_practice).** Report mean and spread over runs for online numbers; human-in-the-loop studies additionally need more than the authors as participants.

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP7](../anti-patterns.md#ap7), [AP8](../anti-patterns.md#ap8), [AP22](../anti-patterns.md#ap22)
