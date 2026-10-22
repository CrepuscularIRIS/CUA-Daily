# UI-MOPD: one 8B GUI agent, two platform teachers, distillation routed by platform

*A CUA Radar reading of arXiv 2607.04425v2 (Lian, Chen, Yu, Duan, Liu, Liu, Fu, Luan, Qu, Xia, Wang; Tsinghua SIGS, Xiaomi, HIT Shenzhen, Zhejiang University, Peng Cheng Laboratory). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2607.04425v2 · Code: https://github.com/EliSpectre/UI-MOPD*

## The problem: platforms share skills but clash in conventions

A GUI agent that works on a laptop and a phone has to keep two interaction vocabularies alive at once. The paper’s framing: desktop and mobile “share transferable capabilities but differ in action semantics and interaction conventions” — returning may mean closing a window on a computer but pressing the back button on mobile. Its preliminary analysis finds that mixed supervised fine-tuning and static model merging “tend to average away or overwrite platform-specific behaviors”. Desktop-only SFT on the 8B base raises OSWorld from 33.9% to 35.8% but collapses MobileWorld from 7.7% to 0%; TIES-merging the two platform models scores 0% on MobileWorld.

## What UI-MOPD is

**The agent.** A screenshot-driven GUI agent covering desktop and mobile. It sees screenshots (during training only the current one; at inference four history screenshots, the current screenshot, and the full text action history) and outputs actions as JSON inside a tool-call format, with coordinates. Desktop actions go through a `computer_use` interface (key, type, mouse clicks, scroll, wait, terminate); mobile actions go through `mobile_use` (click, long_press, swipe, type, answer, system_button, wait, ask_user, terminate). On the CUA Radar board its architecture pattern is R01, in the rule-reward single-step RL family.

**The data.** Uni-GUI, built with a unified cross-platform collection harness: nearly 10K high-quality executable trajectories, about 160K steps and 11.5K trajectories before final filtering, mixing self-collected steps (desktop with Kimi-K2.6, mobile with Gemini-3.1-Pro, which also cleans both sources) with cleaned OpenCUA and OpenMobile steps. Trajectories longer than 40 steps are dropped, and a Gemini-3.1-Pro judge checks sub-task completion before a trajectory is kept.

**The mechanism.** Two stages. Stage 1 supervised-fine-tunes two Qwen3-VL-32B-Thinking specialists on the desktop and mobile partitions of Uni-GUI. Stage 2 trains a single student, initialized from Qwen3-VL-8B-Thinking, with a GRPO-based DAPO objective on its own rollouts — and this is the new part: multi-teacher on-policy distillation (MOPD), claimed as the first use in GUI agent training. Each rollout is routed by its platform label to the matching teacher, which acts as a “platform-conditioned behavioral anchor” through a token-level reverse-KL penalty (the K3 estimator, coefficient 0.01). An adaptive group-level mask removes the KL penalty for rollout groups whose mean task reward is already sufficient. Teachers exist only during training; deployment is the single 8B student.

**The training signal.** A structured rule reward per action: 1.0 when every required dimension matches (action type, coordinate in the target bounding box, scroll direction, key set, case-insensitive text), −0.5 for partially valid actions, −1.0 for unparsable ones. Training runs one epoch per stage, 8 rollouts per prompt, on 64 H100 GPUs.

## Results, as reported

Online task success rate; all integration rows train the same 8B student scale.

| Method (8B student unless noted)        | OSWorld   | MobileWorld | H-Mean    |
|-----------------------------------------|-----------|-------------|-----------|
| Qwen3-VL-8B-Thinking (base)             | 33.9%     | 7.7%        | 12.5%     |
| Mixed-SFT (8B)                          | 35.0%     | 6.4%        | 10.8%     |
| Mixed-RL (8B)                           | 35.9%     | 9.4%        | 14.9%     |
| Unified-Teacher OPD (32B mixed teacher) | 35.9%     | 8.7%        | 14.0%     |
| Mobile-Only OPD (32B teacher)           | 34.9%     | 10.3%       | 15.9%     |
| MOPD (8B teachers)                      | 36.2%     | 9.4%        | 14.9%     |
| **UI-MOPD**                             | **38.2%** | **12.0%**   | **18.3%** |

The paper states relative improvements of 12.7% and 55.8% over the base model, and a gain of 4.3 points on both platforms (MinGain 4.3, the largest in its ablation table). The H-Mean of 18.3% matches Qwen3-VL-235B-A22B-Thinking (38.1% / 12.0% / 18.3%). For context it lists SeedVL-1.5 at 34.1% on OSWorld, GUI-Owl-7B at 34.9% / 4.5%, and GELab-Zero-4B at 31.9% / 10.9%. Under “Controlled Training References” it also reports the two 32B teachers (46.3% desktop; 16.2% mobile) and a 32B Mixed-SFT run at 44.4% / 16.2%, explicitly labeled a capacity reference, not a parameter-matched baseline.

Offline, static capability is evaluated only as a control: AndroidControl⋆ accuracy goes from 78.73% (base) to 80.05%, OSWorld-G from 52.13% to 52.84%, while ScreenSpot-Pro (43.71% to 43.14%) and ScreenSpotV2 (91.27% to 90.88%) stay within 0.6 points of the base; TIES merging degrades AndroidControl⋆ to 74.01%. No seeds, run counts or variance are reported for any number above.

## What the paper’s own controls say

- **Teacher specialization, not scale.** With the 8B student and Stage-2 data fixed, swapping the 32B specialists for 8B teachers gives 36.2% / 9.4%, and a unified 32B teacher trained on mixed data gives 35.9% / 8.7% — “the advantage of UI-MOPD cannot be explained by ordinary OPD or teacher scale alone.”
- **Routing matters.** Randomly selecting between the two teachers (MinGain 1.7, versus 4.3 full) “removes the platform–expert correspondence and substantially reduces the balanced gain.”
- **The adaptive mask matters.** Applying KL to all rollout groups gives 37.1% / 10.3%; once a group already receives sufficient reward, continued imitation “can unnecessarily restrict policy improvement.”
- **Where supervision helps.** Disagreement analysis at student-visited states shows a diagonal pattern — each specialist supplies more useful corrections on its native platform, concentrated in low-reward rollout groups (Figure 4; we cite no percentages because they appear only as figure labels).
- **Integration baselines.** Sequential RL is order-dependent (36.6% / 9.4% mobile-first versus 33.7% / 11.1% desktop-first); weight averaging reaches 36.5% / 6.8%; TIES merging 36.8% / 0%. “All parameter-matched integration baselines underperform UI-MOPD on at least one platform.”

## Where the evidence is thinner, in the paper’s words

- No seeds, run counts or variance are reported; none of the tables carries error bars.
- Evaluation environments are also collection environments: Appendix B states that functional points are extracted “from the original initialized OSWorld environments” and “from the original initialized MobileWorld and AndroidWorld environments”. The paper does not report a held-out app or site split.
- The trajectory judge and the mobile collector are the same model (Gemini-3.1-Pro); the record finds no separate validation of that judge.
- Code is linked, but the judgment record marks code availability as unclear; CUA Radar has not run it.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **transfer**, sub-pattern R01. The judgment record credits online evaluation on OSWorld and MobileWorld, parameter-matched 8B integration baselines, and a component ablation that holds the student and Stage-2 data fixed; it marks budget matching and cost reporting as partial (hardware is given, 64 H100 across 8 nodes). Evidence items marked unclear: held-out environments, variance, and code. No anti-patterns are flagged (AP7: no). The radar did not rerun any experiment; every number here comes from the paper (version v2).
