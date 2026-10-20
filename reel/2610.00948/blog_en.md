# GUI-HARVEST: letting an optimizer rewrite the harness around a frozen GUI model

*A CUA Radar reading of arXiv 2610.00948v1 (Yang, Qu, Li, Wang, Zhang, Zeng, Dai). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.00948v1 · Code: https://github.com/GaryYang12345/GUI-HARVEST*

## The problem: the harness is code, and it is not tuned per model

A desktop GUI agent is more than a model. Around it sits an executable harness: how observations and context are built, how actions are dispatched, and how verification, recovery and termination are controlled. Automatic harness optimizers such as Meta-Harness and Self-Harness already revise prompts and code from traces, but they were built for non-GUI domains and read mostly text, source and scores.

The authors name three problems these optimizers do not address. A text trace can claim success while the screen shows an unresolved state, for example a dialog still open after Save. The same agent can succeed or fail on the same task even with deterministic decoding: in the baseline runs, 11.8 to 20.4% of tasks produce both a zero and a positive score across three executions, depending on the backbone. And a patch motivated by one task need not help elsewhere.

## What GUI-HARVEST is

The agent being improved is a frozen model plus a harness, acting on a desktop from screenshots and text. For Qwen3-VL and the proprietary backbones the starting harness is Agent S3: the worker emits one `agent.*` primitive per step, a grounding model (UI-TARS-1.5-7B) maps the described target to coordinates, and the result is compiled into PyAutoGUI code. The OpenCUA models start from their official runtime, which emits coordinate-bearing PyAutoGUI actions directly. On the CUA Radar board this is pattern C19, accumulating reusable knowledge from the agent’s own runs, here as executable code.

The optimizer never touches weights, tasks, evaluators or resource limits; it edits only files named in a capability manifest. Tasks are split into Search (80), Validation (80) and a sealed Test (201). Each round has five steps:

1.  **Repeated rollouts.** Every Search and Validation task is run K = 3 times from clean snapshots. Search runs give detailed evidence; Validation gives only aggregate scores.
2.  **Evidence Analyst.** For tasks with at least one zero-score run, an analyst compares the runs and writes findings that cite a decisive step, using a successful run as contrast when one exists. A toolkit (GAFT) aligns text, actions and before/after screenshots. A deterministic verifier checks that cited runs and steps exist; the paper notes that the behavioral interpretation remains the analyst’s assessment.
3.  **Cross-task Clusterer.** Findings are grouped into open-vocabulary behavior modes, each needing support from at least two independent tasks.
4.  **Harness Engineer.** It makes one bounded source edit, runs local tests, and records predictions of observable behavior before any GUI evaluation.
5.  **Validator.** After code checks, a utility gate requires no drop on Search or Validation and a gain on at least one. A behavior gate asks a separate validator whether post-edit runs support the frozen prediction. Both must pass for promotion; otherwise the harness is rolled back.

Up to P = 5 candidate edits are tried per round, with at most B = 10 rounds; optimization stops when all five attempts at one state are rejected. All four roles use Claude Sonnet 5, and search uses a 15-step budget. The signal is therefore OSWorld evaluator scores plus behavioral verdicts; no weights are updated.

The appendix traces one example. In a Chrome task, two of three runs type the new profile name, call done() while the field is still in edit mode, and fail. The mode EDIT_NOT_COMMITTED_AT_DONE, shared with Impress and Calc tasks, leads to a gate that withholds the first premature done(); the validator marks the prediction supported in all three post-edit runs.

## Results, as reported

All numbers are online scores on OSWorld-Verified (361 tasks after excluding eight Google Drive tasks): mean raw evaluator score over K = 3 runs, 15-step budget, frozen harness H\*. The paper reports no offline benchmark.

