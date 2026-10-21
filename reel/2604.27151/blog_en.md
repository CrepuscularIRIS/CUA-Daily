# StepWise: run a small computer-use agent, escalate to the big model only when it stalls or drifts

*A CUA Radar reading of arXiv 2604.27151v1 (Wei, Ni, Zhao, Gan, Cohan — Yale NLP Lab and UNC Chapel Hill). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2604.27151v1 · Code: https://github.com/yale-nlp/StepWise*

## The problem: frontier-model inference at every step

The strongest computer-use agents call a large multimodal model at nearly every interaction step. The paper opens from the deployment side: realistic multi-step workloads run 20–35 steps, consume hundreds of thousands of tokens, take tens of minutes, and can cost over one US dollar per task with a frontier model throughout. Its counter-thesis: this uniform allocation of compute is fundamentally inefficient, because GUI trajectories are heterogeneous — most steps are routine, failures concentrate at a few high-risk moments.

It groups failures into two modes. Progress stalls are loops: repeated or equivalent actions with no state change. Silent semantic drift is sneakier: the agent keeps acting plausibly after already deviating from the user’s intent, so the rest of the trajectory is locally coherent but doomed. Measurements on small policies (Figure 2) back the split: failed episodes average 2.8× more steps than successful ones for EvoCUA-8B and 2.5× for Qwen3-VL-8B, failed runs repeat actions far more, and a non-trivial fraction of failures still end with a model-issued done.

## What StepWise is

The agent is conventional: it observes a screenshot plus optional accessibility-tree/DOM signals and emits a short textual rationale with an executable action (click, type, scroll, hotkey) — desktop tasks on OSWorld’s Ubuntu VMs, web tasks on WebArena-Verified. The board pattern is C18, “verify each action’s outcome from before/after observations and feed the verdict back” (under agent-loop context control).

StepWise is a deployment-time controller around two policies, a cheap π_small and a strong π_large; the small one acts by default. Each step t it builds a rolling window w_t of the last K (rationale, action) pairs — text straight from the agent’s generation logs, deliberately no screenshots or DOM deltas — scored by two ModernBERT-base encoders (149M parameters each):

- **Stuck monitor** S_φ(w_t) → p_stuck. Past a threshold θ_s the next step escalates to the large model, whose prompt gets the small model’s recent history re-serialized into its format so it can continue in place.
- **Milestone monitor** M_ψ(u, w_t) → p_mile, also conditioned on the task description u because milestones are goal-dependent. When it fires, the system assembles a milestone packet — the instruction, the trace since the last verified milestone τ_t, and before/after screenshots — and a stronger verifier answers two questions: is the segment advancing the goal (progress validity), and does the UI state match the intent (intent consistency)? Either failing escalates; a pass commits the milestone and saves the screenshot for the next checkpoint.

The training signal is fully synthesized: 300 trajectories from running the small agents, with GPT-5.2 labeling each window stuck vs not (w_t only) and milestone-completed vs not (u, w_t). Each trajectory is labeled in five independent runs — positive at ≥3 hits, negative at 0, discarded at 1–2. The encoders are fine-tuned with class-balanced cross-entropy (5 epochs, AdamW, 80/20 split); thresholds (θ_s, θ_m) trade success against cost.

## Results, as reported

Everything here is online, execution-checked success; costs are OpenRouter reference prices and latency is measured on a 2× H100 local deployment. The paper reports no seeds, variances, or confidence intervals. OSWorld pairs small models EvoCUA-8B and Qwen3-VL-8B with large models Claude Sonnet 4.5 and Kimi K2.5; WebArena-Verified pairs gpt-oss-20b and AgentTrek-32B with GPT-5 mini and GPT-5.2.

| Setting (OSWorld)        | Acc.  | Cost/task | Lat./req. |
|--------------------------|-------|-----------|-----------|
| EvoCUA-8B alone          | 43.3% | \$0.022   | 2.6s      |
| Qwen3-VL-8B alone        | 30.8% | \$0.018   | 3.9s      |
| Claude Sonnet 4.5 alone  | 58.1% | \$0.881   | 6.4s      |
| Kimi K2.5 alone          | 60.1% | \$0.132   | 8.3s      |
| EvoCUA-8B + Sonnet 4.5   | 55.4% | \$0.224   | 4.1s      |
| EvoCUA-8B + Kimi K2.5    | 58.2% | \$0.051   | 4.5s      |
| Qwen3-VL-8B + Sonnet 4.5 | 54.3% | \$0.423   | 5.2s      |
| Qwen3-VL-8B + Kimi K2.5  | 59.3% | \$0.078   | 6.5s      |

