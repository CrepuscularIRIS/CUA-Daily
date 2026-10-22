# SOURCE — 2505.15810 GUI-G1

- 论文:GUI-G1: Understanding R1-Zero-Like Training for Visual Grounding in GUI Agents,arXiv **2505.15810v2**
- 阅读材料:本地 `research/fulltext/2505.15810.txt`(裁剪 core,缺 §3.3 后半、附录);已补读 arxiv.org/html/2505.15810(v2,含附录 A–E)与 arxiv.org/pdf/2505.15810v2 第 3–6 页图像(Fig.2/3/4/6 曲线),缓存在 /tmp,不提交
- 初筛记录:`research/scoring/runs/gui-pc11-20261022-01/batches/p018.jsonl`(L1)、`batches/l11.jsonl`(L2,P3 confirmed);入选见 `selection.md` 第 1 节 #2
- run:gui-pc11-20261022-01;规则 problem-core-v1.1

## 数字与断言映射

| 画报内容 | 原文位置 |
|---|---|
| 三组件拆解(模板/奖励/目标函数) | §1、§3 开头、Fig.1 |
| 只用 R_Hit:框↓ 准确率↑ IoU↓;只用 R_IoU:框↑ 准确率↓ IoU↑;R_Box 单独无法优化(格式失效) | Tab.1;§3.2 正文 |
| 只用 IoU 时准确率中途下滑、终点低于其他组合;只用 Hit 时 IoU 先升后回落 | Fig.3 左/中(读图,画报未标数值) |
| Hit+IoU 仍被一方主导、框偏小;Hit+IoU+Box 准确率与 IoU 均改善、框更接近真值 | §3.2 “R_Box helps mitigate…”;Fig.3 右 |
| 归因:GRPO 组内相对比较使小框/大框分别胜出 | §3.2 “GRPO’s sample selection bias…”;Fig.4 右;Eq.1 |
| 分析设置:Qwen2.5-VL-3B-Instruct,三域各 300 条,8 rollout,无 KL | 附录 C.1 |
| 约 300 步、3 个检查点 | Fig.3 横轴(100/200/300) |
| 1/|o| 长度偏置:错误回答变长、正确回答变短 | §3.3 第一条;Fig.6 左 |
| |o| → Max_Tokens;难度权重 w_q 由相对框尺寸计算,小目标权重大,范围 (0.5,1.5] | §3.3;§3.4;附录 C.3 |
| Tab.2 ScreenSpot 平均:标准 GRPO 82.3 / Max_Tokens 83.2 / w·J 83.3 | Tab.2 最后一列 Avg. |
| 推理长度分析:InfiGUI-R1-3B、ScreenSpot、文字目标随输出 token(75–115)下降,图标目标起伏 | §3.1;Fig.2 左 |
| 同一图像 token 档内文字占比高者更差 | §3.1;Fig.2 右 |
| 快/慢思考模板文本 | §3.1 Template 1/2 |
| 最终设置:17K(UI-BERT + OS-Atlas,8 次采样全对/全错者剔除)、Hit + 0.25·IoU + 0.125·Box、无 KL、1 epoch | §4 Implementation Details / Training Dataset;附录 D.1 Tab.6 |
| GUI-G1-3B ScreenSpot 90.3 vs InfiGUI-R1-3B 87.5(32K) | Tab.4 |
| ScreenSpot-Pro 37.1 vs InfiGUI-R1-3B 35.7、UI-TARS-7B 35.7 | Tab.5;§4 正文 |
| InfiGUI-R1 用 RLOO + Thinking Template | Tab.3 |
| 输出 token 37/39/39 vs 107/107/114 | 附录 D.2 Tab.7 |
| OS 子集 16.1 vs OS-Atlas-7B 16.8 | Tab.5;§4 正文 |
| 仅 grounding、无动作预测/长程规划 | 附录 B (1) |

## 自绘与示意

- 中央“四种框”图:自绘示意,方向依 Fig.3 右与 Fig.4 左,框的比例不是实测值。
- 旁路两张小曲线:按 Fig.2 左、Fig.6 左走势手工重绘,未标纵轴数值,不是原图。
- 投机回路(①–④ 与阀门 A/B):本篇阅读整理的因果结构,节点内容均对应上表原文位置。
- 未使用任何原论文图片。

## 作者结果 / 阅读判断的区分

- 标“作者结果/作者解释/作者观察”的内容来自原文。
- 标“阅读判断”的两处(长度结论仅对文字目标、相关性;ScreenSpot 只判中心点使 Hit 缩框在榜单上不可见)为本篇核对者判断,不是作者结论。
- 未运行任何代码,不构成复现。
