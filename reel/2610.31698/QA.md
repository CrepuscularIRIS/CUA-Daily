# QA — 2610.31698 Tool-Mediated Interaction Failures（Malva / MalvaGuard）

- 状态：**ready**
- 制作：Opus 5.5 L3 选题与 Reel 席，2026-10-26，run gui-rolling-20261023-01 第四期
- 版本：arXiv 2610.31698v1（本地 core 缓存 + arxiv.org/html 全文；本文无附录）

## 原文核对

| 核对项 | 结论 |
|---|---|
| L2 问题判断（Q1 measured_own、Q2 open_failure、Q3 judgment、Q4 fits、P3 confirmed） | 同意 |
| L2 biggest_gap：MalvaGuard 主实验缺失 | 已补读 §V-D：另 20 个应用、与原 40 个不重叠、按 §III 同流程人工建 oracle 112 个缺陷；150 报告中 86 命中，漏 26。数字与摘要一致 |
| 335 的含义 | 99 个确认缺陷跨应用复现之和（§III-D）。与 L2 提醒一致；画报以警示框写明 |
| 发生率解读 | 以 issue 为入口，筛掉偶发故障（§III-D 第 2 条标准），比例只描述缺陷库。画报限制栏写明 |
| κ = 0.95 | 只针对模式归类（§III-D），不是缺陷确认的一致性 |
| 原文 §IV-A “63.0%” | 与 Table II 和各节计数反推不一致（见 SOURCE.md）。属原文问题，不涉及 L2 记录；画报不用 |
| L2 subcard C18 | 同意 fails/fails/partial/unknown；前两项 fails 指被研究系统的条件失效 |

无 correction，不退回。

## 视觉验收（实际打开 poster.png）

- 1400×2000 PNG；PDF 1 页（1050×1500 pt）。深色底，中文 Noto Sans CJK、数字 DejaVu Sans Mono 正常；下标 agent/env 与 ≠ 正常。
- 第一次渲染不过：举例文字按固定字数折行，把 “cua)”“UI-TAR/S”“computer_/use_ootb” 拆断；相位标签压在色环与中心圆交界处；环下方图例与左右两组模式框重叠。
- 重做一次：举例改为手工断句；相位标签移到色环外侧并用相位颜色；图例移出 SVG 放到面板脚注；模式框行距加大、字号 14.5。
- 第二次检查仍不过：中心圆下部“119 例……”宽于该处弦长，压到色环。再改中心排版（文字上移、字号缩小、文案缩为“119 例错而不报”），复查通过。共两轮修改，如实记录。
- 最终检查：无裁切、无重叠；缩到 700 px 宽时标题、335、86.6%、四相位例数与百分比条可辨认；最小字号约 12 px（脚注、“N 个 app 出现”）。
- 标题“模型看到的不是屏幕：工具层让代理的‘所见’与真实界面静默脱节”对应摘要 “makes the agent’s view of the task diverge from the live GUI” 与 §IV-A 的 silent failure 统计，未超出原文。
- 与前三期 19 张及本期另 2 张比较：首个“环形相位 + 四角模式框”骨架；深石墨底配琥珀色，区别于 2604.04918 的深墨蓝漏斗。

## 剩余问题

- 各模式例数原文未直接给全，画报不展示。
- poster.html 若被 .gitignore 忽略，保留本地，发布时精确处理该路径。未操作 git。
