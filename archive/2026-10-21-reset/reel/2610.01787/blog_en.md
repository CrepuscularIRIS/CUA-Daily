# Component routing: which parts of a GUI agent’s experience belong in the weights, and which in the prompt

*A CUA Radar reading of arXiv 2610.01787v1 (Wu, Ding, Huang). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.01787v1 · Code: announced in the paper (“Code and data will be released”), no link given.*

## The problem: the same experience, two destinations, opposite verdicts

Self-improving GUI agents keep the trajectories they produce and hand them back to the agent, either by fine-tuning on them or by retrieving them into the prompt. Comparisons of the two destinations disagree across tool and web tasks. The paper attributes this to the unit of experience. A trajectory bundles items with different properties, so a conclusion about the bundle depends on its mix. In the paper’s weather-app example, fine-tuning on a whole trajectory learns where the search field is and loses that a city is saved by tapping Add on its preview.

## What component routing is

The agent is a phone GUI agent. Each step records a screenshot, the structured application state, the on-screen elements and the action with its target element; the agents act with their own native tap, type and swipe action spaces (coordinates). The platform is mobile: a simulated phone (MobileGym) and Android apps (AndroidWorld). In CUA Radar’s pattern board this paper sits in K27, “retrieve stored past experience into the agent’s context”, and its mechanism is experience memory plus a weights-versus-context decision.

An agent first runs a batch of tasks on its training applications and keeps every trajectory, successful or not. A rule-based extractor then splits this pool into four components, each with a key that identifies it across episodes:

- **Locators (G):** where a named element sits on a screen; the training sample is a screenshot paired with a click on the element.
- **Procedures (P):** a short run of three action targets that recurs inside a task family.
- **State facts (F):** a precondition that must hold before an action succeeds, taken from a failed and a successful attempt at the same target.
- **Lessons (L):** an action that failed in a state, paired with the one that later succeeded there.

Each component can go to the **context** (top five notes appended to the prompt, ranked by state similarity, exact matches first), to the **weights** (a LoRA adapter, rank 16, three epochs, learning rate 10^-5; preference optimization for lessons, supervised fine-tuning for the rest), or to both. The two routes consume the same extracted items and are read on the same held-out instances. The signal is the environment’s deterministic checker on the pool episodes; no model judge is used.

Two properties are measured on the pool before any training. **Recurrence** r is how often an item’s key returns in unrelated tasks. **State-conditionality** is how much an item’s usefulness depends on the current state matching its source state (a proxy, kappa_0, is computed from the pool). A linear rule, score = alpha r - beta kappa_0 - gamma, fitted on the route gains of the other backbone families, sends a component to the weights if the score is positive. The route gain is held-out success of the weights route minus that of the context route, on the same instances.

## Results as reported

Everything below is **online** held-out success, decided by each environment’s checker, mean of 3 seeds (the subscripts in the paper are the std). Backbones are GUI-Owl-1.5-8B, Qwen3-VL-8B and ScaleCUA-7B, each used as both producer and consumer. MobileGym: 20 applications, 224 held-out templates (165 new templates on practiced applications, 59 on unseen applications), 1 106 instances per seed. AndroidWorld: 58 held-out tasks, four instances each, 232 per seed. There is no offline step or grounding accuracy in the paper.

| Arm (MobileGym)              | GUI-Owl-8B | Qwen3-VL-8B | ScaleCUA-7B |
|------------------------------|------------|-------------|-------------|
| Base agent                   | 21.6       | 16.7        | 19.2        |
| Self-retry, three attempts   | 26.4       | 20.6        | 24.6        |
| Success-filtered fine-tuning | 22.2       | 17.3        | 20.0        |
| All to the context           | 29.6       | 27.3        | 28.7        |
| All to the weights           | 28.6       | 28.0        | 27.3        |
| **Routed (rule-assigned)**   | **34.8**   | **30.5**    | **34.3**    |
| Reverse assignment           | 25.2       | 24.4        | 23.2        |