| Setting (WebArena-Verified) | Acc.  | Cost/task | Lat./req. |
|-----------------------------|-------|-----------|-----------|
| gpt-oss-20b alone           | 37.6% | \$0.001   | 6.9s      |
| AgentTrek-32B alone         | 30.3% | \$0.005   | 3.9s      |
| GPT-5 mini alone            | 55.0% | \$0.053   | 11.1s     |
| GPT-5.2 alone               | 60.1% | \$0.335   | 19.6s     |
| gpt-oss-20b + GPT-5 mini    | 51.3% | \$0.027   | 8.5s      |
| gpt-oss-20b + GPT-5.2       | 57.8% | \$0.211   | 12.2s     |
| AgentTrek-32B + GPT-5 mini  | 52.3% | \$0.028   | 9.4s      |
| AgentTrek-32B + GPT-5.2     | 58.8% | \$0.208   | 13.4s     |

The headline savings, in the paper’s own words: Qwen3-VL-8B + Kimi K2.5 reaches 59.3% on OSWorld, “very close to the 60.1% of standalone Kimi K2.5”; EvoCUA-8B + Kimi K2.5 achieves 58.2% at \$0.051 per task, “reducing the cost by 61.4%”; and the contributions claim cost reductions of up to 74.6% and latency reductions of up to 45.8% versus always-large policies. Across the eight cascades, the large model handles 37.4–69.4% of executed steps, and 46.8–73.0% of tasks invoke it at least once. A cross-cutting observation: final success tracks the choice of the large model much more than the choice of the small one — “the small model mostly governs cost, and the large model mostly governs final accuracy.”

## What the paper’s own controls say

**Component ablation (Figure 3).** With Kimi K2.5 on OSWorld, EvoCUA-8B goes 43.3% (no detector) → 49.7% (stuck only) → 53.2% (milestone only) → 58.2% (both); Qwen3-VL-8B goes 30.8 → 52.1 → 47.6 → 59.3. With GPT-5.2 on WebArena, gpt-oss-20b goes 37.6 → 44.9 → 54.7 → 57.8 and AgentTrek-32B 30.3 → 49.6 → 48.9 → 58.8. Either detector alone beats none; both together is best on every pair; and the split matches the failure signatures — loop-heavy Qwen3-VL-8B gains most from stuck detection, while gpt-oss-20b, which repeats less but drifts more, gains most from milestones.

**Event-driven vs fixed-interval (Table 3).** A periodic baseline invoking the same large-model check every k steps (best of k ∈ {3, 5, 7}) reaches 55.1% at \$0.07 per task on OSWorld versus 58.2% at \$0.05 event-driven, and 52.5% at \$0.24 versus 58.8% at \$0.21 on WebArena. Periodic checking is never cheaper, and on shorter WebArena trajectories markedly less accurate.

**Detector quality (Table 4).** On a held-out 20% split of the EvoCUA-8B data, the stuck detector reaches 93.9% accuracy and 91.5 F1; the milestone detector 94.1% and 62.0 F1, with F1 emphasized because milestones are sparse and ambiguous. Independent GPT-5.2 runs agree at 96.5% / 92.7 F1 (stuck) and 94.3% / 77.1 F1 (milestone) on the same data.

## Where the evidence is thinner, in the paper’s words

- The monitors and verifier are validated only against their own teacher: agreement with GPT-5.2 labels, not human ground truth, and the paper does not test whether the policy exploits the checker — CUA Radar flags this as AP4 (judges without two-sided reliability validation).
- No seeds, variances, or confidence intervals are reported for any benchmark number.
- Held-out environments are unclear in the judgment record. The paper states that “we always evaluate on tasks that are disjoint from those used as gold trajectories for data generation,” but training and evaluation tasks come from the same benchmark suites.
- Costs are OpenRouter reference estimates, not metered bills.

## CUA Radar’s read

CUA Radar scores this paper **63 (★★)**, evidence level **transfer**, reflecting what it reports: fully online evaluation on OSWorld and WebArena-Verified, strong baselines including a budget-comparable periodic-checking control, cost and latency reporting, a component ablation, and detector-level measurements against a GPT-5.2 reference. The judgment record also flags what is missing: variance reporting, held-out environments, a code check, and human-side validation of the learned judges (AP4). CUA Radar did not rerun anything; every number here comes from the paper (version v1).
