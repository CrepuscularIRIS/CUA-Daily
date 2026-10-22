# Q-Reflector: a trained 8B reflector that writes pre- and post-conditions before judging a mobile GUI step

*A CUA Radar reading of arXiv 2608.05587v2 (Guo, Liu, Gu, Wang, Chen). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2608.05587v2 · Code: https://github.com/pockyitachi/Q-Reflector*

## The problem: reflection that accepts too much or rejects too much

A mobile GUI agent has to decide, after each action, whether to continue, retry, recover or stop. That decision rests on a reflection step: did the action work, and is the result a valid move toward the task? A valid step need not finish the task. Opening a time picker is useful preparation for setting an alarm, whereas a swipe that leaves the Settings list unchanged has failed. Accepting an invalid transition lets the agent carry on after a failed or irrelevant action; rejecting a valid one triggers needless recovery.

The authors report that, used as standalone reflectors under one common prompt, both frontier VLMs and specialized GUI models are lopsided. On their 1,082 manually verified AndroidWorld transitions, GPT-5.2 reaches 95.10% accuracy on negative transitions but only 51.39% on positive ones, while GUI-Owl-1.5-8B shows the opposite pattern (92.33% positive, 57.78% negative).

## What Q-Reflector is

The agent setting is Android (mobile). The reflector is a separate module built on Qwen3-VL-8B, with the action-generating model left unchanged. After each executed action it receives the task goal, the action (type, arguments and an intent description), up to five recent actions, and a BEFORE and an AFTER screenshot. In a single call it outputs four JSON fields in order: a precondition, a postcondition, a three-part rationale (precondition check, postcondition check, task progress) and a binary Yes/No verdict. The precondition states what the action needs; the postcondition states its intended local effect. Both are meant to be written from the task, action, history and BEFORE screenshot, not fitted to the outcome. The paper notes that this is an instruction to the model rather than a runtime separation, since both images are supplied together. The verdict is Yes only if the intended effect occurred and the step is valid for the task. In CUA Radar’s taxonomy this is pattern C18, verifying each action’s outcome from before/after observations and feeding the verdict back.

Feedback is deliberately narrow. Only a No verdict produces a hint appended to the action model’s next observation: the previous action, the postcondition check, the task-progress judgment, and an instruction not to repeat the same coordinates or text. The generated conditions themselves stay inside the reflector.

Training has three stages on 880 manually reviewed transitions (512 positive, 368 negative) collected by running Agent-SAMA on Mobile-Eval-E and SPA-Bench. First, supervised fine-tuning (LoRA, rank 16) on the four-field response, with GPT-5.2 drafting the condition targets and humans reviewing them. Second, teacher-student distillation from GPT-5.2 responses. Third, GRPO with asymmetric verdict rewards (+2.5 for a correct Yes, +2.0 for a correct No, -2.0 and -2.5 for the two errors, plus a 0.1 format bonus), followed by DPO on 559 pairs of correct and incorrect sampled responses. The training signal is the audited verdict label; the paper states that the reward does not assess the quality of the conditions.

## Results, as reported

**Offline (AndroidWorld, 1,082 transitions: 613 positive, 469 negative).** Accuracy of the binary verdict, same prompt and inputs for every reflector.

| Reflector        | Overall   | Balanced  | Positive | Negative |
|------------------|-----------|-----------|----------|----------|
| GPT-5.2          | 70.33     | 73.24     | 51.39    | 95.10    |
| Claude Haiku 4.5 | 76.89     | 78.96     | 63.46    | 94.46    |
| GUI-Owl-1.5-8B   | 77.36     | 75.06     | 92.33    | 57.78    |
| **Q-Reflector**  | **82.16** | **81.45** | 86.79    | 76.12    |

Balanced accuracy is the unweighted mean of the positive and negative class accuracies; Claude Haiku 4.5 is the strongest baseline on it. GUI-Reflection-8B (its Action Verification pretraining checkpoint) scores 60.72 overall and is not shown.

**Online (MobileWorld, 117 tasks per action model).** Task success (%) with condition generation, as scored by MobileWorld’s evaluator, step cap of 50 action decisions. These are separate from the offline numbers above.

