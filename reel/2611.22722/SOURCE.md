# text-pixels (2611.22722) — SOURCE

论文：*Practice in Text, Act in Pixels: Correcting Where Perception Fails*，arXiv 2611.22722v1，2026-11-17。
缓存全文：`research/fulltext/2611.22722.txt`（FULLTEXT: html，正文 §1–§6 与 Tables 1–5、补充材料节选）。核对于 2026-11-19（本仓 selection-019，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 标题"文本里练会，像素上失手"（practice in text, act in pixels） | "We call this recipe practice in text, act in pixels" | §1 |
| 文本 87.5% vs 截图 43.0%（干净文本练习策略） | "completes 87.5% of new instances … in text but only 43.0% on screenshots"；Table 1 首行 87.5±1.4 / 43.0±3.0 | §1，Table 1 |
| −44.5 点落差（中缝大数字） | Table 1 首行下标 −44.5 | Table 1 |
| 文本回合 GPU 成本约 1/7.2 | "an episode costs about 7.2× more GPU time on screenshots than in text" | §1 |
| 读屏器 Qwen3-VL-4B 半尺寸截图、贪心解码 | "Qwen3-VL-4B-Instruct … reads half-size screenshots with greedy decoding" | §3 |
| 文本视图格式（角色/文字/状态/颜色/位置框，布局序） | "one line per visible element, with its role … its text or icon name, its state, its color and its box" | §3 Text view |
| 五组训练法落差 ≥29.5 点（含三种已花截图的） | "Every first-round group loses at least 29.5 points"；Table 1 五行下标 −44.5/−33.8/−30.6/−31.0/−29.5 | §4.1，Table 1 |
| 哑铃五组 87.5→43.0 / 83.3→49.6 / 82.6→52.0 / 86.6→55.6 / 85.3→55.9 | Table 1 全表（Text/Pixels 两列） | Table 1 |
| 错序单独扣 21.8 点；误读布局序下扣 47.0、读屏器序下 30.4；叠加小于单独之和 | "Listing the correct elements in the reader's order lowers success by 21.8 points. Misreads cost 47.0 points in the layout order and 30.4 in the reader's order, so the two losses overlap" | §4.2 |
| 误读系统性 73.2% vs 30.9%（4B，T=0） | Table 2 首行 73.2 / 30.9，+42.3 | §4.3，Table 2 |
| 8B 全尺寸 77.7% vs 24.9%；T=0.7 61.1 vs 29.8；InternVL3-8B 89.7 vs 77.6（+12.2 未过 20 点阈） | Table 2 后三行及 ✗ 标记 | §4.3，Table 2 |
| 同一文字两次读错写同一错字 98.9% vs 对照 45.6% | "it writes the same wrong text in 98.9% of cases, against 45.6% under the control" | §4.3 |
| 新实例 93.2% 误读落在校准已错元素、占读取量 36% | "93.2% of the 4B reader's errors fall on elements it already misread … although these elements account for only 36% of its reads" | §4.3 |
| 注噪环境预测相关至多 0.70 vs 真跑 0.90 | "correlation across tasks of at most 0.70, against 0.90"；predictivity M | §1，§4.4 |
| 按误读率注噪 vs 直接截图训练无可测差异 | "rate-matched-noise practice … shows no measurable difference from direct screenshot training"（预注册对比） | §1，§4.4 |
| 读屏器对齐：约 2,000 张截图配对文本视图微调、策略不动 | "Reader alignment fine-tunes the screen reader on about 2,000 screenshots paired with their text views … the policy stays unchanged" | §1，§5 |
| 80.9% vs 55.6%（+25.3） | Table 3 首两行 80.9±2.2 / 55.6±8.3（−25.3） | §6.1，Table 3 |
| 复现 +27.6 / +26.6（另两个实例集） | Table 3 下两块 79.6 vs 52.0（−27.6）、81.5 vs 54.9（−26.6） | §6.1，Table 3 |
| 同样标注改策略 67.2%（−13.6） | Table 3 "Adapted, same labels" 行 | §6.4，Table 3 |
| 查表基线 69.4%（回收 70% 增益） | Table 3 Lookup 行（−11.5）；"recovers 70% of the gain" | §6.3，Table 3 |
| 8B 未对齐 46.4%（半尺寸）/48.9%（全尺寸） | Table 3 两行 −34.5/−32.0 | §6.4，Table 3 |
| 4B 对齐后超过 8B、0.52 倍读取成本 | "The aligned 4B reader clearly exceeds both 8B configurations … about 0.52 of the 8B reader's cost per read" | §6.4 |
| 500 张 63.4% 追平 2,000 张直接训策略 | "With only 500 screenshots, alignment reaches 63.4%, comparable to training the policy directly on about 2,000"；Table 3 Aligned with 500 行 | §6.4 |
| 三策略提升 ≥24.0 点无重训：43.0→80.9 / 40.5→75.9 / 52.0→76.0 | Table 4（+37.9/+35.3/+24.0） | §6.2，Table 4 |
| 基座策略例外（文本 21.0%，无可测提升） | "The untrained base policy completes only 21.0% … no measurable difference" | §6.2 |
| 误读率下降：held-out 25.62→1.56 / 确认集 26.51→1.95 / 新屏 27.03→2.92 | Table 5 上部三行组 | §6.3，Table 5 |
| 屏幕精确重复 36.9%（确认集） | "36.9% of the screens encountered on the confirmation set exactly repeat a calibration screenshot" | §6.3 |
| 留出 app：误读 26.27→7.59%，任务成功率 70.4% vs 73.6% 无可测差异 | "the element error rate falls from 26.27% to 7.59%. On their 9 single-app templates, task success is 70.4% … 73.6%" | §6.4 |
| MobileGym 中文模拟 app（微信/支付宝/时钟） | "runs simulated Chinese-language mobile apps, such as WeChat, Alipay and Clock" | §3 Platform |
| 不用官方 256 测试模板（新模板文本也基本失败） | "We use none of MobileGym's 256 official test templates … mostly fail on new ones even in text" | §3 Evaluation |
| 剩余缺口集中少数模板；CalendarEarliestToAlarm 文本全对像素全错 | "CalendarEarliestToAlarm, for example, succeeds in every text episode but in none on screenshots" | §6.1 |
| 剩余缺口归因排序差异/输入框误读、非执行器 | "the first discrepancy … is an ordering difference or a misread input field; none is traced to the executor" | §6.1 |
| 预注册对比框架、固定短语（clearly/slightly/no measurable） | "one of four fixed phrases"；"Decision rules for the headline comparisons were fixed before their results were seen" | §3 Statistics |
| 读屏器/策略同 Qwen 谱系（4B VL + 8B policy）；谱系外仅测误读复发性 | §3 Policies（Qwen3-8B+LoRA）；Table 2 InternVL3-8B 行 | §3，§4.3 |
| 边界：本文不测真实设备任务级效果 | 编辑陈述：全文只在 MobileGym 模拟平台（L2 gap"真实设备任务级效果未测"一致） | 全文范围 |

## 编辑收窄

- 哑铃图红端（像素端）在深底上用数字端点呈现、未画红色端段——73.2% 等深色对比问题不涉及；哑铃共尺度 0–100 与 axis 标注一致。
- "预算该花在错的源头"为编辑综合结论（80.9 vs 55.6 + 系统性误读 + 注噪无效三证据链），原文 §1 问题句"where a fixed budget of real screenshots is best spent"的直接回答。
- 查表基线的 70% 回收如实呈现，并注屏幕重复 36.9% 的口径——不把对齐优势全部归因新屏泛化；新屏误读率 27.03→2.92% 作为泛化侧证。
- 留出 app 的"误读降但成功率不降"不修饰为部分成功：原文口径"task success shows no measurable difference"。
- 上期 selection-018 对本篇的排除理由（中文模拟生态弱、同谱系、屏幕重复）在本期画报以"部署边界"卡如实保留；本期入选理由（机制证据干净：29.5 点跨五法稳定 + 读屏器对齐的预算对照 + 误读系统性因果链）见 selection-019.md。
