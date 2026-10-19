# Localise Small Targets with Resolution, Zoom, Verification and Pointer Heads
_id: `high_resolution_target_localisation` · sub-patterns: C05, C06, C07, C08, C09 · 2 candidate_pattern · 3 case · domains: cua-agents-core (0 K / 5 C) · outcome labels: none in this build_

**Definition.** Improve pixel-level localisation on high-resolution, dense screens by changing how the model sees or points rather than what data it is trained on: a cheap high-resolution detail channel beside a low-resolution global view, skipping redundant visual tokens in uniform UI regions, zoom-and-reground search around a first prediction, cropping and verifying candidate targets against the goal, or a coordinate-free attention head over visual patches.

**Operational signature.** encode the screenshot (low-res global view + high-res detail channel, or with redundant tokens skipped) → propose a target (coordinate tokens or patch attention) → crop/zoom around the proposal → re-ground or verify the crop against the goal → click the first verified target

**When to apply.** When targets are small relative to the screen (professional, high-resolution desktop software, elongated mobile screens) and errors fall near the target, i.e. the plan is right but fine localisation misses.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [C05](../sub/C05.md) | case | Coordinate-free grounding with an attention action head over visual patches | replace numeric coordinate tokens with a special <ACTOR> token whose hidden state is matched against contextualised patch features to give… |
| [C06](../sub/C06.md) | candidate_pattern | Crop the proposed target and verify it against the goal before acting | crop the screenshot around a candidate click target (optionally marking the point), ask a verifier model whether the crop shows the goal,… |
| [C07](../sub/C07.md) | case | Zoom-and-reground search for targets on high-resolution professional screens | ground on the full screenshot, then crop around the prediction (or around planner-proposed areas scored by grounded neighbour votes) and… |
| [C08](../sub/C08.md) | candidate_pattern | Supplement a low-resolution global view with a cheap high-resolution detail channel | keep the backbone's low-resolution global image and add high-resolution detail through a separate path: a small high-res encoder read by… |
| [C09](../sub/C09.md) | case | Skip redundant visual tokens in uniform UI regions | build a graph of same-colour neighbouring patches (union-find) and randomly skip a fixed ratio of tokens inside multi-patch components in… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Evaluated on high-resolution professional screens.** Results are reported on a high-resolution professional benchmark such as ScreenSpot-Pro, where base grounders are weak and the method's gain is large (cropping around the first prediction: OS-Atlas-7B 18.9 -> 40.2) (2504.07981#s1, 2504.07981#s2, 2506.03143#s1).
- **Same-data baseline isolates the architecture.** The new head or encoding is compared with coordinate generation trained on the same data (ScreenSpot-Pro 40.7 vs 15.6 for Aguvis-7B point supervision), or architecture and data gains are ablated separately (2506.03143#s1, 2312.08914#s1).
- **Zoom parameters matched to the grounder.** Crop size is tuned to the grounder's input resolution and the zoom step is applied around the first prediction or around planner-proposed areas scored by grounded neighbour votes (48.1% without training) (2504.07981#s2, 2504.07981#s3).
- **Verification over diverse candidates.** A verifier checks several diverse candidates emitted in one grounding pass and the agent acts on the first verified one (ScreenSpot-Pro +3.5 to +12.9) (2506.03143#s3).
- **Efficiency gain measured at held accuracy.** A high-res channel or token skipping reports compute savings at near-equal accuracy and beats simple alternatives (>10x FLOPs reduction at 1120; 33% tokens removed, 1.4-1.5x speedup, ScreenSpot 70.4 vs 70.8, vs token merging 42.3 and random selection 65.3) (2312.08914#s1, 2411.17465#s1).
- **Region-level supervision for the pointer.** The pointing head is trained against the target region (box-rasterised patch mask) rather than a single point, tolerating spatial ambiguity (2506.03143#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Sub-patch and icon targets remain weak.** Elements smaller than one patch are under-represented (CAD-like precision tasks) and icon accuracy stays low (ScreenSpot-Pro icon 16.4; zoom search icon 22.4%) (2506.03143#s1, 2504.07981#s3).
- **Extra model calls without cost accounting.** Sequential verifier, planner and grounder calls are added per candidate or per action (3.3-5.5 queries per action) while cost/latency is not reported (2506.03143#s3, 2504.07981#s3, 2607.04334#s4).
- **Regressions on easier benchmarks or other platforms.** The method has small or negative effect on easier benchmarks (ScreenSpot Web-Icon 85.4 -> 80.6 for 2B) or on other platforms (anyres Android advanced tasks 80.5 -> 70.1), or is not tested on desktop/web (2506.03143#s3, 2404.05719#s1).
- **Search cannot recover a far-off first guess.** Zoom-and-reground fails when the first prediction is far off (locked onto a background-window tab); crops too small lose context and too large exceed capacity (2504.07981#s2).
- **Training-time trick applied at test time or untested on navigation.** Applying token selection at test time drops ScreenSpot to 64.9, text-rich screens have few redundant components, and navigation is not ablated (2411.17465#s1).
- **Grounding-only evidence for an agent claim.** Only click grounding is evaluated (agent use requires a separate planner), or the architecture gain on an agent task is small (Mind2Web 40.7 -> 41.4) compared with data gains (2506.03143#s1, 2312.08914#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From the `cua-agents-core` domain's `profile/expectations.json`; ids are prefixed `core-` to keep them apart from the `cua-agents` E ids._
- **core-E02 (dataset, common_practice).** Report ScreenSpot-Pro accuracy (text vs icon, per professional application group) for any claim about high-resolution or professional-software grounding — _applies when_ a claim that a method handles high-resolution screens, small targets or professional applications (zooming, high-res encoders, patch heads).
- **core-E12 (ablation, common_practice).** Separate data gains from architecture gains for native GUI policies: same-data baselines (e.g. Aguvis-style coordinate models trained on the same data) or data ablations alongside architecture ablations — _applies when_ a claim that a new architecture component (action head, high-res channel, token selection) of a GUI VLM improves grounding or agent performance.
- **core-E01 (baseline, common_practice).** Compare a new GUI grounding model against SeeClick, CogAgent and OS-Atlas-Base (plus UGround where available) on ScreenSpot / ScreenSpot-v2 click accuracy, split by text vs icon and by mobile/desktop/web — _applies when_ a claim that a screenshot-only grounding model or grounding pre-training recipe localizes GUI targets better.
- **core-E14 (other, common_practice).** Report how grounding handles repeated or identical elements (duplicate buttons, repeated icons, identical text) with failure examples — _applies when_ a grounding claim on dense web or app screens.
- **core-E21 (scale, common_practice).** Report inference cost and latency per step or per task (tokens, model calls, wall-clock) for multi-model or multi-call architectures — _applies when_ a claim for an architecture that adds model calls per step (multi-agent roles, verifiers, parsers, quarantined LLMs).

## Cognitive barriers
- "Coordinate SFT teaches perception." Training only an action head on a frozen backbone already recovers much grounding (ScreenSpot-Pro 1.6 -> 22.9), suggesting backbones perceive UI elements and coordinate SFT mostly learns the mapping (2506.03143#s4).

## Related anti-patterns
[AP7](../anti-patterns.md#ap7), [AP9](../anti-patterns.md#ap9), [AP16](../anti-patterns.md#ap16), [AP17](../anti-patterns.md#ap17), [AP20](../anti-patterns.md#ap20)
