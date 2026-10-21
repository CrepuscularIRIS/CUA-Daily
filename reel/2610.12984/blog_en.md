# Work2Skill: turning recorded human desktop work into reusable agent skills

*A CUA Radar reading of arXiv 2610.12984v1 (Huang, Li, Cao, Cai, Xie, Gao, Guo, Zhang, Li, Zheng, Yan, Liao). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.12984v1 · Code: https://github.com/china-qijizhifeng/Work2Skill*

## The problem: procedural knowledge the request never spells out

“Submit my reimbursement” does not say which internal portal to use, which receipts to attach, or what to check before submitting. Computer-use agents fail on exactly this kind of unfamiliar software and organization-specific workflow. Human demonstrations are a natural source of this knowledge, because humans and agents share the same GUI interaction space. The paper identifies three obstacles to reusing them: action coordinates show where a click happened but not what the control means; prior demonstration studies differ in source demos, task sets and execution protocols, so their numbers cannot be compared; and fixed parsing pipelines prescribe an inspection order, while loading a long recording at once creates context pressure and pre-selecting frames omits details needed later.

## What Work2Skill is

Three components, one per obstacle.

**WorkRecorder** is the collection infrastructure. A macOS interface records the screen region (H.264 video) plus mouse and keyboard activity; for remote Linux desktops, an AT-SPI collector inside the target session supplies accessibility-tree (AX) snapshots, point queries and target-element metadata (names, roles, bounds) when the application supports them. Input events are grouped into semantic actions — clicks, drags, scrolling, hotkeys — and aligned with keyframes on one video-relative timeline, so each action links to its screen image, available target information, and surrounding video. The paper is explicit that alignment uses heuristic temporal tolerances, “not measured accuracy bounds.”

**WorkDemo-350** is the dataset: 350 human demonstrations covering all 64 MyPCBench Bounded Action tasks and a fixed 286-task OSWorld-Verified subset, screened for completeness and task success — about 8.48 hours of recorded experience, with mean episode durations of 119.11 s (MyPCBench) and 80.04 s (OSWorld) and roughly 32.23 and 34.57 actions per episode.

**Agentic skill induction** is the method. A NexAU tool-using agent receives one evidence episode (task.json, action traces, keylogs, indexed images, video) and a skill-creator authoring policy. Its system prompt is deliberately concise; the agent decides what to inspect, using file tools (`read_file`, `glob`), `read_visual_evidence` for indexed images, and `watch_video` / `extract_video_frames` for intervals or exact timestamps. Evidence inspection and skill writing share one conversation, so a draft can expose a missing constraint and send the agent back to the source. The output is SKILL.md files (Agent Skills convention) with semantic UI targets, workflow rules, step dependencies and visible completion checks — executable “without the source recording.” There is no training and no reward: candidate skills are not executed during induction, and “downstream evaluation results are not used as revision feedback.” The `finalize_extraction` check validates structure and tool use only; the paper says these checks “do not verify skill correctness or task success.”

At execution time the skill is pure text, appended to the executor’s system prompt inside a shared `<task skills>` wrapper; the executor (a screenshot-and-action loop over the VM, via PyAutoGUI; GUI actions plus Bash on MyPCBench) never sees the recording. On the CUA Radar board the architecture pattern is R03 under “mine human screen recordings into action knowledge”: human screen video plus input streams, distilled into operational knowledge for an acting agent.

## Results, as reported

Everything below is online, execution-based evaluation with the official benchmark evaluators; the paper reports no offline step-accuracy metric. Executors: GPT-5.5, Opus-4.8, Qwen3.5-35B-A3B, Qwen3.5-9B; by default each model executes with its own induced skills. Settings are shared per model and benchmark: temperature 0, high reasoning effort, a 100-step execution limit, a 100-iteration induction limit. Seeds or repeat runs are not reported. Score is the mean evaluator output scaled to 0–100; SR is the share of tasks with full credit.

MyPCBench Bounded Action (64 tasks), Score / SR (%):

| Method | GPT-5.5 | Opus-4.8 | Qwen3.5-35B-A3B | Qwen3.5-9B |
|----|----|----|----|----|
| No Skill | 74.73 / 23.44 | 81.53 / 42.19 | 38.38 / 9.38 | 24.27 / 6.25 |
| Aloha | 77.48 / 37.50 | 79.27 / 34.38 | 37.69 / 12.50 | 26.61 / 3.13 |
| D2T | 75.25 / 37.50 | 81.28 / 42.19 | 40.61 / 9.38 | 27.75 / 6.25 |
| **Work2Skill** | **85.27 / 48.44** | **86.20 / 50.00** | **44.56 / 20.31** | **34.11 / 12.50** |

