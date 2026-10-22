# GUI-explorer: a training-free phone agent that explores apps and keeps notes on what each tap did

*A CUA Radar reading of arXiv 2505.16827v1 (Xie, Shao, Chen, Zhou, Li, Liu, Zhang, Nie). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2505.16827v1 · Code: https://github.com/JiuTian-VL/GUI-explorer*

## The problem: the model does not know this app

The paper starts from two failure modes of multimodal LLM agents on phones: they misinterpret UI components, and their knowledge of apps is outdated. Its example is a music-recognition icon in QQ Music that GPT-4o misidentifies, while a user familiar with the app reads it correctly. Apps also change often (the paper cites 30 version iterations of Amazon Shopping in 2024) and differ in design (a cart feature that exists in one shopping app may be absent in another), so retraining or fine-tuning a model for every change is described as prohibitively expensive. The authors want an agent that picks up app-specific knowledge without any parameter update.

## What GUI-explorer is

**The agent.** It is an Android agent. At each step GPT-4o receives the task, a screenshot, the same screenshot annotated with numbered boxes from the accessibility tree (Set-of-Mark, “SoM”), the element list and a block of guidance text. It acts through a JSON action catalog that refers to elements by index: click, long press, scroll, text input, keyboard enter, navigate home or back, open app, wait, answer, and a complete or infeasible status. On the CUA Radar board the pattern is C19, “accumulate reusable app knowledge from the agent’s own runs”, under the experience-and-memory-retrieval family.

**Stage 1: goal generation anchored to the app.** The system reads the app’s manifest and collects the activities the developer declared (for example a share-to-story or a drive-mode activity in a music app). These “exploration anchors” are passed with the current screenshot to an MLLM, which proposes up to k candidate tasks. The anchors are meant to stop the model from proposing tasks that target components that do not exist.

**Stage 2: depth-first exploration.** Each task is executed for up to a step limit; the environment is then restored to the parent state before the next sibling task. The paper configures a branching factor of 10, a maximum depth of 5 and a limit of 30 steps for both AndroidWorld and SPA-Bench. This produced over 1,300 knowledge items across 46 applications.

**Stage 3: mining transitions.** For consecutive observations and the action between them, an extractor outputs a key (a visual patch of the UI element that was touched) and a value (a short text on what acting on it does, such as “clicking this button opens search history”). Transitions where the before and after screens are nearly identical (perceptual hash) are discarded, since the action had no effect. New entries are merged into the store when the key embedding is nearly identical (threshold 0.99 or above) and the value is not redundant. No success label or reward is needed, only valid transitions.

**Stage 4: retrieval and ranking at test time.** For every UI element on the current screen the agent retrieves similar stored patches (SigLIP embeddings), then an MLLM compares candidate entries pairwise for relevance to the instruction, and a merge sort turns those comparisons into a ranking. The top entries become the “dynamic guidance” in the prompt.

## Results as reported

Everything in this table is online task success (%) with GPT-4o as the base model; the paper reports one value per cell and no seeds or confidence intervals.

| Agent | SPA-Bench, single-app English, Level 3 | AndroidWorld (116 tasks) |
|----|----|----|
| AppAgent | 14.0 | 14.9 |
| AutoDroid | 12.0 | 15.7 |
| M3A | 42.0 | 40.5 |
| Aria-UI | not listed | 44.8 |
| **GUI-explorer** | **53.7** | **47.4** |

Table 1 also lists MobileAgentV2 (20.0), SeeAct (12.0), CogAgent (0) and DigiRL (0); Table 3 lists Aguvis (37.1), Ponder&Press (34.5), UGround (32.8), SeeAct (15.5, GPT-4-turbo), DigiRL (0.9) and a human reference of 80.0. The first seven rows of Table 1 are taken from the SPA-Bench paper; other baselines are described as reported “in their respective benchmark papers”. The Introduction says the gain over prior methods is between 2.6% and 11.7%, which matches the table (53.7 against 42.0 for M3A; 47.4 against 44.8 for Aria-UI). Section 5.2, however, calls it a “28.1% absolute improvement over M3A”, a figure the table does not support.