| Backbone | Test, initial | Test, GUI-HARVEST | Full, initial | Full, GUI-HARVEST |
|----|----|----|----|----|
| Qwen3-VL-8B | 28.79 | 34.84 | 29.49 | 36.83 |
| Qwen3-VL-32B | 43.02 | 53.18 | 38.61 | 50.94 |
| OpenCUA-32B | 32.82 | 34.31 | 30.71 | 34.24 |
| OpenCUA-72B | 41.25 | 44.18 | 37.65 | 42.33 |
| Gemini 3.1 Pro | 66.42 | 72.63 | 66.46 | 73.37 |
| GPT-5 | 56.35 | 61.86 | 55.20 | 62.42 |

Test gains run from +1.49 to +10.16 points; Qwen3-VL-32B gains +12.33 on Full. Harnesses frozen after 15-step optimization were also run at 50 and 100 steps, where Gemini 3.1 Pro reaches 79.14%. The paper reports the highest score in every comparison it shows against published systems, whose rows keep their own runtimes and budgets.

**Transfer to WindowsAgentArena** (50 steps, no WAA optimization, platform adapters only):

| Backbone     | Agent S3 | GUI-HARVEST |
|--------------|----------|-------------|
| Qwen3-VL-32B | 38.21    | 44.68       |
| GPT-5        | 50.88    | 64.75       |

## What the paper’s own controls say

**Same-model optimizers (Table 2).** From the same Qwen3-VL-32B and Agent S3 harness, optimizer model and ten-round cap, Test scores are 53.18 (GUI-HARVEST), 45.02 (Self-Harness) and 47.40 (Meta-Harness); on Full, 50.94, 42.08 and 45.10. Both baselines are the authors’ GUI adaptations. For LFF, whose optimizer is not public, the authors applied its released OpenCUA patches: on OpenCUA-72B, 44.18 and 42.33 versus 41.29 and 39.50.

**Ablations (Qwen3-VL-32B, Test / Full).** Without visual evidence 44.54 / 40.69; without the clusterer 45.66 / 42.13; single-run evidence (K = 1) 47.44 / 43.12; hard gate only 49.36 / 48.08; full method 53.18 / 50.94. The hard-gate-only variant ran nine rounds yet chose a lower-scoring harness. K = 3 gives 50.9% against 43.1% at K = 1, and K = 5 costs more rollouts for 49.7%.

**Cost.** Costs cover target-model calls only, not optimization. GPT-5 goes from 55.2% at \$78.6 to 62.4% at \$72.3; Gemini 3.1 Pro from 66.5% at \$140.0 to 73.4% at \$92.4. The paper’s comparison with Agent S3 on GPT-5 (62.4% versus 62.6%, \$72 versus \$260) is explicitly not shared-budget: 15 steps against 100.

## Where the evidence is thinner, in the paper’s words

- Gains depend on the backbone: 3.53 to 4.68 Full points for OpenCUA against 6.91 to 12.33 for the others, which the authors call “consistent with” lower adaptability to added tools.
- Raising the budget from 15 to 100 steps adds only 2.54 and 0.85 points for Qwen3-VL-8B and 32B.
- Remaining failures are “actions that execute successfully but target the wrong object, route, or evaluator-relevant state”, which a harness struggles to detect.
- Search, Validation and Test are random splits of one benchmark; the Test tasks are unseen but share domains with Search, and Full includes the optimization tasks. WAA transfer covers two backbones.
- The paper reports a standard error of 0.93 points for the K = 3 Full mean, but no repeated optimization runs, and no check of the behavior validator against human labels.

## CUA Radar’s read

CUA Radar scores this paper **76 (★★★)**, evidence level **transfer**. The judgment record credits online evaluation, a held-out Test split, same-backbone optimizer baselines, matched backbones and budgets in the main comparison, cost reporting, a component ablation and released code. It marks variance as unclear and the behavior-validator check as untested, and flags anti-pattern AP5 (optimization and evaluation drawn from overlapping sources) because Search and Test share one benchmark. The radar did not rerun any experiment; every number here comes from the paper (version v1).
