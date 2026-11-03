# selection-008 — gui-rolling-20261023-01（第八期）

- run：`gui-rolling-20261023-01`（CUA-Daily 增量轮）；规则 `problem-core-v1.1`（PROBLEM_CORE.md / SELECTION.md）
- 选题与制作：Opus 5.5 L3 选题与 Reel 席，2026-11-03，本仓第八期
- 不再入选：前七期 31 篇（`runs/gui-pc11-20261022-01/selection.md`、`selection2.md`、`selection3.md`，本 run `selection-004.md`–`selection-007.md`，`reel/README.md`）。本期 3 个候选都不在其中
- 依据：本 run 的 L2 记录和**每篇的完整原文**。本地缓存 `research/fulltext/<id>.txt` 都是裁剪的 core（无附录），3 篇都按缓存文件头钉定的 v1 从 arxiv.org/html 补读了全文和全部附录。转换稿放在 /tmp/sel8，不提交
- 不用分数、venue、代码或名气；没有改动任何批次记录

## selection_cutoff

- 记录：`batches/inc-l2-11.jsonl`（3 篇），各自 supersede `inc-l1-12` 的 L1 记录
- 候选池：PROBLEM_CORE 第 4 节 `next_action=to_l3` 中、selection-007 之后新增的 3 篇（全部 P3 + confirmed）
- 同 run 的其他 to_l3 维持前期处理：2610.31274 PointerBench 仍为 selection-004 起的备选；2610.32223、2610.36471、2610.36877 维持编辑排除；2610.40133 已按 C-007-1 修订为 P2/park（`batches/inc-l2-10-rev1-40133.jsonl`），不进池
- 同批不进池：2610.40747（P3/pending_experiment/park）、2610.41432（P2/confirmed/park，L2 未给编辑理由）
- 日期：2026-11-03。之后新增的 L2 或 correction 不计入本期

## 候选池（3 篇）

| ID（钉定版本） | 标题 | tier | q3 | 族 | 卡 |
|---|---|---|---|---|---|
| 2610.41397 (v1) | Cross-Interface Authorization for AI Computer-Use Agents | P3 | capability | F4,F0 | injection_defense_isolation |
| 2610.40798 (v1) | Beyond Plausible Prediction: Safety Sufficiency in Web World Models（SafeWebWorld） | P3 | judgment | F2,F1 | learn_and_train_in_gui_world_model；learned_outcome_and_process_judges |
| 2610.41272 (v1) | ANGLER: Verifier-Grounded Benchmarking with an Adaptive Attacker for Web Agents（REEF） | P3 | judgment | F2,F4 | environmental_injection_attacks |

按 SELECTION.md 排列：全部 P3；capability 1 篇、judgment 2 篇，不分先后。三篇都在“代理动作的授权与安全”一带，但问题不同：
- 41397：同一作用经 GUI/CLI/API/脚本/MCP 多条路径到达持久化处，授权凭证能否跨路径复用（执行层，协议与证明）
- 40798：world model 预测出的未来是否携带做 Execute/Ask/Block 决定所需的信息（决策信号层，离线基准）
- 41272：网页注入攻击的测量与自适应搜索（攻击评测层，在线 rollout）
- **不同题，不做同题去重**。三篇的排除或入选都按各自原文核对结果决定。

## 1. 最终入选（1 篇）

| # | ID | q3 / 族 | 卡 | 入选理由 |
|---|---|---|---|---|
| 1 | 2610.41272 REEF / ANGLER | J / F2,F4 | environmental_injection_attacks | 问题清楚：固定的、单类型的攻击集会低估网页代理的漏洞，而且“点了诱饵”不等于“越权做成”。测量设计是本期最直接的：9 个可重置合成站点、8,316 个用例、5 种送达；恶意验证器在重置态须为假、终止时仍成立才计成功，不用自述、不用 LLM 评审；另记 CTA 与良性任务成功率。同任务、同调度、每站 100 次 rollout 下与“编译器过滤后均匀随机”的 NA 对照：8 骨干平均 ASR 15.24→20.36%（Tab.3），预算 50 时 713 vs 545 次成功；攻击使 BSR 61.9→46.4/44.4%（Tab.4）；弹窗 CTA 52.4% 而 ASR 17.1%（Tab.11）；GPT-6.1 Sol 与 Sonnet 5.5 几乎不点网页诱饵（CTA ≤5.4%）但 DPI 仍有三成以上做成。它改变“没被固定样例攻破＝安全”“诱饵点击率＝劫持率”的评测做法。这张主卡此前在 Reel 中一直空着（selection-007 仍列为空白卡）。限制写进画报：合成站点；每格 100 次、单次运行，只 Qwen3-VL 重复三次且 NA 未重复；Tab.6 的 Full 行就是三次中最高的 Run 1，消融差值落在三次运行的波动内（见第 3 节补注）；GPT-4o 一个骨干占平均增益约 39%（我们计算）；预算只匹配 rollout 数；验证器无误差统计；论文没有局限性一节 |

