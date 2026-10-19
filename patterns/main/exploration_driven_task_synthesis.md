# Synthesise Tasks from Exploration and History
_id: `exploration_driven_task_synthesis` · sub-patterns: K14, K15, K32, K33 · 2 candidate_pattern · 2 case · domains: cua-agents (4 K / 0 C) · outcome labels: none in this build_

**Definition.** Generate training tasks and trajectories from what the agent (or an explorer) has actually seen: relabel goal-free exploration with retroactively inferred instructions, propose new tasks from stored history, failures or coverage, route intents between cheap traversal and an LLM agent, or force hard-to-reach app states via code analysis. The gain is claimed from grounded, feasible, coverage-expanding data.

**Operational signature.** explore the environment (random, DFS, instrumented) → store history/coverage → infer or propose intents/instructions → filter by feasibility, difficulty, judge → execute and train

**When to apply.** When human task annotation is the bottleneck, environment exploration is cheap, and a judge or feasibility signal can filter what is kept.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K14](../sub/K14.md) | candidate_pattern | Relabel exploration trajectories with retroactively inferred instructions | explore the environment without a fixed task, then infer an instruction that the observed transitions/trajectory accomplish… |
| [K15](../sub/K15.md) | candidate_pattern | Propose new tasks conditioned on the agent's history, failures or coverage | generate the next tasks/intents from stored history — failed instructions, coverage of activities/functionalities, clusters of the UI… |
| [K32](../sub/K32.md) | case | Route exploration intents between cheap traversal and an LLM GUI agent, asynchronously | generate intents asynchronously from memory while a DFS explorer runs; route single-step intents to value-guided traversal and multi-step… |
| [K33](../sub/K33.md) | case | Reach otherwise unreachable app states via static analysis and runtime instrumentation | infer activation conditions of unreached activities from decompiled code, generate and refine Frida hooks that fake external results, and… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Interaction-first beats instruction-first at equal budget.** The paper compares exploration-first (hindsight) synthesis against instruction-first synthesis at equal budget (MiniWoB 0.48 vs 0.28; WebArena 7.2 vs 4.2) (2410.02907#s3).
- **Instructions reference explored, site-specific entities.** Synthesised instructions reference deep, site-specific entities discovered by exploration, relabelled by a strong LLM/VLM (2410.02907#s3, 2412.19723#s1, 2410.02907#s1).
- **Feasibility/difficulty filter on proposed tasks.** Proposed tasks are filtered by a feasibility or difficulty signal (activity lists, critic value band [0.05, 0.75], feasibility rules) (2311.08649#s1, 2411.02337#s1).
- **History presented per cluster, intents from memory.** Proposals are conditioned on history presented per cluster of the UI transition graph rather than the whole graph or recent states only (coverage 36.94 vs 26.09/31.51), with intents generated from stored history rather than the live screen (2609.10031#s1, 2609.10031#s2).
- **Failure-conditioned curriculum shown to transfer.** A self-evolving curriculum built from failed tasks improves online RL and transfers to another RL algorithm (DigiRL) (2411.02337#s1).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Synthesis environments overlap evaluation.** Synthesis environments overlap the evaluation environments (2412.19723#s1).
- **Poor cross-site transfer.** Synthesised data transfers poorly across sites; mixing live and WebArena data hurts 7 sites (2410.02907#s2).
- **Kept-trajectory judge precision unmeasured.** Judge precision for kept trajectories is not measured, and self-reinforcing loops may overfit easy/popular sites (2510.09038#s2).
- **Saturation bounded by the executor.** Gains saturate with scale, bounded by executor capability (2412.19723#s1).
- **Exploration blind spots.** Widgets without text and single views with sub-regions are poorly explored; live-site exploration cannot log in or submit content; mocked values from instrumentation may not initialise realistic state (2311.08649#s1, 2410.02907#s1, 2601.21253#s2, 2601.21253#s3).
- **Hand-written feasibility rules and noisy generation.** Task-generation randomness raises variance, feasibility rules are hand-written per environment, and residual duplicate or non-existent-functionality intents remain (2411.02337#s1, 2609.10031#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E26 (baseline, single_source).** Compare a synthetic-trajectory recipe against an instruction-first / task-driven synthesis baseline with the same executor and similar data size — _applies when_ a claim that an exploration-first, reverse or world-model data-synthesis method yields better GUI training data.
- **E27 (scale, common_practice).** Show a data-scaling curve (fraction or count of synthetic samples vs downstream score) and say where it saturates — _applies when_ a claim that synthetic GUI grounding, transition or trajectory data improves agents.
- **E28 (other, common_practice).** Separate synthesis/exploration environments from evaluation (held-out apps/sites, filtered test queries) and report out-of-distribution transfer — _applies when_ a claim that self-generated tasks, explored transitions, memory or synthesised environments improve benchmark success.
- **E10 (metric, common_practice).** Validate an LLM/VLM success judge or outcome reward model against human labels on trajectories from agents not used to build it (agreement/accuracy, plus the resulting success-rate gap) — _applies when_ a method that uses an LLM/VLM judge, ORM or reflector to label trajectory success for evaluation, filtering or reward.
- **E16 (reproducibility, common_practice).** Report mean and spread over at least 3 runs (or confidence intervals) for online benchmark numbers — _applies when_ an empirical comparison on an online/live benchmark (OSWorld, AndroidWorld, WebArena, Online-Mind2Web) where LLM sampling and environment noise vary across runs.

## Cognitive barriers
- "Self-generated data improves the agent in general." Gains are often measured on the environments used for synthesis (2412.19723#s1) and transfer poorly across sites (2410.02907#s2).

## Related anti-patterns
[AP2](../anti-patterns.md#ap2), [AP5](../anti-patterns.md#ap5), [AP8](../anti-patterns.md#ap8), [AP10](../anti-patterns.md#ap10)
