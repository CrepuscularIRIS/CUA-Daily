# ToolCUA: teaching a computer-use agent when to switch between clicks and tool calls

*A CUA Radar reading of arXiv 2605.12481v2 (Hu, Zhang, Xu, Qiao, Yang, et al.; Tongyi Lab, Fudan University, Shanghai AI Laboratory). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2605.12481v2 · Code: https://github.com/X-PLUG/ToolCUA*

## The problem: a forked road

A computer-use agent can act through atomic GUI actions (clicks, typing, scrolling) or through high-level tool calls (API-based operations). The paper opens with a diagnostic finding: simply giving a model both action spaces often makes it worse, not better. On the matched feasible task set of OSWorld and OSWorld-MCP (Table 1), adding tools drops Qwen3VL-235B from 41.1% to 38.1%, EvoCUA-32B from 52.6% to 40.5%, Claude-4-Sonnet from 47.7% to 43.5%, and Claude-4.5-Sonnet from 61.9% to 48.4%, while Qwen3VL-8B barely moves (29.0% to 28.2%) because it makes only 0.01 tool calls even on successful tool-beneficial tasks. The paper calls this “optimal path confusion”: deciding whether to continue with GUI actions or switch to a tool is a trajectory-level decision that step-level imitation and final-task rewards do not teach.

## What ToolCUA is

The agent is an end-to-end policy built on Qwen3-VL-8B-Instruct. At each step it sees the current desktop screenshot plus the text results of earlier tool calls (the message construction keeps the most recent 5 screenshots as image history and earlier steps as a text-only action history). It acts through a hybrid action space: coordinate-based GUI actions via a `computer_use` function (key, type, click, scroll, wait, terminate) and MCP-style tool calls emitted as JSON `tool_call` blocks. The platform is a Linux desktop sandbox (OSWorld QEMU images with MCP tool designs from OSWorld-MCP and AutoGLM); transfer to unseen Windows apps is tested on WindowsAgentArena. On the CUA Radar board this is pattern C11, “mix GUI actions with code / shell / SDK calls in one action space”, under the parent pattern planner_grounder_interface.

Training is staged, and the supervision is synthesized:

1.  **Interleaved GUI-Tool trajectory scaling.** Starting from 10,000 successful pure-GUI trajectories (192,000 raw steps; OpenCUA 8,500, ScaleCUA 300, and 1,200 sandbox-collected), an MLLM first writes a trajectory-aware library of simulated tools — 4,350 unique tools at fine, mid and coarse granularity (2,000 / 1,900 / 450), with an average pool of 19.75 candidate tools per trajectory. A second MLLM pass generates a functionally equivalent tool-only trajectory, and a “next-state grounding” step anchors each simulated tool call to the real next-state screenshot from the original demonstration; 82.5% of synthesized tool steps pass this filter, and a human audit finds 93.0% of accepted steps state-aligned versus 28.0% of rejected ones. Randomly swapping some tool calls back to their GUI segments yields 10,000 interleaved trajectories (180k steps) and 5k critical GUI-Tool switching steps. No real tool execution is needed at this stage.
2.  **Tool-Bootstrapped GUI RFT.** Warmup SFT for 3 epochs (full-parameter, 8 × 8 GPUs) on the interleaved data, then single-turn GRPO on the 5k critical switching steps (group size 32, learning rate 1 × 10−6, batch size 128), which directly reinforces the GUI-or-tool decision at the boundary.
3.  **Online Agentic RL.** Multi-turn GRPO in the real GUI-MCP sandbox (rollout size 32, batch size 32, roughly 250 Docker instances, 8 × 8 training GPUs plus 4 × 8 inference GPUs) with a Tool-Efficient Path Reward: R = R_fmt + R_acc + λ·R_tool + β·R_length with λ = 0.4 and β = 0.2. R_tool rewards invoking tools on tasks labelled tool-beneficial (labels come from pass@32 rollouts with and without tools, verified by humans; agreement 91.7% on 60 tool-beneficial and 80.0% on 40 non-tool-beneficial sampled tasks) and abstaining elsewhere; R_length gives a bonus for trajectories shorter than the group average. Both terms act only on successful trajectories.

## Results, as reported

All numbers below are online, on the feasible tasks of OSWorld-MCP (333 tasks: 238 tool-beneficial, 95 non-tool-beneficial), reported as average@3 with a 50-step cap. The paper reports no offline step or grounding accuracy.

