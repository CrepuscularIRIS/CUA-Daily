"""Opus 5.5 (fable) adjudication decisions for p2/a1, written after reading each fixed full text first.

Scope: 2202.08137, 2304.07061, 2305.11854 only. 2209.08655 / 2303.17491 are skipped (material_upgraded_a2_pending).
Seat evidence is namespaced sol:/son55:, own evidence agg:. Every agg quote is substring-checked by agg_evidence().
"""
from common import agg_evidence as A

R = lambda status, rating, reason, ev, ce=(), scope=(): {  # noqa: E731
    "status": status, "rating": rating, "reason": reason, "evidence_ids": list(ev),
    "counterevidence_ids": list(ce), "search_scope": list(scope)}

FULL_SCOPE = lambda pk: [f"research/fulltext/review-runs/gui-v22-20261021-01/fulltext/{pk}.txt (entire fixed HTML text incl. tables/appendix; figures not rendered)"]  # noqa: E731

# Seat evidence that cites files replaced after a1 was frozen (2209.08655 / 2303.17491). Not opened, not relied on.
REPLACED = "cites a material (2209.08655 or 2303.17491) whose shared file was replaced by the a2 upgrade; the aggregator was instructed not to read the upgraded file, so this quote could not be verified against the a1 sha and is not used in any final decision"

