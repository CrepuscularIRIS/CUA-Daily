# OpenCUA: an open pipeline from human desktop demonstrations to a screenshot-based computer-use agent

*A CUA Radar reading of arXiv 2508.09123v3 (Wang, Wang, Lu, Yang, Xie, Wang et al., XLANG Lab and Moonshot AI). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2508.09123v3 · Code: https://github.com/xlang-ai/OpenCUA*

## The problem: the strongest CUA recipes are closed

The paper starts from the observation that the data, architectures and training processes behind the most capable computer-use agents are proprietary, and that open GUI datasets are narrow: they target grounding, mobile or web, or lack the diversity needed for general desktop use. Its first reported finding is a negative one for the obvious baseline: fine-tuning a vision-language-action model directly on 27K state-action trajectories gives only 4.4% success on OSWorld. The rest of the paper is about what it takes to move beyond that.

## What OpenCUA is

OpenCUA is a framework, not a single algorithm: an annotation tool, a dataset, a data-processing and reasoning-synthesis pipeline, a training recipe, and an offline benchmark.

**The agent.** It is a pure-vision desktop agent. The observation is a screenshot (three recent screenshots are used as visual history by default). The action space is a subset of PyAutoGUI actions, with coordinate actions such as click, doubleClick, dragTo and scroll, content actions such as write, press and hotkey, and a terminate action that reports success or failure. Platforms are Windows, macOS and Ubuntu. On the CUA Radar board the pattern is C21, trajectory-level policy training: supervised fine-tuning on whole trajectories.

**Data collection.** AgentNetTool runs on annotators’ own computers and records screen video, mouse and keyboard signals and the accessibility tree. Raw high-frequency signals are reduced by rules into meaningful actions, and each action is paired with a keyframe from just before it, chosen so that the mouse already hovering over a button does not leak the answer. The resulting AgentNet dataset has 22,625 tasks (12K Windows, 5K macOS, 5K Ubuntu) averaging 18.6 steps. Annotators were not required to give perfect demonstrations; identifiable errors are kept.

**The mechanism: reflective long chain-of-thought.** Each state-action pair is augmented with synthesised reasoning at three levels: L3 (observation, thought, action), L2 (thought, action) and L1 (action only). A reflector inspects each step by comparing screenshots before and after the action; steps judged incorrect or redundant are dropped from training, and correct steps get an explanation of what changed. A generator then writes the structured reasoning from the full context, with a red marker and a zoomed patch around the click point to help coordinate grounding, and a summarizer rewrites vague goals. Claude 3.7 Sonnet is used for all three roles. The training signal is purely supervised: the human action at each step plus this synthesised reasoning. Training mixes all three levels, adds grounding data and general text and vision SFT data, and uses L1 text history with three screenshots; at inference the L2 format is used.

Three training strategies are used: stage 2 only (Qwen2-VL and Kimi-VL-A3B bases), stage 1 plus stage 2 (OpenCUA-32B and 72B on Qwen2.5-VL) and joint training (OpenCUA-7B, 200B tokens on 128 A100 GPUs for eight days). The 72B model also uses 8k trajectories rolled out in an Ubuntu environment with o3 and Jedi.

## Results, as reported

Online results below are OSWorld-Verified success rate (%), scored by the OSWorld team on AWS, at 15, 50 and 100 step budgets (Table 3 of the paper; competitor rows are as printed there).

| Model           | 15 steps | 50 steps | 100 steps |
|-----------------|----------|----------|-----------|
| OpenAI CUA      | 26.0     | 31.3     | 31.4      |
| Claude 4 Sonnet | 31.2     | 43.9     | 41.5      |
| UI-TARS-72B-DPO | 24.0     | 25.8     | 27.1      |
| OpenCUA-7B      | 24.3     | 28.1     | 26.6      |
| OpenCUA-32B     | 29.7     | 34.1     | 34.8      |
| **OpenCUA-72B** | **39.0** | **44.9** | **45.0**  |

