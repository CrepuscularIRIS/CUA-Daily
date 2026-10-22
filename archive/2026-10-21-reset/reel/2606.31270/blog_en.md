# Learning from Failure: a computer-use agent whose failed trajectories become inference-time patches

*A CUA Radar reading of arXiv 2606.31270v1 (Sun, Wang, Schmidt, Yeung-Levy, Zhang; Stanford and Tsinghua). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.31270v1 · the abstract lists code at github.com/snow10072740/Learning_from_Failure (the radar’s judgment record marks code availability unclear).*

## The problem: the success loop throws most of the data away

The standard way to build a computer-use agent is a self-improving loop: put the agent in a verifiable environment, keep the trajectories the verifier scores as successes, and fine-tune on them. The paper’s opening observation is that this loop “exploits only successful trajectories and discards the failed ones, even though failures carry rich information about a model’s weaknesses” — and that the discarded failures come from environments that themselves “require considerable human engineering effort” to build. The question the paper asks is direct: can failed trajectories, at inference time and without any training, upgrade the agent?

## What the method is

The agent is OpenCUA-72B, an open-source 72B multimodal model, operating a real computer in OSWorld: it observes screenshots and acts with low-level mouse and keyboard operations (click, moveto, dragto, typing). After patching, its action space also includes a terminal (opened with the Ctrl+Alt+T hotkey) and a search tool. On the CUA Radar board the paper sits in pattern C19 under experience memory retrieval: accumulate reusable knowledge from the agent’s own runs — here the accumulated knowledge is failure-derived code patches rather than prompt-side tips.

The loop has three moving parts:

1.  **Failure collection.** The agent rolls out tasks; the environment’s built-in verifier labels each trajectory. Failed trajectories — instruction, action history and thought process — are kept.
2.  **LLM diagnosis.** A meta-controller LLM, Claude 4.5 Sonnet (picked over GPT-5.2, Gemini 3 Flash and Qwen3-VL-32B-Instruct for more consistent analysis and stronger code implementation), reads each failed trajectory, names a failure mode, and proposes an improvement as a code patch.
3.  **Light human verification.** A human selects and minimally adjusts the patch before it is injected into the agent’s inference-time workflow. The paper quantifies this: “over 97% of LLM-generated refinements are accepted without modification”, and human edits account for “less than 3% of the modified lines on average”.

The loop runs for four rounds, one strategy per round, and the strategies accumulate. Four failure categories produce four strategies:

- **Grounding errors → visual search.** After a grounded action (click, moveto, dragto), a 400×400 crop centered on the action point is upscaled 2× and marked with a red circle of radius 7 pixels; the agent re-examines this view and either confirms or adjusts its coordinates — post-action visual self-verification.
- **Competency gaps → terminal execution.** A hotkey opens a terminal so operation-intensive tasks become command lines instead of long GUI sequences.
- **Knowledge deficiencies → knowledge support.** A curated LibreOffice hotkey manual plus a search interface backed by GPT-5-mini for procedural knowledge the model lacks.
- **Redundant loops → repetition warnings.** A sliding window of the last 5 steps flags a thought or action pattern that appears at least 3 times; a hashed accessibility-tree representation flags a screen unchanged for 3 consecutive steps. A warning pushes the agent into a recovery mode with an alternative strategy.

The training signal is the environment verifier’s pass/fail — but it is the failures, not the successes, that steer the improvement. No weights are updated at any point.

## Results, as reported

**Online, OSWorld full set, 100-step budget, success rate (%).** Main rows are the mean ± standard deviation over 3 independent runs; rows marked \* are single runs “due to resource constraints”.

| Agent             | Steps | Success rate   |
|-------------------|-------|----------------|
| Claude 3.7 Sonnet | 100   | 28.0           |
| OpenAI CUA 4o     | 200   | 38.1           |
| UI-TARS-1.5       | 100   | 42.5           |
| OpenAI CUA o3     | 200   | 42.9           |
| GUI-Owl-32B       | 100   | 19.0 \*        |
| \+ Ours           | 100   | 21.3 \*        |
| OpenCUA-32B       | 100   | 34.5 \*        |
| \+ Ours           | 100   | 38.2 \*        |
| OpenCUA-72B       | 100   | 42.3 ± 2.6     |
| **+ Ours (main)** | 100   | **48.9 ± 1.2** |

