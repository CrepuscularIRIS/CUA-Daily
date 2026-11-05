# SOURCE — 2611.04393 Voluntary Servitude: Weaponized Safety Warning Mechanisms for Controlling AI Agents

- 论文：arXiv **2611.04393v1**（2026-11-03；2026-11-05 查 export.arxiv.org/abs 只有 v1）
- 阅读材料：本地 `research/fulltext/2611.04393.txt`（文件头 v1，裁剪 core，跳过 §2、§7 尾部截断）；按钉定版本补读 arxiv.org/html/2611.04393v1 全文 §1–7 与 App. A–F（表 1–8；图 4、5、6 从原文 SVG 渲染后读数，图 7 只读说明与 App. D 表）。App. F 的判官提示词正文在 HTML 中未展开，只读到说明段。转换稿在 /tmp/sel10，不提交。没有访问作者的投毒页面，没有运行代码
- 初筛记录：`research/scoring/runs/gui-rolling-20261023-01/batches/inc-l2-18.jsonl`（L2，supersedes inc-l1-23#2611.04393；P3 confirmed，q1 measured_own，q2 open_failure，q3 judgment，q4 fits；F4/F2；卡 main/environmental_injection_attacks、main/injection_defense_isolation；子卡 C30、C33、C34）
- 入选：`research/scoring/runs/gui-rolling-20261023-01/selection-010.md` 第 1 节
- 画报源：`poster.html`（手写静态 HTML + 内联 SVG，可直接编辑）；`poster.png`（1400×2000）与 `poster.pdf`（1 页，1050×1500 pt）由本地 Chrome headless 渲染

## 数字与断言 → 原文

