# SOURCE — 2610.30792 Trace2World: Reconstructing App Worlds from Real Interaction Traces for Scalable GUI Agent Training

- 论文：arXiv **2610.30792v1**（2026-10-22）
- 阅读材料：本地 `research/fulltext/2610.30792.txt`（文件头 v1，正文有显式省略、无附录）；已补读 arxiv.org/html/2610.30792v1 全文（正文 + 附录 A–F），转换稿存于 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-02.jsonl`（L2，P3 confirmed，q3 judgment，F2/F3；卡 main/calibrate_simulator_to_real，子卡 K10）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-004.md` 第 1 节
- run：gui-rolling-20261023-01；规则 problem-core-v1.1

## 数字与断言映射

| 画报内容 | 原文位置 |
|---|---|
| 1,570 条轨迹、50 个 app、10 个领域；40 个训练 app / 10 个未见 app | 摘要；§4 首段；App. D.3 Table D4 |
| 中文移动 app 重建为 DOM 浏览器环境 | App. D.3 Table D4（应用名单）；App. E.5 |
| 两道边界：语义承诺先于编码、源证据验收在编码后；app model 冻结，修复只改 package | §1；§3.1–§3.3；Fig. 3 |
| 冲突无法由观察到的状态解释时保持不可执行；未支持控件可见但无效 | §3.2；§3.3 |
| 有界 API 调用编译，无开放式编码代理；状态内核 | §3.3 |
| 只读 checker 看不到 app model、生成的 verifier、修复日志 | §3.3 |
| 修复 ≤3 轮；须改 model 才能过的工作流排除 | §3.3；§4.1 |
| 74.6% 首次通过源回放；1,570 个工作流全部在 3 轮内关闭，无人工 QA | §4.1；App. E.2.3 |
| 1,280 种子 + 768 引导任务，40 个训练 app | §1 贡献 3；§3.4；App. D.3 |
| 美团“关闭免密支付”：源 app 先弹确认、重建版一下保存、终值检查通过 | §1 ¶4；Fig. 2 |
| 6 项检查（可达、界面、状态、效果、终态、数据）；盲评 GPT-5.6 Sol | §4.1 Setup；App. E.1.1 |
| 人工复标 1,200 包，workflow 标签 macro-F1 / 一致 90.2%；人工标注下各条件高 1.4–3.8 点，排序不变 | §4.1；App. E.1.4 Table E3 |
| Table 1 全部 8 行的“全六项”与“Reach”数值 | §4.1 Table 1 = App. E.1.3 Table E2 |
| 终值过而 Effect 败：PhoneWorld 式 14.3、CUA-Gym+ 10.9、Direct+ 15.6、GUI-GENESIS 式 13.2、Trace2World 4.5 | App. E.1.3 末段 |
| 基线在同一底座/工具/运行时/录屏上重实现；PhoneWorld 公开仓库无构建代理编排与提示词 | §4.1 Setup；App. E.1.2 |
| 自验证对照只改验收证据 | §4.2 Setup；App. E.1.2 “Validation-evidence control” |
| 构建 GPT-5.2，修复/验证 GPT-5.5，对比构建器各角色 GPT-5.5 | §4.1 末段；App. E.1.3 |
| 真机面板：100 个配对任务、20 个训练 app；50 实体替换 + 50 留出工作流（与 benchmark 重叠） | §4.2 Setup；App. D.3 Table D5；App. E.4.1 |
| 真机/模拟增益 9.7±2.1 / 17.7±1.5（自验证），15.7±1.5 / 16.7±2.1（源验证），16.3±2.1 / 18.7±1.5（最终）；保留 54.7 / 94.0 / 87.5%；仅模拟通过 18.3 / 10.0 / 10.7% | §4.4 Table 3 |
| 同 1,280 种子、同 32 轮、只换环境 | App. E.4.1 “Matched training-source conditions” |
| 6.0 pp（seed SD 1.0）= −1.0 + 8.3 − 1.3 | §4.2；App. E.4.2 |
| 外部 benchmark：MobileGym +16.2、AndroidWorld +5.4、MobileWorld +8.9、AndroidDaily +11.1 | §4.4；Table 2 |
| 学习者引导 61.1 vs 静态 56.9 vs 实体替换 55.3 vs 种子续训 52.2（iteration 52） | §4.3；Fig. 6 |
| 未见 app 176 题 +13.6 pp；训练 app 任务 +21.6 pp | §4.4；App. E.3.4 |
| 每 app 约 3.6 小时、1,160 次调用 | §4.1；App. E.2.4 |
| 200 个保真评测工作流为 construction-exposed | App. D.3 Table D5 及 “How evaluation tasks are separated” |
| 限制：浏览器重实现、单一采集时点、刷新成本未报、真机只在训练 app | App. E.5 |

## 自绘与示意

- 机制图（五个节点、两道边界、修复回路、自验证虚框）按 Fig. 3 与 §3 文字重绘，不是原文图。
- “关闭免密支付”四个手机框按 Fig. 2 描述重绘，界面元素为示意。
- 哑铃图与柱图由 Table 1、Table 3 数值绘制；坐标按数值线性映射。