# ============================================================================================ 2202.08137 CC-Net
CC = {
    "pk": "2202.08137",
    "prelim": (
        "Read before seat scores. CC-Net is a full keyboard/mouse agent (pixels + DOM + task-field dictionary in, 10 action "
        "types out) trained by equal-weight BC + VMPO on ~2.4M success-filtered human demonstrations of all 104 MiniWoB++ "
        "tasks, single seed, hand-tuned. Central claim: SOTA and human-level mean on MiniWoB++, with data size as the "
        "'primary missing factor' and 'cross-task transfer'. Evidence is online (programmatic rewards) but every evaluated "
        "task family is a training family, so 'transfer' is multi-task sample efficiency, not held-out transfer. Controls "
        "are rich (BC-only/RL-only, data scaling over 3 orders, input/output ablations, multi- vs single-task) but values "
        "are mostly figure-only in the fixed text, and the scaling arm co-varies the BC loss weight. Table 3 recomputation: "
        "human 0.9345 vs CC-Net 0.9355 over 104 tasks, but excluding moving-items (human latency artefact) human leads "
        "0.942 vs 0.936, so 'human-level mean' is fragile. The operation is an audit of the inferred insufficiency of "
        "generic BC+RL (pivot by scaling demonstrations), enabled by a unified human/agent action interface. "
        "Prelim ranges: G3 M2-3 X3 Em3 Ec2-3 Eh1-2 Es1 Ecost1-2."),
    "materials": [("2202.08137", "paper")],
    "evidence": [
        A("2202.08137", "CC-A01", "2202.08137", "Appendix Table 3, row moving-items (with full-table recomputation)",
          "moving-items | 0.18 | 0.88 | 0.13 | 0.78",
          "Aggregator recomputation over all 104 Table 3 rows: Human mean 0.9345, CC-Net 0.9355, BC-only 0.3046; agent>human on 72 tasks, human>agent on 22. Excluding moving-items (human 0.18 attributed by the authors to network latency) gives Human 0.9418 vs CC-Net 0.9360, so the mean-level parity depends on one latency-confounded task.",
          "our_inference"),
        A("2202.08137", "CC-A02", "2202.08137", "Sec 3.1",
          "The biggest performance gap is for the moving-items task where human participants rarely succeeded at all, most likely due to network-related control latency.",
          "Authors attribute the largest agent>human gap to a human-side latency artefact, i.e. a comparator defect rather than agent skill."),
        A("2202.08137", "CC-A03", "2202.08137", "Sec 4 Performance",
          "examining the literature in this space would suggest that conventional approaches are inadequate, and more specialized techniques are needed. We have shown this to not be the case",
          "Explicit statement of the audited assumption (generic BC+RL is inadequate) and the pivot (it is not, given enough demonstrations): the assumption_audit_and_pivot operation."),
        A("2202.08137", "CC-A04", "2202.08137", "Abstract",
          "These results demonstrate the usefulness of a unified human-agent interface when training machines to use computers.",
          "The shared human/agent keyboard-mouse interface is claimed as a separate load-bearing ingredient (supports a supporting unify_into_shared_representation match)."),
        A("2202.08137", "CC-A05", "2202.08137", "Sec 2.1",
          "This simplifies the use of human behavioural data, and we further hypothesise that this interface will better transfer to computer control tasks without a compact DOM to interact with",
          "Interface choice is justified by data compatibility; the transfer-to-non-DOM benefit is a hypothesis, not tested (pixel-only performance is poor per the 75% DOM-removal drop)."),
        A("2202.08137", "CC-A06", "2202.08137", "Sec 3.4",
          "This means that the agent is unable to solve tasks that involve clicking at a specific location within a canvas, dragging, or highlighting.",
          "Element-ID (DOM) action variant cannot express sub-element/drag actions; concrete boundary evidence for the gui K29 action-interface card."),
        A("2202.08137", "CC-A07", "2202.08137", "Sec 3.3",
          "we simply reduced the relative weight of the BC loss (scaled by the square root of the relative size) to slow overfitting",
          "The data-scaling arm also changes the BC loss weight, so the scaling curve is not a pure data intervention."),
    ],
    "rs": {
        "custom": {
            "primary": "assumption_audit_and_pivot",
            "supporting": ["unify_into_shared_representation"],
            "outside_taxonomy": False,
            "base_from": {"assumption_audit_and_pivot": "sol", "unify_into_shared_representation": "son55"},
            "reason": ("Primary: the paper's stated contribution is to overturn the field's inference that generic BC+RL is "
                       "inadequate on MiniWoB (agg:CC-A03, son55:E002, son55:E005) by violating its small-data precondition "
                       "(400x human data) and demonstrating the new behaviour - the assumption_audit_and_pivot signature "
                       "(identify assumption -> violate -> demonstrate). Fit partial: no tightness/identifiability certificate "
                       "and the 'binding constraint' is shown only within one architecture (agg:CC-A07). Supporting: a distinct "
                       "operation maps humans and agents, and all 104 tasks, into one keyboard/mouse action space and one "
                       "multimodal policy (agg:CC-A04, agg:CC-A05, son55:E020); fit partial because no held-out task shows a "
                       "capability only the unified substrate yields. Sub-cards null for both: C01/C05/C11/C19/C28/C29 tactics "
                       "(security locus, identifiability, bounds) are absent; C18 (manufacture a substrate to borrow a mature "
                       "pretrained recipe) is absent since CC-Net trains from scratch."),
            "executes_pattern": "partial",
            "resolves_problem": ("scoped: closes 'generic BC+RL cannot do MiniWoB++' for the trained 104 task families "
                                 "(author-reported); does not close generalisation to unseen tasks, pixel-only control or real computers."),
        },
        "pmap": [("sol", "assumption_audit_and_pivot", "trajectory_level_policy_training"),
                 ("son55", "unify_into_shared_representation", "planner_grounder_interface")],
    },
    "domain": [("son55", "trajectory_level_policy_training", None, "partial"),
               ("son55", "planner_grounder_interface", "K29", "partial")],
    "domain_note": ("Kept son55's two matches. trajectory_level_policy_training/null: success-filtered demonstrations + joint "
                    "BC/online RL update; no K20 critic/advantage filtering. planner_grounder_interface/K29 partial: the paper "
                    "chooses and ablates the action abstraction (raw keyboard/mouse vs DOM-element actions), which is K29's "
                    "operation, but in the opposite direction to K29's element-tag examples; no planner/grounder split."),
    "domain_extra_proposals": [{"status": "revision_proposal_not_checked", "card": "gui:K29",
                                "note": "K29 lists 'Counterexamples: none found'. 2202.08137v2 Sec 3.4 / Fig 8b (agg:CC-A06) reports a DOM-element action variant less effective than raw keyboard/mouse on MiniWoB++ and unable to express canvas clicks/drag/highlight; candidate counter-evidence source for K29's 'When it fails'. Single paper, record only; no card edit in-batch."}],
    "gap_check": {
        "aggregator_check": ("Gap confirmed in the fixed text: the original MiniWob BC (17 h) barely beat random and later work "
                             "moved to DOM actions/curricula/constrained exploration (son55:E004, son55:E005); the residual question "
                             "(does generic BC+RL with a human-compatible interface work at scale) is explicit, and remaining gaps "
                             "(human intent, pixel-only, non-DOM tasks) are stated in Sec 4. Nearest-neighbour originals are not in "
                             "the pinned pack; their per-task numbers come from Table 3, partly figure-estimated (sol:E020)."),
    },
    "claims_append": {
        "C1": ("[agg] Table 3 recomputation (agg:CC-A01): parity holds only with moving-items included (human 0.18 from "
               "network latency, agg:CC-A02); excluding it Human 0.942 > CC-Net 0.936. 'Human-level mean' is a fragile, "
               "comparator-sensitive equality, not a robust capability statement."),
        "C2": "[agg] The scaling arm co-varies BC loss weight with data size (agg:CC-A07); the curve is not a pure data intervention.",
    },
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": ("Live browser episodes scored by MiniWoB++ programmatic rewards. All evaluated task families are "
                                  "training families (new random instances only), so not transfer under EVIDENCE rule 2."),
        "claim_support": "scoped",
        "author_claim": "SOTA and human-level mean across MiniWoB++, data size as primary missing factor, strong cross-task transfer, a formula toward general computer control.",
        "strongest_supported_claim": ("Author-reported, single seed: one BC+RL keyboard/mouse agent trained on ~2.4M human "
                                      "demonstrations reaches a 104-task MiniWoB++ mean (0.9355) numerically equal to the crowd-human "
                                      "mean (0.9345) and far above aggregated published results on the 88 comparable tasks; within "
                                      "this architecture, demonstration scale and joint BC+RL are strong drivers, and multi-task "
                                      "co-training is more sample-efficient on the trained tasks."),
        "cannot_say": ["robustly human-level (parity flips without the latency-confounded moving-items task)",
                       "held-out task/site transfer (all evaluated tasks were trained)",
                       "pixel-only or non-DOM capability (75% drop without DOM)",
                       "data is the unique cause (BC weight co-varies; one architecture; one seed)"],
        "unresolved": ["Figure-only values (Fig 3/5/7/8) not visible in the fixed text; directions taken from author prose.",
                       "Evaluation episode count per task not stated.",
                       "No independent reproduction; all numbers author-reported."],
        "reproduction_note": "Aggregator recomputed Table 3 means only; nothing was run.",
    },
    "ratings": {
        "G": R("resolved", 3, "Specific, sourced bottleneck: original MiniWob BC with 17 h data barely beat random and the field inferred specialised DOM actions/curricula were needed; the paper isolates the residual question (generic BC+RL with a human-compatible interface at scale) and states remaining gaps (human intent, pixel-only, non-DOM). Taskwise comparison to prior work is given. Not 4: neighbour originals are not in the pinned pack and some prior numbers are figure-estimated; 'primary missing factor' is not separated from interface/architecture changes.",
               ["son55:E002", "son55:E004", "son55:E005", "agg:CC-A03", "son55:E019"], ["sol:E020"]),
        "M": R("resolved", 3, "Human-compatible action interface makes demonstrations usable; success-filtered BC supplies behavioural priors that solve the exploration problem RL alone cannot (book-flight permutations); joint BC+RL is a concrete, testable mechanism with distinguishable predictions (BC-only, RL-only, small-data regimes). Not 4: no pretrain-then-RL alternative, data and interface effects not separated, mechanism argued empirically.",
               ["sol:E003", "sol:E008", "sol:E010", "son55:E014", "agg:CC-A05"], ["son55:E008", "agg:CC-A07"]),
        "X": R("resolved", 3, "Observation/action spaces, architecture, hyperparameters (Table 1), filtering, no-op cleaving, BC:RL weighting, splits and privileged task-field dictionary are reconstructable; failure boundaries (simon-says at ~2 Hz, terminal, DOM reliance) are explicit. Not 4: LSTM not ablated in final config, evaluation episode count and harness equivalence to Selenium unvalidated.",
               ["sol:E005", "sol:E008", "sol:E009", "sol:E019", "sol:E004", "son55:E012"], ["sol:E006", "son55:E022"]),
        "E.measurement": R("resolved", 3, "Success is the programmatic MiniWoB++ reward on live episodes with a full per-task table and a same-interface human comparator. Residuals: the human-parity headline hinges on the latency-confounded moving-items task (agg:CC-A01/CC-A02); the external SotA aggregate mixes figure-estimated values and zero-filled tasks; episode counts unstated; no checker audit (E13).",
                           ["sol:E018", "son55:E025", "sol:E012", "sol:E021"], ["agg:CC-A01", "agg:CC-A02", "sol:E020", "son55:E019"]),
        "E.causality": R("resolved", 3, "Controls address each part of the central claim: BC-only (Table 3, mean 0.305) vs RL-only vs joint; data size over three orders with RL-only reference (1/1000 data gives no gain over RL-only); DOM/pixel/task-field input ablations; DOM-action output ablation; frame-matched multi- vs single-task. Not 4: one seed per condition, scaling co-varies BC weight (agg:CC-A07), no pretrain-then-RL alternative, most ablation values figure-only.",
                         ["son55:E014", "son55:E015", "son55:E016", "son55:E020", "son55:E025"], ["agg:CC-A07", "sol:E011", "son55:E008"]),
        "E.holdout": R("resolved", 2, "Evaluation tasks are the training tasks with new random instances; the human test split is used only for BC log-likelihood; 'cross-task transfer' is co-training sample efficiency, not held-out tasks; memorisation is argued by permutation counts, not audited. Matches the MiniWoB-scoped claim, but the abstract's transfer/generality wording exceeds it.",
                       ["son55:E020", "son55:E021", "sol:E009"], ["sol:E014", "agg:CC-A05"]),
        "E.statistics": R("resolved", 1, "One seed per condition (explicit), no intervals or repeated runs; per-task failures (simon-says, terminal) and the 104/88 denominators are reported, and the mean parity margin (0.001) is far inside the unquantified run-to-run variance.",
                          ["sol:E011", "sol:E013", "son55:E025"], ["agg:CC-A01"]),
        "E.cost": R("resolved", 2, "Data cost disclosed (2.4M demos, ~6300 h, 77 participants), 2B-frame scaling snapshot, 300-step cap and frame-matched multi-task comparison. Missing accelerator time/cost, inference latency, and budget matching against prior work that used ~400x less data.",
                    ["sol:E007", "sol:E019", "son55:E006", "sol:E014"], []),
    },
    "expectations": {
        "E03": {"applicable": True, "status": "partial", "score_item": ["E.measurement", "E.holdout"],
                "reason": "applies_when is met literally: a training method claimed to improve a web agent on locally served sites with programmatic checkers (MiniWoB++, all 104 tasks). WebArena did not exist in 2022 and cannot be required by name; status partial records the realism gap of synthetic widget tasks. Kept consistent with both seats' agreed E03=partial for WebGUM (2305.11854) on the same suite.",
                "evidence_ids": ["sol:E018", "son55:E025"]},
        "E07": "sol",
        "E13": "sol",
    },
    "resolutions": {
        "rs.primary": ("sol", "assumption_audit_and_pivot",
                       "The authors frame and test the paper as overturning an inferred necessity (agg:CC-A03, son55:E002): that is the assumption-audit signature. Unification of the interface is real but instrumental to that pivot, so it is retained as supporting, not primary (see rs.matches).",
                       ["agg:CC-A03", "son55:E002", "son55:E005"], "none on score (pattern matches are not scored)"),
        "rs.matches": ("revised", ["assumption_audit_and_pivot/None", "unify_into_shared_representation/None"],
                       "Both seats identified a real operation; each missed the other's. The unified human/agent keyboard-mouse interface and single 104-task policy is a distinct operation (agg:CC-A04, son55:E020) and qualifies as the one supporting card; sub-cards null for both (see rs reason).",
                       ["agg:CC-A04", "agg:CC-A03", "son55:E020"], "none on score"),
        "domain.matches": ("son55", ["trajectory_level_policy_training/None", "planner_grounder_interface/K29"],
                           "K29's operation (change the action abstraction the agent emits and train it to use it) is executed and ablated in Sec 3.4 (son55:E016, agg:CC-A06); parent explicitly covers 'change the action abstraction itself'. Fit partial; recorded a K29 counter-evidence proposal, no card edit.",
                           ["son55:E016", "son55:E017", "agg:CC-A06"], "none on score"),
        "rating.G": ("son55", {"status": "resolved", "rating": 3},
                     "Sol's deduction rests mainly on originals being absent from the pinned pack, which bounds verification, not the paper's gap quality. The fixed text gives a specific sourced bottleneck, taskwise neighbour comparison (Table 3) and explicit remaining gaps, i.e. above anchor 2; not 4 because the data-vs-interface framing is not separated.",
                     ["son55:E002", "son55:E004", "son55:E005", "agg:CC-A03"], "+3.75 vs sol (15*1/4)"),
        "rating.E.causality": ("son55", {"status": "resolved", "rating": 3},
                               "Sol's confounds (BC-weight coupling, LSTM parameters, external interface mismatch) are real but secondary: the central attributions (data scale, joint BC+RL, DOM vs pixels, action space, multi-task) each have an in-architecture control, and the small-data arm was given a tuning advantage rather than a handicap. Residuals keep it below 4.",
                               ["son55:E014", "son55:E025", "son55:E015", "son55:E016", "son55:E020", "agg:CC-A07"], "+2.5 vs sol (10*1/4)"),
        "expectation.E03": ("sol", "partial",
                            "applies_when literally met (training method, locally served web tasks with programmatic checkers); son55's not_applicable conflicts with both seats' agreed partial for WebGUM on the same suite. No score effect beyond the ratings above.",
                            ["sol:E018"], "none (expectation statuses inform, ratings are set separately)"),
        "expectation.E07": ("sol", "partial",
                            "applies_when is 'a trained end-to-end GUI agent model improves online task success', which CC-Net is; son55's not_applicable misreads the trigger. Same-backbone BC-only analog exists; later UI-TARS/agentic baselines cannot be required.",
                            ["son55:E025", "sol:E008"], "none"),
        "expectation.E13": ("sol", "unmet",
                            "The RL pipeline's reward comes from per-task MiniWoB checkers, so applies_when holds; no two-sided checker audit is reported. No checker failure is inferred; weight on E.measurement is light because tasks are templated.",
                            ["sol:E018"], "none (E.measurement stays 3)"),
    },
    "shared": [],
    "status": ("accepted_final", "All 8 mechanical conflicts resolved with fixed-text evidence; no unresolved scoring or core-claim dispute; full fixed HTML read (figures not rendered, limitation recorded)."),
    "unverifiable": {"son55:E028": REPLACED},
}

