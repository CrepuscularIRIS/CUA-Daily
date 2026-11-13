# SOURCE — 2611.16107 Trained on What Screen Readers Cannot Read: Accessibility Debt in the GUI Corpora Behind Computer-Use Agents

- 论文：arXiv **2611.16107v1**（cs.HC；2026-11-13 查 export.arxiv.org/api：published = updated = 2026-11-11T23:28:30Z，唯一版本）。作者 Obada Kraishan、Kulsawasd Jitkajornwanich（Texas Tech University）；作者注录用于 AISSA 2026。标题、作者与 corpus.jsonl、本地缓存头一致
- 阅读材料：本地 `research/fulltext/2611.16107.txt`（裁剪 core：摘要、§I、§III–VII）+ arxiv.org/html/2611.16107v1 全文（§I–VIII、表 I–VI、图 1 决策流程、参考文献；无附录）。转换稿在 /tmp/sel15，不提交。图 2 为栅格图，未读像素，所用数字均取自正文与表。未运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-44.jsonl`（L2，supersedes inc-l1-90#2611.16107；P3 confirmed to_l3；q3 judgment；F2,F4；卡 structured_screen_observation、online_evaluation_methodology）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-015.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG/JS）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome（Playwright，`--disable-lcd-text`）渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | AndroidControl 42.7% 需描述元素无 content-desc | §V-B 末句（“still leaving 42.7%”）；= 100 − 57.27 |
| 标题 | 被点 icon-like 多 9 点有描述 | 摘要；§V-C；表 III（+8.99） |
| 副标题 | 17,373,614 元素；Rico 2017、AndroidControl 2024；10/20 分片 | 摘要；§III |
| 副标题 | 两语料之差不是时间变化 | 摘要；§V-B 第 2 段；§VII 末句 |
| 01 流程 | 可见且面积 > 0；Rico 48.7% 节点面积 ≤ 0；labelled / unlabelled / named_by_text / not_applicable；豁免 container、web；分母为 needs | §IV-A；§IV-C 式（1）（2）、图 1 |
| 01 icon-like | 定义与“全部主结论重算” | §IV-D |
| 01 可靠性 | 300 元素；κ .96 角色 / .91 标签状态；分歧 20 中 11 在 not_applicable–unlabelled 边界；自动 vs 人 .96 / .95（标签状态） | §IV-E |
| 01 手机图 | 自绘示意，非论文截图 | — |
| 02 覆盖率 | 17.74 / 57.27；app 聚类 CI [17.14, 18.37]、[55.65, 58.86]；icon-like 33.20 / 62.75 | 表 I；§V-A |
| 02 注 | 需描述 502,585 / 1,462,544，有 89,146 / 837,536；差 39.53，app 聚类 [37.81, 41.21]；833 个 app 为示范挑选 | 表 I；§V-B |
| 03 角色 | button 45.28→72.26（h 0.56）、image 9.62→58.42（1.11）、input 2.20→27.21（0.80）、text 4.09→45.52（1.07）、other 26.63→38.91（0.26） | 表 II |
| 03 注 | hint 后输入框 30.99%；Rico 无 hint；占位描述 10.25% vs 1.95% | §V-A 第 3 段；§V-E 变体 E |
| 04 五种规则 | A 39.53、B 39.54、C 29.56、D 37.91、E 40.23 及各自两侧覆盖率 | 表 VI |
| 04 注 | D：320,059 元素改角色，差缩 1.6 点约 4%；E 扩大 | §V-E |
| 05 选择效应 | 54.14/56.88 −2.74 [−3.95, −1.47] 屏内 −0.80；55.90/52.59 +3.31 [2.15, 4.51] 屏内 +1.99；69.96/60.97 +8.99 [7.47, 10.51] 屏内 +3.52 | 表 III |
| 05 “屏间”数 | −1.94、+1.32、+5.47 | **我们计算** = 差 − 屏内（原文只给 icon-like “约 5.5”） |
| 05 注 | 26,205 次点击、3,556,428 背景元素；祖先归属 43.71%；直接命中 +7.43 [5.77, 9.06]；Cliff’s δ 0.176；第一行人群不同 | §III；§V-C |
| 06 率比 | 0.818 [0.783, 0.855]、0.819 [0.740, 0.906]、0.986 [0.895, 1.086]；N 7,615 / 7,407；p = .78；r = 0.80 | 表 IV；§V-D |
| 06 表 | 四切分 episode 364/349/318/401，覆盖率 55.17/56.20/54.78/56.26，步数 5.37/5.77/5.74/5.72；1,432 成员 / 780 episode；V = 0.013 | 表 V；§V-D |
| 06 注意 | 只有人类示范，无代理 rollout | §V-D 第 3 段 |
| 07 限制 1–5 | content-desc 构念；下界；数据集之差；坐标推断（18.42% 无可点祖先）；部署分布假设 | §IV-C 末段；§VII；§III；§V-C 末段 |
| 07 “我们的阅读” | 屏内只占 3.52；RQ1 列联检验视元素独立 | 表 III；§VII 第 3 段 |
| 08 用法 | 数据卡、分层报告、像素侧补充 | §VI-A–C（作者建议，无实验） |

## 我们的判断（非原文）

- “屏间”分量为差值相减所得；“9.0 点中屏内只占 3.52”是对表 III 的读法。
- 所有图表按原文数值重绘；配色（绿 = 有描述，橙虚线 = 欠债）为自定。
