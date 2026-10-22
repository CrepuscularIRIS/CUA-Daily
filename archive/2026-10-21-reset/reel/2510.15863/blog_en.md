# PolySkill: giving web-agent skills an abstract interface and per-site implementations

*A CUA Radar reading of arXiv 2510.15863v2 (Yu, Li, Shi, Qi). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2510.15863v2 · Code: https://github.com/simonucl/PolySkill*

## The problem: skills that only work on the site they came from

Skill-induction methods such as Agent Skill Induction (ASI) and SkillWeaver store routines learned on one site as code and reuse them on later tasks, but the paper argues they are over-specialised to that site. It reports that on unseen websites Skill Reusability stays below 9% for ASI and below 3% for SkillWeaver, and that SkillWeaver with Claude-3.7-Sonnet degrades over time because its self-proposed tasks become increasingly complex and specific. The paper asks how to induce skills that transfer across sites in one domain, and how to measure transfer beyond task success.

## What PolySkill is

The agent is a web agent built on an LLM backbone (GPT-4.1, Claude-3.7-Sonnet, Qwen3-Coder-480B-A35B or GLM-4.5). At each step it receives an observation (the accessibility tree and a viewport screenshot) and acts through BrowserGym primitives (click, type, hover, scroll, key presses, tab operations, goto) or by calling a skill from its library, which extends the action space. All experiments run on web environments only. On the CUA Radar board the paper sits in pattern C19, “accumulate reusable knowledge from the agent’s own runs”, under experience and memory retrieval.

The mechanism borrows polymorphism from object-oriented programming. Instead of inducing a flat script per site, the agent organises skills by website category. For a shopping domain it first induces an abstract class (the paper’s example is `AbstractShoppingSite`) that declares method signatures such as `search_product`, `add_to_cart` and `checkout`, plus compositional skills such as `purchase_item` that call only other abstract methods. For each concrete site (`AmazonWebsite`, a Walmart class, and so on) the agent then fills in a subclass with the site-specific implementation. The induction prompt is reframed accordingly: register the signature in the abstract class first, then implement it in the site class. When the agent reaches a new site in a known category, the abstract class acts as a blueprint of what to figure out.

The pipeline is built on ASI’s verification: after a successful trajectory (judged by an LLM judge) the agent induces skills, re-attempts the same task by calling the new skill, and keeps the skill only if that second run succeeds. There is no weight training; the paper says the efficiency-aware objective (task success minus a length penalty) guides prompting rather than being optimised as a loss. A second setting is task-free: the agent proposes its own goals, explores sites and induces skills from its successes.

## Results, as reported

**WebArena (online, execution-checked, 812 tasks).** Average success rate (%) from Table 8; the paper reports no standard deviations for this table. Models and baselines are the same across the row group; SkillWeaver is described as evaluated only on WebArena subsets, yet the table lists it for all categories.

| Backbone              | Baseline | SkillWeaver | ASI  | PolySkill |
|-----------------------|----------|-------------|------|-----------|
| GPT-4.1               | 38.5     | 43.6        | 46.5 | **49.3**  |
| Claude-3.7-Sonnet     | 45.6     | 47.5        | 55.8 | **59.5**  |
| Qwen3-Coder-480B-A35B | 34.4     | 38.1        | 43.9 | **45.2**  |
| GLM-4.5               | 36.2     | 33.6        | 38.9 | **39.8**  |

The paper’s own difference row against ASI is +2.8, +3.7, +1.3 and +0.9 for the four backbones. Per site, PolySkill is below ASI in some columns (for example Shopping on Claude-3.7-Sonnet, 58.3 versus 59.1, and Map on GPT-4.1, 18.9 versus 21.5), and the Cross column (48 instances) has the largest difference for three of the four backbones.

**Mind2Web (judge-scored, held-out splits).** Mind2Web only ships human trajectories, so the authors score agent runs with a GPT-4.1 judge following the Online-Mind2Web protocol, which that prior work reports at 85% agreement with humans. Skills are induced on 1009 training tasks and evaluated on cross-task (252), cross-website (177) and cross-domain (912) test sets. The paper does not state whether these runs are on live sites. GPT-4.1 results, mean ± std (Table 6):

