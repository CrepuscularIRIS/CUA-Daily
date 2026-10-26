# SOURCE — 2610.32536 IGG: A Benchmark for Interactive GUI Grounding under Visibility Constraints

- 论文：arXiv **2610.32536v1**（2026-10-23）
- 阅读材料：本地 `research/fulltext/2610.32536.txt`（文件头 v1，无附录）；已补读 arxiv.org/html/2610.32536v1 全文（正文 + 附录 A–H），转换稿存于 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-02.jsonl`（L2，P3 confirmed，q3 judgment，F1；卡 main/online_evaluation_methodology + main/high_resolution_target_localisation，子卡 C26/C22）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-004.md` 第 1 节
- run：gui-rolling-20261023-01；规则 problem-core-v1.1

## 数字与断言映射

| 画报内容 | 原文位置 |
|---|---|
| 601 个任务、16 个确定性仿制 Web 应用、3 类约束 7 个子类 | 摘要；§3.2–§3.3；Fig. 3 |
| 五种动作、8 步预算、greedy、每题一次；点击时比对元素 ID；1440×900 | §3.1 Table 1；§4.1；App. D |
| 模型只见截图、指令、动作历史；DOM、目标 ID、参考轨迹隐藏 | §3.1；§4.1 |
| 四阶段分解（选显露动作、位置/参数执行、认出目标、点击），前两步 = visibility recovery | §1 ¶3；§3.1 |
| Qwen3-VL 完整 30.8 / 告知交互 33.9 / 代执行显露 81.9；GPT-5.4 Mini (Low) 72.4 / – / 90.4 | §4.3 Table 4 |
| +3.1 与 +51.1 | §4.3 正文 |
| 人 94.6%：15 人、21 题（每子类 3 题）、315 次、298 次成功；预算只计点击/拖动 | §4.5 Table 5；App. H.1–H.2 |
| 子类 × 模型 GA 热表（含全部 601） | §4.2 Table 2 |
| 失败轨迹缺失动作：Drag 59/59、Scroll 207/247、Move 71/96、Wait 1/3 | §4.3；App. F.2 Table A6 |
| 固定规则显露率 68.8 / 61.4 / 87.1 / 17.6 / 16.9 | §4.3；App. F.3 Table A7 |
| 写明操作步骤的提示：Qwen3-VL 56.9%，留出可拖动遮挡 0/8 | App. C.3 “Effect of procedural hints” |
| SFT + GRPO：Qwen3-VL 40.0→59.2、InternVL3.5 28.3→47.5、GUI-Owl-1.5 35.0→52.5（120 题留出） | §4.4 Results；App. G.4 Table A8 |
| 479/120 划分，排除 2 题；留出题不进 SFT/GRPO | §4.4 Setup；App. G.1 |
| GRPO 仅从频率加权 SFT 起步有效；三个基座在留出集不输出 Drag；加权 SFT 7/8 用 Drag、解 4/8，GRPO 解 5/8 | §4.4；Fig. 6–7 |
| 仿真—真实配对 16 题，排序一致（r = 0.98） | §4.5；App. C.2 Table A4 |
| 限制：确定性仿制环境，不替代真实界面评测 | §6 |

## 自绘与示意

- 四阶段方块、括号与三条干预柱为自绘；柱长按 Table 4 数值线性映射，人类参考线按 94.6% 画（人类为 21 题子集，与 601 题不同分母，图中已标注）。
- 热表颜色深浅为按数值手工分档，非原文配色。
- 子类中文名为本栏目翻译。