族覆盖（本期，主族）：F2 ×1；副族 F4。卡覆盖：environmental_injection_attacks 首次入 Reel。selection3 列出的空白卡还剩 mine_human_screen_videos。

## 2. 排除记录（2 篇，均为 correction 退回）

| ID | q3 | 处理 | 理由 |
|---|---|---|---|
| 2610.41397 Cross-Interface Authorization | C | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节 C-008-1。全文没有在任何实际 CUA 栈或代理运行中测出跨接口绕过、凭证跨路径复用或提交前状态竞争；问题依据是引用（HarnessSecurity-Bench 的替代执行路径、Li et al. 的 MCP 发现绕过）和自构的分离执行（App. A.4）。全部实验是私有参考实现对自身生成器的 100% 一致性检查（1,732 场景由公式生成，App. B），Tab.5 的“消融”按场景类别构造必然只有完整协议全对；作者自认有效性、完全中介、当前授权、终局绑定都不是本文新意（§2.4，CONTINUITY） |
| 2610.40798 SafeWebWorld | J | **correction 退回 Sol 单篇修订，本期暂停** | 见第 4 节 C-008-2。L2 标为“未缓存附录”的待查项，补读后答案削弱判断：决策金标只有单人审核、无一致性（App. A.4）；Evidence Recall 是与标注证据串的唯一词元重合率（App. B 式 14，τ=0.35），SA-SFT 在同风格 30k 训练集上学到的是标注措辞；人工研究只判“可信”，作者自述不支持证据充分性与授权正确性结论（App. I Limitations）；“可信预测中 80.37% 属于需 Ask/Block 的例子”等于该 300 题队列的基率（240/300=80%）；主表的决定以完整上下文 X 为输入，“预测本身是否够用”只在附录两个 8B 模型的 F-only 消融中测过 |

`later_work`：3 篇记录都是 null，本期没有按 later_work 降级。

**下期备选**（仅供参考，不改字段）：2610.31274（沿用 selection-004）。本期未新增备选。

## 3. 原文核对状态

| ID | 读到的版本与范围 | 与 L2 的关系 |
|---|---|---|
| 2610.41272 | v1 正文 §1–7 + App. A–B（本文无局限性一节） | 同意 P3/confirmed。**补注（不退回）**：子卡 C30 第二问 verdict=holds 本身成立，但 paper_evidence 以“三次独立完整评测”为支持、facts[0] 直接引用消融数值——补读后 Tab.6 Full 行（14.6/41.1/51.9）即 Tab.5 Run 1，Run 2/3 为 12.1/11.0，三个消融值 10.3–12.0 落在其中，NA 只跑一次 11.6；这三次运行削弱而非支持组件归因与 Qwen3-VL 上的增益。总体 +5.12 点来自跨 8 骨干汇总（72 格中 52 升、18 降、2 平，我们计数）。另：§6.5 正文写 Sonnet 5.5 DPI 32.9%，Tab.11 为 39.8，画报用表值。均不改档位 |
| 2610.41397 | v1 正文 §1–9 + App. A（证明）、B、C | **correction**，见第 4 节 C-008-1 |
| 2610.40798 | v1 正文 §1–6 + App. A–L（表格全部读过；App. C 推理配置与 L 复现清单只看结构） | **correction**，见第 4 节 C-008-2 |

版本复核：2026-11-03 查 arxiv.org/abs，3 篇均只有 v1，与缓存钉定版本一致。

## 4. correction / 待补

### C-008-1　2610.41397v1 Cross-Interface Authorization（退回 Sol 单篇修订，保留旧记录）

旧记录：`batches/inc-l2-11.jsonl`，P3 / confirmed / to_l3；q1 constraint_conflict，q2 open_failure，q3 capability，q4 fits。

