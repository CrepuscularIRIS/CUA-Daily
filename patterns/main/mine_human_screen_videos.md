# Mine Human Screen Recordings into Action Knowledge
_id: `mine_human_screen_videos` · sub-patterns: R03 · 1 candidate_pattern · 0 case · domains: board-induced (2026-10-19), from wave-1 weak fits (1 R) · outcome labels: none in this build_

**Definition.** Use recordings of humans operating software — public tutorial videos or a single recorded demonstration — as the source of GUI knowledge: segment them into key frames, localise elements and cursor, and either infer the actions between frames with a VLM to build training trajectories, or inject the demo's key frames into an acting agent's context. The data come from human screen videos, not from the agent's own runs, logged interaction traces or rendered structure.

**Operational signature.** find recordings (how-to posts → video search, or record one demo) → filter (screen visible, no occlusion, platform) → key-frame detection (OCR-text change, frame similarity, pixel change) → element/cursor detection + OCR (set-of-marks) → (a) VLM infers per-transition actions with narration and neighbouring frames → pretrain/SFT, or (b) sliding window of demo frames in context + reflection against the demo → act

**When to apply.** When target platforms or apps change faster than annotated datasets, public or cheaply recorded videos of the procedures exist, and screen text is legible enough to anchor scene changes and actions.

## Sub-patterns
| id | status | name | operation (abridged) |
|---|---|---|---|
| [R03](../sub/R03.md) | candidate_pattern | Mine operational knowledge and trajectories from human screen-recording videos | key-frame human recordings, localise elements and cursor, infer actions with a VLM into trajectories for training, or inject demo frames into the agent's context… |

## Success conditions
_Derived from the member card's When-it-works lines; each is phrased as a property checkable in a paper's text._
- **Extraction validated against human labels.** Scene segmentation, element detection and inferred actions are scored against human annotation of held-out videos (scene F1 95.04; action accuracy 80.90% / touch 91.84%) (2505.12632#board).
- **Transfer to an unseen platform or app.** Models trained with the mined data are tested on a platform or app absent from it (Windows Mobile 38.54 -> 51.71) (2505.12632#board).
- **Compared with written knowledge or existing datasets at counted cost.** The video source is compared with manually written knowledge or human-annotated data, with authoring/annotation cost reported (86.7 vs 63.3 SR; 0.7 vs 5 min; $0.34 vs $5.76 per video) (2502.17110#board, 2505.12632#board).
- **Context used for labelling ablated.** The contribution of narration, neighbouring frames and multi-step identification is ablated (80.90 vs 78.20 without narration, 70.63 one-step) (2505.12632#board).
- **Generalisation beyond the demonstrated task.** Performance is reported when the video does not match the test task (misaligned videos; one video per scenario for harder tasks: 31.3 vs 18.9) (2502.17110#board).

## Failure modes
_Derived from the member card's When-it-fails lines; each names a design or evidence property whose presence signals the failure._
- **Demonstration aligned with the evaluated task.** Each test task comes with its own demo video on an author-built benchmark, so gains measure replay of the shown procedure (2502.17110#board).
- **Noisy VLM-inferred labels used unchecked.** Action labels are produced by a proprietary VLM with residual error (80.90% accuracy) and used for training without filtering or error analysis of downstream effect (2505.12632#board).
- **Offline matching or captioning as the only evidence.** Results are exact action matching on static sets or captioning metrics, with no acting agent evaluated online (2505.12632#board, 2503.20978#board).
- **Key-frame loss or context overload.** Key-frame sampling may omit essential frames and longer frame windows add irrelevant ones, degrading decisions without a reflection or window ablation (2502.17110#board).
- **Coverage narrowed by filtering.** Aggressive filtering (20K of 129K videos; unobstructed phone screens only) restricts the platforms and interaction styles covered (2505.12632#board).

## Accepted vs rejected gap
pending — no outcome labels in this build

## Reviewer expectations
_Existing ids from the frozen domain profiles that apply to this pattern._
- **E28 (other, common_practice).** Separate the knowledge/data source from the evaluation tasks (held-out apps, misaligned demos) and report out-of-distribution transfer.
- **E15 (metric, common_practice).** Do not rest an agent capability claim on offline step accuracy alone; add an online benchmark.
- **E10 (metric, common_practice).** Validate VLM-produced labels against human labels.

## Related anti-patterns
[AP5](../anti-patterns.md#ap5), [AP7](../anti-patterns.md#ap7), [AP10](../anti-patterns.md#ap10), [AP18](../anti-patterns.md#ap18)
