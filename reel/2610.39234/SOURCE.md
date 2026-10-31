# SOURCE — 2610.39234 AgentHeal: Evaluating Goal-Preserving Resource Recovery of Web Agents under Access Barriers

- 论文：arXiv **2610.39234v1**（2026-10-29；2026-10-31 查 arXiv 仍只有 v1）
- 阅读材料：本地 `research/fulltext/2610.39234.txt`（文件头 v1，裁剪 core，§5.2 RQ4 末段截断）；按钉定版本补读了 arxiv.org/html/2610.39234v1 全文 §1–6 与 App. A–D（含 Tab.4 工具表、结局判定顺序）。代码与数据集在作者 GitHub，未下载。转换稿放在 /tmp/sel7，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-10.jsonl`（L2，supersedes inc-l1-11；P3 confirmed，q3 capability，F3/F2；卡 main/online_evaluation_methodology、main/agent_loop_context_control；子卡 K24）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-007.md` 第 1 节
- 画报源：`poster.html`；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome 经 Playwright 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 13 个模型，TS⁰ 平均 89.4% → 有障碍 TS 43.7% | 摘要；§5.2 RQ1；Tab.2 Average 行 |
| 副标题 | 障碍贯穿整个回合、重试无效；C / V / L 三类来源；嵌入互不相同的答案值 | §3.1 “Access Policy and Barriers”；§3.2；§4.2 式 (3) |
| 01 标题 | 225 个目标 × 3 = 675 例；161 个站点 | §4.2 |
| 01 三份环境 | x⁰ / x⁺ / x⁻ 的定义与各自唯一正确结局；合法来源平均 4.2 步；搜索首页是冒牌页 | §3.3 式 (1)(2)、定义 3.1；§4.2 “Task construction”“Recoverable…” |
| 01 x⁰ | 3–5 步 | §5.2 RQ3 |
| 01 注 | 访问政策在主实验中不告诉代理 | §3.1；§5.1 “Agent Frameworks” |
| 02 小标题 | ReAct、贪心解码（温度 0）、60 步预算 | §5.1 “Evaluation Details” |
| 02 散点 | 13 个模型沙盒 Recover. / Honest. / Violation. | Tab.2 沙盒列 |
| 02 r = 0.19 | 13 个模型 RR 与 HR 的 Pearson 相关 | **我们按 Tab.2 计算**（RR 与违规 r=0.26，RR 与审核准确 r=0.67，未上画报） |
| 同一家族放大 | Qwen3-8B / 3.5-9B / 3.8-27B 的恢复、如实停下、违规 | Tab.2；§5.2 RQ2 |
| 沙盒 vs 回放 | TS 43.7/63.4、恢复 35.2/70.1、如实停下 58.0/61.2、违规 11.0/17.7 | Tab.2 Average 行；§5.2 “Comparison…”（正文写沙盒违规 11.1%，表为 11.0，画报用表值） |
| 沙盒 vs 回放注 | 180 个真实障碍、121 个站点、每族 20 个；HTTP 回放、原生 robots.txt、模拟档案馆 | §4.3；App. A “Real-Web Barrier Collection” |
| 每个回合怎么判 | 政策 → 预算 → 弃权 → 来源归属四道检查；十种结局 | App. A “Outcomes and Failure Modes”；§4.4 |
| 判定图注 | 评审 GPT-6-Luna；10% 抽样与专家一致 >95% | §5.1 “Evaluation Details” |
| Tab.3 表 | DeepSeek-V4.1-Flash 三种设置 | Tab.3；§5.2 RQ4（剩余差距 26.2 点） |
| 步数 | 无障碍 3–5；可恢复 7–26；DeepSeek 不可恢复 >37；Haiku 与 GPT-6.1-Sol <10 | §5.2 RQ3 文字（Fig.3 数值未在正文给出） |
| 限制栏 | 工具清单与“文本与 DOM 网页导航”；快照环境；用户介入只评是否请求 | Tab.4；App. B |
| 本页怎么读 | MiniMax 42.7/19.1/28.7；Haiku 27.6/88.0/5.5；GPT-6.1-Sol 48.7/78.2/7.1 | Tab.2 |
| 我们的阅读 | 真实回放找回率高于沙盒的原因 | 作者解释见 §5.2 “Comparison…”；“不宜当作一般网页平均表现”是**我们的阅读** |

## 示意与重绘

- 01 三份环境示意图、“每个回合怎么判”流程：按 §3–4 与 App. A 文字自行绘制，标“示意”，非原文 Fig.2。
- 步数区间图：原文只给区间与个别模型，图中为区间示意，图注写明。
- 散点、斜率图、对比条、表格：作者 Tab.2–3 原值重绘。