- **错误点**：
  1. **Q1 依据不是本文可核查的约束冲突**。全文没有在任何实际部署、开源运行时或代理轨迹中展示 GUI/CLI 路径绕过、批准凭证跨接口复用、准备与提交之间的状态竞争或跨接口重组泄露。§1 的仓库授权例子是假设情形；App. A.4 的“分离执行”是在作者自己的形式模型里说明每条假设 A1–A9 不可去掉，不是问题在部署中存在的证据。问题存在的依据是引用：HarnessSecurity-Bench 报告的替代执行路径、Li et al. 的 MCP 发现层过滤可被脚本客户端绕过（§2.1、§2.3），本文未复测。按 PROBLEM_CORE 第 3 节，这更接近 `measured_cited_unchecked`（核对被引来源前最高 P2）。
  2. **Q4 / evidence_status 的“confirmed”所依据的实验不能检验问题或方法的实际效用**。RQ1–RQ5 都是私有参考实现（§6、“Data, Code, and Materials Availability”：实现、语料、轨迹、报告均不公开）对自身生成器的穷举一致性检查：1,732 个场景由 2FKI+FK(I−1)+3FK+5I(I−1) 公式生成（App. B），全部 100% 通过。Tab.5 的机制消融在同一场景标签上进行，路线切换、状态变化、重组三类场景本就按“需要相应绑定”构造，只有完整协议全对是必然结果，作者也写明只在“within this corpus”成立。没有代理运行、没有实际 CUA 栈；WeaveBench / Magentic-UI 只是带额外 sidecar 的形状适配，作者明确不是集成也不测上游安全（§6.4、§7.6）；归一化器只处理预结构化信封，不解析自由命令（§6.1）；可用性与任务代价不是目标（§3.4）。
  3. **Q2 余留很窄**。作者自述有效性等价、完全中介、当前授权凭证、终局绑定都已由 CONTINUITY 等定义（§2.4，Tab.1），本文差别是“版本化路由清单 + 图割见证 + 绑定具体路由的准备票据”的落地。L2 已承认这一点但仍给 capability。
- **请 Sol 复核**：(a) q1 是否应改为 `measured_cited_unchecked`（或核对被引的 HarnessSecurity-Bench、Li et al. 原文后再定）；若是，tier 封顶 P2；(b) q3 是否仍为 capability——没有测出阻塞性损失，也没有展示以前做不到的能力，改进是在已有授权契约上增加路由绑定，可能是 `incremental`；(c) q4 是否应为 `partial`、evidence_status 是否应为 `pending_experiment`（缺：在实际混合运行时上的绕过实例、未登记路由的发现能力、真实代理任务下的拒绝与成本）。
- 本期不入选，不制作画报。

### C-008-2　2610.40798v1 SafeWebWorld（退回 Sol 单篇修订，保留旧记录）

旧记录：`batches/inc-l2-11.jsonl`，P3 / confirmed / to_l3；q1 measured_own，q2 open_failure，q3 judgment，q4 fits。L2 的 K16 两项已标 partial 并写明“构造标签与证据充分性的独立人工一致性详情在未缓存附录”，同时给出 confirmed。

