# HiViG: a critic that checks the pixels and remembers the past before a computer-use agent acts

*A CUA Radar reading of arXiv 2606.11078v1 (Lee, Khan, Prasad, Chen, Chakraborty, Balasubramaniam, Sahu, Stengel-Eskin, Lee, Bansal). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.11078v1 · Code: https://github.com/G-JWLee/HiViG*

## The problem: critics that read the intent but never check the screen

Computer Use Agents (CUAs) act in graphical interfaces by looking at screenshots and emitting pixel-level actions, and they make mistakes: clicking the wrong element, hallucinating UI items that are not there, re-exploring folders they already checked. Because many GUI actions are irreversible — the paper cites sending an email or deleting a file — correcting mistakes after execution is often unsafe. That motivates test-time intervention before execution. Existing interveners come in two flavors. Scalar process reward models score candidate actions, but when every candidate is poor the scores offer no path forward. Verbal critics explain failures in words, but, as the paper puts it, existing critics “focus primarily on short-sighted decision loops” and “lack the visual grounding needed to detect flawed actions”: they trust the policy’s stated intent and never verify the raw coordinates the action will actually land on.

## What HiViG is

HiViG (History-aware Visually Grounded) is a test-time framework that wraps a frozen policy — the authors use Qwen3-VL-32B-Thinking (open-weight) and Gemini-3-Flash (frontier, closed) — with a small trained critic. The agent perceives only raw screenshots; no DOM and no accessibility tree. Actions are structured JSON pixel tool calls (click, type, scroll, swipe, …) on a normalized 1000×1000 grid, for web, mobile and desktop environments. On the CUA Radar board this sits in pattern C18, verify each action’s outcome and feed the verdict back — here the verdict is moved to before execution.

The critic is HiViG-critic, a multimodal model initialized from Qwen3-VL-8B-Thinking and fine-tuned for one epoch on 52k samples distilled by a Qwen3-VL-32B-Thinking annotator from the open-sourced ScaleCUA trajectory corpus: 20k history state tracking samples and 32k visually grounded error analysis samples (16k expert actions, 16k perturbed actions from a taxonomy of 12 error dimensions). At test time it does two things per timestep:

1.  **Macro-action history.** Before the policy plans, the critic diffs the previous and current screenshots and compresses what has been achieved and what has failed into a running macro-action history, which the policy conditions on — the training signal comes from verified execution outcomes in the source corpus, not the annotator’s guesses.
2.  **Visually grounded error analysis.** After the policy proposes an action, a red-X marker is rendered on the screenshot at the proposed coordinates. The critic identifies the UI element under the marker, predicts the visual state transition, checks alignment with the instruction, and grades the action Good (execute) or Bad (error dimension plus a corrective explanation; the policy refines before executing).

Two training details matter and are ablated: the policy’s verbal intent is masked in 30% of training samples to break text reliance, and the annotator is given ground-truth state-transitions derived from real execution tuples rather than asking it to imagine outcomes.

## Results, as reported

All numbers are execution-based task success rates, online, from a single run per cell (the paper states all results are from a single run due to compute cost; no seeds or variance are reported). Benchmarks: WebArenaLitev2 (154 web tasks, 15-step horizon), AndroidLab (138 tasks over 9 Android apps), WindowsAgentArena (145 Windows 11 tasks, 30-step horizon).

With Gemini-3-Flash as the policy (success rate %):

| Method                 | WALv2    | ALab     | WAA      | Avg.     |
|------------------------|----------|----------|----------|----------|
| Base agent             | 30.5     | 58.0     | 35.8     | 41.4     |
| OpenCUA (scalar PRM)   | 29.9     | 57.2     | 35.8     | 41.0     |
| SE-WSM (scalar PRM)    | 30.5     | 57.2     | 35.1     | 40.9     |
| CGI (32B, verbal)      | 29.9     | 55.8     | 37.9     | 41.2     |
| GUI-Critic-R1 (verbal) | 22.1     | 53.6     | 32.5     | 36.1     |
| **HiViG**              | **45.5** | **61.6** | **44.2** | **50.4** |

