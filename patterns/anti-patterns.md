# Anti-patterns — failure-prone moves in computer-use agent research

Sources: `antipatterns.json` of the frozen domains `cua-agents/v1` (93 qualitative candidates) and `cua-agents-core/v1` (101 candidates), both status `no_outcome_labels`. The candidates — the When-it-fails lines of the domain cards — are grouped below into recurring moves. AP1–AP13 come from `cua-agents` and keep their ids; `cua-agents-core` candidates were folded into them where the move is identical and otherwise form AP14–AP21. Board-induced sub-patterns R01–R03 (2026-10-19, from wave-1 weak fits; not from a frozen domain) add their When-it-fails lines to existing anti-patterns where the move is identical and form AP22 otherwise. These are reading-derived candidates, **not statistics**: no acceptance or outcome contrast backs them. Every candidate appears under exactly one anti-pattern, quoted verbatim with its card (K = cua-agents, C = cua-agents-core) and citations. Expectation ids `E..` are from `cua-agents`, `core-E..` from `cua-agents-core`.

**Scoring note.** AP7, AP8, AP9 and AP17 are recorded but not penalised by `score.py` (`AP_INFO_ONLY`): each is a pure duplicate of evidence items in `research/EVIDENCE_SCHEMA.md` that already price it (AP7 `online_eval`; AP8 `variance`/`online_eval`/`held_out_env`; AP9 `component_ablation`/`strong_baselines`; AP17 `cost_reported`).

## AP1 — Trusting multi-step or optimistic imagination

**Failure mode.** Using a learned simulator for long autoregressive rollouts, or taking its predictions at face value, when it hallucinates unavailable actions, invents content and caters to the agent's action; error compounds with horizon.

**Main patterns affected.** [Select Actions by Simulated or Verified Lookahead](main/simulated_lookahead_selection.md), [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Calibrate a Simulator or Digital Twin to the Real Target](main/calibrate_simulator_to_real.md)

**Reviewer expectations that catch it.** E31, E30

