# SOURCE — 2601.22781 Learning with Challenges (MobileGen)

- 版本:arXiv 2601.22781v1(2026-01-30)。材料:本地 `research/fulltext/2601.22781.txt`(html 缓存,§1、§3、§4 有截断)+ arXiv HTML 全文(含附录 A.1–A.6)临时存 /tmp,未提交。Fig.3 `ablation.svg`、Fig.4 `point.svg` 为原文矢量图,下载到 /tmp 后按几何坐标读数,未提交、未嵌入画报。
- 初筛记录:`research/scoring/runs/gui-pc11-20261022-01/selection2.md` 第 5 条;L2 `batches/l77.jsonl`(P3 / judgment / F5 / exploration_driven_task_synthesis)。
- 画报图表全部为自绘;没有复制原图。流程图标标"示意"。

| 画报内容 | 原文位置 | 类型 |
|---|---|---|
| 500 条合成轨迹、平均约 20 步、生成骨干 Qwen3-VL-8B、LoRA SFT | §4.1 Implementation Details | 作者 |
| 能力画像:500 条先验轨迹、Pass@K(K=3)、逐步动作匹配 | §3.2.1 Eq.1–2;A.5.1;Table 5 k=3 | 作者 |
| C* = C·(1+α·η) | §3.2.2 Eq.3 | 作者 |
| 高斯核采样 DoT/BoT,三角隶属度采样 ICD/IUD | §3.2.2 Eq.4–6;A.4 | 作者 |
| 探索者+监督者、步数预算、回滚、逆向合成指令 | §3.2.3;A.6.1–A.6.2 | 作者 |
| α 扫描 0 / 0.5 / 1 / 2,α=0 称 trivial、α=2 称 hard;0.5 最优、领先 4.3%、训练 loss 最低 | §4.3 "Impact of Challenge Point Setting";Fig.4(图内标注 +4.31%) | 作者 |
| 四档 SR 41.4 / 45.7 / 40.5 / 35.3 | Fig.4 左图柱高,按矢量坐标换算(y 轴 30→45 每 2.5 为 47.75pt):41.38 / 45.69 / 40.52 / 35.34 | 读图 |
| ≈48/53/47/41 题(116 题) | 116 题见 A.2;四值分别与 48/116、53/116、47/116、41/116 一致到 0.01 | 推算 |
| +4.3 pp ≈ 5 题;α=2 比峰值低 10.3 pp ≈ 12 题 | 由上两行相减 | 推算 |
| 训练 loss 中位数 0.314 / 0.289 / 0.291 / 0.298 | Fig.4 右图小提琴中位线坐标(y 轴 0.20→ 每 0.05 为 63.56pt) | 读图 |
| Fig.4 基准为 AndroidWorld、学生 Qwen3-VL-8B | 学生见 §4.3 原文;基准未写,α=0.5 的 45.7 等于 Table 1 Qwen3-VL-8B AndroidWorld SR 45.7,据此推定 | 推定 |
| AndroidWorld:在线、116 题、M3A 框架、SR | §4.2;A.2 | 作者 |
| 参考线 31.0 零样本 / 37.9 OS-Genesis / 41.4 GUI-ReWalk(Qwen3-VL-8B,AndroidWorld SR) | Table 1 | 作者 |
| 参考线/消融 41.4 随机难度分布(w/o dist)、40.5 去预算、37.9 去回滚、45.7 完整 | Fig.3 雷达图 AW-SR 轴(35–48%),按矢量半径换算:中心=35、外圈 r=239.04pt=48;完整版换算 45.70、AC-SR(Hard) 换算 38.40,与 Table 1 一致,验证读法 | 读图 |
| "去掉回滚下降最多,差 4.4%–12.2%" | §4.3 "Effectiveness of Critical Components" | 作者 |
| 倍数 ×(1+6α)、×(1+α)、×(1+0.8α) 及各档值 | Eq.3 + Table 5 默认 η_d=6、η_b=1、η_int=η_ins=0.8;假设扫描时 η 不变,C 的数值原文未报告 | 推算 |
| AC-Curated、GUI-Odyssey 为离线逐步指标(Type/Grounding/SR、AMS) | Table 1–2 标题;A.2 | 作者 |
| AC-Curated "only 20 out of all included applications were seen during training" | §4.2 AndroidControl-Curated 段 | 作者 |
| 案例用 Simple Calendar Pro | A.1.2 Fig.5 | 作者 |
| 语义难度由提示词指定(ICD 注入探索者提示词,IUD 注入合成者提示词);先验集 ICD 3×3 网格、IUD 均匀采样 | §3.2.3;A.5.1;Fig."Prompt for Semantic Difficulty" | 作者 |
| 数据质量由 VLM judge 打分(Table 3) | A.1.1;A.3.2 | 作者 |
| 未报告 seed/重复次数、未报告不同 α 的生成成本 | 全文(含附录)未见 | 我们核查 |
