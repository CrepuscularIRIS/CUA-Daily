# OS-Helix: one policy that clicks and codes, trained on verifiable synthesized desktop tasks

*A CUA Radar reading of arXiv 2610.22234v1 (Yang, Jin, Ding, Wu, Li, Liu, Cheng, Xu, Sun, Sun, Qiao). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.22234v1 · Code: https://github.com/OS-Copilot/OS-Helix*

## The problem: a desktop task is rarely purely visual or purely programmatic

Most computer-using agents (CUAs) perceive screenshots and act with mouse and keyboard. The paper notes that grounding can fail on small or ambiguous elements and that structured state manipulation is cumbersome. Code agents have the opposite profile: they run compound operations through a shell but cannot handle tasks that depend on visual layout or interface-only state.

The obvious fix is to hand a GUI model a code tool, but the authors’ preliminary experiment suggests this is not enough: Qwen3-VL-32B-Instruct scores 34.17% on OSWorld-Verified with GUI actions alone and 32.68% when code execution is naively exposed (Table 14). Their conclusion is that GUI/code routing must be learned from hybrid training data.

## What OS-Helix is

**The agent.** The policy sees the current screenshot plus history (at evaluation, up to 8 earlier screenshots and the full textual history). It acts through one tool schema: GUI actions (click, drag, type, key, scroll, on a 1000x1000 relative grid), meta actions such as termination, and code actions that run Python or Bash in a fresh process, with stdout and stderr appended to the context. Platforms are Ubuntu (OSWorld) and Windows (WindowsAgentArena). On the CUA Radar board this is sub-pattern C11, mixing GUI actions with code in one action space, under the main pattern “Decouple Planning from Grounding and Redesign the Action Interface”.

**What is new** is the training pipeline, which has four stages.

1.  **Application–artifact composition.** 45 applications with fixed versions and launch configurations are paired with a library of authentic files (.docx, .pptx, .xlsx, .pdf, .png, .blend and others) through a compatibility graph; each episode samples an application and compatible artifacts to instantiate a reproducible Ubuntu VM state.
2.  **Decoupled task synthesis.** An Exploration Agent (Claude Sonnet 4.6) does a short non-destructive exploration (open, click, scroll, terminate only) and proposes an instruction with success conditions. Once accepted, the instruction is frozen and a separate Evaluator Agent compiles the check: rule-based over VM files and command-line state where possible, VLM-based for visual conditions, or both. Evaluators must compile and score zero on the initial state, a GPT-5.5 review agent grades quality, and near-duplicates are removed. The pipeline generated 8,880 tasks before filtering, most with rule-only evaluators.
3.  **SFT cold start.** Claude Sonnet 4.6 (Computer Use and Bash enabled) is the teacher. Evaluator scores drive rejection sampling and filtering, leaving about 31K successful desktop samples out of 83,701, mixed roughly 1:1 with 40K general multimodal samples.
4.  **Online RL with Step-balanced GSPO.** Rollouts run in live Ubuntu sandboxes, and the rule-based evaluator score is the sole outcome reward (an unparsable tool call gets 0). The authors observed that standard GSPO drifted toward code-heavy behavior, attributed to long code actions dominating the token-averaged sample-level importance ratio. Step-balanced GSPO averages token log-ratios within each action step and weights steps equally regardless of token count. RL starts from the dense 27B SFT checkpoint and runs 1,000 steps on rule-evaluator tasks only.

Base models are Qwen3.5-27B and Qwen3.5-35B-A3B; evaluation episodes are capped at 50 steps.

## Results as reported

All numbers below are mean success rate (%), online, on live virtual machines. OSWorld-Verified has 361 tasks after excluding the 8 Google Drive tasks. The paper does not state a number of seeds or runs for the main table; it does report Pass@1 and Pass@3 (see below). Rows marked “repro.” were reproduced by the authors with the same harness; other baselines come from the official leaderboard (OSWorld) or are cited results.

**OSWorld-Verified (Table 1), average success**

| Model                    | Setting | Avg.      |
|--------------------------|---------|-----------|
| Qwen3.5-27B (repro.)     | GUI     | 46.61     |
| Qwen3.5-27B (repro.)     | Hybrid  | 46.50     |
| **OS-Helix-27B**         | Hybrid  | **62.75** |
| **OS-Helix-27B-RL**      | Hybrid  | **66.44** |
| Qwen3.5-35B-A3B (repro.) | GUI     | 39.20     |
| Qwen3.5-35B-A3B (repro.) | Hybrid  | 42.84     |
| OS-Helix-35B-A3B         | Hybrid  | 57.27     |
| Agent S3 w/ GPT-5        | Hybrid  | 62.63     |
| OS-Symphony w/ GPT-5     | Hybrid  | 65.84     |
| Kimi K2.6                | GUI     | 73.07     |
| Qwen3.7-Plus             | GUI     | 73.33     |

