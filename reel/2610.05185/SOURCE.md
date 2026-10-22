# SOURCE: 2610.05185

- 论文：Recurrent Latent Visual Search for GUI Grounding（ReLaViS），作者姓名不在材料中，画报未写作者
- 版本：**2610.05185v1**（2026-10-04）
- 材料：① `research/fulltext/2610.05185.txt`（sha256 前缀 `ff4d06082fc009d1`，含正文 §1、§3–5，无附录）；② `/tmp/2610.05185.html` = `https://arxiv.org/html/2610.05185v1`（sha256 前缀 `fde500d7f6074318`，含附录 B.4、B.5，不提交）
- 初筛记录：`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`（screen_score 96.25，claim_support=supported_in_material，evidence_level=offline）
- 核对记录：`research/v3/runs/gui-v3-20261022-01/verify/2610.05185.md`（verify_ok；3.5% FLOPs 与 2.19 s 已在表 5 核实）
- 只读了原文，没有运行代码，因此不算复现。

## 数字 / 断言 → 原文

| 画报位置 | 数字 / 断言 | 原文 |
|---|---|---|
| 副标题 | Qwen2.5-VL-7B；GroundCUA 随机 100K 训练；推理只需截图和指令，不裁图、不用标注或 UI 树 | §4 Training data；§3.4 末段 |
| 问题条 | 单步定位在高分辨率、小目标、密集布局上吃力；文本推理与视觉空间不对齐；thinking with images 需要多轮交互和图像重编码 | §1 |
| 机制条 | s_t=softmax(Q_tK^T/√d)；Q_t 取自 h_t；z_t=s_t^T V 是凸组合，替换第 t 个 LVS-SLOT 的输入嵌入；T=4 | §3.1 式 (2)–(4)；§4 |
| 监督标签 | 递归二分取两侧外接矩形面积和最小的切分，得到 C1⊇…⊇CT；保留关键步；CWC 要求每个候选质量 ≥1/\|C_t\|；FGP 是末步 KL；三阶段训练 | §3.2 式 (5)(6)；§3.3 式 (7)(8)；§3.4 |
| 读出 | 在最大概率 token 的 3×3 邻域内按概率加权平均 token 中心 | §3.4 |
| 卡片 ①④ 金字 | 目标质量从约 0 升到 0.497；期望距离 0.345→0.091；熵降到 3.06（均为 ScreenSpot-Pro 上的统计） | §4.3；图 4 图注 |
| 卡片 ③ 金字 | 单步干预的效应：第 1 步小，第 2 步中等，第 3 步最大 | §4.2 RQ3 |
| 成本标尺 | TFLOPs：单步 coordinate-free 173.51，ReLaViS 179.65（+3.5%），Zoom-in+单步 coordinate-free 347.03（2 轮），UI-Zoomer 148.70 | 附录 B.4 表 5 |
| 成本标尺 | 延迟 2.06→2.19 s（+6.3%）；Zoom-in+单步 4.28 s；UI-Zoomer 2.34 s；峰值显存 18.78→19.54 GiB；单张 L40、BF16、batch 1；外部方法数据是其官方实现下的参考值 | 表 5 及其后文 |
| 哑铃图 | SS-Pro 53.2→56.3；OSWorld-G-Refine 59.3→62.5；MMBench-GUI-L2 80.2→81.1；SS-v2 90.4→90.7；UI-Vision 43.1→49.7；五集均值 65.3→68.1；3 个种子；单步基线是 T=1 变体 | 表 1 Controlled comparison；§4 Baselines |
| 哑铃图 ◇ | Zoom-in + single-step（coordinate-free）在 SS-Pro 上 62.3；3× 放大裁图后作第 2 轮 | 表 1；附录 B（zoom-in 实现）；表 5（2.0 轮） |
| 4 步消融 | 完整 56.3；仅终点监督 54.0；每步重复目标 53.9；固定 SLOT 54.5；回馈 h_t 55.2；几何缩放 53.8；打乱顺序 53.5；T=1 53.2 | 表 2；§4.2 RQ1/2/4 |
| 干预 | 对准目标注入使准确率升 2.0–13.1 pp，反向注入使其降 4.7–14.2 pp（五个基准） | §4.2 RQ3；图 3 右 |
| 限制 ① | UI-Vision 被作者列为域内，理由是与 GroundCUA 的应用覆盖重叠 | §4 Benchmarks；附录 B.5 |
| 限制 ② | Zoom-in+单步 62.3 > 56.3；Zoom-in+ReLaViS 63.5；GUI-Cursor 56.5（论文引用值） | 表 1 |
| 限制 ③ | UI-Zoomer 2.34 s / 148.70 TFLOPs | 表 5 |
| 限制 ④ | 训练约 88 h vs 69 h（4×L40），增加的部分在 Stage 3 的无梯度探测 | 附录 B.4 表 4 |
| 限制 ⑤ | 只覆盖点击动作，拖拽留待后续；评测是静态离线定位 | §5；初筛 caveat |

## 作者结果 / 阅读判断 / 示意

- **作者结果**：画报上所有数字，以及卡片和机制条中对方法的描述。
- **阅读判断**（限制列底部的虚线框，已标注「非作者主张」）：标题问题的回答是「对同骨干单步基线有效，但外部高分辨率集上 zoom-in 仍更强，两者互补」。限制 ③ 中「更省要看和谁比」的说法来自 verify 记录里我们自己的判断，作者只把 UI-Zoomer 的数据列为参考值。
- **示意**：模拟截图（设计软件界面、「对齐与分布」面板）、示意指令、s_t 热区、螺旋轨迹、C1–C4 候选框位置、3×3 网格的明暗都是自绘，没有复制论文图 1–5，也不是论文的真实样例。
