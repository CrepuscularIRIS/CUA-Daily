# Correct but late: pre-compiled policy trees take decoding off the decision-time critical path

*A CUA Radar reading of arXiv 2607.28399v1 (Zihan Dong, Rui Qian, Qishi Zhan, Dongshen Peng, Kaixin Li, Yu Li). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2607.28399v1 · No code repository is listed on the board.*

## The problem: the right action arrives after the window closes

Most computer-use agents loop: capture a screenshot, call a multimodal model, execute one action, observe again. Boot prompts, auto-dismissing dialogs, transient toasts and reaction-time game states open and close faster than that loop completes. The paper’s diagnosis, in its own words: “the typical failure is not wrong understanding but late understanding” — the agent computes the right action after the window has already closed. Two explanations are possible: the agent fails to anticipate, or it anticipates but is defeated by where its computation happens. The paper holds the model, task, and information fixed and manipulates exactly one thing: whether generation occurs on the decision-time critical path.

## What AAPT is

The method is Adaptive Anticipatory Policy Trees (AAPT). The agent perceives 30 FPS screenshots through a pixel-difference change gate (a frame counts as changed when at least 0.5% of pixels differ by 20 grayscale levels or more, with a probe frame forced every 500 ms so a stalled screen cannot silence the observer). It acts with allowlisted keypress primitives; nothing outside the tree’s pre-authorized actions ever executes. The platform is a desktop timing benchmark the authors built, key_prompt, plus 39 external DynaCU-Bench web tasks. On the CUA Radar board the architecture sits in pattern C17, a manager that plans and a worker that executes — here a slow planner and a fast observer drawn from the same frozen checkpoint.

The mechanism is scheduling, not learning. While the screen is quiet, the frozen model compiles a flat conditional policy tree — observable guards, pre-authorized actions, per-branch deadlines, calibrated confidence, risk class — sized to cover the planner’s own decoding latency: T_cover ≥ L_p95 + M, with a 500 ms margin. At event time a low-token observer (64-token output cap, chosen by sweep) returns one JSON object, {branch_id, confidence, reason}; the runtime checks eligibility, a planner-confidence floor, and the decision age against the branch deadline, then fires the pre-authorized action. A no-match, ambiguity, or expiry falls back to replanning. There is no training signal at all: no fine-tuning anywhere, guided JSON decoding (vLLM’s guided_json backed by xgrammar, planner temperature 0.2), and one bounded resample when post-hoc validation rejects a tree.

## Results, as reported

Everything below is online, deterministically scored server-side: a trial succeeds only if the requested keypress reaches the server before the deadline. All comparisons are paired per-seed — 42 pairs per block, a byte-identical hidden schedule within each pair, condition order alternated — assessed with exact two-sided McNemar tests on frozen models, with pre-registered windows, seeds and endpoints. The primary model is Holo-3.1-35B-A3B; step budgets do not apply (one decision per trial), and seed ranges are pre-registered and never reused.

| Comparison (condition, window) | Reactive R0 | AAPT T2 | exact McNemar p |
|----|----|----|----|
| Contested scan, 600 ms | 4/42 (0.095) | 29/42 (0.690) | 6.0×10⁻⁸ |
| Contested scan, 650 ms | 12/42 (0.286) | 30/42 (0.714) | 4.0×10⁻⁵ |
| Declared primary, 650 ms | 21/42 (0.50) | 33/42 (0.79) | 1.8×10⁻³ |
| Fresh seeds, 550 ms, pooled 84 pairs | 0.143 | 0.619 | 1.8×10⁻¹² |
| Qwen3.6-35B-A3B, 600 ms, pooled 126 pairs | 0.341 | 0.778 | 4.9×10⁻¹³ |
| DynaCU-Bench transfer, 39 tasks | 7/39 (0.18) | 6/39 (0.15) | 1.0 (tie) |

At 500 ms, below the reactive floor, T2 scores 28/42 against R0’s 0/42. Incorrect actions from T2 were 0 at every window; on the Qwen3.6 primary block the reactive arm’s incorrect-action rate was 0.57. The latency story behind the numbers: the reactive round trip is 567 ms p50 against AAPT’s ~325 ms routing call, while the planner’s 1.81 s p50 compilation happens before the event. The premium is real — T2 generates 3.2× R0’s completion tokens per trial (342.8 vs 105.8; the observer call is actually cheaper, 59.3 vs 105.8 tokens), wall time rises from 1.65 s to 3.32 s, and 1.27 trees are compiled per successful trigger. There are no offline metrics in the paper; every number above is online.

