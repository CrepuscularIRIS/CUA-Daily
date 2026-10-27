# SOURCE — 2610.34384 AndroidFlux: Evaluating Failure Recovery and Recovery Action Reward Modeling in Mobile-Use Multimodal Agents

- 论文：arXiv **2610.34384v1**（2026-10-25）
- 阅读材料：本地 `research/fulltext/2610.34384.txt`（文件头 v1，core，无附录）；按钉定版本补读了 arxiv.org/html/2610.34384v1 的正文和附录 A–F。转换稿放在 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-04.jsonl`（L2，P3 confirmed，q3 judgment，F2/F5；卡 online_evaluation_methodology、learned_outcome_and_process_judges、agent_loop_context_control；子卡 K26/K16/C22）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-005.md` 第 1 节
- 画报源：`poster.html`（单文件，内联 CSS/SVG/JS 绘图）；`poster.png`（1400×2000）和 `poster.pdf`（1 页）由 headless Chrome 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 副标题、斜率图 | GUI-Owl-32B Scratch 53.75 → t_all 26.25；Qwen3-VL-30B-A3B 13.75 → 26.25 | App. C Table 9 |
| 斜率图其余 9 条线 | MobileRun 78.75/67.50；FinalRun 66.25/43.75；Mobile-Agent-v3-7B 58.75/38.75；Gemini Flash 3.8 51.25/53.75；Qwen3.8-27B 45.00/32.50；Qwen3-VL-8B 41.25/28.75；Gemma-4-31B (M3A) 37.50/42.50；Qwen3.6-27B 17.50/31.25；UI-TARS-1.5-7B 12.50/23.75 | Table 9（Scratch 80 = 同一 116 题运行限于这 80 题；t_all 80） |
| 斜率图注 | 4 次重复下 80 例总体波动 2.5–8.75 点（6 个模型） | App. C.6.2 Table 18 Range 列 |
| 设置栏 | AndroidWorld 程序化 verifier；目标代理不被告知在恢复 | §3 Eq.(3)；App. C.6.2 |
| 设置栏 | 人工集 80 例：6 个源模型 672 条轨迹逐步人工审，65 重放 + 15 快照 | §4.1；App. C.1 Table 10 |
| 设置栏 | LLM 集 312 例、104 个任务、21 个源模型；检测-复核 step precision 90.8、recall 50.8 | §4.1、§4.1.1；App. C.9 Table 24 |
| 检查点示意 | t−n / t−1 / t / t+1⁺ / t+1⁻ 的定义；历史按目标代理格式重渲染；修好但未完成记失败 | §3；App. C.6.2；Table 15 说明 |
| 交叉线 | 倒带 +8.76 / +7.67 / +3.41；注入 −1.01 / +7.55 / +5.86；n = 116/100/96 | §5.2 Table 4 |
| 交叉线注 | 最晚−最早 +12.22，95% CI [+4.1, +20.8]（episode 重采样）；17/18 模型为正；难度四分位、长度三分位、随机两半全部为正；注入只在 196 个 episode 上算 | §5.2；App. C.6 Table 19、Table 20、“Coverage of the two gains” |
| 哑铃图 | BT-256K .915→.520；BT-128K .904→.490；SFT soft .878→.450；SFT hard .681→.160；GUI-Owl-1.5-8B .744→.590；MAI-UI-8B .736→.600 | §5.3 Table 5 |
| 哑铃图注 | 100 对共享任务/状态/截图/历史；12 个代理续跑成功次数差 ≥2 | §4.2；App. D |
| 哑铃图注 | 100 对时随机波动 ±0.10（95%） | **我们的算术**：1.96×√(0.25/100) ≈ 0.098，原文未给出 |
| 限制 | 一半的对处在差 2（50/100） | App. D Table 27(b) |
| 限制 | 5 个单代理打分模型 = 5 个候选生成模型 | App. D Table 26 与 Table 5 列名对照；**我们的阅读**，原文未讨论 |
| 限制 | Qwen3-VL-32B Instruct Scratch 36.25 vs Thinking 11.25 | App. C Table 9 |
| 限制 | 离线 RL 单 seed、65 题；同配方换 seed 差 2/65 与 4/65 | App. E.2 “Evaluation” 与 “Variance and scope of the mixture study” |
| 限制 | 快照例更易恢复 | Table 2 t_snap 普遍高于 t_rep |

## 未上画报的原文主张及原因

- “explicit reasoning helps only models trained with GUI-domain specific RL”（摘要、Table 3）：思考版在 Scratch 上也普遍更差（Table 9），不能单独归到恢复，只在限制栏提及。
- Oracle 列（5 agents 0.82、+BT-256K 0.87）：“任一打分器对即算对”会随打分器数量机械上升，不能说明互补，未上画报。
- 离线 RL 混合比例结果（Table 6）：单 seed、65 题，差异处在换 seed 的波动范围内，只在限制栏提及。

## 示意与重绘

- 检查点时间轴：按 §3 和 Table 15 的定义自行绘制，标“示意”。
- 斜率图、交叉线图、哑铃图：用作者表格数字重绘，不是原文图片。
