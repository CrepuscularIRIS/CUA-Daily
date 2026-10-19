# Expose the Screen as Indexed Elements and Pruned Structure
_id: `structured_screen_observation` · sub-patterns: C01, C02, C03, C13, C27 · 4 candidate_pattern · 1 case · domains: cua-agents-core (0 K / 5 C) · outcome labels: none in this build_

**Definition.** Turn the screen into a discrete, indexed set of candidate elements — enumerated from a structural view (DOM, accessibility tree, Android view hierarchy, Windows UI Automation) or parsed from pixels by detectors, OCR and captioners — optionally ranked, pruned or restructured, and let the policy pick an id or a multiple-choice candidate instead of free coordinates. The family also covers diagnosing which channel (pixels or serialized structure) the agent actually believes when the two disagree. The gain is claimed from a better observation/target representation, not from a better policy.

**Operational signature.** enumerate elements from a structural API or parse pixels (detector + OCR + captions) → assign ids / draw marks with text descriptions → rank, prune or restructure the list → policy selects an id or multiple-choice candidate → execute on the element (or its centre); probe pixel-vs-structure conflicts

**When to apply.** When the platform exposes interactive elements with geometry (or a detector trained on UI-style interactable elements is available), the backbone can read numeric marks, and the screens are not dominated by canvas content or dense duplicate elements.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [C01](../sub/C01.md) | candidate_pattern | Element-id actions over interactive elements enumerated from DOM / a11y / view hierarchy / UIA | enumerate interactive elements from a structural view (DOM, accessibility tree, Android XML, Windows UI Automation), give each a unique id… |
| [C02](../sub/C02.md) | candidate_pattern | Parse raw pixels into an indexed, text-described element list (detectors, OCR, captions, region marks) | run pixel-level detectors (segmenter, interactable-region detector, OCR, icon detector) and optionally a captioner on the screenshot,… |
| [C03](../sub/C03.md) | candidate_pattern | Generate the next action in text, then ground it by multiple-choice over ranked DOM / a11y candidates | prune the page to top-k candidate elements (fine-tuned cross-encoder or a11y filtering), have the model state the intended action (from… |
| [C13](../sub/C13.md) | candidate_pattern | Prune and restructure the text observation (a11y tree / control list) before the policy sees it | drop low-relevance nodes or control types and restructure repetitive structure (merge StaticText into elements, tables/lists to Markdown;… |
| [C27](../sub/C27.md) | case | Diagnose whether agents believe pixels or serialized structure when the two disagree | pair GUI state probes in which one channel (DOM/a11y text) is edited or naturally stale while pixels define the gold value, measure… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Targets exposed by the structural view.** The evaluated apps/pages expose their interactive elements structurally (XML view hierarchy, DOM element types, UIA controls), and the paper reports the switch from a raw action API to element-indexed actions (AppAgent SR 2.2% -> 48.9%) (2312.13771#s1, 2402.07939#s2, 2401.13919#s1).
- **UI-trained parser, with a pixel/OCR fallback where structure is blind.** Pixel parsing uses a detector fine-tuned on DOM-derived interactable boxes rather than a generic detector (ScreenSpot 68.7 -> 73.0), or an OCR/text locator supplements the a11y marks for content the tree does not expose (PC-Agent: removing APM drops instruction SR 56% -> 20%) (2408.00203#s1, 2502.14282#s1).
- **High-recall ranking, then multiple choice.** When the page is pruned to top-k candidates, the ranker's recall at the cut-off is reported (Recall@50 ~85-89%) and selection is posed as multiple choice over small candidate groups rather than direct element generation (Flan-T5 B step SR 41.0 vs 17.5) (2306.06070#s1, 2306.06070#s2).
- **Observation modalities compared under one backbone.** Marked or parsed screenshots are compared against a11y-tree-only and screenshot-only inputs with the same backbone (WebVoyager 59.1% vs 40.1% with a11y tree only; OmniParser fusion 12.5% -> 19.5% for GPT-4V-1106) (2401.13919#s1, 2401.13649#s1, 2409.08264#s2).
- **Rule-based text-observation refinement with token savings.** The a11y tree is pruned and restructured by rules (merge StaticText into elements, tables/lists to Markdown) and both success and tokens per step are reported (WebArena SR 31.7% -> 37.1%) (2410.13825#s3).
- **Channel reliance probed under conflict.** The paper edits or uses naturally stale structure (DOM/a11y text, ghost nodes) while pixels define the gold value and measures how often the agent follows structure (PFG 0.30-0.75 despite 0.85-0.93 pixel accuracy) (2607.04334#s1, 2607.04334#s2).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Targets missing from the structure or the proposal pool.** Elements absent from the structural view (canvas content, UIA-unsupported controls) or outside the detector/ranker proposals are unaddressable (11-15% of targets outside top-50; GT masks raise mIoU 75.6 -> 90.1) (2402.07939#s2, 2502.14282#s1, 2306.06070#s1, 2310.11441#s1).
- **Duplicate or text-less elements.** Repeated identical icons/text or text-less elements make id choice or centre-click land on the wrong element (picks the first 'Schedule' button; text-and-type matching step SR 16.1 vs 39.1) (2408.00203#s1, 2401.01614#s1, 2401.01614#s3).
- **Marks drawn on dense text-heavy pages.** Marking DOM candidates on the screenshot mislinks labels on dense pages (SeeAct step SR 20.3 vs 39.1 for textual choices; 24.8% of WebVoyager failures are visual grounding errors) (2401.01614#s2, 2401.13919#s1).
- **Mark reading assumed for any backbone.** Gains are shown only for frontier models; SoM did not help IDEFICS-80B, CogVLM or Gemini-Pro, and adding UIA to OmniParser lowered GPT-4o (9.4% -> 8.6%) (2401.13649#s1, 2310.11441#s1, 2409.08264#s2).
- **Actions bound to structure inherit structure errors.** Element-id actions follow a swapped structural label 0.64 of the time vs 0.11 for coordinates, stale DOM snapshots and ghost a11y nodes are followed 0.38-0.88, and an early conflict is unrecoverable without reflection (2607.04334#s3, 2607.04334#s2, 2607.04334#s5).
- **Parsing cost and per-site pruning losses unreported.** Parser inference dominates run time (OmniParser runs 37.8-82.2 min vs 6.5-21.4 min), or pruning hurts some site categories (GitLab SR 35.0 -> 26.7) without per-category reporting (2409.08264#s2, 2410.13825#s3).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From the `cua-agents-core` domain's `profile/expectations.json`; ids are prefixed `core-` to keep them apart from the `cua-agents` E ids._
- **core-E10 (ablation, common_practice).** Compare observation modalities under the same backbone: accessibility tree / DOM only, screenshot only, screenshot + Set-of-Mark, screenshot + a11y tree — _applies when_ a claim that a particular perception input or screen representation improves an agent.
- **core-E11 (ablation, common_practice).** Test Set-of-Mark or mark-id prompting with backbones beyond GPT-4V-class models (open VLMs such as LLaVA, CogVLM, Qwen-VL), since mark reading is not general — _applies when_ a claim that an element-marking or mark-id grounding scheme helps GUI agents in general.
- **core-E13 (ablation, common_practice).** Compare coordinate actions with element-id / candidate-choice actions when claiming an action representation is better, since coordinates trail HTML candidate selection offline and the two differ in channel reliance — _applies when_ a claim about the action/output representation of a GUI policy (coordinates, element ids, indices, action heads).
- **core-E14 (other, common_practice).** Report how grounding handles repeated or identical elements (duplicate buttons, repeated icons, identical text) with failure examples — _applies when_ a grounding claim on dense web or app screens.
- **core-E22 (other, single_source).** When an agent sees both pixels and serialized structure, test conflicting or stale channels (structure-swap, stale DOM / ghost nodes) to show which channel drives belief — _applies when_ a claim about agents that consume screenshot plus DOM / a11y tree / view hierarchy.
- **core-E05 (metric, common_practice).** For offline web-agent claims on Mind2Web, report element accuracy, operation F1 and step success rate per Cross-Task / Cross-Website / Cross-Domain split, with MindAct and SeeAct as baselines — _applies when_ a next-action prediction claim evaluated on cached Mind2Web pages.

## Cognitive barriers
- "More structure is always safer than pixels." Binding actions to serialized structure inherits its staleness and attacker-controlled text (2607.04334#s3, 2409.11295#s1).

## Related anti-patterns
[AP7](../anti-patterns.md#ap7), [AP8](../anti-patterns.md#ap8), [AP9](../anti-patterns.md#ap9), [AP12](../anti-patterns.md#ap12), [AP14](../anti-patterns.md#ap14), [AP15](../anti-patterns.md#ap15), [AP17](../anti-patterns.md#ap17), [AP18](../anti-patterns.md#ap18)