- **错误点**（补读附录后的答案）：
  1. **决策金标未经独立校验**。3,000 条 TEST 由一名审核者按清单检查（AI 辅助），“Because this was a single-reviewer audit, we do not report inter-annotator agreement”（App. A.4）；54.2% 为受控合成（App. A.8）。作者的捷径探针显示 family、unigram、模板信息仍能预测标签（App. A.5）。
  2. **“证据保留”是词元重合**。Evidence Recall = 预测证据与标注证据串的唯一小写词元交集 / 标注词元数（App. B 式 14–15），漏证据阈值 0.35。SA-SFT 在 30,000 条同风格标注上训练后 ER 达 87.95–93.32%，基线 22.8–38.5%。所谓“证据保留提升而授权变差”（Authorisation-Policy Collapse）中的前半句主要反映学到了标注措辞；而且 Llama 的 Ask 塌缩在最终 SA-SFT 之前已发生（App. K.1 Tab.28，L2 已注）。
  3. **“可信但不充分”没有在逐条预测上测出**。人工研究只判可信（一名主标注者 + 150 条重叠的第二标注，均 AI 辅助，未报一致性），作者明确“not claims about real-world rollout accuracy, evidence sufficiency, or authorisation correctness”，也没有逐条标注预测是否遗漏决定性证据（App. I Limitations）。摘要与 §5.2 的“86.1% 可信、其中 80.37% 属于需 Ask/Block 的例子”：该 300 题队列 240 题为 gold-unsafe（80.0%），我们按 App. I 计数推算，unsafe 题可信率 2,076/2,400=86.5%，safe 题 507/600=84.5%，可信与否和标签基本无关，这个数字不携带“可信预测掩盖不安全”的信息。
  4. **主实验没有隔离“预测”这一接口**。Tab.1 各模型的决定以完整上下文 (g,p,o,a) 为输入，预测未来只是同一输出里的一个字段。真正检验“预测是否够用”的是 App. F.5 的 F-only 消融，只有 Qwen3-8B 与 Llama-3.1-8B 两个模型（Llama：X 90.37 BA → F 54.28，FS 0→16.0%；且同一模型 X 条件 90.37 与 Tab.1 的 82.95 不一致，原文未解释）。
  5. **“ASK/BLOCK 分离仍在”主要是族间分离**。合并 DEV 的 LPS 0.82/0.93，在唯一的混合标签族（transaction_permission_abuse，141 Ask / 19 Block）内 Qwen 0.51–0.56、Llama 0.38–0.45（App. H.4）；DCPF 在该族 BA 35.55%、Block 召回 8.77%，30 组匹配三元组精确率 8.89%，低于未训练的 Base Llama 73.33%（App. K.3 Tab.30）。作者把这一点作为“聚合恢复不等于细粒度授权”的结论，但它同时说明基准的聚合指标受族捷径主导。
- **请 Sol 复核**：(a) q4 是否应为 `partial`（基准形式对准问题，但金标、证据度量与“预测接口”都未经独立验证或隔离）；(b) evidence_status 是否应为 `pending_experiment`（缺：决策金标双标一致性、语义而非词元的证据充分性度量、逐条预测的遗漏标注、更多模型上的 F-only 对照）；(c) q3 的 judgment 能保留多少——较稳的只有“只看 False Safe 会奖励一律 Block、需要三分类与族内/匹配对照”，这一点与已有过度拒绝和澄清文献接近（§2.2），可能收窄为 `incremental`；(d) Tab.1 与 Tab.20 中 Llama X 条件 BA 不一致是否影响记录。Q1 measured_own 可保留。
- 本期不入选，不制作画报。

### 待补清单（priority=high，但未 confirmed；补齐后由 Sol 单篇做 L2，不在本期直接入选）

沿用 selection-007 第 4 节的 9 篇（2610.30181、30573、31307、35823、34724、37093、37255、33702、37482），状态未变。本期新增：

| ID | 当前 | 缺什么 | 补齐会改变什么 |
|---|---|---|---|
| 2610.40747v1 Mage-VL-Cowork | P3 / pending_experiment / park | 见 inc-l2-11 biggest_gap：同任务同轨迹量/长度/筛选与训练预算的对照、多 seed、judge 双侧真值、训练章与附录（缓存截断） | 学生 +12.5 点能否归因到 harness 演化本身 |

## 5. 漏检抽查结果

本期没有新增抽查。progress.md 记录的漏检抽查欠账（累计约 4.1，抽查池因无缓存全文为 0）尚未清零，本期不处理，留给巡检班。

## 6. Reel 成品路径

在 `reel/2610.41272/` 下，含 poster.html、poster.png（1400×2000）、poster.pdf（1 页，1050×1500 pt）、SOURCE.md、QA.md。实际打开渲染图做了视觉 QA，用 DOM 测量核对无越界、内容底边不压页脚、SVG 不超出卡片，PDF 栅格化后与 PNG 对照，另缩到 580 px 宽检查小屏可读性。

| ID | 路径 | 版式骨架 | QA |
|---|---|---|---|
| 2610.41272 | `reel/2610.41272/` | 六步攻击闭环 + 增益贡献瀑布 + 72 格差值点阵 + CTA→ASR 漏斗 + 骨干×送达 ASR/CTA 表 + 重复运行噪声条（浅灰底、海军蓝页眉） | ready（第一次渲染：瀑布标签与漏斗“52.4%”被右缘裁切、底部空约 280 px；重做一次后裁切消失但仍空约 150 px；第三次加大行高与字号后通过，为最终版，如实记录） |

索引：`reel/README.md` 新增第八期一节；`README.md` 头部统计行由 31 改为 32（滚动 run 由 12 改为 13）。poster.html 受 `.gitignore` 第 193 行 `reel/*/poster.html` 忽略，保留在本地。本期未操作 git。
