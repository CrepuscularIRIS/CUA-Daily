# 校准冻结报告 — gui-v22-20261021-01(2026-10-21)

## 结论

**rubric 冻结**:SCORE_SPEC v2.2 draft 权重(G15 / M25 / X20 / E40=10+10+10+5+5,总和 100)经留出集一致性检验通过,作为本 run 生产评分的冻结 rubric。锚点澄清 r1(unknown vs not_reported 协议)一并冻结为执行读法。

## 开发集(c1,6 篇)

双席盲评 + Opus 聚合全部完成:5 篇 a1 accepted + 1 篇 a2 材料升级重评(2610.23857,PDF 路径)。
锚点观察(从 Opus 裁决与共有错误纠正提取,不构成权重修改):
- HTML 渲染丢 listing/Box 是系统性材料缺陷 → 材料管线修复(渲染器 + PDF 兜底),不是锚点问题。
- "留存修改"与"证实保留提升"的混淆在两席共有错误中出现 → 已作为聚合固定检查项。

## 留出集一致性(c2/c3 a1 + re1 并集,12 篇)

- 可评分对:**10**(≥8 ✓);排除:2609.29892 双席 out_of_scope、2604.11784 sol G-unknown(聚合阶段经 MAI-UI 参考解决)。
- 中位 |sol−son55| 总分差:**2.5**(≤5 ✓)
- 差 ≤10 比例:**90%**(9/10 ✓;离群 2505.13909 差 11.25,交聚合裁决,不平均)
- 第一轮曾 88.9%(9 对)未过 → anchor_clarification_r1(not_reported 协议统一)→ 2509.00366 sol a4 定向重判(41.25 vs son55 43.75,差 2.5)→ 10 对重测通过。一轮修订即收敛。

## 已知限制(如实记录,不因冻结消除)

1. c2/p1/p2/c1 的两席初评材料为 v1 渲染(缺 listing);其中 6 篇已在 re1 用完整材料重评,2605.23939、2610.23303、2610.23307、2505.13909、2506.03095 未重评——它们的一致性与聚合基于 v1 材料 + Opus 补充核对(引文全部在新渲染中验证)。
2. 2505.13909(PC Agent-E)的 11.25 席间差是留出集唯一 >10 离对,聚合裁决为 67.5;分歧主因是 holdout/measurement 的保守度差,属可裁决范围。
3. 无真实审稿标签;期望全部来自有来源的 common_practice/single_source(35 条,hash 绑定)。
4. 一致性门槛是工程一致性指标,不证明科学正确性(spec 原文立场)。

## 冻结清单

| 资产 | 版本/hash 来源 |
|---|---|
| rubric | research/SCORE_SPEC.md(manifest assets.rubric.sha256) |
| 协议澄清 | calibration/anchor_clarification_r1.md |
| 原 15+31 卡 | reference/researchstudio-15-31/MANIFEST.tsv sha256 |
| 领域卡 | patterns/taxonomy.json + conditions.json sha256 |
| 期望 | .forge/domains/cua-agents/v1/profile/expectations.json sha256(35 条) |
| 材料 | materials.jsonl 逐篇 sha256(v1 渲染 / 修复渲染 / pdf / pdf_supplement / figs 状态显式) |

冻结后日常评审不改权重、锚点或卡片;新反证走 revision proposal + 受影响论文重评。
