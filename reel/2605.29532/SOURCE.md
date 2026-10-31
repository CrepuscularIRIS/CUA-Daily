# SOURCE — 2605.29532 GUITestScape: Towards Open-set Evaluation on Exploratory GUI Testing

- 论文：arXiv **2605.29532v2**（v2 2026-10-29；v1 2026-05-28；2026-10-31 查 arXiv 最新为 v2）
- 阅读材料：本地 `research/fulltext/2605.29532.txt`（文件头 v2，裁剪 core，无附录）；按钉定版本补读了 arxiv.org/html/2605.29532v2 全文 §1–6、Limitations 与 App. A–D（Tab.4–9、人工参考集构建、证据移除对照、编码代理案例）。转换稿放在 /tmp/sel7，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-10.jsonl`（L2，supersedes inc-l1-11；P3 confirmed，q3 judgment，F2/F1；卡 main/online_evaluation_methodology、main/learned_outcome_and_process_judges；子卡 K16、C25、C24）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-007.md` 第 1 节
- 画报源：`poster.html`；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome 经 Playwright 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 编码代理 Reach 93.7% → Detect 51.4%；GUI 专用代理 Detect 4.2%（类别平均召回，Pass@1） | §5.3 “Capability Bottlenecks”（93.72 / 51.36；4.18）；Tab.8 |
| 副标题 | Reach / Trigger / Detect 定义；终态闭集评测的两点不足 | §1；§4.2 |
| 01 统计 | 508 缺陷、61 应用、82 场景、384 任务；显示 47% / 交互 53% | §3.3、Fig.3 |
| 01 树 | CR / EL / NLE / ONR / UTR 定义 | §3.1 |
| 01 注 | 测试依据（前置条件 / 交互或事件 / 可观察证据）来自开发者 issue 描述；多入口任务 | §3.2.2–3.2.3；App. A.1 |
| 02 条形 | GUIJudge 97.12/93.95；去检索 76.92/74.23；去分类型验证器 80.77/87.05；GUI-Tester 73.21/81.19；规则 69.64/80.41；Gemini-3.1 Flash 67.31/67.53；Claude-4.6-opus 60.26/64.14；GPT-5.4 53.85/61.88 | Tab.1 Detect 总体列 |
| 02 注 | 标注者 κ 0.9545/0.9391/0.9010；不看 GUIJudge 输出；证据移除后正向 Detect 为 0；跨骨干 κ 0.822–0.911 | App. C.1 Tab.6；App. A.2；App. B.3 Tab.5 |
| 02 src | 参考集约 202 条 | **我们的推算**：98.51%=199/202、97.03%=196/202、95.05%=192/202；正文未写规模 |
| GUIJudge 流程 | 检索器 → 显示 / 交互验证器 → 与报告比对 → 三个判定 | §4.3；App. B.1 Algorithm 1 |
| 03 阶梯 | 三类平均召回 Reach / Trigger / Detect | §5.3；Tab.8（我们按 Tab.8 逐模型复算一致） |
| 03 注 | Detect/Trigger 59.9%、48.3%、10.4%；把真实缺陷当自身失误 | §5.3 |
| 03 注 | Pass@1→Pass@3 Detect F1 +16.68 / +12.18 / +6.56；GUI-Owl-1.5-32B Trigger +15.67、Detect +0.62 | §5.3 “Multi-Trial Gains”；Tab.8–9 |
| 04 热力图 | 13 系统 × 5 故障 Detect F1 及总体 | Tab.2 |
| 04 注 | 13 个中 11 个 CR > EL；13 个全部 NLE > UTR | §5.3 “Fault-Specific Detection Challenges” |
| 05 哑铃 | UI-TARS 7.48→57.02 / 11.66→69.07；Gemini-3.1-Pro 36.42→61.27 / 46.19→71.07；Seed-1.8 40.55→70.97 / 51.05→79.48 | Tab.3（增益值）与 Tab.2（基线值）；§5.4 |
| 05 图注 | 接入后为人工评估 | §5.1 “RQ3”；§5.4 |
| 06 | 编码代理 Detect F1 增益 +9.04 至 +16.64；Reach +0.59–4.94、Trigger +1.17–6.60（画报合写 0.59–6.60）；三个案例；Claude vs DeepSeek 14.27 / 14.87 | §5.3 “Coding-Agent Gains”；App. C.5 Fig.6 |
| 限制栏 | 只有 Android；测试依据部分人工；默认骨干在同一参考集上按表现选出 | Limitations (1)(3)；App. B.3 |
| 限制栏 | RQ3 基线与接入后口径不一 | Tab.3 注“absolute gains over the corresponding unassisted baseline”与 Tab.2 数值相同，接入后为人工评估（**我们的核对**） |
| 我们的阅读 | GUI 专用代理 Reach 25.6–70.1% | Tab.8 Reach 列（GUI-Owl-1.5-8B 25.64 至 MAI-UI-8B 70.08） |
| 关系栏 | 编码代理案例 1（加载中画面误报为显示缺陷） | App. C.5 Case 1；与 2610.39282 的联系是**我们的阅读** |

## 示意与重绘

- 01 缺陷树、GUIJudge 流程、03 阶梯：按原文文字与表格重绘，标“重绘 / 示意”。
- 02、04、05：作者表格原值重绘。原文 Fig.2、Fig.4–6 未搬运。
