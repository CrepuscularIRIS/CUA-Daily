# VLAA-GUI: a prompted desktop agent that checks before it says “done”, escalates when it loops, and looks things up when it is lost

*A CUA Radar reading of arXiv 2604.21375v3 (Han, Tu, Wang, Dai, Zhou, Lau, Cardenas, Xu, Xu, Xiong, Zheng, Yao, Zhou, Xie). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2604.21375v3 · Code: https://github.com/UCSC-VLAA/VLAA-GUI*

## The problem: stopping too early, and going in circles

The paper names two failure modes of desktop GUI agents. The first is early stopping: the agent declares success “without verifiable evidence”, for example after toggling a setting without checking that the state changed. Existing planners track progress through generated subtasks, but “completing planned steps does not guarantee that the user’s requirements are met”. The second is repetitive loops: anti-loop heuristics usually detect only local repetition and have no way to escalate recovery when the agent stays stuck. Agents also stall on unfamiliar workflows, where a screenshot shows the interface but not the procedure.

## What VLAA-GUI is

VLAA-GUI is a modular framework around one **Manager** agent running a perceive-reason-act loop. The Manager sees screenshots (captured at 1920×1080) together with the task, its history and tool results. It acts with GUI primitives issued as `pyautogui`-style calls (click, type, scroll, hotkey, drag, open an application) or by calling a tool; tools and primitives share one action space. The evaluated platforms are desktop Linux (OSWorld) and Windows (WindowsAgentArena, WAA). On the CUA Radar board the paper sits in pattern C18, “verify each action’s outcome and feed the verdict back”. Nothing is trained: all roles are frontier models driven by prompts printed in the appendix.

The mechanism has five parts, two mandatory and three on-demand:

1.  **Completeness-Aware Planner (CAP), mandatory.** A *Completion Gate* derives K UI-observable success criteria from the instruction and re-checks their evidence at every step, using action-specific rules. It says DONE only if all criteria pass and the UI is stable. When the gate says DONE, a separate *Completeness Model Judge* (temperature 0.2) re-reads the instruction, the screen and the recent trajectory. Termination needs both to agree; on rejection the missing-evidence feedback goes back to the Manager.
2.  **Loop Breaker, mandatory.** It runs after every action. Tier 1: if the same action on the same target gives no visible change twice, the agent must switch interaction modality. Tier 2: if the same screen recurs three times, it must change its overall strategy. Tier 3: an external reflection agent returns keep or switch, and on switch the repeated action is blacklisted. The thresholds are fixed across tasks and both benchmarks.
3.  **Search Agent, on demand.** One “How to” query to an LLM with search grounding (Gemini 3 Pro or 3.1 Pro) returns a plain-text tutorial, with no browser navigation.
4.  **Coding Agent, on demand.** Runs Python or Bash, with 20 code-execution steps of its own.
5.  **Grounding Agent, on demand.** Localizes screen elements (Seed 1.8 by default, MAI-UI in one variant).

## Results, as reported

All results below are online success rates (%) on OSWorld-Verified (361 tasks, Ubuntu) or WAA (154 tasks, Windows). The paper reports no seeds or confidence intervals for the main tables. Baseline rows come from the OSWorld leaderboard (except OS-Symphony at 100 steps, from its paper) and use different backbones, so they are reference points rather than same-model comparisons.

**OSWorld-Verified, by step budget (Table 1, average column):**

| Method                     | 15 steps | 50 steps | 100 steps |
|----------------------------|----------|----------|-----------|
| VLAA-GUI w/ Gemini 3 Flash | 43.15    | 63.14    | 68.77     |
| VLAA-GUI w/ Sonnet 4.6     | 64.13    | 71.11    | 71.67     |
| VLAA-GUI w/ Opus 4.6       | 64.75    | 73.85    | 77.45     |
| OS-Symphony w/ GPT-5       | –        | 65.77    | 65.84     |
| HIPPO w/ Opus 4.5          | –        | –        | 74.49     |

At 100 steps VLAA-GUI with Gemini 3.1 Pro is at 72.47 and with Opus 4.5 at 74.89 (76.26 with the MAI-UI grounder), against Agent S3 w/ Opus 4.5 at 66.00. The human reference is 72.4; the paper counts three backbones as above it at 100 steps.