| Reflector         | GUI-Owl-1.5-8B-Instruct | MAI-UI-8B |
|-------------------|-------------------------|-----------|
| No reflection     | 29.06                   | 21.37     |
| Self-reflection   | 41.88                   | 27.35     |
| GPT-5.2           | 42.74                   | 29.06     |
| Claude Haiku 4.5  | 39.32                   | 29.91     |
| GUI-Reflection-8B | 39.32                   | 29.06     |
| **Q-Reflector**   | **46.15**               | **35.90** |

The paper states the gains over no external reflection as 17.09 and 14.53 percentage points (20 and 17 additional tasks), and over the strongest baseline reflector, GPT-5.2 and Claude Haiku 4.5, as 3.42 and 5.98 points. All reflectors share the same input information and feedback interface for a given action model.

## What the paper’s own controls say

**Condition generation.** A variant of Q-Reflector was trained separately from the same base model, 880 transitions, stages and hyperparameters, differing only in prompt and response structure (rationale and verdict, no conditions). Its MobileWorld success is 41.88% with GUI-Owl and 29.91% with MAI-UI, against 46.15% and 35.90% for the full model. The paper gives the differences as 4.27 points and seven additional tasks. For the other reflectors, whose checkpoints are fixed, prompting condition generation helped with GUI-Owl but gave mixed results with MAI-UI (self-reflection and Claude Haiku 4.5 completed four and two fewer tasks). In the paper’s words, the benefit depends on the combination of action model and reflector.

**Without conditions, Q-Reflector is not the top reflector for MAI-UI.** In the no-condition columns of Table 2, Claude Haiku 4.5 reaches 31.62% and self-reflection 30.77% with MAI-UI, against 29.91% for the Q-Reflector variant. With GUI-Owl the variant (41.88%) is ahead of GPT-5.2 (40.17%). The paper’s claim of highest success is scoped to the common condition-generation setting.

**Token cost.** With conditions, mean input tokens per task rise by 41.1% with GUI-Owl and 76.0% with MAI-UI relative to the ablation; output tokens fall by 5.6% with GUI-Owl and rise by 50.8% with MAI-UI. For GUI-Owl, input tokens per task are 236,132 with conditions against 143,649 with no reflection. The paper cautions that these counts do not measure latency or hardware cost.

**Training stages and order.** Distillation did not consistently preserve standalone accuracy: for Qwen3-VL-8B, overall accuracy goes from 73.11% (base) to 80.87% after SFT and 78.37% after distillation. GRPO then DPO gives 82.16%, against 80.41% for DPO then GRPO; the reversed order raises negative-class accuracy to 87.42% but rejects more valid transitions.

## Where the evidence is thinner, in the paper’s words

- Evaluation is 1,082 transitions and 117 tasks. Both online action models have 8B parameters; “transfer to other sizes remains untested”. Validation is on mobile; web and desktop “remains untested”.
- Each configuration retains one final score per task, and decoding is fixed (temperature 0 or greedy). The paper reports no seeds, standard deviations or confidence intervals.
- “Evaluation measures verdict accuracy and downstream task success, without independently scoring the semantic correctness of generated conditions.”
- The labels are GPT-5.2-assisted and author-audited; this human effort “limits scalability”. Limited history may obscure the purpose of preparatory or recovery steps.
- Screenshot resizing, decoding settings and output budgets were not varied.
- One qualitative MobileWorld example (Appendix D.5) shows seven repeated ineffective swipes without reflection and recovery at the next step with Q-Reflector; both runs end in success.

## CUA Radar’s read

CUA Radar scores this paper **81 (★★★)**, evidence level **transfer**, sub-pattern C18. The judgment record counts as reported: online evaluation on MobileWorld, test benchmarks separate from the training benchmarks, strong baselines, cost reporting, a condition-generation ablation, and a check of the learned judge on labelled transitions. The budget match is recorded as partial, and variance is recorded as not reported. No anti-pattern flag was raised. The radar did not rerun any experiment; every number here comes from the paper (version v2).
