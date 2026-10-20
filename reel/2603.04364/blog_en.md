# DMAST: training a web agent against an attacker that edits the page it sees

*A CUA Radar reading of arXiv 2603.04364v2 (Liu, Li, Rutishauser, Zheng). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2603.04364v2 · Code: https://github.com/huajianduzhuo-code/DMAST_official*

## The problem: one injected edit reaches both observation channels

Many web agents read a rendered screenshot and an accessibility tree (AXTree) at each step. Both come from the same DOM, so an adversary who injects content into the page changes both channels at once and can present one consistent, deceptive story. The threat studied is sensitive-data leakage: the attacker tries to get the agent to type private information (a password, a card number) into a field, without ever seeing that information.

Before proposing a defense, the authors run a vulnerability analysis on MiniWob++ with Gemma-3-27B-IT as both agent and attacker, 125 tasks and 8 episodes per task (1,000 episodes per setting). Without attack the agent succeeds on 36.9% of episodes. Under any injection, agent success falls to about 15.6 to 15.9%. Attacker success differs by modality: 24.1% when only the AXTree is attacked, 34.4% when only the screenshot is attacked, and 35.7% when both are. The authors read this as a gap in text-centric safety training.

## What DMAST is

**The agent.** A Gemma-3-12B-IT student sees a screenshot (896 x 896 input), the AXTree, the focused element, its action and thinking history, the task, and synthetic private user data. It writes a short reasoning trace and then one browser action addressed by element id (click, fill, scroll, drag_and_drop and a few more). The platform is the web (BrowserGym). The board pattern is C34.

**The attacker.** The attacker is the same model with the same weights, switched by a role-specific prompt. It sees the clean page, the task and the agent’s earlier actions, but not the agent’s weights or user data. Its action is a tuple (target, position, html, css): a CSS selector, an insertion position, an HTML payload and optional styling. This is compiled to JavaScript and run in the browser, so the re-rendered screenshot and the AXTree both change.

**The signal.** Rewards are programmatic. The agent gets 1 when the native MiniWob++ checker says the task is complete; the attacker gets 1 when a string match finds one of 14 synthetic sensitive fields in the agent’s generated action. If the task fails without leakage, both get 0, so refusing to act earns nothing. The paper states that no LLM judge or learned reward model is involved in the reward.

**The three stages**, all trained with LoRA (rank 128):

1.  **Imitation.** A Gemma-3-27B-IT teacher plays both roles, and the student is fine-tuned on successful agent steps and successful attacker steps.
2.  **Oracle-guided SFT.** For each step of a clean successful teacher trajectory, the teacher attacker injects an attack. An oracle model is shown the attacked observation, the goal and the correct action, and writes a short task-focused reasoning trace under a “zero-acknowledgment” rule: it must not mention the attack. The training sample is the attacked observation, this reasoning and the unchanged action.
3.  **Adversarial RL (GRPO self-play).** Agent and attacker are updated from the same shared policy on collected episodes, including clean ones. Episodes come from a 42-task training pool with at most 5 steps each. Training was scheduled for 25 iterations, stopped early, and the iteration-10 checkpoint was evaluated.

## Results, as reported

All numbers are percentages for the 12B agent, with standard errors printed in the paper. ASR is attacker success (lower is better) and TSR is task success (higher is better). Both are measured in interactive episodes; there is no offline metric. MiniWob++ uses 28 tasks excluded from every training stage. VisualWebArena (VWA) is 100 easy or medium tasks curated by the authors with synthetic sensitive data and an injecting attacker; training used only MiniWob++, so the authors treat it as out-of-distribution. The evaluation attacker is the fixed 27B model.

