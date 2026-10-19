# Reward with Learned Outcome and Process Judges
_id: `learned_outcome_and_process_judges` · sub-patterns: K16, K17, K18, K19, C25 · 2 candidate_pattern · 3 case · domains: cua-agents + cua-agents-core (4 K / 1 C) · outcome labels: none in this build_

**Definition.** Replace or complement executable checkers with model-based judges of success: a passive LLM/VLM outcome reward model over final or key screenshots, an abstaining ensemble that labels only unanimous cases, a tool-using verifier that probes the preserved terminal state, or a process reward model scoring every step. The judge's output is used as reward, filter, sampling weight or evaluation. From `cua-agents-core`: LLM trajectory judges for success and safety labels (C25).

**Operational signature.** collect trajectory (final/key screenshots, history, live terminal state) → judge success per trajectory or per step (single, ensemble, agentic probe, PRM) → use as reward, filter or weight → validate judge against humans

**When to apply.** When tasks have no executable checker (live sites, free-form tasks) but completion is visible in the observed or probeable final state.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K16](../sub/K16.md) | candidate_pattern | Judge trajectory success with a passive LLM/VLM outcome reward model | give an LLM/VLM the task plus final screenshot/HTML, selected key screenshots, or the action history, and have it output a binary or graded… |
| [K17](../sub/K17.md) | case | Emit a reward only when diverse judges unanimously agree, else abstain | query several VLM judges with different models/prompts (chosen for opposite precision/NPV biases) and label only unanimous cases |
| [K18](../sub/K18.md) | case | Verify outcomes with a tool-using agent that probes the preserved terminal environment | progressively escalate from final screenshot to retrieved intermediate screenshots to read-only shell/Python and GUI probing of the live… |
| [K19](../sub/K19.md) | case | Dense step-level process rewards for multi-turn GUI RL | score every step with a PRM trained on human step labels and use the scores as dense rewards (PPO with GAE) or as GRPO accept/reject reward |
| [C25](../sub/C25.md) | candidate_pattern | Score agent trajectories with an LLM judge | prompt an (M)LLM with the task, the agent's answer and trajectory screenshots or an action/reasoning trace to emit success and safety labels |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Judge agreement with humans reported.** The judge is validated against human labels; key-point extraction plus key-screenshot selection keeps agreement over long trajectories (~85-87% with humans); full-trajectory screenshots raise GPT-4V agreement to kappa 0.70, matching inter-annotator agreement (2504.01382#s1, 2401.13919#s3).
- **Completion visible in the judged state.** Tasks are phrased so that completion is visible in a single screenshot or final-state HTML (2406.11896#s2, 2411.02337#s2).
- **Graded scores as weights, not hard filters.** Graded judge scores are used as sampling weights rather than hard filters (2412.19723#s2).
- **Judge acquires hidden state actively.** The verifier escalates from final screenshot to intermediate screenshots to read-only shell/GUI probing of the preserved terminal environment (verifier SR 83.1% vs actor 55.9%) (2602.00575#s1).
- **Reliability over coverage via abstention.** Several judges with different models/prompts, chosen for opposite precision/NPV biases, label only unanimous cases, and their errors are shown to be not fully correlated (2510.18596#s1).
- **Human-labelled, in-distribution PRM.** A process reward model is trained on human step labels from the same environment (94.9% held-out accuracy) (2509.23738#s1).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Judge sees only partial state.** Judges see only the last screenshots, so mid-trajectory or hidden-state errors are missed (2412.19723#s2, 2510.18596#s2).
- **Disagreement with humans on free-form tasks.** ~13-20% disagreement with humans; free-form tasks lower precision (2411.02337#s2, 2504.01382#s1, 2406.11896#s2).
- **Systematic bias treated as noise.** Zero-mean reward noise only adds variance, but systematic judge bias is not removed by more rollouts; judges show self-preference bias, count partial progress as success and are fooled by injection phrasing (2605.06732#s3, 2401.13919#s3, 2506.14866#s2).
- **Reward exploitation not analysed.** Policy exploitation of judge errors / reward hacking and OOD apps are not analysed, often with a single run (2406.11896#s2, 2411.02337#s2, 2509.23738#s1).
- **Coverage loss from abstention unvalidated in RL.** Recall/specificity drop sharply, abstention may bias kept samples, and the ensemble is not validated in an RL loop (2510.18596#s1).
- **Generic judge assumed adequate.** Visual reasoning dominates judge quality; GUI-specialised reward models are no better than base VLMs; a learned PRM stays below oracle reward on offline single-step GRPO (2510.18596#s2, 2509.23738#s3).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E10 (metric, common_practice).** Validate an LLM/VLM success judge or outcome reward model against human labels on trajectories from agents not used to build it (agreement/accuracy, plus the resulting success-rate gap) — _applies when_ a method that uses an LLM/VLM judge, ORM or reflector to label trajectory success for evaluation, filtering or reward.
- **E11 (metric, common_practice).** Report judge reliability separately for positive and negative verdicts (precision and NPV, or precision/recall per class), not only overall accuracy — _applies when_ a claim that a GUI-agent judge, PRM or ORM is reliable enough to serve as reward or evaluator.
- **E12 (ablation, common_practice).** When a learned judge or PRM is the RL reward, show downstream policy gain against an alternative reward (rule/script checker, ORM vs PRM, another judge), and address reward hacking or bias — _applies when_ a claim that a learned reward model or verifier improves GUI-agent RL training.
- **E14 (ablation, single_source).** For PRMs or step-level verifiers, ablate the label source (human vs GPT-4o-generated step labels) — _applies when_ a claim that a process reward model for GUI steps improves RL or best-of-N.
- **core-E16 (reproducibility, common_practice).** Validate the success checker or LLM judge against human labels (agreement, kappa or F1) when a benchmark uses fuzzy matching or an LLM judge — _applies when_ a new benchmark or evaluation protocol whose success or safety labels come from fuzzy matching, VQA models or an LLM judge.

## Cognitive barriers
- "A judge with high overall accuracy is a safe reward." Precision and NPV differ, systematic bias persists across rollouts (2605.06732#s3), and exploitation is rarely tested.

## Related anti-patterns
[AP4](../anti-patterns.md#ap4)
