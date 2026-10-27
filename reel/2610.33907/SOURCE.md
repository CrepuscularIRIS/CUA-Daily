# SOURCE — 2610.33907 OS-Wizard: Scaling Computer-Using Agents to Specialized Software via Knowledge-Guided Exploration

- 论文：arXiv **2610.33907v1**（2026-10-24）
- 阅读材料：本地 `research/fulltext/2610.33907.txt`（文件头 v1，core，无附录）；按钉定版本补读了 arxiv.org/html/2610.33907v1 的正文和附录 A–F。转换稿放在 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-04.jsonl`（L2，P3 confirmed，q3 capability，F0/F1；卡 exploration_driven_task_synthesis；子卡 K15/C11）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-005.md` 第 1 节
- 画报源：`poster.html`（单文件，内联 CSS/SVG/JS 绘图）；`poster.png`（1400×2000）和 `poster.pdf`（1 页）由 headless Chrome 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题、副标题 | Qwen3.5-27B 5.9 → 64.1±0.7；10,919 条轨迹 | 摘要；§4.1 Data Collection；Table 1 |
| 副标题 | 同 10K：36.5 vs 13.0 / 18.9 → +23.5 / +17.6 | Table 1；§4.2。差值是我们的算术 |
| 统计条 | 最多 50 步；“Ours” 三次评测均值±标准差 | Table 1 注 |
| 统计条 | 54,938 样本、13 个应用；采样器 GPT-5.6-Sol / GPT-5.5 / Kimi-K2.5；GPT-5.6-Sol 兼任奖励模型 | §4.1 Data Collection；App. C |
| 统计条 | 23.73% 样本含 code；CODE 只对 ChimeraX、GRASS、KAlgebra、Lean、TeXstudio 开放；Celestia 与 OSWorld 只用 GUI | App. C 末段；App. A Table 3；§4.1 Benchmarks |
| 统计条 | 31.75% / 17,442 个通用应用样本（LibreOffice、Chrome、GIMP、Nautilus、VS Code） | §4.1；App. C Table 4 |
| 采集树（示意） | f(d)=max(10−3d,1)，D=16；一级全为枢纽；二级每 10 个兄弟选 2 个枢纽并存快照；每个 worker 丢 M=N−f(1)=3 个；二级状态检索 top-5 教程；f=1 时由前缀、教程和 5–10 条示例指令合成任务，连续执行 | §3.1；§3.2；Algorithm 1；Fig. 3 |
| 验收框 | 动作必须执行无错；无指令时 GUI 转移需奖励模型判有效，code 无错即过；有指令时只判完成；只因深度上限终止的轨迹丢弃 | §3.3；App. F |
| 验收框 | 重放动作数 15.7 → 14.2 → 2.7 | §5.3 |
| 三种走法 | 仅 GUI 10 步；在 GUI 中键入命令 3 步；CODE 1 步 | Fig. 1 说明 |
| 三种走法注 | CODE 不提供特权；GRASS 改为在界面中模拟输入命令 | §3.3；App. A “GRASS GIS” |
| 样本构成 | 各应用样本数；Lean 只用线性采集 | App. C Table 4；§4.1 |
| 阶梯 | 基座 5.9；Human Data 9.5；Task-driven 13.0；Branch-driven 18.9；OS-Wizard 10K 36.5±0.7；全量 64.1±0.7；Qwen3.8-27B 42.0；GPT-5.6-Sol 42.6；OS-Wizard-Qwen3-VL-8B 46.6±0.6；SCALECUA-Qwen3.5-9B 54.0†；人类 59.8† | Table 1（† 为原文标注的“引自原论文”） |
| 阶梯注 | “人工示范数据 SFT（样本量未注明）” | Table 1 “Human Data” 行；原文未给出该行的样本量 |
| 领域条 | 基座 12.1/13.8/2.9/0.0/0.0/6.3；全量 52.5/83.9/68.6/77.4/21.8/87.5 | Table 1 |
| 消融 | 20K：混合 55.0；去 code 26.6；只用树 41.4；只用线性 30.7 | Fig. 4(b)；§5.1 |
| 消融混杂 | 去 code 子集不含 Lean，Celestia 与通用应用占比上升；只用树的子集不含 Lean；只用线性的子集含全部 Lean | **我们的推断**：依据 App. A Table 3（CODE 定义）、App. C Table 4、§4.1（Lean 只用线性采集）、App. D（Lean 每步都是 CODE 编辑）。原文未讨论 |
| 消融注 | 不给文档时 75.71% 的分支走到 D=16 而被丢弃 | §5.1 |
| 限制 | Lean 题目来自 Formal Math Autoformalization Dataset，共 1,608 道 | App. D |
| 限制 | 基线按 OS-Genesis、ANCHOR 重实现 | §4.1 Baselines |
| 限制 | OSWorld 39.1 → 42.9 只用 GUI | §4.2；Fig. 4(a) |
| 限制 | 评测适配器增加了应用专属提示和 CODE 分发 | App. E 末段；App. A |

## 示意与重绘

- 采集树和三种走法是按 §3 与 Fig. 1–3 自行绘制的示意，已标注。
- 阶梯、领域条、消融条和样本构成条按原文表格重绘，不是原文图片。
