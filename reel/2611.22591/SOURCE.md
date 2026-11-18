# PACT (2611.22591) — SOURCE

论文：*PACT: Plan-Action Consistency Training by Preserving Correct Plans and Repairing Actions in GUI Agents*，arXiv 2611.22591v1，2026-11-17。
缓存全文：`research/fulltext/2611.22591.txt`（FULLTEXT: html）。核对于 2026-11-18（本仓 selection-018，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 执行缺口（计划对/动作错）定义 | "correct immediate plan … yet emit an action that fails to execute it" | Abstract，§1，Figure 1 |
| 点 + 按钮却发 application-launch 例子 | "may state that it will tap a visible + button, yet emit an application-launch command" | §1 |
| 负优势广播惩罚有效计划 | "broadcasting a negative response-level advantage … penalizing valid planning" | Abstract，§1 |
| 不改原始动作奖励 | "without altering the original scalar action reward" | Abstract，§4.1 |
| 同 Qwen3.5-9B SFT 初始化（冻结 π_ref）、同 10k 数据、KL η=0.01、1250 迭代×2 epoch | Training 段 | §5（Table 3 后） |
| 四配置 O/OA/OAR/PACT 定义 | Table 2 | §4.5 |
| AndroidWorld 60.34→61.21→62.93→68.97 | Table 3(B)，Δ 行 | §5，§6.1 |
| +8.63/+6.04/+7.76 pp | "+8.63 pp over O (60.34%), +6.04 pp over OAR, and +7.76 pp over OA" | §6.1 |
| OSWorld 40.92→44.17（+3.25，163/369） | "solves 163 tasks (44.17%), surpassing O (151, 40.92%) by 12 tasks" | §6.2 |
| AC High C_rule 83.71→89.74 | Table 3(B)，§6.1 | §5 |
| ScreenSpot-v2 Mobile 91.82(460/501)→96.01(481/501) | Table 3(B)，§6.1 | §5 |
| OA 使 C_rule 降至 80.04、ΔE +129 | Table 3(B)（OA 80.04）；Table 4（OA ΔE −31 High）——注意：**ΔE +129 是 OAR @ AC High** | Table 4，§6.3 |
| OAR 86.43 与 PACT 89.51（High 保留率） | "OAR 86.34 … PACT 89.51%" | §6.3（正文 86.43 为 C_rule，Table 4 保留率 86.34） |
| W→R 631 / R→W 553（PACT @ AC High）；OAR R→W 720 | Table 4 | §6.3 |
| 保留率 89.51/92.37 vs OAR 86.34/89.07；净正确 +207/+313 | "retention … 89.51% … 92.37% … +207 and +313 correct actions over OAR" | §6.3 |
| fixed-plan 56.52(13/23)→100(23/23)，OA 95.65(22/23) | Table 5 | §6.4 |
| 自由生成 joint repair 43.33→63.33（+20pp）；24 状态 18/24 vs 13/24 | Table 6，"raising joint repair from 43.33% to 63.33% (+20.00 pp)"，"preserves five more correct plans (18/24 vs  13/24)" | §6.5 |
| 式 5 钳位 max(A,0)，不冻结参数不遮 KL | Eq.(5)，"without … freezing shared model parameters or masking the KL regularizer" | §4.3 |
| y⁺/y⁻ 配对、stop-grad 权重（式 7-8）、不入 rollout 组 | Eq.(6)-(8)，"repair suffixes never affect group statistics"，"without entering the rollout batch" | §4.1，§4.4 |
| 推理保持标准单遍接口 | "At inference, PACT uses the standard single-pass reasoning–action interface" | §4.4 末 |
| 局限：单骨干 9B、选择器需显式计划、桌面诊断缺、跨论文口径 | Limitations 段 | §7 |

## 勘误说明（画报呈现口径）

画报"朴素修复反而更糟"栏写 "ΔE +129（错误变多了）"紧接 OA 的 C_rule 80.04 呈现。原文 Table 4 中 **ΔE +129 属 OAR（AC High）**，OA 的 ΔE 为 −31；但 OA 在 AC Low 的 ΔE 为 +220、且 C_rule 降至 80.04（低于 O 的 83.71）的正是 OA。为避免张冠李戴，此条已在画报上改写为"净错误变化 +129（OAR，AC High）"关联到 OAR 回 86.43 的分句——见 QA.md 记录的修正。最终画报文字为："加上选择（OAR）回到 86.43，再加计划保护（PACT）到 89.51 且 ΔE −78"。ΔE −78 属 PACT（Table 4），无误。

## 编辑收窄

- "+8.63 个百分点（对 O）"严格按 Table 3(B) Δ 行；未使用任何相对增幅表述。
- 机制区两张卡严格对应 §4.3（钳位）与 §4.4（偏好代理），公式编号照抄原文。
- Table 3(A) 的跨论文比较只在限制框提"非同条件重跑"，不做画报主证据。