OSWorld-Verified subset (286 tasks), Score / SR (%):

| Method | GPT-5.5 | Opus-4.8 | Qwen3.5-35B-A3B | Qwen3.5-9B |
|----|----|----|----|----|
| No Skill | 74.47 / 70.98 | 79.23 / 77.97 | 32.52 / 32.17 | 27.48 / 26.92 |
| Aloha | 72.57 / 69.93 | 78.91 / 76.57 | 31.08 / 30.42 | 24.81 / 24.13 |
| D2T | 80.32 / 76.22 | 80.66 / 78.67 | 33.93 / 32.52 | 26.45 / 25.52 |
| **Work2Skill** | **81.97 / 78.67** | **82.34 / 79.37** | **36.36 / 36.01** | **33.41 / 32.52** |

Work2Skill posts the highest Score and SR in every model × benchmark cell. Versus No Skill, mean score improves by 4.67–10.54 points on MyPCBench (SR +6.25 to +25.00 points) and by 3.11–7.50 points on the OSWorld subset (SR +1.40 to +7.69). Costs are model-dependent: fewer execution steps than No Skill for Opus-4.8 and both Qwen models but more for GPT-5.5, and induction token usage (for GPT-5.5, 334.52 k on MyPCBench and 185.19 k on OSWorld) is “not consistently lower” than the baselines’.

## What the paper’s own controls say

**Reuse on changed instances (MyPCBench Jitter).** Each of the 64 tasks gets a paired variant that changes entities, parameters or constraints within the same application; the original skills are reused without re-induction. Work2Skill improves Score by 3.93–8.64 and SR by 6.25–9.38 points over No Skill on all four executors (GPT-5.5: 81.75 vs 73.45; Opus-4.8: 87.23 vs 83.30; Qwen3.5-35B-A3B: 51.58 vs 42.94; Qwen3.5-9B: 36.25 vs 27.80), with 2.49–5.44 fewer steps and a 4.28–6.25-point edge over the stronger demo baseline per executor.

**Cross-model transfer.** Freezing each induced skill and swapping executors (GPT-5.5 × Qwen3.5-9B), all four induction/execution pairings beat the same executor’s No Skill baseline; GPT-5.5-induced skills beat Qwen3.5-9B-induced ones under both executors, with the advantage “reaching 9.46 score points and 9.38 percentage points” under GPT-5.5 execution — though Qwen3.5-9B execution stays far weaker regardless of inducer.

**Evidence ablation (64 tasks, GPT-5.5).** Removing indexed images, UI annotations, or KeyLogs from induction reduces Score by 5.02–10.63 points and SR by 14.06–21.88 points; the largest Score drop comes from removing indexed images, the largest SR drop from removing KeyLogs. A text-only condition (ordered action captions with target UI semantics) still beats video-only and uses the fewest steps, but both trail full evidence.

**Prompt design.** Against a Pipeline Prompt that prescribes the induction stages, the concise on-demand prompt gains 3.97 Score and 6.25 SR points and cuts steps from 48.98 to 47.38, at 12.7% higher induction token usage.

**Matched comparison.** Aloha and D2T are text-adapted into the same wrapper, from the same source episodes, under the same executor, step limit and evaluators — so the comparison isolates the guidance text, not the harness.

## Where the evidence is thinner, in the paper’s words

- The demonstrations are collected on the benchmark tasks themselves, and RQ1 evaluates on those demonstrated tasks; generalization is probed only via Jitter variants “within the same application context” and a two-model transfer grid.
- The OSWorld set is curated: “we first exclude infeasible tasks for which a valid human demonstration cannot be completed,” and “OSWorld results apply to this curated subset.”
- No seeds or repeat runs are reported, so run-to-run variance is unknown.
- AX coverage “depends on the recording configuration and the application’s accessibility support,” and time alignment windows are “implementation tolerances, not measured accuracy bounds.”
- Jitter variants were drafted with GPT-5.6-sol assistance, then human-verified.
- A case study (a TableFind reservation with fallbacks) is a single worked example: both baselines score 55/100, Work2Skill 100/100 on the eight-item rubric.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **online**. The score reflects what is reported: online evaluation with official evaluators on two benchmarks, same-demos/same-settings comparisons against adapted strong baselines (ShowUI-Aloha, Demo2Tutorial), induction-token cost reporting, an evidence-modality ablation and a prompt comparison, and released code and data. The judgment record marks held-out environments as partial (Jitter variants stay inside the same applications) and lists as not reported: variance (no seeds) and budget matching; it also flags anti-pattern AP5 — synthesis/experience data overlapping the evaluation set — since the demos come from the eval tasks. CUA Radar did not rerun anything; every number above comes from the paper (version v1).
