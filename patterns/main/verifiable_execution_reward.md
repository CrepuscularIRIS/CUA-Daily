# Ground Reward in Executable Checkers
_id: `verifiable_execution_reward` · sub-patterns: K12, K13, K34, C22 · 3 candidate_pattern · 1 case · domains: cua-agents + cua-agents-core (3 K / 1 C) · outcome labels: none in this build_

**Definition.** Derive reward from programs that inspect environment state the agent cannot see — files, configs, backend fields, instrumentation flags — and, going further, synthesise tasks starting from such checkers so that every task ships with a programmatic reward. Checkers are themselves validated two-sidedly. From `cua-agents-core`: executable benchmarks with resettable, seeded environments and privileged final-state checkers (C22).

**Operational signature.** define goal conditions over privileged state (or start from an evaluator library/spec) → generate task (and environment code) satisfying it → run agent → score with checker (binary or partial credit) → validate checker against faulty and legal alternatives

**When to apply.** When environment internals are accessible (open-source apps, generated code, instrumented simulators) and RL or evaluation needs reward that does not depend on a judge model.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K12](../sub/K12.md) | candidate_pattern | Score episodes with execution-based checkers that read privileged environment state | after the episode, read environment internals the agent cannot see (files, configs, backend/localStorage fields, instrumentation flags,… |
| [K13](../sub/K13.md) | candidate_pattern | Synthesise tasks from checkers/specs so verifiable reward exists by construction | start from a verification condition (composed evaluator functions, or tests derived from a shared spec) and generate the task (and, for… |
| [K34](../sub/K34.md) | case | Validate checkers two-sidedly: reject faulty, accept legal alternatives | assess a generated test/oracle on independent pools of faulty and legal implementations, and separate setup repair from… |
| [C22](../sub/C22.md) | candidate_pattern | Executable benchmark with resettable environments and privileged final-state checkers | package apps/sites/OS images as resettable containers or emulators with seeded task initialisation, and score each task by programmatic… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Checker reads privileged state.** Reward comes from reading environment internals (files, configs, backend/localStorage fields, instrumentation flags, logs) compared to goal conditions or gold artefacts; benchmarks package apps as resettable containers/emulators with seeded, parameterised task initialisation and report variance across seeds (SR 27.6-33.2%) (2404.07972#s1, 2601.04126#s2, 2609.07712#s2, 2307.13854#s1, 2405.14573#s1, 2405.14573#s4).
- **Outcome-only checks accept alternative paths.** Checkers test the final state rather than the action sequence, so alternative correct paths are accepted, e.g. state-locator checkers (2404.07972#s1, 2609.07712#s2, 2307.13854#s3).
- **Tasks synthesised checker-first with test-driven repair.** Tasks (and generated sites) are produced from an evaluator library or shared spec, with a repair loop until task-relevant tests pass (removing it: 85.6 -> 82.6) (2510.17790#s2, 2601.04126#s1).
- **Dense partial credit from instrumented checkpoints.** Instrumented checkpoints give partial credit and more discriminative RL groups (767 vs 174 discriminative GRPO groups, 4.4x) (2601.04126#s2).
- **Difficulty-band filtering before RL.** Synthesised tasks are filtered to a difficulty band before RL training (2510.17790#s2).
- **Two-sided checker validation.** Checkers/oracles are assessed on independent pools of faulty and legal implementations, measuring false rejects of legal alternatives as well as detection of failures (2610.05001#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Checker error rates unquantified.** Residual false positives/negatives are not quantified, and checkpoint weights are LLM-chosen and unvalidated (2404.07972#s1, 2601.04126#s2); two-sided validation remains a survey recommendation, not measured; must_include and GPT-4 fuzzy match can accept partially wrong content (2610.05001#s2, 2610.05001#s3, 2307.13854#s3, 2401.13649#s3).
- **Manual per-task checkers limit scale.** Checkers are per-task manual work (~2 man-hours each) and do not exist for unannotated tasks (2404.07972#s1).
- **Synthetic environments without real server logic.** Generated sites have no real server logic and are single-site, single-user in scope; benchmark apps are restricted to ones without login and with inspectable local storage, or clones with sampled data (2601.04126#s1, 2405.14573#s1, 2307.13854#s1).
- **Synthesis/test overlap not analysed.** Overlap between synthesised tasks and the test distribution is not analysed (2510.17790#s2).
- **Small downstream RL gain.** Evaluator-first tasks are harder and fewer, and the RL gain is ~2 points (2510.17790#s2).
- **Screenshot-blind state.** Screenshots alone cannot see some state (e.g. file size), so screenshot judges and scripts are complementary; a design relying on one alone misses cases (2404.07972#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E13 (metric, common_practice).** Measure execution checkers (evaluation scripts) two-sidedly: false negatives on alternative valid solutions as well as false positives — _applies when_ a benchmark, synthetic environment or RL pipeline whose reward comes from per-task execution checkers or evaluator scripts.
- **E19 (reproducibility, common_practice).** Disclose and validate any modification to an online benchmark harness (re-implemented checkers, changed action implementations, dropped tasks, extra steps) — _applies when_ a result on AndroidWorld, WebArena, Mind2Web-Live or OSWorld run in a re-engineered or modified harness.
- **E28 (other, common_practice).** Separate synthesis/exploration environments from evaluation (held-out apps/sites, filtered test queries) and report out-of-distribution transfer — _applies when_ a claim that self-generated tasks, explored transitions, memory or synthesised environments improve benchmark success.
- **E01 (dataset, common_practice).** Report execution-checked success rate on OSWorld (or OSWorld-Verified) for desktop computer-use claims, stating the step budget (15 vs 50 steps) and observation setting — _applies when_ an empirical claim that a method improves end-to-end task success of a desktop (Ubuntu/Windows) computer-use agent.
- **E03 (dataset, common_practice).** Report success on WebArena (self-hosted, functional-correctness checkers) for web-agent training or planning claims; if the 165-task WebArena-Lite or a per-template subset is used, say so and justify it — _applies when_ an empirical claim that a training, data-synthesis or planning method improves a web agent on self-hosted sites.
- **E12 (ablation, common_practice).** When a learned judge or PRM is the RL reward, show downstream policy gain against an alternative reward (rule/script checker, ORM vs PRM, another judge), and address reward hacking or bias — _applies when_ a claim that a learned reward model or verifier improves GUI-agent RL training.
- **core-E03 (dataset, common_practice).** Evaluate end-to-end computer-use claims on executable benchmarks with state checkers: OSWorld (or OSWorld-Verified) for Linux desktop and WindowsAgentArena for Windows — _applies when_ a claim that a full agent (framework or native policy) completes desktop tasks better.
- **core-E07 (reproducibility, common_practice).** Report run-to-run variance on online benchmarks: multiple seeds or runs with intervals (AndroidWorld seeds, OSWorld average of 3 runs, Pass@k), not a single run or the best of several runs — _applies when_ a success-rate comparison on an online executable benchmark where differences between systems are a few points.
- **core-E16 (reproducibility, common_practice).** Validate the success checker or LLM judge against human labels (agreement, kappa or F1) when a benchmark uses fuzzy matching or an LLM judge — _applies when_ a new benchmark or evaluation protocol whose success or safety labels come from fuzzy matching, VQA models or an LLM judge.

## Cognitive barriers
- "An execution checker is ground truth." False negatives on legal alternatives and unquantified false positives remain (2404.07972#s1, 2610.05001#s2).

## Related anti-patterns
[AP2](../anti-patterns.md#ap2), [AP4](../anti-patterns.md#ap4), [AP5](../anti-patterns.md#ap5), [AP8](../anti-patterns.md#ap8), [AP9](../anti-patterns.md#ap9)
