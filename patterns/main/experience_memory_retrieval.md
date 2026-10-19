# Retrieve Past Experience and Knowledge into Context
_id: `experience_memory_retrieval` · sub-patterns: K27, K28, C19 · 2 candidate_pattern · 1 case · domains: cua-agents + cua-agents-core (2 K / 1 C) · outcome labels: none in this build_

**Definition.** Store summaries or raw trajectories of past episodes/subtasks (as text or compressed continuous embeddings) and retrieve them — optionally fused with web-search knowledge in a manager-worker hierarchy — into the agent's context at planning or action time. From `cua-agents-core`: libraries of distilled app knowledge, tips, shortcuts or code tools accumulated from the agent's own runs (C19).

**Operational signature.** run episodes (often self-supervised exploration) → summarise / embed and store keyed by task/state → retrieve nearest experience (+ web knowledge) → plan subtasks and act → replan on failure

**When to apply.** When test tasks recur in the same applications the memory was built from and a reliable self-evaluator can summarise what worked.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K27](../sub/K27.md) | candidate_pattern | Retrieve stored past experience into the agent's context | store summaries or raw trajectories of past episodes/subtasks keyed by task/state embeddings and retrieve the nearest ones into the context… |
| [K28](../sub/K28.md) | case | Manager-worker hierarchical planning fused with web knowledge | query web search and narrative memory, fuse into guidance, plan a subtask queue, execute with workers, replan on failure |
| [C19](../sub/C19.md) | candidate_pattern | Accumulate reusable app knowledge, tips, shortcuts or tools from the agent's own runs | explore apps or solve self-proposed tasks, have an LLM distil what worked into a persistent store (element-function documents, Tips,… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Experience from the same environments.** Memory is built from the same applications/environments (self-supervised exploration on benchmark initial states) (2410.08164#s2).
- **Summaries rather than raw trajectories, with ablation.** Stored experience is summarised by a self-evaluator, and removing the summaries is ablated (26.15 -> 18.46) (2410.08164#s2).
- **Memory-size scaling reported.** Scaling with memory size is reported: continuous (Q-Former) memory scales log-linearly where text memory degrades beyond ~10 items (2510.09038#s1).
- **Hierarchical planning with retrieved knowledge.** A manager fuses web search and narrative memory into a subtask queue executed by workers, with replanning on failure; requires a proprietary MLLM, web search and an accessibility tree (2410.08164#s1).
- **Distilled, reusable knowledge from own runs.** What worked is distilled into element-function documents, tips, precondition-guarded shortcuts or code tools and injected into later tasks, with the gain reported against no library (AppAgent SR 48.9% -> 73.3% with stable element ids; Mobile-Agent-E SS 75.1 -> 86.9; SheetCopilot tasks 0% -> 60%) (2312.13771#s2, 2501.11733#s3, 2402.07456#s3).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Small out-of-distribution gain.** OOD gains are small (OSWorld 26.40 -> 26.73) and retrieval drifts under UI shifts (2510.09038#s1).
- **Self-evaluator / reflector not validated.** Self-evaluator correctness is unmeasured; reflector labels disagree with humans ~25% (2410.08164#s2, 2311.08649#s2).
- **Held-out environment gains not isolated.** Gains on environments other than those the memory was built from are not isolated (2410.08164#s2).
- **Thin ablations and execution-dominated failures.** Ablations on 65 tasks with a single run; execution errors account for 79.59% of failures (2410.08164#s1).
- **Distilled knowledge leaks test queries or propagates errors.** Reflectors saw future queries or learning explores the same benchmark's dev set; shortcuts are misused on misperceived preconditions and flawed shortcuts propagate errors; the gain is small or absent with another backbone (Gemini-1.5-pro) (2501.11733#s3, 2402.07456#s3, 2312.13771#s2).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E35 (other, single_source).** For memory/retrieval agents, show gains on environments other than those the memory was built from — _applies when_ a claim that experience memory or retrieved trajectories improve GUI agents.
- **E28 (other, common_practice).** Separate synthesis/exploration environments from evaluation (held-out apps/sites, filtered test queries) and report out-of-distribution transfer — _applies when_ a claim that self-generated tasks, explored transitions, memory or synthesised environments improve benchmark success.
- **E10 (metric, common_practice).** Validate an LLM/VLM success judge or outcome reward model against human labels on trajectories from agents not used to build it (agreement/accuracy, plus the resulting success-rate gap) — _applies when_ a method that uses an LLM/VLM judge, ORM or reflector to label trajectory success for evaluation, filtering or reward.
- **E16 (reproducibility, common_practice).** Report mean and spread over at least 3 runs (or confidence intervals) for online benchmark numbers — _applies when_ an empirical comparison on an online/live benchmark (OSWorld, AndroidWorld, WebArena, Online-Mind2Web) where LLM sampling and environment noise vary across runs.
- **core-E08 (ablation, common_practice).** Ablate each role of a multi-agent / hierarchical GUI framework (manager or planner, reflector, memory or notetaker, perception module) by removing it with the same backbone — _applies when_ a claim that a planner-executor-reflector or manager-worker decomposition improves GUI task success.

## Cognitive barriers
- "Memory transfers wherever the agent goes." Reported OOD gains are near zero (2510.09038#s1).

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP5](../anti-patterns.md#ap5), [AP8](../anti-patterns.md#ap8)