| 画报位置 | 内容 | 原文 |
|---|---|---|
| 标题 | 一条伪造安全隐患评论、无命令；代理自己排除正规商家改推攻击者；检测器放行 | 摘要；§1 第 6 段；§3 “Payload structure”；§5.1 表 1 |
| 副标题 | 1/4 评论属攻击者、整页一次交给模型 | §4 “Datasets”、“Exposure” |
| 副标题 | 60.4% vs 66.0% | 表 1“No filter”列；摘要 |
| 副标题 | 1.7–4.4 倍 | §1 末段、§5.1；表 1：60.4/35.7=1.69，47.1/10.6=4.44（我们复算） |
| 副标题 | 68.4% → 3.6% | §6 表 3 “All three” |
| 副标题 | 浏览器 4 个产品各 20 次；无下游动作 | §5.3 “Browser agents”；§3 “Attacker objectives”（success measured at the selection）；§7 Limitations |
| 01 左图 | 四段式评论结构；只有“主张”在族间变化；无对模型的指令 | §3 图 3 与 “Payload structure”；App. B.1 安全族例（急症时丢下、拒不退款、掩盖，LocalGems 受过急救与特殊需求培训）。**示意重画，非原图** |
| 01 右表 | 三族与三种对照、指令注入基线 | §3 “Payload structure”；§4 “Baselines” |
| 01 右表 | 固定评论数、位置、密度、同一 payload；10 领域 × 50 查询；虚构目标 | §4 “Datasets”、“Baselines” |
| 02 | 放行率 100/54/100（ProtectAI）、78/16/100（Lakera）；有效 60.4/35.7/8.2、47.1/10.6/8.2；真实评论 100/92 | §5.1 表 1 |
| 02 标题 | 表 1 为 4 个模型的匹配对照运行 | App. C 表 4（“Misconduct control, injection baseline” 行为 Haiku、Grok、Gemini、DeepSeek V4）；图 5 四模型安全族值均值 =(85.2+82.6+51.0+22.8)/4=60.4（我们复算） |
| 02 标题 | 有效 = 未过滤 × 放行率，乘积估算 | §4 “Metrics” |
| 02 注 | payload 未针对检测器调过；表 1 未报权威、属性两族放行率 | §4 “Metrics”；表 1 行列表 |
| 03 左图 | 安全 85.2/82.6/51.0/22.8，失当 0.8/21.2/11.0/0.0，只夸 6.8 虚线 | 图 5（fig2_hazard_vs_accusation.svg，渲染读数） |
| 03 左注 | 只夸攻击者 6.8% 来自 3 模型池 | App. C 表 4（“No-poison, benign-positive” 行为 Haiku、Grok、Gemini） |
| 03 左注 | 无投毒 0.7% | §5.2 “What triggers elimination” |
| 03 左注 | 表 2：4/6 个模型上属性族原始成功率最高，安全族只在 Haiku 上最高 | §5.2 “Across models”（Attribute claims reach the highest raw success on four of the six）；表 2 逐行核对：属性族最高为 DeepSeek V4 Flash、DeepSeek R1 8B、Llama 3.3 70B、Grok 4.3，Gemini 上权威族最高，Haiku 上安全族最高 |
| 03 右图 | 成功样本中“排除”占比 6 模型 × 3 族 | 图 4（fig3_elimination_share.svg，渲染读数）；§5.2 “Elimination and comparison”（97–99%、70–75%、≤64%、≤28%） |
| 03 右注 | 判官 Llama 3.3 70B；人工 100 条，类别 90%（κ=0.742），路径 κ=0.479 | §4 “Metrics” |
| 04 左 | Edge 100/20、Comet 60/0、Codex 20/0、Brave 100/100；每攻击 20 次 | 图 6（fig4_browser_agents.svg）；§5.3 |
| 04 左注 | 作者自建虚构页面；只看推荐；浏览器上无失当对照与防御 | §5.3；App. A（页面虚构、离线）；§6（防御只在 3 个 API 模型上评） |
| 04 右表 | 命中率 / 条件成功 / 端到端 | App. D.1 表 5（条件成功取整：61.8→62、51.4→51） |
| 04 右注 | 两领域、9–10 页里 2 页带毒、Gemini 3.1 Flash Lite、50 查询；49–66% | §5.3 “Retrieval”；App. D.1 |
| 攻击要多少 | 4/120 条 74% vs 32 条 78%（p=0.82），单领域、2 模型各 25 查询，Gemini 近饱和 | App. D.2 表 6 |
| 攻击要多少 | 位置损失 ≤9.8 点、页中最弱 | §5.4；App. D.4 表 8（Haiku 22.8→13.0） |
| 攻击要多少 | 刷赞对安全族 ≤3.4，三族最大 7.0 | §5.4；App. D.5 |
| 攻击要多少 | 82.7 → 84.9 | App. D.3 表 7 |
| 05 图 | 引用隐患 99.8→98.4、排除 90.9→4.0、选中 68.4→3.6（95% CI 2.2–5.7） | §6 表 3 与正文 |
| 05 注 | Grok 64.7→0.7、Haiku 52.7→1.3、Gemini 88.0→8.7 | 表 3 |
| 05 标题 | 3 模型 × 3 领域 × 50 = 450；非自适应 | §6 第 2、5 段 |
| 防御提示 | “安全指控须有独立佐证才能据此排除” | App. E 原文转述 |
| 限制 | 整页单次推荐、无执行检查 | §3、§4 “Exposure”；§7 Limitations |
| 限制 | 乘积估算 | §4 “Metrics” |
| 限制 | 非自适应、真实隐患代价与伪造佐证未测 | §6 末段；§7 Limitations |
| 限制 | 两类指控未做严重性/可信度匹配；无后训练阶段对比 | §4 “Baselines”（只说明槽位一致）；§7 Limitations（checkpoint study 留作未来）；L2 facts |
| 限制 | 旅游类、单一虚构目标、温度 0；浏览器每格 20 次 | §4；§5.3 |
| 我们的阅读 | “注入 = 命令”的防御假设 | §1 第 3–4 段；§7 Broader impact。为我们的归纳 |

## 原文内部出入与口径

- L2 facts 记“表 2 六模型安全族等权均值约 66.0%，与表 1 的 60.4% 不一致”：已解。表 1 的 60.4/8.2 是图 5 四个模型（Gemini 3.1 FL、DeepSeek V4 Flash、Grok 4.3、Haiku 4.5）匹配对照运行的均值（85.2、82.6、51.0、22.8 → 60.4；0.8、21.2、11.0、0.0 → 8.25），与 App. C 表 4 的模型覆盖一致；表 2 的 6 模型安全族均值 66.03 与表 1 指令注入的 66.0 数值相同属巧合。两次运行的同一模型数值略有差别（Gemini 表 2 为 86.5、图 5 为 85.2），原文未说明是否为不同运行；Gemini/Grok/Haiku 的图 5 值与表 8“Top”列相同。
- §5.2 用 Fisher 检验比较失当指控 8.2%（4 模型池）与只夸攻击者 6.8%（3 模型池），两组模型集合不同。在共有的 3 个模型上失当指控均值为 3.9%（我们按图 5 复算），结论“失当指控不比只夸更能推动代理”不受影响。
- 表 1 没有报权威、属性两族的检测器放行率；§5.1 “安全族是唯一既过检测器又推得动代理的条件”只对表 1 所列条件成立。

## 示意与自绘

- 01 左图评论页为按 §3 图 3 与 App. B.1 文字重画的示意，地名、商家用占位，不是原文截图。
- 其余条形、点线与表格由我们按原文表格与图中数值绘制。
