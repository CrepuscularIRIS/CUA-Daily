# DRIVE: a web agent that files its experience as reasoning rules and page programs

*A CUA Radar reading of arXiv 2605.23939v1 (Liu et al., National University of Defense Technology). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2605.23939v1 · the paper lists no code repository.*

## The problem

A web agent needs two kinds of knowledge at once. Reasoning knowledge — booking a flight requires first searching for routes — is abstract and transfers across websites. Interaction knowledge — clicking the Search button at a specific coordinate on one site — is bound to a particular page. The paper’s diagnosis is that existing methods store past experience in one uniform form: natural-language reflections carry intent but cannot execute on a concrete page, while retained trajectories and callable programs execute but stop transferring when the layout changes. A second gap follows from the first: when a task fails, nothing in the loop says whether the reasoning or the interaction was at fault, so the experience store cannot be repaired at the right level.

## What DRIVE is

The agent is a DOM-based desktop-web agent evaluated on WebArena (812 tasks over five self-hosted site domains: Shopping, CMS, Forum, Gitlab, Map). At each step it reads the page observation and the active URL, and acts in a predefined primitive action space. The backbone for all main experiments is GPT-4.1 at decoding temperature 0.1, capped at 20 environment steps per episode. On the CUA Radar board this is pattern C19 — accumulate reusable knowledge from the agent’s own runs — under the parent pattern “retrieve past experience and knowledge into context”. Nothing is fine-tuned; all learning lives in a library that is injected into the model’s context.

The mechanism has four pieces:

1.  **A dual-level skill library K = (K<sup>r</sup>, K<sup>i</sup>).** A reasoning skill is a natural-language triple ⟨M, B, V⟩: an observed mistake pattern, a corrected principle, and verification instructions; it is injected as guidance about *what* to do. An interaction skill is a parameterized program k<sup>i</sup>(C, X) → (α, e): given the page context and task arguments, it executes a closed-loop procedure (checking locators, handling dynamic UI) and returns an action trace and outcome — the *how*.
2.  **Scenario descriptors and singleton activation.** Each skill carries a descriptor ⟨U, W⟩: the applicable page context (URL patterns and page-level cues) and the task semantics. Online retrieval first filters by structure (does U match the current URL and page state?) and then ranks semantically against W. At most one reasoning skill and one interaction skill are activated per step; otherwise the agent falls back to primitive actions.
3.  **Induction from successes and counterfactual attribution of failures.** Successful episodes are abstracted into interaction skills, with task-specific entities lifted into arguments. Each failed episode gets a counterfactual question: could the task have been completed if the agent had preserved its high-level intent but followed a different interaction procedure? Yes → an interaction-level error, and a corrected interaction skill (with recovery logic) is synthesized. No → a reasoning-level error, and a ⟨M, B, V⟩ reasoning skill is written.
4.  **Continual maintenance.** Interaction skills are stored as operation templates with ordered selector lists (CSS, XPath, DOM identifiers, text locators, accessibility attributes); failed selectors are demoted or removed, working ones promoted, and a skill that keeps failing is deleted. Reasoning skills are merged and pruned by a smoothed utility score over usage counts and task outcomes.

The training signal is therefore the binary task outcome plus skill-level execution feedback (selector matches, URL/page-state changes, exceptions) — no learned reward model, no weight updates. The paper reports that as training trajectories grow from 42 to 251, task success and interaction-skill invocation success improve across most domains.

## Results, as reported

All numbers below are online success rates (%) under WebArena’s automated functional-correctness evaluator. Every method — DRIVE and the reproduced baselines — uses GPT-4.1, the same environment configuration, the same test tasks, and the same 20-step budget. The split is within-website: 30% of tasks per site for training, 70% for testing.

