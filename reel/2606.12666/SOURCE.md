# SOURCE · 2606.12666

- 论文：Shen, Xu, Diao, Zhang. *CAPED: Context-Aware Privacy Exposure Defense for Mobile GUI Agents*。
- 版本：arXiv 2606.12666**v2**（cs.CR，HTML 页头 16 Jun 2026；缓存头标 2026-06-10）。
- 阅读材料：`research/fulltext/2606.12666.txt`（v2 HTML 提取，§I/§III/§IV/§VI 有截断）；缺的部分（表 I 后文、表 V、§IV-G、附录 A/C/D/E-B）由 https://arxiv.org/html/2606.12666 补齐，只存 /tmp，不提交。
- 初筛记录：run `gui-pc11-20261022-01`；L1 `batches/p049.jsonl`，L2 `batches/l41.jsonl`（P3 / capability / F4,F0 / 主卡 unassigned）；入选见 `selection2.md` 第 22 行，待核问题见第 49 行。

## 数字与断言 → 原文位置

| 画报内容 | 原文 |
|---|---|
| 问题：顺带的视觉隐私暴露；“把海滩照片发给 Bob”例 | §I（图 1）；§II-B |
| 威胁模型：手机侧可信，远端诚实而好奇；不防注入/恶意 App | §II-C |
| 只放出匿名任务 + 遮蔽后截图 | §I；图 2 题注；§III-B |
| 任务需求 `{app, subject, type}`，type ∈ person/item/date/open/none；实体换占位符 | §III-C |
| 本地抽取每条指令一次，Qwen3.5-0.8B | §III-C；附录 A-A |
| 上下文三级 Public / Privacy / Text-Privacy 及典型场景 | §III-D 表 I |
| 包名为主、Activity 补充；未覆盖默认 Public | §III-D；§VI-A |
| 元素切为 text / icon / image；文本名称匹配或语义相关；图像需 VQA | §III-B、§III-D；图 3 |
| 被遮内容可在需要时临时揭开并记录 | §III-A “Make masking recoverable” |
| 远端 GUI-Owl-7B；OCR（PaddleOCR）+ UIED 检测；EmbeddingGemma | §IV-A；附录 A/D |
| 28 任务 × 5 方法 = 140 次运行；三类：模拟 9、本地 10、联网 9 | §IV-A 表 II |
| WSLR 定义、权重 1/2/3、剔除任务所需、只在 utility=1 的运行上平均 | §IV-C |
| 泄漏/效用分栏：模拟 1.000→.217 / 1.000→.944；本地 .847→.254 / .750→1.000；联网 .433→.347 / .944→.833 | 表 III（No Protection vs Full CAPED） |
| 总体：WSLR .766→.268，效用 .893→.929；成功 24/28 vs 25/28 | 表 IV |
| 五方法散点：Text-Only .911/.752；去元素核验 .786/.124（21/28）；去任务抽取 .321/.028（9/28） | 表 IV |
| “遮到走不下去”：去任务抽取 19 个失败/部分中 10 个没走到隐私界面 | §IV-D Takeaways |
| 不加权口径 .773 / .288 | §IV-C “Weight sensitivity” |
| 23/28 任务与原图同分，效用排序仅描述性 | §IV-D Takeaways 末句 |
| 联网 .347 vs Text-Only .402，相对 13.7%；作者称趋势证据 | §IV-D；表 III |
| AndroidWorld 77/116（66.4%）→ 64/116（55.2%），差 11.2 pp；19 退步 / 6 改善；7 个归为受 CAPED 影响 | §IV-F 表 V 及其后段落 |
| 残余：开放式范围 13 条事实、权重 33/80 | 附录 C 表 IX |
| 每步 10.835 s，隐私组件 2.325 s（22.6%），检测器 1.811 s；原型跑在评测主机/服务端，不代表手机时延 | §IV-G 图 5；附录 D |
| 判官 gpt-5.4；重复 3 次，136 条目 1 个翻转（0.74%） | §IV-C “Judge auditability” |
| 跨轨迹推理只部分覆盖 | 附录 E-B “Risks” |

## 我们的推算（非作者结果）

- −0.498（.766−.268）、+0.036（.929−.893）：按表 IV 相减。
- “分母不是同一批轨迹”：由表 IV 成功数 24/28 vs 25/28 与 §IV-C 成功条件化定义推出；Sol L2 已列为待核点。

## 示意（自绘，非论文图）

- 两部手机界面（相册 + 联系人）与遮蔽效果：按 §I 例子与 §III 机制自绘，不是论文图 4 的实拍截图。
- 中间任务三元组 `{相册, 海滩照片, item}` `{消息, ⟨人物_1⟩, person}`：按 §III-C 格式举例，论文未给该例的实际抽取结果。
- 散点图右下“理想区”方框：阅读辅助，不是论文定义的阈值。