**Evidence (8 candidates).**
- [K01](sub/K01.md): Multi-step simulated rollouts hallucinate actions unavailable in predicted states and compound error; horizons 2-3 lose effectiveness (2411.06559#s1, 2410.13232#s2)
- [K03](sub/K03.md): Counterfactual imagination (42% of sampled errors: invented products), low competence with web functions, overly generic predictions (2410.13232#s1)
- [K03](sub/K03.md): Full-page transitions are much harder (~12% completely wrong) and errors compound in multi-step imagination (2601.22149#s1)
- [K03](sub/K03.md): Sycophancy: overly optimistic outcomes that cater to the agent's action; poor detailed content generation (2602.14721#s1)
- [K05](sub/K05.md): Long dreams degrade through compounding hallucination; only ~1/10 world-model rollouts pass quality checks (2601.22149#s2, 2608.05891#s3)
- [K08](sub/K08.md): Out-of-distribution regimes (1.75x pressure) break the residual; autoregressive error accumulates (2402.01086#s1)
- [K08](sub/K08.md): At short horizons not better than open-loop/SysID (2502.01143#s1)
- [K35](sub/K35.md): Deterministic predictions; scaling to complex real data open (2410.08822#s1)

## AP2 — Simulator or synthetic environment substituted for reality without a real anchor

**Failure mode.** Training or evaluating in a world model, twin or generated environment as if it were the target, without real data in the mixture or a measured gap; policies exploit inaccuracies and hidden/server state is missing.

**Main patterns affected.** [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Calibrate a Simulator or Digital Twin to the Real Target](main/calibrate_simulator_to_real.md), [Ground Reward in Executable Checkers](main/verifiable_execution_reward.md), [Synthesise Tasks from Exploration and History](main/exploration_driven_task_synthesis.md)

**Reviewer expectations that catch it.** E32, E34

**Evidence (16 candidates; 15 cua-agents · 1 cua-agents-core).**
- [K04](sub/K04.md): Cannot reproduce real assets or content dependent on hidden/server state; visual similarity drops OOD (2602.09856#s1)
- [K04](sub/K04.md): Transitions absent from the app memory are rejected; functional-logic scores below general code/image generators (2608.05891#s1)
- [K05](sub/K05.md): Purely imagined training underperforms SFT / lowers ATP below the base model (2601.22149#s2, 2608.05891#s3)
- [K05](sub/K05.md): Gains saturate (~20K rollouts); diversity bounded by world-model experience; consensus reward is weak (2608.05891#s3)
- [K08](sub/K08.md): Data-hungry: full 23-DoF delta model impractical, reduced to 4-DoF; MoCap dependence (2502.01143#s1)
- [K09](sub/K09.md): Calibration cannot fully remove the gap of a limited-complexity simulator; twins are site-specific (2507.07067#s1)
- [K09](sub/K09.md): Plain PPI with a single global bias underperforms real-only training where the twin is wrong (NLoS) (2507.07067#s3)
- [K09](sub/K09.md): Bayesian twin training hinges on prior/model choice and costs more compute (2507.07067#s2)
- [K10](sub/K10.md): Fidelity bounded by the underlying simulator; dynamic content, network, personalisation, long-tail data are omitted (2609.07712#s1, 2504.03597#s1)
- [K10](sub/K10.md): Policies trained without real demos exploit twin inaccuracies (2403.03949#s1)
- [K11](sub/K11.md): Step-function dependence on demo count: 0% when real policy fails in sim (2403.03949#s2)
- [K11](sub/K11.md): Sim-only demos can include behaviour that breaks synchronisation at deployment (2504.03597#s2)
- [K11](sub/K11.md): ~2 days wall-clock per task (2403.03949#s3)
- [K13](sub/K13.md): Generated sites have no real server logic; single-site, single-user scope (2601.04126#s1)
- [K33](sub/K33.md): Mocked values may not initialise realistic state; fuzzer may dismiss injected widgets (2601.21253#s2, 2601.21253#s3)
- [C22](sub/C22.md): Restricted to apps without login and with inspectable local storage; clones with sampled data; final-state reward only. (2405.14573#s1, 2307.13854#s1, 2409.08264#s1)

## AP3 — Fidelity or progress scored by an unvalidated or same-family VLM judge

**Failure mode.** Reporting world-model or simulator quality with LLM/VLM-judged or perceptual-similarity metrics, sometimes from the same family as the training reward, instead of executed checks or independent validation.

**Main patterns affected.** [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Make Online Evaluation Discriminating](main/online_evaluation_methodology.md)

**Reviewer expectations that catch it.** E33, E30

**Evidence (6 candidates).**
- [K03](sub/K03.md): No access to server-side state or pixels by construction; intrinsic metrics are LLM-judged, not executed (2601.22149#s1, 2602.14721#s1)
- [K04](sub/K04.md): Same VLM family used as RL reward and evaluation judge may inflate gains (2602.09856#s1)
- [K04](sub/K04.md): Diffusion slots slightly lower functional-logic score (81.70 -> 79.69) (2608.05891#s2)
- [K10](sub/K10.md): Behavioural fidelity measured only indirectly (placeholder residual up to 20.6%) (2609.07712#s1)
- [K31](sub/K31.md): Best reference-action progress 16.7; fine-grained element scores < 20 while SigLIP is 61-77 (2609.00048#s1)
- [K31](sub/K31.md): Single probing agent; same model family as judge; VLM filter unvalidated (2609.00048#s2, 2609.00048#s3)

## AP4 — Judges and checkers used without two-sided reliability validation

**Failure mode.** Using a checker, judge, reflector or PRM as reward, filter or evaluator without measuring its false positives and false negatives against humans or legal alternatives, or without testing whether the policy exploits it.

**Main patterns affected.** [Ground Reward in Executable Checkers](main/verifiable_execution_reward.md), [Reward with Learned Outcome and Process Judges](main/learned_outcome_and_process_judges.md), [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Retrieve Past Experience and Knowledge into Context](main/experience_memory_retrieval.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md), [Hijack Agents Through the Environment and Measure Attempt vs Completion](main/environmental_injection_attacks.md), [Reinforce Single-Step Actions with Rule-Checked Rewards](main/rule_reward_single_step_rl.md), [Let the Agent Decide When to Involve the User](main/agent_initiated_user_interaction.md)

**Reviewer expectations that catch it.** E10, E11, E12, E13, core-E09, core-E16

**Evidence (29 candidates; 17 cua-agents · 10 cua-agents-core · 2 board-induced).**
- [K12](sub/K12.md): Checkers are per-task manual work (~2 man-hours each) and do not exist for unannotated tasks (2404.07972#s1)
- [K12](sub/K12.md): Residual false positives/negatives unquantified; checkpoint weights LLM-chosen and unvalidated (2404.07972#s1, 2601.04126#s2)
- [K12](sub/K12.md): Screenshots alone cannot see some state (e.g. file size), so screenshot judges and scripts are complementary (2404.07972#s1)
- [K15](sub/K15.md): Judge precision for kept trajectories not measured; self-reinforcing loops may overfit easy/popular sites (2510.09038#s2)
- [K16](sub/K16.md): ~13-20% disagreement with humans; free-form tasks lower precision (2411.02337#s2, 2504.01382#s1, 2406.11896#s2)
- [K16](sub/K16.md): Visual reasoning dominates judge quality; GUI-specialised RMs no better than base VLMs; reasoning and visual errors dominate (2510.18596#s2)
- [K16](sub/K16.md): Systematic judge bias is not removed by more rollouts (2605.06732#s3)
- [K16](sub/K16.md): Judges see only partial state (last screenshots), so mid-trajectory or hidden-state errors are missed (2412.19723#s2, 2510.18596#s2)
- [K16](sub/K16.md): Policy exploitation of judge errors not analysed (2406.11896#s2, 2411.02337#s2)
- [K17](sub/K17.md): Recall/specificity drop sharply; abstention may bias kept samples; not validated in an RL loop (2510.18596#s1)
- [K18](sub/K18.md): Probing can alter state (sandboxing needed); outcome-only; mobile lacks shell tools (2602.00575#s1)
- [K19](sub/K19.md): OOD apps and reward hacking not analysed; single run (2509.23738#s1)
- [K19](sub/K19.md): Below oracle reward on offline single-step GRPO (2509.23738#s3)
- [K26](sub/K26.md): Assumes Back restores the previous screen; MLLM verifier/first-error labels not validated against humans (2506.08012#s1, 2506.08012#s2)
- [K27](sub/K27.md): Self-evaluator correctness unmeasured; held-out environment gains not isolated (2410.08164#s2)
- [K27](sub/K27.md): Reflector labels disagree with humans ~25% (2311.08649#s2)
- [K34](sub/K34.md): A recommendation from a survey, not measured (2610.05001#s2, 2610.05001#s3)
- [C04](sub/C04.md): Model confuses composite widgets and predicts plausible words instead of literal text; GPT-4-scored evaluations favour verbosity. (2404.05719#s2, 2404.05719#s3)
- [C18](sub/C18.md): Plausible-looking wrong pages and irreversible actions (sending messages) defeat screenshot-diff reflection; reflection accuracy as low as 78.8%. (2406.01014#s3, 2401.16158#s3, 2501.11733#s2)
- [C18](sub/C18.md): Executor self-checks hallucinate, and the supervising orchestrator also hallucinates unseen content. (2508.03923#s3)
- [C18](sub/C18.md): No ablation of critic/refiner; LLM completion judgement lacks ground truth. (2402.07456#s2)
- [C20](sub/C20.md): Premature plan changes, imprecise drags/double-clicks, and self-declared completion without checker. (2411.10323#s2, 2312.13771#s3)
- [C22](sub/C22.md): Checker false-positive/negative rates largely unreported; must_include and GPT-4 fuzzy match can accept partially wrong content. (2307.13854#s3, 2401.13649#s3, 2405.14573#s1, 2409.08264#s1)
- [C25](sub/C25.md): Self-preference bias across judge models; live drift. (2401.13919#s3)
- [C25](sub/C25.md): Judge counts partial progress as success and is fooled by injection phrasing. (2506.14866#s2)
- [C32](sub/C32.md): Edge weights are judged rather than executed; only shallow components tested. (2406.12814#s2, 2406.12814#s5)
- [C33](sub/C33.md): LLM judge reliability not quantified and judges may themselves be susceptible. (2504.18575#s3, 2505.21936#s2)
- [R01](sub/R01.md): Shaped rewards are hacked: hit rewards shrink boxes and IoU rewards inflate them; text-similarity and piecewise-dense rewards drive the policy to repeat the most common action or emit tokens after the action tag; GRPO's length normalisation favours long incorrect answers; the action-type reward does not always help grounding (2505.15810#board, 2505.22942#board, 2503.21620#board)
- [R02](sub/R02.md): Confidence labels come from a proprietary critic and depend on it: replacing GPT-4o with Qwen-VL-Max drops HSR 86.87 -> 57.63 and causes more interventions (2503.16465#board)

## AP5 — Synthesis, exploration or memory data overlapping the evaluation

**Failure mode.** Generating tasks, transitions or memory in the same environments used for evaluation, so gains cannot be separated from in-distribution exposure; cross-site/OOD transfer is weak where measured.

**Main patterns affected.** [Synthesise Tasks from Exploration and History](main/exploration_driven_task_synthesis.md), [Ground Reward in Executable Checkers](main/verifiable_execution_reward.md), [Retrieve Past Experience and Knowledge into Context](main/experience_memory_retrieval.md), [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Mine Human Screen Recordings into Action Knowledge](main/mine_human_screen_videos.md)

**Reviewer expectations that catch it.** E28, E35

**Evidence (10 candidates; 6 cua-agents · 3 cua-agents-core · 1 board-induced).**
- [K06](sub/K06.md): On OOD AndroidControl transitions the dynamics-pretrained 7B stays below a larger base model (2604.02345#s3)
- [K13](sub/K13.md): Overlap with test distribution not analysed (2510.17790#s2)
- [K14](sub/K14.md): Poor cross-site transfer; mixing live and WebArena data hurts 7 sites (2410.02907#s2)
- [K14](sub/K14.md): Synthesis environments overlap the evaluation environments (2412.19723#s1)
- [K14](sub/K14.md): Live-site exploration cannot log in or submit content (2410.02907#s1)
- [K27](sub/K27.md): OOD gains small (OSWorld 26.40 -> 26.73); retrieval drift under UI shifts (2510.09038#s1)
- [C19](sub/C19.md): Gain small or absent with Gemini-1.5-pro; shortcuts misused on misperceived preconditions; flawed shortcuts propagate errors; reflectors saw future queries. (2501.11733#s3)
- [C19](sub/C19.md): Transfer to unseen apps / changed element ids untested; same apps for exploration and test. (2312.13771#s2)
- [C19](sub/C19.md): No gain on GAIA L3; learning explores the same benchmark's dev set; 20-task evaluation. (2402.07456#s3)
- [R03](sub/R03.md): The demo matches the test task: 30 author-crafted tasks each come with their own video; when the video's actions differ from the task, SR and decision accuracy drop on normal and advanced instructions (2502.17110#board)

## AP6 — Inference-time selection claimed without cost or real-search baselines

**Failure mode.** Claiming gains from simulated lookahead or Best-of-N reranking without reporting candidates/compute, without a real-execution tree-search comparison where reset is possible, or with a near-chance verifier.

**Main patterns affected.** [Select Actions by Simulated or Verified Lookahead](main/simulated_lookahead_selection.md)

**Reviewer expectations that catch it.** E18

**Evidence (6 candidates).**
- [K01](sub/K01.md): Absolute success remains below real-execution tree search where reset is possible (16.6 vs 19.2 WebArena; 23.6 vs 26.2 VWA) (2410.13232#s2, 2411.06559#s1)
- [K01](sub/K01.md): On short MiniWob tasks gains are small (+0.2 to +3.2) and MCTS/hybrid add little; authors conclude world models are worth more for data synthesis than inference-time search (2602.14721#s3)
- [K01](sub/K01.md): Large result-list state spaces (Shopping) shrink gains; element IDs change on reload causing search/execution mismatch (2410.13232#s2)
- [K01](sub/K01.md): Offline SR gains from simulation are ~1.2-1.3 points; hallucinated safety cues could mislead an agent (2602.09856#s2)
- [K02](sub/K02.md): Gains plateau as N grows while compute grows linearly (2509.23738#s2)
- [K02](sub/K02.md): Near-chance verifier accuracy yields negligible or negative Best-of-N gain (theorem assumes symmetric accuracy) (2602.00575#s2)

## AP7 — Exact-match or saturated offline proxies standing in for online success

**Failure mode.** Measuring or training against exact-match expert actions or saturated offline grounding benchmarks, which reject valid alternatives and do not track online success.

**Main patterns affected.** [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads](main/high_resolution_target_localisation.md), [Make Online Evaluation Discriminating](main/online_evaluation_methodology.md), [Reinforce Single-Step Actions with Rule-Checked Rewards](main/rule_reward_single_step_rl.md), [Let the Agent Decide When to Involve the User](main/agent_initiated_user_interaction.md), [Mine Human Screen Recordings into Action Knowledge](main/mine_human_screen_videos.md)

**Reviewer expectations that catch it.** E15, E05, core-E06

**Scoring.** Recorded but not penalised by `score.py` (`AP_INFO_ONLY`): already priced by evidence items in `research/EVIDENCE_SCHEMA.md` (`online_eval`).

**Evidence (13 candidates; 2 cua-agents · 8 cua-agents-core · 3 board-induced).**
- [K21](sub/K21.md): Valid alternative actions are treated as mismatches; non-expert branches never see real next states (2509.11543#s1, 2509.11543#s3)
- [K23](sub/K23.md): ScreenSpot v1/v2 saturate; offline-online gap (2501.12326#s3)
- [C03](sub/C03.md): Whole-task SR stays <= 7.1% offline because step errors compound; >10-point seen/unseen website gap. (2306.06070#s2)
- [C05](sub/C05.md): Only click grounding evaluated; agent use requires a separate planner. (2506.03143#s1)
- [C12](sub/C12.md): Zero-shot navigation remains weak (ShowUI AITW 35.9; OS-Atlas-4B below GPT-4o on OmniAct); offline evaluation with lenient click tolerance. (2410.23218#s2, 2411.17465#s2)
- [C21](sub/C21.md): Plan-rationale contribution not ablated; offline metric under-counts alternative correct paths (42% of sampled mismatches). (2312.08914#s3)
- [C23](sub/C23.md): An uncached action fails the task, giving false negatives when several paths exist; no recovery measured. (2306.06070#s3, 2508.09123#s5)
- [C23](sub/C23.md): Fine-tuned models score higher from action-space alignment; correlation on few points. (2508.09123#s5)
- [C26](sub/C26.md): Single-step static screenshots measure no planning/execution; point-in-box ignores near misses; small English sets. (2401.10935#s4, 2504.07981#s1)
- [C37](sub/C37.md): Held-out evaluation is compression only. (2501.09747#s2)
- [R01](sub/R01.md): Training and evidence are single-step and offline: states are scored by exact match to one reference action (used "as an effective surrogate for real-world verification"), multi-step tasks are cut into independent single-step problems, and single-image non-interactive training shows no "aha moment" (2505.22942#board, 2504.10458#board, 2503.21620#board)
- [R02](sub/R02.md): Evaluation is offline or tiny: single-reference offline trajectories mis-score early ASKs (step success before the ASK step drops without the dual-stream fix) and Mind2Web SR recovers only to ~69-78%; the live study is 27 WebArena tasks with three authors as the humans and a possible ordering bias (2503.24180#board, 2501.16609#board)
- [R03](sub/R03.md): Evidence is offline: exact action matching on static test sets, or captioning metrics for action description on one application's tutorials, with no acting agent evaluated (2505.12632#board, 2503.20978#board)

## AP8 — Thin evaluation: single runs, subsets, in-house benchmarks

**Failure mode.** Resting claims on a single run, a small subset, an in-house benchmark or a single-app case study, with drifting live sites or differing step caps, and without length stratification.

**Main patterns affected.** [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Make Online Evaluation Discriminating](main/online_evaluation_methodology.md), [Retrieve Past Experience and Knowledge into Context](main/experience_memory_retrieval.md), [Synthesise Tasks from Exploration and History](main/exploration_driven_task_synthesis.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md), [Ground Reward in Executable Checkers](main/verifiable_execution_reward.md), [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Let the Agent Decide When to Involve the User](main/agent_initiated_user_interaction.md)

**Reviewer expectations that catch it.** E16, E17, E19, E20, E23, core-E07, core-E15

**Scoring.** Recorded but not penalised by `score.py` (`AP_INFO_ONLY`): already priced by evidence items in `research/EVIDENCE_SCHEMA.md` (`variance`, `online_eval`, `held_out_env`).

**Evidence (16 candidates; 8 cua-agents · 7 cua-agents-core · 1 board-induced).**
- [K06](sub/K06.md): Online evaluation is a single 149-task in-house benchmark without seeds (2604.02345#s2)
- [K15](sub/K15.md): Task generation randomness raises variance; feasibility rules hand-written per environment (2411.02337#s1)
- [K20](sub/K20.md): Short tasks only; few repeats; evaluated on subsets (WebArena-Lite) (2406.11896#s1, 2411.02337#s3)
- [K24](sub/K24.md): Small web-only sets; one model lineage (2604.14262#s1)
- [K28](sub/K28.md): Ablations on 65 tasks single run; execution errors in 79.59% of failures (2410.08164#s1)
- [K30](sub/K30.md): Success falls monotonically with length for every agent (GPT-5 43.6 -> 14.1%) (2609.07712#s3)
- [K30](sub/K30.md): Live sites drift; harnesses and step caps differ across agents (2504.01382#s2)
- [K32](sub/K32.md): Fulfilment rates from a single-app case study; agent errors dominate multi-step failures (2609.10031#s3)
- [C18](sub/C18.md): Small gains on easy suites (M3A-Simple matches the full agent on MobileMiniWoB++); mistyping not recovered. (2405.14573#s2)
- [C20](sub/C20.md): Small benchmarks with no baselines. (2401.16158#s2)
- [C21](sub/C21.md): L3 descriptions mislead; single runs with high online variance. (2508.09123#s3)
- [C22](sub/C22.md): Robustness trials limited to 5 tasks and one agent configuration. (2405.14573#s4)
- [C24](sub/C24.md): Small task sets (20-90), no inter-annotator agreement, live drift prevents reproduction. (2401.01614#s4, 2401.16158#s4, 2501.11733#s4, 2502.14282#s4, 2411.10323#s3)
- [C26](sub/C26.md): Rewriting items changes difficulty so versions are not comparable. (2410.23218#s4)
- [C27](sub/C27.md): Only discrete forced-choice variables, click tasks and 7B models. (2607.04334#s1, 2607.04334#s3)
- [R02](sub/R02.md): Scope is narrow: at most one interaction per episode, a single omitted step of information, and the agent is assumed never to need navigation help (2503.19537#board, 2503.24180#board)

## AP9 — Missing ablations or matched baselines for the claimed component

**Failure mode.** Attributing a gain to a component (auxiliary objective, filtering stage, reflection tuning, world-model synthesis) without isolating it or comparing to an equal-size real/instruction-first baseline.

**Main patterns affected.** [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Ground Reward in Executable Checkers](main/verifiable_execution_reward.md), [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads](main/high_resolution_target_localisation.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md), [Reinforce Single-Step Actions with Rule-Checked Rewards](main/rule_reward_single_step_rl.md)

**Reviewer expectations that catch it.** E26, E29, E32, core-E08, core-E12

**Scoring.** Recorded but not penalised by `score.py` (`AP_INFO_ONLY`): already priced by evidence items in `research/EVIDENCE_SCHEMA.md` (`component_ablation`, `strong_baselines`).

**Evidence (14 candidates; 7 cua-agents · 6 cua-agents-core · 1 board-induced).**
- [K05](sub/K05.md): No comparison against equal-size synthesis in the real environment (2602.14721#s2)
- [K05](sub/K05.md): The theoretical bound is loose by 1-2 orders of magnitude at the median (2605.06732#s1)
- [K06](sub/K06.md): Inverse-dynamics variants can fall below baseline (sparse output tokens, fast saturation — author interpretation) (2604.02345#s3)
- [K06](sub/K06.md): Downstream task-success effect of auxiliary reflection tasks not separately ablated (2506.08012#s3)
- [K07](sub/K07.md): No ablation of filtering stages or caption quality; scaling not monotone for every backbone (2604.02345#s1)
- [K13](sub/K13.md): Evaluator-first tasks are harder and fewer; RL gain ~2 points (2510.17790#s2)
- [K26](sub/K26.md): No ablation isolating reflection tuning in UI-TARS (2501.12326#s1)
- [C08](sub/C08.md): Architecture gain alone on Mind2Web is small (40.7 -> 41.4) compared with data gains; coordinates stay imprecise. (2312.08914#s1)
- [C11](sub/C11.md): SDK effect on OSWorld/AndroidWorld not separated; mixed-interface gain shown only as training curves. (2509.02544#s1, 2509.02544#s5)
- [C13](sub/C13.md): No metric attributed to UFO's filtering. (2402.07939#s3)
- [C15](sub/C15.md): Summary error propagation not measured; hierarchical memory unablated. (2406.01014#s1, 2509.02544#s2)
- [C17](sub/C17.md): No role-removal ablations for several systems, so gains cannot be assigned to the hierarchy alone; extra per-step cost. (2501.11733#s1, 2402.07939#s1, 2402.07456#s4)
- [C21](sub/C21.md): Self-correction is conjectured, not isolated; loops, termination misjudgement and one-character errors remain. (2508.09123#s2)
- [R01](sub/R01.md): The RL contribution is confounded with data and backbone: R1-style agents differ in backbone, data and protocol, gains are compared with SFT models trained on far larger different data (3K vs 13M-14M), and an OS-subset result (16.1 vs 16.8 for the same data) suggests post-training activates pretrained knowledge (2505.15810#board, 2504.10458#board, 2505.12370#board)

## AP10 — Unreported scaling ceilings and teacher-bounded synthesis

**Failure mode.** Presenting synthetic-data or recipe gains without the saturation point, model-size dependence, refusal behaviour or teacher/executor ceilings that bound them.

**Main patterns affected.** [Synthesise Tasks from Exploration and History](main/exploration_driven_task_synthesis.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Learn GUI Dynamics and Train in Them](main/learn_and_train_in_gui_world_model.md), [Reinforce Single-Step Actions with Rule-Checked Rewards](main/rule_reward_single_step_rl.md), [Mine Human Screen Recordings into Action Knowledge](main/mine_human_screen_videos.md)

**Reviewer expectations that catch it.** E22, E25, E27

**Evidence (13 candidates; 10 cua-agents · 1 cua-agents-core · 2 board-induced).**
- [K07](sub/K07.md): Dense text-heavy viewports (Reddit) do not benefit; gains taper with data scale (2411.06559#s2)
- [K14](sub/K14.md): Saturation with scale, bounded by executor capability (2412.19723#s1)
- [K15](sub/K15.md): Widgets without text and single views with sub-regions are poorly explored (2311.08649#s1)
- [K15](sub/K15.md): Residual duplicate intents and occasional intents for non-existent functionality (2609.10031#s1)
- [K21](sub/K21.md): Gains shrink with model size (2509.11543#s1)
- [K23](sub/K23.md): Diminishing returns after ~100K screenshots; long-tail icons (2410.05243#s1)
- [K23](sub/K23.md): Models rarely refuse; ambiguous instructions cause ~40% of errors (2505.13227#s1, 2412.04454#s1)
- [K25](sub/K25.md): Single-sample system-2 decoding is worse in-domain (irrelevant/hallucinated reasoning); better OOD and with Best-of-N (2501.12326#s2)
- [K25](sub/K25.md): Redundant actions in source trajectories yield wrong reasoning (7.8%) (2412.04454#s2)
- [K29](sub/K29.md): Tool gains modest at 7B (+1.9); small models rarely call tools; harmful tool calls before RL (2510.17790#s1)
- [C37](sub/C37.md): Small gains at low control frequency; less efficient than VQ at low fidelity. (2501.09747#s1)
- [R01](sub/R01.md): On high-level tasks the gain over the zero-shot base is small (GUI-R1-7B AndroidControl-High/GUI-Odyssey overall 56.13 vs 50.53); only 3B/7B are tested; the method depends on large, precisely annotated grounding data and costs ~300 H100 GPU hours (2504.10458#board, 2505.12370#board, 2506.09373#board)
- [R03](sub/R03.md): Action labels are inferred by a proprietary VLM and stay noisy (80.90% overall action accuracy); heavy filtering keeps 20K of 129K videos (no hand occlusion, phone OS only) (2505.12632#board)

## AP11 — Domain randomisation as a training fix for GUI brittleness

**Failure mode.** Borrowing robotics-style domain randomisation as training augmentation; in GUIs it works as an evaluation probe but did not fix grounding brittleness.

**Main patterns affected.** [Make Online Evaluation Discriminating](main/online_evaluation_methodology.md)

**Reviewer expectations that catch it.** E24

**Evidence (2 candidates).**
- [K24](sub/K24.md): Relational instructions collapse accuracy (UI-TARS-1.5 91.0 -> 35.0); window perturbations drop 50.79% -> ~15% (2604.14262#s1, 2404.07972#s2)
- [K24](sub/K24.md): Domain-randomised LoRA SFT does not fix the brittleness and more data degrades (2604.14262#s2)

## AP12 — Errors propagating through the planner–grounder or action interface

**Failure mode.** Assuming a modular split or coarse action interface isolates errors, when planner errors flow through the NL description, element IDs cannot target sub-element positions, and correction data covers only grounding errors.

**Main patterns affected.** [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md), [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md)

**Reviewer expectations that catch it.** E08, core-E13

**Evidence (15 candidates; 5 cua-agents · 10 cua-agents-core).**
- [K22](sub/K22.md): Planning errors (wrong/vague element descriptions) dominate failures; planner errors propagate through the NL interface (2410.05243#s2, 2505.13227#s2)
- [K22](sub/K22.md): End-to-end single model is weaker than with a strong external planner (2412.04454#s3)
- [K22](sub/K22.md): Idiosyncratic icons cause grounding errors on mobile/desktop (2410.05243#s2)
- [K26](sub/K26.md): Covers visual/grounding errors, not high-level planning errors; mobile-only (2506.08012#s1)
- [K29](sub/K29.md): Element-ID grounding cannot target sub-element positions (grounding errors in 53% of failures) (2410.08164#s3)
- [C01](sub/C01.md): Label-indexed action spaces exclude drag and continuous actions, and wrong-box typing raises no execution error. (2401.13919#s2, 2312.13771#s1)
- [C10](sub/C10.md): Residual failures are dominated by planning in spreadsheet and multi-app tasks (Calc, Workflow, Office remain low). (2410.23218#s3, 2504.00906#s3)
- [C10](sub/C10.md): Grounding errors persist; structural expert needs an app API; ablation on a 65-task subset. (2504.00906#s1)
- [C10](sub/C10.md): OCR misses when the planner hallucinates target text; similar icons with only a coarse position hint. (2401.16158#s1)
- [C11](sub/C11.md): Code-only cannot handle apps without scripting access; OS-Copilot has no screenshot-to-action GUI control. (2402.07456#s1, 2508.03923#s1)
- [C12](sub/C12.md): Pixel-only coordinate agents trail HTML-based methods on Mind2Web (SeeClick 25.5 vs MindAct 52.0) and unified multi-platform training slightly hurts. (2401.10935#s3)
- [C12](sub/C12.md): Event compression may lose fine-grained actions (letter-level drag-select). (2508.09123#s1)
- [C14](sub/C14.md): Steps per task roughly double; removed hover/press/tabs would be needed on other sites (untested). (2410.13825#s1)
- [C17](sub/C17.md): Planning failures from noisy subtask information are the most frequent failure; no infeasibility prediction. (2504.00906#s2)
- [C20](sub/C20.md): Visual-language misalignment between stated target and chosen id; weaker models hallucinate on long contexts. (2409.08264#s3)

## AP13 — Unregularised multi-phase online updates

**Failure mode.** Running successive online RL phases without a KL constraint or success replay (or replaying failures).

**Main patterns affected.** [Train the Policy on Own, Replayed and Corrected Trajectories](main/trajectory_level_policy_training.md)

**Reviewer expectations that catch it.** E09

**Evidence (1 candidates).**
- [K20](sub/K20.md): Without KL or replay, performance degrades over phases; replaying failures destabilises (2411.02337#s3)

## AP14 — Binding actions to a structural or parsed element list that is incomplete, ambiguous or wrong

**Failure mode.** Restricting the agent to ids from a DOM/a11y/UIA enumeration, a detector's proposals or a ranker's top-k, and assuming that list is complete, unambiguous and agrees with the pixels — when canvas content and unsupported controls are missing, duplicate or text-less elements cannot be told apart, marks are mislinked on dense pages, and stale or edited structure is followed over correct pixels.

**Main patterns affected.** [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md)

**Reviewer expectations that catch it.** core-E22, core-E13, core-E14, core-E10

**Evidence (11 candidates; cua-agents-core).**
- [C01](sub/C01.md): Elements missing from the structural view (canvas content, controls unsupported by UIA, e.g. Adobe Acrobat at 60% success) are not addressable. (2402.07939#s2, 2312.13771#s1, 2502.14282#s1)
- [C01](sub/C01.md): Dense text-heavy pages: marking DOM candidates on the screenshot hallucinates / mislinks labels (SeeAct step SR 20.3 vs 39.1 for textual choices); WebVoyager attributes 24.8% of failures to visual grounding errors (adjacent elements, calendar numbers mistaken for marks) and text-heavy sites show no gain. (2401.01614#s2, 2401.13919#s1)
- [C02](sub/C02.md): Accuracy is capped by proposal quality: missed regions are unrecoverable (GT masks raise mIoU 75.6 -> 90.1). (2310.11441#s1)
- [C02](sub/C02.md): Coarse OCR boxes and repeated identical icons/text make centre-click or id choice land on the wrong element; context-free icon captions misread page-dependent icons. (2408.00203#s1, 2408.00203#s2)
- [C02](sub/C02.md): Mark placement heuristics can attach marks to the wrong object; dense small UI elements not evaluated for the original SoM. (2310.11441#s2)
- [C03](sub/C03.md): Targets outside the ranked pool (11-15% at top-50) cap accuracy; no visual signal in the ranker. (2306.06070#s1, 2401.01614#s1)
- [C03](sub/C03.md): Identical or similar candidate HTML text cannot be told apart (picks first 'Schedule' button); gap to oracle grows with task length. (2401.01614#s1)
- [C03](sub/C03.md): Matching a generated element description to the DOM by visible text and type fails on text-less elements (step SR 16.1 vs 39.1). (2401.01614#s3)
- [C04](sub/C04.md): Supervision inherits the source's coverage: instructions limited to visible text/title attributes; elements absent from HTML/a11y trees (canvas, games) or missed by the detector are never labelled. (2401.10935#s2, 2410.23218#s1, 2404.05719#s2)
- [C27](sub/C27.md): Coordinate actions resist swap hijack but have higher baseline error and still click phantom elements; neither binding is safe. (2607.04334#s3)
- [C27](sub/C27.md): Early conflict is unrecoverable in multi-step click episodes without reflection. (2607.04334#s5)

## AP15 — Scaffold or perception gains assumed to transfer across backbones

**Failure mode.** Presenting a prompting scaffold, mark scheme, caption pipeline or multi-agent decomposition as generally helpful when its gain is shown only with a frontier backbone; weaker or different backbones gain nothing or degrade.

**Main patterns affected.** [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md)

**Reviewer expectations that catch it.** core-E11, core-E08, E22

**Evidence (4 candidates; cua-agents-core).**
- [C01](sub/C01.md): Only strong VLMs read marks: SoM did not help IDEFICS-80B, CogVLM or Gemini-Pro on VWA. (2401.13649#s1)
- [C02](sub/C02.md): Captions miss fine-grained content (OCR, logos); weak LLMs gain nothing from captions. (2401.13649#s2)
- [C11](sub/C11.md): Needs a strong reasoning orchestrator (o4-mini drops to 43.43%); at 15 steps the hybrid trails other agents; GUI-only beats hybrid on OS category. (2508.03923#s1)
- [C17](sub/C17.md): Weaker backbones degrade after decomposition (Qwen2.5-VL full framework below its single agent). (2502.14282#s2)

## AP16 — Aggregate grounding numbers hiding small-target, icon and high-resolution limits

**Failure mode.** Reporting a grounding/localisation gain as an aggregate while icons, sub-patch elements, desktop/professional high-resolution screens, far-off first predictions or other platforms remain weak or regress, or applying a training-time efficiency trick at test time without checking the loss.

**Main patterns affected.** [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads](main/high_resolution_target_localisation.md), [Reinforce Single-Step Actions with Rule-Checked Rewards](main/rule_reward_single_step_rl.md)

**Reviewer expectations that catch it.** core-E02, core-E12, core-E01, E05

**Evidence (7 candidates; 6 cua-agents-core · 1 board-induced).**
- [C04](sub/C04.md): Icons/widgets and desktop remain weakest (SeeClick desktop icon 30.0; OS-Atlas desktop icon 62.86); errors fall near the target, i.e. fine localization is the limit. (2401.10935#s1, 2410.23218#s1, 2411.17465#s4)
- [C05](sub/C05.md): Elements smaller than one patch are under-represented (CAD-like precision tasks); icon accuracy on ScreenSpot-Pro stays low (16.4). (2506.03143#s1, 2506.03143#s2)
- [C05](sub/C05.md): Frozen-backbone LiteTrain without verifier stays well below full fine-tuning (22.9 vs 40.7). (2506.03143#s4)
- [C07](sub/C07.md): Fails when the first prediction is far off (locked onto a background-window tab); crops too small lose context, too large exceed capacity. (2504.07981#s2)
- [C08](sub/C08.md): Anyres reduced Android advanced-task (80.5 -> 70.1) and taperception scores; token cost not reported; not tested on desktop/web. (2404.05719#s1)
- [C09](sub/C09.md): Applying selection at test time drops ScreenSpot to 64.9; text-rich screens have few redundant components; navigation not ablated. (2411.17465#s1)
- [R01](sub/R01.md): Icons stay weak on professional screens (ScreenSpot-Pro icon 16.8 vs text 49.5; 21.0 vs 63.5) (2505.15810#board, 2505.12370#board)

## AP17 — Added per-step model calls without cost or latency accounting

**Failure mode.** Adding parsers, verifiers, zoom passes, planner/grounder calls or slower decoders per step and reporting accuracy without the extra calls, run time, tokens or latency they cost.

**Main patterns affected.** [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads](main/high_resolution_target_localisation.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md)

**Reviewer expectations that catch it.** core-E21, E18

**Scoring.** Recorded but not penalised by `score.py`: a pure duplicate of the evidence item `cost_reported` in `research/EVIDENCE_SCHEMA.md`, which already prices it.

**Evidence (4 candidates; cua-agents-core).**
- [C02](sub/C02.md): Parser inference cost dominates run time (OmniParser runs 37.8-82.2 min vs 6.5-21.4 min) and imprecise SoM boxes cause wrong element selection. (2409.08264#s2, 2409.08264#s1)
- [C06](sub/C06.md): Small or negative effect on easier benchmarks (ScreenSpot Web-Icon 85.4 -> 80.6 for 2B) and adds sequential verifier calls per candidate. (2506.03143#s3)
- [C07](sub/C07.md): Icon accuracy stays low (22.4%); cost/latency of multiple planner and grounder calls not reported; relies on planner layout priors. (2504.07981#s3)
- [C37](sub/C37.md): Inference ~750 ms per chunk vs ~100 ms for diffusion. (2501.09747#s3)

## AP18 — Lossy or state-inconsistent context management

**Failure mode.** Compressing, pruning or replacing the observation and interaction history (summaries, focus content, full-page observations, refined a11y trees, pruned plans) as if lossless: summaries hide intermediate mistakes, outcomes are dropped so agents loop, pruned observations hurt some site categories, long horizons lose context, and plan pruning resets the agent's context but not the environment state.

**Main patterns affected.** [Expose the Screen as Indexed Elements and Pruned Structure](main/structured_screen_observation.md), [Decouple Planning from Grounding and Redesign the Action Interface](main/planner_grounder_interface.md), [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md), [Mine Human Screen Recordings into Action Knowledge](main/mine_human_screen_videos.md)

**Reviewer expectations that catch it.** core-E08, core-E10

**Evidence (9 candidates; 8 cua-agents-core · 1 board-induced).**
- [C03](sub/C03.md): Ported to Android, the scheme struggles with long-press/swipe and loops because it caches actions but not outcomes (AndroidWorld 15.5% vs 30.6% M3A). (2405.14573#s3)
- [C13](sub/C13.md): GitLab SR dropped 35.0 -> 26.7 after refinement; visual-only content is out of scope for text-only agents. (2410.13825#s3)
- [C14](sub/C14.md): Full-page observations double tokens and cannot reach scroll-triggered content (infinite scroll). (2410.13825#s2)
- [C15](sub/C15.md): Summaries returning only the final state hide intermediate mistakes from the orchestrator (mistyped cell scrolled out of view). (2508.03923#s2)
- [C15](sub/C15.md): Long-horizon tasks (>30-50 actions) still lose coherent context. (2508.09123#s4)
- [C16](sub/C16.md): Hurts tasks with dense single-page content or multi-page navigation (Shopping, Reddit SR drop). (2410.13825#s4)
- [C17](sub/C17.md): Plan pruning resets only the agent's context, not the web state; multisite SR stays low. (2410.13825#s5)
- [C20](sub/C20.md): Observation bias, ignoring prior inputs, repeated actions to step limit, and the 'unachievable' hint causing early stopping. (2307.13854#s4)
- [R03](sub/R03.md): Key-frame sampling can drop essential frames and larger windows add irrelevant ones, so performance declines beyond a window size; the decision agent skips steps in long multi-frame input without a reflection pass (2502.17110#board)

## AP19 — Injection threat model mis-scoped: exposure overstated or attack reach untested

**Failure mode.** Measuring an attack (or an evaluation's safety) under a threat model that does not match deployment: episodes started at the trigger page or decoupled from the benign task, tasks filtered to ones the agent solves, untrusted content removed by human gating, one pipeline or backend tested offline, white-box components assumed, and small static injection sets whose conditions for success are not stated.

**Main patterns affected.** [Make Online Evaluation Discriminating](main/online_evaluation_methodology.md), [Hijack Agents Through the Environment and Measure Attempt vs Completion](main/environmental_injection_attacks.md)

**Reviewer expectations that catch it.** core-E17, core-E20

**Evidence (12 candidates; cua-agents-core).**
- [C24](sub/C24.md): Human gating and manual pop-up closing mean untrusted content is not tested. (2401.01614#s4)
- [C28](sub/C28.md): Cannot affect screenshot-driven action generation (full-request ASR 0); distant positions fall to 0.01-0.18. (2409.11295#s1)
- [C28](sub/C28.md): Would not reach pure-screenshot agents; prompts do not transfer across backends (18%); only SeeAct offline tested. (2410.17401#s1, 2410.17401#s2)
- [C28](sub/C28.md): Retargeting tested only on pre-filtered successes with unchanged element/operation. (2410.17401#s3)
- [C29](sub/C29.md): Fails when the agent ends from history, the answer is already on the page, or more confident actionable elements exist; delayed attacks are weaker. (2411.02391#s1)
- [C29](sub/C29.md): Cookie attack fails when the plan queries restricted element types against static ads. (2601.09923#s3)
- [C30](sub/C30.md): Episodes start at the trigger page, overstating exposure; tasks filtered to ones the agent solves. (2406.12814#s1, 2505.21936#s1)
- [C30](sub/C30.md): Screenshot-only agents may not see URL fragments; Office documents and code comments rarely succeed. (2504.18575#s2, 2506.14866#s1)
- [C30](sub/C30.md): Weak open models are not hijacked by faint text; small, non-adaptive injection sets. (2409.11295#s2, 2504.18575#s1)
- [C31](sub/C31.md): Black-box transfer drops sharply when the image is small in the screenshot and text describes the item (10% ASR). (2406.12814#s4)
- [C31](sub/C31.md): Needs a white-box captioner in the pipeline for the strong attack. (2406.12814#s3)
- [C33](sub/C33.md): Decoupled starts overstate real-world ASR relative to end-to-end runs. (2505.21936#s2)

## AP20 — Defenses claimed without adaptive attacks, utility or a separate decision-maker

**Failure mode.** Claiming protection from generic defensive prompts, instruction hierarchy, detectors, self-judged confirmation gating or isolation architectures without attacking the defense itself, without reporting benign utility and token cost, or letting the same policy decide what is sensitive.

**Main patterns affected.** [Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads](main/high_resolution_target_localisation.md), [Defend Agents Against Untrusted Observations: Prompting, Gating and Isolation](main/injection_defense_isolation.md)

**Reviewer expectations that catch it.** core-E18, core-E19, core-E20

**Evidence (8 candidates; cua-agents-core).**
- [C06](sub/C06.md): On dense AndroidWorld screens repair is partial (hijack 0.89 -> 0.77) at 3.3-5.5 queries per action; coordinate-swap attacks out of scope. (2607.04334#s4)
- [C34](sub/C34.md): Generic defensive prompts give no gain (pop-ups, EIA, captioner attack); malware scanners flag nothing. (2411.02391#s3, 2409.11295#s3, 2406.12814#s6)
- [C34](sub/C34.md): Instruction hierarchy did not prevent hijacking (>50% of cases still influenced). (2504.18575#s4)
- [C34](sub/C34.md): Detectors catch 0-30% of high-risk injections; consistency checks are attackable by CLIP attacks and costly. (2505.21936#s3, 2406.12814#s6)
- [C35](sub/C35.md): Per-app rates as low as 50%; same policy decides; no adversarial content tested. (2402.07939#s4)
- [C36](sub/C36.md): Coarse tainting cuts task completion by up to 40%; data-dependent tasks remain largely unsolved; 2-3x tokens. (2505.23643#s1, 2505.23643#s2, 2505.23643#s3)
- [C36](sub/C36.md): Underspecified tasks with unknown start states explode branches; plans cannot adapt to observed failures. (2601.09923#s1)
- [C36](sub/C36.md): Boolean leakage accumulates; termination only via caps. (2601.09923#s2)

## AP21 — Added components that consume untrusted content unfiltered

**Failure mode.** Adding memory, captioners, evaluators or reflection components that read attacker-controllable screen content without filtering, which widens the attack surface — attacked inputs flowing through added components raise ASR above the base agent.

**Main patterns affected.** [Structure the Prompted Agent Loop: Context, Hierarchy and Post-Action Reflection](main/agent_loop_context_control.md), [Hijack Agents Through the Environment and Measure Attempt vs Completion](main/environmental_injection_attacks.md)

**Reviewer expectations that catch it.** core-E20, core-E08

**Evidence (2 candidates; cua-agents-core).**
- [C16](sub/C16.md): Requires the agent to foresee what will be needed; memory stores untrusted screen text without filtering; multi-app evaluation tiny (8 instructions). (2406.01014#s2)
- [C32](sub/C32.md): When added components consume attacked inputs, ASR rises above the base agent (36-38%). (2406.12814#s5)

## AP22 — Human or oracle assistance credited as agent capability

**Failure mode.** Reporting the success of an agent that asks, defers or hands over to a user when the help is answered by the ground-truth action, generated QA pairs or the authors themselves, and without counting how often the agent asked or how many asks were unnecessary — so the gain measures the oracle and the asking cost stays hidden.

**Main patterns affected.** [Let the Agent Decide When to Involve the User](main/agent_initiated_user_interaction.md)

**Reviewer expectations that catch it.** none in the frozen profiles yet (closest: E15, E10)

**Evidence (2 candidates; 2 board-induced).**
- [R02](sub/R02.md): The user is an oracle or a simulation: requested interventions are answered with the ground-truth action, follow-up answers are LLM-generated QA pairs, so success with help credits the oracle rather than the agent (2503.16465#board, 2503.24180#board)
- [R02](sub/R02.md): Prompted detection over-asks: precision 0.08-0.19 against recall up to 0.84, from rigid unnecessary confirmations and navigation questions; over-asking cost is not counted where success is the only metric (2503.19537#board)
