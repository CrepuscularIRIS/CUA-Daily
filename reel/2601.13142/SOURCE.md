# SOURCE — 2601.13142 TVWorld: Foundations for Remote-Control TV Agents

- 论文：arXiv **2601.13142v1**（2026-01-19；2026-11-07 查 export.arxiv.org/abs，最新仍为 v1，与本地缓存版本一致）
- 阅读材料：本地 `research/fulltext/2601.13142.txt`（文件头 v1，裁剪 core，缺 §3 与附录）；按钉定版本补读 arxiv.org/html/2601.13142v1 全文 §1–5、Limitations 与附录 A–L（表 1–10；图 4、5 为位图，只读说明；图 6–10 案例与训练样例只读说明）。转换稿在 /tmp/sel12，不提交。没有运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-31.jsonl`（L2，supersedes inc-l1-46#2601.13142；P3 confirmed，q1 measured_own，q2 new_bottleneck，q3 capability，q4 fits；F3/F0；卡 main/planner_grounder_interface、main/online_evaluation_methodology；子卡 K29、K30、C22）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-012.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 / 01 | 电视界面以焦点为中心，方向键移动高亮，动作只作用于焦点；需要焦点感知与拓扑感知 | 摘要；§1 第 2–3 段；图 1 |
| 页眉遥控器 | 9 个动作：UP/DOWN/LEFT/RIGHT/EXIT/OK/HOME/SETTING/FINISH | §2.1 “Action Set”；附录 B 表 6 |
| 副标题 | UI-TARS-1.5-7B 1.6%、GUI-Owl-7B 5.4% | 表 3 Overall 列 |
| 副标题 / 03 | Qwen3-VL-8B 20.0 → TVTheseus 68.3（3 次运行均值，范围 65.6–71.4）；Gemini 3 Flash 66.4 | 表 3（TVTheseus 上下标 +3.1/−2.7）；附录 I 表 10。三次 Overall 68.0/65.6/71.4 为我们按表 10 文字与截图两列平均复算 |
| 01 示意 | 点击一步到达 vs 方向键多步；停滞（无效键原地）与绕路两种失败 | §2.1；§3.1 “Detour Reflection / Stagnation Escape Traces”；附录 J。**示意重画，非原图** |
| 02 左图 | 三类轨迹：最短路引导、绕路反思（走远一步再回）、停滞逃逸（插入无效键）；理由由 Gemini 3 Pro Preview 合成 | §3.1；附录 K。节点上的命中时间数字为**示意**，非原文 |
| 02 右表 | 奖励 1 / 0.2 / 0；绕路轨迹走远且非原岔路 0.1、原岔路 0；停滞轨迹重复无效键 0、走远 0.1 | 附录 E 式 (3)–(5) |
| 02 右注 | 0.95·拓扑 + 0.05·格式；GRPO rollout 8；只执行一步打分；命中时间定义 | §3.2.2；附录 C “Stage II”；附录 F.2；附录 G |
| 02 信息边界 | 图距离只在训练图上算奖励；测试输入为当前截图、≤4 张历史截图、全部动作历史与指令 | §3.2.1；§4.1 “Training Settings”“Evaluation”。“测试不给图”为我们依据 §4.1 输入定义的阅读判断 |
| 对照条件 | TCL Config 282/1,508；SFT 500 条 → 8,490 例、5 epoch；RL 1,000 条 → 17,825 例、600 步、约 280 GPU·h；测试 5 张 Google TV 图 169/62/24/33/32 节点；每图 50 对 × 2 种目标 = 500；50 步、1024×576、SR = 在目标页 FINISH | 表 1；附录 C；§2.3 “Task Construction”；§4.1 |
| 03 左条形 | 10 个模型 Overall：1.6/5.0/5.4/15.4/20.0/39.0/25.4/60.2/66.4/68.3；竖线为文字 / 截图各自五场景均值 | 表 3。文字 / 截图均值为我们逐格复算（如 Claude Haiku 4.5 = 38.0 / 12.8；TVTheseus 67.3 / 69.3 取表 10 Avg.） |
| 03 左注 | 正文提到“Gemini 3 Pro”，表 3 无此行 | §4.2 第 2 段 vs 表 3 |
| 03 右表 | 导航 20.0 / 48.0 / 68.3；认焦点 78.1 / 83.4 / 81.8 | §4.3 表 5 |
| 03 右注 | “无 grounding 专门监督”；阶段 I 理由先描述当前 UI 与焦点元素 | §4.2 “Focus-Aware Grounding Evaluation”；§3.1 “Geodesic Guidance Traces”（z* 含 “a description of the current UI state and focused element”）。“隐含焦点监督”为我们的阅读判断 |
| 03 右条形 | TVWorld-G Acc@0.5：39.5/49.2/54.0/56.7/65.2/66.3/69.5/78.1/81.8；187 例；思考版低 8.6 | 表 4；§2.4；§4.2 |
| 04 左 | 理由类型消融 36.8/42.4/42.8/46.4/46.8（文字目标） | 附录 I 表 7。增量 +5.6/+0.4/+4.0 为我们复算 |
| 04 右 | 默认三次运行：文字 67.2/64.0/70.8，截图 68.8/67.2/72.0；标准奖励 64.0/67.6；最短路 66.4/67.2；软最短游走 65.6/68.4；PPR 60.8/59.2 | 附录 I 表 8、9、10 |
| 04 栏注 | 表 8/9 中“命中时间 / 拓扑奖励”行 67.2/68.8 与表 10 第 1 次运行相同，故按单次读 | 表 8、9 vs 表 10 Turn 1（我们比对） |
| 限制 | 静态图、屏蔽敏感入口；训练 1 张 TCL 图、测试 5 张 Google TV 图；闭源模型单次 | §2.2；Limitations；表 1；表 3 标题（只对 TVTheseus 报 3 次） |
| 限制 | 点击式模型近零的原因未拆分（格式、非法键、提示适配未报告） | 原文无此类统计（我们核对 §4 与附录 I） |

## 我们的判断（非原文）

- “改变的是动作接口这一环”“图距离奖励只在训练端可用”“能否迁到无图的动态真实界面本文未测”为阅读判断。
- 版式中所有图形均为我们绘制；条形与点位按原文表格数值绘制，01、02 机制图为示意。