**WindowsAgentArena (Table 3, overall):**

| Method                               | 50 steps | 100 steps |
|--------------------------------------|----------|-----------|
| VLAA-GUI (Gemini 3 Flash as Manager) | 60.4     | 61.0      |
| Agent S3 w/ GPT-5                    | 54.1     | 56.6      |
| GTA1-32B w/ o3                       | –        | 51.2      |

## What the paper’s own controls say

**Same-backbone control.** Under the authors’ harness, the Sonnet 4.6 base scaffold (with coder and grounder) scores 69.19 against 71.67 for the full framework, with the same backbone, grounding, action interface and budget. The paper reports this as a 2.48 gain.

**Component ablation on OSWorld (Table 2).** For Sonnet 4.6 at 100 steps: 71.67 full, 68.81 without CAP, 70.04 without Search, 71.63 without the Loop Breaker. The paper reads this as CAP -2.86, Search -1.63, Loop Breaker -0.04. For Gemini 3 Flash at 100 steps: 68.77 full, 67.34 without CAP, 66.95 without the Loop Breaker, 65.82 without Search. The paper says the results “support configuration-dependent benefits rather than a claim that every module always improves performance”.

**Not always positive.** At 50 steps Gemini 3 Flash scores 66.00 without CAP and 63.14 with it. In the appendix, at 15 steps CAP and Search lower Flash’s score (the paper gives -11.3 and -9.7), and the Loop Breaker lowers it from 49.30 to 43.15, because tool calls and escalation actions consume a small budget. Sonnet 4.6 gains at every budget from CAP and Search.

**WAA ablation (Table 3).** At 100 steps the full system scores 61.0; without CAP 51.3, without the Loop Breaker 55.8, without Search 53.9.

**False completion.** For Sonnet 4.6 at 100 steps, CAP reduces false DONE counts from 105 to 91, and the share of failed tasks ending in a false completion from 95.5 to 91.9. For Gemini 3 Flash the counts go from 102 to 100 (91.9 to 86.2). The paper’s summary: “most failed tasks still end with an incorrect completion claim”, so CAP “only partially resolves false completion”.

**Loops.** For Gemini 3 Flash the wasted-steps ratio falls from 4.9 to 2.8 with the Loop Breaker, and loop incidence among failed tasks from 20.7 to 16.2. Flash loops roughly twice as often as Sonnet (10.6 against 5.0 of all tasks).

**Transfer to CoAct-1.** On a fixed 60-task OSWorld subset (Gemini 3 Flash, 100 steps), CoAct-1 scores 65.13. Adding CAP gives 68.91, the Loop Breaker 66.06, Search 65.96, and all three 70.34.

## Where the evidence is thinner, in the paper’s words

- The 60-task subset is “non-random” and supplies “controlled point estimates, not population-level or statistically significant claims”; no confidence intervals are given.
- Loop thresholds are “hand-designed” and “have not been evaluated in a sensitivity sweep”; the 0.04 Sonnet gain at 100 steps shows recovery helps most when the agent is prone to loops.
- All evaluated Manager backbones are proprietary, and the extra studies also use a proprietary Gemini 3.1 Pro coder and searcher. Search results and model versions change over time.
- Tracked cost is “a lower bound”; CAP raises mean actions per task from 16.80 to 27.32, and fixed-action-budget scores are not equal cost efficiency.
- Table 1 lists HIPPO w/ Opus 4.5 (74.49) and Kimi K2.6 (73.07) above the 72.4 human reference at 100 steps, while the text calls VLAA-GUI the first GUI framework above it. Baselines differ in backbone and tools, so rows should be compared with care.

## CUA Radar’s read

CUA Radar scores this paper **73 (★★★)**, evidence level **transfer**, pattern C18. The judgment record lists online evaluation, a second environment (WAA), a same-backbone control, three step budgets, a component ablation and a check of the false-completion judge as present; seeds or variance, cost and code are recorded as not established. (For reference, the paper’s appendix does give tracked cost lower bounds for the 60-task subset, and the first page links a code repository.) The record flags one failure case: verification lowered Gemini 3 Flash’s score at 50 steps. The radar did not rerun any experiment; every number here comes from the paper (version v3).
