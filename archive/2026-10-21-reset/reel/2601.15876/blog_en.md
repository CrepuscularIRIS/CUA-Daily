# EvoCUA: a desktop agent trained on synthetic tasks that ship with their own checkers

*A CUA Radar reading of arXiv 2601.15876v2 (Xue, Peng, Huang et al.; Meituan and collaborators). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2601.15876v2 · Code: https://github.com/meituan/EvoCUA*

## The problem: static traces stop paying off

Native computer-use agents are mostly trained by imitating fixed datasets of recorded interactions. The paper argues that this kind of passive imitation struggles to capture the causal dynamics of long-horizon computer tasks, and that returns from scaling static data are diminishing. It names three obstacles to learning from interaction instead: synthesized tasks are often infeasible (the agent writes plausible plans for impossible goals), large-scale interaction needs infrastructure for asynchronous sandbox rollouts, and unconstrained exploration is too expensive unless training focuses on tasks at the edge of what the policy can do.

## What EvoCUA is

EvoCUA is a native desktop agent. Its only perceptual input is the screenshot; the paper keeps the five most recent screenshots in context and compresses older history into text. At each step it writes a reasoning trace and then one action from a unified action space (Table 6): coordinate-based mouse actions (move, click, double and triple click, drag, scroll), keyboard actions including separate `key_down` and `key_up` so that modifiers such as Shift can be held, and two control primitives, `wait` and `terminate` with a success or failure status. The board files it under pattern K13, checker-first task synthesis, inside the family “ground reward in executable checkers”.

The method has four pieces.

1.  **Verifiable synthesis.** A VLM “task architect” takes a (role, capability, resources) tuple and writes a task instruction together with ground truth and executable validator code. The code is run in a real sandbox and errors are fed back until it executes. Tasks are then filtered by running a reference agent, comparing pass rates from a reward model and the evaluator, and manually spot-checking tasks where the two disagree significantly. A three-way decontamination removes instructions semantically equivalent to benchmark queries, tasks with identical application initialization, and evaluators that overlap with existing evaluation scripts. The paper reports tens of thousands of verified instances.
2.  **Infrastructure.** QEMU-KVM virtual machines inside Docker, a customized Ubuntu 22.04 image, and an asynchronous gateway and scheduler. The paper reports bootstrapping tens of thousands of sandboxes within one minute and sustaining over 100,000 concurrent sandboxes.
3.  **Cold start, then rejection-sampling fine-tuning (RFT).** About 1k trajectories with hindsight-generated reasoning (goal clarification, observation summary, self-check before terminating, reflection) establish the action space and format. RFT then keeps only successful rollouts, allocates rollout budget by a pass@k-guided schedule that concentrates on boundary tasks, and uses a judge model to mask redundant steps.
4.  **Step-level DPO.** For a failed run, the method finds the first step where the agent deviates from a successful reference run while the states are still functionally equivalent. It builds a preference pair at that step (chosen action versus rejected action) and a second pair at the next step that prefers an explicit reflection over blind continuation. The cycle of RFT and DPO is then repeated with the improved policy.

The training signal is therefore a sparse, binary, outcome-level check of the final environment state by the generated validator, plus failure-versus-success preference pairs. The paper’s backbones are Qwen3-VL-Thinking (8B, 32B) and OpenCUA (7B, 32B, 72B).

## Results, as reported

**Online (OSWorld-Verified, pass@1, Table 1).** The step budget is part of the table and differs across rows.

| Model                 | Max steps | Success rate |
|-----------------------|-----------|--------------|
| Qwen3-VL-8B-Thinking  | 100       | 30.6%        |
| Step-GUI-8B           | 100       | 40.2%        |
| **EvoCUA-8B**         | 50        | **46.1%**    |
| Qwen3-VL-32B-Thinking | 100       | 41.0%        |
| OpenCUA-72B           | 100       | 45.0%        |
| UI-TARS-2-2509        | 100       | 53.1%        |
| **EvoCUA-32B**        | 50        | **56.7%**    |
| Claude-4.5-Sonnet     | 50        | 58.1%        |
| Claude-4.5-Sonnet     | 100       | 62.9%        |
| Seed-1.8              | 100       | 61.9%        |

