# UI-TARS-2: a native GUI agent trained with a data flywheel and stabilised multi-turn RL

*A CUA Radar reading of arXiv 2509.02544v2 (ByteDance Seed). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2509.02544v2 · Code: https://github.com/bytedance/ui-tars*

## The problem: four open obstacles to a general computer-use agent

The report names open problems in data scalability, multi-turn reinforcement learning, the limits of GUI-only operation and environment stability. Long-horizon GUI trajectories with reasoning are costly to collect; RL over many turns suffers from sparse rewards and credit assignment across long sequences; real workflows involve files and terminals as well as screens; and training at scale needs sandboxes that stay stable for millions of rollouts.

## What UI-TARS-2 is

UI-TARS-2 is one “native” model: a Mixture-of-Experts LLM with 23B active parameters (230B total) and a 532M vision encoder, initialised from Seed-thinking-1.6. It follows a ReAct loop of thought, action and observation. It sees screenshots and acts through GUI primitives (click, type, scroll) or, in an extended action space, through SDK functions: terminal commands and MCP tool calls. A working memory keeps the last N steps and an episodic memory keeps compressed summaries of earlier episodes. On the CUA Radar board the paper sits in pattern C11, planner and grounder interface.

The paper’s methodology has four parts:

1.  **All-in-one sandbox.** Cloud virtual machines for Windows, Ubuntu and Android (PyAutoGUI and ADB), a shared file system so a file downloaded in the browser can be processed in a shell, and a hardware-accelerated browser sandbox for HTML5 mini-games.
2.  **Data flywheel.** Each round the current model produces trajectories by rejection sampling or interactive annotation. A validation function V(s) in {0, 1} sends passing samples to the SFT set and failing ones to the continual pre-training set, and the model is retrained through continual pre-training, SFT and RL. Annotation includes think-aloud recordings and an on-policy interactive mode in which annotators accept or override the model’s proposed step.
3.  **Multi-turn RL (PPO).** Asynchronous server rollouts with stateful environments and a streaming rollout pool, plus reward shaping, decoupled and length-adaptive GAE, value pretraining and DAPO-style “clip higher”. Rewards come from three sources: scripted checks (games), an LLM judge against a reference answer (GUI-Browsing), and, for open-ended GUI-General tasks across 690 websites, UI-TARS-2 itself as a generative outcome reward model.
4.  **Merging.** Domain-specialised RL models (browsing, general web, games, SDK) are merged by parameter interpolation.

## Results, as reported

Online success rate (%). “-” means the paper’s Table 1 lists no value. For these benchmarks UI-TARS-2 is allowed to use either GUI operations or the GUI SDK.

| Model | OSWorld (369) | WindowsAgentArena (150+) | AndroidWorld (116) | Online-Mind2Web (300) |
|----|----|----|----|----|
| Claude-4-Sonnet | 43.9 | \- | \- | \- |
| OpenAI CUA-o3 | 42.9 | \- | 52.5 | 71.0 |
| UI-TARS-1.5 | 42.5 | 42.1 | 64.2 | 75.8 |
| **UI-TARS-2** | **47.5** | **50.6** | **73.3** | **88.2** |

The paper says UI-TARS-2 surpasses UI-TARS-1.5 on all reported benchmarks. Table 1 does not state the step budgets or the number of runs for these rows.

With the SDK extension the paper reports 45.3 on Terminal Bench, 68.7 on SWE-Bench Verified, 50.5 on BrowseComp-zh and 29.6 on BrowseComp-en. On a separate in-house suite of 15 browser games, the mean score normalised to human level is 59.77 for the RL model, against 44.27 for its SFT model, 24.73 for OpenAI CUA and 21.61 for Claude Computer Use. These game numbers come from the authors’ own suite and are not comparable to the GUI table above.

## What the paper’s own controls say

**RL versus SFT.** On Online-Mind2Web, RL raises accuracy from 83.7 (the SFT baseline of the final iteration) to 88.2. The paper highlights transfer beyond the training focus: OSWorld from 43.0 to 47.5 and AndroidWorld from 64.6 to 73.3. The training tasks (GUI-Browsing, GUI-General) are mostly browser-based.

**GUI-only versus SDK.** Restricted to GUI-only operation, BrowseComp-zh and BrowseComp-en score 32.1 and 7.0, against 50.5 and 29.6 with SDK access.

**Quantization.** With W4A8 quantization, OSWorld drops from 47.5 to 44.4 while decoding speeds up from 29.6 to 47 tokens per second and per-round latency falls from 4.0 to 2.5 seconds.

**Step budget.** A separate inference-time scaling analysis (Figure 11) shows the OSWorld score rising as the maximum allowed steps increase from 20 to 100, even though RL training shortened trajectories; the values appear only in the figure.

**PPO versus GRPO.** In preliminary evaluation the paper finds PPO consistently better than GRPO by a clear margin; it shows training-reward curves, not benchmark numbers.

**The reward model.** The in-house outcome reward model reaches F1 83.8 on 300 human-annotated traces; the paper notes a relatively high false-positive rate, argues that correct intermediate steps still earn appropriate rewards, and reports that manual inspection found no substantial reward hacking.

## Where the evidence is thinner

- No seeds, standard deviations or intervals are reported for the GUI benchmarks, and baseline step budgets are not stated in the text.
- The RL-versus-SFT comparison is within the authors’ own pipeline (the final-iteration SFT baseline). The paper describes OSWorld and AndroidWorld as not the primary training focus, but does not say whether their tasks overlap with training tasks.
- The paper states the OSWorld gain as “nearly 10.5%” (43.0 to 47.5, a relative figure) and the AndroidWorld gain as “over 8.7%” (64.6 to 73.3, an absolute difference); we quote the raw numbers.
- Part of the training signal for GUI-General tasks is the model’s own judge, whose false positives the paper acknowledges.
- Cost and compute for training are not reported.

## CUA Radar’s read

CUA Radar scores this paper **67 (★★)**, evidence level **transfer**. The record credits online evaluation on four GUI benchmarks, strong proprietary baselines, an RL-versus-SFT comparison, a GUI-versus-SDK comparison and a test of the learned reward model on 300 labelled traces. It flags the learned judge (anti-pattern AP4), marks held-out evaluation as partial, and records variance, matched budgets and cost as not stated or unclear, and code as unclear although the title page links the project repository. The radar did not rerun any experiment; every number here comes from the paper (version v2).