**Offline, separate.** The authors also built GUI-KRB, 500 curated samples over 43 apps in 8 categories, which scores a model’s answer about what a UI element does against expert keywords. It is a knowledge benchmark, not a task-success benchmark. Error rates (lower is better), prior-knowledge / dynamic-comprehension: Qwen2-VL 22.8 / 19.8, Qwen2.5-VL 16.6 / 14.0, Gemini 2.0 Flash 15.2 / 11.2, GPT-4o 18.2 / 13.4, GUI-explorer 6.8 / 6.4. The GUI-explorer row uses Qwen2-VL-72B-Instruct-GPTQ-Int4 as base, chosen by the authors as the weakest model to test robustness.

## What the paper’s own controls say

- **Guidance ablation on SPA-Bench.** Removing the dynamic guidance built from transition-aware knowledge causes a 12.2% performance drop. Figure 4 compares no guidance, guidance mined in a different environment (AndroidWorld) and guidance mined in the same environment (SPA-Bench). The text says cross-environment guidance improves over no guidance by 4.3%. The printed labels in the figure read 41.5‡, 46.3‡ and 53.7.
- **Ranker.** On GUI-KRB, turning the ranker off gives 9.8 against 6.8 (prior-knowledge errors) and 6.8 against 6.4 (dynamic comprehension). Appendix F compares alternatives: direct LLM judgment 8.8, confidence score 7.6, sliding-window ranking 6.8, against 6.8 for the paper’s method. The sliding window ties on accuracy; the authors argue merge sort is more parallelizable.
- **Metadata removed.** With goals generated from screenshots only, on tasks from two AndroidWorld apps (Retro Music and Broccoli), success is 16.7 without exploration, 22.2 with screenshot-only exploration and 33.3 with the full method. The number of tasks is not stated in the paper text; the scale is small.
- **Web transfer, offline.** Knowledge mined only on Android, applied to the “website” split of Multimodal-Mind2Web (20 samples): macro element accuracy 45.97 to 47.26, macro step accuracy 42.31 to 43.05. The authors call the gain modest.
- **Cost.** Table 2 gives, per step on average, 7.120 s retrieval, 28.462 s ranking, 30.796 s reasoning, 66.378 s in total, and 0.064 USD in total cost. Ranking is 42.9% of the time. The text’s “0.0015 USD/step” refers to the ranking component only (0.015 in units of 0.1 USD in Table 2).
- **Validity of the mined knowledge.** The authors point to the GUI-KRB dynamic-comprehension task, which they say mirrors their extraction step, where GPT-4o reaches 86.6% accuracy.
- **Errors.** Appendix E groups failures into perceptual errors (for example a filled icon read as unsaved), reasoning errors (appending text instead of replacing it) and missing knowledge (searching the wrong settings menu until the step limit).

## Where the evidence is thinner

- **Exploration and evaluation overlap.** The guidance that gives the full SPA-Bench result is mined by exploring SPA-Bench environments (“in-environment”). Exploration apps are not held-out apps. The cross-environment variant is the closest thing to a held-out test and gives a smaller gain.
- **No variance.** The paper does not report seeds, repeats or confidence intervals for either benchmark.
- **Budget match unclear.** The step budget given to baselines is not discussed beyond the 30-step exploration limit for GUI-explorer, and several baseline numbers are copied from other papers.
- **Mobile only.** The authors list as limitations that anchors rely on Android manifests, so web and desktop are not directly covered, and that the ranker is slow (28.5 seconds per step). The Ethics Statement notes about 66 seconds per step.
- Most experiments ran on a single RTX 4070 laptop GPU (8GB); GPT-4o is called as an API.

## CUA Radar’s read

CUA Radar scores this paper **72 (★★★)**, evidence level **online**. The score reflects what the paper reports: online evaluation on two benchmarks, strong baselines, cost, a component ablation, a check of the mined knowledge on its own benchmark, and released code. The judgment record also marks seeds and variance as not reported, step-budget matching as unclear, held-out apps as partial, and flags the overlap between exploration and evaluation environments. The radar did not rerun any experiment; every number here comes from the paper (version v1).