| Method | MiniWob++ ASR | MiniWob++ TSR | VWA ASR | VWA TSR |
|----|----|----|----|----|
| Base Model | 18.9 | 14.0 | 41.2 | 6.2 |
| Prompt Defense | 7.4 | 15.3 | 8.2 | 3.1 |
| SPAG | 14.4 | 22.7 | 35.1 | 6.2 |
| ART | 14.6 | 21.8 | 30.9 | 8.2 |
| Online SFT | 15.1 | 18.4 | 33.0 | 7.2 |
| **DMAST** | **10.8** | **25.7** | **21.4** | **10.2** |
| DMAST + Prompt Defense | 4.5 | 25.0 | 7.2 | 8.2 |
| Teacher as agent (27B, reference) | 13.6 | 39.2 | 21.4 | 7.1 |

Among standalone training-based methods, DMAST has the lowest ASR and highest TSR on both benchmarks. Pure Prompt Defense has a lower ASR than any training-based method, but on VWA its TSR drops to 3.1%, which the authors describe as “refusal collapse”. Combining DMAST with the prompt gives the lowest ASR on both benchmarks while keeping TSR high. Against the 27B teacher, DMAST matches its VWA ASR (21.4%) with higher VWA TSR (10.2% vs. 7.1%) and has lower MiniWob++ ASR (10.8% vs. 13.6%); the teacher’s MiniWob++ TSR (39.2%) is well above DMAST’s 25.7%.

## What the paper’s own controls say

**Stage-wise ablation.** The middle of Table 2 adds stages one at a time. Stage 1 gives MiniWob++ ASR 16.8 and TSR 19.5; adding Oracle SFT gives 15.3 and 23.3; adding RL gives 10.8 and 25.7. On VWA, Stage 1 and Stage 2 leave ASR at 36.4 and 36.7, and RL brings it to 21.4.

**Is Oracle SFT needed?** A variant that skips it and goes from imitation straight to RL reaches ASR 11.2 and TSR 23.8 at iteration 10, against 10.8 and 25.7 for the full pipeline (iteration 5: 13.4 / 22.5 vs. 11.0 / 24.0). This is on MiniWob++ only.

**Do the roles co-evolve?** Cross-evaluating checkpoints (Figure 3) shows, generally, that later agents do better against a fixed attacker and later attackers against a fixed agent. Attack diversity rises: strategy entropy goes from 3.21 to 3.27 and distinct strategy combinations from 465 to 523 across iterations 1 to 10. The authors note the entropy change is small.

**Stronger prompts.** Two further prompts (manual v2, teacher-searched v3) raise base-model VWA TSR but also VWA ASR, to 28.9 and 22.4; v3 lowers base MiniWob++ ASR to 3.1. For each of v1, v2 and v3 on both benchmarks, DMAST plus the prompt has equal or higher TSR and lower ASR than the base model plus the same prompt (for example VWA with v3: 8.2 / 13.3 against 7.1 / 22.4, as TSR / ASR).

**Beyond the training setting.** With the DMAST agent unchanged and the attacker re-prompted to plant a wrong value (11 typed-value tasks, 264 episodes per method), DMAST has ASR 38.3 and TSR 28.4, against the base model’s 44.7 and 13.6. On Qwen3-VL-8B-Instruct, the authors apply only the RL stage (no teacher was available) and report ASR 36.8 and TSR 16.5, against 41.1 and 14.3 for the base.

## Where the evidence is thinner, in the paper’s words

- The authors say the absolute VWA task success (10.2%) “remains modest”, which may partly reflect the 12B student’s capacity. The VWA set has 100 tasks, and its standard errors are 4.1 and 3.1 for the DMAST row.
- Only data leakage is trained and tested; goals such as control-flow hijacking are listed as not evaluated. The misinformation and Qwen3-VL results are described as “preliminary evidence”, and the Qwen3-VL run is a partial reproduction.
- The 27B model is both the Stage 1-2 teacher and the fixed evaluation attacker.

## CUA Radar’s read

CUA Radar scores this paper **72 (★★★)**, evidence level **transfer**. The score reflects online evaluation with programmatic checks, a held-out MiniWob++ split plus out-of-distribution VisualWebArena tasks, several training-based and prompt-based baselines, a stage-wise ablation, and released code. The judgment record marks variance across seeds, budget matching and cost as not reported (the tables do print standard errors) and records no flags. The radar did not rerun any experiment; every number here comes from the paper (version v2).
