# AliyunConsoleAgent: training a 32B cloud-console agent with distillation, then RL on live accounts

*A CUA Radar reading of arXiv 2606.09447v1 (Rong, Shen, et al.). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.09447v1 · Code: https://github.com/AlibabaResearch/aliyun-console-agent*

## The problem: documentation drifts from the console

Cloud consoles change quickly, while the documentation that describes them is written by hand. The paper’s setting is “Execution-as-Verification”: an agent follows each documented procedure end to end on the live console, and a failure points to a documentation defect. The authors estimate that keeping documentation current needs about 4 million recurring inspections a year, each taking roughly 1.6 hours of manual effort, so manual coverage stays below 1%. They already ran a production system on frontier proprietary models, but per-task API cost (about CNY 7 for Gemini 3 Pro Preview) and the privacy risk of sending console metadata to external services push them toward a private 32B model. The obstacle for RL, in their words, is that cloud tasks have strong resource dependencies: a missing prerequisite (say, a specific ECS instance) produces a failure that looks exactly like an agent mistake and pollutes the reward.

## What AliyunConsoleAgent is

**The agent.** It is a web agent for the Alibaba Cloud console. At each step the observation is a Set-of-Mark (SoM) annotated screenshot, extracted DOM text and the action history. The model writes an explicit Thought (ReAct style) and then picks one action: a GUI interaction executed through Playwright on headless Chromium (targeting elements by SoM id rather than pixel coordinates, because console pages carry hundreds of small elements), `task_complete`, `task_unachievable`, or an on-demand provisioning action that pauses the GUI and calls an LLM coding agent, ResourceCoder, to build missing resources with Terraform or the Aliyun CLI. A procedure is split into sub-steps by its ordered list, with an interaction budget of 40 per sub-step. On the CUA Radar board the pattern is K12, verifiable-execution reward.

**The rollout environment.** Four layers: an account pool (one isolated account per concurrent rollout), containerized sandboxes on Alibaba Cloud’s Kubernetes service, an offline layer of “Resource META” records (a description, key attributes, and create, verify and destroy code, produced for 4,000+ documents), and a runtime layer where ResourceCoder fills gaps that were not documented. After each task, cleanup restores the account to its initial state.

**The training.** Stage one is full-parameter SFT of Qwen3-VL-32B-Instruct on about 160K single-step samples for 1 epoch, drawn from distilled frontier-model trajectories (filtered at task and step level) and from autonomous self-exploration. Stage two is GRPO with group size 16, a per-token MSE-form KL penalty, and two-layer advantage normalization.

**The signal.** A dual-channel outcome reward. Channel 1 queries ActionTrail, Alibaba Cloud’s API audit log, with task-specific rules checked by domain experts; this gives a binary reward. Channel 2, for tasks without a decisive audit event, uses two LLM judges that must agree, otherwise the trajectory gets a label of -1 and is dropped. On 308 expert-labeled trajectories the two-judge ensemble reaches 96.7% agreement with humans, against 91.9% for a single model. Evaluation uses only the rule channel.

## Results, as reported

All numbers are online, end-to-end success on 278 documentation-verification tasks across 12 Alibaba Cloud products (76 standard, 202 hard), verified by ActionTrail rules with no LLM judge. Each task is run 3 times. pass@1 is the mean over runs (± std); pass@3 counts a task as solved if any run passes. All models use the same rollout environment. Cost is CNY per task.

| Model | Deployment | Cost | pass@1 | pass@3 |
|----|----|----|----|----|
| Qwen3-VL-32B-Instruct (base) | Private | 0.56 | 43.28 ± 0.50% | 60.79% |
| AliyunConsoleAgent-32B (SFT) | Private | 0.56 | 56.89 ± 0.83% | 72.66% |
| **AliyunConsoleAgent-32B (SFT+GRPO)** | Private | 0.56 | **63.52 ± 1.86%** | **75.18%** |
| Qwen3.6-Plus | API-only | 0.97 | 57.69 ± 1.50% | 72.66% |
| Kimi K2.6 | API-only | 2.70 | 60.79 ± 0.72% | 73.38% |
| Gemini 3 Pro Preview | API-only | 7.00 | 65.34 ± 2.15% | 79.86% |
| GPT-5.5 | API-only | 15.50 | 62.08 ± 2.00% | 76.09% |

The paper states that the SFT+GRPO model improves on the base by 20.24 pp in pass@1 and sits 1.82 pp below Gemini 3 Pro Preview, at 92% lower cost. The 0.56 CNY figure is for 4 L20 GPUs at 0.4 QPS. By difficulty (pass@3), the model gets 84.21% on standard and 71.78% on hard tasks, against 88.16% and 76.73% for Gemini 3 Pro Preview.

Offline, separate from the table above: on a 400-sample single-step benchmark (each model evaluated 3 times), AliyunConsoleAgent-32B after SFT reaches 92.75%, against 83.00% for the base and 95.25% for Gemini 3 Pro Preview.

## What the paper’s own controls say

**Training stages.** On pass@1, SFT lifts the base by 13.61 pp and GRPO adds 6.63 pp on top, with a paired-bootstrap 95% CI of \[2.97, 9.64\] for the GRPO-over-SFT gain. The paper’s training ablation (Table 5) has only these three rows; it does not include an RL-only run or a longer-SFT control.

**Versus the frontier.** The paired bootstrap for the Gemini-to-GRPO pass@1 gap gives a 95% CI of \[-1.27, 7.39\] (p \> 0.05), which the authors read as “approaching” Gemini 3 Pro Preview. In pass@3 the model scores 75.18% against 79.86% for Gemini 3 Pro Preview and 76.09% for GPT-5.5.

**Per-task behavior.** No task falls from 3/3 to 0/3 after GRPO, and 9 tasks move from consistent SFT failure to GRPO success (at least 2/3 passes). The authors describe two acquired behaviors: building a precondition (enabling auto-renewal first so that “disable” can be verified) and adapting the plan when the documented button does not exist.

**The environment.** For ECS, parallel execution with provisioning lifts success from 33.81% to 84.39% compared with parallel execution on empty accounts, and a 10-product cross-validation gives 80% average success.

**The judges.** The two-judge reward ensemble reaches 96.7% against expert labels on 308 trajectories.

## Where the evidence is thinner, in the paper’s words

- Held-out is at document level: “no document URL appearing in SFT or RL rollouts is included in the benchmark.” The training self-exploration starts from product entry points, and the paper does not describe product-level separation.
- The budget is a per-sub-step interaction budget of 40, “effectively a dynamic max-turn limit”; the paper does not give a per-method step comparison for the frontier models.
- Checkpoints were selected by validation every 5 steps, best at step 25, and training “exhibits non-monotonic oscillations”.
- The paper’s own error analysis names resource provisioning gaps as the largest failure category, mostly deterministic, “reflecting Rollout Environment coverage gaps rather than agent errors”. It lists static Terraform templates going stale, fragile DOM parsing for SoM, and infrastructure expense as limitations.
- The production audit (54,000+ procedures, 4,399 confirmed defects) used frontier models; the 32B model is in gray testing.

## CUA Radar’s read

CUA Radar scores this paper **69 (★★)**, evidence level **online**. The record credits live, rule-verified evaluation, 3 runs with standard deviations, strong baselines, reported cost, an ablation of the environment and training stages, a tested reward-model check, and released code. It marks held-out evaluation and budget matching as partial. The radar did not rerun any experiment; every number here comes from the paper (version v1).