# ============================================================================================ 2304.07061 DroidBot-GPT
DB = {
    "pk": "2304.07061",
    "prelim": (
        "Read before seat scores. DroidBot-GPT serialises the DroidBot-extracted Android view tree into numbered natural-"
        "language element/action descriptions, adds task and action history, and asks ChatGPT (snapshot unstated) to pick an "
        "action ID (second call for typed text). Evaluation: 33 author-designed tasks on 17 F-Droid apps, one run, no baseline, "
        "no ablation, no cost. Progress = prefix match against one reference action sequence; the criterion for 'fully "
        "completes' is not stated as an execution/state check. Table 2/3 weighted means (67.51%/68.28%) do not reproduce "
        "the reported 66.76%. 'First' and 'generalises across more categories than prior work' are asserted without "
        "comparison. Prelim: G1-2 M2 X2 Em1 Ec0 Eh1 Es1 Ecost0; evidence_level cannot be online under EVIDENCE.md."),
    "materials": [("2304.07061", "paper")],
    "evidence": [
        A("2304.07061", "DB-A01", "2304.07061", "Sec 3.1",
          "In order to evaluate the model on the tasks not fully completed, we record the actions DroidBot-GPT generates, which are compared with the proper action sequence.",
          "The reference-sequence comparison is described for not-fully-completed tasks; how 'fully completes' is judged is not stated, and no device-state or execution-result check is described anywhere in the text."),
        A("2304.07061", "DB-A02", "2304.07061", "Sec 2.1",
          "we propose an alternative approach, which involves converting the GUI interface into a familiar natural language sentence that can be more readily processed by GPT models.",
          "Serialisation of the structured view tree into the surface form of a mature modality (natural language) so a pretrained LLM recipe applies: C18 tactic step 2."),
        A("2304.07061", "DB-A03", "2304.07061", "Table 1 caption",
          "World Weather (an application that reports current weather and forecasts around the world)",
          "At least some tested apps fetch live network content, so results depend on live app/content state that is not dated or versioned (E20)."),
        A("2304.07061", "DB-A04", "2304.07061", "Sec 3.1",
          "Compared to the previous works that are designed for a specific range of applications or actions",
          "Comparative superiority claim over prior systems (with different observation spaces and budgets) made without any measured comparison (triggers E17/E21)."),
        A("2304.07061", "DB-A05", "2304.07061", "Sec 1",
          "Besides, our system can even finish some complex tasks needing multiple GUI jumps",
          "Multi-step capability claim on the self-created task set (triggers E23)."),
    ],
    "rs": {"seat": "son55", "reason": ("son55 kept: primary adapt_via_conditioning/null (frozen ChatGPT solves each task from "
                                        "a prompt of task + serialized UI + history, no parameter update; C03's canonical-schema "
                                        "upstream training / category holdout absent). Supporting unify_into_shared_representation/C18 "
                                        "partial: a distinct operation serialises the view tree into natural language for a pretrained "
                                        "LLM (agg:DB-A02), but the serializer is never validated against the raw tree or alternatives.")},
    "domain": [("son55", "structured_screen_observation", "C01", "strong"),
               ("son55", "structured_screen_observation", "C13", "partial")],
    "domain_note": ("C01 strong: elements enumerated from the view hierarchy, numbered, actions restricted to IDs (missing unnamed "
                    "elements are unaddressable, matching C01's failure condition). C13 partial: only user-visible elements kept "
                    "and per-element text truncated to 20 words before the policy sees it; no token/success effect reported."),
    "gap_check": {
        "aggregator_check": ("No measured nearest-neighbour comparison anywhere in the fixed text; related work is only qualitative. "
                             "The 'first' claim cannot be certified from the pinned pack. son55's evidence for an earlier LLM+mobile-UI "
                             "neighbour (2209.08655) cites a file that has since been replaced and is not used here; the only "
                             "aggregator-verifiable fact is that 2304.07061v5's 24-item reference list contains no 2209.08655 entry."),
    },
    "claims_append": {
        "C1": ("[agg] Recomputed: Table 2 strata give a weighted mean progress of 67.51% and Table 3 categories 68.28%, "
               "neither equal to the reported 66.76% (both full-completion counts do sum to 13/33). The full-completion criterion "
               "itself is unstated (agg:DB-A01)."),
    },
    "assessment": {
        "evidence_level": "offline",
        "evidence_level_reason": ("Actions are executed live on a phone, but EVIDENCE.md 'online' requires task success determined by "
                                  "an execution-result check. The text gives a reference-sequence prefix metric and does not describe "
                                  "any state/outcome check for 'fully completes' (agg:DB-A01), so online cannot be certified; the "
                                  "result is a reference-trajectory-match measurement, recorded at the offline level with this "
                                  "qualification."),
        "claim_support": "scoped",
        "author_claim": "Off-the-shelf ChatGPT automates Android app tasks without app/model modification, generalising across more categories than prior specialised systems; first such work.",
        "strongest_supported_claim": ("Author-reported, one run: on 33 self-designed tasks in 17 F-Droid apps, prompting ChatGPT with a "
                                      "serialized DroidBot view tree yields 13 tasks judged fully completed and partial reference-path "
                                      "progress on others (reported 66.76%, internally inconsistent with Tables 2-3). Feasibility only; "
                                      "no comparative, causal or generalisation claim is supported."),
        "cannot_say": ["better than any prior system (no baseline)", "any design choice helps (no ablation)",
                       "stable (single run; authors report order variation on repeats)", "verified task success (no execution check)",
                       "first (no novelty search in pinned pack)"],
        "unresolved": ["ChatGPT snapshot/temperature, max steps and stop criterion unstated.",
                       "Full-completion criterion unstated.", "Figure 4 prompt example not rendered in fixed text."],
        "reproduction_note": "Aggregator recomputed table means only; nothing was run.",
    },
    "ratings": {
        "G": R("resolved", 2, "Real problem (natural-language automation of diverse apps without per-app development) and a plausible LLM-based response, but no measured nearest-neighbour comparison, an unverified 'first' claim, and residual problems described only qualitatively.",
               ["son55:E004", "son55:E005", "sol:E013", "sol:E019"], ["agg:DB-A04"]),
        "M": R("resolved", 2, "Concrete mechanism (view tree -> numbered NL descriptions, ID choice, history, two-step typing, parser fallback) with a partial causal account linking failures to unnamed elements; but no distinguishable prediction against naive alternatives (raw tree, no history, few-shot) and the 'LLM has read how-to manuals' rationale is asserted.",
               ["sol:E003", "sol:E004", "sol:E006", "agg:DB-A02", "son55:E024"], ["sol:E005", "sol:E008"]),
        "X": R("resolved", 2, "Main loop steps are described in prose; model version/settings, max steps, termination, history length, app launch, and the full-completion criterion are not, and the prompt example figure is not rendered. Failure boundaries are qualitatively explicit.",
               ["sol:E001", "sol:E006", "son55:E012", "son55:E014", "sol:E014"], ["agg:DB-A01", "son55:E015"]),
        "E.measurement": R("resolved", 1, "Single-reference prefix matching rejects valid alternative paths, the full-completion criterion is unstated with no execution-state check, the task set is author-built, and the reported 66.76% does not reproduce from Tables 2-3 (67.51%/68.28%).",
                           ["sol:E009", "sol:E010", "son55:E019"], ["agg:DB-A01", "sol:R001", "sol:R002"]),
        "E.causality": R("not_reported", 0, "After a complete search of methods, evaluation, limitations and related work, no baseline, ablation or control is reported; the comparative claims over prior work (agg:DB-A04) have no measured support.",
                         ["agg:DB-A04", "son55:E027"], [], FULL_SCOPE("2304.07061")),
        "E.holdout": R("resolved", 1, "One author-built 33-task set; the 20-word truncation was tuned 'based on our experiments' with no separate development split; no app-version/LLM-exposure audit; 'generalises across categories' is not tested against held-out categories.",
                       ["sol:E007", "sol:E008"], ["son55:E022"]),
        "E.statistics": R("resolved", 1, "Denominators by complexity and category are given (2-6 tasks per category), and failure types are named, but one run with admitted nondeterminism, no intervals, no failure counts, and an internally inconsistent headline mean.",
                          ["sol:E011", "sol:E012", "son55:E018", "son55:E023"], ["sol:E016", "son55:E019"]),
        "E.cost": R("not_reported", 0, "No tokens, calls, latency, dollar cost, step cap or budget comparison anywhere in the fixed text; the second typing call means step counts are not a cost proxy.",
                    ["sol:E004"], [], FULL_SCOPE("2304.07061")),
    },
    "expectations": {
        "E02": {"applicable": True, "status": "partial", "score_item": ["E.measurement", "E.holdout"],
                "reason": "Partly met in spirit: tasks run closed-loop on real apps, not offline AITW/AndroidControl step metrics. Unmet part: no execution-checked success and no public benchmark (AndroidWorld postdates the paper and is not required by name).",
                "evidence_ids": ["son55:E008", "sol:E010", "agg:DB-A01"]},
        "E15": "son55",
        "E17": "sol",
        "E20": {"applicable": True, "status": "unmet", "score_item": ["E.measurement"],
                "reason": "Results are measured on installed real apps, some fetching live network content (agg:DB-A03); neither evaluation date nor app versions nor drift/blocked-task handling is reported. Naming F-Droid as source does not meet the requirement.",
                "evidence_ids": ["agg:DB-A03", "sol:E007"]},
        "E21": "sol",
        "E23": "son55",
    },
    "resolutions": {
        "evidence_level": ("son55", "offline",
                           "EVIDENCE.md defines online by an execution-result success check. The fixed text only describes reference-sequence comparison and leaves the full-completion criterion unstated (agg:DB-A01); sol itself notes there is no audited goal checker. Live execution alone does not earn 'online'. Recorded as offline with the live-execution qualification in evidence_level_reason.",
                           ["agg:DB-A01", "sol:E009", "son55:E008"], "none (evidence_level is listed separately and not scored)"),
        "rs.supporting": ("son55", ["unify_into_shared_representation"],
                          "Serialising the GUI tree into natural language for a pretrained LLM is a distinct, explicitly motivated operation (agg:DB-A02), matching C18 step 2; it is not just a restatement of conditioning.",
                          ["agg:DB-A02", "son55:E009"], "none on score"),
        "rs.matches": ("son55", ["adapt_via_conditioning/None", "unify_into_shared_representation/C18"],
                       "Primary agreed; supporting C18 added for the serializer operation; C18 under unify_into_shared_representation is a valid parent/child pair.",
                       ["agg:DB-A02", "sol:E003"], "none on score"),
        "domain.matches": ("son55", ["structured_screen_observation/C01", "structured_screen_observation/C13"],
                           "Visible-element filtering and 20-word truncation before the policy sees the list is C13's prune/restructure operation (sol:E002, sol:E008); partial because no token/success effect is reported.",
                           ["sol:E002", "sol:E008", "son55:E015"], "none on score"),
        "expectation.E02": ("sol", "partial",
                            "Live closed-loop execution on real apps meets the 'not only offline step metrics' half; absence of execution-checked success leaves the other half unmet. 'unmet' would ignore the live execution that does exist.",
                            ["son55:E008", "agg:DB-A01"], "none"),
        "expectation.E15": ("son55", "unmet",
                            "The capability claim rests on a reference-path proxy with no execution-checked success and no evidence the proxy predicts success; closed-loop generation does not satisfy the expectation's remedy.",
                            ["sol:E009", "agg:DB-A01"], "none (E.measurement stays 1)"),
        "expectation.E17": ("sol", "unmet",
                            "Triggered by the measured-free comparative claim over prior systems (agg:DB-A04). After full search no step cap, budget or exhaustion is reported; a reporting requirement found absent in complete text is unmet, not unknown.",
                            ["agg:DB-A04"], "none (E.cost stays 0)"),
        "expectation.E20": ("revised", {"applicable": True, "status": "unmet"},
                            "Applies (live real apps with network content, agg:DB-A03) contrary to son55; but sol's 'partial' credits only the app-store name, while date, versions and drift handling are all absent.",
                            ["agg:DB-A03", "sol:E007"], "none"),
        "expectation.E21": ("sol", "partial",
                            "Same trigger as E17: the paper compares itself with prior agents using different observation spaces (agg:DB-A04). Its own observation channel (view-tree text only) is clearly stated, but no matched comparison exists.",
                            ["agg:DB-A04", "sol:E002"], "none"),
        "expectation.E23": ("son55", "partial",
                            "Applies (self-created task set plus multi-jump capability claim, agg:DB-A05). Stratification by reference length is met (Table 2), but failure causes are named qualitatively without counts per stratum, so the audit half is only partial.",
                            ["sol:E011", "sol:E012", "sol:E014", "agg:DB-A05"], "none"),
    },
    "shared": [
        {"field_path": "claims[C1].result / assessment (full-completion criterion)",
         "sol_value": "13/33 complete according to reference-path comparison",
         "son55_value": "成败由与单一参考序列的前缀匹配得出",
         "error": "Both seats state that full completion was judged by reference-sequence matching. The text describes the reference comparison only 'to evaluate the model on the tasks not fully completed' and never states how full completion was judged.",
         "correction": "Final record treats the full-completion criterion as unstated. Either way no execution/state check is documented, so evidence_level=offline and E.measurement=1 are unchanged.",
         "evidence_ids": ["agg:DB-A01"], "score_impact": "none"},
    ],
    "status": ("accepted_final", "All 10 mechanical conflicts resolved; ratings agree between seats and were independently re-derived; no unresolved scoring or core-claim dispute."),
    "unverifiable": {"son55:E029": REPLACED},
}

