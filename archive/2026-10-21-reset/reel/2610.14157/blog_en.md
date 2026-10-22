# OpenMobile-2: an open mobile-agent stack — commercial app replicas, 11.6K trajectories, and app-native tools

*A CUA Radar reading of arXiv 2610.14157v1 (Yan, Zhang, Cheng, Sun, Pan, Ma, et al.; Nanjing University, SenseTime, HKU, Xi’an Jiaotong University, NUS, ECNU). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.14157v1 · Code: https://github.com/OpenMobile2/OpenMobile2-Code*

## The problem

Mobile agents live on interaction experience, and that experience is mostly proprietary: the paper opens by noting that “high-quality interaction data remains largely proprietary, leaving the open community with limited training resources and open models trailing well behind.” The two existing ways to manufacture experience each hit a wall. Real apps on Android emulators are realistic, but “resist clean reset and is costly to parallelize,” which makes large-scale rollouts and reinforcement learning impractical. Simulated mock clients reset cheaply and parallelize well, but cover only a narrow, shallow slice of commercial life. On top of that, a new interaction channel is arriving — apps exposing structured interfaces next to their GUIs — and no mobile environment lets an agent train on both at once. The paper’s framing sentence: “reproducing rich workflows and persistent user states at scale has remained a key obstacle.”

## What OpenMobile-2 is

**The agent.** A vision-language mobile agent that sees only raw screen pixels — there is no accessibility tree, and business state is not readable. In supervised fine-tuning the last three screenshots stay as images (older ones collapse to text); in RL up to 32 screenshots stay in context at 448 px short side. Every turn is a `Thought:` paragraph plus exactly one tool call: either the always-available `mobile_use` GUI tool (click, long_press, swipe, type, answer, system_button, wait, terminate) with coordinates predicted in a normalized 999 × 999 space, or an **app-native tool** — over 300 scoped functions across 50+ apps (e.g. `taobao__search_items`, `clock__create_alarm`), appended to the action list only while that app is in the foreground and operating on the same persistent state as the GUI. Platforms: a browser-hosted simulator, Android emulators, and physical Android devices for evaluation.

**Board pattern.** CUA Radar places this paper at pattern C22, “executable benchmark with resettable environments and privileged final-state checkers” (parent: ground reward in executable checkers). Every task specifies a user goal, a bound initial state, and a programmatic checker over the before/after diff of application business state; the checker reads no screenshots and uses no model judge.

**The mechanism.** MobileGym++ extends the MobileGym simulation framework with 35 high-fidelity re-implementations of commercial apps (63 simulator clients in total, plus 62 newly configured emulator apps — a playground spanning over 110 apps). Each replica is built from the source app’s data schema and interaction graph, then checked by a coverage map and a replay of core flows. The median new app exposes 37 routes, 166 interactive actions, and 86 page transitions — 1.48× the actions and 1.91× the transitions of the 12 prior MobileGym business apps. Device state is fully serializable, so reset is deterministic and parallel instantiation is cheap; clipboard, app-to-app sharing, payment redirection, and media selection carry information across app boundaries. MobileGym++ Bench adds 215 long-horizon tasks (109 single-app, 74 two-app, 27 three-app, 5 four-app), each solvable with or without tools under the same checker.

**The training signal.** OpenMobile-Data-v2 contains 11.6K demonstration trajectories (including 1,774 that interleave GUI actions with tool calls) and more than 2K executable RL tasks (2,475 goals), each a triple of instruction, initial state, and verifier. Instructions and teacher trajectories come from Gemini-3.1-Pro-Preview; rollouts are kept only if the task completes and passes the runtime verifier — a programmatic check in the simulator, a vision-language judge on the emulator. Training runs two 5-epoch SFT branches (GUI-only and hybrid) from each base model (Qwen3.5-9B, Qwen3.6-27B), then DAPO-style RL (group size 8, 150 steps) from the hybrid checkpoint on 512 sampled tasks, with reward r = v · m_tool · ℓ − 0.2 n_fmt − 0.2 f_succ: a relaxed state verifier, a 2× tool bonus, a length factor, and penalties for malformed turns and claimed-but-failed completion.

## Results, as reported

All numbers below are **online** success rates — final device or application state, judged programmatically; the paper reports no offline step accuracy. ± is the standard deviation across evaluation seeds; ∗ marks baseline results reproduced by the OpenMobile-2 authors. SFT is 5 epochs; RL adds 150 steps on 512 tasks.

