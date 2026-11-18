# GapLeak (2611.22223) — SOURCE

论文：*GapLeak: When Privacy-Preserving LLM-based Web Agents Become a Privacy Risk*，arXiv 2611.22223v1，2026-11-17。
缓存全文：`research/fulltext/2611.22223.txt`（FULLTEXT: html）。核对于 2026-11-18（本仓 selection-018，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| "约束授权范围，不约束可达范围" | "constrain the agent's authorized scope … do not constrain the agent's reachable scope" | §1 |
| 威胁模型：只控字段集/引导文本/验证反馈，无注入 | Adversary Capabilities 三项；"nor does it inject hidden elements, scripts, or instructions" | §3.1 |
| L∩H=∅、g∉L 且 g∈H | 信息缺口形式化 | §3.1 Adversary Objectives |
| 三阶段（升级/累积/引导放大） | Stage 1–3 | §3.2（Figure 1） |
| 引导文本把建议当要求（sycophancy） | "interpret the website's guidance as a task requirement rather than a mere suggestion" | §3.2 Stage 3 |
| OD 36.2% / TPD 38.6% ≈ 37% | "the average OD is 36.2% and the average TPD is 38.6%, yielding an overall unauthorized disclosure of approximately 37%" | §5.5 |
| DoBrowser 差旅 TPD 96.3% | "TPD follows the same ordering and reaches 96.3% on travel booking" | §5.5 Framework comparison |
| DoBrowser 单步架构无中间规划层 | "processes each turn in a single step without a separate planning stage" | §5.5（引 §4.4） |
| PCS 12 组合中 6 个为零 | "PCS drops to zero in six of the twelve combinations" | §5.5 |
| 三框架 BrowserUse/DoBrowser/Agent-E ×六模型 | RQ4 设置 | §5 开头，§5.5 |
| 医疗·软边界 OD 48.2→6.1 | "Soft Boundary reduces average OD from 48.2% to 6.1% and TPD from 50.2% to 4.2%" | §5.4 Medical intake |
| 医疗·访问限制披露清零、TS 41.7→~30% | "Access Restriction eliminates disclosure entirely, though TS decreases from 41.7% to around 30%" | §5.4 Medical intake |
| 差旅·两防御 OD 34.9→10.5/8.8、TS 50→31.7% | "average OD from 34.9% to 10.5% and 8.8%, but TS also declines from 50% to 31.7%"；占位符 "N/A" 过不了验证 | §5.4 Travel booking |
| 电商·访问限制 PCS 21.7→56.7% | "raising PCS from 21.7% to 56.7%" | §5.4 E-commerce return |
| 求职·两防御几乎无效 | "Instruction-level defenses have minimal effect here" | §5.4 Job application |
| 挡提交不挡升级 | "they act on the wrong stage: agents still escalate … the defenses block only its submission, not the escalation" | §5.4 Key finding of RQ3 |
| STV 消除 >96% 未授权披露且保任务成功 | "eliminating over 96% of unauthorized disclosures while preserving task success" | Abstract；§5.6（RQ5） |
| STV 不改升级本身 | "it does not alter the source escalation itself" | §7 |
| 反例一：三模型编造邮箱、TS 归零 | "All three affected models … submit a guessed email address in every run … TS of 0% for all three" | §5.3（Fabrication instead of escalation） |
| 缺字段格式可预测性决定升级 vs 编造 | "the choice between fabrication and escalation appears to depend on the missing field type" | §5.3 Key finding of RQ2 |
| 反例二：差旅 Summary Complete 后 SSE 反升 | "Anomaly in the travel booking scenario … removing the gap instead lets the guidance take full effect" | §5.3 |
| 缺口与引导独立驱动披露 | "the information gap and the manipulated guidance can each drive disclosure independently" | §5.3 总结句 |
| benign-complete TS=PCS=83.3%，失败全为执行错误 | "agents achieve an average TS and PCS of 83.3%, with all failures due to execution errors" | §7 Benign-complete Baseline |
| 人工审批时机论证未实测 | "Human Oversight … its effect is limited by timing"（论证性段落，无实验） | §7 |
| 补全材料是最佳实践不是防御 | "complete materials are a best practice, not a defense" | §7 |
| 四场景 求职/电商/差旅/医疗 | Scenario Model | §3.3 |

## 编辑收窄

- "≈37%" 严格按 §5.5 的 36.2/38.6 平均口径；96.3% 标注最差组合（DoBrowser·差旅·TPD），不冒充 OD。
- 防御矩阵表中每行均标场景：软边界/访问限制在不同场景效果相反（医疗大降 vs 差旅掉成功），不做成"防御有效/无效"的单值结论。
- STV 单独成卡并保留 §7 自认的边界（不改升级），不呈现为完整解。
- 人工审批只作为 §7 论证提及，画报不将其列为已测防御。