| Method              | Cross-task     | Cross-website  | Cross-domain   |
|---------------------|----------------|----------------|----------------|
| No skills           | 53.8           | 56.2           | 62.3           |
| ASI (static)        | 52.3 ± 1.2     | 54.9 ± 0.8     | 57.3 ± 1.5     |
| PolySkill (static)  | 55.4 ± 1.3     | 57.6 ± 1.1     | 60.1 ± 0.6     |
| ASI (+Update)       | 59.4 ± 2.1     | 58.7 ± 1.8     | 62.1 ± 1.9     |
| PolySkill (+Update) | **63.2 ± 2.4** | **61.3 ± 2.2** | **63.4 ± 2.7** |

“+Update” means the skill library keeps growing online while testing. The headline +9.4 on Mind2Web in the abstract corresponds to PolySkill (+Update) on cross-task. With Claude-3.7-Sonnet the numbers are close together: the no-skill baseline is 59.1, 64.4 and 66.2, and PolySkill (+Update) reaches 64.6, 66.2 and 68.3. On the open-source models (Table 7) static PolySkill is below the no-skill baseline on cross-domain for both (Qwen3-Coder 35.9 against 37.5; GLM-4.5 42.9 against 43.7), and only the +Update variant is above it (39.9 and 46.0).

## What the paper’s own controls say

**Static versus online update.** Static PolySkill with GPT-4.1 is above ASI on all three Mind2Web splits, but below the no-skill baseline on cross-domain (60.1 against 62.3). Gains over the baseline mostly appear in the +Update setting, where both ASI and PolySkill adapt online. Variants restricted to same-domain or same-sub-domain skills are also reported, but they are not an ablation of the polymorphic structure.

**Library size.** With GPT-4.1 on cross-task, static PolySkill holds 43 skills against 50 for ASI, and with +Update 47 against 66, which the paper reads as refining existing polymorphic definitions instead of accumulating redundant skills.

**Reuse and steps.** On WebArena shopping, step counts fall from about 6.1 to between 3.3 and 4.4 as Skill Reusability rises from 0% to over 20%, for all three methods; PolySkill reaches 20.4% by task 180.

**Cost.** Average tokens per task on Mind2Web cross-task (GPT-4.1): action generation 55,367.4 for the no-skill baseline, 53,840.5 for ASI and 49,710.3 for PolySkill; verification adds 4,963.2 and skill induction 8,476.4 for PolySkill, for a total of 63,149.9 against 64,287.5 for ASI.

**Continual learning.** Starting from a library learned on WebArena shopping and then adapting to Amazon and Target (3 runs), PolySkill’s performance on the original WebArena tasks stays stable while ASI’s degrades; the paper reports a final +4.9% advantage over ASI there.

**Task-free exploration (GPT-4.1, Table 3).** On WebArena shopping, a self-guided agent exploring Amazon, Target and WebArena reaches 43.1 against 37.4 for no skills, 39.8 for SkillWeaver 42.1 for the sequential curriculum WA, Target, Amazon, and 42.3 for the WebArena-only specialist. On GitHub/GitLab (Table 9) it reaches 66.2 on GitLab and 84.0 on GitHub, against 38.9 and 66.7 with no skills.

## Where the evidence is thinner

- The paper calls WebArena shopping and GitLab “held-out” in the self-guided experiments, yet the table lists those sites among the ones the self-guided agent explores (AMZ + Target + WA; GitHub + GitLab). These rows are therefore not clean held-out transfer, and the self-guided row is close to the curriculum and specialist rows (43.1 against 42.1 and 42.3 on WebArena shopping).
- The WebArena table has no standard deviations, and its caption states that experiments marked with a dash are pending completion. The paper does not describe how WebArena tasks were split between skill induction and evaluation, beyond saying ASI is induced online.
- Mind2Web scoring relies on a GPT-4.1 judge whose 85% agreement is cited from earlier work, not measured here. The paper does not say whether the budgets or number of attempts are matched across methods.
- Some summary figures in the abstract and conclusion (13.9% on unseen websites, 73% of skills transferring) could not be matched to a specific table row in the text; the introduction gives 31% reuse on unseen websites. The deltas printed in Table 6 for two static cross-domain rows also do not agree with the printed absolute values, so this summary uses absolute values only.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **transfer**. The judgment record credits online evaluation, held-out splits (Mind2Web cross-website and cross-domain), strong baselines (ASI, SkillWeaver), cost reporting, a static versus +Update comparison, a tested judge (the 85% agreement cited from prior work) and released code. It marks variance as not reported and budget matching as unclear; the paper does give ± values on Mind2Web but none on WebArena. It also flags AP5, data overlapping the evaluation, which matches the overlap between exploration sites and evaluated sites in the task-free experiments. The radar did not rerun any experiment; every number here comes from the paper (version v2).
