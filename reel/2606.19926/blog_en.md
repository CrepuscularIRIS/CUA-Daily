# MemGUI-Agent: a mobile GUI agent that treats context management as an action

*A CUA Radar reading of arXiv 2606.19926v1 (Liu et al., Zhejiang University and Kuaishou Technology). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2606.19926v1 · Code (announced): https://github.com/kwai/MemGUI-Agent*

## The problem: long horizons break passive context

Mobile GUI agents handle short tasks but degrade as task length grows: the paper opens with GUI-Owl-1.5-8B dropping from 71.6% on AndroidWorld (average 8.4 steps) to 38.2% on MobileWorld (average 27.8 steps) and 11.7% on MemGUI-Bench (average 36.2 steps). The authors attribute this to ReAct-style prompting, which “passively accumulates per-step records, leading to prompt explosion and dilution of critical cross-app facts.” Prices, identifiers and copied text must survive screen changes and app transitions, but passive strategies append, truncate or discard records mechanically, while external-memory frameworks move curation outside the end-to-end policy.

## What MemGUI-Agent is

The agent is an end-to-end multimodal mobile GUI agent. It perceives a screenshot together with a structured state S<sub>t</sub> = (G, H<sub>t</sub>, M<sub>t</sub>, L<sub>t</sub>): the goal G, a Folded Action History H (compressed trajectory summaries), a Folded UI State M (persistent UI-derived facts), and a Recent Step Record L. It acts with exactly one action per step from A<sub>ui</sub> ∪ A<sub>mem</sub>: UI actions (click, long_press, swipe, type, answer, system_button, wait, terminate) on a 1000×1000 coordinate space, or memory operations (memory_add, memory_update, memory_delete) over triples (id, description, content) that store complete content, not summaries. The platform is Android-style: the snapshot-based MemGUI-Bench environment (26 apps) and the containerized MobileWorld (Mattermost, Mastodon, Mall4Uni).

The mechanism is **Context-as-Action (ConAct)**: context management becomes a first-class output of the same policy. Each step, the model emits a 5-part response — reasoning, a folding directive, the tool call, a grounded UI observation, and an action intent — in one forward pass. The folding directive specifies a history span and a generated summary; step-level distillation compresses the latest step, span-level abstraction summarizes a completed sub-task. On the CUA Radar board this is sub-pattern C16, “let the agent nominate task-relevant content to retain,” under the main pattern of structuring the prompted agent loop.

The training signal is **MemGUI-3K**: the 128 MemGUI-Bench seed tasks are expanded by entity substitution (456 tasks), memory-operation augmentation (289) and task simplification (6,558) into a 7,303-task pool; 5,293 are rolled out once by a Qwen3-VL-235B-Thinking teacher under the full ConAct protocol, judged by the MemGUI-Eval progressive scrutiny pipeline, and filtered at trajectory and step level (every step annotated reasonable or unreasonable). The result is 2,956 trajectories across 26 apps, averaging 28.8 steps (the paper notes 1.9× the 15.3 of GUIOdyssey), 75.7% reasonable steps, 64,430 SFT samples with verified zero overlap against the evaluation tasks. **MemGUI-8B-SFT** is Qwen3-VL-8B-Instruct fine-tuned on the 57,951 training samples with LoRA (rank 8, alpha 32), one epoch, seed 42, 535 minutes on 8×80GB GPUs.

## Results, as reported

All headline numbers are **online** (interactive runs). MemGUI-Bench: 128 tasks, up to 3 attempts, budget 2.5g + 1 steps (g = golden-step count), success judged by MemGUI-Eval. MobileWorld GUI-Only: 117 tasks, one attempt, 50-step limit, backend verifier.

| Agent (MemGUI-Bench) | P@1 | P@3 | IRR |
|----|----|----|----|
| M3A (Gemini-2.5-Pro, best framework) | 32.8 | 47.7 | 39.3 |
| Qwen3-VL-235B-Thinking | 24.2 | 46.9 | 30.0 |
| Qwen3-VL-8B-Instruct | 9.4 | 20.3 | 15.1 |
| MemGUI-8B-SFT | 23.4 | 35.9 | 30.2 |
| **MemGUI-Agent-235B** (zero-shot, weights unchanged) | **37.5** | **62.5** | **46.8** |