| Arm (AndroidWorld)         | GUI-Owl-8B | Qwen3-VL-8B | ScaleCUA-7B |
|----------------------------|------------|-------------|-------------|
| Base agent                 | 23.6       | 17.8        | 24.0        |
| Self-retry, three attempts | 26.1       | 22.7        | 27.2        |
| All to the context         | 33.6       | 28.0        | 29.0        |
| All to the weights         | 29.0       | 28.2        | 29.5        |
| **Routed**                 | **33.3**   | **33.2**    | **32.6**    |
| Reverse assignment         | 27.7       | 23.4        | 27.9        |

The paper summarises this as routing exceeding the better single destination of each backbone by +3.5 points on average over three backbones and two environments, and the reverse assignment by +7.8. On MobileGym the average lead over the better single destination is +4.4; on AndroidWorld it is +5.0 with Qwen3-VL-8B and +3.2 with ScaleCUA-7B, and routing matches it with GUI-Owl-8B (Table E.2 gives -0.3 against all-to-context, interval -2.6 to +2.0). The best whole-trajectory baseline, self-retry, is +9.3 points below routing on MobileGym.

The route gain by component, pooled over backbones on MobileGym, is +4.9 for locators and +1.5 for lessons (weights ahead), and -4.2 for procedures and -4.1 for state facts (context ahead). The rule fitted with one backbone family held out recovers the sign in 24 of 24 cells, 19 of them with intervals clear of zero.

## What the paper’s own controls say

**Interventions on one property (MobileGym, gain over the base agent).** Serving the same notes retrieved by task text only, without the state condition, costs 3.9 points for procedures and 3.4 for state facts; the paper reads this as the context route buying the condition, not the payload. Copying every procedure item eightfold before fine-tuning raises the weights route by +3.5 and moves the route gain of procedures from -4.2 to -0.8 (across zero on Qwen3-VL-8B); for state facts the shift is +3.6.

**Controls on the instrument.** Random notes from other applications change the base agent by -1.6; shuffled keys or shuffled training labels leave it within 1.1 points. The paper concludes that neither the prompt format nor fine-tuning itself produces the gains.

**Producer and consumer.** Notes help whichever model produced them (the 8B consumer gains +3.6 from its own procedures, +4.8 from the 32B model’s). Fine-tuning on another family’s samples hurts (-7.5), and most of the weights gain on own procedures is practice (+0.6 from own procedures alone against +0.9 with all samples).

**Cost (Appendix H, MobileGym, GUI-Owl-8B).** Routed training uses 6.1 GPU-hours against 15.4 for all-to-the-weights; routed prompts carry 1.07 times the base agent’s tokens.

## Where the evidence is thinner, in the paper’s words

- Budget: “Two quantities the budget does not equalize are reported in Appendix H: the notes block that the context route adds to every prompt, and the adapter training run that the weights route adds.” Self-retry uses three attempts per instance; every other arm runs one.
- The AndroidWorld cells “repeat the pattern with the wider intervals of a smaller task set”; lessons lean toward the weights “by a margin whose interval includes zero in half of the cells”.
- Held-out means held-out templates. Applications used for experience also appear in the “new templates on practiced applications” tier (165 of 224 MobileGym templates); only the unseen-application tier (59) and AndroidWorld’s 8 held-out applications are unseen apps.
- The rule is fitted on 24 cells (three 7 to 8B backbones, two environments), with one LoRA configuration for all arms. Code and data are announced, not yet released.

## CUA Radar’s read

CUA Radar scores this paper **73 (★★★)**, evidence level **transfer**. The judgment record marks as present: checker-scored online evaluation, held-out applications and templates, variance over three seeds, strong baselines (whole-trajectory fine-tuning and retrieval, self-retry) and a component-level ablation. It marks budget matching and cost reporting as unclear and records code as announced; it records no anti-pattern flags. The radar did not rerun any experiment; every number here comes from the paper (version v1) and the plain differences quoted are the ones the paper states.
