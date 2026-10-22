# SOURCE · 2310.03720 SteP: Stacked LLM Policies for Web Actions

- 版本：arXiv 2310.03720v4（2024-08-08 更新；首发 2023-10-05；COLM 2024）。作者 Paloma Sodhi、S. R. K. Branavan、Yoav Artzi、Ryan McDonald。
- 材料：本地缓存 `research/fulltext/2310.03720.txt` 是裁剪版，含摘要、§1、§3、§4、§5.1 正文和 §6，缺 §2、表 1 数值、图和附录。表 1、§2、附录 A.1–A.2/B/D 以及图 1、3、7 的 PNG 从 `https://arxiv.org/html/2310.03720v4` 补读，存放在 /tmp，不提交。
- 初筛记录：run `gui-pc11-20261022-01`，selection2.md 第 4 行（P3 / judgment / F5,F0 / agent_loop_context_control）；L1 见 `batches/p003.jsonl`，L2 见 `batches/l60.jsonl`，paper_id=2310.03720。
- 制作：Opus 5.5，2026-10-22。没有运行论文代码，也没有复现实验。

## 数字与断言 → 原文

| 画报内容 | 原文位置 |
|---|---|
| 一个大 prompt 覆盖所有行为会很复杂，并造成无关行为之间的 “behavior leaks” | 摘要；§1 |
| 长历史使模型更难关注要点，错误和成本都会增加 | §1 |
| 控制状态是策略栈 Σ=⟨π₀\|…\|πᵢ⟩；每个策略维护自己的历史；只有栈顶策略行动 | §4.1 State |
| invoke：新策略以空历史压栈，不向环境发动作；stop：出栈，返回值写进父策略历史，同样不向环境发动作 | §4.1 Transition，式 (2)(3) |
| 发出网页动作时，观察结果只追加到栈顶策略的历史里 | §4.1 式 (1) |
| 任一策略可调用任一策略、包括自己；栈深随任务变化 | §1；§4.2 Key features 1 |
| 示例 search_list("&lt;user&gt; commits","repository list") 递归调用 search_list("&lt;user&gt;","commit list") | 图 1 及图注 |
| 网页动作 click [id]、type [id] [value]；stop [response] | §3；§4.2 |
| WebArena 策略库 14 个；策略名 find_commits … search_nearest_place | §5.1 Policies；附录 A.2 列表 |
| 14 个策略覆盖 170 个 intent 中至少 50 个；收益集中在覆盖较多的 Shopping、Reddit | §5.1.2 |
| Flat：把库内所有策略的说明和示例拼进同一 prompt；Flat-4K/8K 把 prompt 上限设为 4000/8000 token | §5.1 Baselines (i)(ii) |
| SteP 每个策略 prompt ≤4K | §5.1.3；表 1 表注 |
| WebArena 模型 gpt-4-turbo（附录写作 gpt-4-turbo-preview），804 题 | §5.1 Environments / Models；附录 A.1 |
| 全量均值：Zhou 0.12、Akter 0.15、Flat-4K 0.20、Flat-8K 0.23、SteP 0.33 | 表 1 末行 |
| 摘要 14.9% → 33.5% | 摘要（对应表 1 的 Akter 0.15 → SteP 0.33） |
| 4K → 8K 只从 0.20 到 0.23（作者用词 “only marginally”） | §5.1.3 |
| 各站点均值（Flat-4K / Flat-8K / SteP）：Shopping 0.28/0.30/0.37，CMS 0.17/0.18/0.24，Reddit 0.17/0.30/0.59，GitLab 0.20/0.23/0.32，Maps 0.20/0.20/0.30；intent 数 48/41/21/41/29 | 表 1 |
| 4K → 8K 退化的 intent：Config 0.20→0.00，Summarize 0.60→0.40，Like submissions 0.50→0.33，Create forum 0.60→0.40；作者解释为 prompt 变大后难以集中注意力 | 表 1；§5.1.3 |
| Flat-8K → SteP 的 intent 级反例：Reply to post 0.60→0.00，Summarize 0.40→0.00，How many reviews 0.60→0.20；Post notice 0.00→0.60 | 表 1 |
| 每个 intent 3–5 题 | 表 1 表注 |
| 平均动作数 Flat-8K 7.25，SteP 10.0 | 表 1 末行 #act |
| 成功轨迹平均输入 token：SteP 22.7K、Flat-8K 52K；约 2.3 倍 | §5.1.4；图 3(b)；§1 |
| 控制权来回交接使模型调用次数增加（未给次数） | §5.1.4 |
| 同示例数（≤7）的提升来自拆分说明，&gt;7 来自各策略专用示例；最多 21 个示例 | §5.1.5；图 7 |
| 图 7 读点：Flat 0/3/5/7 ≈ 0.12/0.30/0.55/0.60；SteP ≈ 0.23/0.38/0.60/0.65，10/12/16 ≈ 0.77/0.77/0.90 | 图 7 PNG 读点（MiniWoB++ 子集） |
| MiniWoB++ 使用 text-davinci-003 | §5.1 Models；附录 A.1 |
| 限制：策略手写；通信开销；信息不足时子策略无法告诉父策略缺什么，可能无尽循环 | §6 (1)(2)(3) |
| 静态层级局限于 2–3 层；DecomP 子程序不能互相调用 | §2 |

## 示意内容（不是论文实验图）

- 策略栈三帧：策略名和参数取自图 1，各帧局部历史里的观察/动作文字（“GitLab 首页”“第 2 页”“找到 3 条”等）是我们编写的。
- Flat 面板：14 个策略名取自附录 A.2；灰条、4K/8K 截断位置和平铺历史的内容都是示意，原文没有说明截掉了哪些策略。
- “两边相同/不同”对照栏是根据 §5.1 Baselines 整理的阅读。
- 图 7 按原图读点重绘，空心点为约数，原文没有给出数值。
- 所有图标和箭头均为自绘。
