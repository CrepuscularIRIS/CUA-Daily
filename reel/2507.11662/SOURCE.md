# SOURCE — 2507.11662 Let's Think in Two Steps: Mitigating Agreement Bias in MLLMs with Self-Grounded Verification

- 论文：arXiv **2507.11662v3**（v1 2025-07-15、v2 2025-12-23、v3 2026-03-08；2026-11-06 查 export.arxiv.org/abs，最新为 v3，与本地缓存版本一致）。作者 Moises Andrade, Joonhyuk Cha, Brandon Ho, Vriksha Srihari, Karmesh Yadav, Zsolt Kira
- 阅读材料：本地 `research/fulltext/2507.11662.txt`（文件头 v3，裁剪 core）；按钉定版本补读 arxiv.org/html/2507.11662v3 全文 §1–6 与附录 A–F（表 1–24；附录 B 提示词只读结构说明；附录 C、G 定性例子只读说明文字，图 3 转移图读正文与 D.3 文字）。转换稿在 /tmp/sel11，不提交。没有运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-27.jsonl`（L2，supersedes inc-l1-33#2507.11662；P3 confirmed，q1 measured_own，q2 challenges_barrier，q3 judgment，q4 fits；F2/F5；卡 main/learned_outcome_and_process_judges；子卡 C25、K16）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-011.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 侧栏标题与导语 | 约一半失败轨迹判成功；agreement bias；思考/投票压不下；先写先验再看轨迹 | 摘要；§1 贡献 1；§3.2；§4 “Agreement Bias”“Effectiveness of SGV” |
| 侧栏大数字 | Gemini 2.5 Flash TNR 55 → 76、TPR 94 → 88（VWA + OSWorld 合并） | §4 表 1 |
| 侧栏大数字 | 14 个模型 TNR 上升 8–25 点 | 表 1 逐行差值（我们复算：最小 GPT-5-Nano 65→73 = +8，最大 GPT-4.1 Mini 40→65 = +25） |
| 侧栏分布条 | 判分器 57/43；无 SGV 二分类 73/25/U2；无 SGV 三档 70/6/23/U1；SGV 56/4/39/U1 | §4 表 3(A) |
| 侧栏注 | 表 3A 判分器 57% 与 VWA 47% 不一致 | 表 3(A) 首行 vs §4 首段（“success rates of 47% and 22%”） |
| 实验怎么搭 | VWA 用 Gemini 2.5 Flash ReAct（47%），OSWorld 用 UI-TARS-1.5（22%） | §3.3 “Agents and Trajectory Quality”；§4 首段 |
| 实验怎么搭 | 判分器修订；AgentRewardBench 人工标注 Acc 85.1 → 98 | §3.3 “Trajectory Annotations”；附录 E.1 表 9；F.2 |
| 实验怎么搭 | 三档 Likert，部分成功记 0 | §3.3 “Baselines and Ablations” |
| 限制 | TPR 除 o1 外下降 1–6 点；宽松判分器 | 表 1 逐行（我们复算）；§4 “Leniency-Strictness Trade-offs” |
| 限制 | token 1× / 1.5× / 2.2× | §5 表 4 |
| 限制 | 8 次投票、思考作加算力对照 | 表 2 第 5、7、8 行；附录 A.1（8 completions, T=1.5） |
| 限制 | 3 次运行均值；“超过最好 20 点”跨实现 | 表 4 注；§5 “Online Supervision” |
| 限制 | 未消除；剩余错误来自视觉感知 | §6 |
| 我们的阅读 | 召回 90%+ 与榜单第一 | §4 “Fine-Grained Metrics”；§5 “Discussion”；附录 E.1 表 10。分开报 TPR/TNR 是我们的归纳 |
| 我们的阅读 | 先验由更弱模型写、写时不思考效果相近 | 附录 E.8 表 20 第 (3)、(6) 列 |
| 同卡已入 Reel | 2404.06474、2610.34384、2611.04073 | `reel/README.md` 各期条目 |
| 原文小出入 | “72%” vs 表 3A 73；正文引“表 3 第 3–6 行”实为表 2 | §4 “Agreement Bias” 段与表 2、表 3 |
| 原文小出入 | robomimic 不引用 | §5 表 5 |
| 01 示意 | 一次调用 vs 两次调用；手机壳例 | §3.2 两个公式；图 1 说明文字；§1 第 2 段例子。**示意重画，非原图**；先验三条为我们按原文图 7、图 9 的描述概括 |
| 01 条 | 47 / 49 / 67 / 71 | 附录 E.7 表 18（TNR 列） |
| 01 注 | 弱模型先验 69、加噪 68、只给网页搜索 44 | 附录 E.8 表 20（TNR 行：G-Lite 69，G + Noise 68，G + Web 无先验 44） |
| 02 哑铃 | 14 模型 TNR 与 TPR（无 SGV → SGV） | §4 表 1 |
| 02 注 | 跨家族、验证器更弱时更重 | §4 “Cross-Model Variations”；附录 E.6 |
| 03 左 | 不写推理 44/60、CoT 47/63、二分类 36/61、投票 48/62、细则 53/–、思考 55/73、思考+投票 55/71、SGV 71/81、SGV+思考 70/86 | §4 表 2（TNR 列，VWA / OSWorld）。表 2 第 4 行“CoT 无 SoM”未画 |
| 03 左注 | 三档 Likert 较好 | 附录 E.2 第 (4) 点 |
| 03 右 | 失败轨迹上 48/55/70（VWA）、56/65/77（OSW）；7,280 / 2,784 次采样 | §4 表 3(B) “F” 列 |
| 03 右注 | 74% 落在最高档；Platt 后 74% 落在 [0.5,0.6)；TNR 37→40，SGV 64 | 附录 E.3.1 表 11、表 12 |
| 04 左 | VWA 45.0 / 46.1 / 54.0；OSWorld 21.7 / 24.3 / 26.5（每 5 步） | 附录 E.4 表 14（VWA 取“Outcome-based”行，与表 4 的 45/46/54 一致；OSWorld 取“Every 5 Steps”，与表 4 的 22/24/27 一致） |
| 04 左 | token 1× / 1.5× / 2.2×；VWA 910 题 | 表 4；§3.3 |
| 04 右 | 30%；10%；7.4% → 6.6% / 0.8% | §5 “Online Supervision” 第二段（Fig. 3 量化） |
| 04 注 | 判分器反馈 +21、SGV 最多 +10.4 | §5 “Self-Improvement”；图 2 说明 |
| 04 注 | Gemini 2.0 Flash：36 / 36 / 40 | 附录 E.9 表 21 |
| 05 左 | 47→71、63→79、63→77、28→42、42→61；代理成功率 47/33/31；TPR 93 vs 90 | 附录 E.6 表 17 |
| 05 右 | 步数 1–10 / 11–20 / 21–30 / >30：TNR 41→61、49→70、63→80、89→94；成功率 54/20/16/2；三模型平均 | 附录 E.5 表 16 与正文 |
| 05 右注 | 长轨迹多已跑偏 | 附录 E.5 第 3 段 |

## 原文内部出入与口径

- 表 3(A) 首行判分器“成功 57%”，而 §4 首段称 VWA 轨迹成功率 47%、OSWorld 22%；原文未说明表 3(A) 用的轨迹子集。画报侧栏照表画并加注。
- §4 正文写二分类模板“72% SR vs 57% expected”，表 3(A) 为 73。正文两处引“Tab. 3 rows 3–6 / row 5”，指的是表 2 的行。均不影响结论。
- 表 4 的 VWA 基线 45 与附录 F 表 22 的 ReAct Gemini 2.5 全集 47 不同，属不同批次运行；画报统一用表 14 / 表 4 一组。
- 下游比较中 SGV 验证器 token 为 2.2×、常规验证器 1.5×，不是等算力对照；离线部分的“思考（最大预算）”和“8 次投票”是加算力对照，但下游没有同等 token 的常规验证器对照。画报限制栏写明。

## 示意与自绘

- 01 两条流程为按原文 §3.2 公式与图 1 文字重画的示意，不是原图；先验三条是概括。
- 其余条形、哑铃、矩阵由我们按原文表格数值绘制。
