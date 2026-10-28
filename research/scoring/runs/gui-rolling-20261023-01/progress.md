# gui-rolling-20261023-01 进度

## 2026-10-23 巡检班（首班）

- 本班无可评分新增：inbox 两个候选（2026-10-22-0955 LBYL、2026-10-22-1552 IGG）均为 GitHub-only（arxiv: null）。
- 已做 arXiv API 标题精确+关键词两级检索（ti:"..." 与 all: AND 组合），均无命中 → 暂无对应论文，保留在 inbox 待 Grok 后续收集补 arXiv ID；不评 repo-only 条目。
- 下班巡检：新 inbox 候选照常处理；这两个 ID 若在 corpus 出现对应论文即可按常规流程评。

（本 run 目录预建，首批 L1 批次落此 run。）

## 2026-10-24 巡检班（第二班）

- 新增：8 候选（inbox/2026-10-23-0356，ingest 入库 7，1 篇已在 corpus；corpus 1331→1338），run.md 本班补建。另 2 个 GitHub-only 候选（LBYL、IGG）arXiv 标题复检仍无命中，继续留 inbox 待关联。
- L1：inc-l1-01 7/7 完成（材料 6 abstract_intro + 1 abstract）。assessed 5 / out_of_scope 2。档位 P3×4 / P2×1 / null×2。
- L2：预算 2（=max(2, 20%×7 取整)），inc-l2-01 2/2 完成：2610.30181v1、2610.30573v1 均 P3 / pending_material / to_l2（q1=measured_own，q4=partial）。
- 漏检抽查：2×10%=0.2→0，无名额（audit 池已记录待后续班次）。
- L2 缺口（写入记录）：两篇全文缓存尾部截断（2610.30573 §4.5 截断、缺 Table 3(a)；2610.30181 缺 judge 校准/访问隔离对照材料）→ pending_material，进补材料队列，不隐性淘汰。
- 注：本 run 的 paper_id 带 v1 后缀（worker 沿用 inbox 版本写法），corpus 键为裸 ID；后续班次统一用裸 ID，L1/L2 记录内已自洽。

## 2026-10-24 08:43 每日 Opus 判断

- 新增 confirmed P3：0 篇（2 篇 P3 均 pending_material，全文截断待补）→ 本轮跳过 Reel。补材料后 Sol 重核，确认后再进选题。

## 2026-10-25 08:43 每日 Opus 判断

- 新增 confirmed P3：0 篇（2 篇 P3 维持 pending_material，10-25 06:17 重抓 v1 全文无变化）→ 跳过。

## 2026-10-25 18:17 巡检班

- 无 arXiv 新候选。Grok 恢复收集：新增 2 个 GitHub-only 候选（2026-10-24-2155 Occlusion-Aware Observations、2026-10-25-0356 Dynamic web-agent reliability），arXiv 标题检索均无命中 → 留 inbox 待关联。待关联累计 5 个。

## 2026-10-26 08:43 每日 Opus 判断 + 漏网补评

- 新增 confirmed P3：0 篇 → 跳过。夜间巡检漏了 inbox/2026-10-25-0952 的 1 篇 arXiv 候选（2610.22155），本班补入库并入 inc-l1-02 评 L1；L2 预算已用满（2/2），结果为 to_l2 则排队。

## 2026-10-27 补跑班（fetch 盲区修复后）

- 盲区说明：2026-10-24/25/26 巡检未先 git fetch，漏掉 Grok 直推远端的收集；本班补齐 fetch-first（cron 提示词已修）。
- 新增：4 篇（inbox/2026-10-26-0358 → queue/2026-10-26-1230，corpus 1338→1342）。
- L1：inc-l1-03 4/4 完成（P3×3 / P2×1，全 assessed）。
- 预算修订：run.md 2026-10-27 增量轮声明——每班 = 本班 to_l2 全部 + 遗留 high ≤5。
- L2：inc-l2-02 8/8 完成（本班 4 + 遗留 4）。**6 篇 P3/confirmed/to_l3**（31698/32223/32536/22155/30792v1/31274v1）；31712 P2/confirmed/park；31307v1 P3/pending_experiment（记忆隔离/等预算/标签可靠性阻塞）。子卡 44 项：holds 14 / partial 20 / unknown 7 / fails 2（Malva 被诊断系统违反条件，非诊断失败）/ challenged 1。
- 漏检抽查：欠账未清（本班预算 8×10%=0.8→0）。
- 下一步：明早每日 Opus 班 CUA 新增 confirmed P3=6 ≥3 → 首次选题。

## 2026-10-27 12:17 巡检班

- 新增：1 篇（inbox/2026-10-27-0356 → queue/2026-10-27-0516，corpus 1342→1343）。入库前遇 arXiv API 429/超时，15 分钟退避后成功；教训：inbox mv 只挂入库成功之后（本轮已两度误挪并恢复）。
- L1：inc-l1-04 1/1 完成（P3/pending_method/to_l2）。
- L2：inc-l2-03 1/1 完成（本班预算 = 新 to_l2 全部；high 遗留 0）：2610.35823 P3/pending_experiment/to_l2（q4=partial；K13/K34/K16/C17/K30 共 13 项：holds 5 / partial 7 / unknown 1）。阻塞：跨站数据隔离、合法替代轨迹、等预算对照、§3.2 与 §4.4 数据生成模型文述不一致。暂不送 L3。
- 31307v1 维持 pending_experiment 待 v2 对照材料。漏检抽查欠账：0.1×1=0.1，累计至 0.2。