| Method | AndroidWorld Pass@1 | MobileWorld GUI | MobileGym++ GUI | MobileGym++ Hybrid | SPA-Bench L3 (real device) |
|----|----|----|----|----|----|
| UI-Venus-1.5-8B | 73.7 | – | 19.5\* | 16.3\* | 29.8\* |
| GUI-Owl-1.5-32B | 69.4 | 43.9 | 18.6\* | 23.3\* | – |
| Gemini-3.1-pro-preview | 70.7 | 58.1 | – | – | 70.2\* |
| Qwen3.5-9B (base) | 54.3 ± 3.7\* | 12.8\* | 9.3\* | 12.1\* | 25.5\* |
| OpenMobile-2-9B (+RL) | 74.0 ± 2.9 | 38.5 | 40.5 | 46.5 | 48.9 |
| Qwen3.6-27B (base) | 67.1 ± 4.1\* | 35.9\* | 46.5\* | 50.7\* | 31.9\* |
| OpenMobile-2-27B (+RL) | 79.9 ± 3.0 | 50.4 | 57.2 | 67.0 | 59.6 |

The paper reports gains of 19.7 points on AndroidWorld for the 9B model (54.3 to 74.0) and 12.8 points for the 27B model (67.1 to 79.9), and describes real-device transfer as “nearly doubling SPA-Bench performance from 31.9 to 59.6.” On MobileGym the 27B model goes from 37.1 (base) to 51.2 (+RL). Closed-weight references on MobileWorld GUI: GPT-5.6-Sol 70.1, Gemini-3.1-pro-preview 58.1; on SPA-Bench L3, GPT-5.6-Sol 68.1\* and Gemini 70.2\* remain above the open models.

## What the paper’s own controls say

- **Overlap audit.** Embedded with text-embedding-3-large, only 1.11%, 0.39%, 0.46%, and 2.25% of SFT instructions exceed 0.7 cosine similarity with AndroidWorld, MobileWorld, MobileGym, and MobileGym++ Bench respectively, and none exceeds 0.9; among the 2,475 RL goals, 6.1% exceed 0.7 with MobileGym++ Bench.
- **Coverage ablation.** With backbone, optimizer, and a fixed 2K-trajectory budget, raising application coverage from 15 to 53 apps lifts held-out AndroidWorld Pass@1 from 60.7 to 67.5 while in-distribution Pass@1 stays largely stable (73.7 to 71.4).
- **Tools need hybrid training.** Before hybrid SFT, tool calls appear in only 20–102 of 215 tasks and Qwen models improve by 2.8–4.2 points; after hybrid SFT, tools appear in 113 and 128 tasks (110 and 115 distinct tools), gains rise to 5.6 and 10.3 points, and trajectories become 4.8 and 5.8 steps shorter. On MobileWorld MCP — tools unseen in training — hybrid SFT scores 27.5 vs 12.5 (9B) and 45.0 vs 35.0 (27B) for GUI-only SFT.
- **Where RL helps.** RL raises MobileGym success from 35.9 to 38.3 (9B) and 48.4 to 51.2 (27B), and 27B SPA-Bench from 57.4 to 59.6. The paper states plainly: “Gains on other benchmarks remain limited, suggesting that RL benefits depend on the alignment between training environments and evaluation scenarios.”

## Where the evidence is thinner, in the paper’s words

- Emulator SFT trajectories pass “a vision-language judge”; the paper does not validate that judge’s accuracy, and the checker design (no model judge) applies only to the simulator side.
- Held-out evaluation is partial: the coverage study fixes 15 in-distribution applications on AndroidWorld (74 in-domain vs 42 held-out tasks), so part of the headline benchmark overlaps the training app pool.
- The RL stage is trained and validated on MobileGym++ tasks (512 of the 2K+ pool), and its measured gains sit mostly in that environment.
- Simulated apps trade “fidelity for cheap parallelism, clean reset, and direct state checks” — the paper’s own description of the mock-client family — so simulator scores measure commercial-style, not commercial, apps.

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **transfer**. The judgment record credits online evaluation across five suites, standard deviations over evaluation seeds, strong open and closed baselines, a coverage ablation, a train/eval overlap audit, and released code. It flags two anti-patterns (AP2, AP5), holds-out-apps status as partial, an untested VLM judge on the emulator data, and an unclear budget match for RL comparisons. The radar did not rerun anything; every number above comes from the paper (version v1).
