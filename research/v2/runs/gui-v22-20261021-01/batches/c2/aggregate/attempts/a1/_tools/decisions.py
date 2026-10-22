"""Opus 5.5 (fable) adjudication decisions for c2/a1, written after reading each fixed full text first.

Seat evidence is namespaced sol:/son55:, own evidence agg: (quotes asserted against the on-disk fixed texts,
PDF supplements and the frozen MAI-UI reference). 2504.14603 is out of this aggregation (skipped_a2_pending).
"""
from common import agg_evidence as A

R = lambda status, rating, reason, ev, ce=(), scope=(): {  # noqa: E731
    "status": status, "rating": rating, "reason": reason, "evidence_ids": list(ev),
    "counterevidence_ids": list(ce), "search_scope": list(scope)}

NA = "none (pattern matches and expectation statuses carry no points)"
UPGRADED = ("On-disk file is the fixed (listing-preserving) re-render of the same arXiv version; the seats' a1 records are bound to the "
            "manifest pin (v1 render, which dropped ltx_listing content and is no longer on disk). Every seat quote was re-found in this "
            "file; it is used here as a superset of the pinned text.")
EXP = lambda applicable, status, reason: {"applicable": applicable, "status": status, "reason": reason}  # noqa: E731

# ----------------------------------------------------------------------------------------------- PC Agent-E
PA = {
    "pk": "2505.13909",
    "prelim": ("Read before seat scores. SFT of Qwen2.5-VL-72B on 312 human Windows trajectories (two annotators, one day) whose steps get "
               "Claude-3.7 reconstructed thoughts plus 9 unexecuted Claude-3.7 alternative single-step decisions per human state (27K samples; "
               "history always the human trunk). Main evaluation is the authors' WAA-V2: 141 feasible tasks, VM snapshot reset, some checkers "
               "fixed and a few tasks human-graded, all infeasible tasks removed; 30-step cap; single reported run whose percentages are not "
               "k/141 counts. 14.9 -> 36.0 vs human-only 17.2, unfiltered end-to-end Claude distillation 26.2, human+distillation 26.9 at "
               "equal trajectory count; Claude-3.7 32.6 is run in the authors' scaffold (no image history) while UI-TARS uses its native "
               "framework. OSWorld (Linux, unseen OS) 11.1 -> 14.9, feasible 4.4 -> 10.9 but infeasible 86.7 -> 63.3, i.e. the trained "
               "model regresses on exactly the category WAA-V2 removed. Explicit n-gram/semantic decontamination against the test tasks. "
               "Applicable cards/expectations: gui C21 (reasoning synthesis + SFT), C22 (resettable executable benchmark); E01, E13, E16, "
               "E19, E22, E23, E25, E27."),
    "materials": [("2505.13909", "paper", None)],
    "evidence": [
        A("PA-A01", "2505.13909", "Sec 4 (Preventing infeasible hacking)", "we removed all infeasible tasks to prevent infeasible hacking",
          "Main benchmark is feasible-only by authors' design."),
        A("PA-A02", "2505.13909", "Table 4 (OSWorld)", "PC Agent-E (Ours) | 10.9 | 63.3 | 14.9",
          "Trained model drops from 86.7 (base) to 63.3 on infeasible OSWorld tasks: the category removed from WAA-V2 is one where the method regresses; the 141% headline is scoped to feasible tasks."),
        A("PA-A03", "2505.13909", "Sec 5.1 Method Baseline", "We sample 10 end-to-end trajectories from Claude 3.7 Sonnet for each of the 312 tasks.",
          "Direct-distillation baseline is sampled without any stated success filter, so 'error accumulation' is not separated from training on failed rollouts."),
        A("PA-A04", "2505.13909", "Sec 5.1 Settings", "All other models, including Claude and Qwen, were evaluated using our simple PC Agent-E scaffold.",
          "Teacher is evaluated in the student's scaffold (no image history), while UI-TARS gets its native framework; 'beats the teacher' is scaffold-bound."),
        A("PA-A05", "2505.13909", "Sec 4 (Fixing evaluation flaws)", "relied on human evaluators for a few complex tasks to improve assessment reliability",
          "Part of WAA-V2 success is human-graded; the number and rule are not given."),
        A("PA-A06", "2505.13909", "Table 3", "PC Agent-E (Ours) | 4.8 | 64.1 | 46.2 | 50.0 | 57.9 | 35.7 | 33.3 | 36.0",
          "With 17 Chrome / 141 total tasks, 64.1 and 36.0 are not k/n counts; the averaging or grading behind them is unexplained."),
        A("PA-A07", "2505.13909", "Sec 3.2", "we retained only trajectories whose task descriptions have an overlap of 0 under 13-gram and less than 0.7 under 3-gram, and a cosine semantic similarity under 0.85 with respect to any test task",
          "Explicit task-text decontamination against WAA-V2."),
    ],
    "assessment": {
        "evidence_level": "transfer",
        "evidence_level_note": "OSWorld (Linux) was not used to build the system and is checked by executable evaluators, so EVIDENCE rule 1 gives transfer; the transfer gain is small (feasible 4.4 -> 10.9) and apps overlap with the Windows training data.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single run: on the authors' feasible-only WAA-V2 (141 tasks, 30 steps), SFT of Qwen2.5-VL-72B on 312 human trajectories plus 9 unexecuted Claude-3.7 single-step alternatives per human state raises success from 14.9 to 36.0, above human-only SFT (17.2) and unfiltered end-to-end Claude distillation (26.2) at equal trajectory count; on unseen-OS OSWorld feasible tasks 4.4 -> 10.9, with a drop on infeasible tasks (86.7 -> 63.3).",
        "not_supported": ["Superiority over a success-filtered distillation baseline", "Beating the teacher outside the authors' screenshot-only scaffold or beyond noise (36.0 vs 32.6, ~5 tasks)", "Gains on infeasible-task behaviour", "Correctness of the synthetic alternative actions"],
        "unresolved": ["Non-integer success rates", "Number of human-graded tasks", "Teacher token/API cost"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "Closest operational alternative (teacher end-to-end distillation on the same 312 tasks) is compared at equal trajectory count; AgentTrek/UI-TARS data pipelines (fixed references) are positioned but not run. Residual (human-anchored single-step teacher branching without executing teacher rollouts) is concrete and quantified (3 h vs 900 h).",
        "evidence_ids": ["agg:PA-A03", "son55:E027", "son55:E048", "son55:E050"],
    },
    "rs": ("sol", "self_supervised_signal_engineering with sub null: rs:C08's load-bearing step is a quality gate before candidates enter training; Trajectory Boost has none (both seats agree on the missing filter). Supporting controlled_diagnostic_design/rs:C02 (partial) for the infeasible-hacking benchmark repair, as in both seats."),
    "domain": [("son55", "trajectory_level_policy_training", "C21", None), ("son55", "verifiable_execution_reward", "C22", "weak")],
    "pmap_patch": {0: {"main": "trajectory_level_policy_training", "sub": "C21"}, 1: {"main": "verifiable_execution_reward", "sub": "C22"}},
    "domain_note": "Thought Completion = gui:C21 (strong MLLM writes reasoning for demonstrations, then SFT a screenshot policy; more specific than sibling K25); Trajectory Boost's sampled alternatives are recorded as unassigned. WAA-V2 (snapshot reset + privileged checkers + fixes) = gui:C22, weak.",
    "expectations": {"E01": "son55", "E13": "son55", "E20": "son55", "E22": "son55", "E23": "sol", "E25": "son55", "E26": "sol", "E27": "son55"},
    "ratings": {
        "G": R("resolved", 3, "Desktop-trajectory scarcity and the cost of teacher rollouts are concrete and quantified (two annotators/one day; 900 h vs 3 h); the residual is distinguished from the nearest operational alternative (end-to-end teacher distillation) by experiment, and lineage (AgentTrek, OS-Genesis, UI-TARS thought augmentation) is stated. Not 4: data pipelines like AgentTrek/UI-TARS are only positioned, not bounded.",
               ["son55:E045", "son55:E027", "son55:E046", "sol:E08", "agg:PA-A03"]),
        "M": R("resolved", 3, "Human-state anchoring + single-step teacher branching is reconstructable and yields a distinguishing prediction vs end-to-end distillation that is tested; the assumption that unexecuted teacher alternatives are valid is unchecked.",
               ["son55:E003", "son55:E005", "son55:E047", "sol:E03"], ["son55:E025"]),
        "X": R("resolved", 3, "Prompts, action space, sample construction (trunk-only history), training hyper-parameters and scaffold are given; missing a quality gate for alternatives and termination supervision (50-step decline).",
               ["son55:E006", "son55:E007", "son55:E038", "son55:E036"]),
        "E.measurement": R("resolved", 2, "Executable WAA checkers with VM snapshot reset and OSWorld are credible, but the headline benchmark is author-modified (checker fixes without error rates, infeasible tasks dropped, an unstated number of human-graded tasks) and its success rates are not k/141 counts.",
                           ["son55:E014", "son55:E016", "agg:PA-A01", "agg:PA-A05", "agg:PA-A06"], ["son55:E021"]),
        "E.causality": R("resolved", 2, "Same-backbone human-only, end-to-end distillation and human+distillation controls at equal trajectory count plus a scaling curve support a recipe effect, but the distillation baseline is unfiltered (so 'error accumulation' is not separated from training on failed rollouts), Thought Completion and anchoring are not ablated, and the teacher comparison is scaffold-bound.",
                         ["son55:E022", "son55:E023", "son55:E024", "son55:E026"], ["agg:PA-A03", "agg:PA-A04"]),
        "E.holdout": R("resolved", 3, "Explicit n-gram/semantic decontamination of training tasks against every test task and an executable test on an unseen OS (OSWorld) with a small but positive feasible-task gain; same apps by design and OSWorld itself not decontaminated keep it below 4. The feasible-only WAA-V2 scope is disclosed in the benchmark definition.",
                       ["agg:PA-A07", "son55:E009", "son55:E033", "sol:E09"], ["agg:PA-A02"]),
        "E.statistics": R("resolved", 1, "Task denominators and a 50-step negative result are given, but there is a single run, no spread, and the teacher margin is ~5 tasks.",
                          ["son55:E042", "son55:E020", "sol:E11"]),
        "E.cost": R("resolved", 3, "Annotation effort, training compute (32 GPUs, ~5 h), synthesis wall-clock (3 h vs 900 h), equal 30-step caps and step-limit sensitivity are reported; teacher token/API cost and UI-TARS's native-framework advantage are not accounted.",
                    ["son55:E027", "son55:E038", "son55:E039", "son55:E036"], ["son55:E043", "son55:E040"]),
    },
    "resolutions": {
        "rs.matches": ("sol", "self_supervised_signal_engineering/null + controlled_diagnostic_design/rs:C02", "C08 requires a single quality gate before training; none exists here (son55's own tactic check marks the filter step 'missing'). Assigning C08 would rest on generator vocabulary only.", ["son55:E004", "son55:E025"], NA),
        "domain.matches": ("son55", "gui:C21 + gui:C22 (weak)", "C21 matches Thought Completion more specifically than K25 (strong MLLM + SFT of a screenshot policy); the benchmark repair is the resettable executable-checker benchmark card C22 rather than an unspecific online_evaluation_methodology/null.", ["son55:E008", "son55:E014"], NA),
        "rating.G": ("sol", {"status": "resolved", "rating": 3}, "The residual is bounded against the nearest operational alternative by an actual matched experiment and its stakes are quantified; son55's deduction (no equal-budget AgentTrek/UI-TARS comparison) is real but keeps G at 3 rather than the anchor-2 'incomplete nearest-neighbour comparison'.", ["agg:PA-A03", "son55:E027", "son55:E046"], "+3.75 vs son55"),
        "rating.E.measurement": ("son55", {"status": "resolved", "rating": 2}, "Re-read Sec 4 and Table 3: the headline benchmark is author-modified with undisclosed human grading and non-integer rates; sol's 3 credited the checkers without these.", ["agg:PA-A01", "agg:PA-A05", "agg:PA-A06"], "-2.5 vs sol"),
        "rating.E.causality": ("son55", {"status": "resolved", "rating": 2}, "The unfiltered distillation baseline is the key missing control for the stated mechanism (error accumulation), and the teacher comparison runs the teacher in the student's scaffold.", ["agg:PA-A03", "agg:PA-A04"], "-2.5 vs sol"),
        "rating.E.holdout": ("sol", {"status": "resolved", "rating": 3}, "Explicit, thresholded decontamination against all test tasks plus an executable unseen-OS test is more than anchor 2; son55's points (same apps, OSWorld not decontaminated, author-built benchmark) cap it at 3. The infeasible regression (agg:PA-A02) is a scope boundary already visible in the paper's own tables.", ["agg:PA-A07", "son55:E033"], "+2.5 vs son55"),
        "expectation.E01": ("son55", "partial", "OSWorld is reported only as a base-vs-ours transfer check at a non-standard 30-step budget; the desktop headline is on WAA-V2.", ["son55:E032"], NA),
        "expectation.E13": ("son55", "unmet", "Checker fixes are anecdotal; no two-sided measurement is reported, which is what E13 asks.", ["son55:E016"], NA),
        "expectation.E20": ("son55", "not_applicable", "Claims are desktop-VM claims; no live-web result is claimed.", [], NA),
        "expectation.E22": ("son55", "met", "Results are reported for 7B and 72B, with the small 7B gain disclosed.", ["son55:E030", "son55:E031"], NA),
        "expectation.E23": ("sol", "partial", "WAA-V2 is released as a benchmark contribution, so E23 applies; failure audit is qualitative and success is not stratified by reference length.", ["sol:E11"], NA),
        "expectation.E25": ("son55", "partial", "Infeasible behaviour is reported only on OSWorld (63.3 vs 86.7) and removed from WAA-V2; the 'infeasible hacking' argument is one two-model contrast, not a challenge that replaces the expectation.", ["agg:PA-A01", "agg:PA-A02"], NA),
        "expectation.E26": ("sol", "not_applicable", "Trajectory Boost is human-anchored teacher augmentation, not exploration-first/reverse/world-model synthesis; the distillation comparison is credited under E.causality.", [], NA),
        "expectation.E27": ("son55", "partial", "Scaling factor is varied (Fig 7) but numeric points and saturation are not given in the text.", ["son55:E022"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items M=3, X=3, E.statistics=1, E.cost=3, claim_type component_training, evidence_level transfer, claim_support scoped were re-checked against the text: all stand. Added scope boundary: the trained model regresses on infeasible tasks (OSWorld), the category WAA-V2 removes.",
    "claims_append": {"C1": (["agg:PA-A01", "agg:PA-A02", "agg:PA-A06"], "Headline is on a feasible-only benchmark; the trained model regresses on infeasible OSWorld tasks (86.7 -> 63.3); table rates are not k/141 counts."),
                      "C2": (["agg:PA-A04"], "Teacher run in the student's scaffold without image history."),
                      "C3": (["agg:PA-A03"], "Distillation baseline has no stated success filter.")},
    "status": ("accepted_final", "All 14 mechanical conflicts resolved from the fixed text; no scoring unknowns."),
    "expected_score": 67.5,
}

# ----------------------------------------------------------------------------------------------- DPO LLM-judge
DP = {
    "pk": "2506.03095",
    "prelim": ("Read before seat scores. UI-TARS-2B samples 10 single-step responses per AGUVIS instance; GPT-4o scores all 10 (0-100) with the "
               "ground-truth answer in the prompt; pairs are gold vs <80 samples (DPO-1), higher vs lower sample (DPO-2) or both (DPO-3); DPO "
               "hyper-parameters and pair counts are not reported, the judge prompt is only a figure. OSWorld (369 tasks), 3-run averages: "
               "15-step 6.91 -> 9.18/8.46/9.33, 50-step 8.83 -> 9.01/8.88/8.24 with admitted hardware failures; no spread, no SFT-on-gold or "
               "rule-matching control, judge never validated, privacy/local-efficiency never measured. Applicable cards/expectations: "
               "rs C26; gui judges, R01-like single-step offline update; E09, E10, E12, E16, E17, E27."),
    "materials": [("2506.03095", "paper", None)],
    "evidence": [
        A("DP-A01", "2506.03095", "Sec 3 Response Scoring", "For each task in the AGUVIS dataset, we present GPT-4o with 10 sampled responses from UI-TARS-2B alongside the ground truth answer, all within a single prompt.",
          "The judge sees the gold answer, so it grades closeness to an existing label rather than replacing annotation."),
        A("DP-A02", "2506.03095", "Sec 3 Pairing", "The first strategy pairs each model-generated response with a score below 80 against the corresponding ground-truth answer.",
          "DPO-1 uses the gold label as the preferred sample."),
        A("DP-A03", "2506.03095", "Sec 4.2", "we run the evaluation three times and average the performance.", "Three-run means; no spread reported."),
        A("DP-A04", "2506.03095", "Table 1 (15 steps)", "Weighted Avg. | 9.18 | 8.46 | 9.33 | 6.91 | 3.14", "15-step gain about 2.4 points of 369 tasks."),
        A("DP-A05", "2506.03095", "Table 2 (50 steps)", "Weighted Avg | 9.01 | 8.88 | 8.24 | 8.83 | 1.52", "No gain at 50 steps; DPO-3 below baseline."),
        A("DP-A06", "2506.03095", "Sec 4.4", "our system did experience hardware failures during inference in some 50-step runs", "50-step arm contaminated and not rerun."),
        A("DP-A07", "2506.03095", "Sec 1", "This local-first design eliminates the need for network communication during inference, providing strong privacy guarantees",
          "Privacy/local claim is asserted; no on-device measurement exists in the text."),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "OSWorld execution checkers; AGUVIS composition is outside the fixed package, so non-use of OSWorld apps cannot be verified and the DPO variant is reported on the same benchmark -> online, not transfer.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported 3-run means: offline DPO of UI-TARS-2B on GPT-4o-scored (gold-referenced) AGUVIS single-step pairs raises OSWorld success from 6.91 to 8.46-9.33 at 15 steps; no gain at 50 steps (8.83 vs 8.24-9.01, partly affected by hardware failures). The judge's contribution beyond the gold labels, and the privacy/local-efficiency claims, are not supported.",
        "not_supported": ["LLM-judge necessity vs gold-label matching/SFT", "Privacy-preserving / resource-efficient deployment", "Benefit at 50 steps", "DPO-3 as most robust"],
        "unresolved": ["DPO hyper-parameters and pair counts", "Judge prompt text (figure only)", "AGUVIS/OSWorld overlap"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "UI-TARS (fixed reference) already trains DPO on corrected-vs-erroneous action pairs; the residual is a label-source swap (annotator -> GPT-4o with the gold answer visible). AGUVIS itself is not in the fixed package, so lineage statements about it stay author-attributed. The controller's 'RCI lineage gap' cue does not occur in this paper or either seat record (RCI = 2303.17491 belongs to the re1 reference request); no RCI judgement is made here.",
        "evidence_ids": ["agg:DP-A01", "son55:E031", "sol:R01"],
    },
    "rs": ("son55", "self_supervised_signal_engineering/C26 in both seats (sol writes rs:C26): same card. Fit partial: the card's own failure mode (label-source swap without attribution control) applies."),
    "domain": [("sol", "learned_outcome_and_process_judges", None, None), ("son55", "rule_reward_single_step_rl", "R01", "partial")],
    "pmap_patch": {1: {"main": "learned_outcome_and_process_judges", "sub": None}},
    "domain_note": "Judge role recorded under learned_outcome_and_process_judges with sub null (C25 scores trajectories; here single-step responses are scored against a gold answer). Operational shape = R01 (static single-step instances, k base samples, label-referenced scoring, offline update) with an LLM scorer and DPO instead of rules and GRPO. trajectory_level_policy_training/K26 not kept: no first-error localisation or trajectory-level data.",
    "expectations": {"E09": "son55", "E12": "son55", "E21": "son55", "E22": "sol", "E27": "son55", "E28": "sol"},
    "ratings": {
        "G": R("resolved", 1, "The stated 'no human annotation' gap is undercut by the method itself (the judge is given the AGUVIS gold answer and DPO-1 prefers that gold label), the privacy/local gap is generic to any small model and not diagnosed, and the residual over UI-TARS's DPO (label source) is not isolated.",
               ["agg:DP-A01", "agg:DP-A02", "agg:DP-A07", "son55:E031"], ["sol:E01"]),
        "M": R("resolved", 2, "Concrete pairing rules and DPO; the judge's marginal role over gold matching is unargued and score distributions collapse near 0.", ["son55:E009", "son55:E010", "son55:E011", "sol:E03"]),
        "X": R("resolved", 2, "Sampling parameters, threshold and pairing rules are given; DPO hyper-parameters, data size and observation setting are missing and the judge prompt is only an image.", ["son55:E006", "son55:E008", "son55:E022"], ["son55:E027"]),
        "E.measurement": R("resolved", 2, "Execution-checked OSWorld outcomes averaged over three runs, but small absolute values, a 50-step arm with hardware failures and an unvalidated training judge.", ["son55:E012", "agg:DP-A03", "agg:DP-A06"], ["son55:E026"]),
        "E.causality": R("resolved", 1, "Only DPO variants vs base; no SFT-on-gold, rule/exact-match reward or judge-free control, so the gain cannot be attributed to the judge or the preference structure.", ["son55:E028", "agg:DP-A02"], ["son55:E026"]),
        "E.holdout": R("resolved", 2, "Training instances (AGUVIS, static) are distinct from the online OSWorld evaluation, a real separation; no overlap analysis, a single benchmark, and all variants reported on that benchmark.", ["son55:E004", "son55:E033", "son55:E012"], ["son55:E020"]),
        "E.statistics": R("resolved", 2, "Three-run means over 369 tasks for every model (partly meets E16) but no spread; the 2.4-point 15-step margin is ~9 tasks, the 50-step arm is contaminated, and the 'Max Diff' statistic takes the best of three variants per domain.", ["agg:DP-A03", "agg:DP-A04", "agg:DP-A05"], ["agg:DP-A06", "son55:E024"]),
        "E.cost": R("resolved", 1, "Equal inference settings and step caps; no GPT-4o labelling cost, training compute or on-device latency despite the efficiency framing.", ["son55:E034"], ["agg:DP-A07", "son55:E029"]),
    },
    "resolutions": {
        "rs.matches": ("same_supported_fact", "self_supervised_signal_engineering/rs:C26", "Identical card; the conflict is only the 'rs:' prefix. Fit recorded as partial (son55).", ["son55:E009"], NA),
        "domain.matches": ("revised", "learned_outcome_and_process_judges/null + rule_reward_single_step_rl/gui:R01 (partial)", "Keeps sol's null sub for the judge (C25 is trajectory scoring) and son55's R01 as the operational shape; drops trajectory-level entries (sol's null and son55's K26) because training is on single-step instances without first-error localisation.", ["agg:DP-A01", "son55:E005"], NA),
        "rating.G": ("son55", {"status": "resolved", "rating": 1}, "The gap premise is partly contradicted by the method's reliance on gold labels (agg:DP-A01/A02) and the privacy gap is asserted only; sol's 2 credited the framing.", ["agg:DP-A01", "agg:DP-A02", "agg:DP-A07"], "-3.75 vs sol"),
        "rating.E.holdout": ("son55", {"status": "resolved", "rating": 2}, "Static AGUVIS training vs online OSWorld evaluation is a genuine train/test separation (anchor 2 with gaps), and all three variants are reported, limiting selection bias; sol's 1 under-credited this.", ["son55:E033"], "+2.5 vs sol"),
        "rating.E.statistics": ("sol", {"status": "resolved", "rating": 2}, "Repeated runs (n=3) with denominators are the relevant statistical evidence; missing spread and the contaminated 50-step arm are the remaining gaps (anchor 2). Consistent with single-run papers in this run receiving 1.", ["agg:DP-A03"], "+1.25 vs son55"),
        "expectation.E09": ("son55", "unmet", "No SFT-only, filtered-BC or other RL/preference baseline on the same data; pair-strategy variants are not comparison baselines.", ["son55:E028"], NA),
        "expectation.E12": ("son55", "unmet", "No alternative reward source and no hacking/bias analysis; a gain over base alone is not what E12 asks.", ["son55:E028"], NA),
        "expectation.E21": ("son55", "unknown", "The observation setting is not stated in the text.", [], NA),
        "expectation.E22": ("sol", "not_applicable", "No claim that the recipe generalises across policy backbones; 'generalizable' refers to tasks.", [], NA),
        "expectation.E27": ("son55", "unmet", "The judged preference pairs are synthetic training data; no data-size or scaling information exists.", [], NA),
        "expectation.E28": ("sol", "not_applicable", "No self-generated tasks, explored transitions, memory or synthesised environments; AGUVIS instances are fixed. Train/test separation is judged under E.holdout.", [], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items M=2, X=2, E.measurement=2, E.causality=1, E.cost=1, claim_type component_training, evidence_level online, claim_support scoped were re-checked: all stand.",
    "claims_append": {"C3": (["agg:DP-A01", "agg:DP-A02"], "The judge sees the gold answer; DPO-1 prefers the gold label itself."),
                      "C4": (["agg:DP-A07"], "Privacy guarantee asserted, not measured.")},
    "status": ("accepted_final", "All 11 mechanical conflicts resolved from the fixed text; no scoring unknowns."),
    "expected_score": 42.5,
}

# ----------------------------------------------------------------------------------------------- KG-RAG
KG = {
    "pk": "2509.00366",
    "prelim": ("Read before seat scores (on-disk listing-preserving render; algorithm bodies visible). Offline: xTester explores each app (1 h "
               "DroidTask apps, 8 h for 30 Chinese apps) into a UTG; a VLM infers intents from screens, an LLM decomposes them into "
               "milestones and scores BFS candidate paths (threshold/step_size/max_depth/top-K named, values absent); paths are summarised "
               "into an intent->trajectory vector store. Online: top-K retrieval of stored paths into the agent prompt. Evaluation on the "
               "same apps the store was built from; the success/decision-accuracy adjudication is never described; KG-Android-Bench "
               "reference sequences are generated by KG-RAG itself and its size is given as 300 and 'over 200'; plug-in and transfer "
               "cells have ~10 tasks; construction model/embedding choices are selected on KG-Android-Bench. Applicable cards/expectations: "
               "rs adapt_via_conditioning (retrieval conditioning); gui K27; E02, E10/E11, E13, E16, E28, E35."),
    "materials": [("2509.00366", "paper", UPGRADED)],
    "evidence": [
        A("KG-A01", "2509.00366", "Sec 4", "These steps are generated by KG-RAG, as demonstrated in Figure 1",
          "Benchmark reference sequences come from the method under test."),
        A("KG-A02", "2509.00366", "Sec 5.1", "A new benchmark of over 200 real-world tasks spanning 30 Chinese apps",
          "Conflicts with Table 1's 300 tasks; denominator unclear."),
        A("KG-A03", "2509.00366", "Sec 5.1 metrics", "Success Rate (SR), which measures the percentage of user instructions successfully completed",
          "Only definition of success; no checker, annotator or judge is described."),
        A("KG-A04", "2509.00366", "Sec 3.1", "we utilize a 1-hour automated exploration per app using xTester",
          "The knowledge store is built from the same DroidTask apps that are evaluated."),
        A("KG-A05", "2509.00366", "Algorithm 3 (re-render)", "13 Keep top- K K candidates (by score, prefer shorter paths) and update Q Q 14 end while",
          "Algorithm body (visible only in the listing-preserving render) takes threshold, step_size, max_depth and top-K as inputs without values; it matches the prose."),
        A("KG-A06", "2509.00366", "Sec 5.5", "Based on these results, we select doubao-embedding-text for the final KG-RAG system",
          "Retrieval component selected on the evaluation benchmark."),
        A("KG-A07", "2509.00366", "Table 9", "Weibo (web) | UI-TARS-web | 50.0 | 70.0 | 7.6", "Transfer cells are multiples of 10 (about 10 tasks)."),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "Live device interaction, but the success adjudicator is undescribed (provisional online); the store is built from the evaluated apps (EVIDENCE rule 2 caps at online) and the web/desktop rows are the same services with ~10 tasks and the same undescribed scoring, so transfer is not established.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single run: with GPT-4, retrieving intent->trajectory paths compiled from a 1-hour UTG of each DroidTask app raises average SR from 66.94 (AutoDroid) to 75.80 on the same apps (Qwen2-VL-72B 62.8 -> 70.5); plug-in and cross-platform rows are directionally positive on ~10-task cells.",
        "not_supported": ["That intent-guided LLM search (vs any same-app path store) causes the gain", "Transfer to unseen apps", "Benchmark quality of KG-Android-Bench (self-generated references)"],
        "unresolved": ["Success/DA adjudication", "Overlap between stored intents/paths and test tasks", "Search hyper-parameter values"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "AutoDroid is the explicit UTG neighbour but its full text is outside the fixed package (author-attributed delta). Fixed references AWM/SkillWeaver already store reusable workflows/skills for retrieval; KG-RAG does not compare to them. Benchmark references are generated by KG-RAG (agg:KG-A01).",
        "evidence_ids": ["agg:KG-A01", "sol:R01", "son55:E033"],
    },
    "rs": ("custom", "Online operation is retrieval-as-conditioning of a frozen agent (adapt_via_conditioning, C03 partial, both held-out steps missing). The offline intent->milestone->BFS search is a distinct operation recorded as supporting decompose_and_delegate with sub null: C25 needs the intermediate artifact checked by a sound solver/oracle, but milestones are only scored by an LLM. Not outside_taxonomy: the conditioning main fits the executed operation."),
    "domain": [("sol", "experience_memory_retrieval", "K27", None), ("son55", "exploration_driven_task_synthesis", "K14", "weak")],
    "pmap_patch": {0: {"main": "experience_memory_retrieval", "sub": "K27"}},
    "domain_note": "K27 (retrieve stored experience into context) matches the online retrieval; C19 not kept because the store is built by a test tool, not the agent's own runs. K14 weak: intents are inferred over explored states, but used for retrieval memory rather than training pairs.",
    "expectations": {"E02": "sol", "E11": "sol", "E13": "son55", "E15": "son55", "E18": "son55", "E27": "son55", "E28": "sol"},
    "ratings": {
        "G": R("resolved", 2, "Deep navigation in unfamiliar apps is a real, illustrated bottleneck with AutoDroid named, but the AutoDroid delta is author-attributed and workflow/skill-memory neighbours are neither discussed nor compared.",
               ["son55:E033", "son55:E034", "sol:E04"]),
        "M": R("resolved", 2, "Concrete offline-to-online mechanism; untested assumptions that inferred intents match real instructions and that LLM milestone scores identify correct paths; no distinguishing prediction against simply exposing the UTG/shortest paths.",
               ["son55:E006", "son55:E007", "son55:E008", "sol:E02"], ["son55:E042"]),
        "X": R("resolved", 2, "Pipeline stages, scoring and storage are described and Algorithm 1-3 bodies (listing-preserving render) match the prose, but top-K, thresholds, step size, depth, prompts and per-agent integration have no values; retrieved paths are not verified; staleness boundaries are limited to cost.",
               ["agg:KG-A05", "son55:E008", "son55:E009", "son55:E031"], ["son55:E041"]),
        "E.measurement": R("resolved", 1, "Success and decision accuracy are defined but their adjudication is not described; KG-Android-Bench references are produced by KG-RAG and its size is inconsistent.",
                           ["agg:KG-A03", "agg:KG-A01", "agg:KG-A02"], ["son55:E038"]),
        "E.causality": R("resolved", 1, "With/without comparisons exist, but the knowledge store is built from the evaluated apps with no overlap check, there is no raw-UTG/shortest-path/workflow-memory baseline or ablation of intent/milestone/BFS steps, and construction choices were selected on the evaluation benchmark.",
                         ["son55:E015", "son55:E019", "son55:E020"], ["agg:KG-A04", "agg:KG-A06", "son55:E042"]),
        "E.holdout": R("resolved", 1, "Store and evaluation share apps; no held-out apps or filtered queries; benchmark references are self-generated; the web/desktop rows are the same services on ~10-task cells.",
                       ["agg:KG-A04", "agg:KG-A01", "agg:KG-A07", "son55:E026"]),
        "E.statistics": R("resolved", 1, "Benchmark-level denominators are given (162, 150 tasks; 300 vs 'over 200' inconsistent), but single runs, no spread and ~10-task cells.",
                          ["son55:E017", "son55:E018", "agg:KG-A02", "agg:KG-A07"]),
        "E.cost": R("resolved", 2, "Exploration time (1 h / 8 h) and a 1-8 h quality curve plus average steps are reported; LLM search tokens, retrieval latency, store size and K are not.",
                    ["son55:E004", "son55:E028", "sol:E13"], ["son55:E041"]),
    },
    "resolutions": {
        "evidence_level": ("son55", "online", "Store built from the evaluated apps caps the main results at online (EVIDENCE rule 2), the success adjudicator is undescribed, and the web/desktop rows are the same services with ~10 tasks; this does not establish transfer.", ["agg:KG-A03", "agg:KG-A04", "agg:KG-A07"], "none (evidence_level is not scored)"),
        "status": ("son55", "reviewed", "sol's needs_evidence was due to the v1 render dropping Algorithm 1-3; the listing-preserving render shows the bodies (no parameter values), which resolves X without changing it from son55's 2.", ["agg:KG-A05"], "enables a score (raw 41.25)"),
        "rs.primary": ("son55", "adapt_via_conditioning", "Retrieval of stored paths into a frozen agent's context is the card's 'retrieved instances as conditioning' operation; outside_taxonomy would ignore an executed fit.", ["son55:E010"], NA),
        "rs.supporting": ("son55", ["decompose_and_delegate"], "The offline intent->milestone->BFS search is a separate operation from retrieval.", ["son55:E008"], NA),
        "rs.outside": ("son55", False, "See rs.primary.", ["son55:E010"], NA),
        "rs.matches": ("revised", "adapt_via_conditioning/rs:C03 (partial) + decompose_and_delegate/null", "Keeps son55's mains; drops C25 because milestones are scored by an LLM, not a sound solver/oracle that closes the loop (same criterion as c3 MobileSteward/EcoAgent).", ["son55:E008", "agg:KG-A05"], NA),
        "domain.matches": ("revised", "experience_memory_retrieval/gui:K27 + exploration_driven_task_synthesis/gui:K14 (weak)", "K27 (sol) fits the online retrieval better than C19 (store comes from a test tool, not the agent's runs); K14 (son55) kept as weak for intent inference over explored states.", ["son55:E010", "son55:E006"], NA),
        "rating.X": ("son55", {"status": "resolved", "rating": 2}, "sol's unknown came from the v1 render dropping the algorithm listings. The listing-preserving render of the same version shows Algorithm 1-3 consistent with the prose and still without parameter values; son55 had read the same bodies (recorded material_drift). Final 2.", ["agg:KG-A05", "son55:E031"], "unknown -> 2 (X contributes 10.0); score becomes computable"),
        "rating.E.causality": ("son55", {"status": "resolved", "rating": 1}, "The strongest alternative explanation (retrieval of same-app paths that overlap the test tasks) is untested, there is no simple path-store baseline, and choices were tuned on the evaluation set; sol's 2 credited the with/without design only.", ["agg:KG-A04", "agg:KG-A06"], "-2.5 vs sol"),
        "rating.E.holdout": ("son55", {"status": "resolved", "rating": 1}, "Same-app store and evaluation with self-generated benchmark references; the 10-task web/desktop rows cannot carry a holdout claim.", ["agg:KG-A01", "agg:KG-A04", "agg:KG-A07"], "-2.5 vs sol"),
        "rating.E.statistics": ("son55", {"status": "resolved", "rating": 1}, "Benchmark-level denominators exist, so not_reported/0 is too strong (same rule as c3 ClawGUI); single runs keep it at 1.", ["son55:E017"], "+1.25 vs sol"),
        "expectation.E02": ("sol", "unmet", "No AndroidWorld result; the online substitute has no described verifier.", ["agg:KG-A03"], NA),
        "expectation.E11": ("sol", "unmet", "The LLM milestone scorer acts as the evaluator that selects which paths enter the store; no per-class reliability is reported.", ["son55:E008"], NA),
        "expectation.E13": ("son55", "unknown", "Whether execution checkers exist for the new benchmarks cannot be determined from the text.", ["agg:KG-A03"], NA),
        "expectation.E15": ("son55", "partial", "Decision accuracy is a headline metric alongside SR; its reference and the SR verification are unspecified.", ["agg:KG-A03"], NA),
        "expectation.E18": ("son55", "not_applicable", "Offline BFS is store construction, not inference-time best-of-N or lookahead.", [], NA),
        "expectation.E27": ("son55", "partial", "Synthesised stored trajectories improve agents; a construction-time curve (1-8 h) exists but on one app with 10 tasks.", ["son55:E028"], NA),
        "expectation.E28": ("sol", "partial", "Synthesis and evaluation share apps, but a (weak) out-of-platform transfer is reported.", ["agg:KG-A07"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items G=2, M=2, E.measurement=1, E.cost=2, claim_type system_method, claim_support scoped were re-checked; all stand, with E.measurement reasons extended by the self-generated benchmark references and the 300 vs 'over 200' inconsistency.",
    "claims_append": {"C6": (["agg:KG-A01", "agg:KG-A02"], "Benchmark reference sequences are generated by KG-RAG; task count inconsistent (300 vs over 200)."),
                      "C3": (["agg:KG-A07"], "Web/desktop rows are ~10-task cells on the same services.")},
    "status": ("accepted_final", "All 18 mechanical conflicts resolved; X resolved from the listing-preserving render of the same version (son55 value); no scoring unknowns."),
    "expected_score": 41.25,
}

# ----------------------------------------------------------------------------------------------- StainFlow
SF = {
    "pk": "2606.07027",
    "prelim": ("Read before seat scores (main text, appendices, and the PDF supplement prompts). Prompted auxiliary VLM (Qwen3.5-9B/27B) "
               "extracts screenshot-checkable entities, observes them per step (also sees the policy's actions and raw response as text "
               "context), updates decaying stain concentrations, recalls candidate key nodes, verifies them with entity-linked evidence "
               "windows, and mixes stain and key-node terms into step rewards added to GRPO outcome advantages. AndroidWorld: training "
               "tasks from the same templates with other seeds; single run per cell; 60.34 vs OS-Themis 58.62 (9B) and 62.28 vs 60.34 (27B) "
               "= ~2 tasks; 62.28 is not k/116; eta and lambda_r tuned on the same evaluation. OGRBench judgment 87.4-88.2 vs OS-Themis "
               "86.4-86.6. Baselines re-implemented with binary step rewards. Applicable cards/expectations: rs C26 (partial); gui K19, "
               "C25; E02, E11, E12, E13, E14, E16, E28."),
    "materials": [("2606.07027", "paper", UPGRADED), ("2606.07027.pdf-supplement", "pdf_supplement", "Authoritative Appendix E prompt bodies (sha 502c25c4...), absent from both HTML renders; added after both seat a1 records closed.")],
    "evidence": [
        A("SF-A01", "2606.07027", "Sec 4.1 Datasets", "The training set is generated from AndroidWorld task templates with random seeds different from the validation set, yielding 928 trajectories.",
          "Seed-level split only; same templates and apps."),
        A("SF-A02", "2606.07027", "Table 1", "StainFlow | 62.28 | 0.81 | 0.39 | 0.42 | 18.36", "62.28% is not k/116 (72/116=62.07); other cells are."),
        A("SF-A03", "2606.07027", "Appendix D Table 5", "0.4 | 60.34 | 0.78 | 0.41 | 0.37", "lambda_r selected on the AndroidWorld evaluation it reports."),
        A("SF-A04", "2606.07027", "Sec 4.1 Baselines", "For ADMIRE and OS-Themis, milestone and non-milestone steps receive rewards of 1 and 0.", "Baselines re-implemented with binary step rewards."),
        A("SF-A05", "2606.07027.pdf-supplement", "Appendix E Prompt 2", "Raw model response: {raw_response}", "Observer receives the policy's raw response as text context (rules say: never as proof)."),
        A("SF-A06", "2606.07027.pdf-supplement", "Appendix E Prompt 3", "A key node must change what is known or achieved for the task, not merely show that the agent",
          "Key-node acceptance/rejection rules are explicit, making the verifier interface reconstructable."),
        A("SF-A07", "2606.07027.pdf-supplement", "Appendix E Prompt 1", "Extract screenshot-checkable entities for later trajectory scoring and classify the task.",
          "Entity extraction prompt with schema (persistent/transient, importance, validation_rule)."),
        A("SF-A08", "2606.07027", "Appendix B.1", "StainFlow instead makes at most two verifier calls per step", "Cost advantage asserted, not measured."),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "AndroidWorld rule-based outcome checks; training and evaluation share templates and apps (rule 2 caps at online); OGRBench is an offline judgment benchmark.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported single runs: adding StainFlow step rewards to GRPO outcome reward for Qwen3-VL-8B raises AndroidWorld success from 54.31 (outcome only) to 60.34 (9B verifier) / 62.28 (27B), about two tasks above re-implemented OS-Themis, with seed-level train/test separation and hyper-parameters tuned on the reported set; as a completion judge it is 1-2 points above OS-Themis on OGRBench across verifiers.",
        "not_supported": ["'Objective' rewards (VLM-dependent, unvalidated against human step labels)", "Statistical separation from OS-Themis", "Lower compute than OS-Themis (asserted)", "Generalisation to unseen templates/apps/backbones"],
        "unresolved": ["62.28 not a k/116 count", "Measured verifier cost"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "Global milestone PRMs (ADMIRE, OS-Themis) and local step critics (GUI-Critic-R1) are re-implemented and compared, but their full texts are outside the fixed package; the local-window limitation is measured (evidence span), the milestone-subjectivity limitation is argued.",
        "evidence_ids": ["agg:SF-A04", "son55:E039"],
    },
    "rs": ("son55", "self_supervised_signal_engineering/C26 in both seats (sol 'rs:C26'): same card. Fit partial: a manufactured dense scalar reward compared within GRPO groups, not a preference objective."),
    "domain": [("son55", "learned_outcome_and_process_judges", "K19", None), ("son55", "learned_outcome_and_process_judges", "C25", "partial")],
    "domain_note": "K19 (dense step-level process rewards for multi-turn GUI RL) for the RL reward; C25 (LLM judge scoring whole trajectories) for the OGRBench completion-judgment half. sol's null sub rejected K19 as human-label-trained, which the card title does not require.",
    "expectations": {"E02": "son55", "E07": "son55",
                     "E13": EXP(True, "unmet", "The RL outcome reward comes from AndroidWorld per-task rule-based validators; their false positives/negatives are not measured (same reading as c3 ClawGUI)."),
                     "E14": "son55", "E15": "son55", "E21": "son55",
                     "E22": EXP(False, "not_applicable", "No claim that the recipe generalises across policy backbones; the paper states it has not been validated at larger scales. Only verifier size is varied."),
                     "E28": "son55"},
    "ratings": {
        "G": R("resolved", 3, "Two concrete PRM limitations with named neighbours; the local-window one is measured (evidence spans 7.6-14.1 steps), the milestone one argued; neighbour full texts outside the fixed set.", ["son55:E003", "son55:E039", "sol:E01"], ["son55:E048"]),
        "M": R("resolved", 3, "Entity-state dynamics and entity-linked windows target the credit-assignment gap and make predictions the ablations test (stain-only over-rewards failures; fixed window loses signal); assumes progress is visible and VLM recognition reliable.", ["son55:E004", "son55:E007", "son55:E028", "son55:E029"], ["son55:E046"]),
        "X": R("resolved", 3, "Equations, thresholds, windows, reward mixing, advantage, training settings, baseline adaptations, Algorithm 1/2 (listing-preserving render) and all five prompt blocks (PDF supplement) make the verifier interface reconstructable; tau_B=0 leaves candidate recall nearly unfiltered and invisible-progress/failure boundaries are not characterised.",
               ["agg:SF-A05", "agg:SF-A06", "agg:SF-A07", "son55:E004", "son55:E012"], ["son55:E006"]),
        "E.measurement": R("resolved", 2, "AndroidWorld rule-based success and labelled OGRBench are credible; step rewards are not validated against human labels, the reward-gap statistic compares differently scaled rewards, and 62.28 is not a k/116 count.", ["son55:E011", "son55:E019", "agg:SF-A02"], ["son55:E048"]),
        "E.causality": R("resolved", 2, "Outcome-only, three PRM baselines and three component ablations give real attribution, but eta and lambda_r were tuned on the reported evaluation, baselines are re-implemented with binary rewards, there is no plain per-step VLM judge with the same verifier, and margins are ~2 tasks.",
                         ["son55:E028", "son55:E029", "son55:E012"], ["agg:SF-A03", "agg:SF-A04", "son55:E014"]),
        "E.holdout": R("resolved", 1, "Training uses other seeds of the same AndroidWorld templates/apps; hyper-parameters chosen on the reporting data; no unseen templates/apps/backbones.", ["agg:SF-A01", "agg:SF-A03", "son55:E030"]),
        "E.statistics": R("resolved", 1, "One run per cell, no spread; checklist cites fixed seeds instead of error bars; ~2-task margins.", ["son55:E022", "son55:E042"], ["son55:E047"]),
        "E.cost": R("resolved", 1, "Equal epochs/batch/group and average steps reported; compute, wall-clock, tokens and verifier calls are not measured and the saving over OS-Themis is asserted.", ["son55:E012", "son55:E015"], ["agg:SF-A08", "son55:E049"]),
    },
    "resolutions": {
        "status": ("son55", "reviewed", "sol stopped at needs_evidence because the HTML render lacked Appendix E prompts and algorithm listings. The PDF supplement (prompts) and the listing-preserving render (algorithms) supply them and confirm son55's X=3 (see shared_error_corrections).", ["agg:SF-A05", "agg:SF-A06", "agg:SF-A07"], "enables a score (raw 60.0)"),
        "rs.matches": ("same_supported_fact", "self_supervised_signal_engineering/rs:C26 (partial)", "Same card; conflict is the 'rs:' prefix. Fit partial (son55): scalar rewards within GRPO groups, no preference objective.", ["son55:E004"], NA),
        "domain.matches": ("son55", "gui:K19 + gui:C25 (partial)", "Both operations (RL step reward; completion judgment) have specific subs; K19's title does not require human-label training.", ["son55:E019", "son55:E033"], NA),
        "rating.X": ("son55", {"status": "resolved", "rating": 3}, "With the five prompts (supplement) and algorithm listings, the interface is reconstructable; remaining gaps (tau_B=0, no failure boundaries, no cost) keep it at 3, matching son55's value reached without the prompts.", ["agg:SF-A05", "agg:SF-A06", "agg:SF-A07"], "unknown -> 3 (X contributes 15.0); score becomes computable"),
        "rating.E.causality": ("son55", {"status": "resolved", "rating": 2}, "Tuning eta/lambda_r on the reported 116-task evaluation and binary re-implementations of baselines are untested alternative explanations for ~2-task margins; sol's 3 credited the control set without them.", ["agg:SF-A03", "agg:SF-A04"], "-2.5 vs sol"),
        "expectation.E02": ("son55", "met", "Online AndroidWorld success is reported.", ["son55:E019"], NA),
        "expectation.E07": ("son55", "not_applicable", "The claim is about a PRM improving RL, not a new end-to-end agent model.", [], NA),
        "expectation.E13": ("revised", "unmet", "Neither seat applied E13: the outcome reward comes from AndroidWorld rule validators (an RL pipeline with per-task checkers) and no two-sided checker measurement is given.", ["son55:E011"], NA),
        "expectation.E14": ("son55", "partial", "Verifier models are varied (8B/9B/27B/GPT-5/Gemini) but there is no human-label source; varying VLMs is not a challenge to the expectation.", ["son55:E033"], NA),
        "expectation.E15": ("son55", "not_applicable", "OGRBench supports a judge claim; the capability claim is measured online.", [], NA),
        "expectation.E21": ("son55", "met", "All methods share the same screenshot-based policy and observation; no cross-observation comparison.", [], NA),
        "expectation.E22": ("revised", "not_applicable", "No cross-backbone generalisation claim (only verifier size varies); sol's partial and son55's unmet both applied it.", [], NA),
        "expectation.E28": ("son55", "unmet", "Training tasks are instantiated from the evaluation templates (seed-level split); no held-out templates/apps.", ["agg:SF-A01"], NA),
    },
    "shared": [
        {"field_path": "rating.X / materials (Appendix E prompts)", "shared_value": "Neither seat had the five Appendix E prompt bodies (sol: X unknown; son55: X 3 with prompts recorded as missing_sections)",
         "corrected_value": {"status": "resolved", "rating": 3},
         "reason": "The authoritative PDF supplement (sha 502c25c4...) gives the system prompt and four verifier prompts: entity schema, step observation (including the policy's raw response as non-proof context), explicit key-node accept/reject rules and completion rules. This confirms that the verifier interface is reconstructable; it adds one risk (raw-response exposure) that is already bounded by the prompt rules. No rating moves beyond son55's 3.",
         "evidence_ids": ["agg:SF-A05", "agg:SF-A06", "agg:SF-A07"], "source": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2606.07027.pdf-supplement.txt (added after a1 seat closure, per controller instruction)",
         "score_impact": "sol's X unknown -> 3; final score computable (60.0); son55 value unchanged"},
    ],
    "agreed_review": "Agreed items G=3, M=3, E.measurement=2, E.holdout=1, E.statistics=1, E.cost=1, claim_type component_training, evidence_level online, claim_support scoped were re-checked against the text and supplement; all stand.",
    "claims_append": {"C1": (["agg:SF-A02", "agg:SF-A03"], "62.28 is not k/116; lambda_r/eta tuned on the reported evaluation."),
                      "C6": (["agg:SF-A08"], "Two calls per step is asserted; no measured cost.")},
    "status": ("accepted_final", "All 13 mechanical conflicts resolved; X resolved via the PDF supplement and listing-preserving render (recorded as a shared-error correction); no scoring unknowns."),
    "expected_score": 60.0,
}

# ----------------------------------------------------------------------------------------------- ATMem
AT = {
    "pk": "2606.31612",
    "prelim": ("Read before seat scores (main text, appendix, PDF Boxes A.3/A.7, MAI-UI reference). ATMem: agent-written JSON state (phase, "
               "constraints, schema, item status remaining/finished/skipped) carried in the prompt; SFT on 21,713 verifier-gated steps from "
               "a GPT-5+UIIns teacher on a 20-app virtual Android platform with 120 templates; STR-GRPO contrasts memory-ON/OFF cohorts "
               "with a memory-activity cost. AndroidWorld 76.6 (8B; not k/116), MobileWorld 23.3 (base 9.4; stated unseen), DataScope "
               "(authors', 32 families x 3 levels on AndroidWorld-style apps, verifiers calibrated on perturbed terminal states) 6.2/6.2/3.1 SR "
               "= 2/2/1 tasks. Table 2 copies MAI-UI's MobileWorld GUI-only column but omits MAI-UI-8B 27.5 and Doubao-1.5-UI-TARS 26.3, "
               "both above 23.3, so 'strongest / +36.2%' is contradicted. No SFT/RL control without the ATMem block. Single runs. "
               "Applicable cards/expectations: gui C16, K13, trajectory-level RL; E02, E07, E16, E17, E19, E21, E27, E28."),
    "materials": [("2606.31612", "paper", UPGRADED),
                  ("2606.31612.pdf-supplement", "pdf_supplement", "Authoritative Box A.3/A.7 prompt bodies (sha f988a9d9...), absent from both HTML renders; added after both seat a1 records closed."),
                  ("2512.22047", "nearest_neighbor_reference", None)],
    "evidence": [
        A("AT-A01", "2606.31612", "Table 2", "UI-Venus-1.5 ( Team et al., 2026 ) | 30B | 17.1", "Strongest row ATMem lists on MobileWorld; 23.3/17.1 = the claimed +36.2%."),
        A("AT-A02", "2512.22047", "MAI-UI Table 8 (GUI-Only 116)", "MAI-UI-8B | 27.5 | 22.2 | 20.0 | 24.9", "Same column ATMem copies its other rows from; MAI-UI-8B 27.5 > 23.3."),
        A("AT-A03", "2512.22047", "MAI-UI Table 8", "Doubao-1.5-UI-TARS ( Seed, 2025b ) | 26.3 | 32.4 | - | 20.9", "Doubao-1.5-UI-TARS 26.3 > 23.3; ATMem names it as a baseline but omits it from Table 2."),
        A("AT-A04", "2606.31612", "Sec 1 contributions", "achieves a 36.2% relative improvement over the strongest baseline on MobileWorld", "Claim contradicted by agg:AT-A02/A03."),
        A("AT-A05", "2606.31612", "Sec 4.1 Baselines", "Doubao-1.5-UI-TARS ( Qin et al., 2025 ) , and GELab-Zero ( Team, 2025 )", "Doubao-1.5-UI-TARS listed as a compared baseline."),
        A("AT-A06", "2606.31612", "Sec 4.1", "We use a virtual Android platform containing 20 applications for both SFT trajectory collection and online RL training.",
          "Training platform parallels AndroidWorld (20 apps) and DataScope apps; no overlap analysis."),
        A("AT-A07", "2606.31612", "Table 4", "SFT + STR-GRPO | 76.6 | 31.9 | 23.3 | 30.1", "76.6 is not k/116 (89/116=76.7)."),
        A("AT-A08", "2606.31612.pdf-supplement", "Box A.3", "Use <memory> only when cross-step storage or comparison is needed; otherwise output {}.",
          "Execution prompt: memory is optional and schema-bound (phase/context/schema/items with status)."),
        A("AT-A09", "2606.31612.pdf-supplement", "Box A.3", "You are given a task goal, previous action history, and screenshots of the current screen.",
          "Agent observation is screenshot + action history (no a11y tree)."),
        A("AT-A10", "2606.31612", "Table 2 vs MAI-UI Table 8", "GUI-Owl ( Ye et al., 2025 ) | 72B | 8.5", "MAI-UI lists 8.5 for GUI-Owl-32B; ATMem labels it 72B (minor provenance slip)."),
    ],
    "assessment": {
        "evidence_level": "transfer",
        "evidence_level_note": "MobileWorld is stated unseen (different app set) and shows a same-protocol base-to-final gain (9.4 -> 23.3); AndroidWorld/DataScope alone would be online because the training platform parallels their apps.",
        "claim_support": "scoped",
        "contradicted_subclaims": ["'Outperforms the strongest baseline on MobileWorld by 36.2%': MAI-UI-8B 27.5 and Doubao-1.5-UI-TARS 26.3 in the same GUI-only column exceed 23.3"],
        "strongest_supported_claim": "Author-reported single runs: SFT on 21,713 verifier-gated ATMem steps then STR-GRPO takes Qwen3-VL-8B from 47.6 to 76.6 on AndroidWorld and from 9.4 to 23.3 on stated-unseen MobileWorld; STR-GRPO lowers the fraction of memory-active tasks by ~14 points at equal or higher SR than standard GRPO. The contribution of the ATMem structure itself (vs in-domain verified teacher data and RL) is not isolated for the trained model, and on MobileWorld it is below published MAI-UI-8B and Doubao-1.5-UI-TARS.",
        "not_supported": ["Best end-to-end agent on MobileWorld", "ATMem structure as the cause of the trained model's gains", "Memory cost reduction in tokens/latency"],
        "unresolved": ["Overlap of the 120 training templates with AndroidWorld/DataScope", "Evaluation step caps", "Run-to-run variance"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "MAI-UI (fixed reference, whose RL infrastructure ATMem says it follows) supplies the MobileWorld rows ATMem copies, including the two omitted stronger results. Execution-memory neighbours (note-taking, anchored states, program-state) are named but outside the fixed package.",
        "evidence_ids": ["agg:AT-A02", "agg:AT-A03", "son55:E043"],
    },
    "rs": ("son55", "outside_taxonomy: the central operations (agent-maintained execution-state block; memory-ON/OFF interventional RL with a cost term) match no original main card's load-bearing step. sol's controlled_diagnostic_design/C02 primary attaches to a training-signal intervention (not an evaluation instrument) and to the secondary benchmark; son55 read the candidate cards and declined to force one."),
    "domain": [("son55", "agent_loop_context_control", "C16", None), ("sol", "trajectory_level_policy_training", None, None), ("son55", "verifiable_execution_reward", "K13", "partial")],
    "domain_note": "C16 (agent nominates content retained across steps) = ATMem; STR-GRPO under trajectory_level_policy_training with sub null (K20 needs learned value baselines/replay; replay is disabled); K13 for template+verifier task construction (SFT data and DataScope).",
    "expectations": {"E02": "son55", "E17": "sol", "E19": "son55",
                     "E21": EXP(True, "partial", "Box A.3 (PDF supplement) fixes ATMem-UI's observation as screenshots plus action history; observation settings of the cross-paper baselines are not stated."),
                     "E27": "son55", "E35": "son55"},
    "ratings": {
        "G": R("resolved", 3, "A concrete failure mode (repeated/missed/over-scoped operations; stuck loops 40.9% of MAI-UI-8B DataScope failures) tied to a representational gap; execution-memory neighbours are named but not compared head-to-head.", ["son55:E003", "son55:E004", "son55:E036", "son55:E037"], ["son55:E041"]),
        "M": R("resolved", 3, "Item-status execution state plus ON/OFF-interventional RL is a coherent, testable answer (fewer stuck loops, higher scope-F1, lower memory use at equal SR); the assumption that the model writes correct statuses is untested.", ["son55:E006", "son55:E007", "son55:E013", "son55:E025"], ["son55:E048"]),
        "X": R("resolved", 3, "State fields, statuses, SFT pipeline, RL objective, cohorts, hyper-parameters, infrastructure and (via Box A.3/A.7) the execution and task-generation prompts are specified; state-update correctness is never checked and evaluation step caps are unstated.", ["agg:AT-A08", "agg:AT-A09", "son55:E008", "son55:E013", "son55:E039"], ["son55:E050"]),
        "E.measurement": R("resolved", 2, "Execution-based AndroidWorld/MobileWorld and calibrated DataScope verifiers are good, but Table 2 omits stronger published rows from the very column it copies (contradicting the 'strongest' claim), baselines are cross-paper under unknown protocols, and own numbers are not k/116 counts.",
                           ["son55:E016", "son55:E034", "agg:AT-A01"], ["agg:AT-A02", "agg:AT-A03", "agg:AT-A04", "agg:AT-A07", "agg:AT-A10"]),
        "E.causality": R("resolved", 2, "Stage ablation and a same-planner memory-format case give partial attribution; no fine-tuned control without the ATMem block, and the +23 SFT gain comes from in-domain verified teacher data.", ["son55:E022", "son55:E023", "son55:E024", "son55:E041"], ["son55:E048"]),
        "E.holdout": R("resolved", 2, "MobileWorld is a stated-unseen environment with a same-protocol base gain, but the AndroidWorld headline rests on a training platform that parallels its apps with no template-overlap analysis, and DataScope uses the same app family.", ["son55:E019", "son55:E021"], ["agg:AT-A06", "son55:E049"]),
        "E.statistics": R("resolved", 1, "Single runs; DataScope SR differences are one task of 32; STR-GRPO margins are 2-3 tasks; own values not k/116.", ["son55:E031", "son55:E047", "agg:AT-A07"]),
        "E.cost": R("resolved", 2, "Training compute (128 H20, 2 h SFT, 3 days RL) and memory-usage fraction are reported; evaluation step budgets and per-step token/latency overhead are not.", ["son55:E039", "son55:E044"], ["son55:E050"]),
    },
    "resolutions": {
        "claim_type": ("son55", "system_method", "The central claim is an agent (memory mechanism + training recipe) with SOTA online success, which the system_method interpretation evaluates; component_training would not cover the closed-loop agent claim.", ["son55:E019"], "none (claim_type sets interpretation, not weights)"),
        "status": ("son55", "reviewed", "sol stopped at needs_evidence because Box A.3/A.5/A.7 were missing from the render. The PDF supplement supplies A.3 and A.7 and confirms son55's X=3 (see shared_error_corrections); Listing 1 is present in the listing-preserving render.", ["agg:AT-A08", "agg:AT-A09"], "enables a score (raw 63.75)"),
        "rs.primary": ("son55", None, "See rs entry: no main card's load-bearing step matches the central operations.", [], NA),
        "rs.outside": ("son55", True, "Same as rs.primary.", [], NA),
        "rs.matches": ("son55", [], "outside_taxonomy requires empty matches.", [], NA),
        "domain.matches": ("revised", "gui:C16 + trajectory_level_policy_training/null + gui:K13 (partial)", "Adds the memory mechanism itself (C16, absent from sol); keeps sol's null sub for STR-GRPO (K20 conditions unmet); keeps K13 for template+verifier construction; drops online_evaluation_methodology/null (DataScope's construction is captured by K13).", ["son55:E006", "son55:E008"], NA),
        "rating.X": ("son55", {"status": "resolved", "rating": 3}, "With Box A.3/A.7 the execution protocol and task generation are reconstructable; gaps (no update-correctness check, unstated step caps) keep 3, matching son55's value reached without them.", ["agg:AT-A08", "agg:AT-A09"], "unknown -> 3 (X contributes 15.0); score becomes computable"),
        "rating.E.measurement": ("son55", {"status": "resolved", "rating": 2}, "Verified against the frozen MAI-UI table: the copied MobileWorld column contains MAI-UI-8B 27.5 and Doubao-1.5-UI-TARS 26.3, both omitted and both above 23.3, so the competitive measurement is selectively reported; sol's 3 did not check it.", ["agg:AT-A02", "agg:AT-A03", "agg:AT-A04", "agg:AT-A05"], "-2.5 vs sol"),
        "rating.E.holdout": ("son55", {"status": "resolved", "rating": 2}, "The headline AndroidWorld number lacks any template/app overlap analysis while training on a parallel 20-app platform; MobileWorld alone supports holdout. sol's 3 rested on MobileWorld.", ["agg:AT-A06"], "-2.5 vs sol"),
        "expectation.E02": ("son55", "met", "Online AndroidWorld success is reported.", ["son55:E019"], NA),
        "expectation.E17": ("sol", "unmet", "Own evaluation step caps are not stated and baseline rows are cross-paper; an equal stated budget cannot be checked.", [], NA),
        "expectation.E19": ("son55", "unknown", "Whether the AndroidWorld/MobileWorld harness was modified cannot be determined from the text.", [], NA),
        "expectation.E21": ("revised", "partial", "Box A.3 (supplement) establishes ATMem-UI as screenshot + history; baselines' observation settings are unstated (son55 'unknown' predates the supplement; sol 'partial' had no stated basis).", ["agg:AT-A09"], NA),
        "expectation.E27": ("son55", "unmet", "Synthetic verified trajectories (21,713 steps) drive the +23 SFT gain; no data-size curve.", [], NA),
        "expectation.E35": ("son55", "not_applicable", "ATMem is within-task working memory, not experience memory built from environments.", [], NA),
    },
    "shared": [
        {"field_path": "rating.X / expectation.E21 / materials (Box A.3, A.7)", "shared_value": "Neither seat had the Box A.3 execution prompt or Box A.7 generator prompt (sol: X unknown; son55: X 3 and E21 unknown with the boxes recorded as missing)",
         "corrected_value": {"rating.X": {"status": "resolved", "rating": 3}, "expectation.E21": "partial"},
         "reason": "The authoritative PDF supplement (sha f988a9d9...) shows the three-block output format, action space, optional schema-bound memory with remaining/finished/skipped statuses and usage protocol, a screenshot+history observation, and a task-generator prompt that varies only data volume/distractors within a fixed task class. This confirms X=3 and fixes ATMem-UI's observation setting for E21.",
         "evidence_ids": ["agg:AT-A08", "agg:AT-A09"], "source": "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2606.31612.pdf-supplement.txt (added after a1 seat closure, per controller instruction)",
         "score_impact": "sol's X unknown -> 3; final score computable (63.75); E21 carries no points"},
    ],
    "agreed_review": "Agreed items G=3, M=3, E.causality=2, E.statistics=1, E.cost=2, evidence_level transfer, claim_support scoped were re-checked; all stand. Additional provenance slip noted (GUI-Owl 8.5 labelled 72B; MAI-UI lists it as 32B).",
    "claims_append": {"C2": (["agg:AT-A01", "agg:AT-A02", "agg:AT-A03", "agg:AT-A04", "agg:AT-A10"], "Generalisation part (9.4 -> 23.3, same protocol) stands as author-reported; the 'strongest baseline / +36.2%' part is contradicted by MAI-UI-8B 27.5 and Doubao-1.5-UI-TARS 26.3 in the copied column."),
                      "C1": (["agg:AT-A07", "agg:AT-A06"], "76.6 is not k/116; training platform parallels AndroidWorld apps without overlap analysis.")},
    "status": ("accepted_final", "All 15 mechanical conflicts resolved; X resolved via the PDF supplement (shared-error correction); MobileWorld omission verified against the frozen MAI-UI reference; no scoring unknowns."),
    "expected_score": 63.75,
}

PAPERS = [PA, DP, KG, SF, AT]
SKIPPED = {"2504.14603": "skipped_a2_pending: the two seats read different renders of 2504.14603 (material_incident_2); the paper is being re-reviewed in batch re1, so neither seat record was opened or used here."}
