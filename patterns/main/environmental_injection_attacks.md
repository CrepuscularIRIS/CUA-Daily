# Hijack Agents Through the Environment and Measure Attempt vs Completion
_id: `environmental_injection_attacks` · sub-patterns: C28, C29, C30, C31, C32, C33 · 4 candidate_pattern · 2 case · domains: cua-agents-core (0 K / 6 C) · outcome labels: none in this build_

**Definition.** Attack GUI/web agents by planting attacker content in a channel the agent reads — non-rendered HTML attributes consumed by the grounding stage, rendered fake UI elements (pop-ups, cookie banners), natural-language instructions in attacker-writable content of legitimate apps, or adversarially perturbed images — and evaluate security by separating hijack attempts from completion of the adversarial goal and by attributing success to agent components.

**Operational signature.** pick the channel the attacked stage reads (HTML attribute / rendered UI / writable content / image) → place the injection near the target or at the trigger page (optionally optimise or retarget it) → run the agent → score attempt (judge or intermediate measure) and completion (executable check of the adversarial goal) → attribute success to components

**When to apply.** When an agent reads untrusted environment content in the same context as its instructions and can take consequential actions.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [C28](../sub/C28.md) | candidate_pattern | Inject instructions into non-rendered HTML channels read by the grounding stage | insert zero-opacity elements or adversarial strings in non-rendered attributes (aria-label, id) next to the expected target, optionally… |
| [C29](../sub/C29.md) | candidate_pattern | Render fake UI elements (pop-ups, cookie banners) that direct the agent's click | draw attacker-controlled UI on screen (pop-up with attention hook, click instruction and OK banner; fake cookie popup in ad banners) so the… |
| [C30](../sub/C30.md) | candidate_pattern | Plant natural-language instructions in attacker-writable content of legitimate apps | place a hand-written instruction (sometimes faintly visible, or persisted in a URL fragment) in user-editable surfaces such as posts,… |
| [C31](../sub/C31.md) | case | Perturb a trigger image to steer captions or the VLM's reading of it | optimise an L-inf-bounded perturbation on an attacker-owned image, white-box against an open captioner or transfer via a CLIP ensemble… |
| [C32](../sub/C32.md) | case | Attribute attack success to components via an agent graph | model the compound agent as a graph and weight each edge by the bound on ASR if its value is followed, then compare component in/out… |
| [C33](../sub/C33.md) | candidate_pattern | Separate hijack attempts from attack completion in security evaluation | score attacks both by executable final-state checks of the adversarial goal and by an intermediate measure (LLM-judged attempt /… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Channel matched to the attacked stage.** The injection sits in a channel the attacked stage actually consumes: hidden HTML attributes for HTML-reading grounding (ASR up to 0.70), rendered pop-ups for screenshot-driven agents (62-100% step ASR) (2409.11295#s1, 2410.17401#s1, 2411.02391#s1).
- **Placement ablated.** The injection's position relative to the expected target is varied and reported (adjacent/after the target matters most; distant positions fall to 0.01-0.18) (2409.11295#s1, 2410.17401#s1).
- **Attempt and completion both reported.** Attacks are scored both by an intermediate measure (ASR-intermediate, attempt rate, step-level ASR) and by executable completion of the adversarial goal (ASR-intermediate up to 0.857 vs end-to-end <= 0.167; AR up to 92.45%) (2504.18575#s3, 2505.21936#s2, 2411.02391#s4).
- **Weak threat model across agents and vectors.** Low-effort injections in attacker-writable surfaces are tested across several frontier agents and vectors, with per-vector results (WASP ASR-intermediate 0.167-0.857; RedTeamCUA ASR 7.57-66.19%; notifications and emails most effective) (2504.18575#s1, 2505.21936#s1, 2506.14866#s1).
- **Component-level attribution.** The compound agent is modelled as a graph to localise where adversarial content is filtered or amplified (92% of attacked captions vs 31% end-to-end ASR) (2406.12814#s2, 2406.12814#s5).
- **Optimised attack with transfer and retargeting tested.** An optimised attacker (black-box-trained prompter, 97.5-99.8% ASR) is evaluated for transfer across backends (18%) and retargeting (98.5%) (2410.17401#s1, 2410.17401#s2, 2410.17401#s3).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Exposure overstated by episode start or task filtering.** Episodes start at the trigger page or are decoupled from the benign task, and tasks are filtered to ones the agent solves, which overstates real-world ASR relative to end-to-end runs (2406.12814#s1, 2505.21936#s1, 2505.21936#s2).
- **One pipeline, one backend, offline.** The attack is tested only on one pipeline offline (SeeAct), does not transfer across backends, or cannot reach screenshot-driven action generation (full-request ASR 0) (2410.17401#s1, 2410.17401#s2, 2409.11295#s1).
- **Attempt judged by an unvalidated, susceptible LLM judge.** The intermediate hijack measure comes from an LLM judge whose reliability is not quantified and which may itself be susceptible (2504.18575#s3, 2505.21936#s2).
- **Small, static, non-adaptive injection sets.** Injections are few, hand-written and non-adaptive; weak open models are not hijacked by faint text, so the set measures only a lower bound (2504.18575#s1, 2409.11295#s2).
- **Strong attack needs a white-box component.** The strong attack depends on a white-box captioner in the pipeline; black-box transfer drops sharply when the image is small in the screenshot (10% ASR) (2406.12814#s3, 2406.12814#s4).
- **Unstated success conditions.** Attacks fail when the agent ends from history, the answer is already on the page or more confident actionable elements exist; delayed attacks are weaker; retargeting is tested only on pre-filtered successes (2411.02391#s1, 2410.17401#s3).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From the `cua-agents-core` domain's `profile/expectations.json`; ids are prefixed `core-` to keep them apart from the `cua-agents` E ids._
- **core-E17 (metric, common_practice).** Report both hijack attempt and attack completion for prompt-injection attacks on agents (ASR-intermediate vs ASR-end-to-end, Attempt Rate vs ASR, step-level vs task-level ASR) — _applies when_ an attack or robustness claim for a web or computer-use agent under environmental injection.
- **core-E20 (other, common_practice).** Treat static, hand-written injections as a lower bound and test adaptive or optimized attacks (optimized strings, attacks on the defense itself such as branch steering) before claiming robustness — _applies when_ a robustness or defense claim against environmental prompt injection.
- **core-E16 (reproducibility, common_practice).** Validate the success checker or LLM judge against human labels (agreement, kappa or F1) when a benchmark uses fuzzy matching or an LLM judge — _applies when_ a new benchmark or evaluation protocol whose success or safety labels come from fuzzy matching, VQA models or an LLM judge.
- **core-E22 (other, single_source).** When an agent sees both pixels and serialized structure, test conflicting or stale channels (structure-swap, stale DOM / ghost nodes) to show which channel drives belief — _applies when_ a claim about agents that consume screenshot plus DOM / a11y tree / view hierarchy.

## Cognitive barriers
- "A screenshot-only agent is immune." Rendered pop-ups and visible text in writable content still hijack screenshot agents (2411.02391#s1, 2409.11295#s2).

## Related anti-patterns
[AP4](../anti-patterns.md#ap4), [AP19](../anti-patterns.md#ap19), [AP21](../anti-patterns.md#ap21)