The paper states that EvoCUA-32B is +11.7 above OpenCUA-72B, +3.6 above UI-TARS-2-2509, and 1.4 below Claude-4.5-Sonnet at an equal 50-step budget, and that EvoCUA-8B reaches 46.1% against 40.2% for Step-GUI-8B, which it says starts from the same Qwen3-VL-8B backbone.

**Offline (grounding and general ability, Table 2; not comparable with the table above).** For the OpenCUA-72B backbone the paper reports ScreenSpot-v2 93.47, ScreenSpot-Pro 63.24 and OSWorld-G 67.65 after training, against 92.90*, 60.80* and 66.95 for OpenCUA-72B. For the 32B model the picture is different: ScreenSpot-Pro is 49.76 against 57.10\* for Qwen3-VL-32B-Thinking, and MMMU is 68.11 against 78.10*. For the 8B model, ScreenSpot-v2 is 85.21 against 90.09. (Values with* are taken by the paper from other public reports.) The paper attributes the 32B decline to a mismatch between its non-thinking general-purpose data and the thinking-style base model, and notes shorter outputs (2,514 versus 3,620 tokens).

## What the paper’s own controls say

**Component ablation (Table 3, 32B).** Absolute gain over the previous stage: unified action space +4.84, cold start +2.62, RFT +3.13, offline DPO +3.21, a second iteration of RFT and DPO +1.90. The table does not say which benchmark it uses or what the base score is. The five gains sum to 15.7‡, and Table 1 gives 56.7 − 41.0 = 15.7‡ for the base model; the paper’s text, however, states +15.1 over the base model, and does not reconcile the two.

**Second backbone (Table 4, OpenCUA-72B).** Cold start +2.14, RFT +3.69, offline DPO +3.02, iterative training +1.82. Without any cold start, three rounds of RFT alone give +8.12.

**Experience scaling (Table 5, early OpenCUA-72B iteration, RFT only).** Round 1 on 20k samples: +2.61. Round 2 on 226k: +6.79. Round 3 on 1M: +8.12. The authors say the tolerance for noise falls as the model improves, so data quality and on-policy alignment limit further scaling.

**Pass@k and steps (Figure 6).** The 32B model keeps a positive gain over its base at every k, peaking at +4.93 at k = 16. Going from 15 to 50 maximum steps raises the 32B model by +16.25 relative to its 15-step result.

**Practitioners’ notes (Section 6.5).** From over a thousand experiments totalling more than 1 million accelerator hours, the authors report that aggressive step-level filtering of successful runs is needed, that a lightweight cold start beats a heavy one, and that on-policy data matters.

## Where the evidence is thinner

- **Budgets and variance.** The paper itself notes that EvoCUA’s results use a strict 50-step constraint while baselines typically need 100 steps to reach peak performance. It reports one score per cell, with no seeds or confidence intervals, and says that success rates vary even at temperature 0 because of system perturbations.
- **No held-out application split.** Decontamination removes semantic, configuration and evaluator overlap with the benchmark; tasks are synthesized from desktop applications such as browsers, Excel and Word, and no separate held-out set of applications is reported.
- **Checker quality.** The validators and the reward-model filter are cross-checked by sandbox rollouts and manual spot checks on discrepant tasks; the paper gives no false-positive or false-negative rates.
- **Offline regressions.** The 32B model scores below its base on several offline benchmarks, which the authors expect an upgraded thinking-style general dataset to fix.
- **Online RL is preliminary.** Section 7 introduces a step-level policy-optimization variant (STEPO) and compares it with GRPO on OpenCUA-32B in a figure; the authors say they have not yet done sufficient training and benchmark evaluation. The reported OSWorld numbers come from the offline-synthesis pipeline above.

## CUA Radar’s read

CUA Radar scores this paper **70 (★★★)**, evidence level **online**. The judgment record credits online OSWorld evaluation, strong baselines, cost reporting and a component ablation, and marks validator checking as tested (manual spot checks). Held-out environments and budget matching are recorded as partial, variance as unclear, and code as unclear. Two anti-patterns are flagged: AP4 (a checker or judge used without two-sided reliability validation) and AP9 (missing ablation or matched baseline for the claimed component), the latter with a quote pointing to the Table 3 setup. The radar did not rerun any experiment; every number here comes from the paper (version v2), except those marked ‡.
