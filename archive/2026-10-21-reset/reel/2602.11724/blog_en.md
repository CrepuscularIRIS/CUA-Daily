# WebTestPilot: a web-testing agent that symbolizes GUI elements to assert its own oracles

*A CUA Radar reading of arXiv 2602.11724v3 (Teoh, Lin, Nguyen, Ren, Zhang, Dong; Proc. ACM Softw. Eng. 3, FSE, Article FSE087). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2602.11724v3 · Code: https://github.com/code-philia/WebTestPilot*

## The problem: is it a bug, or is the model hallucinating?

Specification-based E2E testing turns natural-language requirements (PRDs, user stories, meeting notes) into executable web tests. LLM agents promise to do this automatically, but the paper opens with an uncomfortable measurement: five mainstream LLMs (GPT, Gemini, Grok, Deepseek, Qwen) were each shown the same cart-page screenshot 10 times and asked “Does the shopping cart contain only one item?” — across trials the models produced seven distinct answers. An oracle that changes its mind per trial produces flaky verdicts, and when an agent flags an inconsistency you cannot tell hallucination from a real bug. Prior testers do not help: NaviQAte and LaVague only drive the flow and never verify intermediate states, and PinATA (the strongest prior baseline) keeps a precomputed, unstructured, capacity-limited natural-language memory that loses intermediate values, dependencies, and changes over time.

## What WebTestPilot is

The agent is a neurosymbolic web tester; no component of it is trained. At each state it perceives the full-page screenshot plus the DOM tree, and it acts with five primitives — click, type, press, scroll, wait — bound to element ids. Action grounding is two-stage: a GUI grounding model (UI-Venus-7B) predicts coarse coordinates, Set-of-Mark prompting annotates interactable elements with boxes and ids, and an LLM sees only a square crop around the predicted point before emitting the executable action. The platform is desktop web, evaluated on live applications. On the CUA Radar board its architecture pattern is C18: verify each action’s outcome from before/after observations and feed the verdict back.

The loop per step: (1) **Input parsing** splits the requirement into steps of (condition, action, expectation). (2) **Oracle inference** prompts the LLM with the explicit requirement plus the textual execution trace to infer implicit causal, data, and temporal dependencies, then defines symbols — strongly typed Pydantic schemas such as `Cart` or `Product`, instantiated on demand from current or past states — and writes pre/postcondition assertions in a Python-extended DSL over those symbols (existence, relational, temporal, causal, and data-integrity checks). (3) **Oracle execution** evaluates the precondition, runs the action, evaluates the postcondition; a failed assertion triggers regeneration and retry (n = 1 in this work; majority voting over n candidates is the alternative), and a persistent failure is reported as a bug. **Page reidentification** supports cross-state reasoning: a new state gets the page_id of the most DOM-similar prior state if an LLM judges the two screenshots the same page, so revisits (cart → product → cart) can be compared. The training signal is none — the assertion verdict itself is the only feedback, used for retry rather than learning.

## Results, as reported

All evaluation is online: four live open-source web apps (BookStack, Indico, InvoiceNinja, PrestaShop — each ≥5,000 stars, \>1,000 commits) packaged in reproducible Docker Compose environments, 100 natural-language requirements, 100 injected bugs modeled on a 10% sample of 2,043 closed GitHub bug issues (missing UI elements, data inconsistency, no-op actions, navigation failures). Base model GPT-4.1; a test stops when executed steps reach the scripted step count (budget-matched); fresh instance and restored database per test; sequential runs. No seeds or run counts are reported.

Task Completion (TC, all scripted assertions satisfied) and Correct Trace (CT, correct prefix), totals over 100 tests:

| Method           | TC       | CT       |
|------------------|----------|----------|
| LaVague          | 0.64     | 0.77     |
| NaviQAte         | 0.54     | 0.70     |
| PinATA           | 0.08     | 0.18     |
| **WebTestPilot** | **0.99** | **0.99** |

The paper reports beating the best baseline by 54.7% in TC and 28.6% in CT. Bug detection (RQ2, only PinATA can assert): WebTestPilot 0.96 precision / 0.96 recall vs PinATA 0.26 / 0.69 — absolute improvements of 0.70 precision and 0.27 recall (the paper’s “+70 / +27” in percentage terms). There are no offline benchmarks; everything above is online execution.

## What the paper’s own controls say

**Manual oracle check.** To rule out coincidental matches, the authors manually verified the semantic correctness of all assertions — the validator behind the precision number is human-audited.

**Real bugs.** Beyond injected bugs, 23 real bugs from GitHub issues were replicated: WebTestPilot detected 22, PinATA 15; the 7 PinATA misses came from missing cross-state context (1), requirement misinterpretation (2), and verifier hallucinations (4).

**Cost.** Median 29 s and 10k tokens per step — fastest of the four (LaVague 33 s, PinATA 38 s, NaviQAte 40 s); second-cheapest on tokens (NaviQAte 9k, PinATA 19k, LaVague 49k). Page reidentification dominates: 32% of tokens and 39% of execution time.

**Robustness and scale (RQ3/RQ4).** Under four input transformations (add-noise, dropout, restyle, summarize), GPT-4.1’s TC falls from 1.00 (default) to 0.93 (noise) and 0.70 each for dropout, restyle, summarize (total 0.81). Across Qwen2.5-VL scales, halving the model costs under 10% but below 7B performance drops 20–30% (Qwen2.5-VL-3b total TC 0.57; 0.48 under noise). Assertion analysis on GPT-4.1: 91% of assertions reference both prior and current states; 41.3% of symbols are physical concepts, 58.7% UI components. On local models, 52% of errors are wrong symbol declarations, 39% DSL misuse, 9% runtime errors.

**Industry deployment.** On China Mobile’s no-code platform, WebTestPilot converted a PRD into 56 test inputs (6.4 mins) and found 8 bugs in 32.7 mins (mean time to detect 4.9 mins); 5 of 8 were data-binding issues, which PinATA-style memory would only catch if explicitly specified.

## Where the evidence is thinner, in the paper’s words

- “Our metrics may underestimate tester performance, as multiple paths can achieve the same functionality.”
- “Our benchmark (webapp, test case, bugs) may not fully reflect real-world scenarios.”
- “We assume requirements are self-contained and complete, specifying all conditions, actions, and expected outcomes in order.”
- No component ablation is reported (no symbolization-off or retry-off run); no seeds/variance; the apps, requirements, and injected bugs come from the same four applications rather than held-out ones.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**, sub-pattern C18 (post-action reflection). The judgment record credits: live-app online evaluation, a strong SOTA baseline (PinATA), budget-matched termination, cost reporting, and manually verified assertions. It marks as not reported: held-out environments, variance/seeds, and component ablation; the code evidence item is unclear in the record, and an anti-pattern check (AP8) returns no. The radar did not rerun anything; every number here comes from the paper (version v3).
