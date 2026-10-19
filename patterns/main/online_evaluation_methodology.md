# Make Online Evaluation Discriminating
_id: `online_evaluation_methodology` · sub-patterns: K24, K30, K31, C23, C24, C26 · 5 candidate_pattern · 1 case · domains: cua-agents + cua-agents-core (3 K / 3 C) · outcome labels: none in this build_

**Definition.** Design evaluation so it measures what end-to-end success hides: validated, de-shortcut task sets stratified by human reference length with fixed step budgets, controlled one-change-at-a-time perturbation probes with matched pairs, and closed-loop (autoregressive) evaluation of GUI world models instead of teacher-forced one-step fidelity. From `cua-agents-core`: offline step-level evaluation on recorded trajectories (C23), live evaluation with human success judgement (C24) and single-step click-in-box grounding benchmarks (C26) — evaluation designs whose discriminating power must be checked against online, executable success.

**Operational signature.** validate/clean tasks and attach reference lengths → fix step budget and resettable environment → run agents (or roll out world models closed-loop) → stratify, perturb with matched pairs, audit failure causes

**When to apply.** When headline success rates saturate, are confounded by shortcuts, drift or harness differences, or when a component (grounder, world model) must be shown to work in the loop.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K24](../sub/K24.md) | candidate_pattern | Probe agent/grounder robustness with controlled environment perturbations | re-render or reconfigure the environment under one controlled change at a time (style, zoom, text size, window position/clutter,… |
| [K30](../sub/K30.md) | candidate_pattern | Stratify online success by human reference length and audit failure causes | build or reuse tasks with human reference step counts, report success per length stratum and efficiency/budget-exhaustion, and audit… |
| [K31](../sub/K31.md) | case | Evaluate GUI world models in closed loop rather than teacher-forced one-step | roll the world model out autoregressively along reference action sequences and with a frozen probing agent, scoring consistency and… |
| [C23](../sub/C23.md) | candidate_pattern | Offline step-level evaluation on recorded trajectories | replay cached states of human demonstrations and score each predicted step against annotated (possibly multiple) valid actions, aggregating… |
| [C24](../sub/C24.md) | candidate_pattern | Evaluate agents live on real apps/sites with human success judgement | run the agent on real live apps, websites or desktops and have humans judge success, rubric satisfaction, step correctness or failure… |
| [C26](../sub/C26.md) | candidate_pattern | Single-step click-in-box grounding benchmarks | collect screenshots with instructions and target boxes split by platform and text vs icon, and score whether a predicted point falls inside… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Validated, de-shortcut task set.** Tasks are validated by humans and shortcuts removed (47% of sampled Mind2Web tasks invalid/outdated; a naive search agent scores 51% vs 22%) (2504.01382#s2).
- **Fixed step budget in deterministic resettable apps.** Agents are compared at a fixed step budget in deterministic, resettable apps (2609.07712#s3).
- **Success stratified by reference length with failure audit.** Success is reported per human reference-length stratum together with efficiency/budget exhaustion and a failure audit (2609.07712#s3, 2504.01382#s2).
- **Controlled matched-pair perturbations.** DOM/VM control is used to inject one controlled change at a time and recompute targets, reporting matched-pair accuracy changes (2604.14262#s1, 2404.07972#s2).
- **Closed-loop world-model evaluation with filtered references.** World models are rolled out autoregressively along reference action sequences and with a probing agent, using reference trajectories filtered for plausibility and state dependence (2609.00048#s3).
- **Offline and static proxies made multi-reference and checked against online.** Offline step evaluation scores each step against multiple valid actions and is shown to track online success and preserve rankings (power-law fit to OSWorld 15-step SR), and grounding-benchmark annotations are audited (~11% errors removed, rankings preserved) (2508.09123#s5, 2306.06070#s3, 2410.23218#s4).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Live-site drift and heterogeneous harnesses.** Live sites drift, and harnesses and step caps differ across compared agents (2504.01382#s2).
- **Aggregate success hides length collapse.** Success falls monotonically with length for every agent (GPT-5 43.6 -> 14.1%), so an unstratified number hides long-horizon failure (2609.07712#s3).
- **Perceptual similarity as world-model fidelity.** Fine-grained element scores are < 20 while SigLIP is 61-77 and best reference-action progress is 16.7, so global similarity overstates fidelity (2609.00048#s1).
- **Single probe agent or same-family judge.** A single probing agent, a judge from the same model family, and an unvalidated VLM filter are used (2609.00048#s2, 2609.00048#s3).
- **Narrow probe sets and training-time randomisation as the fix.** Perturbation sets are small, web-only and from one model lineage; relational instructions collapse accuracy (UI-TARS-1.5 91.0 -> 35.0) and domain-randomised LoRA SFT does not fix the brittleness (2604.14262#s1, 2604.14262#s2).
- **Small human-judged live sets or single-reference static proxies.** Live human-judged evaluation uses small task sets (20-90) without inter-annotator agreement, or claims rest on single-reference offline replay that counts alternative paths as failures (SeeAct 37.8 online vs 3.3 offline) or on single-step click-in-box benchmarks that measure no planning (2401.01614#s4, 2501.11733#s4, 2502.14282#s4, 2306.06070#s3, 2401.10935#s4).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E15 (metric, common_practice).** Do not rest an agent capability claim on offline step accuracy (AndroidControl, Multimodal-Mind2Web, GUI Odyssey) alone; add an online benchmark or show the offline metric predicts online success — _applies when_ a claim of improved agent capability measured with offline, teacher-forced step metrics.
- **E16 (reproducibility, common_practice).** Report mean and spread over at least 3 runs (or confidence intervals) for online benchmark numbers — _applies when_ an empirical comparison on an online/live benchmark (OSWorld, AndroidWorld, WebArena, Online-Mind2Web) where LLM sampling and environment noise vary across runs.
- **E17 (other, common_practice).** Compare agents at an equal, stated max-step budget (e.g. OSWorld 15 vs 50 steps), and report steps used / budget exhaustion — _applies when_ a comparison of agent success where methods or baselines may run with different step caps.
- **E19 (reproducibility, common_practice).** Disclose and validate any modification to an online benchmark harness (re-implemented checkers, changed action implementations, dropped tasks, extra steps) — _applies when_ a result on AndroidWorld, WebArena, Mind2Web-Live or OSWorld run in a re-engineered or modified harness.
- **E20 (reproducibility, common_practice).** For live-web results, state the evaluation date and handle site drift (replace outdated tasks, report blocked/CAPTCHA tasks) — _applies when_ a claim measured on live websites or live apps.
- **E21 (other, common_practice).** Report screenshot-only and accessibility-tree/DOM-augmented settings separately; a11y-tree availability changes results and reverses across models — _applies when_ a comparison of GUI agents whose observation spaces may differ.
- **E23 (metric, single_source).** Stratify online success by human reference step count (difficulty) and audit failure causes — _applies when_ a new benchmark or a claim about long-horizon GUI task capability.
- **E24 (other, common_practice).** Test grounding robustness under controlled perturbations (zoom, text size, window position/clutter, relational instructions) with matched pairs — _applies when_ a claim that a grounder or agent is robust or generalises across visual layouts.
- **E30 (metric, common_practice).** Evaluate a GUI world model by downstream agent success and closed-loop (multi-step, autoregressive) rollouts, not only teacher-forced one-step fidelity — _applies when_ a claim that a GUI/web world model (text, code or image next-state predictor) is accurate or useful.
- **core-E05 (metric, common_practice).** For offline web-agent claims on Mind2Web, report element accuracy, operation F1 and step success rate per Cross-Task / Cross-Website / Cross-Domain split, with MindAct and SeeAct as baselines — _applies when_ a next-action prediction claim evaluated on cached Mind2Web pages.
- **core-E06 (other, common_practice).** Do not rest an agent-capability claim on offline step matching alone: offline single-reference matching under-counts alternative valid paths, so pair it with online/executable success or show offline-online correlation — _applies when_ a claim of improved multi-step agent capability measured by offline trajectory matching (Mind2Web, AITW, AndroidControl).
- **core-E07 (reproducibility, common_practice).** Report run-to-run variance on online benchmarks: multiple seeds or runs with intervals (AndroidWorld seeds, OSWorld average of 3 runs, Pass@k), not a single run or the best of several runs — _applies when_ a success-rate comparison on an online executable benchmark where differences between systems are a few points.
- **core-E15 (dataset, common_practice).** For mobile agents, evaluate on AndroidWorld (executable, seeded) rather than only on small self-built human-judged instruction sets — _applies when_ a claim that a mobile GUI agent or framework completes Android tasks better.
- **core-E16 (reproducibility, common_practice).** Validate the success checker or LLM judge against human labels (agreement, kappa or F1) when a benchmark uses fuzzy matching or an LLM judge — _applies when_ a new benchmark or evaluation protocol whose success or safety labels come from fuzzy matching, VQA models or an LLM judge.

## Cognitive barriers
- "Domain randomisation fixes visual brittleness." It worked in robotics sim-to-real but did not improve GUI grounding under rank-8 LoRA SFT (2604.14262#s2).

## Related anti-patterns
[AP3](../anti-patterns.md#ap3), [AP7](../anti-patterns.md#ap7), [AP8](../anti-patterns.md#ap8), [AP11](../anti-patterns.md#ap11), [AP19](../anti-patterns.md#ap19)