| Agent          | Shopping | CMS  | Forum | Gitlab | Map  | Average |
|----------------|----------|------|-------|--------|------|---------|
| WebArena agent | 21.4     | 15.4 | 8.1   | 14.1   | 12.7 | 14.3    |
| SteP           | 37.0     | 24.0 | 59.0  | 32.0   | 30.0 | 36.4    |
| Go-Browse      | 41.2     | 38.4 | 51.6  | 41.2   | 38.4 | 42.2    |
| SkillWeaver    | 25.1     | 23.8 | 41.3  | 32.0   | 26.2 | 29.7    |
| AgentOccam     | 37.2     | 41.5 | 60.4  | 41.4   | 46.8 | 45.5    |
| DRIVE          | 45.9     | 46.1 | 66.7  | 50.0   | 55.4 | 52.8    |

DRIVE averages 52.8% against 45.5% for AgentOccam: +7.3 percentage points, a 16.0% relative gain, and +10.6 / +23.1 points over Go-Browse and SkillWeaver. With the open-source Qwen2.5-7B-Instruct backbone the average rises from 8.2 to 12.5 (a 52% relative gain; per domain 8.4 → 12.3, 6.1 → 8.9, 9.9 → 16.9, 8.7 → 12.7, 7.8 → 11.7). The paper reports no offline step or grounding accuracy; everything above is online. The main table carries no variance; mean ± standard deviation appears only in the 100-task error study below. On efficiency (Shopping test set, N = 137): success 37.23 → 45.99 (+8.76 pp), input tokens per task 61,316 → 69,858 (+13.9%), but tokens per success 164.7k → 151.9k (−7.8%), with steps per task 9.3 → 9.1 and model calls 10.8 → 13.3; on a matched task subset, total input-token consumption falls 10.9% and total interaction steps 12.9%.

## What the paper’s own controls say

- **Component ablation** (WebArena average): the skill-free baseline is 45.5; adding interaction skills distilled from successes gives 49.8 (+4.3 pp); interaction skills from failures 48.5 (+3.0); reasoning skills from failures 47.8 (+2.3); the full DRIVE 52.8 (+7.3).
- **The attribution module is validated, not assumed.** On a 150-task subset (30 per domain) the baseline produces 81 failed trajectories, labeled by two human annotators. The LM attribution agrees on 69.1%: it catches 36 of 47 reasoning errors (76.6% recall) and 20 of 34 interaction errors (58.8% recall); 14 interaction errors are misread as reasoning (cascading UI failures) and 11 reasoning errors as interaction (premature termination).
- **Routing matters.** On the same subset: no-skill 46.0, human attribution 54.0 (+8.0), LM attribution 49.3 (+3.3), random attribution 46.7 (+0.7), reversed attribution 44.7 (−1.3). Deliberately routing failures to the wrong library drops performance below the no-skill baseline — the paper’s own evidence that the two levels must stay separated.
- **Each level cuts its own error type.** On 100 sampled tasks, three runs, mean ± std: no-skill 42.3 ± 3.06 correct / 35.7 ± 2.52 reasoning errors / 22.0 ± 3.57 interaction errors; reasoning-only 48.0 ± 1.81 / 30.3 ± 2.36 / 21.7 ± 2.08; interaction-only 47.7 ± 2.52 / 33.3 ± 0.58 / 19.0 ± 2.17; both levels 52.3 ± 2.52 / 30.0 ± 2.03 / 17.7 ± 1.53.

## Where the evidence is thinner, in the paper’s words

- The split is within-website, not held-out sites: “We then use a within-website stratified split, assigning 30% of tasks to training and 70% to testing.” Skills are induced and evaluated on the same five websites; cross-site transfer is not measured.
- “Our experiments use a DOM-based benchmark and do not fully capture the visual complexity of real websites.”
- “Retrieval may become less precise as the library grows, which calls for more scalable selection mechanisms.”
- No variance is reported for the main comparison table, and no code repository is given.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**. The judgment record credits what the paper reports: online functional-correctness evaluation, same-backbone and same-budget baselines, token-cost reporting, a component ablation, and an attribution module checked against human labels. It flags that the skill data overlaps the evaluation websites (anti-pattern AP5, unmitigated), that the main table reports no variance, and that no code is available. The radar did not rerun any experiment; every number here comes from the paper (version v1).