# ============================================================================================ 2305.11854 WebGUM
WG = {
    "pk": "2305.11854",
    "prelim": (
        "Read before seat scores. WebGUM jointly finetunes Flan-T5 + ViT (temporal H=2, local patch tokens) on success-filtered "
        "agent rollouts (WebN-T5 -> own Flan-T5-XL policy; 347K) plus 54K Synapse/PaLM-2 demonstrations and a scripted "
        "book-flight policy (401K), emitting text actions over integer element selectors. Online evidence: MiniWoB++ (56 tasks, "
        "100 episodes each, time limit ignored, one seed) and WebShop (500 instructions, in-domain finetune); Mind2Web is "
        "offline step-level after target finetuning. Same-data controls exist (T5 vs Flan-T5 49.8->75.5 at 347K XL; HTML vs "
        "HTML+Image; white/random images; token types; data/model scaling). Headline confounds: 401K vs 347K adds ~14 pp "
        "(80.3 -> 94.2) unablated; headline 'beats CC-Net/humans/GPT-4' compares a 56-task mean with 104/54-task means; "
        "white images alone give +2.2 of the +5.5 image gain. Mind2Web gains over same-backbone MindAct are small. "
        "Prelim: G3 M3 X3 Em3 Ec2-3 Eh2 Es1 Ecost2."),
    "materials": [("2305.11854", "paper")],
    "evidence": [
        A("2305.11854", "WG-A01", "2305.11854", "Appendix G Table 8 (# of Tasks row, with full-table recomputation)",
          "# of Tasks | 63 | 104 | 53 | 54 | 54 | 104 | 104 | 48 | 56 | 56 | 56",
          "Aggregator recomputation on tasks where WebGUM is scored: CC-Net 0.964 vs WebGUM 0.942 (56 tasks); Human 0.945 vs 0.942 (56); RCI-GPT-4 0.941 vs 0.937 (51); Synapse 0.986 vs 0.939 (54); AdaPlanner 0.930 vs 0.937 (51); RCI-GPT-3.5 0.904 vs 0.937 (51). The abstract's 'outperforming online-finetuned SoTA, humans, and GPT-4-based agent' reverses on matched tasks.",
          "our_inference"),
        A("2305.11854", "WG-A02", "2305.11854", "Sec 5.1",
          "the performance of the model with white images is comparable to the unimodal model.",
          "Fig 3 table: HTML 88.7, white 90.9, random 92.2, real 94.2. A blank image already adds +2.2 pp, so at most +3.3 pp of the +5.5 pp HTML->HTML+Image gain is attributable to image content (single seed)."),
        A("2305.11854", "WG-A03", "2305.11854", "Appendix F",
          "also write a scripted policy for book-flight",
          "Part of the 401K headline corpus comes from a hand-scripted policy and a prompted PaLM-2 agent (54K), i.e. privileged supervision beyond the self-generated 347K; Table 5 XL multimodal at 347K is 80.3% vs 94.2% at 401K."),
        A("2305.11854", "WG-A04", "2305.11854", "Appendix H Table 9",
          "click-link_click-dialog | 0.55 | 0.00 | 0.93 | 0.95",
          "Synapse scores 0.00 on one of six compositional tasks and is higher than WebGUM on 4/6; the average advantage (0.785 vs 0.738) rests on this single task."),
    ],
    "rs": {"seat": "son55", "reason": ("son55 kept: primary unify_into_shared_representation/C18 (recast web navigation as "
                                        "text,image->text and bridge screenshot patches into a pretrained T5 so the mature "
                                        "seq2seq recipe applies); supporting self_supervised_signal_engineering/C08 partial "
                                        "(policy rollouts filtered by environment success, iterated twice, released as a 347K "
                                        "corpus; gate is an executable reward rather than a model self-signal, and no filter-"
                                        "removal ablation).")},
    "domain": [("son55", "trajectory_level_policy_training", None, "partial"),
               ("son55", "structured_screen_observation", "C01", "partial")],
    "domain_note": "No domain conflict between seats; son55's entries kept (C01 fit partial because the screenshot is an auxiliary channel and no marks are drawn).",
    "gap_check": {
        "aggregator_check": ("Gap (offline training lagging online RL; web-specific architectures blocking foundation-model priors; "
                             "no multimodal demonstrations) is specific and sourced; WebN-T5 is the clear nearest neighbour. Verified "
                             "son55's matched-task recomputation (agg:WG-A01): 'offline matches online RL' does not hold on common tasks, "
                             "while 'far above offline HTML-LM WebN-T5' does. Mind2Web GPT-4 row used 50 tasks/top-10 candidates in the "
                             "Mind2Web paper (son55:E056), unlike WebGUM's setting."),
    },
    "claims_append": {
        "C1": ("[agg] Verified on Table 8 (agg:WG-A01); additionally RCI-GPT-4 0.941 > WebGUM 0.937 on 51 common tasks, so the "
               "abstract's GPT-4-agent superiority also reverses. Evaluation ignored the MiniWoB time limit (sol:E038)."),
        "C2": ("[agg] White images alone give +2.2 pp over HTML-only (agg:WG-A02); image-content-attributable gain is at most "
               "+3.3 pp of the +5.5 pp, single seed."),
        "C3": "[agg] Compositional average advantage over Synapse hinges on one task where Synapse scores 0.00 (agg:WG-A04).",
    },
    "assessment": {
        "evidence_level": "online",
        "evidence_level_reason": ("MiniWoB++ and WebShop success are environment-checked. Training data was generated in the same "
                                  "MiniWoB task families and WebShop was finetuned in-domain; Mind2Web is offline step-level after "
                                  "target finetuning, so transfer is not reached."),
        "claim_support": "scoped",
        "author_claim": "Offline instruction-tuned multimodal recipe surpasses prior offline/online SoTA, humans and GPT-4 agents on MiniWoB++, beats PaLM-540B on WebShop, and transfers strongly to real-world Mind2Web.",
        "strongest_supported_claim": ("Author-reported, one seed: an offline-trained Flan-T5-XL+ViT policy reaches 94.2% on 56 "
                                      "MiniWoB++ tasks (time limit ignored), far above the offline HTML-LM WebN-T5 (48.4%) and close "
                                      "to, but on matched tasks below, CC-Net, humans and RCI-GPT-4; instruction tuning (+25.7 pp at "
                                      "equal data/size) and visual tokens (<= +3.3 pp content-attributable) both help; 45.0% on "
                                      "WebShop after in-domain finetuning; small offline Mind2Web gains over same-backbone MindAct."),
        "cannot_say": ["beats CC-Net, humans or GPT-4 agents (reverses on matched tasks)",
                       "94.2% comes from the architecture/recipe alone (54K Synapse/scripted data adds ~14 pp)",
                       "strong real-world transfer (offline, re-finetuned, 0.1-3.3 pp task-SR gains, single seed)",
                       "multi-step reasoning is the causal mechanism (not isolated)"],
        "unresolved": ["Effect of ignoring the MiniWoB time limit not quantified.", "54K teacher data excluded from release.",
                       "Sec 5.2 '2.8K -> 66.1%' conflicts with Table 4 (61.1% at 2.8K)."],
        "reproduction_note": "Aggregator recomputed Table 8/9 means only; nothing was run.",
    },
    "ratings": {
        "G": R("resolved", 3, "Specific, sourced bottlenecks (offline policies lag online RL; web-specific DOM architectures and categorical outputs block pretrained priors; no multimodal demonstrations) with WebN-T5/CC-Net/MindAct lineage checkable; residuals stated (real sites, memory tasks). Not 4: firstness/closest originals not in pack and the 'match online RL' gap is not actually closed on matched tasks.",
               ["son55:E005", "son55:E006", "sol:E012", "son55:E023"], ["agg:WG-A01"]),
        "M": R("resolved", 3, "Each design piece targets a named bottleneck (local/temporal visual tokens for grounding and transitions, instruction-tuned LM for HTML comprehension, filtered rollouts for data, text actions for open output) and yields testable predictions (white/random images, vanilla T5, perturbations, compositions). Not 4: reasoning mechanism asserted, teacher-data coverage not separated from model changes.",
               ["sol:E001", "sol:E003", "sol:E004", "sol:E006", "son55:E007"], ["sol:E044", "agg:WG-A03"]),
        "X": R("resolved", 3, "Architecture, token counts, batch/sequence length, compute, two-round data generation with success filter, 54K/scripted supplements, 100-episode protocol and Mind2Web setup are reconstructable; failures explicit. Not 4: private 54K data excluded from release, per-task teacher mix and training-step details thin, time limit ignored.",
               ["sol:E002", "sol:E005", "sol:E007", "sol:E008", "sol:E035", "son55:E060"], ["sol:E036", "son55:E020", "sol:E038"]),
        "E.measurement": R("resolved", 2, "Own MiniWoB++/WebShop successes are environment-checked with explicit denominators, but the central comparative claims are not measured on a common basis: different task sets (56 vs 104/54/63; reversal on matched tasks, agg:WG-A01), MiniWoB time limit ignored for WebGUM only, baselines copied from other papers, Mind2Web GPT-4 row on a different subset/candidate setting, and a text/table inconsistency (2.8K/66.1).",
                           ["sol:E010", "sol:E025", "sol:E041", "son55:E021"], ["agg:WG-A01", "sol:E038", "sol:E047", "son55:E056", "sol:E021"]),
        "E.causality": R("resolved", 3, "Same-data/same-size controls support the component claims: T5-XL 49.8 vs Flan-T5-XL 75.5 at 347K; HTML vs HTML+Image with white/random controls; temporal vs local tokens; ViT pretraining; data and model scaling incl. decoder-only Flan-PaLM. Not 4: the headline 94.2 is confounded by unablated 54K Synapse/scripted data (+~14 pp, agg:WG-A03), content-attributable image gain is <= 3.3 pp (agg:WG-A02), reasoning not isolated, single seed.",
                         ["son55:E036", "son55:E037", "sol:E013", "sol:E014", "sol:E015", "sol:E017", "son55:E039"], ["agg:WG-A03", "agg:WG-A02", "sol:E032"]),
        "E.holdout": R("resolved", 2, "Main MiniWoB result is in-distribution (training data generated on the evaluated task families); genuine held-out checks exist but are small or weak: 6 stitched click compositions (advantage over Synapse hinges on one task, agg:WG-A04), HTML-side perturbations vs one baseline, Mind2Web held-out splits offline after target finetuning with 0.1-3.3 pp task-SR gains; WebShop in-domain. 'Strong positive transfer' exceeds the evidence.",
                       ["sol:E018", "sol:E020", "sol:E028", "sol:R002", "son55:E051"], ["agg:WG-A04", "son55:E052", "son55:E053", "sol:E035"]),
        "E.statistics": R("resolved", 1, "One training seed per model (explicit), no intervals; 100 episodes/task and 500 WebShop instructions give denominators, but several reported differences (+0.7 vs CC-Net, +2.2 white image, Mind2Web +0.1 SR) are within unquantified seed variance (MindAct reports 0.2-0.8 SD).",
                          ["sol:E032", "sol:E010", "sol:E041"], ["son55:E057", "agg:WG-A01"]),
        "E.cost": R("resolved", 2, "Training compute (TPU-v4 256/512 cores, 1-2 days), parameter counts, rollout counts and dataset sizes reported. Missing teacher/collection cost (PaLM-2 Synapse calls, 10,000 rollouts/task), inference cost, and equal step/time budgets with baselines (time limit ignored).",
                    ["sol:E033", "sol:E007", "sol:E008", "son55:E060"], ["sol:E038"]),
    },
    "expectations": {
        "E13": "sol",
        "E17": "son55",
        "E23": "son55",
        "E27": "son55",
        "E28": "sol",
    },
    "resolutions": {
        "rs.supporting": ("son55", ["self_supervised_signal_engineering"],
                          "Generating training trajectories by model rollouts, filtering by success and iterating (sol:E007, sol:E008, sol:E035) is a distinct operation from the representation unification and is a stated contribution (347K corpus); fits C08's generate-then-gate tactic. Partial: gate is an external executable reward and no filter-removal ablation.",
                          ["sol:E007", "sol:E008", "sol:E035", "son55:E014"], "none on score"),
        "rs.matches": ("son55", ["self_supervised_signal_engineering/C08", "unify_into_shared_representation/C18"],
                       "Primary C18 agreed; C08 added as supporting (valid parent self_supervised_signal_engineering).",
                       ["sol:E001", "sol:E003", "sol:E035"], "none on score"),
        "rating.E.measurement": ("son55", {"status": "resolved", "rating": 2},
                                 "Sol's own reason concedes 'broad baseline aggregates not comparable'. The abstract-level claims are comparative and the comparison basis is broken: matched-task recomputation reverses superiority over CC-Net, humans and RCI-GPT-4 (agg:WG-A01), and the time limit was ignored only for WebGUM (sol:E038). Own environment-checked numbers keep it above 1.",
                                 ["agg:WG-A01", "sol:E038", "sol:E047", "son55:E021"], "-2.5 vs sol (10*1/4)"),
        "rating.E.causality": ("son55", {"status": "resolved", "rating": 3},
                               "The component attributions each have a same-data, same-size control (T5 vs Flan-T5; image vs white/random; token types; scaling). Sol's confounds bear on the headline number and on the 'reasoning' mechanism, which remain residuals (agg:WG-A03, agg:WG-A02), not on the controlled component effects.",
                               ["son55:E036", "son55:E037", "sol:E013", "sol:E014", "sol:E017"], "+2.5 vs sol (10*1/4)"),
        "rating.E.holdout": ("son55", {"status": "resolved", "rating": 2},
                             "Held-out tests exist (compositions, perturbations, Mind2Web splits) but the main corpus is generated on the evaluated families, the compositional edge hinges on one task (agg:WG-A04), and Mind2Web gains are offline, re-finetuned and small. Sol's 3 credits the number of tests rather than their support for the claimed 'strong transfer'.",
                             ["agg:WG-A04", "son55:E052", "son55:E053", "sol:E028"], "-2.5 vs sol (10*1/4)"),
        "expectation.E13": ("sol", "unmet",
                            "The data pipeline selects training trajectories by the per-task MiniWoB checker reward and evaluation uses it, so applies_when holds (consistent with 2202.08137 in this batch); no two-sided checker audit.",
                            ["sol:E035", "sol:E046"], "none (E.measurement set on other grounds)"),
        "expectation.E17": ("son55", "unmet",
                            "Budgets are known to differ: WebGUM ignored the time limit while baselines were reported under their own protocols; no max-step or exhaustion report. Disclosing 100 episodes is a sample size, not a step budget, so 'partial' overstates.",
                            ["sol:E038", "son55:E026"], "none (E.cost stays 2)"),
        "expectation.E23": ("son55", "not_applicable",
                            "No new benchmark (a dataset is released, not a benchmark) and no long-horizon capability claim; MiniWoB/WebShop episodes are short and the multi-step-reasoning claim is about priors, judged under E.causality.",
                            ["sol:E043", "son55:E062"], "none"),
        "expectation.E27": ("son55", "partial",
                            "Curve 2.8K/68K/347K is shown, but the expectation also asks where it saturates; not stated, and the headline 401K point (with teacher data) is off the curve; main-text 2.8K value conflicts with Table 4.",
                            ["son55:E039", "son55:E040", "sol:E021", "sol:E022"], "none"),
        "expectation.E28": ("sol", "partial",
                            "Synthesis and evaluation share MiniWoB task families (unmet half), but OOD transfer is reported on never-synthesised compositions and held-out Mind2Web splits (met half, albeit weak), so 'unmet' ignores the reported OOD tests.",
                            ["sol:E019", "sol:E028", "son55:E043"], "none (E.holdout set at 2)"),
    },
    "shared": [
        {"field_path": "claims[C2] (visual-modality gain attribution)",
         "sol_value": "correct visual 94.2 vs 90.9 white/92.2 random; 'Visual token construction ... improve measured performance'",
         "son55_value": "HTML 88.7 -> 94.2 (+5.5) as the visual gain; '总体 +5.5'",
         "error": "Both seats accept the authors' 'white images comparable to the unimodal model' framing. Blank images already add +2.2 pp over HTML-only, so the +5.5 pp HTML->HTML+Image difference is not all image-content gain.",
         "correction": "Image-content-attributable gain is at most +3.3 pp (94.2-90.9), single seed; recorded in claims C2 note and in E.causality reason.",
         "evidence_ids": ["agg:WG-A02", "sol:E013", "sol:E014"], "score_impact": "none (confirms E.causality=3, not 4)"},
    ],
    "status": ("accepted_final", "All 10 mechanical conflicts resolved with fixed-text evidence and recomputation; one shared attribution error corrected without score impact; no unresolved scoring or core-claim dispute."),
    "unverifiable": {"son55:E064": REPLACED},
}

PAPERS = [CC, DB, WG]
