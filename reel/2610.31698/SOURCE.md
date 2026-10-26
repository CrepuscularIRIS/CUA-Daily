# SOURCE — 2610.31698 Understanding Tool-Mediated Interaction Failures in Agentic GUI Software: An Empirical Study

- 论文：arXiv **2610.31698v1**（2026-10-21）
- 阅读材料：本地 `research/fulltext/2610.31698.txt`（文件头 v1，有显式省略，缺 MalvaGuard 实验节）；已补读 arxiv.org/html/2610.31698v1 全文（§I–IX，含 §V-D 评估与 §VI 效度威胁；本文无附录），转换稿存于 /tmp，不提交
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-02.jsonl`（L2，P3 confirmed，q3 judgment，F1/F2；卡 main/structured_screen_observation + main/agent_loop_context_control，子卡 C18）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-004.md` 第 1 节
- run：gui-rolling-20261023-01；规则 problem-core-v1.1

## 数字与断言映射

| 画报内容 | 原文位置 |
|---|---|
| 40 个应用：Web 16 / 桌面 17 / 移动 7；2026-01-01 时的最新版本 | §I-B；§III-A；Table I |
| 约 2,000 个 issue → 关键词 + GPT-4o 初筛 + 人工 → 208 候选（closed 104 / open 104） | §III-B；§III-C |
| open issue 派生 62 个任务，各 20 次、3 分钟超时，共 1,240 次；录屏、DOM、提示与动作、调用与返回 | §III-C |
| 99 个确认缺陷（open 43 + closed 56）；在其余 39 个应用逐个检查并复现，得 335 例 | §III-D |
| 3 人独立分类，Fleiss κ = 0.95，第 4 人裁决，约 7 人月 | §III-D |
| 11 种模式，P1 88 / P2 104 / P3 82 / P4 61 例（和 = 335） | §IV-B–E 各节首段 |
| 各模式出现在 40 个应用中的比例（33/38/18/65/5/48/63/25/33/20/58%） | Table II “Apps (%)” |
| 各模式“N 个 app 出现” | Table II 末三列 Web/Desktop/Mobile 之和（反推；与正文“13 applications”“26 applications”“23 applications”“8 applications”一致） |
| 90% 的应用有两种以上模式 | 摘要；Table II 末行 |
| 86.6% 失败造成结果错误；119 例错而无 fail-stop | 摘要；§IV-A |
| 各模式举例：AppAgent tap(70)/66 元素；gemini-browser 未写文件报完成；LaVague 中心点遮挡；UI-TARS 取整；UI-TARS 最上层窗口归属；computer_use_ootb 下拉框；WebVoyager CAPTCHA；browser-use-typescript 530,000 vs 128,000 token；screenAgent ```json；pywinassistant x=331 y=79；autoMate 200→500 px；Surf 终端；cua get_vm；cua 按键早确认；desktop-agent ESC | §IV-B.1–IV-E.11；Fig. 5–12 |
| WhatsApp 案例：type 成功、click 投到代理自己的置顶透明状态窗、消息未发出；缺“哪个窗口持有焦点”的检查 | §I-A；Fig. 1 |
| MalvaGuard：交互区域 = 所在函数/方法（及同文件 helper）；缺护栏即告警；同规则同类型合并 | §V-A |
| 另 20 个应用（与 40 个不重叠），oracle 112；497 处告警 → 150 个缺陷；86 命中 / 64 误报；漏 26；57.3% / 76.8% | §V-D |
| 4 类全召回（模式不匹配、参数语义、上下文溢出、生命周期）；进展检查、前置条件、目标绑定召回低；升级边界 0 报告 | §V-D；Fig. 14 |
| 只给护栏类别建议，非自动修复 | §V-B |
| 限制：标签偏差、关键词漏检、复现环境、静态局部分析、开源与 Windows/Linux 外推 | §VI |

## 原文内部不一致（画报不使用）

- §IV-A 称进展检查缺失、工具模式不匹配、生命周期传播失败与上下文预算溢出“合计占 63.0%”（≈211 例）。按正文给出的“受影响应用数 × 平均例数”反推：进展检查 26×3.08≈80、生命周期 23×2.17≈50、上下文溢出 21，则模式不匹配须约 60 例；而 P3 总共 82 例，其中参数语义约 10×1.70≈17，前置条件出现在 13 个应用、至少 13 例，三项相加超过 82。画报因此不用 63.0% 和各模式例数，只用 Table II 的应用比例与各相位总例数。

## 自绘与示意

- 四相位环、各相位颜色、中心 State 标注：按 Fig. 2 与 §II-B 自绘示意。
- WhatsApp 案例图按 Fig. 1 文字描述重绘，界面元素与位置为示意。
- 模式中文名为本栏目翻译；举例为原文案例的转述。