| Agent                       | Accuracy (%) | TIR (%) | ACS (steps) |
|-----------------------------|--------------|---------|-------------|
| UI-Tars-1.5-7B              | 12.31        | 4.5     | 37.11       |
| Qwen3-VL-8B-Instruct (base) | 28.23        | 8.41    | 19.34       |
| EvoCUA-32B                  | 40.54        | 22.52   | 26.16       |
| GUI-Owl-1.5-8B              | 43.84        | 36.04   | 21.19       |
| Claude-4-Sonnet             | 43.54        | 35.74   | 19.76       |
| Gemini-3.1-Pro              | 41.14        | 34.23   | 25.40       |
| GUI-Owl-1.5-32B             | 48.05        | 41.14   | 24.19       |
| Claude-4.5-Sonnet           | 48.35        | 40.24   | 19.07       |
| **ToolCUA-8B**              | **46.85**    | 24.32   | **14.93**   |

ToolCUA-8B sits above the previous same-scale state of the art GUI-Owl-1.5-8B (43.84%) and trails Claude-4.5-Sonnet by 1.50 points, with the lowest ACS of all evaluated models (14.93 versus 19.34 for the base). Against the base model the paper prints a Δ of +18.62 accuracy and describes it as “a relative improvement of approximately 66%”. On the tool-beneficial / non-tool-beneficial split it scores 45.80 / 49.47. It is the only model in Table 1 that gains from tools: 42.9% GUI-only to 46.8% with tools (+3.9 points), while its tool calls concentrate where they help — 2.11 calls on successful tool-beneficial trajectories, 0.12 on failed ones, and 0.74 per task pooled over all 333 tasks.

Transfer: on the held-out multi_apps domain (excluded from RL training) ToolCUA reaches 23.9% against 9.8% for the base and 18.5% for the pre-online-RL checkpoint; on unseen Windows apps it reaches 33.8% on the full GUI-only WindowsAgentArena, and on a matched 107-task subset 37.7% GUI-only rising to 40.5% with ported MCP tools (1.74 tool calls), while the base drops from 28.0% to 26.8%.

## What the paper’s own controls say

- **Pure-GUI control (Table 3).** Cold-starting the same base with a GUI-only dataset of comparable scale, then pure-GUI agentic RL, gives 29.03% → 34.93% (SFT) → 42.05% (RL); the hybrid path gives 38.13% after RFT and 46.85% after online RL. Hybrid training wins at both stages, and the final gap is not explained by GUI skill alone.
- **Ablation: data (Figure 6).** Skipping the interleaved data and running online RL directly from the baseline still improves accuracy, but TIR “only reaches around 15% by the end of training” and tool calls stay near zero — the reward alone does not overcome GUI-centric bias.
- **Ablation: reward (Figure 6).** Replacing the path reward with vanilla GRPO (accuracy + format only) makes training less stable, with “an eventual gap of about 7 percentage points after 20 training steps”, and TIR and trajectory length show no consistent trend.
- **Held-out tasks and platform.** As above: multi_apps was excluded from the 339-task online RL pool, and the Windows evaluation covers apps never seen in training.
- **Efficiency reference.** Pooling all models and keeping the shortest successful tool-invoking trajectory per task gives an empirical reference of 2.65 tool calls over 249 tasks; ToolCUA’s 2.11 is close to it, which the paper reads as selective rather than indiscriminate tool use.

## Where the evidence is thinner, in the paper’s words

- Diversity is coupled to the source data: “the diversity and quality of the synthesized hybrid trajectories are coupled with the breadth, fidelity, and task distribution of the source demonstrations.”
- Synthesis depends on strong proprietary MLLMs: “replacing stronger proprietary models with Qwen3.5-Plus led to noticeably lower generation efficiency and trajectory quality.”
- The synthesized tools are not executable implementations, so “real-world execution still depends on the maturity of available tools and the way tool feedback is organized”.
- Benchmark coverage: “our main performance evaluation is primarily conducted on OSWorld-MCP”.
- Variance: results are average@3 over sandbox stochasticity, but no standard deviations or confidence intervals are reported; the R_tool labels, though human-verified on a sample, still carry residual noise (the paper argues the soft weight λ = 0.4 keeps it from overriding task success).

## CUA Radar’s read

CUA Radar scores this paper **65 (★★)**, evidence level **transfer**. The record credits what the paper reports: online evaluation, held-out tasks and a held-out platform, strong baselines, step-cost reporting, component ablations, and released code. It marks as not reported: variance beyond average@3, matched training compute across compared models, and a validation of the next-state-grounding MLLM as a judge (the paper does report a human audit of the grounding filter itself). The sub-pattern is C11, hybrid GUI + tool actions in one action space. CUA Radar did not rerun any experiment; every number here comes from the paper (version v2).
