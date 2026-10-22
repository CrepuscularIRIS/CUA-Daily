# EFR: a desktop GUI reflector that marks what changed before judging whether it worked

*A CUA Radar reading of arXiv 2608.24015v1 (Ma, Niu, Wu, Chen; Shanghai Jiao Tong University). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.24015v1*

## The problem: one-pass reflection on large desktop screens

The Planner-Operator-Reflector (POR) loop is a standard skeleton for GUI agents: a planner issues sub-goals, an operator executes grounded actions, and a reflector compares the pre- and post-action screenshots to decide whether the action worked. On desktops this comparison is hard. Screens are, in the paper’s words, “several to even dozens of times larger” than mobile screens, so an action may produce a nearly invisible change (a cursor blink) or many scattered changes at once (switching a year in a calendar view).

The paper quantifies the cost. In GUI-Owl-32B trajectories on OSWorld-Verified, 61 of 223 failed trajectories (27.35%) are attributed to incorrect reflector judgments; of those, 43 cases (70.49%) are page-difference identification errors and 18 (29.51%) are success-judgment errors. The authors’ diagnosis is structural: conventional reflectors “collapse change detection and outcome verification into one step”, so the evidence behind each verdict stays implicit and unchecked.

## What EFR is

The agent is a screenshot-driven desktop agent inside the POR implementation of Mobile-Agent-v3, running in the Docker environments of the two benchmarks. It observes raw screenshots only (no accessibility tree or DOM metadata); it acts through pyautogui primitives — click, double_click, right_click, type, hotkey, scroll, wait, drag, done — adopted unchanged from Mobile-Agent-v3, with a grounding step resolving element descriptions to coordinates. Platforms are the desktop OSes of the benchmarks: Linux (OSWorld-Verified) and Windows (WindowsAgentArena). The architecture pattern on the CUA Radar board is C18, “verify each action’s outcome from before/after observations and feed the verdict back”.

Evidence-First Reflection (EFR) rebuilds the reflector module itself; nothing is trained, and the planner and operator are untouched. After the operator acts, three things happen:

1.  **SoM marking (classical CV).** The pre- and post-action screenshots are converted to grayscale, differenced pixel-wise, thresholded, and turned into contours; nearby regions are merged into red bounding boxes with shared indices, overlaid on both screenshots. The executed action’s coordinates are drawn as a blue circle (or a yellow start/end pair for drags) on the pre-action screenshot.
2.  **Difference analysis and filtering (VLM pass 1).** Given the marked pair and the grounded action — action type and coordinates only, deliberately not the intended action, to reduce intention bias — the VLM describes each region’s change and tags it as action-relevant or environmental noise (a taskbar clock refresh, say). Noise regions are dropped and the remaining boxes redrawn, yielding a “clean” evidence pair plus filtered change descriptions.
3.  **Outcome verification (VLM pass 2).** Given the clean pair, the filtered descriptions, and the intended action, the VLM outputs the reflection: success label, key evidence, and a status summary that feeds the next planning step.

The steering signal is thus the marked visual diff itself; the only supervision in the study is the manual annotation of reflector judgments used for analysis.

## Results, as reported

All numbers are online end-to-end success rates, mean of 3 runs, max 50 steps for GUI-specialized and proprietary models and 15 for open-source general-purpose ones. OSWorld-Verified is used as a 361-task subset (369 minus 8 Google Drive tasks); WindowsAgentArena uses all 154 tasks. The paper reports no offline grounding or step-accuracy metric.

| Backbone     | POR, OSW-V | EFR, OSW-V | POR, WAA | EFR, WAA |
|--------------|------------|------------|----------|----------|
| GUI-Owl-32B  | 37.82      | 44.91      | 29.04    | 34.24    |
| Qwen3-VL-32B | 33.36      | 38.38      | 31.60    | 37.55    |
| Kimi-K2.5    | 52.36      | 59.74      | 47.40    | 52.88    |
| Seed-1.8     | 44.88      | 49.16      | 48.16    | 51.32    |

Average gains are 5.94 points on OSWorld-Verified and 4.95 on WindowsAgentArena, positive for every backbone. The strongest setting, POR-EFR with Kimi-K2.5, reaches 59.74 on OSW-V (+7.38) and 52.88 on WAA (+5.48). Standard deviations of the overall rates across the three runs range from 0.17 to 1.13. On step-level reflector accuracy (manually audited GUI-Owl-32B trajectories on OSW-V), EFR raises the mean from 80.39% to 87.50% (+7.11), while task success rises from 44.91% to 51.94%; the Pearson correlation between reflector accuracy and task success across categories is 0.86.

## What the paper’s own controls say

**Ablation (GUI-Owl-32B, OSW-V).** The full method scores 44.83. Two-stage judging without SoM drops 2.72 to 42.11; SoM without two-stage judging drops 6.70 to 38.13; the plain POR baseline is 37.86 (a 6.97 drop). Swapping the grounded action for the intended action in stage 1 costs 1.38 (43.45), and judging from change descriptions without screenshots costs 10.58 (34.25) — the largest single drop.

**Matched setup.** Baseline and method share the POR implementation, the backbones, the Docker environments, and the step budgets; only the reflector differs.

**Failure attribution.** EFR cuts reflector-attributed failures from 61 of 223 (27.35%) to 27 of 199 (13.57%), a 13.78-point drop; page-difference identification errors fall from 43 to 14 and judgment errors from 18 to 13.

**Cost.** Averaged over the four backbones, per-task latency rises 15.8% and token usage 14.9% on OSW-V (13.3% and 17.9% on WAA), mostly from the extra VLM call. EFR lowers executed steps by 11.5% on OSW-V and 3.7% on WAA, which “only partially offsets the increased per-step reflection cost”; per-step latency and tokens rise 30.8% and 29.8% on OSW-V.

**Outcome flips.** On OSW-V, 12.68% of trajectories flip failure-to-success and 3.27% success-to-failure (10.19% and 4.30% on WAA).

## Where the evidence is thinner, in the paper’s words

- “The large failure→failure proportion indicates that many GUI-agent tasks remain unsolved even after applying our method” — 84.05% on OSW-V, 85.51% on WAA.
- “Explicit visual evidence alone is not always sufficient: the final judgment still requires correctly mapping observed changes to task semantics” — a case study shows EFR observing an `export.jpg.jpg` filename and judging it harmless.
- When EFR does detect a failed action, later modules may not recover: one case’s reflection signal “is not effectively converted into a recovery strategy by the subsequent planner and operator”.
- No code release is mentioned, and the judgment record reads the held-out-environment item as unclear: both benchmarks are standard evaluation suites rather than apps held out from development.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**. The score reflects what the paper reports: online evaluation on OSWorld-Verified and WindowsAgentArena, three-run variance, budget-matched POR baselines, a component ablation, a manual audit of the reflector’s own judgments, and cost accounting. The judgment record also flags AP4 — the reflector is used as a judge without two-sided reliability validation against human verdicts beyond the reported accuracy audit — and lists held-out environment and code as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v1).
