# WebMix: a scout writes the site manual, a router remixes the LoRA bank

*A CUA Radar reading of arXiv 2610.22539v1 (Md Farhan Ishmam, Minh Pham-Dinh, Kenneth Marino; Kahlert School of Computing, University of Utah). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2610.22539v1 · Project page: https://webmix-hyper.github.io/ · no public code repository listed at review time.*

## The problem: every new interface means a new adapter

Small open-weight models become competent web agents only after fine-tuning, usually through a LoRA adapter on a frozen base — and “every new site or redesign calls for a new corpus and a new adapter.” Mind2Web reports a steady drop from cross-task to cross-website and cross-domain splits, and TimeWarp (six eras of web design) shows an agent trained on one era degrades on the next. Demonstrations are expensive, and sites get redesigned before corpora grow. Recent methods cut the supervision but “treat each new interface as a separate adaptation problem … none of them learns how to adapt.” Directly generating adapter weights with a hypernetwork is hard: a family of interfaces gives only a handful of conditionings for millions of weights, and LoRA factors are not identifiable. WebMix’s answer: don’t generate weights, compose them.

## What WebMix is

The agent is a text-based web agent on the BrowserUse harness: it reads a goal, the current page’s accessibility tree and its history, and emits one browser action at a time (click, typed string, scroll); a task succeeds if a verifier accepts the final state of the website. Platforms are self-hosted websites — TimeWarp (domains Wiki, News, Shop, each in six versions) and WebArena-Lite-v2 (Reddit, GitLab, CMS, Map, OSS) — with base models Qwen-3.5 4B and Llama-3.1 8B. On the CUA Radar board this is pattern C19, “accumulate reusable knowledge from the agent’s own runs” — except the knowledge is a bank of per-interface LoRA adapters and the retrieval is a mixing of weights. WebMix has four pieces:

1.  **Adapter bank.** One LoRA per source interface (rank r = 16, scale α = 32, on attention q/k/v/o and MLP gate/up/down projections), trained by supervised fine-tuning plus a KL-anchor term (β = 1.0, a clipped k3 estimator, bounds \[−20, 8\]) penalizing drift from the base policy on the *other* source interfaces’ demonstrations. The bank is then frozen.
2.  **Scout (entirely frozen).** For version transfer an explorer runs a task-free breadth-first crawl: up to 25 pages per site at link depth 3, plus one search probe. For domain transfer the frozen base policy attempts n = 1 task from the training split and the explorer replays the visited pages. A frozen writer LLM (Qwen-3.5 9B, temperature 0) condenses the record into a seven-section manual (plus a worked-path section for domain transfer); a frozen encoder (BGE-large-en-v1.5, d_c = 1024) embeds it.
3.  **Router.** A two-layer perceptron (hidden width 256, SiLU, zero-initialized output so training starts from the uniform mixture; about 0.26M parameters) maps the manual embedding to a softmax over K mixing coefficients, one per bank adapter. Composition concatenates the bank factors along the rank dimension: one standard LoRA of rank at most Kr and scale α_out = Kα, served by an unmodified stack, never larger than the biggest bank adapter.
4.  **Training and adaptation.** Stage 2 trains only the router (500 steps, AdamW) with a behavior-cloning loss on the pooled source corpus, gradients flowing through the composed updates and the frozen base. Adaptation is one scout visit plus one forward pass — no target demonstrations, no gradient updates on the target; adding an interface later adds one adapter and retrains the router only. The signal: expert demonstrations on the source interfaces, the KL anchor on the other sources, and the scouted manual as the only information from the unseen interface.

## Results, as reported

All numbers are online success rate (%), a verifier accepting the final state of the website; each is the average of three runs on the BrowserUse harness (non-rationale tokens, memory enabled). “Unseen” means the evaluated domain or version is left out of the training data and the in-context examples. No offline step or grounding metrics are reported. TW = TimeWarp, WAL = WebArena-Lite-v2.

