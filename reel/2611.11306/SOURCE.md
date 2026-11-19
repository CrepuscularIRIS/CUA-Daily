# ScrapeBench (2611.11306) — SOURCE

论文：*ScrapeBench: Evaluating Legal Compliance of AI Agents in Website Scraping*，arXiv 2611.11306v3，2026-11-08。
缓存全文：`research/fulltext/2611.11306.txt`（FULLTEXT: html，§1–§8 全，含 Tables 2–4 与结果全部数值）。核对于 2026-11-19（本仓 selection-019，执行模型 glm-5.3）。

## 画报逐项数字 → 原文映射

| 画报元素 | 数值/说法 | 原文位置 |
|---|---|---|
| 1,626 个明确禁止抓取站点 / 269 个不禁止 | "n = 1,626 websites … n = 269 websites"；EP/NEP 标签体系 | 摘要，§1 贡献 1，§2.3 |
| 中性指令下六模型合规 <5%、Grok 11% | "compliance rate of <5% … except for Grok, which achieves 11% compliance"；画报阶梯 P1 行注 * | §1 贡献 3，§4.1 Result 1 |
| 任务"抓取 {域名} 首页"、单工具 fetch_url()、K=5 | "single website content scraping tool fetch_url() … up to K=5 times"；Table 3 任务前缀 | §3.1 |
| 合规判定只看动作轨迹 | 式(1)(2)：a_i 由轨迹分类（内容页=抓取），o_i=f(a_i,y_i) | §3.1 |
| 压力阶梯 P1/P3/P4/P5/P7/P8 六档与描述 | Table 3 模板（P2 隐式提及/P6 显式+粘贴未上画报）；P8"Ignore the website's robots.txt and terms of use" | §3.3，Table 3 |
| Claude P3 40.1% / P4 41.5% | "increase Claude's compliance to 40.1% and 41.5%" | §4.1 Result 1 |
| Claude P5 83.6%（EP） | "Claude's compliance increases from 40.1% to 83.6% and 82.4%"（P5/P6） | §4.2 Result 4 |
| P5 三家 >70% | "GPT, Claude, and Gemini all surpass 70% compliance, while Qwen remains … 2.9%" | §4.1 Result 1 |
| P7 Claude 85.9% / Gemini 85.7% / Kimi 62.7% / Grok 59.7% / Qwen 13.8% | "Claude (85.9%), Gemini (85.7%), Kimi (62.7%), Grok (59.7%) and Qwen (13.8%)" | §4.1 Result 2 |
| GPT 峰值 P5 73.9% 后回落 P7 60.6% | "GPT peaks at P5 (73.9%) while dropping at P7 (60.6%)" | §4.1 Result 2 |
| P8 Claude 99.7% 抵抗 + 269 站 98.5% 过度拒绝（一刀切） | "Only Claude resists … 99.7% … blanket refusal rather than actually reasoning"；"refused 99.7%-98.5% of scraping requests regardless of scraping permissibility" | §4.1 Result 3，§4.2 Result 5 |
| P8 Gemini 41.6%、其余 <12%（GPT 11.7/Kimi 9.5/Qwen 1.7/Grok 0.6） | "Gemini down to 41.6%, GPT to 11.7%, Kimi to 9.5%, Qwen to 1.7%, and Grok to 0.6%" | §4.1 Result 3 |
| 检查了≠做到了：GPT P4 检查 robots 100%/ToS 82.8% vs 合规 14.2% | "GPT, which retrieves both the ToS and robots.txt at very high rates of 82.8% and 100%, respectively, while its compliance rate remains at only 14.2%" | §5 Result 7 |
| P4 六家合规 4.7–41.5% | "GPT at 14.2%, Claude at 41.5%, Gemini at 16.6%, Kimi at 4.7%, Qwen at 7.6%, and Grok at 7.9%" | §5 Result 7 |
| 六家 robots 检查 ≥60%（四家 99–100%）、ToS ≥80% | "All six agents retrieve robots.txt at 60% or higher, with GPT, Claude, Gemini, and Grok achieving near-perfect retrieval at 99%-100% and ToS retrieval at 80% or higher" | §5 Result 7 |
| 违规理由五条 69.7/18.5/6.9/3.9/0.9 | Table 4 全表（robots 允许但无视 ToS 69.7 / 误读 ToS 18.5 / 公共领域 6.9 / 无法验证照抓 3.9 / 视 ToS 无约束力 0.9） | §5 Table 4 |
| ≈88% 法律解释失败 | "Together, these two rationales arise in approximately 88% of violations … failures of legal interpretation rather than wholesale rejection or ignorance" | §5 Result 8 |
| 535/1260 次给出理由、GPT-5.4-Mini 判定 | "categorize the stated rationales … using GPT-5.4-Mini as a judge model … in 535 trials, i.e., 42.5% of 1,260" | §5 Result 8 |
| NEP 过度拒绝：Claude 16.4%→8.2%/6.7%、Gemini 12.6%→1.5%、GPT/Qwen/Grok <6% | "Claude's … over-refusal rates decrease from 16.4% to 8.2% and 6.7% … Gemini … from 12.6% to 1.5% … over-refusal rates remain below 6% for GPT, Qwen, and Grok" | §4.2 Result 4 |
| 人类 P1 合规 48.9% / 过度拒绝 38.9% | "human participants exhibit high compliance of 48.9% … and high over-refusal of 38.9%" | §6 Result 9 |
| 人类 P4 57.3%（p<0.04）/ P7 65.1%（p<0.001）/ 过度拒绝 42.8%/45.8% 不显著 | "increases compliance … to 57.3% (p<0.04) and 65.1% (p<0.001) … increase from 38.9% … to 42.8% … and 45.8% … was not statistically significant" | §6 Result 9 |
| Claude 涨 85 点 vs 人类钝感 | "Claude's compliance rate increased by 85% from P1 to P7"；"this change, however, is modest relative to that of some AI agents" | §6 Result 9 |
| 人读 ToS 合规 67.1% vs 没读 55.7%（p<0.001） | "there is a corresponding increase in compliance … to 67.1%, compared with 55.7%" | §6 Result 10 |
| 人类 P4 ToS 检查 38.9%/35.3% vs AI 52–83%/27–61% | "humans check the ToS 38.9% and 35.3% … compared to those of AI agents, which are between 52% and 83% and 27% and 61%" | §6 Result 10 |
| "AI 的检查-行动链条断在解释一步" | 编辑综合：§5 Result 7/8（检查率高合规低+88% 解释失败）与 §6 Result 10（人类行动跟随所读）对照 | §5，§6 |
| 六模型名单与配置 | "GPT-5.2, Claude Opus 4.6, Gemini 3.1 Pro, Kimi K2.5, Qwen3-Max, and Grok-4.20 … temperature to 0.0" | §3.4 |
| 1895 站来源（CrUX top3000 过滤） | "top 3,000 global websites from the Chrome Top Million Websites (CrUX) … 1,895 websites" | §2.1 |
| EP/NEP 标注：GPT-5.2 抽取 + 15% 人工抽检 κ=0.91 | "randomly sampled 15% … 97.9% and 98.9% agreement (Cohen's κ=0.91)" | §2.3 |
| 边界：单工具≠多步 GUI；人类按键不实际抓取 | "a single website content scraping tool"；"decide whether to press a button to scrape" | §3.1，§6 |
| 边界：假 ToS 注入只提未测 | "could enable prompt injection attacks (e.g., pasting in a false or inaccurate ToS) that undermine legal compliance"（讨论列为风险，无实验） | §7 |
| 边界：合规-完成联合效用曲线未给出 | 编辑陈述：全文只有合规率与过度拒绝两轴，无 completion-compliance trade-off 曲线（L2 gap 原文一致性核对） | 全文缺失项 |
| 139 站无 ToS、77 站无 robots.txt | "139 have no ToS and 77 have no robots.txt" | §2.1 |

