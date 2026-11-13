# selection-015 — gui-rolling-20261023-01（第十五期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-11-13，本仓第十五期（单席串行）
- 不再入选：前十四期 45 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`–`selection-014.md`，`reel/README.md`）。本期 3 篇候选均不在其中
- 依据：本 run 最新 L2 记录 `batches/inc-l2-43.jsonl`（2611.12918，supersedes inc-l1-89）与 `batches/inc-l2-44.jsonl`（2611.16107、2611.16693，supersedes inc-l1-90）。三篇本地缓存均为裁剪 core，全部从 arxiv.org/html/<pid>v1 补读全文与附录。转换稿在 /tmp/sel15，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 候选池（总控清单 3 篇）：逐篇核对为该 paper_id 的最新记录，均为 P3 / confirmed / to_l3
- 日期：2026-11-13。之后新增的 L2 或 correction 不计入本期

## 候选池（3 篇）与处理

全部 P3，q3 全为 judgment；族均为 F2,F4。三篇都是评测 / 审计类，按问题族多样性看：一篇离线网页动作预测协议，一篇移动语料观察字段，一篇移动注入攻击的暴露可比性。

标注：J = judgment；“读”列 = 本期读到的范围（全文 = 正文 + 可得附录）。

| ID | 简称 | tier | q3 | 族 | 主卡 | 读 | 处理 |
|---|---|---|---|---|---|---|---|
| 2611.16107 | Accessibility Debt | P3 | J | F2,F4 | structured_screen_observation / online_evaluation_methodology | 全文（v1 §I–VIII、表 I–VI；无附录） | **入选** |
| 2611.16693 | MobileProbe | P3 | J | F2,F4 | environmental_injection_attacks / online_evaluation_methodology | 全文（v1 §I–VIII、表 I–XI、附录 A–G） | **入选**（按 L2 收窄范围呈现） |
| 2611.12918 | IntentTwin | P3 | J | F2,F4 | online_evaluation_methodology | 全文（v1 §1–5、附录 A–E） | **correction C-015-1**，本期暂停 |

版本复核：2026-11-13 查 export.arxiv.org/api，2611.12918 最新 v1（2026-10-27）、2611.16107 最新 v1（2026-11-11）、2611.16693 最新 v1（2026-11-12），与读取版本一致。

## 1. 最终入选（2 篇）

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2611.16107 Accessibility Debt | J / F2,F4 | structured_screen_observation / online_evaluation_methodology | 改变一个数据判断：代理训练与评测用的无障碍树里，“目标叫什么”这一栏有多空、示范是否偏向好认的目标。17,373,614 个元素，覆盖率 Rico 17.74%、AndroidControl 57.27%（app 聚类 CI 不重叠，表 I）；输入框最低（2.20 / 27.21，hint 后 30.99，表 II）；五种编码规则下差距 29.56–40.23、不翻转（表 VI）；同屏比较中被点 icon-like 多 8.99 点有描述，屏内选择 3.52（表 III），直接命中仍 +7.43；描述密度与示范长度在固定暴露后无关（IRR 0.986，表 IV）。编码可靠性 κ .96 / .91。限制写进画报：只测 content-desc，不是“读得出”；覆盖率为下界；两语料之差不是时间趋势；没有代理 rollout；坐标推断目标；只解析 10/20 分片 |
| 2 | 2611.16693 MobileProbe | J / F2,F4 | environmental_injection_attacks / online_evaluation_methodology | 改变一个评测判断：固定注入点会把“没走到”记成“防住了”。83 个移动端攻击实例 × 3 代理 × 3 次，专家固定点 PMR 13.3 / 12.0 / 22.9%，跨代理点 12.0 / 10.8 / 15.7%，按本代理良性轨迹选点 4.8 / 3.6 / 6.0%（表 II）。**编辑理由**：environmental_injection_attacks 卡已有四张 Reel（2610.41272、2611.04879、2611.04393、2611.11971），但都在网页端、都测攻击或防御本身；本篇是首篇移动端、首篇把“暴露是否可比”单列测量的。画报按 L2 的收窄口径呈现：标题只用表 II；85% ASR 标为“≤15 次实测搜索下的找到率”，表 III 写明只比载荷生成、前两行无迭代；可用性判据混入原任务基线失败（BU 26.5–56.6）、LLM 补充判据占比未报告、无专家点 ASR / 排名翻转、经验记忆顺序未说明，全部写进画报 |

族覆盖（本期）：两篇都是 F2,F4。卡覆盖：structured_screen_observation 第三次（2610.31698 测工具层不核对就交状态、2610.35237 测视口外目标，本篇测语料观察字段完整性与示范选择偏差，不同题）；environmental_injection_attacks 第五次（理由见上）。年代：两篇均为 2026-11。

## 2. 排除与暂停

| ID | 处理 | 理由 |
|---|---|---|
| 2611.12918 IntentTwin | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节 C-015-1。L2 依据的“既有离线网页基准存在候选 support 泄露”在原文中只在作者自建的 16 选 1 构造上成立（SIR = 1 是构造的必然结果）；Mind2Web 表 5 无方法说明，且与附录 C 的“未运行候选元素排序”说法冲突 |

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2611.16107 | v1 全文 §I–VIII、表 I–VI、图 1 决策流程（图 2 未读像素） | 同意 P3/confirmed。**补注（不退回）**：(a) §II-B 已列 Ross、Fok、Alshayban、Chen 等 Android 缺标签审计，新颖处是“对象为代理语料 + 示范选择效应”，L2 未写成“首次发现缺标签”，口径正确；(b) 表 III 第一行（−2.74）两组人群不同，作者明言不据此下结论；(c) “报告成功率偏乐观”依赖作者自承无法检验的部署分布假设 |
| 2611.16693 | v1 全文 §I–VIII、表 I–XI、附录 A–G（图 1–5 未读像素） | 同意 L2 收窄后的 P3/confirmed（固定点覆盖不足与按轨迹选点减少漏测，表 II）。**补注（不退回）**：(a) L2 fact 称最终完成由程序核验——§IV-B4 另设“轨迹 LLM 判断”作补充判据，占比未报告；(b) 可用性目标成功 = 原任务校验失败（§V-D），原任务基线失败 43.4–73.5%（表 V），恶意文本类可用性实例的 ASR、ASR-F 混入基线失败，作者“ASR-F 证明与能力无关”的解释证据不足；(c) 无专家点 ASR 与排名翻转，“低估风险”的直接证据只有 PMR；(d) 表 III 前两行无迭代、后三行 ≤15 次；(e) 经验记忆跨任务累积，任务顺序与留出未说明。子卡 C33 “When it fails” 补读后仍 unknown。不改档位，请巡检班下次触及时把 (a)(b) 记入 biggest_gap |
| 2611.12918 | v1 全文 §1–5、附录 A–E（表 1–33） | **correction C-015-1** |

## 4. correction / 待补

### C-015-1　2611.12918v1 IntentTwin（退回 Sol 单篇修订，保留旧记录）

旧记录：`batches/inc-l2-43.jsonl`（supersedes inc-l1-89#2611.12918），P3 / confirmed / to_l3；q1 measured_own，q2 open_failure，q3 judgment，q4 fits；卡 main/online_evaluation_methodology；problem_statement 为“离线 Web 动作预测在保证金标进入候选、负例仅从训练 support 抽取时，候选 support 成员身份是否泄露目标，且 oracle reranking 与部署时无目标候选生成之间有多大差距”；card_anchor 写“Q2 只对照首版前 OPeRA 和 Mind2Web 等既有协议的此项未控制条件”。L2 时缓存不含附录。

- **错误点**：
  1. **“原协议”是作者自己的构造，不是已发布基准的协议**。§3.1 描述的是本文的 builder（“The builder deduplicates the train action vocabulary… 15 deterministic negatives are drawn from that vocabulary”），并说明部分产物保留“historical ‘IRL’ label”、附录 A.1 称“legacy factorized scorer”。OPeRA 原文（2506.05606）的基准是下一动作预测，本文没有指出 OPeRA 或任何已发布基准使用“训练词表抽负例 + 插入金标”的 16 选 1 构造。摘要首句“Offline web-behavior benchmarks frequently insert…”没有引文支撑。因此 OOV 行 SIR = 1.0000、support-only 规则 1.0000 是该构造的必然结果（§4.2 自述 “by construction”），证明的是一个自建协议的缺陷，不是领域内既有协议的测量。L2 的 q1 measured_own 与 q2“既有协议未控制此条件”超出了原文证据。
  2. **Mind2Web 结果没有方法，且与附录自相矛盾**。表 5（§4.6）报告三 split 的 SIR、oracle、proposal R@16、covered、E2E，但正文没有说明 Mind2Web 上的训练 support、候选构造、排序器与 proposer。附录 C 表 21 把 Mind2Web 只列为“target-free action-type probe; non-claimable transfer”，并在 §C.1 末写明 “candidate-element ranking, an official MindAct comparison, and online browser validation were not run”。L2 facts 第 2 条把表 5 当作分层结果引用，是唯一能支撑“已发布基准也有此混淆”的证据，而它的来历不明。
  3. 附录显示多项实验仍在进行（表 21：“A0/A1 artifact gate in progress; A7/A8 pending”；分段标签“external human labels pending”），384-token 评测下同一适配器只有 0.3737（表 15），1,024-token 截断 0.0968（表 18），说明管线对评测设置非常敏感；L2 只提到表 4 局部文字错误。
- **请 Sol 复核**：(a) q1 是否应改为 `asserted`（领域层面）——自建构造上的 SIR 只能算“自身设置的测量”；按封顶规则档位最高 P2，`evidence_status` 改为 `pending_material`（需作者说明 Mind2Web 表 5 的协议，或指认使用该构造的已发布基准）；(b) q2 是否应为 `unknown`，card_anchor 去掉“既有协议未控制”的表述；(c) facts 第 2 条注明表 5 无方法、与附录 C 冲突；(d) 若认为本文主体价值是“oracle 候选 vs 无目标 proposal 的分解报告”，可另按 incremental 判断。
- 本期不入选，不制作画报。

### 待补清单

沿用 selection-014 第 4 节，状态未变。本期候选池以外，巡检记录里 2611.15097、2611.16744（pending_material）与 2611.14326（缺关键附录）仍待巡检班补材料，不在此处直接入选。C-013-1 已由 Sol 修订（P3→P2，见 progress.md 2026-11-11）。

## 5. 漏检抽查结果

本期没有新增抽查。

## 6. Reel 成品路径

各目录含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。实际打开渲染图做视觉 QA；DOM 探针核对卡片越界、SVG 文本越框、最小有效字号与内容底边；PDF 以 40 dpi 栅格化后与 PNG 对照，兼作约 580 px 宽小屏检查。Playwright 驱动本地 Chrome，`--disable-lcd-text`。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2611.16107 | `reel/2611.16107/` | 炭黑页眉 + 读屏焦点绿框徽记 + 自绘手机界面（绿框 / 橙虚线）+ 覆盖率进度条（欠债橙底）+ 分角色哑铃 + 五规则条 + 被点 vs 背景“屏内 / 屏间”堆叠条 + 率比森林图 + 切分表 | ready（三次渲染：CI 文字越界、hint 标签互压、差值截断、留白约 170 px；逐次修正） |
| 2611.16693 | `reel/2611.16693/` | 深色底 + 两代理路线分叉示意 + PMR 点阶梯 + 六段流水线与“设计时 / 部署时”权限带 + 五方法分组横条（带迭代列）+ 消融条 + 三判据卡 + 基线失败分段条 | ready（四次渲染：判据卡粗体断行、标签被箭头压住、图例截断、标题数字不准、标题孤行；逐次修正） |

索引：`reel/README.md` 新增第十五期一节；`README.md` 头部统计行由 45 改为 47（滚动 run 由 26 改为 28）。poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git、未写 progress.md（由总控记录）。
