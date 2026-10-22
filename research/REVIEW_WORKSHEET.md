# 逐篇阅读与评分工作表 v2.2

状态：待校准模板，不含真实论文评分。事实提取与评价分开保存，按 SCORE_SPEC 使用。
只填实际读到的内容；不能为了字段完整补写事实。每个事实/判断均绑定 evidence ID。

## 0. 身份与材料

paper ID/title/version；claim_type；作者中心主张（保留原意）；reviewer/model/session/time。
材料 manifest：版本化 URL、文件 SHA-256、实际读过的节/页/表/附录、缺失部分。
rubric、卡片和 expectations 的版本/hash；输入包/输出包 hash；supersedes（若为重评）。

## 1. Operation signature：究竟改了什么

每个独立操作一条（通常 1–3 条）：

- sig_id / object：改动哪个具体对象，基线是什么。
- information：可见输入、反馈及明确不可见信息；是否有特权、标签、未来帧或测试数据。
- operation → output：可以复述成操作的变化，不抄摘要口号。
- feedback → proposal → selection：信号从何而来、候选如何产生、用什么规则接受/拒绝，使用哪份数据和预算。
- persistence：改动保存在哪里、有效期/版本、何时被后续任务读取，什么时候撤回或淘汰。
- claimed_effect：作者声称什么指标改变，条件是什么；引用原文位置。
- evidence / failure_boundary：支持与反证，未报告和材料缺失分开。

对静态 harness、组件或 benchmark，selection/persistence 可明确 `not_applicable` 并解释；不能因此虚构自我改进闭环。

## 2. Gap identify：它回应的是什么残余问题

- 作者 gap 与我们核对的 gap 分开。
- method_lineage：祖先方法 → 最近邻/frontier → 本文改变；固定最近邻版本与当时可得性。
- closest_adjacent：同类机制（包括别名/其他领域）已解决什么，仍没解决什么。
- bottleneck / residue / stakes：具体在哪个条件失败、可观察代价是什么；“缺少我们的模块”不算问题定义。
- 本文填上多少、仍剩什么、支持/不支持哪一段；证据不足写 unresolved。
- 本文之后的新论文放 current_relevance，不倒过来否定发表时的问题位置；gap 核查不自动等于全面 novelty 检索。

## 3. 模式执行和审稿期望

先按 PATTERN_PROTOCOL 完成原15+31层：primary/supporting/子卡（核父类）、tactic/步骤执行、无匹配理由；再记录领域 namespace 与映射。
选择 0–3 张最相关领域卡（或 unassigned）：稳定 ID/版本、匹配的操作/信息/条件、真正执行了什么。
每条适用 success condition / failure mode 记录 met / partial / unmet / unknown / challenged_with_evidence，并附引用。
“看起来属于该模式”与“执行充分并带来效果”分别回答。没有观察到 failure 不记为避免失败。
列具体 reviewer expectations：ID、来源/强度、applies_when、本篇是否适用、证据、回答、映射的 G/M/X/E 项。

## 4. 主张—证据矩阵

| claim ID / 原主张 | 对照与设置 | 选择集/测试集 | 结果与分母 | 支持证据 ID | 反证/替代解释 | 允许结论 |
|---|---|---|---|---|---|---|
| 待填 | 固定模型/预算/接口 | 是否用于开发/选择 | 不仅最优值，也含失败 | 版本/节/表/原文 | 缺项如实记录 | 不扩大范围 |

留存收益需区分 task improvement、retained improvement、improver improvement；GUI/具身按各自 evidence_level。
`claim_support`：supported / scoped / unsupported / contradicted / unresolved；写出最高可支持结论与仍不能说的话。
数据类型：author_report / reviewer_comment / our_inference / static_code_check / our_run；后者没有实际运行就不得使用。

## 5. 评分与独立审阅

逐项保存 status、0–4 rating、evidence IDs、reason、counterevidence、not_reported 的查找范围。
按冻结权重计算 G/M/X/E、总分或 L/U/coverage。未知项不能补零生成总分。
审阅者先看固定材料与规则独立判断，再比首轮结果；记录争议与解决依据，不平均凑分。
最终 audit status：pending / passed / needs_revision；审核记录绑定 judgment hash，后改任何字段则审核失效。

## 6. 下游路由

选题前只进入内部评分记录，不生成海报、不上全量画报墙。
阈值/去重/数量决策写独立 selection snapshot，理由不得倒灌改变原始分数。
若 Reel 核查发现新反证，撤回该条 selection，回本工作表修订，再审核和重新选题。
