# SOURCE — 2611.16693 MobileProbe: Adaptive Security Evaluation of Mobile Agents via Trajectory-Aware Injection

- 论文：arXiv **2611.16693v1**（cs.CR；2026-11-13 查 export.arxiv.org/api：published = updated = 2026-11-12T12:08:43Z，唯一版本）。作者 Jin、Wang、Chai、Luo、Hu、Li、Zheng、Hu、Ye、Hu；作者注 NDSS 2027。标题、作者与 corpus.jsonl、本地缓存头一致
- 阅读材料：本地 `research/fulltext/2611.16693.txt`（裁剪 core：摘要、§I、§III、§VI–VIII）+ arxiv.org/html/2611.16693v1 全文（§I–VIII、表 I–XI、附录 A–G 的评分细则、策略 / 风格定义、页面模板、基线提示与示例）。转换稿在 /tmp/sel15，不提交。图 1–5 为栅格图，未读像素。未运行代码或攻击
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-44.jsonl`（L2，supersedes inc-l1-90#2611.16693；P3 confirmed to_l3；q3 judgment；F2,F4；卡 environmental_injection_attacks、online_evaluation_methodology）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-015.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG/JS）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome（Playwright，`--disable-lcd-text`）渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 固定（专家）点 PMR 12.0–22.9%；MobileProbe 3.6–6.0% | 表 II；§VI-B |
| 副标题 | 12 app、83 实例、恶意文本 44 / 假弹窗 39、C 27 / I 28 / A 28；3 代理；每任务每代理 3 次 | §I 末段；§V-B–C；§VI-A |
| 副标题 | ASR 为 ≤15 次实测搜索后的成功 | §III-B 式（8）；§IV-C3；§VI-A “T_max = 15” |
| 01 路线图 | 两代理不同路线、未触达记为安全 | §I “Insufficient Test Coverage”、图 1（**自绘示意**，非原图） |
| 02 PMR | 13.3 / 12.0 / 22.9；12.0 / 10.8 / 15.7；4.8 / 3.6 / 6.0 | 表 II |
| 02 注 | 专家点 = 安全背景标注者跑良性任务后手选；跨代理分组；残余来自同代理重跑换路 | §VI-B |
| 03 流水线 ①–⑥ | 自动渗透 + 人工指定内容位置；轨迹记录与过滤；Rel / Crit / Expl 1–5 等权；5 策略 × 4 风格（按载体剔除）；GPT-5.4 语义 / 视觉预筛、LLM 四级评分、k = 3、m = 2；成功即停、写入经验记忆 | §IV-B2、§IV-B3、§IV-C1–C3、式（9）（10）；§VI-A 实现细节；附录 A、B |
| 03 权限带 | 设计时 root + 完整轨迹；部署时无权限第三方；排除悬浮窗；监控 APK 叠加模拟 | §III-A、表 I；§IV-B1 |
| 04 ASR | 表 III 五方法 × 三代理（6.8 / 8.0 / 34.5 … 85.1 / 86.3 / 85.1） | 表 III |
| 04 迭代列 | 静态模板“无”（检索模板替换变量）、零样本“单次 LLM 调用”、三种迭代方法 ≤15 | §VI-C 基线描述；§VI-A |
| 04 注 | 所有方法共用 MobileProbe 注入点 | §VI-C “All methods share the injection points selected by MobileProbe” |
| 05 消融 | 85.1 / 76.3 / 63.9 / 28.5；轮数 7.9 / 11.4 / 12.8 / — | 表 VI |
| 05 表 | C 88.9 / 88.9 / 85.2；I 91.7 / 89.3 / 89.3；A 75.0 / 81.0 / 81.0；单 / 跨 app 77.8 / 90.8、82.4 / 89.4、75.9 / 92.2 | 表 IV |
| 06 判据 | 假弹窗 = 点 Accept（APK 记录）；恶意文本 C / I = 任务程序 + 轨迹 LLM 判断作补充判据；A = MobileWorld 原任务校验失败 | §IV-B4；§V-D |
| 06 条 | BU 54.6 / 56.6 / 26.5；失败 45.4 / 43.4 / 73.5；可用性 ASR 75.0 / 81.0 / 81.0；ASR-F 90.3 / 97.2 / 87.4 | 表 V；表 IV；失败比例 = 100 − BU（**我们计算**） |
| 06 “我们的阅读” | ASR-F 的“与能力无关”解释对恶意文本可用性实例不成立 | **我们的阅读**，依据 §V-D 可用性判据与 §VI-D ASR-F 定义 |
| 07 边界 | 无专家点 ASR、无排名翻转；85% 含特权与搜索预算；叠加模拟；2 个基座；LLM 裁判未校验，人评 CA 4.3 / 4.7、CC 3.9 / 3.8、BP 3.2 / 3.4；经验记忆跨任务 | §VI-B–D、图 4 正文；§VII-B；§IV-C3 末段；**部分为我们的阅读** |

## 我们的判断（非原文）

- “85% 是找到率而非被骗率”“表 III 只比载荷生成”“可用性判据混入原任务基线失败”“ASR-F 解释证据不足”“经验记忆的任务顺序未说明”均为我们的阅读。
- 路线图为自绘示意；其余图表按原文数值重绘。
