# PACE: deciding when compiling a GUI procedure into a program actually saves tokens

*A CUA Radar reading of arXiv 2610.02932v1 (Ming, Xu, Wu, Jia). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.02932v1 · Code: https://github.com/myl7/computer-use*

## The problem: cheap to run is not the same as cheap overall

A computer-use agent that repeats a GUI procedure (add a calendar event, delete a note) can turn its successful traces into a parameterised program. A single model call extracts the task inputs, and the program then runs the procedure with no further model calls. Prior audits report payback counts, the number of uses needed to cover the compilation cost, from 4 to 17, but they measure different parts of the system, so the numbers cannot be compared. The paper names two difficulties. Compilation cost is uncertain, because an attempt can need repair and still produce no usable program. And future reuse is unknown, because tasks may stop arriving or GUI drift may break the program. Compiling early wastes tokens if tasks do not repeat; waiting forfeits savings if they do.

## What PACE is

PACE (Payback-Aware Compilation from Experience) has two parts: a measurement protocol and an online algorithm. The agent reads a screenshot plus an accessibility or DOM tree at every step and runs a ReAct-style loop. A compiled program replaces that loop after one input-extraction call. There is no training: the signal is token charges and verification outcomes. On the CUA Radar board the paper sits in pattern C19, accumulating reusable knowledge from the agent’s own runs.

**Measurement.** Compile from k = 3 completed agent traces (following AutoRPA’s translation and construction stages) with bounded repair, and require the program to pass all three source tasks. Record the cost of successful and failed attempts, and compare program and agent costs on matched inputs, in weighted tokens. Families: four AndroidWorld tasks, two custom LibreOffice tasks in an OSWorld-based container, and one WebArena Reddit comment task, with GLM 5.3 Flash, DeepSeek Flash and Qwen 3.8 Flash.

**Online algorithm.** PACE serves each arriving task first, then considers compiling. A savings test compares the estimated future saving with the estimated compilation cost, including expected failed attempts. A separate budget check reserves the worst-case charge before any serving or compiling action. Under the stated cost-model assumptions, cumulative cost stays at most 1 + ε times the cost of serving every task with the agent after each arrival; ε = 0.25 in the main evaluation. The paper says this bounds cost, not task success, and does not claim PACE minimizes expected cost.

## Results, as reported

**Measured compilation costs.** Eleven of twenty cells with compilation-stage records produced programs that passed verification. Extraction costs of those programs range from 331 to 724 tokens, with estimated saving shares of 0.936 to 0.999. On 180 matched agent replays across six verified Android programs, saving shares range from 0.952 to 0.999; 157 agent runs and 178 program runs succeeded. Among DeepSeek attempts with complete records, failed attempts have a median cost of 1701K tokens against 259K for successful ones. The payback count excluding source runs is 1.389 to 15.488 uses.

**Simulated decision rules (offline).** Policies are compared under the same compiler and the same cost charges; the baselines are decision-rule adaptations of AutoRPA (one attempt, no retry) and ToolPro (counts the saving of the current task only), not the original systems. ToolPro’s cost equals ReAct’s in these conditions. On two grids of 300 conditions each, ReAct costs 1.107 and 1.130 times PACE on average. On four recorded arrival sequences (two process logs, two Wikipedia edit streams) PACE is 17.34% cheaper than ReAct (conditional 95% interval \[14.96, 19.61\]%) and cheaper in nine of twelve model-and-log conditions; the abstract also gives 24.9% against the AutoRPA adaptation.

| Cost, GLM 5.3 Flash (× PACE) | Sepsis | BPI 2019 | Wiki tools | Wiki humans |
|------------------------------|--------|----------|------------|-------------|
| ReAct (= ToolPro)            | 0.971  | 1.531    | 1.730      | 1.056       |
| AutoRPA adaptation           | 1.145  | 1.582    | 1.754      | 1.164       |
| PACE                         | 1.000  | 1.000    | 1.000      | 1.000       |

Note that ReAct is cheaper than PACE on Sepsis in this column; PACE’s largest ratio to ReAct is 1.030 and its lowest is 0.578. No online task-success benchmark is reported: everything above is cost, simulated on measured profiles.

## What the paper’s own controls say

**Ablations (logs, mean over models).** Removing the savings test raises cost by 52.68% (\[48.25, 58.36\]%); using one cost for successful and failed attempts raises it by 23.34% (\[19.18, 28.06\]%); eager retry costs 3.303 to 4.922 times full PACE. Removing the budget changes mean cost on the logs by only 0.0013%, but raises the largest tested ratio to ReAct from 1.2468 to 1.7563, so its contribution is protection against large losses. Across 4800 grid runs and 120 log runs every recorded cost ratio stayed within the 1.25 bound.

**Cost assumptions.** Varying the failed-to-successful compilation cost ratio over 0.5, 1, 2 and 5 gives mean PACE-to-ReAct ratios of 0.833 to 0.866 on the logs. When high compilation costs go to frequent families with low verification probability, the mean is 1.015, about 1.5% above ReAct, so task frequency alone does not decide when to compile.

**Live check.** A separate study on the OpenApps Calendar app tests a fixed, pre-compiled program, not the online algorithm: twelve agent/program pairs (four seeds, three interface conditions). The agent succeeded in 7 of 12 (four call interruptions); program plus agent fallback succeeded in 11 of 12. Mean serving cost bounds are 8.142 to 21.590 milli-USD for the agent and 1.202 to 4.564 for the program path.

## Where the evidence is thinner, in the paper’s words

- “We used these grids while developing PACE, so the comparisons are not independent confirmation.”
- The logs give task frequencies and arrival order, not live GUI tasks; costs and outcomes are assigned to families, and the policies receive family labels and failure parameters.
- Historical mean costs “do not provide the action bounds required for the cost guarantee.”
- The live study uses four seed clusters and one task family; its 95% envelope for the paired cost difference, \[-33.017, 4.621\] milli-USD, includes zero.
- Latency, device use and program-maintenance effort are excluded; silent program failures and partly changed interfaces need further evaluation.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **offline**. The record credits bootstrap intervals, baselines charged under the same cost model, cost reporting, a component ablation and released code, and marks online evaluation and held-out evaluation as partial. The judgment flags the development-grid caveat quoted above. The radar did not rerun any experiment; every number here comes from the paper (version v1).
