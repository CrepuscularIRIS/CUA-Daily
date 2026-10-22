# REBASE: keeping a phone GUI agent’s cached experience correct after an app update

*A CUA Radar reading of arXiv 2609.32130v1 (Wu, Huang, Zhao). This is a third-party summary of what the paper reports, not an endorsement by the authors. Poster: `poster.png`. Paper: https://arxiv.org/abs/2609.32130v1*

## The problem: a stale path does not look broken

A GUI agent that ships on a phone runs a small model and reuses experience: action paths recorded on earlier runs, consolidated by the vendor in the cloud and cached on the device. When the app updates, some of those paths become partly wrong without becoming unusable. On nine real version pairs, the paper reports that an agent carrying old-version experience succeeds 10.1 points less often than one carrying none. The failure is silent: in 62.2% of executions a step the update broke still finds an element to act on, so the agent notices the mismatch only 3 steps later. Two signals go unused. The vendor’s cloud can often get the new version before the device does, and the device knows it has updated before it fails.

## What REBASE is

REBASE (Replay-Backed Attestation with Staged Evidence) is a device-cloud protocol, not a trained model. The device runs Qwen3-VL-8B-Instruct at INT4 on a Jetson AGX Orin; the cloud agent is Gemini 3.1 Pro; a Jetson AGX Thor acts as gateway and hosts a virtual Android device. The agent observes the accessibility tree and replays recorded paths whose steps are bound to elements by a fingerprint (role, label, normalized box and a two-ancestor hash), acting by executing those steps. On the CUA Radar board it sits in pattern C19, reusing the agent’s own experience.

Two clocks drive the protocol:

- **Update clock** (a version changes). The cloud replays its copy of each path on the new version without any model call, finds the first failing step per path, re-derives a patch and pushes one bit per path plus a step index. On the device, every recorded step is verified before and after execution: the element must be on screen, and the successor screen must match the recorded one.
- **Failure clock** (a verification mismatch). The device sends evidence in increasing size and stops at the first level that lets the cloud produce a tested patch: L0 the fingerprint and failing step, L1 an accessibility-subtree diff, L2 a low-resolution crop, L3 a screenshot. The cloud proposes candidate elements, tests them on the virtual device and commits the patch under a version key (app, version, element), so one repair serves every device in the fleet.

The signal is what the verification and the virtual-device test report; nothing is fine-tuned. The paper’s measurement behind the ladder: an accessibility-subtree diff repairs 79.1% of failing steps, a fingerprint alone 27.4%, and the crop, the 298 KB screenshot and the complete trajectory each add about 9.4 points, at a screenshot median of 36.6 times the bytes of the diff.

## Results, as reported

All results are online on AndroidWorld: nine apps, each with two releases (the pinned one and the next F-Droid release that changes an accessibility tree on a recorded path), five tasks per pair, 45 units in total. Six pairs are obtainable by the cloud and three are blind (the cloud cannot get the new version). Each arm runs K = 5 post-update episodes under three seeds, with an episode capped at 30 steps or six minutes. Success is read from app state by the evaluator, so no model judges it. Succ@K is the success rate across the K episodes.

| Method | Succ@K (%) | Uplink KB | Cloud calls | Device J |
|----|----|----|----|----|
| No experience | 47.7 ± 2.0 | 0.0 | 0.00 | 1730 |
| Stale experience | 37.6 ± 2.5 | 0.0 | 0.00 | 940 |
| Re-explore on failure | 69.3 ± 4.5 | 0.0 | 0.00 | 1612 |
| Screenshot to cloud (MAI-UI form) | 92.9 ± 0.8 | 2912.0 | 9.60 | 539 |
| Trajectory upload (CoMIC form) | 92.1 ± 1.1 | 883.9 | 0.30 | 1042 |
| **REBASE** | **93.8 ± 1.3** | 2.5 | 0.20 | 702 |
| Cloud-only agent (capability bound) | 97.5 ± 1.1 | 3825.7 | 12.57 | 152 |

Against stale experience, REBASE raises Succ@K by 56.1 points (95% interval \[51.6, 60.6\]) and is within 0.4 points of fresh experience recorded on the new version (interval \[-2.1, 3.0\]). It recovers in the first episode for 91.1% of cloud-visible units and 68.9% of blind units, against 28.1% for re-explore. The paper states 708 times fewer bytes and 47.3 times fewer cloud calls than screenshot-to-cloud, and 215 times fewer bytes than trajectory upload. Screenshot-to-cloud matches REBASE on Succ@K because the cloud completes every broken episode; it never returns to autonomous success.

## What the paper’s own controls say

**Ablations (Succ@K, nine pairs).** Without the update clock 90.5; without the failure clock 80.6 (on blind pairs 56.4 against 88.0, on cloud-visible pairs 92.7 against 96.7); cloud blind 90.5; without device verification 90.4; evidence fixed at the screenshot level 93.0, but with 14.4 times the uplink bytes; fixed at the diff level 84.0; text guidance instead of an executable patch 80.4. The paper says the small model replays a recorded action more reliably than it interprets repair advice.

**Link tiers.** From 50 down to 2 Mbps and from 20 up to 250 ms round-trip time, REBASE keeps Succ@K within 2.7 and 4.0 points of the fastest tier, with episode latency between 32.5 and 33.2 seconds; screenshot-to-cloud latency rises from 48 to 61 seconds.

**Fleet and energy.** With version keys, cloud re-derivations in a trace-driven fleet of 100 devices are 80.0 times fewer than without keys. Per episode the device uses 2.5 times less energy than with no experience and 2.3 times less than re-explore, but more than screenshot-to-cloud (539 J against 702 J) because the cloud does more of the inference there.

## Where the evidence is thinner

- One testbed: two Jetson devices and a gateway, nine Android apps, one release pair each. Only three pairs are blind, and the 100-device fleet is trace-driven rather than real.
- The two baselines are re-implementations “in the form of” MAI-UI and CoMIC, not those systems end to end.
- The approach relies on an accessibility tree: “every measured failure in our nine apps exposed a subtree”, and screens without one (a canvas, an opaque web view) start at the crop level. The paper lists desktop agents as next.
- Standard deviations are over three seeds.
- The paper contains no limitations section and no link to code; the CUA Radar record marks code as unclear.

## CUA Radar’s read

CUA Radar scores this paper **68 (★★)**, evidence level **online**. The record credits online evaluation with an app-state evaluator, standard deviations over three seeds, takeover and trajectory-upload baselines under matched K and step cap, cost reporting and a component ablation; it marks held-out evaluation as partial (the three blind pairs) and records no flags. The radar did not rerun any experiment; every number here comes from the paper (version v1).
