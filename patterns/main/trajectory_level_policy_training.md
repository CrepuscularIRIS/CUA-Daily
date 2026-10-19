# Train the Policy on Own, Replayed and Corrected Trajectories
_id: `trajectory_level_policy_training` · sub-patterns: K20, K21, K25, K26, C21 · 4 candidate_pattern · 1 case · domains: cua-agents + cua-agents-core (4 K / 1 C) · outcome labels: none in this build_

**Definition.** Improve a GUI policy by shaping the trajectories it trains on: online RL on sparse terminal reward with learned value baselines and filtered/replayed data, semi-online rollouts over expert trajectories, reasoning augmentation of action-only traces, and error-correction/recovery data built at the first mistake. From `cua-agents-core`: reasoning annotations synthesised by a strong MLLM for SFT, trained as a mixture of reasoning levels (C21).

**Operational signature.** initialise from SFT/offline data → roll out (online, semi-online over expert traces) → filter, relabel, augment with reasoning or first-error corrections → update with constrained RL, SFT or DPO

**When to apply.** When an SFT-initialised policy and a terminal success signal (checker or judge) exist, and failures concentrate at identifiable steps.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K20](../sub/K20.md) | candidate_pattern | Online RL on sparse terminal reward with learned value baselines and filtered/replayed data | train step- and instruction-level critics with cross-entropy on the terminal (judge) reward, compute mixed TD/MC advantages, and update the… |
| [K21](../sub/K21.md) | case | Semi-online RL: roll out over expert trajectories with own history and patched mismatches | step through static expert trajectories conditioning on the policy's own generated history, patch mismatched actions with the expert action… |
| [K25](../sub/K25.md) | candidate_pattern | Augment action-only traces with generated reasoning | prompt a VLM with the ground-truth action (or bootstrap from an early model and keep thoughts whose sampled action matches) to write… |
| [K26](../sub/K26.md) | candidate_pattern | Build error-correction and post-error recovery training data at the first mistake | locate the first erroneous step of an agent trajectory (human or MLLM), create a corrected action for that step and a reflection/recovery… |
| [C21](../sub/C21.md) | candidate_pattern | Synthesize reasoning annotations for demonstrations with a strong MLLM, then SFT a screenshot policy | have a proprietary model rewrite each demonstration step into plan/thought/reflection + grounded action (with hindsight before/after… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **SFT/offline initialisation before online RL.** Online RL starts from an SFT/offline-trained policy; ~1k online trajectories suffice on short AitW tasks (2406.11896#s1, 2411.02337#s3).
- **Constrained updates with success replay.** Updates are KL-constrained to the previous-phase policy and replay successful trajectories within a perplexity band; tasks are curriculum-filtered for informativeness (2411.02337#s3, 2406.11896#s1).
- **First-error correction and recovery data.** Training data corrects the first erroneous step and adds a recovery action after it; reflection data raises level-2 success 14.58% -> 23.61%, online reflection tuning 23.61% -> 34.72%, and DPO on corrected vs erroneous actions improves OSWorld (72B 18.8 -> 22.7) (2506.08012#s1, 2506.08012#s2, 2501.12326#s1).
- **Reasoning kept only if action-consistent.** Generated per-step thoughts are kept only when the sampled action matches ground truth (bootstrapping), avoiding superficial rationalisation (2501.12326#s2, 2412.04454#s2).
- **Offline proxy validated against online success.** A semi-online/offline protocol is shown to correlate with online success (SOP vs AndroidWorld, R^2=0.934) (2509.11543#s3).
- **Mixed reasoning levels with the decoding level ablated.** Reasoning annotations synthesised by a strong MLLM are trained as a mixture of levels and the level used at decoding is ablated (mixing L1/L2/L3 and decoding L2: OSWorld 18.5% vs 13.1% L2-only; reflective long CoT 11.5% -> 15.3%) (2508.09123#s2, 2508.09123#s3, 2312.08914#s3).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Unregularised multi-phase updates.** Without KL or replay, performance degrades over phases; replaying failures destabilises (2411.02337#s3).
- **Exact-match correctness rejects valid alternatives.** Valid alternative actions are treated as mismatches and non-expert branches never see real next states (2509.11543#s1, 2509.11543#s3).
- **Short tasks, subsets, few repeats.** Evaluated on short tasks only, with few repeats and on subsets (WebArena-Lite) (2406.11896#s1, 2411.02337#s3).
- **Gains not shown across model sizes.** Gains shrink with model size (2509.11543#s1).
- **Unvalidated error labels and environment assumptions.** MLLM verifier/first-error labels are not validated against humans, the method assumes Back restores the previous screen, and covers visual/grounding but not high-level planning errors; reflection tuning is not isolated by ablation (2506.08012#s1, 2506.08012#s2, 2501.12326#s1).
- **Reasoning noise from source traces.** Single-sample system-2 decoding is worse in-domain (irrelevant/hallucinated reasoning); redundant actions in source trajectories yield wrong reasoning (7.8%); an observation-description (L3) level misleads at inference and self-correction is conjectured rather than isolated (2501.12326#s2, 2412.04454#s2, 2508.09123#s3, 2508.09123#s2).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E09 (baseline, common_practice).** Compare GUI online-RL methods against DigiRL, WebRL, filtered BC / AWR and an SFT-only model trained on the same data — _applies when_ a claim that an RL algorithm (online, offline-to-online, semi-online or model-based) improves a GUI/web agent.
- **E15 (metric, common_practice).** Do not rest an agent capability claim on offline step accuracy (AndroidControl, Multimodal-Mind2Web, GUI Odyssey) alone; add an online benchmark or show the offline metric predicts online success — _applies when_ a claim of improved agent capability measured with offline, teacher-forced step metrics.
- **E22 (scale, common_practice).** Report results across backbone sizes (e.g. 7B and 32B/72B), since gains from GUI data/RL recipes shrink with model size — _applies when_ a claim that a training recipe generalises across policy backbones.
- **E29 (ablation, single_source).** Ablate error-correction/reflection data against filtered behaviour cloning at the same iteration count — _applies when_ a claim that reflection, self-correction or first-error recovery data improves GUI agents.
- **E16 (reproducibility, common_practice).** Report mean and spread over at least 3 runs (or confidence intervals) for online benchmark numbers — _applies when_ an empirical comparison on an online/live benchmark (OSWorld, AndroidWorld, WebArena, Online-Mind2Web) where LLM sampling and environment noise vary across runs.
- **E07 (baseline, common_practice).** Compare a native end-to-end GUI policy against UI-TARS(-1.5)-7B (or the same backbone's SFT-only model) and against an agentic framework (GPT-4o/o3 planner + specialised grounder such as UGround, Aria-UI, Jedi, GTA1) — _applies when_ a claim that a trained end-to-end GUI agent model improves online task success.
- **core-E06 (other, common_practice).** Do not rest an agent-capability claim on offline step matching alone: offline single-reference matching under-counts alternative valid paths, so pair it with online/executable success or show offline-online correlation — _applies when_ a claim of improved multi-step agent capability measured by offline trajectory matching (Mind2Web, AITW, AndroidControl).

## Cognitive barriers
- "More online RL phases monotonically help." Without KL or replay performance degrades over phases (2411.02337#s3).

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP7](../anti-patterns.md#ap7), [AP8](../anti-patterns.md#ap8), [AP9](../anti-patterns.md#ap9), [AP10](../anti-patterns.md#ap10), [AP12](../anti-patterns.md#ap12), [AP13](../anti-patterns.md#ap13)
