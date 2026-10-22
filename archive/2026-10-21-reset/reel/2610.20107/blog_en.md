# Why Generate a Click? Plug-in decision heads that read the action from the prefill

*A CUA Radar reading of arXiv 2610.20107v1 (Gan, Liang, Wei, Zhang, Cai, Ni). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.20107v1*

## The problem: the agent writes out choices it has already made

A web agent built on a vision language model acts by writing. At each step it reads a goal and a screenshot whose elements carry numbered boxes, then generates a string such as `click(6)` or `type(5, "chair")`. As the paper puts it, “Most of this string records a choice from a short list: one of eleven action types and one of a few dozen boxes.” Writing that choice costs one sequential decoding pass per token, and only typing or answering text is genuinely open ended. The question the paper asks: by the time the generator writes its first token, it has already read the goal, the history and every box — so is the decision recoverable from the hidden states of the prefill, and can an agent use cheap heads on the well-read steps and generation on the rest, without paying for both?

## What the method is

**The agent.** A visual web agent on desktop websites. It perceives a Set-of-Mark screenshot (each of N candidate elements drawn as a numbered box), the goal, the history of earlier actions in Mind2Web’s text form, and a list of text options from the goal and the page. It acts through an action grammar with eleven types (click, type, select, hover, clear, enter, scroll down, scroll up, go back, answer, no operation); a harness parses and executes the string. The generator is Qwen3-VL-4B-Instruct or Qwen3-VL-8B-Instruct with a rank-16 LoRA adapter. On the CUA Radar board this sits in sub-pattern C05, an attention action head over visual patches on a frozen backbone.

**The mechanism: plug-in decision heads plus a confidence cascade.** Three small heads (6.0M parameters on the 4B generator, 9.2M on the 8B, about 0.1% of the backbone) read a learned scalar mix of five of the generator’s 36 layers (12, 18, 24, 30, 36) followed by layer normalization. A **type head** attention-pools the whole prefill into a distribution over action types, restricted to types the page allows. A **target head** averages the visual tokens inside each numbered box (Qwen3-VL encodes each 32 x 32 cell as one token) and scores the box against a learned query, so it needs box coordinates but no element text. An **argument head** scores each listed text option pointer-style, plus a learned WRITE slot. The confidence cascade takes the product c = p(type) p(box \| type) p(argument \| type, box): above a threshold τ the agent acts at once with no decoding; if the argument head picked WRITE, the generator writes only the text (at most 24 tokens) from the cached prefill; below τ the generator decodes the whole action from the same KV cache — one forward pass serves both readouts.

**Training signal.** The generator trains for one epoch on 213k web steps converted into this format (successful MiniWoB++ episodes, Multimodal-Mind2Web training split, GUIAct single and multi step tasks, UGround grounding, WebLINX demonstrations). The heads then train for one epoch on the same demonstrations with the generator frozen, on the demonstrated (type, box, argument) triple plus an auxiliary binary loss on whether the step completes the task. For WebArena both continue for three epochs on 1,298 replayed steps of successful expert trajectories (from a GPT-5.5 Set-of-Mark agent) on 115 training tasks disjoint from the test tasks. The two thresholds were fixed in early MiniWoB++ experiments: τ = 0.9 strict, τ = 0.5 loose.

## Results, as reported

Online task success, mean over three training seeds; MiniWoB++ runs all 119 tasks with five environment seeds (12 tasks held out from training, at most 10 steps); WebArena runs 174 test tasks on six sites with at most 25 steps per task.

| Method (Qwen3-VL base) | MiniWoB++ 4B | MiniWoB++ 8B | WebArena 4B | WebArena 8B | Tokens/step 4B | Tokens/step 8B |
|----|----|----|----|----|----|----|
| Generator | 53.3 | 55.5 | 12.5 | 13.6 | 7.4 | 7.5 |
| Cascade, τ = 0.5 | 52.5 | 53.6 | 13.8 | 14.6 | 3.1 | 3.3 |
| Joint, generation | 53.3 | 55.0 | 11.5 | 11.1 | 7.3 | 7.4 |
| Joint, heads only | 45.4 | 45.3 | 3.1 | 4.4 | 0 | 0 |

