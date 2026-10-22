# MobileForge: an annotation-free loop that explores an app, critiques its own attempts, and trains a mobile GUI agent with hints

*A CUA Radar reading of arXiv 2606.19930v2 (Liu, Zhao, Wu, Yin, Li, et al.; Zhejiang University, Kuaishou Technology, Tsinghua University). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.19930v2 · Code (announced): https://github.com/kwai/MobileForge*

## The problem: adapting to a target app without labels

Mobile apps are numerous, frequently updated, and expensive to cover with human-written tasks, demonstrations, or reward labels. The paper frames annotation-free adaptation as the goal: the agent explores a target app, attempts grounded tasks, evaluates its own behavior, and learns from self-collected experience. Its critique of existing work has two parts: prior pipelines lack a unified substrate connecting target-app exploration, curriculum mining, rollout execution, and feedback; and policy optimization treats rollouts as isolated experiences with sparse, trajectory-level rewards, so a failed rollout’s correct local steps are thrown away and a diagnosed mistake never reaches the next attempt.

## What MobileForge is

The agent is an MLLM-based mobile GUI agent running on Android. At each step it observes a screenshot, the interaction history, and — during adaptation — corrective hints from earlier attempts of the same task; it emits one structured action (click, long_press, swipe, type, answer, system_button, wait, terminate; the GUI-Owl action space adds open and key). Two 8B base agents are studied: the open generalist Qwen3-VL-8B-Instruct and the GUI-specialized GUI-Owl-1.5-8B-Instruct; the adapted models are called ForgeQwen3-8B and ForgeOwl-8B. On the CUA Radar board the paper sits in pattern K19 — dense step-level process rewards for multi-turn GUI RL, under the “learned outcome and process judges” family.

The system has two components. **MobileGym** is the substrate. Function-aware exploration (inspired by GUI-explorer) walks the target app: APK activity anchors and screenshots guide goal generation, depth-first traversal records reachable screens and transitions into an evidence pool Z. MobileGym-Curriculum converts Z into executable tasks, each carrying an instruction, an estimated step budget, core functionality, variation type, and prerequisites; the full pool holds 3,249 candidate tasks grounded in 527 source trajectories over 20 AndroidWorld apps, and training uses 200-, 400-, and 900-task subsets. MobileGym-Critic watches each completed attempt as a visual action trace and returns hierarchical feedback: a trajectory outcome label z, per-step process labels (a reasonable-step tag plus rationale), and a corrective hint h. **HiFPO** is the training recipe. Each task runs K serialized attempts, where attempt k conditions only on hints from attempts 1..k−1. Tasks solved every time are dropped; for the rest, HiFPO picks the most reasonable successful attempt (else the most reasonable one) and keeps only its reasonable steps. Each kept step becomes a prompt with the hint context appended; the policy samples a group of G = 5 candidate actions, scored by a rule-based reward (0.2 for action-type match, 0.8 for argument match), and normalized into a group-relative advantage — step-level GRPO, with KL regularization to the reference policy. No human-written task, demonstration, or reward label enters the loop; the supervisory signal is entirely the critic’s outcome and step labels plus hints, with Gemini-2.5-Pro as the default final-decision model and Qwen3-VL-8B writing step descriptions.

## Results, as reported

Everything below is online evaluation. AndroidWorld (116 tasks) is in-domain: the adaptation data is mined there. MobileWorld GUI-only (117 tasks) is out-of-domain: no MobileWorld rollout, task, or feedback is used. Pass@k is over the 116 AndroidWorld tasks; MobileWorld reports single-attempt success. The paper does not report seed counts or variance. The 900-task 8B runs took roughly 80 hours on 8×80GB GPUs.

| 8B model                  | AW Pass@1 | AW Pass@3 | MW GUI-only SR |
|---------------------------|-----------|-----------|----------------|
| Qwen3-VL-8B (base)        | 40.5%     | 55.2%     | 7.7%           |
| ForgeQwen3-8B (900 tasks) | 50.9%     | 67.2%     | 10.3%          |
| GUI-Owl-1.5-8B (base)     | 56.0%     | 69.0%     | 37.6%          |
| ForgeOwl-8B (900 tasks)   | 67.2%     | 77.6%     | 41.0%          |

Annotation-free adaptation brings the generalist close to the closed-data GUI-specialized base (67.2% vs 69.0% Pass@3) and improves the specialist further (77.6% Pass@3; hard-task Pass@1 rises from 19.3% to 29.8%). On MobileWorld, ForgeOwl-8B’s 41.0% leads the evaluated open-data agents (OpenMobile-8B 17.7%, ClawGUI-2B 17.1%, OpenMobile-7B 14.8%) and approaches larger or closed-data systems (GUI-Owl-1.5-32B 43.9%, MAI-UI-235B-A22B 39.7%). ForgeQwen3-8B transfers much more modestly at 10.3% — the paper itself notes that out-of-domain generalization “still depends strongly on the base agent’s mobile GUI competence.” There are no offline step-accuracy or grounding numbers; both benchmarks are online.

## What the paper’s own controls say

**Hints.** With 200 tasks and the Qwen base, adding corrective hints to repeated rollouts lifts overall rollout success from 52.0% to 77.0% and Pass@3 from 49.0% to 72.5%, while average steps per attempt fall from 18.4 to 17.2 — improvement from accumulated feedback, not extra sampling. Under matched HiFPO training, hint removal degrades both agents (Qwen base AW Pass@1 55 → 49; GUI-Owl base 75 → 71) and both MobileWorld counts drop.

**Objective.** On the same generated data, no-hint SFT at 200 tasks lands below the base model (34.5% vs 40.5% Pass@1); hint SFT reaches 45.7%, hint-contextualized GRPO 47.4%; at 900 tasks GRPO is again strongest at 50.9%.

**Filtering.** Keeping all-fail plus mixed tasks (success-rate range \[0.0, 0.9)) gives the best combined AndroidWorld (48.3%) and MobileWorld (15/117) result among tested filters — remove mastered tasks, not failures.

**The critic.** Against reference labels on 400 trajectories, the Gemini configuration reaches 89.75% trajectory and 86.53% step accuracy (F1 91.40% and 89.35%); an all-Qwen critic reaches 77.00% and 71.37% and still improves the policy (AW 52/67/70 Pass@1/2/3, MW 11/117), so the gains do not require a proprietary evaluator.

**Grounding.** On the Broccoli app, a landing-screen-only generator puts 27.3% of tasks on recipe deletion; the trajectory-grounded curriculum spreads coverage into shopping lists, cooking assistant, meal planning, and settings, which the baseline never touches.

## Where the evidence is thinner, in the paper’s words

- Seeds and variance are not reported; single runs per configuration.
- External MobileWorld numbers “follow the GUI-only reporting protocol” rather than being rerun under matched budgets; budget-matching against those baselines is not shown.
- The adaptation data is mined from AndroidWorld, the in-domain benchmark, so in-domain gains include exposure to the evaluated apps; MobileWorld transfer is the paper’s answer to this.
- “Training remains limited to AndroidWorld-side apps, leaving broader coverage, long multi-app workflows, persistent user state, and unusual task rules challenging.”
- Code, data, and models are announced (“will be released”) rather than available at review time.

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **transfer**, sub-pattern K19 under learned outcome and process judges. The recorded evidence notes online evaluation, a genuinely held-out environment (MobileWorld), component ablations, and a critic validated against reference labels; it marks variance and budget-matching as unclear, external baselines as partial, code as announced, and flags anti-pattern AP5 — synthesis/exploration data overlapping the evaluation environment. The radar did not rerun anything; every number above comes from the paper (version v2).
