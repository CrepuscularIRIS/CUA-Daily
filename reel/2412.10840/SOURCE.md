# SOURCE · 2412.10840

- 论文：Attention-driven GUI Grounding: Leveraging Pretrained Multimodal Large Language Models without Fine-Tuning（Xu, Chen, Wang, Liu）
- 版本：arXiv **2412.10840v1**（2024-12-14，abs 页只有 v1）
- 材料：`research/fulltext/2412.10840.txt`（sha256 前缀 3564c827e8817242，正文完整，附录被截断）；附录 §6.1–6.7 补自 https://arxiv.org/html/2412.10840 （临时存于 /tmp，sha256 前缀 ca216558c4a83243，不提交）
- 初筛记录：run `gui-pc11-20261022-01`；L1 `batches/p012.jsonl`；L2 `batches/l07.jsonl`；入选 `selection.md` 第 1 行（P3 · judgment · F1 · high_resolution_target_localisation）

## 数字 → 原文位置

| 画报上的数字 | 含义 | 原文位置 |
|---|---|---|
| 8.5B、1344×1344、14×14 patch、1024 个头、单张 RTX 4090 | 骨干与运行设置 | §3.1；§3.2(3)；§3.4；Table 2 Model Size；§4 开头 |
| 0–1000 归一化、W/1000 缩放、取框中心 | 坐标路径机制 | 附录 §6.2 式 (8)–(11) |
| K=10、δ=0.5 | 筛头与阈值 | §3.5；§4.5（Fig 6/7 扫描；正文写 "Figure 7" 指 K，标题中 K 是 Fig 6） |
| OCG 48.1 / 84.5；SeeClick 60.2 | 10 种宽高比平均 | Table 1 |
| OCG 各比例：MiniCPM 17.2, 13.6, 15.9, 21.4, 31.0, 80.2, 84.6, 81.1, 77.2, 59.2；TAG 86.1, 80.3, 80.2, 84.8, 84.7, 82.6, 86.6, 87.9, 83.9, 88.0；SeeClick 52.7 … 69.1 | 折线图（按数值重绘） | Table 1 |
| 每个比例 1030–3797 个目标 | OCG 样本量 | 附录 Table 5 |
| ScreenSpot 36.0 / 54.8；SeeClick 53.4 | 三平台平均 | Table 2 |
| 移动文本 40.3 / 88.3；移动图标 14.0 / 29.3 | ScreenSpot 分项 | Table 2 |
| 图标 14.0 / 12.1 / 19.9（基线），29.3 / 28.6 / 29.1（TAG），SeeClick 移动图标 52.0 | 失败面 | Table 2 |
| Mind2Web 15.7 / 24.3；SeeClick* 24.3（在 Mind2Web 训练集上微调） | 单步元素准确率 | Table 3；§4.3；附录 §6.5（提示含最近 4 步真值历史） |
| VisualWebBench 78.4 / 87.4 | 元素定位（MiniCPM 直接输出框 vs TAG） | 附录 Table 7 |
| 1.10 s → 1.04 s | ScreenSpot-Desktop 每例耗时 | 附录 Table 6 |
| 40.3→71.8、14.0→27.1、62.4→73.2；+token 选择 86.4；全部 88.3 | 组件消融（行 2 = 只开注意力回投） | Table 4；§4.4 |
| Qwen-VL-Chat 2.7 → 10.2 | 换骨干（OCG 4:3） | §4.5 Generalization |
| "预训练数据未覆盖所有宽高比" | 作者推测，画报标"作者推测" | §4.1 Results |

## 关键断言与标签

- 作者报告：证据蝴蝶图、折线图、归因分离①。
- 阅读判断（画报以虚线标签标出）：归因分离②"目标看得见、失败在坐标接口"，③"图标缺口不能归给坐标格式"，以及限制栏"不说明坐标 SFT 无用"。
- 对照条件：OCG 两路径用同一 OCR 查询文本与基本相同的问句（§4.1、§6.1）；ScreenSpot 上 TAG 先生成元素描述（Fig 4），提示不等长。
- 自绘示意：截图图标、坐标数字串（412/087/530/121 为虚构示例）、patch 热图。未复用原论文图片。
- 柱图、折线图只按原文表格数值重绘。