The paper states that OS-Helix-27B and OS-Helix-35B-A3B improve over their matched Hybrid baselines by 16.25 and 14.43 absolute points (35.0% and 33.7% relative), and that OS-Helix-27B-RL “further improves by 42.9%” to 66.44%. The largest SFT gains are in Office (72.60 against 39.26 for the 27B Hybrid baseline) and Work., the multi-application category (54.28 against 38.29). RL then adds Professional (+23.10 points over SFT), OS (+7.61) and Daily (+6.69), while Office and Work. do not improve further. The paper calls the model competitive with GPT-5-based frameworks and notes that newer, substantially larger general models remain stronger overall.

**WindowsAgentArena (Table 2, 50-step budget, hybrid action space, Python-only code actions)**

| Model                       | Avg.  |
|-----------------------------|-------|
| Qwen3.5-27B GUI (repro.)    | 40.82 |
| Qwen3.5-27B Hybrid (repro.) | 56.41 |
| Agent S3 w/ GPT-5           | 54.10 |
| OS-Symphony w/ GPT-5        | 63.45 |
| OS-Helix-27B                | 57.95 |
| OS-Helix-27B-RL             | 63.87 |

The RL model is 23.05 points above the GUI baseline and 7.46 above the Hybrid baseline, with no Windows-specific training data.

**Offline measurement.** Grounding benchmarks are offline and kept separate: for the 32B SFT variant (Qwen3-VL-32B-Instruct base), OSWorld-G is 57.21 against 61.35 for the reproduced base, and ScreenSpot-V2 is 93.47 against 95.05 (Table 13). The authors call the decrease expected.

## What the paper’s own controls say

- **Same harness and budget.** All reproduced baselines use the same harness; all WindowsAgentArena entries use a 50-step budget and a hybrid action space.
- **Domain removal.** Removing the nine OSWorld-related application domains from the SFT data (about 31K down to about 17K samples) moves success from 62.75% to 62.31%.
- **Teacher.** On 800 synthesized tasks, Kimi K2.5 as teacher gives 54.03 and Claude Sonnet 4.6 gives 58.77, both above the unadapted Hybrid backbone.
- **Training stages (Table 4).** Hybrid backbone 46.50, RL only 48.20 (+1.70), SFT only 62.75, SFT then RL 66.44. SFT gives the main gain.
- **RL objective.** Under the same SFT initialization, data, sampling, reward and budget, standard GSPO gives 60.47 (-2.28 against SFT) and raises the code-action rate from 27.9% to 40.0%; Step-balanced GSPO gives 66.44 with a 26.1% code-action rate.
- **Code access.** The same OS-Helix-27B checkpoint scores 52.13 with code disabled and 62.75 with it enabled. At a fixed 10K-sample SFT budget, GUI-only trajectories give 57.56 and hybrid trajectories 60.61 (3.05 points higher).
- **Repeated sampling.** From SFT to RL, Pass@1 goes from 62.75% to 66.44% and Pass@3 from 70.88% to 76.44% (+5.56), with a paired-bootstrap 95% interval of \[2.24, 8.97\] over the 361 tasks. For Pass@1 the paper’s Table 16 interval is \[0.93, 8.33\].
- **Efficiency and behavior.** OS-Helix-27B uses fewer interactions under small step budgets (Figure 3). In a manual audit of 30 Work. trajectories, 27 contain a grounded GUI/code handoff; the paper cautions that the subset may not reflect the full benchmark.

## Where the evidence is thinner, in the paper’s words

- Automatic verification “remains imperfect”: evaluators “carry intrinsic brittleness”, and VLM-based scoring is excluded from RL rewards. The paper does not report a human check of evaluator accuracy.
- RL was run “only on the dense 27B model” with conservative settings; the 35B-A3B MoE model was not RL-trained.
- Infeasible tasks (roughly 10% of both benchmarks) are not generated by the pipeline; removing them raises average success “up to 3-5 absolute points”.
- On WindowsAgentArena the code action is restricted to Python by prompt revision. Many benchmarks were designed for GUI-only agents, so evaluators may not accept every valid GUI/code solution.
- The paper says it “will release” the models, environments and data; this summary did not check the repository.

## CUA Radar’s read

CUA Radar scores this paper **75 (★★★)**, evidence level **transfer**. The judgment record credits online evaluation, the domain-removal control, the Pass@3 bootstrap interval, reproduced baselines with a matched 50-step budget, efficiency reporting and component ablations; WindowsAgentArena supplies the transfer evidence. Evaluator or judge validation is not reported, and code availability is unclear from the paper. The record also flags AP5: synthesis data overlaps the evaluated applications, so gains cannot be fully separated from in-domain exposure beyond the domain-removal run above. CUA Radar did not rerun any experiment; every number here comes from the paper (version v1).
