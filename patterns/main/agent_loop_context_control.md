# Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection
_id: `agent_loop_context_control` · sub-patterns: C15, C16, C17, C18, C20 · 5 candidate_pattern · 0 case · domains: cua-agents-core (0 K / 5 C) · outcome labels: none in this build_

**Definition.** Control what a prompted (M)LLM agent carries and checks from step to step: a fixed observe-think-act schema, interaction history compressed to recent full-fidelity steps plus model-written summaries, agent-nominated salient content retained for later steps, a manager that decomposes the task into subgoals for workers and replans, and post-action reflection that compares before/after observations and triggers retry, revert, replanning or escalation. The gain is claimed from loop and context design around a fixed backbone, not from training.

**Operational signature.** observe → (describe) → reason over plan / progress summary → act → reflect on before/after state → update summary and focus memory → manager replans or worker continues → self-declared stop

**When to apply.** When tasks are long, multi-step or multi-app, a strong prompted backbone is available, and errors surface as visible non-change or a recognisably wrong page and are reversible.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [C15](../sub/C15.md) | candidate_pattern | Compress interaction history: recent steps at full fidelity, older steps as model-written text | keep only the last few screenshots/steps verbatim and replace older history by text (a running progress summary from a separate LLM, an… |
| [C16](../sub/C16.md) | candidate_pattern | Let the agent nominate task-relevant content to retain for later steps | while acting, prompt the agent to list pivotal element ids or 'focus content' on the current screen; keep only those (plus tree neighbours)… |
| [C17](../sub/C17.md) | candidate_pattern | Decompose into a manager that plans subgoals and workers that execute them | have a manager (host agent, planner LLM, orchestrator) decompose the instruction into subgoals/subtasks (linear, DAG, or planning tree),… |
| [C18](../sub/C18.md) | candidate_pattern | Verify each action's outcome from before/after observations and feed the verdict back | after each action, have a reflector (same or separate model) compare pre/post screenshots or execution outputs, classify the step (as… |
| [C20](../sub/C20.md) | candidate_pattern | Prompt a fixed observe-think-act schema at every step | prompt the frontier model each step to describe the screen, reason about the goal/plan, then emit one action (plus optional history… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Each role removed with the same backbone.** The paper ablates the progress-summary/planning agent, memory unit, manager or reflector by removing it and reports the drop (SR 88.6 -> 59.1 without the planning agent; instruction SR 56% -> 12% without the manager hub or the reflection agent; subtask SR 76.0 -> 48.1) (2406.01014#s1, 2502.14282#s2, 2502.14282#s3).
- **Recent steps at full fidelity, older steps as text, with the window ablated.** A few recent screenshots are kept verbatim and older history becomes action text or summaries, with the number of screenshots / history level ablated (three recent screenshots plus L1 action text beats one; L2 text history adds nothing) (2508.09123#s4, 2406.01014#s1).
- **Proactive replanning or prunable plan trees.** The manager replans after every subgoal rather than only on failure (+4.62 / +6.15 points), or the agent maintains a plan tree it can branch and prune (WebArena SR 38.2% -> 43.1%) (2504.00906#s2, 2410.13825#s5).
- **Reflection on visible, reversible errors.** Post-action reflection compares before/after observations in settings where errors show as screen non-change or a recognisably wrong page and are reversible; guidelines plus a post-action success/failure summary lift M3A 19.8% -> 30.6% on AndroidWorld (2401.16158#s3, 2406.01014#s3, 2405.14573#s2).
- **Hierarchy benefit shown across backbones.** Separating planning from action decisions is reported across several backbones (Mobile-Agent-E 75.1 vs 53.0 satisfaction across three backbones) (2501.11733#s1).
- **Agent-nominated retained content with step savings.** The agent lists pivotal element ids or focus content to keep, and the paper reports both success and steps (WebArena SR 37.1% -> 38.2%, steps 12.0 -> 8.6; removing the focus memory: SR 88.6 -> 77.3) (2410.13825#s4, 2406.01014#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Reflector and self-check accuracy unmeasured.** Reflection accuracy is as low as 78.8%, executor self-checks and the supervising orchestrator hallucinate, and completion is self-declared without a checker (2406.01014#s3, 2508.03923#s3, 2411.10323#s2, 2312.13771#s3).
- **Summaries hide errors over long horizons.** Summaries returning only the final state hide intermediate mistakes from the orchestrator, long-horizon tasks (>30-50 actions) still lose coherent context, and summary error propagation is not measured (2508.03923#s2, 2508.09123#s4, 2406.01014#s1).
- **Decomposition degrades weaker backbones.** With a weaker backbone the full multi-agent framework falls below its single agent (Qwen2.5-VL) (2502.14282#s2).
- **No role-removal ablation and unreported per-step cost.** Several systems give no role-removal ablation, so gains cannot be assigned to the hierarchy alone, while each role adds per-step cost (2501.11733#s1, 2402.07939#s1, 2402.07456#s4).
- **Irreversible actions and state-blind replanning.** Plausible-looking wrong pages and irreversible actions (sending messages) defeat screenshot-diff reflection; plan pruning resets only the agent's context, not the web state (2406.01014#s3, 2401.16158#s3, 2410.13825#s5).
- **Loop pathologies on small, baseline-free suites.** Repeated actions to the step limit, early stopping triggered by an 'unachievable' hint, loops from caching actions but not outcomes, or retained content that hurts dense single-page tasks, evaluated on small benchmarks without baselines (2307.13854#s4, 2405.14573#s3, 2410.13825#s4, 2401.16158#s2).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From the `cua-agents-core` domain's `profile/expectations.json`; ids are prefixed `core-` to keep them apart from the `cua-agents` E ids._
- **core-E08 (ablation, common_practice).** Ablate each role of a multi-agent / hierarchical GUI framework (manager or planner, reflector, memory or notetaker, perception module) by removing it with the same backbone — _applies when_ a claim that a planner-executor-reflector or manager-worker decomposition improves GUI task success.
- **core-E09 (ablation, common_practice).** For self-reflection / post-action verification, report the reflector's own accuracy (false positives and negatives) and analyse wrong-but-plausible screen changes, not only end success with and without reflection — _applies when_ a claim that a reflection or verification step after each action improves recovery.
- **core-E21 (scale, common_practice).** Report inference cost and latency per step or per task (tokens, model calls, wall-clock) for multi-model or multi-call architectures — _applies when_ a claim for an architecture that adds model calls per step (multi-agent roles, verifiers, parsers, quarantined LLMs).
- **core-E07 (reproducibility, common_practice).** Report run-to-run variance on online benchmarks: multiple seeds or runs with intervals (AndroidWorld seeds, OSWorld average of 3 runs, Pass@k), not a single run or the best of several runs — _applies when_ a success-rate comparison on an online executable benchmark where differences between systems are a few points.
- **core-E15 (dataset, common_practice).** For mobile agents, evaluate on AndroidWorld (executable, seeded) rather than only on small self-built human-judged instruction sets — _applies when_ a claim that a mobile GUI agent or framework completes Android tasks better.

## Cognitive barriers
- "More reasoning text per step always helps." An observation-description step at inference can mislead (2508.09123#s3), and the agent can state the right target yet pick the wrong id (2409.08264#s3).

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP8](../anti-patterns.md#ap8), [AP9](../anti-patterns.md#ap9), [AP12](../anti-patterns.md#ap12), [AP15](../anti-patterns.md#ap15), [AP18](../anti-patterns.md#ap18), [AP21](../anti-patterns.md#ap21)
