# Agent S2: a computer-use agent that routes actions to specialist grounders and replans after every subgoal

*A CUA Radar reading of arXiv 2504.00906v1 (Agashe, Wong, Tu, Yang, Li, Wang — Simular Research). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2504.00906v1 · Code: https://github.com/simular-ai/Agent-S*

## The problem: one generalist does everything, badly in three places

Computer-use agents operate a desktop or phone through the GUI itself. The paper names three limits of monolithic agents that use a single generalist model for everything. First, grounding: turning a textual description of a UI element into a precise pixel coordinate is still unreliable. Second, long horizons: tasks span multiple apps and screens, and pop-ups, distractions and evolving observations defeat a plan fixed at the start. Third, the generalist bottleneck: a single model asked to plan, act and ground is, in the paper’s words, outperformed by specialist models on domain-specific subtasks, which “constrains the overall performance of computer-use agents”.

## What Agent S2 is

Agent S2 is a prompted, compositional framework; no component is trained in this paper. The agent perceives **screenshots plus action history only** — it deliberately drops the accessibility tree that earlier hierarchical agents used. It acts through a function-call-style action space (Table 8 of the paper): click, type, scroll, hotkey, hold-and-press, drag and drop, highlight a text span, set cell values, save to knowledge, switch applications, wait, done, fail. Platforms are desktop Linux (OSWorld, 369 tasks), Windows (WindowsAgentArena, 154 tasks) and Android (AndroidWorld, 116 tasks over 20 apps, run in a worker-only configuration because the tasks are shorter). On the CUA Radar board its architecture pattern is C10, “split a generalist planner that describes the target from a specialist grounder that localises it”.

Two mechanisms carry the paper:

1.  **Mixture of Grounding (MoG).** A generalist Worker emits an atomic action together with a natural-language description of its target, then acts as a gating network that routes the grounding to one of three specialists: a Visual Grounding expert (UI-TARS-72B-DPO) that returns pixel coordinates for any point on the screen; a Textual Grounding expert (Tesseract OCR) that takes the start and end phrases of a span and returns span coordinates for word-level selection; and a Structural Grounding expert (the UNO interface) that takes a dictionary of cell:value mappings and writes spreadsheet cells programmatically. The worker can also refine its descriptions over time to self-correct.
2.  **Proactive Hierarchical Planning (PHP).** A generalist Manager decomposes the instruction into subgoals. After **every** completed subgoal — not only after a failure, as in reactive planning — it regenerates the remaining subgoals from the original instruction, the completed subgoals and the latest screenshot, recontextualising the task as observations evolve.

The system also reuses the Agent S knowledge base (task- and subgoal-level interaction experience plus web knowledge). There is no training signal anywhere in Agent S2 itself; the “signal” is the composition, i.e. which specialist the Worker routes each action to, and the fresh observation that drives each replan.

## Results, as reported

All numbers below are **online success rates** from functional evaluation scripts; the paper reports no offline step or grounding accuracy for Agent S2. Step budgets are 15 and 50 steps, and on OSWorld and WindowsAgentArena a task that hits the step limit before the agent signals completion counts as a failure. No seeds, run counts or variances are reported.

| Method                              | OSWorld 15-step | OSWorld 50-step |
|-------------------------------------|-----------------|-----------------|
| CCU w/ Claude-3.5-Sonnet (new)      | 14.9            | 22.0            |
| CCU w/ Claude-3.7-Sonnet            | 15.5            | 26.0            |
| OpenAI CUA (Operator)               | 19.7            | 32.6            |
| UI-TARS-72B-DPO                     | 22.7            | 24.6            |
| Agent S2 w/ Claude-3.5-Sonnet (new) | 24.5            | 33.7            |
| **Agent S2 w/ Claude-3.7-Sonnet**   | **27.0**        | **34.5**        |

The paper reports relative improvements of 18.9% (15-step) and 32.7% (50-step) over the leading baselines (UI-TARS and Claude Computer Use, per its footnote). On the 50-step run the Claude-3.7 variant scores 50.00 on OS tasks, 49.73 on Daily, 57.14 on Professional, but 25.64 on Office and 18.21 on Workflow — the hard categories stay hard.

| Method       | WindowsAgentArena (15 steps) |
|--------------|------------------------------|
| Agent S      | 18.2                         |
| NAVI         | 19.5                         |
| **Agent S2** | **29.8**                     |

| Method           | AndroidWorld |
|------------------|--------------|
| GPT-4o + UGround | 44.0         |
| GPT-4o + Aria-UI | 44.8         |
| UI-TARS-72B-SFT  | 46.6         |
| **Agent S2**     | **54.3**     |

These are +52.8% relative on WindowsAgentArena (over NAVI) and +16.52% relative on AndroidWorld (over UI-TARS), as reported. Note the input asymmetry: on WindowsAgentArena, Agent S and NAVI also read the accessibility tree, while Agent S2 uses screenshots only; on OSWorld all listed baselines are screenshot-input except Agent S.

## What the paper’s own controls say

- **Step-budget standardisation.** Both 15- and 50-step numbers are given for the same agents; Agent S2’s margin grows with the budget (27.0 to 34.5), while UI-TARS-72B-DPO barely moves (22.7 to 24.6).
- **Backbone swap.** With Claude-3.5-Sonnet (new) in both Manager and Worker, Agent S2 still gets 24.5 / 33.7, which the paper reports as 58.1% and 29.6% relative over Claude Computer Use with the stronger 3.7 model — the argument that composition, not the backbone, carries the gain.
- **Component ablations (65-task OSWorld subset).** Removing MoG drops success from 30.77 to 27.69 at 15 steps and from 38.46 to 33.85 at 50 steps; proactive over reactive planning is worth +4.62 points at 15 steps and +6.15 at 50. Removing the Textual expert from routed tasks lowers subtask success from 70.6% to 65.2%; removing the Structural expert, from 73.7% to 69.4%.
- **Grounding-expert swap.** In the visual slot, smaller open models (UI-TARS-7B-DPO, UGround-V1-7B) outperform Claude-3.7-Sonnet inside the framework — the specialist does not have to be big.
- **Error analysis.** With grounding delegated, planning failures become the most frequent error category, while grounding errors are relatively less common than in earlier reports.
- **Scaling behaviour.** Of the tasks that fail at 15 steps but pass at 50, the paper attributes the flips mainly to adaptive navigation and adaptive interaction, plus backward correction and irreducible task complexity.

## Where the evidence is thinner, in the paper’s words

- No seeds, repetitions or variance are reported for any headline number.
- Cost is not reported, although the framework issues multiple model calls per step (Manager, Worker, expert).
- The ablations run on a 65-task stratified subset of OSWorld, not the full 369.
- Relative-improvement percentages are computed against different baselines per benchmark (footnote 1), which the main text does not always restate.
- The Structural expert is an app-specific API (UNO for LibreOffice); the paper’s own failure analysis notes planning failures now dominate, and Office (25.64) and Workflow (18.21) remain the weakest OSWorld categories.
- AndroidWorld is evaluated worker-only, so the Manager/PHP mechanism is untested there.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **transfer**, sub-pattern C10 under the planner-grounder-interface pattern. The judgment credits online evaluation, generalisation to held-out operating systems and apps, strong baselines (OpenAI CUA, Claude Computer Use, UI-TARS), matched 15/50-step budgets, component ablations and released code; it marks variance and cost as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v1).