| Agent (MobileWorld GUI-Only)                | SR   |
|---------------------------------------------|------|
| GUI-Owl-1.5-32B-Instruct (best open-weight) | 43.9 |
| Qwen3-VL-235B-Thinking                      | 14.5 |
| Qwen3-VL-8B-Instruct                        | 9.4  |
| OpenMobile-8B (open-data)                   | 17.7 |
| **MemGUI-8B-SFT**                           | 17.9 |
| **MemGUI-Agent-235B**                       | 29.1 |

The paper reports +13.3 P@1 and +16.8 IRR over the same 235B backbone on MemGUI-Bench, +14.6 SR on MobileWorld for the 235B agent and +8.5 for the 8B, and calls MemGUI-8B-SFT the best open-data 8B performance. Gains concentrate on harder tasks (8B-SFT: Medium +19.0, Hard +18.5, Easy +6.2). **Offline** step-level skill metrics, kept separate: on the MemGUI-3K test split with gold context, UI action match rises from 29.2 to 36.3, memory trigger F1 from 19.9 to 48.0, deep-fold ratio from 8.8 to 26.1 (gold 23.2), format compliance to 99.9.

## What the paper’s own controls say

**Scale sweep (Table 1).** Zero-shot ConAct helps only the strongest backbone: P@1 on MemGUI-Bench-40 goes 10.0→5.0 (2B), 20.0→12.5 (4B), 12.5→7.5 (8B), 23.4→19.5 (235B-Instruct), but 5.0→40.0 for 235B-Thinking (P@3 27.5→62.5, IRR 19.5→51.0). This is the paper’s own motivation for supervised training.

**Component ablation (Table 5, MemGUI-Bench-40, zero-shot 235B-Thinking).** From a ReAct baseline of 5.0 P@1: + UI memory actions 17.5, + history folding 22.5, + self-describing step output 25.0, full ConAct 40.0 P@1 / 62.5 P@3. MTPR rises 0.143→0.429, IRR 19.5→51.0.

**Held-out transfer.** MobileWorld differs in environment, apps and protocol; the 8B still reaches 17.9 SR. Training data overlap with the 128 evaluation tasks was verified to be zero.

**Cost.** ConAct keeps prompt growth substantially flatter than ReAct over 150 steps, saving about 1.5k input tokens by step 150.

**Failure analysis.** Total failures fall from 99 to 58 (−41%), mainly process hallucination (−42%) and output hallucination (−57%); knowledge deficiency and intent misunderstanding stay roughly stable.

## Where the evidence is thinner, in the paper’s words

- Scale dependence: “on smaller open models and Qwen3-VL-235B-Instruct, the added protocol often reduces performance” — the zero-shot gains rest on one backbone.
- Scope: “Our experiments focus on Android-style mobile GUI environments. Extending ConAct to iOS, desktop, and web interfaces remains future work.”
- Code and data are promised rather than shipped in v1: “Code, data, and trained models will be released at https://memgui-agent.github.io/.”
- Variance across evaluation runs is not reported (seed 42 covers the SFT split and training); MobileWorld uses a single attempt per task.
- MemGUI-Bench and the MemGUI-Eval judge come from the authors’ earlier work, and the dataset teacher shares the Qwen3-VL-235B-Thinking backbone with the strongest zero-shot agent; on MobileWorld both MemGUI agents remain far below the best open-weight models (43.9).

## CUA Radar’s read

CUA Radar scores this paper **62 (★★)**, evidence level **transfer** — the held-out MobileWorld result is what carries the level. The judgment record credits online evaluation, a held-out environment, same-backbone deltas, a component ablation and cost reporting, and lists run variance and budget-match as unclear, the MemGUI-Eval validator as untested, and code as announced. It also flags two anti-patterns: AP15 (scaffold gains shown only on a frontier backbone) and AP18 (folding is lossy compression). The radar did not rerun any experiment; every number here comes from the paper (version v1).
