"""Opus 5.5 (fable) adjudication decisions for c1/a1, written after reading each fixed full text first.

Every entry cites the fixed paper text (seat evidence namespaced sol:/son55:, own evidence agg:).
"""
from common import agg_evidence as A

R = lambda status, rating, reason, ev, ce=(), scope=(): {  # noqa: E731
    "status": status, "rating": rating, "reason": reason, "evidence_ids": list(ev),
    "counterevidence_ids": list(ce), "search_scope": list(scope)}

FULL_SCOPE = lambda pk: [f"research/fulltext/review-runs/gui-v22-20261021-01/fulltext/{pk}.txt (entire fixed HTML text)"]  # noqa: E731

# --------------------------------------------------------------------------------------------- DRIVE
DRIVE = {
    "pk": "2605.23939",
    "prelim": ("Read before seat scores. DRIVE is a prompted GPT-4.1 DOM web agent (its skill-free baseline row is "
               "numerically identical to AgentOccam, so DRIVE = AgentOccam + dual skill library) that induces programmatic "
               "interaction skills and NL reasoning skills from a 30% within-site training split and is tested on the other 70% "
               "of the same five WebArena sites. Main gain 45.5->52.8 is single-run; ablations single-run; a 100-task 3-run "
               "error-type study and a 150-task attribution study (split membership unstated) give the most controlled evidence. "
               "No unseen-site test, so 'dynamic/continual adaptation' is not established; whether test-time feedback updates "
               "the library is unstated. Nearest neighbour AWM (reference library) already compared text/code/action-space "
               "experience formats, which DRIVE does not engage. Applicable: C19/K27 memory cards, E28/E35 (held-out "
               "environments), E16 (spread)."),
    "materials": [("2605.23939", "paper"), ("2409.07429", "nearest_neighbor_reference")],
    "evidence": [
        A("2605.23939", "D-A01", "2409.07429", "AWM Sec 4.2 (Table 7 discussion)",
          "Overall, we do not find substantial performance variance between workflows represented in text and code formats, indicating that both forms can bring effective augmentations to agent memory.",
          "Nearest neighbour already tested the abstract-text vs executable-code representation axis DRIVE's gap is built on; DRIVE neither cites nor controls for this.", "reviewer_comment"),
        A("2605.23939", "D-A02", "2409.07429", "AWM Sec 5",
          "Besides integrating workflows as agent memory, we also explore workflows in expanding the agent action space",
          "AWM already offers workflows both as context memory and as callable actions (AWM_AS), i.e. both DRIVE representation types exist in the neighbour.", "reviewer_comment"),
        A("2605.23939", "D-A03", "2605.23939", "Sec 2 Related work",
          "In most cases, however, the experience is reused as a single object, such as a memory entry or workflow.",
          "DRIVE's characterisation of the neighbour lineage, which the AWM text shows is incomplete.", "author_report"),
        A("2605.23939", "D-A04", "2605.23939", "Sec 4.5",
          "We randomly sample 30 tasks from each of the five WebArena domains, yielding a 150-task evaluation subset.",
          "Attribution study subset; whether these tasks belong to the 30% training or 70% test split is not stated, and failures from the same subset feed the skills that are then scored on it.", "author_report"),
        A("2605.23939", "D-A05", "2605.23939", "Sec 3.1",
          "During online deployment, invoking retrieved skills also produces skill-level feedback",
          "Online feedback is said to feed later updates; whether this happens across test tasks during evaluation is not stated (possible test-time library leakage).", "author_report"),
        A("2605.23939", "D-A06", "2605.23939", "Table 2 baseline row vs Table 1 AgentOccam row",
          "Baseline | 37.2 | 41.5 | 60.4 | 41.4 | 46.8 | 45.5",
          "Skill-free baseline equals AgentOccam per domain, so the +7.3 pp is library-on vs library-off on the AgentOccam agent; the 23.1 pp margin over SkillWeaver mixes base-agent and skill-method differences.", "author_report"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": "WebArena functional-correctness checkers on held-out tasks; skills are induced on the same five sites and task types, so not transfer (EVIDENCE rule 2).",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, single main run: on the 70% held-out tasks of the same five WebArena sites (GPT-4.1, 20 steps), adding the induced dual-level skill library to the AgentOccam-equivalent agent raises macro success 45.5 -> 52.8; a 3-run 100-task subset shows each skill type shifting its own error class. Separation-vs-unified-store necessity, cross-site adaptation and continual retention are not shown.",
        "not_supported": ["Cross-website transfer / adaptation to changed sites", "Necessity of separating the two levels vs a unified store (AWM already found text vs code formats roughly equivalent)", "Statistical reliability of Table 1/2 gaps", "Continual-learning curve magnitudes (Fig 2 not in text)"],
        "unresolved": ["Whether test-episode feedback updates the library during evaluation (agg:D-A05)", "Split membership of the 150-task attribution subset (agg:D-A04)", "Whether SteP/Go-Browse/SkillWeaver rows were re-run on the same 70% split (SteP values are round integers)"],
        "retention_trace": "before: AgentOccam-equivalent agent, no library (45.5) -> candidates: skills induced from 30% training episodes -> selection: success/failure outcome, LM attribution (69.1% vs humans), selector patching, utility-based pruning/merging -> persisted: two libraries -> later use: disjoint test tasks on the same sites -> measured: +7.3 pp single run. A retained library is shown to help on same-site held-out tasks; selective maintenance is not isolated and changed-site retention is not tested.",
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "Reference library AWM (2409.07429) was read for the representation question: AWM Sec 4.2 finds no substantial difference between text and code workflows and Sec 5 already wraps workflows as callable actions. DRIVE's premise that existing methods force one representation and lose either executability or transferability is therefore only partly accurate, and DRIVE runs neither AWM nor an equal-capacity unified store. Residual gap = coordinating both forms plus failure-type routing, bounded to same-site WebArena.",
        "evidence_ids": ["agg:D-A01", "agg:D-A02", "agg:D-A03"],
    },
    "rs": ("son55", "Both seats agree on heterogeneous_decomposition (sub null; C04 not applicable) + adapt_via_conditioning (sub null). son55's per-condition notes kept; executes_pattern partial, resolves_problem unproven."),
    "domain": [("sol", "experience_memory_retrieval", "C19", None), ("sol", "experience_memory_retrieval", "K27", None),
               ("son55", "planner_grounder_interface", "K29", "partial")],
    "domain_note": "Union: reasoning skills are retrieved into context (K27) and interaction skills are invoked as callable procedures alongside primitive actions with fallback (K29, partial); both distilled from own runs (C19).",
    "expectations": {"E10": "son55", "E11": "sol", "E19": "son55", "E21": "son55", "E22": "son55", "E23": "son55",
                     "E24": "son55", "E27": "son55", "E29": "son55"},
    "ratings": {
        "G": R("resolved", 2, "Real limitation and named lineage, but the nearest neighbour AWM already compared text vs code experience formats (little difference) and offered workflows as callable actions; DRIVE does not engage this or run AWM/a unified store, so the residual gap is incompletely bounded (anchor 2).",
               ["son55:E002", "son55:E003", "agg:D-A01", "agg:D-A02", "agg:D-A03"]),
        "M": R("resolved", 3, "Concrete per-level operators (selector-set patching vs add/merge/prune of NL rules), scenario descriptors and counterfactual routing give distinguishing predictions (each skill type lowers its own error class; reversed routing hurts). LM attribution is only 69.1% accurate and reasoning-skill utility is confounded by interaction success.",
               ["son55:E005", "son55:E009", "son55:E021", "son55:E023", "sol:D01", "sol:D04"], ["sol:D08"]),
        "X": R("resolved", 3, "Induction, routing, structural+semantic retrieval with singleton activation and primitive fallback, patch/prune/merge are specified with formulas; label source for training y, thresholds/lambda, round schedule and test-time updating are unstated.",
               ["son55:E006", "son55:E007", "son55:E010", "sol:D03", "sol:D04"], ["agg:D-A05"]),
        "E.measurement": R("resolved", 3, "WebArena functional-correctness checkers and per-domain values; attribution module validated against two human annotators. Deductions: 70% subset with per-domain counts unstated, post-hoc GPT-4.1 error classifier unvalidated, provenance of some baseline rows unclear.",
                           ["son55:E014", "son55:E019", "son55:E020", "sol:D05", "sol:D06"]),
        "E.causality": R("resolved", 2, "Induction-pathway ablation and human/LM/random/reversed routing controls support that skills and correct routing matter; no unified-store or matched-context control for the separation claim, and the SkillWeaver margin mixes base agent with skill method (agg:D-A06).",
                         ["son55:E018", "son55:E021", "son55:E023", "sol:D07", "sol:D09"], ["agg:D-A06", "son55:E024"]),
        "E.holdout": R("resolved", 1, "Task-disjoint 30/70 split inside the same five sites and task types; no unseen site/UI-change test; attribution subset split membership and test-time library updating unstated.",
                       ["son55:E011", "sol:D05"], ["agg:D-A04", "agg:D-A05"]),
        "E.statistics": R("resolved", 2, "3-run mean±SD on a 100-task subset and full failure denominators for the attribution study (81 failures, confusion counts); main tables single-run without CIs.",
                          ["son55:E022", "son55:E023", "sol:D08", "sol:D09"], ["son55:E015"]),
        "E.cost": R("resolved", 2, "Same backbone/decoding/20-step cap; Shopping tokens, steps and calls reported (+13.9% input/task, +23.2% calls, -7.8% input/success). Offline induction/maintenance cost, latency and baseline budgets are not reported.",
                    ["son55:E012", "son55:E024", "sol:D10"]),
    },
    "resolutions": {
        "domain.matches": ("revised", "C19 + K27 + K29(partial)", "Both seats' extra card describes a real, different operation: K27 for retrieved reasoning guidance (sec 3.5), K29 for callable interaction skills with primitive fallback. Card matching carries no score.", ["sol:D03", "son55:E007", "son55:E010"], "none (pattern matches are not scored)"),
        "expectation.E10": ("son55", "partial", "The LM attribution reflector labels failed trajectories and routes them into libraries (a filtering role); Sec 4.5 validates it against two human annotators plus the downstream success gap, as E10 asks, but on one agent's 81 failures with 69.1% accuracy.", ["son55:E019", "son55:E020"], "none; supports E.measurement=3 with deduction"),
        "expectation.E11": ("sol", "not_applicable", "E11 applies to judges claimed reliable enough to serve as reward or evaluator; DRIVE presents attribution only as an imperfect routing aid. Per-class recall is nevertheless reported (36/47, 20/34).", ["son55:E020"], "none"),
        "expectation.E19": ("son55", "partial", "The evaluation drops 30% of WebArena tasks into a training split and uses a 20-step cap; split and cap are disclosed, but per-domain test counts and baseline re-runs on the split are not.", ["son55:E011", "sol:D05"], "none"),
        "expectation.E21": ("son55", "partial", "Baselines (SteP, Go-Browse, SkillWeaver, AgentOccam) are compared without stating each one's observation setting; only 'DOM-based' is stated for DRIVE.", ["son55:E011"], "none"),
        "expectation.E22": ("son55", "partial", "Sec 4.9 claims effectiveness is not tied to a high-capacity backbone (generalisation across backbones), so E22 applies; only GPT-4.1 and Qwen2.5-7B are reported.", ["son55:E025"], "none"),
        "expectation.E23": ("son55", "not_applicable", "The central claim is not a new benchmark or a long-horizon-capability claim; failure-cause audit exists but is assessed under statistics, not via E23.", [], "none"),
        "expectation.E24": ("son55", "unmet", "DRIVE frames its value as adaptation to dynamic pages and layout changes (selector fallbacks), a robustness claim, but no controlled perturbation/drift test is reported.", ["sol:D04"], "none; consistent with E.holdout=1"),
        "expectation.E27": ("son55", "partial", "Sec 4.3 claims gains grow with accumulated own trajectories (42->251); curve values are figure-only and saturation is only described qualitatively.", ["son55:E026"], "none"),
        "expectation.E29": ("son55", "partial", "Failure-derived (reflection) skills are ablated against a success-only skill arm (Table 2), the closest analogue of filtered BC, but not at a matched iteration/trajectory count.", ["son55:E018"], "none"),
    },
    "shared": [
        {"field_path": "rating.G", "shared_value": {"status": "resolved", "rating": 3}, "corrected_value": {"status": "resolved", "rating": 2},
         "reason": "Both seats left the AWM/SkillWeaver lineage as unverified author_report. The pinned reference AWM full text shows the neighbour already tested text vs code formats (no substantial difference) and workflows-as-actions, so DRIVE's gap is less bounded than both seats credited.",
         "evidence_ids": ["agg:D-A01", "agg:D-A02", "agg:D-A03"], "source": "reference_library 2409.07429", "score_impact": "-3.75 (G weight 15 x 1/4); final 61.25 vs both seats' 65.0"},
        {"field_path": "gap.checked_gap", "shared_value": "neighbour characterisation taken from DRIVE related work only",
         "corrected_value": "AWM already explored representation format and action-space workflows; residual = coordination of both forms + failure routing, same-site only",
         "reason": "Same reference-library fact as above, recorded on the analysis field.", "evidence_ids": ["agg:D-A01", "agg:D-A02"], "source": "reference_library 2409.07429",
         "score_impact": "none beyond the rating.G correction"},
    ],
    "status": ("accepted_final", "All seat disagreements resolved from the fixed text; one shared error corrected from the pinned reference library; no scoring unknowns."),
}

# --------------------------------------------------------------------------------------------- LiteCUA
LITECUA = {
    "pk": "2505.18829",
    "prelim": ("Read before seat scores. LiteCUA wraps an Ubuntu VM as an 'MCP server' (screenshot + a11y tree + extra "
               "inspection such as software versions; pyautogui atomic actions) and runs a prompted orchestrator/"
               "perceptor/reasoner/actor loop. Only evidence: a single OSWorld run, 54.10/369 = 14.66%, against GPT-4o "
               "11.21% and three GPT-4o frameworks, with no ablation of the contextualisation. LiteCUA's per-domain average "
               "steps (35.3; Calc/Thunderbird at 50.0 = budget exhausted) show a 50-step cap, while the OSWorld paper's "
               "GPT-4o 11.21% row was run at 15 steps, so the headline comparison is budget-unmatched. Backbone only implied "
               "by the 'Agents (based on GPT-4o)' grouping. Applicable: E01/E17/E19/E21; C17 manager-worker card."),
    "materials": [("2505.18829", "paper"), ("2404.07972", "benchmark_reference")],
    "evidence": [
        A("2505.18829", "L-A01", "2404.07972", "OSWorld appendix (experiment settings)",
          "We set the maximum steps of interaction to 15 and the maximum time limits to 30 minutes for all tasks",
          "OSWorld baseline numbers were produced with a 15-step cap.", "reviewer_comment"),
        A("2505.18829", "L-A02", "2404.07972", "OSWorld results table, Screenshot + A11y tree block",
          " | GPT-4o | 41.67% | 6.16% | 12.33% | 14.29% | 7.46% | 11.21%",
          "LiteCUA's GPT-4o baseline 11.21 is the OSWorld-paper number (15-step setting), not a re-run at LiteCUA's budget.", "reviewer_comment"),
        A("2505.18829", "L-A03", "2505.18829", "Sec 4.3",
          "The maximum step count (50.0) in these domains indicates that the system exhausts its operation budget without achieving the task goals.",
          "LiteCUA ran with a 50-step budget (mean 35.3 steps), > 3x the baseline's 15-step cap.", "author_report"),
        A("2505.18829", "L-A04", "2505.18829", "Sec 2.2 Environment Perception Framework",
          "Aside from the information from the visible elements in the screenshot, we also provide the mechanisms to inspect invisible information like the version information of softwares.",
          "LiteCUA receives inspection channels beyond the screenshot+a11y setting it claims to share with baselines.", "author_report"),
        A("2505.18829", "L-A05", "2505.18829", "Table 1",
          "Agents (based on GPT-4o)",
          "LiteCUA is listed in this group, so the backbone is implied (not explicitly stated) to be GPT-4o.", "author_report"),
        A("2505.18829", "L-A06", "2505.18829", "Sec 4.1 Baselines vs Table 1",
          "and Gemini-1.5-flash ( 31 )",
          "Text names Gemini-1.5-flash while Table 1 lists Gemini-1.5-pro 5.1: baseline provenance inconsistent.", "author_report"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": "OSWorld execution-checked success (author report); single benchmark/platform, no transfer.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported single run: a GPT-4o (implied) LiteCUA agent with a 50-step budget and extra inspection channels scores 54.10/369 = 14.66% on OSWorld. Neither the causal role of MCP contextualisation nor superiority over GPT-4o (11.21% at 15 steps) or AgentStore (+1.1 pp, ~4 tasks) is established.",
        "not_supported": ["Causal benefit of environment contextualisation (no ablation)", "Superiority over baselines at a matched step budget (agg:L-A01..A03)", "Generality beyond Ubuntu OSWorld"],
        "unresolved": ["Exact backbone (implied GPT-4o)", "Whether the official OSWorld harness/evaluators were used unmodified behind the custom VM controller", "Perceptor/Reasoner prompts and JSON schemas"],
        "retention_trace": "not_applicable: static system; no retained or self-improving component claimed",
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "OSWorld (2404.07972) reference read for the baseline setting: the GPT-4o screenshot+a11y 11.21% row was run with a 15-step cap, whereas LiteCUA used 50 steps. UFO2 not re-read (son55's targeted reading stands). The gap remains a conceptual 'semantic disconnect' without a measured failure mode or comparison to prior agent-computer interfaces.",
        "evidence_ids": ["agg:L-A01", "agg:L-A02", "agg:L-A03"],
    },
    "rs": ("son55", "outside_taxonomy kept: the MCP/JSON wrapper keeps screenshot and a11y as separate inputs to a prompted LLM and introduces no shared learned representation, vocabulary or objective, so unify_into_shared_representation's definition is not executed (sol's own reason calls the fit an engineering-interface analogy). Paper still fully scored."),
    "domain": [("sol", "agent_loop_context_control", "C17", "partial"), ("son55", "structured_screen_observation", "C13", "weak"),
               ("sol", "planner_grounder_interface", "K29", "weak")],
    "domain_note": "C17: orchestrator-worker loop exists but no role ablation or replanning detail (partial). C13: Perceptor restructures a11y elements into usage descriptions (weak, unquantified). K29 weak: MCP schema wraps the same pyautogui atomic actions; C14 considered but no pruning/simplification ablation of the action space is reported.",
    "expectations": {"E19": "son55", "E21": {"applicable": True, "status": "partial", "score_item": ["E.causality", "E.measurement"],
                                             "reason": "All systems are reported in a 'Screenshot + A11y tree' setting (sol), but LiteCUA additionally inspects invisible information such as software versions (agg:L-A04) and no screenshot-only/a11y-only or raw-vs-contextualised variant is reported (son55).",
                                             "evidence_ids": ["agg:L-A04", "son55:E022"]},
                     "E17": {"applicable": True, "status": "unmet", "score_item": ["E.cost", "E.causality"],
                             "reason": "Shared-error correction: the step cap is not stated, and the pinned OSWorld reference shows the GPT-4o 11.21% baseline used 15 steps while LiteCUA ran to 50 steps (mean 35.3); the comparison is at unequal budgets.",
                             "evidence_ids": ["agg:L-A01", "agg:L-A02", "agg:L-A03"]}},
    "ratings": {
        "G": R("resolved", 1, "Gap is a conceptual 'semantic disconnect' with no measured failure mode; prior agent-computer interfaces (Agent S ACI, UFO/UFO2) are named only as context and not compared, so the residue is unbounded (between anchors 0 and 2).",
               ["son55:E002", "son55:E025", "son55:E026", "sol:E01"]),
        "M": R("resolved", 1, "Contextualisation is described at slogan level; what the Perceptor's 'usage semantics' and the JSON schemas contain, and why they should beat the same screenshot+a11y prompt, is not reconstructable and yields no distinguishing prediction.",
               ["son55:E003", "son55:E005", "son55:E026", "sol:E02", "sol:E03"]),
        "X": R("resolved", 1, "Module names and the perceive-reason-act cycle are given, but backbone (only implied), prompts, schemas, step cap (inferable only from 50.0 exhaustion), history handling and recovery are unspecified.",
               ["son55:E004", "son55:E007", "son55:E010", "agg:L-A05"], ["agg:L-A03"]),
        "E.measurement": R("resolved", 2, "OSWorld execution checkers are trustworthy (fractional task scores are permitted by OSWorld evaluators), but harness fidelity behind the custom VM controller is unstated, baselines are copied from other settings and the Gemini row is internally inconsistent.",
                           ["son55:E011", "son55:E016", "sol:E08", "agg:L-A02"], ["agg:L-A06"]),
        "E.causality": R("resolved", 0, "No ablation isolates contextualisation, roles or perception channels; the only comparison is cross-system and, against GPT-4o, at a 50- vs 15-step budget with extra inspection channels, so it cannot attribute the 3.45 pp to the claimed mechanism.",
                         ["son55:E022", "agg:L-A01", "agg:L-A03", "agg:L-A04"], [], ["full fixed text incl. Tables 1-2; OSWorld reference for baseline setting"]),
        "E.holdout": R("resolved", 1, "One benchmark on one platform; no statement separating development of the 'operational rules' from the evaluated tasks; the platform claim is framed as general computer use.",
                       ["son55:E016", "son55:E024", "sol:E13"]),
        "E.statistics": R("resolved", 1, "Single run, no spread; margin over AgentStore is 1.1 pp (~4 of 369); per-domain counts and steps help failure accounting.",
                          ["son55:E015", "son55:E017", "sol:E11", "sol:E12"]),
        "E.cost": R("resolved", 1, "Steps per domain and VM spec are reported, but no tokens/latency, and the budget is unfair: 50 steps vs the 15-step baseline setting.",
                    ["son55:E017", "son55:E020", "agg:L-A01", "agg:L-A03"]),
    },
    "resolutions": {
        "rs.primary": ("son55", None, "See rs reason: no shared representation/objective is built; the operation is an interface wrapper outside the 15 original definitions.", ["son55:E003", "sol:E02"], "none (pattern matches are not scored)"),
        "rs.outside": ("son55", True, "Follows rs.primary; outside_taxonomy ratio for this batch becomes 1/5.", [], "none"),
        "rs.matches": ("son55", [], "Follows rs.primary.", [], "none"),
        "domain.matches": ("revised", "C17(partial) + C13(weak) + K29(weak)", "Union of supportable operations; C14 dropped (no simplification ablation; K29 better names the MCP action-schema wrapper).", ["sol:E04", "son55:E003", "sol:E02"], "none (pattern matches are not scored)"),
        "rating.G": ("son55", 1, "Fixed text gives no measured bottleneck and no neighbour comparison; sol's 'specific interface bottleneck plausible' is an inference not supported by a measurement.", ["son55:E002", "son55:E026"], "vs sol -3.75; vs son55 0"),
        "rating.M": ("son55", 1, "Sec 2.2/3.2 contain no schema, example or argument why the wrapper differs from the identical-information baseline prompt.", ["son55:E003", "son55:E005"], "vs sol -6.25; vs son55 0"),
        "rating.X": ("son55", 1, "Backbone, prompts, cap and recovery absent; cap only inferable from exhaustion.", ["son55:E004", "agg:L-A03", "agg:L-A05"], "vs sol -5.0; vs son55 0"),
        "rating.E.measurement": ("son55", 2, "Checker is trusted but harness fidelity and baseline provenance (copied, budget-mismatched, Gemini flash/pro inconsistency) are not auditable; sol's 3 did not account for copied baselines.", ["agg:L-A02", "agg:L-A06", "son55:E016"], "vs sol -2.5; vs son55 0"),
        "rating.E.causality": ("revised", {"status": "resolved", "rating": 0}, "Value matches son55 but status changes from not_reported to resolved: a cross-system comparison is reported, and the reference library shows it is budget- and information-confounded, i.e. it does not support the mechanism claim (anchor 0 'evidence ... does not answer the claim'). sol's 1 credited the same-GPT-4o comparison without knowing the 15-step baseline cap.", ["agg:L-A01", "agg:L-A03", "agg:L-A04"], "vs sol -2.5; vs son55 0"),
        "rating.E.holdout": ("son55", 1, "Static system but development/evaluation separation unstated and only one platform for a general-computer claim; sol's 2 treated OSWorld as automatically held out.", ["son55:E024"], "vs sol -2.5; vs son55 0"),
        "rating.E.cost": ("son55", 1, "Budget fairness is refuted for the GPT-4o comparison (50 vs 15 steps); only steps/VM spec reported.", ["agg:L-A01", "agg:L-A03"], "vs sol -1.25; vs son55 0"),
        "expectation.E19": ("son55", "unknown", "A custom VM controller/MCP layer replaces the standard OSWorld interface; whether official evaluators and task set are used unmodified is not stated. Applicable, status unknown.", ["son55:E011"], "none"),
        "expectation.E21": ("revised", "partial", "sol is right that one shared setting is declared; son55 is right that no channel variants are reported; additionally LiteCUA gets extra inspection info (agg:L-A04).", ["agg:L-A04"], "none; supports E.causality=0"),
    },
    "shared": [
        {"field_path": "expectation.E17.status", "shared_value": "partial (baseline caps unknown)", "corrected_value": "unmet",
         "reason": "Both seats treated baseline step budgets as unknown. The pinned OSWorld reference shows the GPT-4o 11.21% row used a 15-step cap; LiteCUA's own Table 2 shows a 50-step cap. The comparison is budget-unmatched, not merely undocumented.",
         "evidence_ids": ["agg:L-A01", "agg:L-A02", "agg:L-A03"], "source": "reference_library 2404.07972",
         "score_impact": "none beyond resolutions (E.cost and E.causality already resolved to son55's values; reasons now rest on the established mismatch)"},
        {"field_path": "assessment.unresolved / claims.C1.counterevidence", "shared_value": "baseline step budgets unknown",
         "corrected_value": "GPT-4o baseline at 15 steps vs LiteCUA at 50 steps",
         "reason": "Same fact recorded on the claim matrix.", "evidence_ids": ["agg:L-A01", "agg:L-A03"], "source": "reference_library 2404.07972", "score_impact": "none"},
    ],
    "claims_append": {"C1": "Aggregate: OSWorld reference shows the GPT-4o 11.21% baseline used a 15-step cap vs LiteCUA's 50 (agg:L-A01, agg:L-A03); LiteCUA also gets extra inspection channels (agg:L-A04)."},
    "status": ("accepted_final", "All seat disagreements resolved; one shared factual error corrected from the pinned OSWorld reference; no scoring unknowns."),
}

# --------------------------------------------------------------------------------------------- TongUI
TONGUI = {
    "pk": "2504.12679",
    "prelim": ("Read before seat scores. TongUI mines YouTube/Bilibili/WikiHow/Baidu tutorials, extracts per-step frames and "
               "step descriptions, and asks UI-TARS (a stronger released agent) to label thought+action per frame conditioned "
               "on the human step description; no execution or verifier, unlike neighbour AgentTrek's guided replay with a "
               "validated VLM evaluator. Qwen2.5-VL-3B/7B/32B are LoRA-tuned in two stages that also use each evaluation "
               "dataset's own training split. Held-out evidence: zero-shot ScreenSpot/-V2/-Pro and UI-Vision grounding; "
               "navigation results are offline (AITW, AndroidControl, Mind2Web, GUI Odyssey) after in-domain SFT, and the only "
               "online result is MiniWob (trained on MiniWob, SeeClick setting). Reproduced base-Qwen baselines are format-"
               "broken (Mind2Web 3B step SR 0.4), inflating 'improvement' margins; the ShowUI-data same-base arm and Table 12 "
               "source additions are the meaningful controls (data size unmatched). One 3-run error bar (Mind2Web, 3B). "
               "Applicable: component_training; E05/E06 grounding, E15/E02 offline-vs-online, E22 sizes, E27 scaling, E28 overlap."),
    "materials": [("2504.12679", "paper"), ("2412.09605", "nearest_neighbor_reference")],
    "evidence": [
        A("2504.12679", "T-A01", "2504.12679", "App A Resource Consumption",
          "we utilize the SFT data (training set) of the evaluation dataset to fine-tune the model.",
          "Navigation benchmarks are evaluated after in-domain SFT on their own training splits.", "author_report"),
        A("2504.12679", "T-A02", "2504.12679", "Method: Trajectory Generation",
          "we use a pretrained GUI agent (such as UI-TARS",
          "Labels come from a stronger teacher conditioned on human step descriptions (privileged at labelling time), without execution.", "author_report"),
        A("2504.12679", "T-A03", "2412.09605", "AgentTrek abstract",
          "employs a visual-language model (VLM) agent to execute these instructions in real environments, while a VLM-based evaluator verifies trajectory correctness.",
          "Nearest neighbour already converts tutorials to trajectories with execution and a verifier; TongUI trades both away for scale, a trade-off it does not analyse.", "reviewer_comment"),
        A("2504.12679", "T-A04", "2504.12679", "App A Resource Consumption",
          "Our training involves two stages.",
          "Stage composition and data mixture (GUI-Net vs public vs benchmark train splits) are not specified, a key execution condition.", "author_report"),
        A("2504.12679", "T-A05", "2504.12679", "App A Prompt (rendered text)",
          "In the following, we show the system prompt in our agent framework.\n\nSystem prompt for GUI-Net Agent\n\nIn the following",
          "Prompt boxes are empty in the fixed HTML render (rendering loss); not counted as not_reported.", "author_report"),
        A("2504.12679", "T-A06", "2504.12679", "Table 6 Mind2Web",
          "Qwen2.5-VL-3B † \\dagger | 2.5 | 14.5 | 0.4",
          "Reproduced zero-shot base model is format-broken, so gains over it overstate data value; the ShowUI-data arm is the meaningful control.", "author_report"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": "Only MiniWob is interactive with reward checks, and it is trained on; per EVIDENCE rule 2 the ceiling is online. Grounding and navigation evidence otherwise offline.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported: adding teacher-labelled, tutorial-derived GUI-Net data to Qwen2.5-VL SFT improves zero-shot screenshot grounding (ScreenSpot-family, UI-Vision) and, after in-domain SFT, offline step accuracy over a same-base ShowUI-data arm and a public-data arm (sizes unmatched); online evidence is limited to MiniWob. TongUI-7B remains below UI-TARS-7B on ScreenSpot-family.",
        "not_supported": ["Generalised online GUI-agent capability across platforms", "Label correctness of unexecuted teacher labels beyond a 100-sample rating study", "Low-cost claim (data-construction cost not reported)"],
        "unresolved": ["Two-stage training mixture (agg:T-A04)", "Tutorial-benchmark overlap beyond ID-level dedupe", "Prompts lost in HTML render (agg:T-A05)"],
        "retention_trace": "not_applicable: static corpus and LoRA weights; no retained online self-improvement claimed",
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "AgentTrek (2412.09605) reference read: it already turns web tutorials into trajectories via guided replay in real environments with a VLM evaluator validated on human labels. TongUI's residual is multi-platform scale without replay; it does not analyse what is lost (execution verification) nor that its own labels are synthetic teacher outputs, contrary to its framing of synthetic data as lacking accuracy.",
        "evidence_ids": ["agg:T-A03", "agg:T-A02"],
    },
    "rs": ("son55", "Both seats: self_supervised_signal_engineering / C08 (generate candidate supervision from tutorials, gate by filters). Fit kept partial (son55): the generator is an external teacher and the gate's accuracy is unvalidated."),
    "domain": [("son55", "mine_human_screen_videos", "R03", None), ("son55", "trajectory_level_policy_training", "C21", None)],
    "domain_note": "Identical card IDs in both seats.",
    "expectations": {"E02": "sol", "E03": "sol", "E06": "sol", "E17": "sol", "E22": "son55", "E26": "sol", "E28": "son55"},
    "ratings": {
        "G": R("resolved", 2, "Trajectory-data scarcity is real and AgentTrek/Synatra are the right neighbours, but the gap is argued by dataset size; it does not analyse the execution/verification it gives up relative to AgentTrek or its dependence on a stronger teacher.",
               ["son55:E003", "son55:E004", "sol:T01", "agg:T-A03"], ["son55:E020"]),
        "M": R("resolved", 2, "Concrete conversion chain (ASR/frames -> step descriptions -> teacher labels -> filters); the key assumption that unexecuted teacher labels on extracted frames are correct is weakly supported (100-sample rating study), and why tutorial data adds information beyond the teacher (human step descriptions as privileged hints) is not tested.",
               ["son55:E005", "son55:E006", "son55:E008", "sol:T03", "sol:T04", "agg:T-A02"], ["son55:E020"]),
        "X": R("resolved", 2, "Sources, Whisper/MOG2 processing, teacher call, filter stages and LoRA settings are described and artefacts released, but the two-stage training mixture (GUI-Net vs public vs benchmark train splits) and filter thresholds are not specified, so the trained configuration is not reconstructable; prompt boxes are lost in the HTML render.",
               ["son55:E009", "son55:E012", "sol:T05", "sol:T09", "agg:T-A01", "agg:T-A04"], ["agg:T-A05"]),
        "E.measurement": R("resolved", 2, "Click-in-box and MiniWob rewards are reliable, but navigation is offline exact-match, the 'improvement over baselines' partly compares against format-broken reproduced base models, and data quality rests on a 5-rater 0-5 study without ground-truth accuracy.",
                           ["son55:E014", "son55:E015", "son55:E030", "agg:T-A06"]),
        "E.causality": R("resolved", 2, "Same-base ShowUI-data arm and Table 12 source additions give partial attribution; data size, teacher distillation and in-domain SFT remain confounded; no filter ablation.",
                         ["son55:E026", "son55:E027", "sol:T07", "sol:T10"], ["agg:T-A01", "agg:T-A02"]),
        "E.holdout": R("resolved", 2, "Zero-shot grounding on ScreenSpot-Pro/UI-Vision and Mind2Web cross-website/domain splits are genuine held-out signals; navigation uses in-domain train splits, Baidu Experience is in-source, and tutorial-benchmark overlap is not audited.",
                       ["son55:E019", "son55:E022", "son55:E029"], ["agg:T-A01", "son55:E017"]),
        "E.statistics": R("resolved", 1, "Single runs except one 3-run Mind2Web error bar for TongUI-3B; no CIs, no failure analysis; several margins (e.g. MiniWob 72.7 vs 71.5) are within plausible run noise.",
                          ["son55:E028", "sol:T08"], ["son55:E024"]),
        "E.cost": R("resolved", 1, "Training compute disclosed (8xA100, 4-7 days); the 'low-cost' data construction (crawl, ASR, LLM and teacher calls) is not costed and baseline compute is not matched.",
                    ["son55:E018", "sol:T09"]),
    },
    "resolutions": {
        "rating.G": ("son55", 2, "The AgentTrek reference confirms son55's point: the residual vs the nearest neighbour is scale-without-replay, not argued as a measured deficit.", ["agg:T-A03", "son55:E003"], "vs sol -3.75; vs son55 0"),
        "rating.M": ("son55", 2, "Key label-validity assumption is weakly supported; sol's own reason lists teacher privilege and executability as weak.", ["agg:T-A02", "son55:E020"], "vs sol -6.25; vs son55 0"),
        "rating.X": ("sol", 2, "The training mixture across two stages is a key unstated condition (anchor 2); released code does not substitute for the fixed text, and render-lost prompts are not held against the paper.", ["agg:T-A01", "agg:T-A04"], "vs sol 0; vs son55 -5.0"),
        "rating.E.measurement": ("son55", 2, "Offline exact-match plus format-broken reproduced baselines and an unvalidated quality filter keep measurement at anchor 2.", ["agg:T-A06", "son55:E030"], "vs sol -2.5; vs son55 0"),
        "rating.E.holdout": ("son55", 2, "Zero-shot grounding benchmarks and cross-website/domain splits are real held-out evidence; sol's 1 underweights them.", ["son55:E019", "son55:E022"], "vs sol +2.5; vs son55 0"),
        "rating.E.statistics": ("son55", 1, "Only one 3-run setting and no failure denominators, weaker than DRIVE-style subset repeats; sol's 2 overcredits.", ["son55:E028"], "vs sol -1.25; vs son55 0"),
        "expectation.E02": ("sol", "unmet", "TongUI claims improved mobile navigation via AITW/AndroidControl/GUI Odyssey only; E02 applies to mobile-agent improvement claims and no AndroidWorld online result is given.", ["son55:E022"], "none"),
        "expectation.E03": ("sol", "unmet", "A data-synthesis method claiming web-agent gains (Mind2Web, MiniWob) without a self-hosted realistic web benchmark such as WebArena.", [], "none"),
        "expectation.E06": ("sol", "partial", "UGround/Aguvis/OS-Atlas/UI-TARS-7B appear on ScreenSpot, but ScreenSpot-V2/-Pro omit some, UI-TARS-1.5 absent; partial rather than met.", [], "none"),
        "expectation.E17": ("sol", "unmet", "E17 requires an equal, stated budget; MiniWob step caps are never stated, so the requirement is unmet (not merely unknown).", [], "none"),
        "expectation.E22": ("son55", "met", "3B/7B/32B results are reported, including where 32B does not beat 7B.", [], "none"),
        "expectation.E26": ("sol", "not_applicable", "E26 targets exploration-first/reverse/world-model synthesis; tutorial mining with task extraction is instruction-first, so the requirement does not apply.", [], "none"),
        "expectation.E28": ("son55", "partial", "Some evaluations are separate from the data sources (zero-shot grounding), but Baidu Experience is both source and test and no overlap audit is reported.", ["son55:E029"], "none"),
    },
    "shared": [],
    "status": ("accepted_final", "All seat disagreements resolved from the fixed text; AgentTrek reference used only to confirm the gap resolution; no scoring unknowns."),
}

# --------------------------------------------------------------------------------------------- MobileInject
MOBILEINJECT = {
    "pk": "2610.23307",
    "prelim": ("Read before seat scores. Evaluation resource: 108 dependent emulator instances (9 workflows x 12 objectives) "
               "with deterministic benign/adversarial state oracles - strong endpoint measurement. RSDF labels come from an "
               "unnamed automated evaluator with no human agreement reported, and the pipeline forces action-hijack (and "
               "rationale-hijack) labels whenever the adversarial oracle fires, so AHR>=AGR and part of the 'reasoning precedes "
               "action' coupling is by construction. UC is measured on 9 benign workflows (values in ninths). CMCI equal-"
               "exposure and budget-matched controls exist but only on Gemini-2.5-Flash over four workflows without intervals; "
               "defenses are tested only on GLM-4.5V/MobAgent. Neighbour GhostEI-Bench already uses a judge LLM on reasoning "
               "traces with a reliability validation. Applicable: C30/C33/C34 cards; E10 (LLM labels), E13, E16, E34."),
    "materials": [("2610.23307", "paper"), ("2510.20333", "nearest_neighbor_reference")],
    "evidence": [
        A("2610.23307", "I-A01", "2610.23307", "Sec 4 RSDF",
          "The implemented pipeline additionally enforces that an episode whose adversarial state oracle fires contains at least one action-hijack label",
          "Outcome-constrained labelling: AHR>=AGR and RHR coupling partly by construction.", "author_report"),
        A("2610.23307", "I-A02", "2610.23307", "Fig 11 caption",
          "Figure 11: Equal-exposure CMCI controls on Gemini-2.5-Flash, averaged over four major benign workflows.",
          "Key causal control limited to one model and four workflows.", "author_report"),
        A("2610.23307", "I-A03", "2610.23307", "Table 4 row",
          "GLM-4.5V | 66.67% | 0.93% | 83.33%",
          "UC values are multiples of 1/9: clean utility rests on ~9 benign workflows, not 108 instances.", "our_inference"),
        A("2610.23307", "I-A04", "2610.23307", "Table 9 baseline row",
          "Baseline | 0.93% | 83.33% | 2.78%",
          "Defense baseline equals GLM-4.5V/MobAgent, so defenses were tested on one model-framework pair.", "our_inference"),
        A("2610.23307", "I-A05", "2510.20333", "GhostEI-Bench abstract",
          "We also introduce a novel evaluation protocol where a judge LLM performs fine-grained failure analysis by reviewing the agent’s action trajectory alongside the corresponding sequence of screenshots.",
          "Neighbour already diagnoses reasoning/perception failure points with an LLM judge on trajectories.", "reviewer_comment"),
        A("2610.23307", "I-A06", "2510.20333", "GhostEI-Bench appendix heading",
          "D.1 Reliability Validation of the LLM Judge",
          "Neighbour validates its judge; MobileInject reports no human agreement for RSDF labels.", "reviewer_comment"),
        A("2610.23307", "I-A07", "2610.23307", "Sec 4 RSDF",
          "an automated semantic evaluator separate from the tested mobile agent proposes the diagnostic vector",
          "Diagnoser identity/prompts unstated.", "author_report"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": "Resettable Android emulator with deterministic state oracles (author report).",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported: on 108 dependent, authored emulator instances, nine MLLMs under two frameworks reach high oracle-verified adversarial-goal rates with low utility under attack; on Gemini-2.5-Flash over four workflows, one-visual-plus-one-textual exposure beats equal-exposure single-channel controls. RSDF's reasoning-to-action diagnosis is partly constructed by outcome-forced labels and is not human-validated; defense insufficiency is shown for one model-framework pair.",
        "not_supported": ["Independently validated reasoning-hijack onset/coupling", "Cross-modal reinforcement beyond one model/four workflows", "Prompt-defense insufficiency beyond GLM-4.5V/MobAgent", "'First benchmark' novelty (GhostEI-Bench already judges reasoning traces)"],
        "unresolved": ["RSDF evaluator identity and validity", "Real vs mock apps in the emulator", "Sample size behind Fig 11/12 controls"],
        "retention_trace": "not_applicable: evaluation resource",
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "GhostEI-Bench (2510.20333) reference read: it already runs emulator environmental injection with an LLM judge over trajectories and screenshots and reports judge reliability validation. MobileInject's Table 1 marks GhostEI 'partial' on trajectory diagnosis; its genuine residue is the controlled cross-modal channel manipulation, while RSDF is an unvalidated variant of an existing practice.",
        "evidence_ids": ["agg:I-A05", "agg:I-A06"],
    },
    "rs": ("son55", "Primary controlled_diagnostic_design/C02 (both seats). Supporting assumption_audit_and_pivot (sub null) accepted from son55: MRCD/RCI are constructed exploits of the trusted-instruction/untrusted-observation boundary, a distinct operation from the diagnostic design; C01 considered but its representational-locus relocation is not the paper's framing."),
    "domain": [("son55", "environmental_injection_attacks", "C30", "strong"), ("sol", "environmental_injection_attacks", "C33", "strong"),
               ("son55", "injection_defense_isolation", "C34", "partial")],
    "domain_note": "Same card IDs in both seats; fits set to C30 strong (payloads in attacker-writable SMS/email/calendar/web content), C33 strong (AGR vs RHR/AHR), C34 partial (prompt defenses on one model-framework pair).",
    "expectations": {"E10": "son55", "E34": "sol"},
    "ratings": {
        "G": R("resolved", 3, "Concrete residue (does synchronized visual+textual exposure amplify injection beyond repeated single-channel exposure) with named neighbours; the RSDF residue is smaller than claimed because GhostEI already judges reasoning traces with validation.",
               ["son55:E003", "son55:E012", "sol:I01"], ["agg:I-A05", "agg:I-A06"]),
        "M": R("resolved", 2, "Channel manipulation with equal-exposure and matched-template controls is a sound intervention design, but the second pillar (RSDF) forces hijack labels from the outcome oracle, so its headline findings (early reasoning hijack, tight coupling) are partly tautological rather than distinguishing predictions.",
               ["son55:E012", "son55:E013", "sol:I02", "sol:I10"], ["agg:I-A01", "sol:I03"]),
        "X": R("resolved", 2, "Six-stage protocol, instance contract and admission checks are described, but the annotation step (diagnoser model, prompts, adjudication, fallback positives) and the control-condition sample sizes are not reconstructable.",
               ["son55:E009", "son55:E024", "sol:I01", "sol:I09"], ["agg:I-A01", "agg:I-A07"]),
        "E.measurement": R("resolved", 2, "Deterministic state oracles for UA/AGR are strong; diagnostic metrics lack human validation, OSS weights are ad hoc, UC rests on ~9 workflows, and oracle error is not measured two-sidedly.",
                           ["son55:E018", "son55:E021", "sol:I05", "sol:I06"], ["agg:I-A01", "agg:I-A03"]),
        "E.causality": R("resolved", 2, "Equal-exposure and budget-matched controls address repetition/length/salience alternatives for the endpoint effect, but on one model and four workflows without intervals; diagnostic causation is constrained by construction.",
                         ["son55:E013", "son55:E014", "son55:E016", "sol:I02", "sol:I10"], ["agg:I-A01", "agg:I-A02"]),
        "E.holdout": R("resolved", 2, "Nine models x two frameworks give breadth for the vulnerability claim; instances are dependent authored templates in one emulator, attack templates are developed on the evaluated set, and no realism check exists.",
                       ["son55:E010", "son55:E023", "sol:I05"], ["sol:I09"]),
        "E.statistics": R("resolved", 2, "N=108 per condition, three-seed AGR for one condition, cluster-paired intervals with Holm correction for selected comparisons (honest non-significance); most conditions are point estimates.",
                          ["son55:E025", "son55:E033", "sol:I09", "sol:I11"]),
        "E.cost": R("resolved", 2, "Budget fairness is strong for this resource (common 20-action cap; attack controls matched in length, repetitions, exposure and salience); actual compute/token/latency and diagnoser cost are not reported.",
                    ["son55:E024", "sol:I02", "sol:I10"]),
    },
    "resolutions": {
        "rs.supporting": ("son55", ["assumption_audit_and_pivot"], "MRCD/RCI are constructed boundary-violating exploits, an operation distinct from the controlled diagnostic; supporting count stays within 2.", ["son55:E016"], "none (pattern matches are not scored)"),
        "rs.matches": ("son55", ["controlled_diagnostic_design/C02", "assumption_audit_and_pivot/None"], "Follows rs.supporting.", [], "none"),
        "rating.M": ("sol", 2, "son55 itself notes RSDF's outcome-constraining weakens independence; since RSDF is one of the four contributions and the source of the reasoning-hijack findings, the key assumption is weak (anchor 2).", ["agg:I-A01", "sol:I03"], "vs sol 0; vs son55 -6.25"),
        "rating.X": ("sol", 2, "The annotation execution (unnamed evaluator, fallback positive steps, outcome-dependent persistence) and control sample sizes are key unstated conditions.", ["agg:I-A01", "agg:I-A07", "agg:I-A02"], "vs sol 0; vs son55 -5.0"),
        "rating.E.causality": ("sol", 2, "The controls are well designed but cover one model and four workflows with no reported intervals; '30/108 reversals' does not name the model. Not 'strong alternative explanations tested' (anchor 4/3).", ["agg:I-A02"], "vs sol 0; vs son55 -2.5"),
        "rating.E.holdout": ("son55", 2, "For an evaluation resource whose main claim is broad vulnerability, nine models x two frameworks is real coverage; remaining gaps (dependent templates, single emulator, no realism check) fit anchor 2 rather than 1.", ["son55:E010", "son55:E023"], "vs sol +2.5; vs son55 0"),
        "rating.E.cost": ("son55", 2, "Budget fairness is explicitly engineered (common cap + matched attack controls); only actual cost is missing, which fits anchor 2.", ["son55:E024", "sol:I10"], "vs sol +1.25; vs son55 0"),
        "expectation.E10": ("son55", "unmet", "RSDF's LLM evaluator produces headline evaluation metrics (SAR/RHR/AHR, OSS); E10's purpose applies and no human-label agreement is reported, unlike neighbour GhostEI (agg:I-A06).", ["agg:I-A06", "agg:I-A07"], "none; supports E.measurement=2"),
        "expectation.E34": ("sol", "not_applicable", "Experiments use the AndroidWorld/MobileSafetyBench-style resettable Android emulator; no simulated app or digital twin is claimed to substitute for real apps, so E34's trigger is not met. Ecological realism remains a holdout limitation.", ["son55:E009"], "none"),
    },
    "shared": [
        {"field_path": "gap.checked_gap", "shared_value": "neighbour comparison rests on the authors' Table 1; sources unverified",
         "corrected_value": "GhostEI-Bench already judges reasoning traces with an LLM and validates the judge; MobileInject's residue is the controlled cross-modal channel manipulation",
         "reason": "Both seats left the neighbour characterisation as author_report. The pinned GhostEI full text shows Table 1 understates the neighbour on trajectory diagnosis.",
         "evidence_ids": ["agg:I-A05", "agg:I-A06"], "source": "reference_library 2510.20333",
         "score_impact": "none (G stays 3 because the cross-modal residue is concrete; the correction narrows the RSDF novelty claim and supports E10=unmet)"},
    ],
    "status": ("accepted_final", "All seat disagreements resolved; one shared gap characterisation corrected from the GhostEI reference; no scoring unknowns."),
}

# --------------------------------------------------------------------------------------------- MobileJailBench
MOBILEJAIL = {
    "pk": "2610.23303",
    "prelim": ("Read before seat scores. Evaluation resource in a browser-based Android-like simulator (abstracts process "
               "isolation and live services), 520 tasks claimed but tables use 50 benign + 70 explicit + 70 implicit; M3A results "
               "for the '20 pairings' are not shown. ASR is oracle-checked; SAF labels come from two calls of one judge model "
               "with quote audit and outcome-forced aggregation, validated against a 'ground truth' of unspecified provenance "
               "and size. FDJE is adaptive search on the evaluation tasks with unstated budget vs pass@2; the abstract's 100% "
               "ASR on Qwen3.5-122B is not in the tables (98.6). Two-run results show large run-to-run variance (Gemini-2.5-Pro "
               "36 vs 56) while main tables are single-run and exclude unresolved episodes without counts. Neighbour "
               "MobileSafetyBench already evaluates harmful/high-risk tasks and indirect injection in Android emulators."),
    "materials": [("2610.23303", "paper"), ("2410.17520", "nearest_neighbor_reference")],
    "evidence": [
        A("2610.23303", "J-A01", "2610.23303", "Table 2 caption",
          "TSR uses 50 benign tasks; Explicit and Implicit each contain 70 attacks.",
          "Reported tables use 190 of the claimed 520 tasks.", "author_report"),
        A("2610.23303", "J-A02", "2610.23303", "Sec 5 SAF",
          "Each rate excludes unresolved episodes and reports coverage alongside bootstrap confidence intervals",
          "Denominators exclude unresolved episodes; no counts or intervals appear in the rendered tables.", "author_report"),
        A("2610.23303", "J-A03", "2610.23303", "Abstract",
          "reaching a 100% ASR on Qwen3.5-122B",
          "Headline number; Table 3(a) shows FDJE ASR 98.6 for Qwen-122B.", "author_report"),
        A("2610.23303", "J-A04", "2610.23303", "Table 3(a)",
          "Qwen-122B Baseline 89.3 95.0 91.4 6.4 FDJE 98.6 100.0 99.3 0.0",
          "Tabulated FDJE ASR is 98.6 (RHR 100), not 100 ASR.", "author_report"),
        A("2610.23303", "J-A05", "2610.23303", "Table 3(b)",
          "Gemini-2.5-Pro | 36.0 | 56.0 | 96.0",
          "First-run vs two-run union differs by 20 pp: single-run main comparisons are noisy.", "author_report"),
        A("2610.23303", "J-A06", "2610.23303", "Sec 3.1 Mobile Environment",
          "The environment supports controlled execution while abstracting real Android process isolation and live service behavior.",
          "Simulator, not real Android; realism untested.", "author_report"),
        A("2610.23303", "J-A07", "2410.17520", "MobileSafetyBench intro",
          "Additionally, our benchmark includes scenarios that challenge agents with indirect prompt injection attacks, deceiving them into taking actions contrary to user intentions.",
          "Neighbour already evaluates mobile workflows (emulator) with harmful tasks and injections; MobileJailBench's 'conversational-only' gap is partly overstated.", "reviewer_comment"),
    ],
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": "Interactive simulator with state-diff oracles (author report); simulator is Android-like, not real Android.",
        "claim_support": "scoped",
        "strongest_supported_claim": "Author-reported, in a browser-based Android-like simulator: ten MLLMs under GenericV2 show high oracle-verified ASR on 70 explicit and 70 implicit tasks, implicit tasks draw far fewer refusals and more coded risky execution without higher verified ASR, adaptive FDJE search at an unstated budget raises ASR (Qwen-122B 98.6, not 100), a 50-task WDBE expansion transfers to other models, and SAF agrees more with an unspecified reference than a single judge.",
        "not_supported": ["100% ASR as tabulated", "Budget-matched superiority of FDJE", "Real-Android fidelity", "Results for M3A pairings and composite/expansion benches beyond WDBE-50"],
        "unresolved": ["SAF reference provenance and size", "Unresolved-episode counts per rate", "Step limit and search budgets"],
        "retention_trace": "not_applicable: evaluation resource (benchmark releases are frozen; no agent improvement claimed)",
        "author_report_only": True, "our_run": False,
    },
    "gap_check": {
        "aggregate_neighbor_check": "MobileSafetyBench (2410.17520) reference read: Android-emulator evaluation already includes harmful/high-risk tasks and indirect prompt injection, so 'existing jailbreak evaluations focus on conversational attacks' is partly overstated (the paper's own Table 1 marks MobileSafetyBench as workflow-grounded). Residue: implicit/composite jailbreak delivery, evolving attack/task sets, layered adjudication; the static-difficulty gap is argued, not shown.",
        "evidence_ids": ["agg:J-A07"],
    },
    "rs": ("sol", "Primary assumption_audit_and_pivot / C01 (sol): the operational core relocates the harmful payload from the instruction text to a GUI environmental carrier (implicit track) to test whether refusal alignment keyed to conversational cues survives - a locus relocation exploit, C01's tactic. Supporting controlled_diagnostic_design / C02 for matched/mismatched placement and judge-apparatus comparisons. son55's weak self_supervised_signal_engineering listing dropped (WDBE gating is task generation for evaluation, not a training signal)."),
    "domain": [("sol", "verifiable_execution_reward", "C22", "strong"), ("sol", "exploration_driven_task_synthesis", "K15", "strong"),
               ("sol", "environmental_injection_attacks", "C33", "strong"), ("son55", "learned_outcome_and_process_judges", "C25", "partial")],
    "domain_note": "Union: C22 (resettable executable oracles), K15 (WDBE proposes tasks from observed failures), C33 (SAF separates adoption/violation from verified breach), C25 partial (dual-track LLM judge).",
    "expectations": {"E10": "son55", "E17": "sol", "E21": "son55", "E28": "son55"},
    "ratings": {
        "G": R("resolved", 2, "Workflow-grounded jailbreak and ASR-only evaluation gaps are real, but MobileSafetyBench already covers harmful tasks/injection in emulator workflows and the 'static difficulty' gap is argued while the own static bench is unsaturated (~56-60% ASR).",
               ["son55:E003", "son55:E005", "son55:E031", "sol:J02"], ["agg:J-A07"]),
        "M": R("resolved", 3, "Coherent layered design: fixed-oracle adaptive attack routing, gated task generation with oracle sanity conditions and GUI witness, and a deterministic-anchor/dual-track/quote-audit/arbitration judge; predictions (single judge under-detects RHR) are tested. Weaknesses: outcome-consistency forcing and same-judge tracks.",
               ["son55:E014", "son55:E017", "son55:E020", "sol:J04", "sol:J05", "sol:J06"]),
        "X": R("resolved", 2, "Episode protocol, FDJE routing, WDBE gates and SAF equations are described; step limit, search budgets, judge model, reference annotation, per-bench counts and M3A results are absent from the text.",
               ["son55:E013", "son55:E017", "sol:J03"], ["son55:E027", "sol:J08"]),
        "E.measurement": R("resolved", 2, "State oracles with sanity tests are sound inside the simulator, but SAF's reference ('ground truth') provenance/size is undefined, rates drop unresolved episodes without counts, outcome-forced aggregation shapes RHR/SVR, and the headline 100% is not traceable to the tables.",
                           ["son55:E018", "son55:E024", "sol:J05", "sol:J06"], ["agg:J-A02", "agg:J-A03", "agg:J-A04"]),
        "E.causality": R("resolved", 2, "FDJE component/strategy ablations and matched-vs-mismatched placement exist; explicit vs implicit are different task sets and FDJE vs pass@2 has unmatched compute.",
                         ["son55:E024", "son55:E035", "sol:J08"], ["son55:E031", "sol:J04"]),
        "E.holdout": R("resolved", 2, "WDBE-50 transfers to models other than its source, a held-out signal; FDJE is optimised on the evaluation tasks, everything runs in one custom simulator without realism check.",
                       ["son55:E037", "son55:E038", "sol:J09"], ["agg:J-A06"]),
        "E.statistics": R("resolved", 1, "Main tables are single-run on 70-task sets with no visible intervals, denominators exclude unresolved episodes without counts, and the two-run data show 20 pp run-to-run swings, so the explicit-vs-implicit mean contrasts (59.8 vs 56.4 ASR) are not statistically supported.",
                          ["sol:J07", "son55:E029"], ["agg:J-A02", "agg:J-A05"]),
        "E.cost": R("resolved", 1, "Budgets are said to be recorded but not given; adaptive search compared with pass@2 and other attacks without matched compute; evaluation cost unreported.",
                    ["son55:E035", "son55:E036", "sol:J04"]),
    },
    "resolutions": {
        "rs.primary": ("sol", "assumption_audit_and_pivot", "The contribution's operational core is relocating the harmful payload to a GUI carrier to break conversational-cue alignment (C01 tactic); C02 fits the evaluation-control parts and is kept as supporting.", ["sol:J03", "sol:J04"], "none (pattern matches are not scored)"),
        "rs.supporting": ("sol", ["controlled_diagnostic_design"], "self_supervised_signal_engineering (weak, son55) dropped: WDBE generate-and-gate produces evaluation tasks, not supervision, and protocol allows supporting cards only when a distinct operation needs them.", [], "none"),
        "rs.matches": ("sol", ["assumption_audit_and_pivot/C01", "controlled_diagnostic_design/C02"], "Follows rs.primary/supporting; C01 sub under correct parent per PARENTS.tsv.", [], "none"),
        "domain.matches": ("revised", "C22 + K15 + C33 + C25(partial)", "Each seat's extra card names a real operation (C33: adoption/violation vs breach; C25: LLM judge tracks).", ["sol:J05", "sol:J06", "son55:E020"], "none (pattern matches are not scored)"),
        "rating.G": ("son55", 2, "MobileSafetyBench reference confirms partial coverage of the claimed gap; the Red Queen staleness gap is not demonstrated.", ["agg:J-A07", "son55:E031"], "vs sol -3.75; vs son55 0"),
        "rating.E.measurement": ("sol", 2, "son55's 3 credits a judge study whose reference is undefined; unresolved exclusions and the untraceable 100% headline keep measurement at anchor 2.", ["agg:J-A02", "agg:J-A03", "agg:J-A04"], "vs sol 0; vs son55 -2.5"),
        "rating.E.statistics": ("sol", 1, "Failure denominators (unresolved exclusions) are not given and run-to-run variance is large relative to the reported contrasts; stated-but-invisible bootstrap CIs cannot be credited.", ["agg:J-A02", "agg:J-A05"], "vs sol 0; vs son55 -1.25"),
        "expectation.E10": ("son55", "partial", "SAF's judge produces headline labels (RHR/SVR/SRR); agreement with a reference is reported but its annotators/size/independence are not, so partial.", ["son55:E024", "son55:E025"], "none"),
        "expectation.E17": ("sol", "unmet", "Step limit and search budgets are never stated and FDJE is compared with pass@2 at unequal search; E17's 'equal, stated budget' is unmet.", ["sol:J04"], "none"),
        "expectation.E21": ("son55", "unknown", "GenericV2 and M3A may differ in observation space; the text gives only a generic 'reads screenshots' protocol and shows no M3A results, so applicability holds and status is unknown.", ["son55:E013"], "none"),
        "expectation.E28": ("son55", "partial", "Self-generated WDBE tasks are evaluated on models other than their source (held-out signal) but in the same simulator; FDJE itself is optimised on evaluation tasks.", ["son55:E037", "son55:E038"], "none"),
    },
    "shared": [],
    "status": ("accepted_final", "All seat disagreements resolved; MobileSafetyBench reference used to confirm the gap resolution; no scoring unknowns. Note: figure-only content (Fig 3) and the unrendered bootstrap intervals could change E.statistics only if a fuller version with visible intervals and unresolved counts is pinned."),
}

PAPERS = [DRIVE, LITECUA, TONGUI, MOBILEINJECT, MOBILEJAIL]
