"""Opus 5.5 (fable) adjudication decisions for c3/a1, written after reading each fixed full text first.

Seat evidence is namespaced sol:/son55:, own evidence agg: (quotes asserted against the fixed texts).
"""
from common import agg_evidence as A

R = lambda status, rating, reason, ev, ce=(), scope=(): {  # noqa: E731
    "status": status, "rating": rating, "reason": reason, "evidence_ids": list(ev),
    "counterevidence_ids": list(ce), "search_scope": list(scope)}

NA = "none (pattern matches and expectation statuses carry no points)"

# --------------------------------------------------------------------------------------------- MobileSteward
MS = {
    "pk": "2502.16796",
    "prelim": ("Read before seat scores. Prompted GPT-4v/GPT-4o system: a Steward agent splits a cross-app instruction into an "
               "app-level DAG, app-specific Staff agents (AppAgent-style XML+marked screenshots, BM25 top-3 guideline memory) execute, "
               "the Steward judges each sub-task with LLM self-evaluation, forwards results along the DAG and writes successful "
               "experience into two text memories. Evaluation: authors' CAPBench (500 GPT-4-templated instructions over 14 live apps on "
               "an Android Studio emulator; 150 test, the other 350 used for prior self-evolution, memory also updated during test), "
               "SAPBench (50) and MobileAgentBench (baseline rows copied from that paper). How 'instruction completed' is adjudicated "
               "is never stated; Table 2 and Table 3 disagree on the full GPT-4v Task Rate (0.76 vs 0.81); MobileSteward gets 20 steps "
               "x 3 tries per Staff agent while baselines get 80 steps in total; single temperature-0 run. Strongest evidence: module "
               "ablations and app-count stratification. Applicable cards/expectations: gui C17/C18/C19; E10, E16, E17, E20, E28, E35."),
    "materials": [("2502.16796", "paper"), ("2409.07429", "nearest_neighbor_reference")],
    "evidence": [
        A("MS-A01", "2502.16796", "Sec 4.2.2 Evaluation Metrics",
          "Success Rate : To evaluate whether the instruction is completed.",
          "The only definition of success; no checker, annotator protocol or judge is described anywhere in the fixed text, so the verifier cannot be audited."),
        A("MS-A02", "2502.16796", "Table 2 (CAPBench, GPT-4v row)", "MobileSteward | GPT-4v | 0.55 | 0.76 | 0.99",
          "Full system, GPT-4v: SR 0.55, Task Rate 0.76."),
        A("MS-A03", "2502.16796", "Table 3 (ablation, full row)", "MobileSteward | 0.55 | 0.81 | 0.99",
          "Same SR 0.55 but Task Rate 0.81: the 'full' ablation row does not match Table 2; the ablation configuration is unstated."),
        A("MS-A04", "2502.16796", "Sec 4.2.3", "to 80 for all of the baselines",
          "Baselines capped at 80 steps in total, while MobileSteward has N_step=20 per Staff agent with N_try=3 retries, i.e. an unequal and unbounded-by-design budget."),
        A("MS-A05", "2502.16796", "Sec 4.2.3", "we also update the memories during the test.",
          "Memory is written during the test stream on the same 14 apps/templates; no frozen-memory or unseen-app arm."),
        A("MS-A06", "2409.07429", "AWM Sec 2 (online setting)",
          "iteratively induces workflows from self-generated past predictions that are judged correct by an evaluator module",
          "Fixed nearest-neighbour reference already distils evaluator-judged successful runs into reusable memory; MobileSteward's self-evolution half of the gap is not bounded against it.",
          "reviewer_comment"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "Live emulator interaction with real third-party apps, but the success adjudicator is not described (agg:MS-A01), so 'online' is provisional; memory is built and tested on the same apps/templates, so not transfer.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single run: on the 150-instruction CAPBench test split (same 14 apps as the 350 memory-building instructions, memory also updated during test) MobileSteward (GPT-4o) reaches SR 0.59 vs MobileAgent-v2 0.21 under unequal step/retry budgets; module removals lower SR (0.55 -> 0.50/0.44/0.36) with an unstated configuration whose Task Rate disagrees with Table 2.",
        "not_supported": ["App-oriented decomposition per se as the cause (confounded with memory, budget and observation differences)", "Retained self-evolution on unseen apps or other benchmarks", "Reliability of the Steward's success judgements that gate memory writes", "Verifier-checked success (adjudication method unreported)"],
        "unresolved": ["Who/what judges CAPBench success", "Table 2 vs Table 3 Task Rate (0.76 vs 0.81)", "Global step/retry budget actually used per task"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "AWM (2409.07429, fixed reference) already induces reusable workflows from evaluator-judged successful runs (agg:MS-A06); MobileSteward neither cites nor compares to such memory, so only the app-DAG/handoff part of its gap is bounded (vs MobileAgent-v2).",
        "evidence_ids": ["agg:MS-A06", "son55:S035"],
    },
    "rs": ("sol", "decompose_and_delegate with sub null: rs:C25 requires a machine-checkable artifact routed to a sound solver or oracle; here the DAG and results are consumed and judged by LLM agents only (no checker grades the intermediate object). adapt_via_conditioning/null kept as in both seats."),
    "domain": [("sol", "agent_loop_context_control", "C17", None), ("son55", "agent_loop_context_control", "C18", "partial"),
               ("sol", "experience_memory_retrieval", "C19", None)],
    "domain_note": "Union: manager/worker DAG (C17), Steward post-execution evaluation with reflection tips fed back (C18, partial: task-level not action-level), and own-run experience distillation into memory (C19).",
    "expectations": {"E08": {"applicable": False, "status": "not_applicable", "reason": "The Steward/Staff split is a planner/app-executor split; no grounding component or grounder swap is claimed, which is what E08 targets."},
                     "E11": "son55", "E19": "son55", "E20": "sol", "E21": "son55", "E25": "sol", "E28": "sol", "E35": "sol"},
    "ratings": {
        "G": R("resolved", 2, "Cross-app dependency/handoff failure is concrete and MobileAgent-v2 is compared, but the gap size rests only on the authors' own benchmark and the self-evolution half is not bounded against existing success-filtered experience memory (AWM; MobileGPT/AutoDroid only named). Real limitation, incomplete nearest-neighbour comparison -> 2.",
               ["sol:E01", "sol:E15", "son55:S001", "son55:S017", "agg:MS-A06"]),
        "M": R("resolved", 3, "App-level DAG with explicit information flow, per-app specialists and staged evaluation map onto the three named failure sources and yield a testable prediction (advantage grows with app count, Fig 5/Table 5). The LLM self-judgement that gates retries and memory writes is an untested assumption -> 3, not 4.",
               ["son55:S003", "son55:S004", "son55:S007", "son55:S008", "son55:S025", "sol:E03"], ["son55:S026"]),
        "X": R("resolved", 2, "Algorithm, action space, N_try/N_step, BM25 top-3 retrieval are given; prompts, initial expertise contents, the memory-update acceptance rule, retry/stop handling and the ablation configuration are missing.",
               ["son55:S005", "son55:S008", "son55:S012", "sol:E02"], ["son55:S034"]),
        "E.measurement": R("resolved", 1, "Success is only defined as 'whether the instruction is completed'; no checker, annotator or judge is described for CAPBench/SAPBench/online users, so verifier trust cannot be assessed; the full-system Task Rate differs between Table 2 and Table 3; MobileAgentBench baselines are copied. Metrics and denominators exist, so not 0.",
                           ["agg:MS-A01", "agg:MS-A02", "agg:MS-A03", "son55:S015", "son55:S009"], ["son55:S034"]),
        "E.causality": R("resolved", 2, "Three module removals and app-count/backbone analyses point the same way, but baselines lack memory, use different budgets and observations, the DAG itself is not ablated, and the ablation configuration is unclear.",
                         ["son55:S022", "son55:S023", "son55:S024", "son55:S025", "sol:E08"], ["agg:MS-A04", "son55:S021"]),
        "E.holdout": R("resolved", 1, "Instruction-level split only: memory comes from the other 350 instructions on the same apps/templates and is updated during test; no unseen-app or frozen-memory test.",
                       ["son55:S012", "sol:E05"], ["agg:MS-A05"]),
        "E.statistics": R("resolved", 1, "Test denominator (150) and complexity strata given; single temperature-0 run, no spread, no failure taxonomy; ablation gaps are 7-28 tasks.",
                          ["son55:S012", "son55:S025", "sol:E07"]),
        "E.cost": R("resolved", 2, "Actions/task and tokens/action vs MobileAgent-v2 reported, IOT on MobileAgentBench is the highest in its table; no wall-clock or dollars; step/retry budgets differ from baselines.",
                    ["son55:S030", "son55:S031", "son55:S028", "sol:E10"], ["agg:MS-A04"]),
    },
    "resolutions": {
        "rs.matches": ("sol", "decompose_and_delegate/null + adapt_via_conditioning/null", "rs:C25's tactic needs a machine-checkable artifact graded by a sound solver/oracle; MobileSteward's DAG and results are consumed and judged only by LLM agents. son55 itself rated C25 partial with that failure noted.", ["sol:E01", "son55:S007"], NA),
        "domain.matches": ("revised", "gui:C17 + gui:C18(partial) + gui:C19", "Each seat's extra card names a real, different operation: Steward evaluation with reflection tips fed back (C18, task-level) besides the manager/worker DAG (C17) and own-run memory (C19). Namespaced IDs normalised to gui:.", ["son55:S007", "son55:S024", "sol:E04"], NA),
        "rating.G": ("sol", {"status": "resolved", "rating": 2}, "The self-evolution part of the gap is not bounded against existing evaluator-filtered workflow memory (AWM) and the gap size is shown only on the authors' benchmark; son55 listed the same deductions but still placed it at 3.", ["agg:MS-A06", "son55:S017"], "-3.75 vs son55 (G weight 15 x 1/4)"),
        "rating.E.measurement": ("son55", {"status": "resolved", "rating": 1}, "Re-read Sec 4.1-4.2: no success adjudication procedure exists in the fixed text, and Table 2/3 disagree on the same configuration's Task Rate. Without a describable verifier the item cannot sit at 2.", ["agg:MS-A01", "agg:MS-A02", "agg:MS-A03"], "-2.5 vs sol (weight 10 x 1/4)"),
        "expectation.E08": ("son55", "not_applicable", "Value from son55, rationale replaced (son55's text was a generic 'no training' template): E08 concerns grounder swaps / planner-grounder splits, and MobileSteward claims no grounding component.", [], NA),
        "expectation.E11": ("son55", "unmet", "The Steward's success/error verdicts gate retries and memory writes; no per-class reliability is reported. MobileAgentBench FN/FP describe the agent's own FINISH decisions on another benchmark, not the Steward evaluator.", ["son55:S034"], NA),
        "expectation.E19": ("son55", "partial", "MobileAgentBench is an online benchmark whose baseline rows are copied while MobileSteward is run in the authors' own emulator; the added home() action for baselines is disclosed but no harness-equivalence check is given.", ["son55:S029"], NA),
        "expectation.E20": ("sol", "unmet", "CAPBench runs real third-party apps (e.g. Expedia flight search) and online-user tasks; evaluation date and app/content drift are not reported. son55's not_applicable used a generic template.", ["sol:E13"], NA),
        "expectation.E21": ("son55", "unmet", "Baselines use different observation spaces (text-only AutoDroid, XML+marks AppAgent, vision MobileAgent) and nothing is reported per setting.", ["son55:S014"], NA),
        "expectation.E25": ("sol", "partial", "CAPBench is a new benchmark; invalid instructions were removed by annotators and ambiguity is discussed for online users, but no refusal/infeasible behaviour is measured. son55's not_applicable used a generic template.", ["sol:E11"], NA),
        "expectation.E28": ("sol", "partial", "Test instructions are disjoint from the 350 memory-building ones, but apps/templates are shared and memory updates during test; no OOD report.", ["sol:E05"], NA),
        "expectation.E35": ("sol", "unmet", "No memory-on/off comparison is reported on any environment other than CAPBench; the absence of such a comparison is verifiable in the full text, so this is not an unknown fact.", ["sol:E05"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items M=3, X=2, E.causality=2, E.holdout=1, E.statistics=1, E.cost=2, claim_type system_method, evidence_level online, claim_support scoped were re-checked against the text: all stand; evidence_level carries a provisional note because the success adjudicator is unreported.",
    "claims_append": {"C1": (["agg:MS-A01", "agg:MS-A04"], "SR comparison uses an unreported success adjudicator and unequal budgets (20 steps x 3 tries per Staff agent vs 80 total)."),
                      "C2": (["agg:MS-A03"], "Ablation 'full' row Task Rate 0.81 vs Table 2 0.76 for the same GPT-4v system; configuration unstated.")},
    "status": ("accepted_final", "All 12 mechanical conflicts resolved from the fixed text and the fixed AWM reference; no scoring unknowns."),
    "expected_score": 50.0,
}

# --------------------------------------------------------------------------------------------- EcoAgent
EA = {
    "pk": "2505.05440",
    "prelim": ("Read before seat scores. GPT-4o cloud planner (Dual-ReACT: describe initial screenshot, plan steps each with an "
               "expected outcome) + device-side executor (ShowUI-2B or OS-Atlas-Pro-4B) + device-side observer (Qwen2-VL-2B) that "
               "checks each post-action screen against the expectation and returns 50-150-token text summaries; failure triggers "
               "memory/reflection replanning. AndroidWorld (116 tasks, programmatic checks), single run: 25.6/27.6% vs M3A 28.4, "
               "but Agent S2 54.3 and UGround-7B 44.0 (GPT-4o cloud/open-loop) are far higher, so 'matches fully cloud-based "
               "agents' holds only against M3A. Cloud calls/tokens, uplink kB and per-step latency are measured with device models "
               "on an RTX 3090; step caps are not stated; the initial screenshot is uploaded to the cloud. Cumulative ablation "
               "executor -> +planner -> +observer on two executors. Applicable: gui C10/C15/C17/C18; E02, E16, E17, E19, E21."),
    "materials": [("2505.05440", "paper")],
    "evidence": [
        A("EA-A01", "2505.05440", "Abstract", "Experiments on AndroidWorld demonstrate that EcoAgent matches the task success rates of fully cloud-based agents",
          "Central performance claim."),
        A("EA-A02", "2505.05440", "Table 1", "Agent S2 | Multi | GPT-4o * 4 | 54.3",
          "A fully cloud GPT-4o multi-agent baseline in the same table at 54.3 vs EcoAgent 27.6: the 'matches' claim holds only against M3A."),
        A("EA-A03", "2505.05440", "Table 7 (Dual-ReACT initial planning prompt)", "Based on this Android screenshot, please help me with: {instruction}",
          "The raw initial screenshot is sent to the cloud planner, so the privacy argument covers later steps only."),
        A("EA-A04", "2505.05440", "Appendix, Experimental Setup", "All device-side models are deployed on a local server with an NVIDIA RTX 3090 GPU (24G) to simulate mobile inference.",
          "Latency and device cost are surrogate measurements, not phone hardware."),
        A("EA-A05", "2505.05440", "Sec Metrics", "Latency refers to the average time taken for the agent to complete each execution step.",
          "Per-step latency, not per-task time; step counts per method are not reported."),
        A("EA-A06", "2505.05440", "Sec Evaluation on Operational Costs", "it still requires 6.5 × \\times more MC and 14 × \\times more MT than EcoAgent (OS-Atlas)",
          "Table 2 gives 12.21 vs 1.53 MC (about 8.0x), so the stated 6.5x does not follow from the table."),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "AndroidWorld programmatic checkers; single benchmark/platform, no held-out environment -> online, not transfer.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single AndroidWorld run: EcoAgent (GPT-4o planner + 2-4B device models) reaches 25.6/27.6% SR, close to M3A (28.4) but far below Agent S2 (54.3) and UGround-7B (44.0), while using about 1.5-1.9 cloud calls and 3.2-3.5K cloud tokens per task and 120 kB uplink; adding the observer/feedback loop raises SR on both executors (7.0->15.5->25.6; 4.3->19.0->27.6).",
        "not_supported": ["Matching fully cloud-based agents in general (Agent S2/UGround-7B much higher)", "Privacy protection (initial screenshot uploaded; no leakage measure)", "Real-phone latency/energy", "Separate contributions of Dual-ReACT vs ReACT and Pre-Understanding vs raw screenshots", "Observer reliability"],
        "unresolved": ["Step caps for EcoAgent and baselines", "Provenance/settings of baseline SR and cost numbers", "SR values (25.6, 7.0) not integer multiples of 1/116"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {"aggregate_neighbor_check": "No additional reference needed; both seats' neighbour reading (M3A/UGround open loop, V-Droid device-only, Agent S2 cloud) matches the fixed text.", "evidence_ids": ["agg:EA-A02"]},
    "rs": ("sol", "decompose_and_delegate with sub null: the step+expectation JSON is checked by an unvalidated 2B VLM observer, not routed to a sound solver/oracle as rs:C25 requires; the main card fits the cloud-plan/device-execute split."),
    "domain": [("sol", "agent_loop_context_control", "C17", None), ("sol", "agent_loop_context_control", "C18", None),
               ("son55", "planner_grounder_interface", "C10", None), ("son55", "agent_loop_context_control", "C15", "partial")],
    "domain_note": "Union: cloud manager plans subgoals for device workers (C17), post-action expectation check with feedback (C18), generalist planner vs specialist device grounder (C10), history compressed to text summaries (C15, partial: no fidelity/window ablation).",
    "expectations": {"E17": "son55", "E19": "son55", "E23": "sol"},
    "ratings": {
        "G": R("resolved", 2, "Latency/cost/privacy limits of cloud and open-loop systems are real and partly quantified, but the residual is weakened by device-only V-Droid (59.5, 3.0 s) and cloud Agent S2 (54.3), and the privacy gap is argued, not measured.",
               ["son55:C001", "son55:C002", "son55:C010", "son55:C011", "sol:E07"], ["agg:EA-A02"]),
        "M": R("resolved", 2, "Expectation-driven device-side checking with cloud escalation only on failure is a concrete mechanism, but its key assumptions are untested: a 2B general VLM judging 'screen meets expectation', text summaries sufficing for replanning, and summaries protecting privacy while the initial screenshot is uploaded. No distinguishing test against cloud-side verification.",
               ["son55:C003", "son55:C004", "son55:C006", "sol:E01"], ["agg:EA-A03", "son55:C005"]),
        "X": R("resolved", 3, "Algorithm, all four prompts (Tables 7-10), action space incl. DeleteText, model choices and the surrogate deployment are given, so the replanning loop and its stop condition are reconstructable. Missing: step caps, replan limits, handling of observer misjudgements, baseline settings.",
               ["son55:C003", "son55:C004", "son55:C033", "sol:E02"], ["son55:C031"]),
        "E.measurement": R("resolved", 3, "Primary SR comes from AndroidWorld programmatic checkers; cloud cost measured as calls/tokens/uplink. Deductions: latency per step on an RTX 3090, baseline number provenance unstated, some SR values not multiples of 1/116, privacy unmeasured.",
                           ["son55:C007", "son55:C016", "son55:C022", "sol:E04"], ["son55:C030", "son55:C031", "agg:EA-A04"]),
        "E.causality": R("resolved", 2, "Cumulative role-addition ablation on two executors supports the feedback package as a whole; Dual-ReACT vs plain ReACT, Pre-Understanding vs raw-screen upload and device- vs cloud-side verification are not isolated; baseline comparisons mix planners, executors and caps.",
                         ["son55:C019", "son55:C020", "son55:C021", "sol:E05"], ["son55:C031"]),
        "E.holdout": R("resolved", 1, "Single benchmark, no dev/test separation for prompts, no other benchmark or real device.", ["son55:C008", "sol:E04"], ["son55:C031"]),
        "E.statistics": R("resolved", 1, "Task denominator and a 20-task failure audit given; single run, no spread; 27.6 vs 28.4 is within known AndroidWorld run-to-run variation.",
                          ["son55:C025", "son55:C026"], ["son55:C030", "son55:C032"]),
        "E.cost": R("resolved", 2, "Cost is the central claim and is measured several ways (MC/MT, uplink kB, FLOPs, per-step latency), but budget fairness is not established: step caps are unstated for all methods, the cost table omits the strongest baselines (Agent S2, V-Droid), cost per success is not given, latency is per step on surrogate hardware, and a stated ratio (6.5x MC) does not follow from Table 2.",
                    ["son55:C015", "son55:C016", "son55:C017", "son55:C022", "sol:E06"], ["agg:EA-A04", "agg:EA-A05", "agg:EA-A06", "son55:C029"]),
    },
    "resolutions": {
        "rs.matches": ("sol", "decompose_and_delegate/null", "Same criterion as MobileSteward: the intermediate artifact is verified by an unvalidated small VLM, not a sound solver or oracle, so the singleton sub rs:C25 is not assigned.", ["son55:C004"], NA),
        "domain.matches": ("revised", "gui:C17 + gui:C18 + gui:C10 + gui:C15(partial)", "All four describe distinct operations present in the text (manager/worker split, expectation check with feedback, planner/grounder split, text history compression). IDs normalised to gui:.", ["son55:C003", "son55:C006", "sol:E01", "sol:E02"], NA),
        "rating.M": ("son55", {"status": "resolved", "rating": 2}, "The mechanism is concrete, but each load-bearing assumption (small-VLM verification accuracy, summary sufficiency, privacy) is untested, and the Table 7 prompt shows the initial screenshot is uploaded. sol's 3 credited the logic without these deductions.", ["agg:EA-A03", "son55:C005", "son55:C031"], "-6.25 vs sol (M weight 25 x 1/4)"),
        "rating.X": ("son55", {"status": "resolved", "rating": 3}, "All prompts and the action space are in the appendix, making the closed loop reconstructable; sol's deductions (observer validation, device conditions) belong to M/E, not to execution completeness. Missing step caps keep it below 4.", ["son55:C033", "son55:C004"], "+5.0 vs sol (X weight 20 x 1/4)"),
        "rating.E.cost": ("sol", {"status": "resolved", "rating": 2}, "E.cost covers budget fairness as well as cost: step caps are unstated, the strongest baselines are absent from the cost table, latency is per step on an RTX 3090, and the 6.5x MC claim does not match Table 2 (about 8.0x). son55 listed these but kept 3.", ["agg:EA-A04", "agg:EA-A05", "agg:EA-A06"], "-1.25 vs son55 (weight 5 x 1/4)"),
        "expectation.E17": ("son55", "unmet", "No numeric step cap is stated for EcoAgent or any baseline; 'Max Steps' appears only as a failure category in the 20-task sample.", ["son55:C031"], NA),
        "expectation.E19": ("son55", "partial", "AndroidWorld is run with a changed action set (new DeleteText) and Pixel 6/API 33 disclosed; no validation that the change leaves checker outcomes comparable.", ["son55:C033"], NA),
        "expectation.E23": ("sol", "partial", "The paper claims robustness on complex tasks, so E23 applies; a 20-task failure-cause audit exists, but no difficulty/step-length stratification.", ["son55:C025"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items G=2, E.measurement=3, E.causality=2, E.holdout=1, E.statistics=1, claim_type system_method, evidence_level online, claim_support scoped were re-checked: all stand. Both seats correctly scope the 'matches cloud agents' claim to M3A only.",
    "claims_append": {"C1": (["agg:EA-A02", "agg:EA-A06"], "Agent S2 (54.3) and UGround-7B (44.0) are higher; the stated 6.5x MC ratio vs UGround does not follow from Table 2 (12.21/1.53)."),
                      "C4": (["agg:EA-A03"], "The initial screenshot is uploaded to the cloud planner (Table 7 prompt).")},
    "status": ("accepted_final", "All 8 mechanical conflicts resolved from the fixed text; no scoring unknowns."),
    "expected_score": 53.75,
}

# --------------------------------------------------------------------------------------------- MONDAY
MD = {
    "pk": "2505.12632",
    "prelim": ("Read before seat scores. MONDAY mines 20K YouTube mobile how-to videos (iOS/Android) into 313K annotated frames: "
               "GroundingDINO phone isolation, OCR-based scene transitions (F1 95.04), GroundingDINO+OCR element boxes (hit ratio "
               "99.87, a lenient 'any box contains the target' bound), and a 3-step GPT-4o action identifier using neighbouring frames "
               "and narration (80.9% all / 91.8% touch on 100 human-annotated videos; 80.4% human-judged accuracy on training "
               "samples). Downstream: SeeClick and Llama-3.2 get an extra LoRA stage on MONDAY, then AitW or AMEX fine-tuning; "
               "offline action matching on AitW/AMEX/MONDAY and a 50-video Windows Mobile set (unseen OS). Gains on Windows Mobile "
               "are 12-23 points, but there is no equal-data/compute control, no platform ablation, single runs, and the abstract's "
               "18.11 average does not equal the table's 17.99. The paper's contribution is a training-data resource, so "
               "component_training applies. Applicable: gui R03 (C02 on the annotator side); E15, E26, E27, E28."),
    "materials": [("2505.12632", "paper")],
    "evidence": [
        A("MD-A01", "2505.12632", "Appendix D", "Using our scene transition detection output, annotators labeled actions between consecutive scenes",
          "Action ground truth is conditioned on the pipeline's own segmentation, so action accuracy is not fully independent of the method."),
        A("MD-A02", "2505.12632", "Sec 4.2.1", "To ensure a fair comparison, all models are further finetuned using LoRA on either the AitW or AMEX dataset for an equal number of epochs",
          "Fairness is matched only in the downstream fine-tune; MONDAY variants receive an extra training stage with no equal-size alternative-data arm."),
        A("MD-A03", "2505.12632", "Abstract", "achieving an average performance gain of 18.11%p",
          "Table 5 Windows Mobile gains are 13.17, 12.20, 23.41, 23.17 (mean 17.99), not 18.11."),
        A("MD-A04", "2505.12632", "Appendix H.1", "AgentTrek [ 50 ] simulates actions in a virtual environment based on tutorial text",
          "The tutorial-to-trajectory neighbour is discussed (appendix), so lineage is acknowledged, though not compared experimentally."),
        A("MD-A05", "2505.12632", "Appendix F", "Workers found that 80.40% of 250 sampled actions were accurate",
          "About one in five training labels is wrong and no label-confidence filter is applied."),
    ],
    "assessment": {
        "evidence_level": "offline",
        "evidence_level_note": "All downstream results are offline action matching; the unseen-platform set is offline and human-annotated.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported: the pipeline labels actions at 80.9% (touch 91.8%) on 100 human-annotated videos at about $0.34/video, and an extra LoRA stage on MONDAY raises offline action-matching accuracy of SeeClick and Llama-3.2 on an unseen Windows Mobile set by 12-23 points (mean 17.99, single runs), without an equal-data control.",
        "not_supported": ["Online task-success gains", "Attribution to cross-platform diversity rather than extra data/training", "Superiority over equal amounts of other data", "'Consistently' better on all test sets (SeeClick AMEX column regresses)"],
        "unresolved": ["GPT-4o prompts not provided", "Code release pending"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {"aggregate_neighbor_check": "AgentTrek (fixed reference) is discussed in Appendix H.1 (agg:MD-A04); Video2Action and Chen et al. are compared at dataset level (Table 1) though not run. Gap lineage is reasonably bounded; the stake (real-world diversity improves generalization) is tested offline only.", "evidence_ids": ["agg:MD-A04", "son55:M034"]},
    "rs": ("son55", "Both seats assign self_supervised_signal_engineering / rs:C08 partial (inverse artifact->specification mapping with a weak quality gate); kept."),
    "domain": [("son55", "mine_human_screen_videos", "R03", None), ("son55", "structured_screen_observation", "C02", "partial")],
    "domain_note": "Union: R03 is the core operation; C02 (pixels -> indexed element list via detector+OCR) is used on the annotator side, not as agent observation (partial). son55's circularity warning on R03 (card derived from this paper) is kept.",
    "expectations": {"E02": "son55", "E05": {"applicable": False, "status": "not_applicable", "reason": "No screenshot-to-coordinate grounding claim; touch accuracy is part of offline navigation action matching."},
                     "E06": {"applicable": False, "status": "not_applicable", "reason": "No claim that MONDAY yields a better grounder than prior grounders."},
                     "E24": "sol", "E26": "son55"},
    "ratings": {
        "G": R("resolved", 3, "Concrete bottleneck (manual annotation cost, obsolescence, missing iOS/configuration diversity) with dataset-level lineage (Table 1: RICO, AitW, Video2Action, Chen et al.) and the tutorial-replay neighbour discussed in the appendix; residual (automated multi-platform real-video extraction at scale) is bounded. Nearest video methods are not run (no code), keeping it below 4.",
               ["son55:M001", "son55:M002", "son55:M003", "sol:E01", "agg:MD-A04"]),
        "M": R("resolved", 3, "OCR text is more OS/theme-stable than pixels, SoM boxes offset VLM localisation error, narration+neighbour frames+zoom disambiguate, each with an ablation; the unaddressed ~20% label noise and the assumption that offline matching reflects navigation ability keep it at 3.",
               ["son55:M006", "son55:M007", "son55:M008", "son55:M015", "sol:E05"], ["agg:MD-A05"]),
        "X": R("resolved", 3, "Filtering funnel, OCR/transition thresholds, detection heuristics, zones, training hyper-parameters and the unified action space are given; GPT-4o prompts and code are not released and there is no label-confidence gate.",
               ["son55:M004", "son55:M006", "sol:E09", "sol:E10"], ["son55:M032", "son55:M036"]),
        "E.measurement": R("resolved", 2, "Pipeline metrics use dual human annotation with adjudication (3.93% disagreement), but action labels are built on the pipeline's own scene segmentation, ambiguous cases are excluded, the hit ratio is a lenient bound, and the downstream metric is offline exact matching restricted to shared action types (78-94% of actions).",
                           ["son55:M009", "son55:M013", "son55:M019", "sol:E03", "sol:E04"], ["agg:MD-A01", "son55:M011"]),
        "E.causality": R("resolved", 2, "Pipeline ablations (1/2/3-step, narration, single image) are clean, and the with/without-MONDAY comparison holds on two backbones and two fine-tune sets; but no equal-size alternative-data or equal-compute arm and no platform ablation, so attributing gains to cross-platform diversity rather than extra data/training is open.",
                         ["son55:M014", "son55:M015", "son55:M016", "sol:E07", "sol:E08"], ["agg:MD-A02", "son55:M018"]),
        "E.holdout": R("resolved", 2, "Windows Mobile is a genuinely unseen platform, human-annotated independently of the pipeline; video-level splits; decontamination only by 30-character title overlap; offline only.",
                       ["son55:M021", "sol:E11"], ["son55:M033"]),
        "E.statistics": R("resolved", 1, "Test sizes and annotator disagreement reported; all downstream results single-run without intervals; abstract average 18.11 vs table 17.99; the AMEX regression is not discussed.",
                          ["son55:M009", "son55:M017", "son55:M021"], ["agg:MD-A03", "son55:M027", "son55:M029"]),
        "E.cost": R("resolved", 2, "Collection cost ($6,976 total, $0.34/video vs $5.76 manual) and preprocessing time are reported, but training compute is given only in epochs and the MONDAY arm's extra training stage is not budget-matched against any alternative.",
                    ["son55:M030", "son55:M031", "sol:E17"], ["agg:MD-A02"]),
    },
    "resolutions": {
        "claim_type": ("son55", "component_training", "The central empirical claim is that adding MONDAY to pre-training improves agents' cross-platform generalization; the corpus and collection framework are training resources. The 100-video test set is a by-product used to validate the pipeline, not a benchmark claim. The type changes how G/M/X/E are read, not the item scale.", ["son55:M001", "sol:E01"], "none directly; ratings read under component_training"),
        "domain.matches": ("revised", "gui:R03 + gui:C02(partial)", "R03 in both seats; son55's C02 names a real annotator-side operation (detector+OCR element list). IDs normalised to gui:.", ["son55:M013"], NA),
        "rating.G": ("son55", {"status": "resolved", "rating": 3}, "The gap is concrete and its lineage is laid out in Table 1 and Appendix H (incl. AgentTrek); the residual is bounded. sol's 2 rested on the unavailability of earlier video methods, which limits experimental comparison (an E issue) more than gap identification.", ["agg:MD-A04", "son55:M002"], "+3.75 vs sol"),
        "rating.E.measurement": ("son55", {"status": "resolved", "rating": 2}, "The action ground truth is conditioned on the pipeline's own scene segmentation and the downstream metric covers only shared action types offline; these coverage limits sit at anchor 2. sol's 3 credited the human audit without these deductions.", ["agg:MD-A01", "son55:M019"], "-2.5 vs sol"),
        "rating.E.causality": ("sol", {"status": "resolved", "rating": 2}, "Pipeline-design claims are causally supported by clean ablations and the with/without comparison is consistent across 2x2 settings; the missing equal-data arm limits the diversity attribution but leaves 'relevant results with a key control missing' (anchor 2), not 1.", ["son55:M015", "son55:M016", "agg:MD-A02"], "+2.5 vs son55"),
        "rating.E.cost": ("sol", {"status": "resolved", "rating": 2}, "Collection cost is clearly reported, but E.cost also covers budget fairness: the MONDAY arm's extra training stage is not matched and training compute is reported only as epochs. son55's 3 credited reporting only.", ["agg:MD-A02", "son55:M030"], "-1.25 vs son55"),
        "expectation.E02": ("son55", "unmet", "The paper claims better mobile navigation agents and cross-platform generalization; only offline action matching is reported (no AndroidWorld). Consistent with both seats' E15=unmet.", ["son55:M036"], NA),
        "expectation.E05": ("son55", "not_applicable", "Value from son55, rationale replaced: MONDAY makes no screenshot-to-coordinate grounding claim.", [], NA),
        "expectation.E06": ("son55", "not_applicable", "Value from son55, rationale replaced: no claim that MONDAY beats prior grounders.", [], NA),
        "expectation.E24": ("sol", "partial", "The paper claims robustness to themes, dark mode, configurations and unseen platforms; the Windows Mobile test is evidence of layout generalization but not a controlled matched-pair perturbation test. son55's not_applicable used a generic template.", ["sol:E11"], NA),
        "expectation.E26": ("son55", "unmet", "MONDAY is a reverse (video->labels) synthesis recipe claimed to give better training data; no instruction-first or equal-size alternative is compared.", ["son55:M018"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items M=3, X=3, E.holdout=2, E.statistics=1, evidence_level offline, claim_support scoped, rs C08 partial were re-checked: all stand. The 18.11 vs 17.99 arithmetic was verified from Table 5.",
    "claims_append": {"C2": (["agg:MD-A03", "agg:MD-A02"], "Table 5 Windows Mobile gains average 17.99, not 18.11; no equal-data control.")},
    "status": ("accepted_final", "All 11 mechanical conflicts resolved from the fixed text; no scoring unknowns."),
    "expected_score": 63.75,
}

# --------------------------------------------------------------------------------------------- GUIrilla
GR = {
    "pk": "2510.16051",
    "prelim": ("Read before seat scores. GUIrilla crawls 12,298 macOS apps through the Accessibility API (handlers for pop-ups, "
               "invisible/empty elements, menus; optional GPT-4 input/order/login/task agents), yielding MacApp Trees for 1,108 apps "
               "and 27,171 single-step click/type tasks on about 4.2K screens; app-disjoint split (881/227 apps). Trained grounders "
               "(Florence-0.7B, Qwen2.5-VL-3B/7B) improve on the in-house app-disjoint test and on ScreenSpot-v2/Pro "
               "(7B: 87.5->94.73, 27.13->35.36). Problems: A.3 'Prompts' section is empty; Gold count stated as 1,283 vs 1,319 "
               "audited vs 1,565 test tasks; leakage adjustment 90.41->90.33 matches no Table 6 value; 'agentic' Table 8 is single-step "
               "accuracy; handler ablation on 3 apps; no data-scaling curve or equal-size alternative corpus. The paper calls itself a "
               "data crawler whose output trains downstream models, so component_training applies. Applicable: gui K14/K23/C01; "
               "E05, E06, E26, E27, E28."),
    "materials": [("2510.16051", "paper")],
    "evidence": [
        A("GR-A01", "2510.16051", "Appendix A.3 heading", "### A.3 Prompts\n\n### A.4 Training Setup",
          "The prompts section is empty in the fixed text; GPT-agent behaviour cannot be reproduced exactly."),
        A("GR-A02", "2510.16051", "Sec 1 contributions", "GUIrilla-Gold (1,283 human-verified tasks)", "Gold size as stated in the contributions."),
        A("GR-A03", "2510.16051", "Appendix A.9.1", "From the 1319 original English language-based tasks",
          "A different audited count; 84.3% of 1,319 doable is about 1,112, matching neither 1,283 nor the 1,565-task test split."),
        A("GR-A04", "2510.16051", "Appendix A.1", "applications with 1,565", "Test split size (1,565 tasks over 227 apps)."),
        A("GR-A05", "2510.16051", "Appendix A.5.1", "from 90.41% -> 90.33%",
          "Leakage-adjusted ScreenSpot-v2 score; Table 6 reports 94.73% (7B) and 89.54% (3B), neither 90.41 nor 90.33."),
        A("GR-A06", "2510.16051", "Table 6", "| 4.2K | 94.73%", "GUIrilla-See-7B ScreenSpot-v2 accuracy as tabulated."),
        A("GR-A07", "2510.16051", "Sec 1", "GUIrilla remains a data crawler whose output is intended to train and stabilize downstream models",
          "Self-description supporting the component_training type."),
    ],
    "assessment": {
        "evidence_level": "offline",
        "evidence_level_note": "Static grounding and single-step action accuracy only; ScreenSpot is external but offline.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported: LoRA fine-tuning on about 4.2K macOS screens / 25.6K crawler-derived tasks raises Qwen2.5-VL-3B/7B grounding on an app-disjoint macOS test and on ScreenSpot-v2/Pro by roughly 7-8 points (7B: 94.73 / 35.36), and functional task descriptions train better than raw AX labels (Florence 53.55 vs 40.35); the crawler can run without GPT.",
        "not_supported": ["Desktop agent / online task success ('agentic' Table 8 is single-step accuracy)", "Exploration coverage or quality", "Data-efficiency superiority over OS-Atlas under matched conditions (A.7 has no table)", "Leakage-adjusted ScreenSpot-v2 figure (does not reconcile)"],
        "unresolved": ["A.3 prompts missing", "Gold count 1,283 vs 1,319 vs 1,565", "90.41->90.33 vs Table 6"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {"aggregate_neighbor_check": "No further reference needed; both seats bound the residual against OS-Atlas (AX-based macOS collection exists; son55 notes the 'crawler not released' contrast conflicts with OS-Atlas's own account).", "evidence_ids": ["son55:U003", "son55:U004"]},
    "rs": ("son55", "self_supervised_signal_engineering / rs:C08 partial: crawler + functional relabelling is an inverse artifact->specification mapper producing training instances, with the weak gate and missing cheap baseline recorded as failure checks. Consistent with both seats' treatment of MONDAY."),
    "domain": [("sol", "exploration_driven_task_synthesis", "K14", None), ("son55", "planner_grounder_interface", "K23", None),
               ("son55", "structured_screen_observation", "C01", "partial")],
    "domain_note": "Union: retroactive instruction labelling of explored edges (K14), grounding data synthesised from rendered AX structure (K23), crawler acting over enumerated AX elements (C01, partial: the trained model itself is screenshot-only).",
    "expectations": {"E15": "son55", "E22": "sol", "E24": "sol", "E25": "son55", "E28": "son55"},
    "ratings": {
        "G": R("resolved", 2, "macOS data scarcity and non-scalable manual annotation are real, but OS-Atlas already automates AX-based macOS collection and the 'crawler not released' contrast is disputed; the residual (handlers, functional labels, full-desktop trees) is only partly measured.",
               ["sol:E08", "sol:E23", "son55:U002", "son55:U003", "son55:U005"]),
        "M": R("resolved", 3, "Handlers and functional relabelling respond directly to observed AX failures and give distinguishable, tested predictions (handler vs random crawler; functional vs AX-label supervision 53.55 vs 40.35). Weak points: 80%-accurate boxes as training targets and single-step tasks framed toward desktop automation.",
               ["sol:E02", "sol:E05", "sol:E10", "son55:U027"], ["son55:U012", "son55:U013", "son55:U016"]),
        "X": R("resolved", 2, "Crawler modules, parameters, tree schema, split and training settings are described; the GPT-agent prompts are absent (A.3 empty), the random-crawler baseline is undefined, retry/stop rules and collection cost are missing, and Gold counts are inconsistent.",
               ["son55:U006", "son55:U007", "son55:U011", "sol:E07"], ["agg:GR-A01", "agg:GR-A02", "agg:GR-A03"]),
        "E.measurement": R("resolved", 2, "External ScreenSpot-v2/Pro use human labels and clear point-in-box judging; the in-house test uses AX boxes (80% accurate) and GPT task strings, Table 8 'Success Rate' is single-step accuracy, and the leakage-adjusted figure does not reconcile with Table 6.",
                           ["son55:U013", "son55:U014", "son55:U019", "sol:E14"], ["agg:GR-A05", "agg:GR-A06", "son55:U023"]),
        "E.causality": R("resolved", 2, "Clean base-vs-tuned controls on the same backbones and two small ablations; data-efficiency claims vs OS-Atlas/UGround mix backbone, data and recipe, and A.7's same-backbone claim has no table.",
                         ["son55:U017", "son55:U018", "son55:U019", "sol:E10"], ["son55:U020", "son55:U026"]),
        "E.holdout": R("resolved", 3, "App-disjoint 881/227 split with harder test apps, external ScreenSpot benchmarks and a manual overlap audit (OneNote/Excel disclosed); the adjusted score does not reconcile and everything is offline.",
                       ["son55:U011", "son55:U022", "sol:E12"], ["agg:GR-A05"]),
        "E.statistics": R("resolved", 2, "Denominators given; three stochastic-decoding runs with SD (inference noise, not training seeds); handler ablation on 3 apps single-run; Gold denominators inconsistent.",
                          ["son55:U029", "son55:U030", "sol:E16"], ["agg:GR-A03"]),
        "E.cost": R("resolved", 2, "Collection hardware, parallelism, training hours and GPUs are reported; GPT-4 API cost, total crawl time and any cost comparison with manual annotation or OS-Atlas are missing.",
                    ["son55:U031", "sol:E08", "sol:E13"]),
    },
    "resolutions": {
        "claim_type": ("son55", "component_training", "The paper calls GUIrilla a data crawler whose output trains downstream models (agg:GR-A07) and its main evidence is training grounders and testing transfer; GUIrilla-Gold is a secondary evaluation artifact.", ["agg:GR-A07", "son55:U019"], "none directly; ratings read under component_training"),
        "rs.matches": ("son55", "self_supervised_signal_engineering/rs:C08 (partial)", "Explored edges -> GPT functional task strings is an inverse artifact->specification mapping producing new training instances (C08 step 2); the weak gate and missing cheap baseline are recorded as failure checks, the same treatment both seats gave MONDAY.", ["son55:U006", "son55:U019"], NA),
        "domain.matches": ("revised", "gui:K14 + gui:K23 + gui:C01(partial)", "son55's K23 (grounding data from rendered UI structure) is the closest fit for the training data itself; K14 and C01 describe the crawl/relabel and AX-action operations. IDs normalised to gui:.", ["son55:U010", "sol:E05"], NA),
        "rating.M": ("sol", {"status": "resolved", "rating": 3}, "The method makes two distinguishing predictions that are tested (handlers vs random crawl; functional vs AX-label supervision). son55's deductions about long-horizon framing and exploration-quality measurement concern claim scope and evidence (E items), not whether the operation fits the stated data bottleneck.", ["sol:E10", "son55:U027"], "+6.25 vs son55"),
        "expectation.E15": ("son55", "partial", "The authors mostly confine claims to grounding/understanding, but Table 8 is labelled 'agentic Success Rate' while being single-step accuracy, inviting an agent-capability reading.", ["son55:U023"], NA),
        "expectation.E22": ("sol", "partial", "Results cover 0.7B, 3B and 7B but stop at 7B; E22 asks for larger backbones (32B/72B) because gains shrink with size.", ["sol:E10"], NA),
        "expectation.E24": ("sol", "partial", "Cross-OS transfer (Windows subset of ScreenSpot-Pro) is claimed, which is a layout-generalization claim; no controlled perturbation pairs. son55's not_applicable missed the cross-OS claim.", ["sol:E14"], NA),
        "expectation.E25": ("son55", "unmet", "About 15.7% of audited test tasks are NOT DOABLE, but no model refusal/infeasible behaviour is reported; labelling infeasible tasks in the audit does not meet the requirement.", ["son55:U014"], NA),
        "expectation.E28": ("son55", "met", "Exploration apps and evaluation apps are disjoint, external OOD benchmarks are reported, and overlap is audited; the unreconciled adjusted score is recorded under E.holdout/E.measurement.", ["son55:U011", "son55:U022"], NA),
    },
    "shared": [],
    "agreed_review": "Agreed items G=2, X=2, E.measurement=2, E.causality=2, E.holdout=3, E.statistics=2, E.cost=2, evidence_level offline, claim_support scoped were re-checked; the three known reporting inconsistencies (A.3, Gold counts, leakage figure) are confirmed and already deducted.",
    "claims_append": {"C1": (["agg:GR-A05", "agg:GR-A06"], "Leakage-adjusted SS-v2 90.41->90.33 matches no Table 6 entry.")},
    "status": ("accepted_final", "All 9 mechanical conflicts resolved from the fixed text; no scoring unknowns."),
    "expected_score": 58.75,
}

# --------------------------------------------------------------------------------------------- ClawGUI
CLAW = {
    "pk": "2604.11784",
    "prelim": ("Read before seat scores, then checked against the frozen MAI-UI reference (2512.22047). ClawGUI bundles (i) an "
               "online-RL harness on MobileWorld Docker emulators (reset, root-level + MLLM-judge outcome reward, spare-server rotation) "
               "with a Qwen3.5-72B PRM step reward and GiGPO, (ii) a three-stage grounding-evaluation harness (46/48 official cells "
               "within a one-sided 2-point rule), and (iii) a deployment agent (hybrid CLI/GUI, memory) with no evaluation. ClawGUI-2B "
               "(from MAI-UI-2B) reaches 17.1% on 117 MobileWorld GUI-only tasks vs 11.1%; GRPO-binary 14.5 vs GiGPO-dense 17.1 changes "
               "estimator and reward together; single runs; training-task source and overlap with the 117 test tasks are not reported; "
               "real-device training is called 'validated' with no result. MAI-UI shows the neighbour already has a containerised "
               "environment manager with failover and a hybrid rule/MLLM verifier with 83% human agreement, trained only in virtual "
               "environments on the same app family as MobileWorld; its own MobileWorld table (116 tasks) lists MAI-UI-8B at 27.5 and no "
               "MAI-UI-2B, while ClawGUI's Table 1 copies the other rows verbatim but gives MAI-UI-8B 19.7 and MAI-UI-2B 11.1. "
               "Applicable: gui K19, C26, trajectory_level_policy_training; E09, E10, E12, E13, E16, E28."),
    "materials": [("2604.11784", "paper"), ("2512.22047", "nearest_neighbor_reference")],
    "evidence": [
        A("CG-A01", "2512.22047", "MAI-UI Sec 2.3.3", "we introduce a centralized Environment Manager that coordinates container instances across multiple physical machines",
          "The base model's own RL stack already has a containerised environment manager (reuse, cross-machine orchestration, fault tolerance).", "reviewer_comment"),
        A("CG-A02", "2512.22047", "MAI-UI Sec 2.3.3", "maintaining backup sessions for seamless failover and replacement",
          "Failover/replacement sessions already exist in the neighbour, the counterpart of ClawGUI's spare-server rotation.", "reviewer_comment"),
        A("CG-A03", "2512.22047", "MAI-UI Sec 2.3.3", "This hybrid approach achieves 83% agreement with human annotations",
          "The neighbour validates its rule+MLLM verifier against humans; ClawGUI reports no such validation for its MLLM judge or PRM.", "reviewer_comment"),
        A("CG-A04", "2512.22047", "MAI-UI Sec 2.3.3", "This constraint motivates our use of virtualized environments rather than physical devices.",
          "Physical-device training is genuinely absent in the neighbour, so ClawGUI's residual includes it, but ClawGUI reports no physical-device result.", "reviewer_comment"),
        A("CG-A05", "2512.22047", "MAI-UI Table (MobileWorld), Ours rows", "Ours MAI-UI-8B 27.5 22.2 20.0 24.9",
          "Official MAI-UI-8B GUI-only SR is 27.5; ClawGUI lists 19.7. No MAI-UI-2B row exists in the official table.", "author_report"),
        A("CG-A06", "2512.22047", "MAI-UI Table (MobileWorld) header", "GUI-Only (116)",
          "Official GUI-only denominator is 116 tasks; ClawGUI states 117.", "author_report"),
        A("CG-A07", "2604.11784", "Table 1", "MAI-UI-8B | 19.7", "ClawGUI's MAI-UI-8B value, 7.8 points below the official one."),
        A("CG-A08", "2604.11784", "Table 1", "MAI-UI-2B | 11.1", "Same-scale comparator; absent from the official table, so evaluated by ClawGUI under unstated settings."),
        A("CG-A09", "2604.11784", "Table 1 caption", "Table 1 : Comparison of models on GUI-Only (117 tasks) benchmark.",
          "117 tasks, while all non-MAI-UI rows are identical to MAI-UI's 116-task table, i.e. mixed provenance and denominators."),
        A("CG-A10", "2512.22047", "MAI-UI Sec 2.3.3",
          "we integrated over 35 applications, encompassing system utilities and open-source software such as Mattermost (enterprise communication), Mastodon (social media), and Mall4Uni (e-commerce)",
          "The base model was already RL-trained on the MobileWorld app family, so the starting point is in-distribution for the test apps.", "reviewer_comment"),
        A("CG-A11", "2604.11784", "Sec 3.2.1", "ClawGUI-RL launches dozens of Docker-based Android emulators in parallel via MobileWorld",
          "Training environment = evaluation environment; training-task source/overlap never reported."),
        A("CG-A12", "2604.11784", "Sec 4.2", "Both models share the same base weights; the gain stems entirely from ClawGUI-RL’s scalable environment management and reward design.",
          "Attribution claim not supported by any infrastructure-isolating control."),
        A("CG-A13", "2604.11784", "Table 2", "GiGPO | Dense (episode- & step-level) | 17.1",
          "The only ablation changes estimator (GRPO->GiGPO) and reward type together."),
        A("CG-A14", "2604.11784", "Sec 2.2", "none of these works open-source their training infrastructure",
          "Author gap statement; consistent with MAI-UI, which states model release but no infrastructure release."),
        A("CG-A15", "2604.11784", "Sec 1 contributions",
          "We release ClawGUI-RL , the first open-source GUI agent RL infrastructure with validated support for both large-scale parallel virtual environments and real physical devices",
          "'Validated' physical-device support has no reported experiment."),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_note": "RL claim: MobileWorld interactive benchmark, but training runs in the same MobileWorld environment and the base model was trained on the same app family -> at most online. Eval-harness claim: offline static reproduction. Deployment/real-device: no evidence.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single run: after GiGPO+PRM training inside MobileWorld emulators, ClawGUI-2B solves 17.1% of 117 GUI-only tasks vs 11.1% for its MAI-UI-2B starting point as evaluated by the authors (about 20 vs 13 tasks), and the GiGPO-dense arm beats a GRPO-binary arm by 3 tasks; the evaluation harness matches 46/48 official grounding cells under a one-sided 2-point rule.",
        "not_supported": ["Gain caused by environment management/infrastructure", "PRM effectiveness or reliability", "Validated physical-device training", "Deployment/memory benefit", "Train/test task disjointness", "Like-for-like comparison with copied Table 1 rows (116 vs 117 tasks; MAI-UI-8B 19.7 vs official 27.5)"],
        "unresolved": ["Evaluation settings used for the MAI-UI-2B/8B re-runs", "Whether per-model eval configs were tuned toward official numbers"],
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "MAI-UI (2512.22047), the base model and closest neighbour, already runs online RL in a containerised Android environment with a centralised environment manager, failover sessions and a hybrid rule/MLLM verifier validated at 83% human agreement, trained only on virtual devices and with no stated infrastructure release. ClawGUI's residual is therefore open release + physical-device support + step-level credit assignment, not environment management as such; ClawGUI does not acknowledge the overlap, and the physical-device part has no result.",
        "closest_adjacent_aggregate": {"name": "MAI-UI", "version": "2512.22047 (fixed reference, sha256 c134dac5...)", "relationship": "base weights and nearest RL-infrastructure neighbour"},
        "evidence_ids": ["agg:CG-A01", "agg:CG-A02", "agg:CG-A03", "agg:CG-A04", "agg:CG-A14"],
    },
    "rs": ("son55", "self_supervised_signal_engineering / rs:C26 partial (both seats) plus son55's supporting controlled_diagnostic_design/null for the distinct evaluation-harness operation (pin confounding eval choices, anchor to official numbers), recorded as weak because the instrument is never varied."),
    "domain": [("sol", "learned_outcome_and_process_judges", "K19", None), ("sol", "online_evaluation_methodology", "C26", None),
               ("son55", "trajectory_level_policy_training", None, "weak")],
    "domain_note": "Union: zero-shot PRM step reward (K19), single-step click-in-box evaluation harness (C26), online RL training of the policy (trajectory_level_policy_training, no sub: K20 needs value baselines/filtered replay).",
    "expectations": {"E12": "sol", "E13": "son55", "E21": "son55", "E22": "sol", "E25": "sol", "E28": "son55"},
    "ratings": {
        "G": R("resolved", 2, "Concrete bottlenecks (environment instability, sparse reward, eval drift, no open RL stack) with a now-checkable nearest neighbour: MAI-UI already has the container environment manager, failover and a human-validated hybrid verifier but trains only on virtual devices and releases no infrastructure. The residual (open release, physical devices, step-level credit) is real but narrower than claimed and the overlap is not acknowledged; eval-drift existence is shown only indirectly -> 2.",
               ["son55:E001", "son55:E002", "son55:E020", "agg:CG-A01", "agg:CG-A02", "agg:CG-A03", "agg:CG-A04", "agg:CG-A14"]),
        "M": R("resolved", 2, "Mechanisms are concrete (unified device interface, spare-server rotation, PRM step score, GiGPO anchor grouping, pinned eval configs), but PRM prompt/scale/combination details are thin, 'dense reward' and the GiGPO estimator are conflated, and real-device reward relies on an unvalidated MLLM judge; no distinguishing prediction against a plain RL-in-MobileWorld baseline.",
               ["son55:E004", "son55:E005", "son55:E007", "son55:E016", "son55:E017", "sol:E02"], ["son55:E019"]),
        "X": R("resolved", 2, "Environment lifecycle, training hyper-parameters and the eval pipeline are described; PRM I/O and reward combination, training task set (source, size, overlap), real-device task set, CLI/GUI routing and memory write/evict rules are missing.",
               ["son55:E004", "son55:E009", "son55:E022", "sol:E03"], ["son55:E033"]),
        "E.measurement": R("resolved", 2, "MobileWorld SR uses the benchmark's privileged checks and the grounding judges are explicit, but Table 1 mixes rows copied from MAI-UI's 116-task table with authors' re-runs on 117 tasks (MAI-UI-8B 19.7 vs official 27.5), the reward-side MLLM judge/PRM is unvalidated, and the reproduction rule counts any overshoot as success.",
                           ["son55:E006", "son55:E011", "son55:E023", "sol:E08"], ["agg:CG-A05", "agg:CG-A06", "agg:CG-A07", "agg:CG-A08", "agg:CG-A09", "son55:E033"]),
        "E.causality": R("resolved", 1, "Only GRPO-binary vs GiGPO-dense (+3 tasks), which changes estimator and reward together; no PRM on/off, no environment-manager ablation, no same-base continued-training control, yet the gain is attributed 'entirely' to infrastructure and reward design; the 11.1 comparator was evaluated under unstated settings.",
                         ["son55:E016", "son55:E017", "agg:CG-A13", "sol:E06"], ["agg:CG-A12", "agg:CG-A08", "son55:E018"]),
        "E.holdout": R("not_reported", 0, "After the full text was checked, training-task source, count and disjointness from the 117 test tasks are not reported; training and evaluation share the MobileWorld environment, and the MAI-UI-2B base was itself RL-trained on the same app family. No cross-benchmark, unseen-app or real-device test.",
                       ["agg:CG-A11", "agg:CG-A10"], [],
                       ["research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2604.11784.txt: entire fixed text (no appendix exists): Sec 3.2.1 Task Reset/Task Source, Sec 4.1 Training/Evaluation, Tables 1-2",
                        "research/fulltext/review-runs/gui-v22-20261021-01/fulltext/2512.22047.txt: Sec 2.3.3 and 2.5 (base-model RL environment and MobileWorld)"]),
        "E.statistics": R("resolved", 1, "Denominators are given (117 tasks; 48 reproduction cells) but online results are single runs without spread; the +2.6 point ablation is about 3 tasks; no failure breakdown.",
                          ["son55:E011", "son55:E017", "son55:E024"], ["son55:E033"]),
        "E.cost": R("resolved", 1, "Training hardware and hyper-parameters (8xA6000, 64 environments) and a 50-step evaluation cap are given; no wall-clock, GPU-hours, 72B-PRM inference cost or baseline budget alignment.",
                    ["son55:E009", "son55:E010", "sol:E04"], ["son55:E033"]),
    },
    "resolutions": {
        "status": ("revised", "reviewed", "sol stopped at needs_evidence only because the MAI-UI neighbour was not yet in the frozen reference set. It is now frozen in references.json and was used as a shared fact check (see shared_error_corrections), which resolves G; son55's 'reviewed' had been reached without that neighbour. Final: reviewed, all eight items resolved.", ["agg:CG-A01", "agg:CG-A04"], "enables a score (raw 40.0)"),
        "rs.supporting": ("son55", ["controlled_diagnostic_design"], "The evaluation harness is a separate operation from the RL signal and partly matches controlled_diagnostic_design (named confounds pinned, external anchor) while failing its central step (the instrument is never varied); kept as weak supporting, no sub.", ["son55:E003", "son55:E022", "son55:E023"], NA),
        "rs.matches": ("son55", "self_supervised_signal_engineering/rs:C26 (partial) + controlled_diagnostic_design/null (weak)", "Primary identical in both seats; supporting entry as above.", ["son55:E007", "son55:E016"], NA),
        "domain.matches": ("revised", "gui:K19 + gui:C26 + trajectory_level_policy_training/null", "Three distinct operations: PRM step reward (K19, both), click-in-box evaluation harness (C26, sol), online policy RL (son55; K20 not assigned because GiGPO has no learned value baseline/filtered replay).", ["sol:E07", "son55:E009"], NA),
        "rating.G": ("revised", {"status": "resolved", "rating": 2}, "Not a choice between seats: the G unknown is resolved by the shared MAI-UI reference (see shared_error_corrections[0]). sol's unknown came from the missing neighbour; son55's 2 used UI-TARS-2 as closest neighbour without MAI-UI. With MAI-UI, environment management/failover/hybrid verification are prior art, the residual is open release + physical devices + step credit -> 2 on new grounds.", ["agg:CG-A01", "agg:CG-A02", "agg:CG-A03", "agg:CG-A04"], "unknown -> 2 (G contributes 7.5); score becomes computable"),
        "rating.M": ("son55", {"status": "resolved", "rating": 2}, "PRM design detail is thin, dense reward and estimator are conflated in the only ablation, and the real-device reward is an unvalidated MLLM judge; key assumptions are weak (anchor 2). sol's 3 credited plausibility.", ["son55:E016", "son55:E017", "son55:E019", "agg:CG-A13"], "-6.25 vs sol"),
        "rating.E.holdout": ("son55", {"status": "not_reported", "rating": 0, "search_scope": "see ratings.E.holdout"}, "The necessary evidence (training-task provenance and disjointness from the test tasks) is absent after a full-text check, and training/evaluation share the environment; MAI-UI adds that the base model was trained on the same app family. sol's 1 gave credit for merely naming the benchmark.", ["agg:CG-A11", "agg:CG-A10"], "-2.5 vs sol"),
        "rating.E.statistics": ("son55", {"status": "resolved", "rating": 1}, "Denominators (117 tasks, 48 cells) are reported, so the item is not wholly absent; single runs and no intervals keep it at 1. sol's not_reported/0 ignored the reported denominators.", ["son55:E011", "son55:E024"], "+1.25 vs sol"),
        "expectation.E12": ("sol", "partial", "Table 2 does compare against an alternative reward configuration (binary episode reward), but confounded with the estimator change, and reward hacking is not addressed.", ["agg:CG-A13"], NA),
        "expectation.E13": ("son55", "unmet", "The RL reward partly comes from root-level execution checks plus an MLLM judge; neither side's false positives/negatives are measured, so E13 applies and is unmet. sol's not_applicable overlooked the RL-pipeline clause.", ["son55:E006", "son55:E033"], NA),
        "expectation.E21": ("son55", "unknown", "Neither ClawGUI-2B's observation space nor the baselines' is stated, so whether observation spaces differ (E21's condition) cannot be determined from the fixed text.", ["son55:E011"], NA),
        "expectation.E22": ("sol", "not_applicable", "No claim that the training recipe's gain generalises across backbone sizes; supporting several models in the harness is a capability claim, and the 2B-only result is already scoped in claims/assessment.", [], NA),
        "expectation.E25": ("sol", "partial", "The evaluation harness covers OSWorld-G, which contains infeasible instructions, with a refusal-aware judge; no refusal analysis of models is reported.", ["sol:E10"], NA),
        "expectation.E28": ("son55", "unmet", "Training runs in MobileWorld emulators with tasks that 'can be procedurally generated', evaluation is MobileWorld GUI-only, and separation is never reported; consistent with E.holdout not_reported.", ["agg:CG-A11", "son55:E033"], NA),
    },
    "shared": [
        {"field_path": "rating.G / gap.closest_adjacent", "shared_value": "sol: G unknown (MAI-UI absent from frozen references); son55: G 2 with UI-TARS-2 as closest neighbour, MAI-UI unread",
         "corrected_value": {"status": "resolved", "rating": 2, "closest_adjacent": "MAI-UI 2512.22047"},
         "reason": "Neither seat could check the base model / nearest neighbour. The now-frozen MAI-UI text shows a containerised environment manager with failover, a hybrid rule/MLLM verifier with 83% human agreement, virtual-only training and no infrastructure release. This resolves G's unknown and shifts the residual to open release + physical devices + step credit.",
         "evidence_ids": ["agg:CG-A01", "agg:CG-A02", "agg:CG-A03", "agg:CG-A04", "agg:CG-A14"], "source": "shared reference 2512.22047 (references.json, added after c3 seat dispatch)",
         "score_impact": "G unknown -> 2 for sol's record; final score computable (40.0)"},
        {"field_path": "claims.C1.baseline/control", "shared_value": "MAI-UI-2B 11.1 treated as a same-protocol same-scale comparator (sol); provenance flagged unknown (son55)",
         "corrected_value": "Table 1 non-MAI-UI rows are copied verbatim from MAI-UI's 116-task table; MAI-UI-8B is 19.7 in ClawGUI vs 27.5 official, and MAI-UI-2B has no official row, so 11.1 is an authors' re-run under unstated settings on a stated 117-task set",
         "reason": "Shared factual check against the frozen MAI-UI table. It strengthens the existing deductions (mixed provenance and denominators; a re-run 7.8 points below official for 8B suggests the authors' harness may depress baselines) but does not move any rating beyond the values already resolved.",
         "evidence_ids": ["agg:CG-A05", "agg:CG-A06", "agg:CG-A07", "agg:CG-A08", "agg:CG-A09"], "source": "shared reference 2512.22047",
         "score_impact": "none (E.measurement 2, E.causality 1 unchanged; reasons updated)"},
    ],
    "agreed_review": "Agreed items X=2, E.measurement=2, E.causality=1, E.cost=1, claim_type system_method, evidence_level online, claim_support scoped were re-checked against the text and MAI-UI; all stand, with E.measurement/E.causality reasons extended by the Table 1 provenance finding.",
    "claims_append": {"C1": (["agg:CG-A05", "agg:CG-A07", "agg:CG-A08", "agg:CG-A09", "agg:CG-A10"], "Comparator 11.1 is an authors' re-run (no official MAI-UI-2B MobileWorld number); their MAI-UI-8B re-run is 19.7 vs official 27.5; other rows copied from a 116-task table; the base model was already RL-trained on the MobileWorld app family."),
                      "C4": (["agg:CG-A15", "agg:CG-A04"], "Physical-device training is claimed 'validated' with no experiment; it is the one part of the RL residual absent from MAI-UI.")},
    "status": ("accepted_final", "All 14 mechanical conflicts resolved; G's unknown resolved via the frozen MAI-UI shared reference and recorded as a shared-error correction; no scoring unknowns remain."),
    "expected_score": 40.0,
}

PAPERS = [MS, EA, MD, GR, CLAW]

# --------------------------------------------------------------------------------------------- Qwen-Planner-Agent (out of scope)
QP = {
    "pk": "2609.29892",
    "evidence": [
        A("QP-A01", "2609.29892", "Sec 2.1.2 Task Formulation",
          "The agent primarily acts through structured tools rather than pixel-coordinate GUI actions",
          "The action space is typed tool calls, memory/skill operations and clarification; no GUI operation surface."),
        A("QP-A02", "2609.29892", "Sec 4 Related work (mobile agents)",
          "Qwen-Planner-Agent focuses on this planning problem rather than introducing a new screen-grounding architecture.",
          "Authors place the contribution outside screen perception/grounding."),
        A("QP-A03", "2609.29892", "Sec 2.2.1",
          "Programmatic sandbox environments execute typed tool calls through predefined program logic over structured application databases.",
          "Main training/evaluation substrate is tool-call sandboxes; MobilePA-Bench verifies via tool calls/state changes."),
    ],
    "reason": ("Confirmed out_of_scope. Qwen-Planner-Agent is a mobile planner over typed tool calls, memory and skills; the agent "
               "'primarily acts through structured tools rather than pixel-coordinate GUI actions', the authors state they do not "
               "introduce screen grounding, and the headline benchmark (MobilePA-Bench) verifies tool calls/state changes. Optional "
               "visual tool returns and opaque sub-agent sessions do not give the evaluated system a GUI operation surface. Under "
               "docs/EVIDENCE.md this is a pure API/function-calling agent, excluded from the GUI Agents radar. The exclusion is a "
               "scope disposition, not a quality judgement; CARE/harness contributions may belong to a tool-agent project."),
    "expected_conflicts": 41,
}
