# Decouple Planning from Grounding and Redesign the Action Interface
_id: `planner_grounder_interface` · sub-patterns: K22, K23, K29, C04, C10, C11, C12, C14, C37 · 7 candidate_pattern · 2 case · domains: cua-agents + cua-agents-core (3 K / 6 C) · outcome labels: none in this build_

**Definition.** Treat the interface between reasoning and pixels as the design object: split each step into a language planner and a specialised visual grounder, train that grounder on data synthesised from rendered UI structure, or change the action abstraction itself (tagged elements, programmatic tools alongside GUI primitives). From `cua-agents-core` it also holds the generalist-planner / specialist-grounder split (C10), coordinate grounding pre-trained on harvested element-box pairs (C04), hybrid GUI + code/SDK actions (C11), one declared action schema for multi-source SFT (C12), action-space simplification for prompted agents (C14) and, as a cross-domain case, DCT+BPE tokenisation of continuous action chunks (C37).

**Operational signature.** planner emits action + NL target description → grounder (trained on rendered-structure data) maps it to coordinates on the raw screenshot; or the action space is redefined (element tags, tool library) → execute

**When to apply.** When the planner is strong at reasoning but weak at pixel grounding, and rendered UI structure (DOM, element trees, accessibility trees) is available for data synthesis or tagging.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [K22](../sub/K22.md) | candidate_pattern | Split each step into a language planner and a specialised visual grounder | a general (M)LLM planner emits the next action and a natural-language description of its target; a separate pure-vision grounding model… |
| [K23](../sub/K23.md) | candidate_pattern | Synthesise grounding data from rendered UI structure | render web pages, UI-component code or parsed screens, read exact element boxes/attributes from the DOM/element tree, synthesise referring… |
| [K29](../sub/K29.md) | candidate_pattern | Redesign the action interface between model and computer | change the action abstraction the agent emits — restrict actions to tagged accessibility/OCR elements with one bounded primitive per step,… |
| [C04](../sub/C04.md) | candidate_pattern | Continual-pretrain a VLM to emit target coordinates as text from automatically harvested element-box pairs | harvest (screenshot, referring text, box/point) triplets from DOM, accessibility trees or a UI detector without human labels, format them… |
| [C10](../sub/C10.md) | candidate_pattern | Split a generalist planner that describes the target from a specialist grounder that localises it | have a (prompted) MLLM plan and emit a natural-language target description or semantic argument, then dispatch localisation to a separate… |
| [C11](../sub/C11.md) | candidate_pattern | Mix GUI actions with code / shell / SDK calls in one action space | let the policy (or an orchestrator choosing between a GUI operator and a programmer) invoke scripts, terminal commands or tool/SDK… |
| [C12](../sub/C12.md) | candidate_pattern | Normalise heterogeneous trajectories into one declared action schema for end-to-end screenshot policy SFT | rewrite actions from many datasets/platforms (or raw input-event logs) into a small shared schema (click(x,y), type, scroll plus… |
| [C14](../sub/C14.md) | case | Simplify the prompted agent's action space toward what the LLM handles well | remove rarely useful or embodiment-heavy actions (noop, tabs, hover, press, goto, scroll), collapse dropdown selection into a click, add… |
| [C37](../sub/C37.md) | case | Compress continuous action chunks with DCT + BPE into autoregressive tokens | quantile-normalise action chunks, DCT per dimension, quantise, flatten low-frequency-first and BPE-compress into VLM tokens; optionally a… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Grounder value shown with a fixed strong planner.** Holding a strong planner fixed and adding the grounder is reported (o3 23.0 -> 51.0, GPT-4o 5.0 -> 27.0 on OSWorld with Jedi); replacing GPT-4o's own coordinates with a grounding model's triples OSWorld SR (5.03 -> 14.63 with OS-Atlas-7B) (2505.13227#s2, 2410.23218#s3).
- **Screenshot-only grounder at dynamic high resolution.** The grounder operates on raw screenshots only, trained at dynamic high resolution (2410.05243#s2, 2412.04454#s3).
- **Grounding data from rendered structure, mixed and multi-level.** Exact element boxes are read from rendered DOM/element trees; mixed data types and multiple levels (icon/component/layout) scale without saturation, and web-only data transfers to desktop/mobile; harvested element-box pairs are curated (dropping static text, balanced per-source sampling: 71.2 -> 74.9) rather than only scaled (2505.13227#s1, 2410.05243#s1, 2401.10935#s1, 2411.17465#s4).
- **Unified cross-platform action space.** A unified pyautogui action space is used, packing multiple pairs per screenshot; normalising heterogeneous datasets into one shared schema (17 -> 10 action types) helps zero-shot OOD transfer (2412.04454#s1, 2410.23218#s2, 2508.09123#s1).
- **Interface matched to available structure.** An element-tag interface is used only where a parseable accessibility tree plus OCR exists; an application-specific tool library fits in context (881 tools, 32K) (2410.08164#s3, 2510.17790#s1).
- **Hybrid GUI + code action space compared with each alone.** GUI actions are mixed with code/shell/SDK calls and compared against GUI-only and code-only agents on the same benchmark (OSWorld-Verified 60.76% vs 50.68% / 35.73%, with fewer steps per passed task), or the action space is pruned toward what the LLM handles well with each step ablated (WebArena SR 16.5% -> 25.9% -> 31.7%) (2508.03923#s1, 2509.02544#s1, 2410.13825#s1, 2410.13825#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Planner errors propagate through the NL interface.** Planning errors (wrong/vague element descriptions) dominate failures and propagate through the natural-language interface; an end-to-end single model is weaker than with a strong external planner; residual failures are dominated by planning in spreadsheet and multi-app tasks (2410.05243#s2, 2505.13227#s2, 2412.04454#s3, 2410.23218#s3, 2504.00906#s3).
- **Ambiguity and refusal unhandled.** Models rarely refuse; ambiguous instructions cause ~40% of errors (2505.13227#s1, 2412.04454#s1).
- **Claims on saturated grounding benchmarks only.** ScreenSpot v1/v2 saturate and there is an offline-online gap (2501.12326#s3).
- **Data returns diminish on long-tail icons.** Diminishing returns after ~100K screenshots; long-tail and idiosyncratic icons cause grounding errors on mobile/desktop (2410.05243#s1, 2410.05243#s2).
- **Interface granularity too coarse.** Element-ID grounding cannot target sub-element positions (grounding errors in 53% of failures); pruned or compressed action spaces drop actions other sites need (hover/press/tabs untested) or lose fine-grained actions (letter-level drag-select) (2410.08164#s3, 2410.13825#s1, 2508.09123#s1).
- **Tool interface unused by small models.** Tool gains are modest at 7B (+1.9); small models rarely call tools and make harmful tool calls before RL; hybrid code actions need a strong reasoning orchestrator (o4-mini drops to 43.43%) and code-only cannot handle apps without scripting access (2510.17790#s1, 2508.03923#s1, 2402.07456#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From `profile/expectations.json`; ids are stable across the domain._
- **E05 (dataset, common_practice).** Report GUI grounding on ScreenSpot-Pro (high-resolution professional desktop) and ScreenSpot-v2, not only ScreenSpot v1, which saturates (7B and 72B indistinguishable) — _applies when_ a claim that a model or data recipe improves screenshot-to-coordinate GUI grounding.
- **E06 (baseline, common_practice).** Compare a new grounder against UGround(-V1-7B), Aguvis-7B/72B, OS-Atlas-7B and UI-TARS(-1.5) at matched backbone size — _applies when_ a claim that a grounding model or grounding-data recipe beats prior GUI grounders.
- **E07 (baseline, common_practice).** Compare a native end-to-end GUI policy against UI-TARS(-1.5)-7B (or the same backbone's SFT-only model) and against an agentic framework (GPT-4o/o3 planner + specialised grounder such as UGround, Aria-UI, Jedi, GTA1) — _applies when_ a claim that a trained end-to-end GUI agent model improves online task success.
- **E08 (ablation, common_practice).** For planner-grounder systems, hold the planner fixed and swap grounders (e.g. GPT-4o + UGround vs + Aguvis vs + Jedi), and report the planner alone — _applies when_ a claim that a grounding component (or the planner-grounder split itself) improves agent task success.
- **E24 (other, common_practice).** Test grounding robustness under controlled perturbations (zoom, text size, window position/clutter, relational instructions) with matched pairs — _applies when_ a claim that a grounder or agent is robust or generalises across visual layouts.
- **E25 (metric, common_practice).** Report refusal / infeasible-task behaviour (instructions with no valid target) — _applies when_ a grounding or agent benchmark claim where some instructions are ambiguous or infeasible.
- **E21 (other, common_practice).** Report screenshot-only and accessibility-tree/DOM-augmented settings separately; a11y-tree availability changes results and reverses across models — _applies when_ a comparison of GUI agents whose observation spaces may differ.
- **core-E01 (baseline, common_practice).** Compare a new GUI grounding model against SeeClick, CogAgent and OS-Atlas-Base (plus UGround where available) on ScreenSpot / ScreenSpot-v2 click accuracy, split by text vs icon and by mobile/desktop/web — _applies when_ a claim that a screenshot-only grounding model or grounding pre-training recipe localizes GUI targets better.
- **core-E12 (ablation, common_practice).** Separate data gains from architecture gains for native GUI policies: same-data baselines (e.g. Aguvis-style coordinate models trained on the same data) or data ablations alongside architecture ablations — _applies when_ a claim that a new architecture component (action head, high-res channel, token selection) of a GUI VLM improves grounding or agent performance.
- **core-E13 (ablation, common_practice).** Compare coordinate actions with element-id / candidate-choice actions when claiming an action representation is better, since coordinates trail HTML candidate selection offline and the two differ in channel reliance — _applies when_ a claim about the action/output representation of a GUI policy (coordinates, element ids, indices, action heads).

## Cognitive barriers
- "Grounding is the bottleneck." With a strong grounder, planning errors dominate failures (2410.05243#s2, 2505.13227#s2).

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP7](../anti-patterns.md#ap7), [AP9](../anti-patterns.md#ap9), [AP10](../anti-patterns.md#ap10), [AP12](../anti-patterns.md#ap12), [AP14](../anti-patterns.md#ap14), [AP15](../anti-patterns.md#ap15), [AP16](../anti-patterns.md#ap16), [AP17](../anti-patterns.md#ap17), [AP18](../anti-patterns.md#ap18)