Claude Sonnet 4.5 is listed at 61.4 at 100 steps, and the paper states that proprietary models still lead. OpenCUA-72B is presented as the best open-source result. Decoding is at temperature 0; OSWorld-Verified figures are described as the average of 3 runs. Appendix Table 11 gives the per-run detail: at 100 steps the averages are 26.67 (7B), 34.88 (32B) and 44.99 (72B preview), and Pass@3 is 36.48, 45.10 and 53.02. For the 72B model the 15- and 50-step rows in Table 11 list a single run.

Offline results are a different measurement and are not comparable to the table above. On AgentNetBench (100 held-out Windows and macOS tasks from the authors’ own data, step-level matching), average step success is 75.2 for OpenCUA-7B and 79.1 for OpenCUA-32B, against 73.1 for OpenAI CUA and 67.0 for Qwen2.5-VL-72B. On grounding, OpenCUA-72B reaches 60.8 on ScreenSpot-Pro and 37.3 on UI-Vision.

## What the paper’s own controls say

**Reflective CoT.** On Qwen2-VL-7B with 14K Windows/macOS and 3K Ubuntu trajectories, replacing Aguvis-style short CoT with reflective long CoT raises OSWorld success from 11.5 to 15.3. The authors conjecture the gain comes from self-correction; this is not tested directly.

**CoT mixture and test-time format.** Training on L2 data alone gives 13.1, against 18.5 for the mixture of L1, L2 and L3. At inference, L2 gives 18.5, L3 17.6 and L1 16.9 (15-step budget). The paper notes this differs from earlier work where L1 beat L2.

**Data scale.** Adding 14K Windows/macOS trajectories to 7K Ubuntu ones lifts OSWorld from 9.8 to 18.5, which the authors read as positive cross-platform transfer. Scaling Ubuntu data from 3K to 10K improves average performance by 72%, and Windows/macOS data from 3K to 14K by 125%.

**Pass@n and variance.** For OpenCUA-Qwen2-7B with 16 samples at temperature 0.1, success at 15 steps rises from 16.9 (Pass@1) to 34.6 (Pass@16), and at 50 steps from 18.4 to 39.2. At temperature 0, minor differences such as the system date give Pass@16 of 38.60 against Pass@1 of 20.10; the authors describe the agent as not robust to small environment changes.

**Cost.** Annotation took about six months and about USD 20,000; synthesising CoT cost USD 0.6 per task, for about USD 32,000 in total.

## Where the evidence is thinner, in the paper’s words

- Held-out evaluation is only partial. The authors split data by operating system and state that there is “no overlap with OSWorld tasks to prevent data leakage”, but the paper does not say whether the 8k Ubuntu rollouts used for the 72B model avoid OSWorld environments or tasks. AgentNetBench is built from the same collection as the training data; the zero-shot baselines were not trained on it, and the authors note OpenCUA scores are higher partly “due to the alignment of the domain and action space”.
- The reflector and generator are LLM calls (Claude 3.7 Sonnet) that decide which steps are dropped; the paper does not report a validation of their judgments.
- The ablations are on small Qwen2-VL-7B runs, and the 72B model is not ablated. Table 6’s two comparisons come from separate runs.
- The paper’s own text and tables disagree in places: Section 4.2 gives Claude 4 Sonnet as 43.9 at 100 steps whereas Table 3 prints 41.5 there (43.9 is the 50-step entry), and the 72B Pass@3 is 53.2 in the text and 53.02 in Table 11. The 72B row in Table 11 is labelled “preview”.
- Limitations listed by the authors: dataset scale is bounded by human annotation, annotators may not use the most efficient methods, and informed consent introduces selection bias. The error study names task knowledge, precise grounding, action repetition, termination misjudgment, long horizons and error recovery.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **online**. The judgment record credits online evaluation by the OSWorld team, 3 runs, same-benchmark baselines across 15, 50 and 100 steps, reported training and annotation cost, and a component ablation. It marks the held-out environment as partial, the learned reflector as untested, and code as announced rather than verified. The radar did not rerun any experiment; every number here comes from the paper (version v3).
