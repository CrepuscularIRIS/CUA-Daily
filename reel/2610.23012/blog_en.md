# MAGE: reading the user manual to plan, and training on tasks made from it

*A CUA Radar reading of arXiv 2610.23012v1 (Yoon, Park, Yun, Jeong, Yun, Jung). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.23012v1 · Code: https://github.com/ku-autoai/MAGE*

## The problem: a new application, no demonstrations

The paper’s starting point is that adapting a CUA to such an application usually means paying people to define executable tasks and record trajectories. Reinforcement learning can reduce that need, but GUI tasks are long-horizon: functions sit behind menus, dialogs and shortcuts, so a weak policy rarely produces the successful trajectories that RL needs. The authors observe that user manuals already describe those functions and the procedures to reach them, and ask whether manuals can serve as procedural supervision both at inference and at training time.

## What MAGE is

MAGE (Manual-augmented computer use AGent Execution and learning) wraps an existing CUA. The agent perceives a screenshot at each step and acts with mouse and keyboard primitives (click, right click, double click, drag, scroll, type, hotkey; the action space follows the backbone). It runs on desktop software: LibreOffice Calc, Impress and Writer, GIMP, VSCode and Slack. On the CUA Radar board its pattern is K28 under “retrieve past experience and knowledge into context”.

**At run time (retrieval-augmented planning, RAP).** Manual sections are embedded with Qwen3-Embedding-0.6B and stored in a vector database. For a task, the top-5 sections by cosine similarity are retrieved. A multimodal planner (Qwen3.6, 27B) reads the instruction, the retrieved sections and the first screenshot, and writes one step-by-step plan with concrete button names and shortcuts. The plan stays fixed for the whole episode; the CUA conditions each action on the instruction, the plan, the current screenshot and its recent history.

**At training time (policy optimization, PO).** There are three stages. First, a multimodal LLM (GPT-5.4) reads each manual section, text and images, and generates up to two task pairs: an optional setup task (to create the data or objects the main task needs) and a main task, each with a plan. Second, the current policy executes these tasks in the real GUI with the plan as guidance, several times per task, up to 50 steps; the setup task must succeed before the main task starts. Third, a VLM judge (GPT-5.4) reads the instruction and the last five screenshots and returns a binary success reward; on success a step-efficiency bonus is added with weight 0.1. The policy is updated with GRPO (LoRA), using one sampled episode per task and an advantage computed over the task’s group; groups with zero reward variance are dropped. Training is round-based (two rounds for UI-TARS-1.5, one for EvoCUA).

The supervision signal is therefore a learned judge’s binary verdict on self-generated trajectories, with manual-derived plans used to steer rollouts toward task-completing states. No human demonstrations or step-level labels are used.

## Results, as reported

All results are online task success (%), 50-step budget. Base CUAs are UI-TARS-1.5 (7B) and EvoCUA (8B); main rows are the mean of five runs (for the backbones, the five runs include results from the official OSWorld dashboard). No offline step-accuracy benchmark appears in the paper.

OSWorld, Table 1 (mean ± std; overall is micro-averaged over tasks):

| Model | Calc | Impress | Writer | GIMP | VSCode | Overall |
|----|----|----|----|----|----|----|
| UI-TARS-1.5 (7B) | 14.47 ± 6.45 | 38.15 ± 3.38 | 40.87 ± 2.38 | 53.85 ± 3.85 | 56.52 ± 5.32 | 36.83 ± 3.09 |
| **MAGE (UI-TARS-1.5)** | 34.04 ± 3.69 | 45.39 ± 1.90 | 44.35 ± 1.94 | 60.77 ± 5.70 | 66.09 ± 3.64 | **47.31 ± 2.02** |
| EvoCUA (8B) | 32.77 ± 2.43 | 35.98 ± 3.38 | 46.09 ± 5.83 | 80.00 ± 3.22 | 66.09 ± 1.94 | 47.54 ± 0.96 |
| **MAGE (EvoCUA)** | 37.02 ± 1.90 | 45.32 ± 3.56 | 50.43 ± 4.96 | 81.54 ± 1.72 | 76.52 ± 2.38 | **53.67 ± 1.73** |