The paper reports this as an absolute gain of +6.6 points (+15.6% relative), with “about an 8% increase in runtime” and interaction steps reduced “by roughly 15%”, at no additional training cost. For the two 32B backbones it reports consistent +10–12% relative gains.

**Ablation, OSWorld small set (a lightweight subset used for rapid iteration), 30-step limit, online.**

| Configuration                   | Success rate |
|---------------------------------|--------------|
| Baseline OpenCUA-72B (30 steps) | 41.67        |
| \+ Visual search                | 47.22        |
| \+ Terminal execution           | 47.19        |
| \+ Knowledge support            | 44.44        |
| \+ Repetition detection         | 44.40        |
| \+ Full method                  | 52.74        |

The text states +5.52 points for terminal execution and +2.73 for repetition detection on this set.

**Cross-benchmark transfer of the OSWorld-mined patches** (Qwen3-VL-32B-Instruct backbone, 3 repeats except WebVoyager). The paper does not split these by online/offline; on the radar’s taxonomy WebVoyager is an online benchmark while AndroidControl and ScreenSpotPro are offline benchmarks, so we keep them off the online axis above.

| Benchmark                       | Base         | Ours         |
|---------------------------------|--------------|--------------|
| OmniACT                         | 4.77 ± 0.02  | 6.90 ± 0.10  |
| AndroidControl (offline)        | 28.37 ± 0.13 | 36.23 ± 0.22 |
| ScreenSpotPro (offline)         | 27.50 ± 0.35 | 30.74 ± 0.27 |
| WebVoyager (online, single run) | 23.80        | 27.90        |

The paper calls out the largest gains on WebVoyager (+4.10 points) and AndroidControl (+7.86 points).

## What the paper’s own controls say

- **Fair comparison.** The refined framework “retains exactly the same tool access, environment configurations, and action spaces as the baseline agents.”
- **Component ablation.** Every strategy helps alone and the combination (52.74) beats any single one (41.67 baseline); the paper reads this as the strategies composing constructively across four stacked updates.
- **Failure modes shift.** Categorized by the LLM, action loops fall from 43% of failures to 24% and coordinate-precision errors from 24% initially; what remains is dominated by multi-step planning (28%), UI recognition (24%), CAPTCHA (12%) and task misinterpretation (12%). The paper’s reading: low-level bottlenecks are fixed, higher-level cognition remains.
- **Human involvement measured.** \>97% of patches accepted as-is; under 3% of lines adjusted.
- **Variance reported where it matters most.** Mean ± std over 3 runs for the main rows and three of four transfer benchmarks; the 32B cross-model rows and WebVoyager are single runs and are marked as such.

## Where the evidence is thinner

- The patches are mined on OSWorld and the headline gains are measured on OSWorld; the cross-benchmark table is the paper’s own transfer evidence, and the radar’s record rates held-out evaluation partial for exactly this reason (anti-pattern AP5: synthesis or memory data overlapping the evaluation).
- Some leaderboard baselines run at 15, 50 or 200 steps rather than 100, so those comparisons are not budget-matched.
- The meta-controller comparison (Claude 4.5 Sonnet vs GPT-5.2, Gemini 3 Flash, Qwen3-VL-32B-Instruct) is qualitative; no numeric table is given.
- The judgment record marks code availability unclear, though the abstract announces a repository.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **transfer**, sub-pattern C19 (accumulate reusable knowledge from the agent’s own runs). The score reflects what the paper reports — online OSWorld evaluation, 3 runs with standard deviation on the main result, cost reporting, a per-strategy ablation, and transfer across models and benchmarks — and what it does not: a code check, and full budget matching on the leaderboard. The record also flags AP5. The radar did not rerun any experiment; every number here comes from the paper (version v1).
