# UI-TARS: a screenshot-only “native” GUI agent trained on its own corrected traces

*A CUA Radar reading of arXiv 2501.12326v1 (Qin, Ye, Fang, Wang, Liang, et al.; ByteDance Seed and Tsinghua University). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2501.12326v1 · Code: https://github.com/bytedance/UI-TARS*

## The problem: agent frameworks lean on a general model and hand-written glue

Many GUI agents wrap a general model such as GPT-4o in prompts, tool modules and hand-written workflows, often reading HTML or accessibility trees that differ across platforms. The paper argues for a “native agent”: one model that folds perception, action, reasoning and memory together, takes screenshots as input and is trained end to end. Its stated obstacle is data: the transition from frameworks to agent models “introduces a fundamental data bottleneck”, because large, standardized records of real GUI interaction are scarce.

## What UI-TARS is

UI-TARS sees only screenshots (the last N = 5 observations are kept, together with its earlier thoughts and actions) and acts through a unified action space shared across desktop, mobile and web: click, drag, scroll, type, hotkeys and a few control actions. Before each action it writes an explicit “thought”. On the CUA Radar board it is in pattern K25, action traces with generated thoughts, under trajectory-level policy training.

The paper lists four ingredients:

1.  **Perception data.** Large GUI datasets for element description, dense captioning, state-transition captioning, question answering and set-of-mark prompting.
2.  **Unified action modeling.** Standardized actions across platforms, a large set of action traces (annotated plus standardized open-source data) and grounding data pairing element descriptions with coordinates.
3.  **System-2 reasoning.** About 6M crawled GUI tutorials, filtered, and reasoning patterns injected into the collected traces: task decomposition, long-term consistency, milestone recognition, trial and error, reflection.
4.  **Iterative refinement from online traces.** The model explores task instructions (human-written and model-generated) on hundreds of virtual PCs. Traces pass a rule-based reward, a VLM score threshold and partial human review. Annotators also label error corrections and “post-reflection” recovery steps. The corrected steps are used for supervised fine-tuning, and corrected-versus-erroneous action pairs are used for DPO. The improved model then collects the next round.

Training starts from Qwen-2-VL (the 7B and 72B variants are the ones reported here) on about 50 billion tokens in three phases: continual pre-training, annealing (the resulting model is called UI-TARS-SFT) and DPO (UI-TARS-DPO).

## Results, as reported

Online benchmarks, screenshot-only. OSWorld has 369 tasks, and its score is averaged over 3 runs; AndroidWorld has 116 tasks on a live emulator. Table 9 gives the OSWorld rows without a step label under a 15-step cap.

| Model | OSWorld, 15 steps | OSWorld, 50 steps | AndroidWorld |
|----|----|----|----|
| Aria-UI + GPT-4o (framework) | 15.2 | not reported | 44.8 |
| Aguvis-72B | 10.3 | not reported | 26.1 |
| Claude Computer-Use | 14.9 | 22.0 | 27.9 |
| UI-TARS-7B-SFT / DPO | 17.7 / 18.7 | not reported | 33.0 / not reported |
| UI-TARS-72B-SFT | 18.8 | not reported | 46.6 |
| **UI-TARS-72B-DPO** | **22.7** | **24.6** | not reported |

The paper notes that 72B-DPO at 15 steps (22.7) is comparable to Claude with a 50-step budget (22.0), and calls 24.6 at 50 steps a new state of the art on OSWorld. On AndroidWorld, the 72B-SFT model’s 46.6 exceeds the best previous framework (44.8) and agent model (26.1). Offline results are reported elsewhere in the paper and kept apart here: for example 82.8 for the 72B model on VisualWebBench against 78.5 for GPT-4o, and 38.1 on ScreenSpot-Pro.

## What the paper’s own controls say

**DPO.** Comparing SFT and DPO models on OSWorld at 15 steps: 72B 18.8 to 22.7, 7B 17.7 to 18.7. The paper reads this as negative samples helping the model separate better from worse actions. This is the only component ablation reported, and DPO is evaluated only on OSWorld; for the other benchmarks the SFT model is used.

**Scale.** The 72B model beats the 7B model by more online than offline, which the paper takes as evidence that scale improves system-2 reasoning and that offline benchmarks alone may not capture real-time capability.

**System 1 versus system 2 (offline).** On three in-domain benchmarks with best-of-N sampling, system 2 is slightly below system 1 at N = 1 and clearly ahead at N = 16 and 64; on out-of-domain AndroidWorld (N = 1) the paper reports system 2 significantly ahead. Exact values are shown only in a figure.

## Where the evidence is thinner

- No standard deviation or interval is reported; only OSWorld says it is a 3-run average.
- The paper does not state whether OSWorld applications or tasks overlap with the online-trace tasks used for training. It only calls AndroidWorld out-of-domain (no corresponding training data); the CUA Radar record marks held-out evaluation as unclear.
- Some step budgets are not labelled in Table 9 and follow the caption’s 15-step cap; the 50-step comparison has a single baseline, Claude.
- The DPO model is not evaluated on AndroidWorld, so the 46.6 comes from the SFT model.
- Human annotators review traces and label corrections, so the loop is not fully automatic. The VLM scoring filter is not validated in the paper, and training compute is given only as about 50B tokens.

## CUA Radar’s read

CUA Radar scores this paper **67 (★★)**, evidence level **transfer**. The record credits online evaluation on two benchmarks, step budgets matched to Claude’s, a 3-run mean on OSWorld, and a DPO comparison; the abstract states the model is open sourced at the linked repository, although the record lists code as unclear. Held-out environments, variance and validation of the trace filter are recorded as not reported. The radar did not rerun any experiment; every number here comes from the paper (version v1).
