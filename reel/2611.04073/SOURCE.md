# SOURCE — 2611.04073 Computer-Use Agents Gain Little Benefit from a World Model When Conditioned on Tutorials

- 论文：arXiv **2611.04073v1**（2026-11-02；2026-11-04 查 export.arxiv.org/abs 只有 v1）
- 阅读材料：本地 `research/fulltext/2611.04073.txt`（文件头 v1，裁剪 core）；按钉定版本补读 arxiv.org/html/2611.04073v1 全文 §1–8 与 App. A–U（表 1–14 全部读过；App. L–N、O.3–O.5、P、T 的提示词只看结构）。转换稿在 /tmp/sel9，不提交。没有下载或运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-17.jsonl`（L2，supersedes inc-l1-22#2611.04073；P3 confirmed，q2 challenges_barrier，q3 judgment，F1/F2；卡 main/simulated_lookahead_selection、main/learned_outcome_and_process_judges；子卡 K01、K02、K16）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-009.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 给了教程，真实未来几乎不加分；瓶颈在判官读不懂“做完没有” | 摘要；§6.3 Finding 3、Finding 4 |
| 副标题 | policy 出 3 个候选 → judge 选 1 → grounder；全部 Qwen 零样本 | §4.1–4.2；§5 “Baselines”（K=3）、“Base MLLMs”；§7 第三条 |
| 副标题 | 无教程 43.8 → 48.0（+4.2） | 表 2 第 1、7 行（15 步） |
| 副标题 | 有教程 51.7 → 51.6 | 表 6 第 3、5 行（15 步，360 题，Qwen3-VL-32B） |
| 副标题 | 以往“教程＋世界模型”的收益主要来自教程和判官 | 摘要；§6.2 末句 |
| 具体问题 | R-WoM 只与无教程基线比、未与“有教程判官不看未来”比 | §1；§2 “Most similar…”；App. D |
| 关键研究动作 | 360 + 169 题；固定 policy/judge/grounder、harness、动作空间 | §3 “Dataset statistics”；§5 “Baselines” |
| 关键研究动作 | 每个候选在恢复到同一检查点的 VM 副本里执行 1–3 步 | §5 GT-rollout；App. F、F.1、Q |
| 机制图 | 教程：110 题人工验证，其余 419 题（250 OSWorld + 169 ScienceBoard）由 Gemini 3.8 Flash 联网生成 | §3 “Generating tutorials”、“Dataset statistics” |
| 机制图 | 当前截图 + 近 5 步截图 + 全部动作（+ 近 5 步思考） | §4.2 “Policy and Grounding Models”；App. K |
| 机制图 | Grounder UI-Venus-1.5，只看当前截图与选中动作 | §4.2 |
| 机制图 | 文本预测：同一 Qwen 写下一屏描述，R-WoM/WebDreamer，H=1–3 | §5 “Baselines”；App. O、P |
| 机制图 | 与主 VM 不一致 0.97%（2,298 / 237,709 完成任务状态） | App. F |
| 机制图 | 只执行被选中分支的第一步；分支 VM 不替换真实状态 | App. F（图 10 说明） |
| 机制图下注 | 动作空间 Agent-S2；Policy Only 只出 1 个候选、无判官 | §4.2；§5 “Baselines” |
| 右栏“上界” | 真实截图是下一屏保真度上界 | §1；§5 脚注 7；App. F |
| 右栏“复现基线” | 无教程 R-WoM H=2：43.8→44.9；50 步 47.4→49.4 | 表 2 第 1、5 行；§5 脚注 6 |
| 右栏“ViMo 空格” | 本仓 reel/2504.13936 画报“没有出候选＋打分但不预测屏幕的对照” | 本仓画报；**判断为我们的** |
| 结果点图·不给教程 | 15 步：判官 43.8、文本最好 44.9（R-WoM H=2）、真实最好 48.0（H=2）、真实 H=1 44.7 | 表 2 |
| 结果点图·不给教程 | 50 步：47.4、49.4（R-WoM H=2）、50.6（H=2）、H=1 46.8 | 表 2 |
| 结果点图·给教程 | 15 步：RAG-PJ 51.7；真实 H=1/2/3 = 49.4/51.6/50.5 | 表 6 |
| 结果点图·给教程 | 50 步：57.4；真实 57.5/57.7/58.0 | 表 6 |
| 结果点图·给教程 | 文本最好：15 步 50.1（H=2）、50 步 54.0（H=1） | **我们按表 4（110 题）与表 5（250 题）第 8–10 行加权**；同法得 RAG-PJ 51.7、57.4，与表 6 一致 |
| 结果说明 | 有教程时真实未来与 RAG-PJ 不显著；文本预测更差或相近 | §6.2 Finding 2；§6.3 Finding 3；表 4–5 阴影说明；App. A “Statistical tests”、App. B “Significance tests” |
| 收益阶梯·OSWorld | 42.5 → 47.8 → 51.7 → 51.6 | 表 6 第 1、2、3、5 行（15 步） |
| 收益阶梯·SB 32B | 14.8 → 36.1 → 40.2 → 42.4（H=3）；p=0.32 | 表 1 / 表 7 第 1、2、4、13 行；App. B 显著性（hierarchical bootstrap） |
| 收益阶梯·SB 27B | 29.0 → 44.2 → 48.3 → 49.9（H=3）；任务级 p≈0.11–0.14 | 表 1 / 表 8；App. B（sign-flip 0.11、Wilcoxon 0.14） |
| 阅读判断 | 27B 上 H=1/2/3 名义 +0.8/+1.0/+1.6；Welch p=0.013/0.001/0.052，作者不采用 | 表 1 第 4、11–13 行；App. B “Significance tests”；**差值与“不显著≠等价”为我们的** |
| Celestia 例 | 三选一、漏了取得键盘焦点、5 步预算、G/双击/右键三种结果、真实前瞻 4 步完成 | App. B “Why do GT rollouts help in Celestia and GrassGIS?”；图 4–5 |
| Celestia 说明 | 40 个例子；教程不全、步数紧、效果可见时有用；VS Code、GIMP 不灵 | §6.3 Finding 3；App. A “Per-task-category analysis” |
| 瓶颈栏 | 最常见：不理解任务成功；第二：不能就未来推理进度、重复失败动作；VS Code Explorer 例 | §6.3 Finding 4；App. A；App. R |
| 瓶颈栏来源 | 2,116 条失败轨迹；人工 30 题定 9 类；Gemini 3.8 Flash 标主/次因；主因一致率 90%；另抽 20 条 | 图 3 说明；App. R |
| 瓶颈栏阅读判断 | 各类占比只在图 3 图像中，HTML 未给数值 | v1 HTML 图 3 无数值文本；**判断为我们的** |
| 限制 1 | 一个模型家族、零样本判官 | §5 “Base MLLMs”；§7 第三条 |
| 限制 2 | 生成教程读任务指令与初始截图；图 9 生成器搜过任务文件 ID 与 OSWorld 仓库；人工教程 110 题上 72.6 vs 72.3 | §3 “Generating tutorials”；App. E 图 9 说明；表 4 第 4、12 行（15 步，32B） |
| 限制 3 | 仅在有教程时成立；无教程 +3~4；未测本地检索 | §6.3；§7 第一条 |
| 限制 4 | 未统计候选覆盖率 | 全文无此统计（与 L2 K01 第二问一致） |
| 限制 5 | 真实前瞻每步 K 台 VM × H 步；只报总算力 272 GPU 时 + 约 1,080 小时 DGX Spark | §4.1 末；App. F.1 “Resource accounting”；§8 |
| 限制 6 | v1 HTML 缺 OSWorld 主表；正文把 ScienceBoard 表称“表 9” | v1 HTML：§6.1–6.3 的 “Table ” 引用为空，表 1 标题为 ScienceBoard，表 9 实为 App. E 的教程评审表 |

## 原文内部出入

- v1 HTML 中 OSWorld-Tutorial 主表（正文所称 “Table ”，含第 3a/3b 行“Policy + RAG Judge”）不存在；正文与 App. B 把 ScienceBoard 结果称作“Table 9”，实际是表 1（表 9 是 App. E 的 20 对教程评审）。画报只引用实际存在的表 1–8，并用表 4/5 加权重建 360 题的文本预测行（与表 6 的 RAG-PJ 数值逐一吻合）。
- 图 1、图 3、图 6 在 v1 HTML 中没有图像或数值，画报没有使用其中任何数值。

## 示意与自绘

- 机制图、Celestia 三分支图为我们按 §4–5、App. F 与 App. B 图 4–5 重画的示意，不是原文图 2 / 图 4–5。
- 结果点图与收益阶梯由我们按表 1、2、4–8 的数值绘制；原文图 1、图 6 未使用。
