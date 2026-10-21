# EconSkills: distilling verified web-agent runs into reusable procedures for live economic data

*A CUA Radar reading of arXiv 2609.19523v2 (Yinzhu Quan, Zefang Liu; NeurIPS 2026 workshop IAEval). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2609.19523v2 · Skills library (dataset): https://huggingface.co/datasets/EconWebArena/EconSkills*

## The problem: solved procedures are thrown away

An agent that pulls one inflation print from a statistics office, then a second print a year later, starts from scratch both times. Standard web-agent evaluations treat each task in isolation, and prior experience-reuse work (ExpeL, Agent Workflow Memory, Voyager-style skill libraries) tends to evaluate the stored procedure and its delivery into the prompt together. EconSkills separates two questions that the paper argues are usually conflated: first, when a task has a known corresponding skill, does that skill transfer to a new instance; second, when the agent must select from an entire library, can it keep the benefit. The economic setting makes the second question unusually exacting: a portal can expose neighbouring series that differ only in unit, seasonal adjustment, geographic coverage, release vintage, or effective date.

## What EconSkills is

The agent runs on gpt-5-mini inside the BrowserGym and AgentLab ecosystem, on live desktop web. At each step it observes the page accessibility tree (AXTree), a screenshot, and contextual metadata (focused element, recent action history), and emits one or more actions from the EconWebArena high-level action set — element-based and coordinate-based interaction, keyboard input, scrolling, navigation, tab management — until it commits a final answer or hits the 30-step budget. On the CUA Radar board the architecture pattern is K27: retrieve stored past experience into the agent’s context.

The mechanism is a 50-skill library built in three stages:

1.  **Seed execution.** Each seed task is solved on the live portal; a trajectory is kept only if it passes the benchmark’s automatic check — the answer contains the gold value and the browser ends on the authoritative domain. This yields 50 verified seeds across nine of EconWebArena’s ten economic categories and 37 distinct authoritative websites.
2.  **Skill extraction.** gpt-5 distills each solved trajectory into one skill: a seven-part standard operating procedure (SOP) with name, purpose, preconditions, procedure, website guidance, verification, and recovery. Instance-specific values — a year, a country, an indicator — are replaced by named placeholders such as `<year>`, `<country>`, `<indicator>`, so the procedure refers to slots rather than one concrete question.
3.  **Skill application.** Skills are serialized to Markdown and prepended through the same extra-instructions channel; the model, browser, observations, and action budget are fixed, so conditions differ only in the added text.

The supervision signal is the native benchmark reward itself: nothing enters the library except a run that already succeeded on the live site, and nothing is trained — the policy is unchanged across all conditions.

## Results, as reported

Everything below is online success on live portals under the native EconWebArena reward. The two studies use different run protocols, so they are kept apart.

Controlled matched-skill transfer — 100 held-out task variants of the 50 skill families, 3 independent runs each (seeds 0, 1, 2):

| Condition                           | SR (%)     | Mean steps |
|-------------------------------------|------------|------------|
| BASE: task alone                    | 41.0 ± 2.0 | 19.83      |
| TRAJ1: + one matched raw trajectory | 7.0 ± 1.0  | 7.95       |
| MATCH1: + one matched skill         | 49.3 ± 3.1 | 15.67      |

Full-library deployment — all 360 tasks, one run per task, skill no longer given:

| Condition | Direct match (150) | No direct match (210) | Overall (360) |
|----|----|----|----|
| BASE: no skill | 44.0% | 16.7% | 28.1% |
| ALL50: full library | 18.0% | 6.7% | 11.4% |
| RETR5: five retrieved | 48.0% | 14.3% | 28.3% |
| RAND5: five random | 41.3% | 12.4% | 24.4% |
| HINT30: one optional hint | 46.0% | 11.4% | 25.8% |

The paper reports no offline step or grounding accuracy; there is only this live setting.

## What the paper’s own controls say

**Paired outcomes, not aggregates.** On the 300 matched cells, MATCH1 turns 46 BASE failures into successes against 21 in the opposite direction (McNemar’s exact test, p = 0.0031). Step counts are compared only on the 102 cells where both conditions succeed: MATCH1 uses 2.37 fewer actions on average (median two fewer), shorter in 59 cells, tied in 15, longer in 28 (sign test p = 0.0012). TRAJ1’s short 7.95-step mean is early termination, not efficiency — the paper says deleting the source answer while leaving instance-specific actions in place “does not produce a useful demonstration”.

**Where the gains and losses sit.** At the pair level the matched skill improves 27 of 100 pairs and hurts 12; 29 pairs are unchanged with at least one success and 32 never succeed. In deployment, every skill condition trails BASE on the 210 tasks without a family match; on those tasks the approximate top-1 hint lowers success from 16.7% to 11.4% (p = 0.043). Subset analysis of HINT30: source tasks 42.0% vs 48.0% (+6.0, p = 0.581); held-out variants 45.0% vs 45.0% (p = 1.000) — framed as optional and run once, the matched skill no longer moves the aggregate.

**Known confound, stated.** TRAJ1 and MATCH1 differ in abstraction, length, and format, so the paper itself says that comparison “does not isolate abstraction alone”. Four benchmark values that had changed at their source were handled through a fixed correction table constructed without reference to condition outcomes.

## Where the evidence is thinner, in the paper’s words

- “Each full-library deployment condition has one run per task, enabling paired comparisons but not across-run variance estimates.”
- “We study one benchmark, one agent backbone, and a fixed 30-step budget.”
- “50 skills do not establish scalability to organizational libraries with hundreds or thousands of procedures.”
- “Direct family match is defined against this library and is not an external coverage annotation.”
- Skill maintenance — revalidation, revision, retirement of stale procedures — is proposed but not evaluated. No code repository is listed; the skills themselves are released as a dataset.

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **online**. The score reflects what is reported: live online evaluation with the native reward, three seeds with standard deviations in the controlled study, fixed agent configuration and step budget across conditions, a condition ablation, and paired significance tests throughout. The judgment record also flags that the skill families come from the benchmark itself — mitigated, in its view, by the held-out variant design and by reporting source tasks separately as a diagnostic — that no external skill-memory methods are rerun as baselines, and that one backbone and one benchmark are used. Code is recorded as unclear. The radar did not rerun any experiment; every number here comes from the paper (version v2).