## What the paper’s own controls say

- **Acting early is not enough.** The open-loop baseline R1 and the predict-and-replan baseline P1 (a receding-horizon control in the spirit of TraceR1) both act before a full round trip and both score zero at the contested windows, because they still decode during execution.
- **Oracle routing bounds the observer.** O1 routes with ground truth at zero decision latency and sits above T2, but the gaps do not survive Holm–Bonferroni; the paper reads them as headroom — the binding constraint is the observer, not the planner.
- **The sizing rule predicts the onset.** In a preparation-time sweep, T2 scores 0/42 with 0.5–1 s of prep (the event fires mid-compile), ties R0 at 2 s (36/42 vs 37/42), and reaches 42/42 at 4 s: the crossover brackets L_p95 + M ≈ 2.4 s. All starved-prep failures are misses, never wrong actions.
- **The branch budget has a knee.** In the k × n sweep at 600 ms, the cell (k=3, n=1) — one branch per outcome — succeeds on all 42 pairs (19/0 discordants, p = 3.8×10⁻⁶) against a shared reactive arm at 0.548; budgets below the outcome-set size fail mainly through planner tree validity. An observer token-cap sweep picks 64 tokens (0.833 pooled) over 32 (0.571, truncation) and 128 (0.690, branch accuracy below the gate).
- **Three capability gates, six models.** The gain appears only where observer decode is sub-second, flat-tree validity holds, and branch accuracy reaches 0.85. UI-Venus-1.5-30B-A3B is fast and schema-valid but routes at 0.39 accuracy and ties R0 (11/42 vs 13/42, p = 0.625); swapping its observer for ground-truth routing flips the tie to a win (22/42 vs 12/42, p = 0.021) — the probe the paper had pre-registered with the opposite prediction, and reports as failed. EvoCUA-32B’s ~2.5 s observer loses outright (T2 0/43 vs R0 22/43); UI-TARS-1.5-7B fails the validity gate and is stopped by protocol.
- **A boundary, not a blanket win.** On DynaCU-Bench the aggregate is a tie, and the discordant wins split by structure: all four AAPT-only wins are dashboard deadlines with pre-enumerable responses (fired 140–215 ms after the gated frame), while the five reactive-only wins need multi-step sequencing or late-revealed values. Randomizing the event delay over \[500, 1000\] ms leaves the advantage unchanged (15/0 discordants, p = 6.1×10⁻⁵).

## Where the evidence is thinner, in the paper’s words

The positive result “is confined to two Qwen3.5-MoE checkpoints on one controlled scenario family”; the three-outcome key_prompt event “was designed to isolate the mechanism, not to represent computer use broadly.” The DynaCU dissociation “rests on 4 versus 5 discordant tasks.” Contested-window rates are seed- and latency-sensitive — “only paired per-seed comparisons carry evidential weight” — and absolute rates should not be quoted outside their seed sets; a ~100 ms serving shift moved the five-outcome 900 ms block from contested to ceiling and produced a null (R0 42/42, T2 38/42, p = 0.125), reported verbatim. UI-Venus tree coverage shifted between sessions (outcome recall 0.22 vs 0.59 under identical config and compile key), and a compiled-kernel change once moved tree validity from 88.1% to 18.3% under identical weights. The click_target scenario was dropped because both arms fail for independent reasons (the reactive arm misses a 90 px target by a 229 px median; the tree cannot bind coordinates revealed only at fire time). Asynchronous tree refresh, reusable policy memory, and any fine-tuning remain untested.

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **online**. The judgment record credits the deterministic online scoring (“a trial succeeds only if the requested keypress reaches the server before the deadline”), the external DynaCU-Bench pairing on 39 deterministic tasks, fresh-seed replication of the direction, a full cost ledger, and the component ablations. It flags AP15 — scaffold gains assumed to transfer across backbones — which the paper itself maps with its six-model gate matrix, and it records code as unclear and baselines as only partially budget-matched (T2 spends 3.2× the completion tokens). The radar did not rerun anything; every number above comes from the paper (version v1).