At τ = 0.9 on MiniWoB++ the cascade reaches 53.1% (4B) and 55.4% (8B), within 0.2 points of the generator, with the heads acting alone on 29% and 33% of steps; at τ = 0.5 it gives up 0.8 and 1.9 points while the heads act alone on 67% and 69%. On WebArena the heads act alone on 52% (4B) and 51% (8B) of steps and decide a WRITE on another 17% and 14%, and episodes get shorter, from 15.7 to 14.0 steps per task (4B) and from 16.8 to 16.2 (8B). Offline (step success, a different axis): at τ = 0.9 the cascade stays between 0.3 points below and 1.4 above its generator on all seven test sets (three Multimodal-Mind2Web splits with unseen tasks, websites or domains, plus four GUIAct sets) while the heads decide 12 to 64% of the steps; at τ = 0.5 step success on unseen Mind2Web websites rises by 3.1 (4B) and 1.8 (8B) points, and the GUIAct sets lose 1.0 to 1.9 points. Timing on MiniWoB++: 0.234 s/step for the 4B generator against 0.207 at τ = 0.9 (1.13x) and 0.168 at τ = 0.5 (1.39x).

## What the paper’s own controls say

**Template split (the decisive one).** The whole WebArena gain comes from the 47 test tasks whose intent template also occurs among the 115 replayed training tasks: 34.8 to 41.8 (4B) and 33.3 to 36.9 (8B). On the 127 new-template tasks both systems stay below 7%; the cascade trails the 4B generator by 0.8 points and ties the 8B one.

**Joint training is not free.** Training heads and generator in one adapter lowers the generator’s own step success by 0.5 to 4.9 points on the offline sets (validation loss 0.214 to 0.235 at 4B), though the joint heads themselves gain 0.3 to 1.9 points; a two-model cascade (joint heads, separate generator) gives the best Mind2Web results, up to 3.8 points above the generator under the standard protocol.

**Head swap.** Replacing the target head with the patch attention head of GUI-Actor (trained the same way, GUIAct held out): heads-only box pooling is ahead on four of five test sets, e.g. 37.3 against 35.3 on M2W cross-task; attention mass fails on M2W where 82% of steps contain a larger enclosing candidate.

**Routing is not random.** On the steps the heads decide (37% of M2W cross-website), they succeed 68.6% where the generator would give 60.3; random allocation of the same share would give 39.8% against the cascade’s 44.0. Typing improves by 9.1, 9.1 and 6.3 points across M2Web splits, selecting from 14.8 to 39.8 on unseen websites.

**Reference points.** Under the standard Mind2Web protocol, Aguvis 7B is ahead of all systems in this paper on the three splits (60.4 / 54.6 / 56.6 step success). A reasoning generator that writes a thought before each action trails the plain generator by 4.0 points and is seven times slower; heads on it act alone on two thirds of steps and cut time from 1.56 to 0.70 seconds per step.

## Where the evidence is thinner, in the paper’s words

- “Our heads choose among numbered boxes, so agents that act through raw screen coordinates would need a different target head.”
- “The heads are tied to one generator; after fine-tuning the generator for WebArena we trained them again.”
- “All experiments use Qwen3-VL backbones and a single action grammar, and the threshold is fixed per experiment.”
- Success on WebArena “follows the WebArena checkers, with GPT-5.5 judging answers that need fuzzy matching” — the judge itself is not separately validated, and the judgment record marks this untested.
- No code repository is listed on the board.

## CUA Radar’s read

CUA Radar scores this paper **61 (★★)**, evidence level **online**. The score reflects what the paper reports: online evaluation on WebArena and MiniWoB++, every success rate averaged over three training seeds, budget-matched comparisons (every system shares the same generator, prompt and boxes), token and time cost, and component ablations (threshold sweep, joint training, target-head swap, template split). The judgment record marks the held-out environment question partial (WebArena training tasks are replayed expert trajectories, disjoint from the test tasks but sharing intent templates), the judge validation untested, and the code status unclear; it flags no anti-patterns. The radar did not rerun any experiment; every number here comes from the paper (version v1).