| Model | Method | TW domains (unseen) | TW versions (unseen) | WAL overall (unseen) |
|----|----|----|----|----|
| Qwen-3.5 4B | Zero-shot | 22.92 | 18.28 | 21.86 |
| Qwen-3.5 4B | In-context learning | 25.42 | 20.06 | 24.89 |
| Qwen-3.5 4B | LoRA | 25.42 | 24.27 | 29.22 |
| Qwen-3.5 4B | **WebMix** | **33.75** | **27.51** | **34.42** |
| Qwen-3.5 4B | LoRA (in), seen specialist | 33.75 | 25.40 | 37.23 |
| Llama-3.1 8B | Zero-shot | 7.50 | 6.63 | 6.28 |
| Llama-3.1 8B | In-context learning | 7.08 | 6.15 | 4.98 |
| Llama-3.1 8B | LoRA | 8.33 | 16.99 | 12.12 |
| Llama-3.1 8B | **WebMix** | **15.83** | **18.77** | **16.67** |
| Llama-3.1 8B | LoRA (in), seen specialist | 15.83 | 17.64 | 22.29 |

Headline facts, as stated: 56.1% on unseen News with Qwen-3.5 4B (table: 56.06 vs 45.45 transferred LoRA), “exceeding transferred LoRA by 10.6 percentage points”; TimeWarp held-out domain gains of 8.3 points for Qwen and 7.5 for Llama-3.1 8B, nearly doubling Llama’s success and matching target-trained specialists on average (33.75 and 15.83, the LoRA (in) rows above). Version-transfer gains are smaller, 1.8–3.2pp; WAL gains are stated as 3.3–4.6pp. Transfer is strongest near the training domains: News gains 26pp over zero-shot with Qwen against ∼5pp on Wiki and Shop; OSS gains most on WAL (14–15pp). The paper names Map with Llama-3.1 as its one unseen-transfer failure case (every unseen baseline 0.00 there, WebMix 7.69). In the seen setting WebMix is best or tied-best in every column; with target domains in training, Qwen reaches 42.4% on WAL overall, 4.3 points above LoRA trained on all domains.

## What the paper’s own controls say

- **Same base models.** The zero-shot, ICL and LoRA baselines all run on the same two base models as WebMix.
- **Design ablation** (Table 3, Qwen, unseen TW domains, pooled): regressing stored adapters with Text-to-LoRA (T2L-Recons) reaches 16.25; training the same generator end-to-end (T2L-SFT) adds 9.17pp; the mixture hypernetwork adds 3.75pp; conditioning the router on the scout’s manual adds 4.58pp more — 8.33pp total over the strongest T2L variant (33.75).
- **Scouting budget.** n = 1 scouted task is best; n = 3 gives +1.5pp on News but costs 6–8 points on Wiki.
- **KL anchor.** β = 1.0 is the best tested value on every domain and on average; β = 0 lowers the average by over 7pp, and β = 3.0 also hurts.
- **Retention.** Transfer does not cost seen interfaces: +4.6–6.3pp over LoRA (all) on TW domains, +1.8–2.4pp on TW versions, +2.6–4.3pp on WAL. LoRA trained on all domains adds only 0.2–1.3pp over in-domain LoRA, so the gain is not just more data.
- **Analysis.** The bank’s adapters are close to orthogonal (pairwise cosine below 0.16, twice as similar without the KL anchor), and the router tracks similarity: held-out v1 is built from v2 (81%) and v3 (17%); with v6 in the bank, 96% of the weight goes to v6.
- **Theory.** Appendix D splits held-out imitation risk into an approximation term (distance from the oracle adapter to the bank’s convex hull) and a routing term; idealized direct generation is routing with unnormalized coefficients. Proofs are formalized in Lean 4.

## Where the evidence is thinner, in the paper’s words

- Version transfer is the weaker axis: gains of 1.8–3.2pp, and “LoRA is a strong baseline there.”
- The theory’s testable predictions are left untested: “The experiments of §4 do not include the transfer matrix, the uniform mixture, or the hull-distance panel, so these three predictions remain untested”; for bank growth, “The experiments of §4 include neither sequential arrival nor this curve.”
- No standard deviations or confidence intervals; each number is an average of three runs.
- Code: “The complete source code is included in the supplementary material and will be released publicly upon acceptance” — nothing public at review time.

## CUA Radar’s read

CUA Radar scores this paper **64 (★★)**, evidence level **transfer**, sub-pattern C19 (“accumulate reusable knowledge from the agent’s own runs”) under experience-memory retrieval. The judgment record credits online verifier-scored evaluation, properly held-out domains and versions, strong baselines on the same base models, and a component ablation; it marks variance (three-run averages, no std/CI), budget matching, compute cost and code availability as not reported or unclear. The radar did not rerun any experiment; every number here comes from the paper (version v1).