With Qwen3-VL-32B-Thinking as the policy, HiViG reaches 25.3 / 51.5 / 38.0 (avg 38.3) against a base agent at 13.0 / 44.2 / 35.7 (avg 31.0). The paper’s headline: WebArenaLitev2 success for Gemini-3-Flash goes from 30.5% to 45.5%, a 15.0-point gain, and average gains over the strongest baseline are 5.8 (Qwen3-VL-32B) and 9.0 (Gemini-3-Flash) points. There are no offline step-accuracy numbers; everything above is online. The largest category-level jumps: the WebArenaLitev2 Map category for Qwen3-VL-32B from 3.9% to 23.1%, and the WindowsAgentArena Office category for Gemini-3-Flash from 4.7% to 23.3%.

## What the paper’s own controls say

**Component ablation (WebArenaLitev2).** Neither component: 30.0 (Gemini-3-Flash) and 13.5 (Qwen3-VL-32B). Visually grounded error analysis alone: 35.1 and 21.4. History tracking alone: 42.9 and 23.4. Both: 45.5 and 25.3. Either component alone beats every baseline, and a single critic inference per step — rather than the full two — is already enough to improve results.

**Matched baselines.** The scalar PRM baselines (OpenCUA, SE-WSM) use the same Qwen3-VL-8B-Thinking backbone as the critic, with N=2 to match the computational cost of verbal frameworks. Scalar feedback yields no improvement over the base agent; baseline interventions at best add 2.1 points (WindowsAgentArena) and at worst drop Gemini-3-Flash by 8.4 (WebArenaLitev2). GUI-Critic-R1 gains 5.1 on AndroidLab but only 0.6 on WebArenaLitev2 and loses 1.3 on WindowsAgentArena.

**Training-data ablations.** Removing the visual marker during training drops WebArenaLitev2 from 25.3% to 20.8% (MLLMs struggle to interpret raw numerical coordinates); removing intent masking drops AndroidLab from 51.5% to 47.1%. Denying the annotator ground-truth state-transitions also drops WebArenaLitev2 to 20.8%. Training one mixed 8B critic (25.3) beats two separate 8B critics (23.4), and matches a zero-shot Qwen3-VL-32B history-provider. A task-level overlap analysis reports 9 tasks fixed only by history tracking, 7 only by error analysis, 6 by both, and 4 only by the combination.

**Cost.** Training took about 4 hours on 8 H100-80GB GPUs; evaluation ran on 8 H100s. History windows are W=4 for the Qwen policy and W=2 for Gemini-3-Flash.

## Where the evidence is thinner, in the paper’s words

- “All experimental results are from a single run, due to heavy compute costs for long-horizon GUI tasks” — no seeds, no variance, and several per-benchmark gaps are a few points.
- The critic’s own accuracy is never measured against ground truth: no precision/recall of Good/Bad verdicts is reported, so the quality of the steering signal is inferred only through end-task success.
- Whether the evaluation environments are held out from the critic’s training corpus (ScaleCUA trajectories spanning web, mobile and desktop) is not stated explicitly; WebArenaLitev2 is introduced by the same ScaleCUA paper.
- Reported failure cases: the critic misses a “dark red” versus “red” color option in Windows Paint, and the macro-action history once recorded a hidden (not deleted) alarm as successfully deleted.
- The 12-error taxonomy “remains bounded by the current landscape of digital interfaces”, in the authors’ own limitation note.

## CUA Radar’s read

CUA Radar scores this paper **63 (★★)**, evidence level **transfer**. The score reflects what the paper reports: execution-based online evaluation across web, mobile and desktop, budget-matched scalar and verbal baselines on the same 8B backbone, component and training-data ablations, and cost reporting. The judgment record flags what is missing: single-run results with no variance, held-out status of the evaluation environments unclear, critic verdicts unvalidated, and the code link unverified. CUA Radar did not rerun any experiment; every number here comes from the paper (version v1).
