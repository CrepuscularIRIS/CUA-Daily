# Calibrate a Simulator or Digital Twin to the Real Target
_id: `calibrate_simulator_to_real` · sub-patterns: K08, K09, K10, K11 · 3 candidate_pattern · 1 case · domains: cua-agents (4 K / 0 C) · outcome labels: none in this build_

**Definition.** Build or correct a resettable simulator of the specific deployment environment — a task-scoped twin, a residual correction learned from logged real trajectories, or a calibrated twin whose synthetic data is debiased with a small real set — and use it for training or evaluation while real data remains in the loop. Most members are robotics/telecom; the GUI instance is an app twin (APPSim-Bench).

**Operational signature.** reconstruct the target environment (task-scoped) → replay/compare against real logs → learn residual or calibrate/debias → train or evaluate in the twin → co-train or validate on real data

**When to apply.** When the real environment is costly, unsafe or non-resettable for training, logged real trajectories or a small real validation set exist, and tasks touch only a bounded subset of the environment.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K08](../sub/K08.md) | candidate_pattern | Learn a residual correction that makes a simulator reproduce logged real trajectories | replay logged real state-action segments in the simulator from recorded start states and learn a residual (force or delta-action) model… |
| [K09](../sub/K09.md) | case | Calibrate a digital twin with sparse real measurements and debias its synthetic data | calibrate simulator parameters by gradient through a differentiable twin (EM over latent errors), train on posterior-sampled twins, and… |
| [K10](../sub/K10.md) | candidate_pattern | Build a task-scoped digital twin of the specific target environment | reconstruct (scan, re-implement, or synchronise) the specific deployment environment as a resettable simulator restricted to the… |
| [K11](../sub/K11.md) | candidate_pattern | Use the twin to harvest or target demonstrations, retrain with real data as anchor | run the current policy in the twin to collect successful rollouts or find failure states, add targeted (sim) demonstrations there, and… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Twin of the exact target, scoped to the task.** The twin reconstructs the specific deployment environment restricted to the task-relevant subset, with pruned regions as explicit placeholders; a twin of the exact target scene beats generic assets (90% vs 10% real success) (2403.03949#s1, 2609.07712#s1).
- **Resettable to logged real states.** The simulator can be reset to recorded real states and real states are measurable, so simulated and real next states can be compared step by step (2502.01143#s1, 2402.01086#s1).
- **Twin preserves real ranking.** Offline twin evaluation is shown to preserve the relative ordering of checkpoints/agents seen in the real environment (reported with 5-8x speedup) (2504.03597#s1).
- **Real data kept in the training mixture.** Distillation or retraining co-trains on real demonstrations (3.5x/2x over sim co-training); targeted twin demos are added where the policy fails (30 targeted sim demos ~= 30 extra real demos) (2403.03949#s3, 2504.03597#s2).
- **Correction model is more expressive than a global parameter fit.** A learned residual beats parameter SysID, which yields implausible parameters and little gain; debiasing uses context features that separate regions where the twin is wrong; RL fine-tuning in the corrected simulator beats training-free use of the correction (2402.01086#s2, 2502.01143#s1, 2507.07067#s3, 2502.01143#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Training without real anchor.** Policies trained without real demos exploit twin inaccuracies; sim-only demos can include behaviour that breaks synchronisation at deployment (2403.03949#s1, 2504.03597#s2).
- **Fidelity measured only indirectly.** Behavioural fidelity is measured only indirectly (placeholder residual up to 20.6%); dynamic content, network, personalisation and long-tail data are omitted (2609.07712#s1, 2504.03597#s1).
- **Single global bias correction.** Plain PPI with a single global bias underperforms real-only training where the twin is wrong; calibration cannot fully remove the gap of a limited-complexity simulator (2507.07067#s3, 2507.07067#s1).
- **Correction evaluated out of its regime.** Out-of-distribution regimes (1.75x pressure) break the residual and autoregressive error accumulates; at short horizons it is not better than open-loop/SysID (2402.01086#s1, 2502.01143#s1).
- **Bootstrap needs the real policy to succeed in the twin.** Step-function dependence on demo count: 0% when the real policy fails in sim (2403.03949#s2).
- **Construction cost unreported or prohibitive.** ~2 days wall-clock per task; full 23-DoF delta model impractical (reduced to 4-DoF); Bayesian twin training costs more compute (2403.03949#s3, 2502.01143#s1, 2507.07067#s2).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E34 (other, common_practice).** For a digital twin / simulated app used for training or evaluation, measure its realism and whether it preserves the ranking of agents or checkpoints seen in the real environment — _applies when_ a claim that a simulated app, synthetic site or digital twin substitutes for the real environment.
- **E32 (ablation, common_practice).** For training in a world model, include sim-only vs real-anchored vs SFT-only arms — _applies when_ a claim that policy training on world-model or simulated GUI rollouts improves agents.
- **E33 (metric, common_practice).** Back world-model or synthetic-environment fidelity scores with a second independent judge, human validation or executable checks, not a VLM judge from the same family as the training reward — _applies when_ a claim about GUI world-model or simulated-app fidelity measured with LLM/VLM judges.
- **E28 (other, common_practice).** Separate synthesis/exploration environments from evaluation (held-out apps/sites, filtered test queries) and report out-of-distribution transfer — _applies when_ a claim that self-generated tasks, explored transitions, memory or synthesised environments improve benchmark success.

## Cognitive barriers
- "A twin is a drop-in replacement for the real environment." Members keep real data in the loop and measure ranking preservation (2403.03949#s3, 2504.03597#s1).
- "Robotics sim-to-real tricks transfer to GUIs unchanged." GUI twins do not yet have continuous synchronisation (K10 transfer note); domain randomisation did not transfer as training augmentation (2604.14262#s2).

## Related anti-patterns
[AP1](../anti-patterns.md#ap1), [AP2](../anti-patterns.md#ap2)