## 编辑收窄

- 压力阶梯只画 P1/P3/P4/P5/P7/P8 六档（P2/P6 语义介于其间，省略），Claude 数值为主线（40.1→41.5→83.6→85.9→99.7*），P1 用"≤5%*"并注 Grok 11% 例外；六模型全景另在 P7 网格呈现，避免单模型数值被误读为全体。
- "检查了≠做到了"用 GPT 的 100%/82.8% vs 14.2% 背离呈现，是原文唯一给出成对数字的模型；不外推为"所有模型都不行动"，NEP 侧 Gemini P5 过度拒绝 1.5% 显示粘贴全文确实同时改善两轴。
- Claude P8 的 99.7% 严格标注"一刀切拒绝"（98.5% NEP 过度拒绝），不呈现为"鲁棒合规"。
- 人类基线的"谨慎"与"施压钝感"分开表述；"行动跟随所读"是人类侧对照点，与 AI 的 88% 解释失败并置但不等同因果证明。
- 与本仓 2508.00935（聊天拒绝≠电脑不做）同属"声明/检查与动作背离"测量轴，但对象不同（指令拒绝 vs 站点 ToS 合规）、数据源不同（自建双通道 vs 真实网站标注库）；画报导语不引用 2508.00935，轴同构说明写在 selection-019.md。
