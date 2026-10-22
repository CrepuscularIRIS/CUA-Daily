# SCAFFOLD: a web agent that turns its own successes into a skill library, then into weights

*A CUA Radar reading of arXiv 2609.05511v1 (He, Zhang, Ding, Liu). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2609.05511v1 · Code: https://github.com/BokwaiHo/SCAFFOLD*

## The problem: every task starts from scratch

A web agent that books a flight and then books a second flight usually behaves as if it had never seen a booking form. Recent work keeps some experience around: stored trajectories, natural-language workflows, or callable skills. The paper argues that even the strongest of these, skill induction, has three open problems. Skill libraries are essentially flat (SkillWeaver stores APIs in one pool, SkillRL uses two tiers), so skills cannot call other skills and abstraction depth is capped at one. Libraries only grow, and fill up with near-duplicates. And the knowledge lives in the prompt, so the underlying policy is as weak after many iterations as it was at the start.

## What SCAFFOLD is

The agent is a visual web agent. At each step it observes a screenshot, an accessibility-tree/DOM snippet and the current URL; it acts with primitives (click, type, scroll, wait) or by calling a skill, which is a macro action. Its base policy is Qwen2.5-VL-7B-Instruct. The architecture pattern on the CUA Radar board is C19, “accumulate reusable knowledge from the agent’s own runs”. A skill is a small program with typed parameters, a precondition, a body, a postcondition and an abstraction depth; semantic element references inside a skill (for example “the search input”) are grounded on the live page by a small VLM at run time.

Each self-improvement iteration has five stages:

1.  **Rollout.** Run the current policy with the current library on a task pool. A per-task verifier labels each trajectory as success or failure.
2.  **Multi-instance induction.** Cluster successful trajectories by instruction embedding. A frozen LLM (GPT-4o) proposes a skill only when at least two trajectories (n_min = 2) support the same parameter structure, and the skill must re-execute correctly on a held-out instance of the cluster or it is discarded.
3.  **Recursive composition.** A new skill may call any skill already in the library. Its depth is d = 1 + the maximum depth of the skills it calls. Cycles are forbidden and bodies are capped at 30 lines; depth itself is not capped.
4.  **MDL compaction.** Every M = 2 iterations the library is compressed against a minimum-description-length objective F(L) (library size plus the length of the shortest programs that reproduce the successful trajectories), using three greedy operators: merge behaviourally equivalent skills, refactor recurring sub-sequences into new mid-level skills, and prune unused ones. A change is accepted only if F falls and success on a held-out validation set does not drop.
5.  **Distillation.** The successful skill-augmented trajectories are re-parsed against the compacted library and used to fine-tune the policy (LoRA, rank 64) with a plan-augmented format plus an auxiliary loss that predicts the next skill name. The improved policy produces the next round of trajectories.

The supervision signal is therefore binary task success from a verifier, filtered twice (multi-instance support and held-out re-execution) before anything is added to the library.

## Results, as reported

All numbers below are success rate (%) of execution-checked, online evaluation, mean of 3 seeds, with Qwen2.5-VL-7B as the base model for every row. The three benchmarks are WebArena, VisualWebArena (VWA) and a held-out split of Online-Mind2Web (OM2W-X). For OM2W-X the authors partition sites into a 9-domain training pool and a 3-domain held-out test set (Jobs & Careers, Travel & Transportation, Government & Services).

| Method                             | WebArena | VWA      | OM2W-X   |
|------------------------------------|----------|----------|----------|
| SkillWeaver                        | 29.1     | 21.5     | 25.8     |
| SkillRL (strongest skill baseline) | 31.6     | 22.7     | 26.3     |
| **SCAFFOLD**                       | **42.7** | **36.3** | **43.5** |

The paper reports gains of 11.1, 13.6 and 17.2 points over SkillRL, all significant under a paired bootstrap. With UI-TARS-7B as the backbone the same method reaches 51.2, 44.6 and 49.1; the paper labels this an upper reference, because the backbone differs. There are no offline step-accuracy numbers in the paper; everything above is online.

## What the paper’s own controls say

**Ablations.** Removing one component at a time on WebArena gives: without distillation 34.7, without recursive composition 36.4, without multi-instance induction 38.1, without held-out validation 39.0, without MDL compaction 39.6, against 42.7 for the full system. Removing all four gives 29.1, which is the SkillWeaver row. The paper notes that the single-component drops add up to more than the total gap, and reads this as the components being synergistic rather than additive. A separate supervision-format study (same trajectories) finds that a STaR-style loop with no library reaches 30.4, and abstraction without distillation 34.7, so the authors conclude that neither piece alone explains the gain.

**Matched budgets.** The 30-step horizon is counted in primitive actions for every method, and a skill call draws on the same budget. Capping the budget at 10, 20 and 30 steps gives 19.8, 36.9 and 42.7 for SCAFFOLD against 13.2, 26.4 and 31.6 for SkillRL. Per successful WebArena task, SCAFFOLD issues 5.3 policy calls against 9.6 for SkillWeaver. All skill-induction baselines use the same GPT-4o inducer.

**Library dynamics.** Without compaction the library grows to about 470 skills by iteration 5; with compaction it saturates near 181 (about 2.6x fewer). Mean abstraction depth rises from 1.05 at iteration 1 to 2.71 at iteration 5, while the SkillRL-style two-tier hierarchy stays at depth 2 or below. Skill reuse reaches 64%.

**Robustness.** Under injected latency, shuffled non-functional DOM attributes, and a re-run seven days later, SCAFFOLD loses at most 2.1 points on WebArena, versus 3.6 to 4.4 for SkillWeaver and SkillRL on the first two perturbations.

**The judge.** Replacing the ground-truth verifier with a model-based judge (WebJudge protocol) for filtering gives 40.2 on WebArena and 41.0 on OM2W-X, against 42.7 and 43.5.

## Where the evidence is thinner, in the paper’s words

- The method needs a per-task verifier during rollout. The paper lists this as a limitation: it is realistic for WebArena and VisualWebArena, less so for autonomous deployment.
- The inducer is GPT-4o and accounts for roughly 70% of dollar cost. With the open-weight Qwen2.5-72B-Instruct as inducer WebArena drops to 40.8, still 9.2 above SkillRL.
- Gains shrink when held-out sites differ structurally from training sites; the paper’s example is GitHub, where transfer is modest.
- A full 5-iteration run on one benchmark takes about 36 hours on 8 A100-80GB GPUs. LoRA distillation shows at most a 1.2-point regression on tasks the original policy already solved.

## CUA Radar’s read

CUA Radar scores this paper **86 (★★★)**, evidence level **transfer**. The score reflects what the paper reports: execution-checked online evaluation, held-out Online-Mind2Web sites, 3 seeds, same-base-model and same-budget baselines, cost reporting, a component ablation, a check on a model-based judge, and released code. The judgment record also flags the dependence on a ground-truth verifier, which the paper addresses with the judge-swap experiment above. The radar did not rerun any experiment; every number here comes from the paper (version v1).