The paper reports significance under a two-sided Welch’s t-test (p = 4.13 × 10^-4 for UI-TARS-1.5 and p = 3.63 × 10^-4 for EvoCUA). Larger systems in the table score higher overall (EvoCUA 32B 66.24, Claude-Sonnet-4.5 62.66, one run each); the paper bolds best results only among base CUAs of 8B or fewer.

Slack, Table 2: 30 tasks in 15 themes, built independently of the manuals and scored by Gemini 3.1 Pro Preview from the last five screenshots. UI-TARS-1.5 26.67 ± 5.27, MAGE (UI-TARS-1.5) 49.33 ± 11.88, EvoCUA 32.67 ± 4.94, MAGE (EvoCUA) 51.33 ± 8.03. The paper states gains of 22.66 and 18.66 points (Welch p = 0.0094 and 0.0035). On the 18 tasks without a setup step, UI-TARS-1.5 gets 27.78 ± 6.80 and MAGE 56.67 ± 6.09.

## What the paper’s own controls say

**Component ablation (Calc, UI-TARS-1.5, Table 3).** The baseline gets 14.47. Policy optimization alone gives 14.89 (+0.42 points), retrieval-augmented planning alone gives 25.53 (+11.06), both together 34.04 (+19.57), which the paper describes as an additional 8.51 points over RAP alone. The baseline and the full system are five-run means; the two single-component variants are single runs.

**Manual quality (Calc, Table 7).** With the full 2021 manual MAGE gets 34.04. The 2010 manual gives 25.53; keeping 75%, 50% and 25% of the 2021 sections gives 25.53, 21.28 and 17.02; without RAP it is 14.89.

**Retrieval quality (Table 8, Table 9).** Top-5 retrieval gives 34.04, five random sections 27.66, sections ranked 6 to 10 give 14.89 (equal to no RAP). Top-K of 1, 3, 5 and 10 gives 25.53, 27.66, 34.04 and 25.53. The authors chose K = 5 from this sweep, which was run on Calc.

**Qualitative case.** On one leading-zeros task the vanilla agent runs out of its 50 steps; MAGE plans a Ctrl+1 shortcut and finishes in five, and a plan made without manual sections finishes in seven.

**Validation of the generated supervision.** Humans judged 150 generated tasks (Calc, Impress, Writer): 93.3% useful, 84.0% feasible, all visually verifiable. Of 47 plans on Calc, 70.21% were helpful by the paper’s definition. The GPT-5.4 evaluator agrees with OSWorld’s rule-based evaluators on 79.82% (91/114) of trajectories across Calc, Impress and Writer, with disagreements mostly on multi-condition tasks that the final screenshots cannot show.

**Cost.** Averaged over five applications with UI-TARS-1.5, adaptation takes 46.62 hours on three NVIDIA H100 GPUs and about \$37.83 in API cost. VSCode was run on six RTX 4090 GPUs: \$91.25 and 108.08 hours.

## Where the evidence is thinner, in the paper’s words

- Apps are not held out. “Training is performed separately for each application to evaluate application-specific adaptation,” and the manual for that application is used for both planning and task construction. Only the Slack test set was built apart from the manuals.
- The ablation, manual and retrieval sweeps are on Calc with one backbone, and the variants are “evaluated using a single run” while the baseline and MAGE are five-run means.
- The judge agreement (79.82%) was measured on three applications; the Slack scores come from a different judge, Gemini 3.1 Pro Preview, and no agreement figure for it is given.
- Slack has a large spread (± 11.88 for MAGE on UI-TARS-1.5), and in Table 1 the unadapted EvoCUA (8B) has 47.54 overall against 47.31 for MAGE (UI-TARS-1.5); the gains are measured against each model’s own base.
- Human review found 84.0% of generated tasks feasible and 72.34% of plans procedurally correct; the paper states that MAGE “is sensitive to retrieval quality”.
- The authors state that the results “do not establish safe deployment in unrestricted settings”.

## CUA Radar’s read

CUA Radar scores this paper **70 (★★★)**, evidence level **online**, pattern K28. The score reflects what the paper reports: online OSWorld evaluation under a 50-step budget, five runs with standard deviations, a component ablation, cost reporting, a check of the VLM judge against the rule-based evaluators, and released code. The judgment record marks held-out evaluation and strong baselines as partial, and flags that the learned judge is only partly validated (AP4) and that the ablation variants are single runs. The radar did not rerun any experiment; every number here comes from the paper (version v1).
