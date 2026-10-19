# Defend Agents Against Untrusted Observations: Prompting, Gating and Isolation
_id: `injection_defense_isolation` · sub-patterns: C34, C35, C36 · 2 candidate_pattern · 1 case · domains: cua-agents-core (0 K / 3 C) · outcome labels: none in this build_

**Definition.** Reduce environmental prompt injection by in-context defenses inside the same model (defensive system prompts, delimiters, instruction-hierarchy privilege, paraphrasing, injection detectors, self-caption consistency checks), by pausing sensitive actions for user confirmation, or by architectural isolation — information-flow labels on data, quarantined LLMs that answer typed queries over untrusted content, policy checks on tool/GUI calls, and branching plans compiled before any observation.

**Operational signature.** identify untrusted inputs → (in-context) mark, paraphrase or detect them / (gating) mark sensitive actions PENDING for user confirmation / (isolation) label data, hide it behind variables, query it via a quarantined LLM with typed outputs, check calls against flow policies or fix a branching plan before observing → measure ASR and benign utility under attack

**When to apply.** When agents take consequential actions while reading untrusted content, and some utility or extra cost can be traded for control-flow integrity.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [C34](../sub/C34.md) | candidate_pattern | Defend against injections inside the same model's context (prompts, delimiters, role hierarchy, paraphrase, detectors) | add defensive system prompts or delimiters, place web content at lowest instruction-hierarchy privilege, paraphrase untrusted text, run… |
| [C35](../sub/C35.md) | case | Pause sensitive actions for user confirmation, judged by the policy itself | have the policy label actions it deems sensitive or irreversible as PENDING and wait for user confirmation |
| [C36](../sub/C36.md) | candidate_pattern | Separate trusted planning from untrusted observations with information-flow labels and quarantined LLMs | label data by confidentiality/integrity, hide untrusted results behind variables, query them only through a quarantined LLM with… |

## Success conditions
_Derived from the member cards' When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Untrusted data isolated and calls policy-checked.** Untrusted results are hidden behind variables, queried only through a quarantined LLM with constrained typed outputs, and tool/GUI calls are checked against information-flow policies (AgentDojo policy-relevant injections 163 -> 9 / 0) (2505.23643#s1, 2505.23643#s3).
- **Benign utility reported under the defense.** Utility on benign tasks is reported next to attack success (single-shot branching plans: 58.3% pass@3 on 60 OSWorld tasks; selective hiding plus quarantined queries recovers utility, best with reasoning models) (2601.09923#s1, 2505.23643#s2).
- **Defense attacked directly.** The defense itself is attacked adaptively (fake cookie popups or optimised banner pixels steering a fixed plan; CLIP attacks on consistency checks) and the result reported (2601.09923#s3, 2406.12814#s6).
- **Compared against standard in-context defenses.** A new defense is compared with defensive system prompts, instruction hierarchy and injection detectors, which roughly halve ASR for some models (2504.18575#s4, 2505.21936#s3).
- **Specific checks with access to raw inputs.** In-context defenses use specific per-step prompts or let the defender see raw inputs (self-captioning consistency check nearly removes captioner-attack ASR when the defender LM sees raw images) (2411.02391#s3, 2406.12814#s6).
- **Confirmation gating measured on benign and attacked runs.** Confirmation behaviour on sensitive requests is reported (85.7% vs 50-57% for GPT baselines) and gating is also tested under injection (Operator ASR 30.89% -> 7.57% with confirmation checks) (2402.07939#s4, 2505.21936#s3).

## Failure modes
_Derived from the member cards' When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Generic defensive prompts.** Generic defensive prompts give no gain (pop-ups, EIA, captioner attack) and malware scanners flag nothing (2411.02391#s3, 2409.11295#s3, 2406.12814#s6).
- **Instruction hierarchy or detectors trusted as sufficient.** Instruction hierarchy did not prevent hijacking (>50% of cases still influenced) and detectors catch 0-30% of high-risk injections (2504.18575#s4, 2505.21936#s3).
- **Utility and token cost of isolation.** Coarse tainting cuts task completion by up to 40%, data-dependent tasks remain largely unsolved, and isolation costs 2-3x tokens or much more for iterative variants (2505.23643#s1, 2505.23643#s2, 2505.23643#s3, 2601.09923#s2).
- **Fixed plans that cannot adapt.** Underspecified tasks with unknown start states explode branches, plans cannot adapt to observed failures, boolean leakage accumulates and termination is only via caps (2601.09923#s1, 2601.09923#s2).
- **Self-judged gating without adversarial content.** The same policy decides which actions need confirmation (per-app rates as low as 50%), no adversarial content is tested, or an attentive human is assumed (2402.07939#s4, 2505.21936#s3).
- **Channels outside the policy.** Text-to-text injections that affect final responses fall outside tool-call policies (2505.23643#s1).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_From the `cua-agents-core` domain's `profile/expectations.json`; ids are prefixed `core-` to keep them apart from the `cua-agents` E ids._
- **core-E18 (baseline, common_practice).** Compare a new injection defense against a defensive system prompt, delimiters / instruction hierarchy and prompt-injection detectors (PromptGuard / PromptArmor), and paraphrasing — _applies when_ a claim that a defense reduces prompt-injection attack success on GUI/web agents.
- **core-E19 (other, common_practice).** Report utility under the defense (benign task completion, AgentDojo/OSWorld utility) and its cost in extra queries or tokens alongside attack success — _applies when_ a claim that a defense or isolation architecture secures an agent.
- **core-E20 (other, common_practice).** Treat static, hand-written injections as a lower bound and test adaptive or optimized attacks (optimized strings, attacks on the defense itself such as branch steering) before claiming robustness — _applies when_ a robustness or defense claim against environmental prompt injection.
- **core-E21 (scale, common_practice).** Report inference cost and latency per step or per task (tokens, model calls, wall-clock) for multi-model or multi-call architectures — _applies when_ a claim for an architecture that adds model calls per step (multi-agent roles, verifiers, parsers, quarantined LLMs).

## Cognitive barriers
- "Adding a checker component always reduces risk." Components that consume attacked inputs (a reflexion evaluator) raise ASR above the base agent (36% vs 31%) (2406.12814#s5).

## Related anti-patterns
[AP20](../anti-patterns.md#ap20)
