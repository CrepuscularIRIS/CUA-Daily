# SOURCE · 2604.00073 Terminal Agents Suffice for Enterprise Automation

- 版本：arXiv 2604.00073v4（arXiv HTML 页头 "v4 [cs.SE] 14 Oct 2026"）。本地缓存 `research/fulltext/2604.00073.txt` 标 v4，但在 §5.3 和 Limitations 处截断、不含附录；附录 A/B/C.1/C.2/D/E/I/J 和 Limitations 全文取自 `https://arxiv.org/html/2604.00073`（临时存 /tmp，不提交）。主表数字在缓存和 HTML 两处一致。
- 作者：Bechard 等（ServiceNow）。
- 初筛记录：`research/scoring/runs/gui-pc11-20261022-01/batches/l106.jsonl`（L2，P3 confirmed，q3 judgment，F1/F0，主卡 planner_grounder_interface）；入选理由见 `selection3.md` §1 第 1 行。
- 画报源文件：`poster.html`（单文件、内联 CSS/SVG）；`poster.png`、`poster.pdf` 由 headless Chrome 渲染。

## 数字 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 设置栏 | 729 = ServiceNow 330 + GitLab 192 + ERPNext 207 | §3.3 Table 1 |
| 设置栏 | 成功 = 对最终平台状态的任务级程序化校验；成本 = token 推理费 | §3.4 Metrics |
| 设置栏 | 同一骨干；主对照不开文档和 skills | §3.4 Experimental design |
| 设置栏 | 729 题总体 SE ≈ 1.5 点（SR 约 80% 时） | 附录 A |
| 矩阵 Sonnet 点/卡 | Tool 32.9%/$0.51；Web 72.2%/$3.29；Terminal 72.7%/$0.56 | §4.1 Table 2 Overall |
| 矩阵 Opus 点/卡 | Tool 39.2%/$0.58；Web 79.9%/$3.97；Terminal 78.7%/$1.22 | Table 2 Overall |
| 矩阵 Hybrid | Sonnet 72.0%/$1.94；Opus 81.4%/$2.22 | §4.3 Table 3 Overall |
| 矩阵 api_call 虚圈 | Sonnet 73.5%/$0.15；Opus 79.2%/$0.25 | 附录 C.2 Table 5 |
| 矩阵底栏 | GPT-5.4 Web 73.4%/$0.43 vs Terminal 73.5%/$0.19；Gemini Web 68.9%/$0.69 vs Terminal 77.5%/$0.09 | Table 2 Overall |
| 成本倍数 ×5.9 / ×3.5 / ×0.9 / ×3.3 / ×1.8 / ×0.5 / 2.3× / 7.7× / 1.3–11.3× | 本页按 Table 2/3 成本相除（我们的算术，非原文给出） | Table 2、Table 3 |
| ERPNext×Opus ≈ 9× | $6.49 vs $0.72 | §4.1 正文 |
| 标题副句"3 个骨干只差约 1 点 0.5/1.2/0.1" | Sonnet/Opus/GPT 的 Web−Terminal 差；Gemini 差 8.6 点 | Table 2；§4.1 "within about a point for three of the four models" |
| 工具面板 | 可行子集 444 题（120/127/197），Sonnet ServiceNow 工具代理 11.5→24.2% | 附录 C.1 Table 4 |
| 工具面板 | 单一 api_call(method,path,body,query)，无 shell/文件系统；Sonnet 73.5% $0.15 | 附录 C.2 Table 5 |
| 混合面板 | ServiceNow：Terminal 独解 55、Web 独解 51，oracle 89.1%；Sonnet SN Terminal 73.6 / Web 72.4 / Hybrid 72.1，Hybrid $3.02；Opus Hybrid SN 83.0% $2.57 | §4.3 正文与 Table 3。89.1% = (243+51)/330，与 Sonnet 的 73.6%（243 题）对得上，可确认是 Sonnet 运行 |
| 混合面板 | 路由靠基座模型隐式判断，偏向浏览器 | Limitations "Hybrid agent routing" |
| 浏览器面板 | 18 类中 7 类显著（终端 4、Web 3），四骨干不加权平均，配对精确 McNemar | 附录 D Table 9 及正文 |
| 浏览器面板 | Impersonation n=10 Web 95.0/Term 0.0；GitLab Social n=49 81.0/71.1；SN Form Creation n=50 67.0/89.0；ERPNext Composite n=25 57.0/71.0 | 附录 D Table 9 |
| 浏览器面板 | Web token 在除一类外各类多 1.5–20.8×（例外为 SN 排序） | 附录 D 正文 |
| 限制 | 单会话、单平台、短流程；Flow Designer 不在题集 | Limitations；§5.1.2 |
| 限制 | 重复 3 次仅 SN×Gemini、GL×GPT-5.4，SD 0.5–1.4 / 1.9–2.2 点 | 附录 A |
| 限制 | SN 上 Sonnet/Opus 终端领先 1.2/1.5 点"不是范式差异的证据" | §4.1 |
| 限制 | 只校验所请求状态存在；终端代理 31% 写请求被拒、多为重试 | Limitations；附录 E |
| 限制 | 现成 MCP server（7–83 个工具） | §3.3；Limitations |
| 限制 | 墙钟 Sonnet Web 123 s / Terminal 53 s（729 总体） | 附录 I Table 12 |
| Web 卡 | Playwright MCP，21 个工具，含 a11y 快照、截图、JS 执行；提示先检查后验证 | §3.1；附录 L、N |

## 示意与阅读判断

- 自绘：四个接口图标、对角虚线、$1.5 / 55% 象限分界、等效果色带，均为示意，不是原文图。数据点位置按 Table 2/3/5 的数值在对数成本轴上绘制。
- "我们的阅读"栏是本项目判断，不是作者结论。
- 未运行论文代码，未复现。