## 2026-10-27 18:17 巡检班

- 新增：6 篇（inbox/2026-10-27-0954 → queue/2026-10-27-1048，corpus 1343→1349）。入库一次路径拼接失误（queue 文件名重复前缀），cut_l1 重跑成功，inbox 移动仍挂在成功之后。
- L1：inc-l1-05 6/6 完成（P3×5 / P2×1，全 assessed）。
- L2：inc-l2-04 6/6 完成（本班 to_l2 全部）。**4 篇 P3/confirmed/to_l3**（33528/33907/34384/33636）；34959 P2/confirmed/park；34634 L2 判 out_of_scope/exclude（纯业务 API actor，无 GUI/浏览器操作面——L1 遗留核对项落定，非误排除）。子卡 33 项：holds 10 / partial 13 / fails 2 / unknown 2 / NA 6。
- 漏检抽查：0.6→0 名额，欠账累计 ~0.8。
- to_l3 池：Realtime-Bench（上期备选）+ 本班 4 = 5 篇 ≥3 → 明早 Opus 班选题（第五期）。

## 2026-10-28 08:43 每日 Opus 判断（第五期选题 + correction 落档）

- 新增 confirmed P3：5 篇 ≥3 → 第五期选题。终选 3 篇（34384 AndroidFlux 失败恢复重排 / 33636 Build-or-Adopt 循环对照 / 33907 OS-Wizard 合成训练数据），3 张全过 QA（2–3 轮渲染修复，历史在 QA.md）；22155 第三次列备选（v3 仍未解除单 run 顾虑，但 Paused vs Token 36–40 点差远超 Wall Clock 三次极差，范围收窄后站得住）。见 selection-005.md。累计 25 张。
- Correction（33528 SkillShift-Bench：Q1"测到技能可执行性问题"超出证据）已退回 Sol 修订：inc-l2-04-rev1-33528.jsonl → **P2/pending_experiment/park**（q1_basis=asserted、q4=partial；四点接受+一点部分接受并纠正 SD 表述——Tgt 增益 1.46pp 实际略大于两组 SD；补 q2_prior=Kara et al. 2026 WAREX；q2_open 维持 open_failure）。原记录保留。
- to_l3 池：22155（第三期连续备选）。

## 2026-10-28 12:17 巡检班

- 新增：4 篇（inbox/2026-10-27-1550 → queue/2026-10-27-1648，corpus 1349→1353）。
- L1：inc-l1-06 4/4 完成（assessed 3 / oos 1——2610.35215 无 GUI/浏览器操作面证据；P3×2 / P2×1）。
- L2：inc-l2-05 3/3 完成（本班 to_l2 全部）。**2 篇 P3/confirmed/to_l3**（35237 探索依赖任务规划诊断、34735 persona 个性化——限单 persona/mock iOS）；34724 P3/pending_experiment（WebShop 指标为部分匹配 reward 非成功率；model-only 消融同时移除记忆与 replay 缺隔离证据）。子卡 23 项：holds 4 / partial 12 / fails 1 / unknown 4 / NA 2。
- 漏检抽查：0.3→0 名额，欠账累计 ~1.1。
- to_l3 池：22155（三连备选）+ 本班 2 = 3 篇 ≥3 → 明早第六期选题。

## 2026-10-28 18:17 巡检班

- 无 arXiv 新候选。Grok 新收 2 个 GitHub-only 候选（Doppelganger Screens、Stale Screens/Now），arXiv 标题检索无命中 → 留 inbox 待关联。待关联累计 7 个。

## 2026-10-28 06:17 巡检班

- 新增：6 篇（inbox/2026-10-28-1002 → queue/2026-10-28-1050，corpus 1353→1359）。
- L1：inc-l1-07 6/6 完成（P3×5 / P2×1，全 assessed）。
- L2：inc-l2-06 6/6 完成（本班 to_l2 全部）。**4 篇 P3/confirmed/to_l3**（36471/36831/36877/37482，各带收窄边界）；37093 P3/pending_experiment（LLM judge 无独立校验、等预算/种子证据缺）；36874 P2/park。子卡 34 项：holds 4 / partial 18 / fails 2 / unknown 3 / challenged 2 / NA 2。
- 漏检抽查：0.6→0 名额，欠账累计 ~1.7。
- to_l3 池：22155（三连备选）+ 35237 + 34735 + 本班 4 = 7 篇 ≥3 → 今晨 Opus 班第六期选题。

## 2026-10-29 08:43 每日 Opus 判断（第六期选题 + correction 落档）

- 新增 confirmed P3：7 篇 ≥3 → 第六期选题。终选 3 篇（36831 点击结果评分偏差 / 35237 离屏滑动诊断 / 34735 iPrefBench），3 张均三审通过（渲染历史在 QA.md）；**22155 三期未满足转正条件（重复运行/web 子集），从备选名单除名**。见 selection-006.md。累计 28 张。
- Correction（37482："capability, confirmed" 超出同协议证据）已退回 Sol 修订：inc-l2-06-rev1-37482.jsonl → **P3/pending_experiment/to_l2**（q4=partial；四点接受：12.0 出处不可追溯、同协议 State-only 不及 ConAct、领先依赖跨任务 Graph 且终局判定可回流、主比较单次无区间——SPA-Bench 段有两序列，措辞已限定）。原记录保留。
- to_l3 池：0（备选已清）。
