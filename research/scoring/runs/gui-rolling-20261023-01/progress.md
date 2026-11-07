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

## 2026-10-28 12:17 巡检班

- 新增：1 篇（2610.37255，RSI 仓今晨已评价的同文跨库收集；MiniWoB++ 浏览器实验判在 CUA 收录范围内，corpus 1359→1360）。
- L1：inc-l1-08 1/1 完成（P3/pending_method/to_l2）。
- L2：inc-l2-07 1/1 完成：37255 P3/pending_material/to_l2（q1=measured_own、q4=partial；钉定缓存截断缺 §5–6 与附录——上限求解条件、批量点击成本、等预算适配主实验、先前工作比较均无法核实）。子卡 K24/K29 共 10 项。跨库同文不共享结论，本仓独立判断。
- 漏检抽查：0.1→0 名额，欠账累计 ~1.8。
- to_l3 池：0（备选已清）。

## 2026-10-29 00:17 巡检班

- 新增：1 篇（inbox/2026-10-29-0405 → queue/2026-10-29-0447，corpus 1360→1361）。
- L1：inc-l1-09 1/1 完成（P3/pending_method/to_l2）。
- L2：inc-l2-08 1/1 完成：33702 P3/pending_material/to_l2（q1=measured_own、q4=fits 限离线受控诊断；阻塞：钉定缓存为裁剪 core 缺校准/成本实验与附录、首版日期记录冲突致先前工作未核；条件化版不能跨请求复用、AUROC≠校准）。子卡 C03/C06 共 12 项。
- 漏检抽查：0.1→0 名额，欠账累计 ~1.9。
- to_l3 池：0。

## 2026-10-29 06:17 巡检班

- 新增：2 篇（inbox/2026-10-29-0958 → queue/2026-10-29-1048，corpus 1361→1363）。
- L1：inc-l1-10 2/2 完成（P3×1 / P2×1，全 assessed）。
- L2：inc-l2-09 2/2 完成（本班 to_l2 全部）。**1 篇 P3/confirmed/to_l3**（32482 等待瓶颈与方法对齐——回放过早返回 15.64%，非安全部署确认）；33645 P2/park（grounding 增量改善）。子卡 C06/C07 共 10 项+1 NA。
- 漏检抽查：0.2→0 名额，欠账累计 ~2.1。
- to_l3 池：1 篇（32482）。

## 2026-10-29 08:43 每日 Opus 判断

- selection-006 后新增 confirmed P3：1 篇（32482）<3 → 跳过（22155 已除名）。37255/33702 均阻塞于材料。

## 2026-10-31 12:17 巡检班

- 新增：10 篇（inbox/2026-10-30-1223，ingest.py 入库 corpus→queue/2026-10-31-1052，材料 10/10 abstract_intro）。
- L1：inc-l1-11 10/10（全 assessed，to_l2 10 = high 8 / medium 2）。
- L2：inc-l2-10 10/10（本班 to_l2 全部；遗留 high 0）。**8 篇 P3/confirmed/to_l3**（37786/39234/39282/39488/40133/40246/40578/2605.29532）；39251 P2/park；39264 P2/pending_experiment/park（Q1→measured_own、Q3 收窄 incremental）。层级改判 0。
- 漏检抽查：名额 1（预算 10×10%）+ 欠账 2.1 补抽 2，但抽查池 0（遗留 park/needs_material 篇均无缓存全文，不自动下载）→ 欠账滚存 ~3.1。seed=20261031。
- to_l3 池：1（32482）+ 本班 8 = 9 篇 ≥3 → 明晨 Opus 班可做 selection。

## 2026-10-31 08:43 每日 Opus 判断（第七期选题 + C-007-1 落档）

- selection-006 后新增 confirmed P3：9 篇 ≥3 → 第七期选题。终选 3 篇（39282 陈旧截图点击错位 / 39234 AgentHeal 资源恢复 / 2605.29532 GUITestScape 开放集探索测试），各经多轮修复后过视觉 QA；32482（与 39282 同题证据更弱）/40578（弃权计失败）/39488/37786/40246 落选。见 selection-007.md。累计 31 张。
- Correction C-007-1（40133 DynaRev 未验证裁判循环）已退回 Sol 修订：inc-l2-10-rev1-40133.jsonl → P3→P2、pending_experiment、q3→incremental、q4→partial、park。原记录保留。
- 隔夜收集 +1 未评（06:17 巡检班丢失），12:17 班补。

## 2026-11-01 08:43 每日 Opus 判断

- selection-007 后新增 confirmed P3：0 篇 <3 → 跳过（40133 已经 correction 降档）。周末 arXiv 停更无新增。

## 2026-11-02 08:43 每日 Opus 判断

- selection-007 后新增 confirmed P3：0 篇 <3 → 跳过。隔夜收集 +5 待 12:17 巡检班入库评分。

## 2026-11-02 12:17 巡检班

- 新增：5 篇（inbox/2026-11-02-1324，ingest.py 入库→queue/2026-11-02-1749，材料 5/5 abstract_intro）。
- L1：inc-l1-12 5/5（全 assessed，to_l2 5 = high 4 / medium 1）。
- L2：inc-l2-11 5/5（本班 to_l2 全部；遗留 high 0）。**3 篇 P3/confirmed/to_l3**（41397/40798/41272）；40747 P3/pending_experiment/park（缺等数据量归因对照）；41432 P2/park。改判 0。
- 漏检抽查：名额 1（预算 5×10%）但池 0 → 欠账 ~3.1+1→~4.1 滚存。seed=20261102。
- to_l3 池：0 + 本班 3 = 3 篇 ≥3 → 明晨 Opus 班可做 selection。

## 2026-11-03 08:43 每日 Opus 判断（第八期选题 + C-008-1/2 落档，补跑）

- selection-007 后新增 confirmed P3：3 篇 ≥3 → 第八期选题。终选 1 篇（41272 ANGLER，主卡 environmental_injection_attacks 首张），第 3 次渲染过视觉 QA；累计 32 张。41397、40798 因 correction 暂停未制作。
- Correction C-008-1（41397 问题未在真实栈观察、自洽检查）已退回 Sol 修订：P3→P2、q1→measured_cited_unchecked、q3→incremental、q4→partial、pending_experiment/park。
- Correction C-008-2（40798 单人金标、词重叠指标、基率头条）已退回 Sol 修订：保留 P3/high，q4→partial、pending_experiment/park，q3 收窄为"预测式门控需隔离预测接口与族内对照"。

## 2026-11-04 08:43 每日 Opus 判断

- selection-008 后新增 confirmed P3：0 篇 <3 → 跳过。收集端自 11-02 晨无新产出；40747 归因对照与 40798 Llama 两表对账仍待补。

## 2026-11-04 18:17 巡检班（GitHub 查新首班）

- 查新来源：refs/lists 拉齐（Awesome-CUA→11-03、Awesome-GUI-Agents→11-01、GUI-Agents-Paper-List→10-29）→ 11 篇新候选（queue/2026-11-04-0033，材料 10 abstract_intro + 1 abstract）。
- L1：inc-l1-13 11/11（assessed 7，out_of_scope 4：32441/38174/40754/01860；to_l2 7 = high 3 / medium 4，含 needs_material 2）。
- L2：inc-l2-12 11/11（to_l2 7 + 排除抽查 4，欠账 4.1 清偿）。改判 1 篇 P2→P3（2611.03126）。**1 篇 P3/confirmed/to_l3**（2610.41181）；2605.28629、2611.03126 P3/pending_experiment/park；41998/3178/3634 pending_material（范围/章节待补）。抽查 4 篇排除全部维持（漏检改判 0）。
- 漏检抽查：seed=20261104，名额 1（预算 7×10%）+欠账 4.1 补抽 4，池 4 全抽；改判 0/4。
- to_l3 池：0 + 1 = 1 篇 <3 → 明晨 Opus 班暂不达标。

## 2026-11-05 06:17 巡检班（GitHub 查新·Awesome-CUA 回填大批）

- 查新来源：Awesome-CUA 11-03 public-source scan 目录扩充 → 129 篇回填候选（queue/2026-11-04-0601，材料 123 abstract_intro + 6 abstract）。工具事故与修复：批输入 TSV 因 l1_manifest 换行 bug 折行，全部重写后已核对（在跑 agent 均确认按修复版处理）。
- L1：inc-l1-14..20 七批 129/129（exclude 74 / to_l2 55 = high 43 + medium 12，needs_material 若干）。
- L2：inc-l2-13..16 四批 61/61（to_l2 55 全部 + 漏检抽查 6）。**17 篇 P3/confirmed/to_l3**（含 2611.02472/2611.02644/2611.03238 等）；16 篇 pending_experiment/park；14 篇 pending_material/park（范围/章节待补）；2 篇 P2/confirmed/park；12 篇排除（其中抽查样）。抽查 6 篇漏检改判 0。
- 漏检抽查：seed=20261105，名额 6（预算 55×10% 取整），池 26 抽 6。
- to_l3 池：1 + 17 = 18 篇 ≥3 → 今晨 Opus 班达标可做 selection。

## 2026-11-05 12:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA 再更新 → 3 篇新候选（queue/2026-11-04-1148，材料 3/3 abstract_intro）；RSI EvoMap 更新无新 id；Embodied lists 无更新；三仓 inbox 均空。
- L1：inc-l1-21 3/3，**均 out_of_scope/exclude**（2606.30296/2610.06514/2611.05036 不属 CUA 收录口径，理由见批次记录）。无 to_l2，无 L2。
- to_l3 池：维持 18 篇 ≥3 → 今晨 Opus 班可做 selection-009。

## 2026-11-06 08:17 巡检班（收集端恢复）

- 新增：6 篇（inbox/2026-11-04-1321 5 篇 + GitHub 查新 2611.04785；queue 1750/1751，材料 6/6 abstract_intro）。
- L1：inc-l1-22 6/6（to_l2 4，exclude 2：04579、04785——理由见批次）。
- L2：inc-l2-17 4/4（to_l2 全部；遗留 high 0）。**3 篇 P3/confirmed/to_l3**（2611.04879/05263/04073）；2611.04142 P3/pending_experiment/park（前缀长度/阈值/早停待核）。改判 0。
- 漏检抽查：名额 0（预算 4×10%），欠账 ~0.4 滚存（池 49 可用）。seed=20261106。
- to_l3 池：18 + 3 = 21 篇 ≥3 → 今日 Opus 班达标。

## 2026-11-06 每日 Opus 判断（第九期选题 + C-009-1 落档）

- selection-008 后新增 confirmed P3：20 篇 ≥3 → 第九期选题。终选 2 篇（04073 教程 vs 世界模型瓶颈 / 04879 ScamWorld 代理受骗暴露），各第 3 次渲染过 QA；第 3 席空缺（其余候选均有去重/范围/证据/主卡重叠理由，不为凑数入选）；41181 主卡已覆盖+缓存截断落选；03238 与 04073 同题落选。备选：31274、DIBench 06898、Coati 02644。见 selection-009.md。累计 34 张。
- Correction C-009-1（05263 JHiMA-WebRL 无方差/头条差距归因错误）已退回 Sol 修订：P3→P2、q3→incremental、q4→partial、pending_experiment/park。原记录保留。

## 2026-11-05 18:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA 再更新 → 1 篇新候选 2611.04393（queue/2026-11-05-0548，材料 1/1 abstract_intro）；RSI/Embodied lists 与三仓 inbox 均无新增。
- L1：inc-l1-23 1/1（P3/high/to_l2）。L2：inc-l2-18 1/1 → **P3/confirmed/to_l3**（附录与 60.4% 汇总口径、防御真实危险效用留 L3 核）。
- to_l3 池：21 - 02079 用后余量 + 1 ≈ 视 selection-009 消耗而定（selection-009 用 2 席，31274/06898/02644 仍为备选）。

## 2026-11-05 20:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA + GUI-Agents-Paper-List 更新 → 4 篇新候选（queue/2026-11-05-1148，材料 4/4 abstract_intro）；三仓 inbox 空。
- L1：inc-l1-24 4/4（全 to_l2）。L2：inc-l2-19 4/4：**0 篇 to_l3**——05873 P3/pending_experiment/park（缺实现审计与 RQ5/Table X 原段）、06039 P3/pending_method/park（缺安全修复与诊断反馈实现段）、06544 与 06854 P2/confirmed/park（06854 由 P3 降档）。改判 1 篇 P3→P2。
- 漏检抽查：名额 0（预算 4×10%），欠账 ~0.4+0.8→~1.2 滚存（池 49）。seed=20261107。
- to_l3 池：维持（selection-009 后备选 31274/06898/02644 + 04393）。

## 2026-11-06 06:17 巡检班（GitHub 查新补）

- 查新来源：Awesome-CUA 更新 → 1 篇 2605.26079（queue/2026-11-05-1751，材料 1/1 abstract_intro）；inbox 空。
- L1：inc-l1-25 1/1（P3/high/to_l2，needs_material）。L2：inc-l2-20 1/1 → P3/q4=partial/**pending_material/park**（缓存缺 App. B/C/D 与完整 §5，GUI/browser 基准覆盖与两侧审计未确认）。
- to_l3 池：维持（备选 31274/06898/02644 + 04393）。

## 2026-11-07 每日 Opus 判断（第十期选题）

- selection-009 后新增 confirmed P3：4 篇 ≥3 → 第十期选题。终选 2 篇（04393 Voluntary Servitude 假评论操纵 / 31274 PointerBench 指针格式塌缩，上期备选），分别 6/7 轮渲染后过视觉 QA；无 correction（04393 L2 三项待核全部核清：60.4% 为四模型均值、附录样例无命令、防御真实代价未测）。06898 与 04393 同题去重、02644 消融不配对维持落选。见 selection-010.md。累计 36 张。

## 2026-11-07 巡检班（GitHub 查新·Awesome-CUA 回填第二波）

- 查新来源：Awesome-CUA 目录再扩充 → 271 篇回填候选（queue/2026-11-06-0014，材料 261 abstract_intro + 10 abstract）。
- L1：inc-l1-26..39 十四批 271/271（exclude 122 / to_l2 147 = high 96 + medium 71；needs_material 若干）。上游书目疑点：2208.02685 实为 ICLP 2022 论文集（疑似错配，已排除处理）；2604.14872 原文成功率 1000%/100% 矛盾（L2 已记）。
- L2：inc-l2-21..29 九批 166/166（to_l2 147 全部 + 漏检抽查 19，欠账 4.3 清偿）。**46 篇 P3/confirmed/to_l3**；49 篇 pending_material/park（老论文缓存缺章为主）；17 篇 pending_experiment；17 篇 P2/confirmed/park；37 篇排除（含抽查样）。抽查 19 篇范围漏检改判 0。
- 漏检抽查：seed=20261108，名额 15（预算 147×10%）+欠账 4 补抽，池 137 抽 19。
- to_l3 池：+46 篇 → 明晨 Opus 班大幅达标（候选众多，选题余地大）。

## 2026-11-06 20:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA 更新 → 4 篇新候选（queue/2026-11-06-0549，材料 4/4 abstract_intro）；三仓 inbox 空。
- L1：inc-l1-40 4/4（to_l2 3，out_of_scope 1：06500 纯搜索 API/QA 无 GUI 操作面）。
- L2：inc-l2-30 3/3：**2 篇 P3/confirmed/to_l3**（05620/07765，Q1 改判 1 篇）；06075 park。
- 漏检抽查：名额 0（预算 3×10%），欠账 ~0.3 滚存（池 118 可用）。seed=20261109。
- to_l3 池：46 + 2 = 48 篇（回填池待明晨 Opus 班选题）。

## 2026-11-07 02:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA 更新 → 1 篇 2610.14488（queue/2026-11-06-1148，材料 1/1 abstract_intro）；三仓 inbox 空。
- L1（单篇快通道 L1+L2）：inc-l1-41 1/1 → **out_of_scope/exclude**（验证 coding-agent 权限约束，无 GUI/browser 操作面，未构成 CUA 集成验证）；L2 按条件未执行。
- to_l3 池：维持 48。

## 2026-11-08 每日 Opus 判断（第十一期选题 + C-011-1 落档）

- selection-010 后新增 confirmed P3：48 篇（回填第二波为主）→ 第十一期选题。粗筛短名单 12 → 终选 2 篇（2507.11662 SGV 期望锚定轨迹核验 / 2505.10978 GiGPO 同页动作对比步级信用），各 4/6 轮渲染后过视觉 QA；第 3 席按证据不足空缺。见 selection-011.md。累计 38 张。
- Correction C-011-1（2604.25235 CUA 相关性）已退回 Sol 修订：**out_of_scope/exclude（P1）**——Mind2Web 398 条为 VQA 式答案评分，不涉轨迹/动作；C25/K16 六项检查改 NA。原记录保留。
- 备注未退回：GiGPO "<0.002%" 计算开销实为 ~0.15%（结论不变）；SGV 表 3A 与正文数字矛盾。

## 2026-11-08 12:17 巡检班（GitHub 查新·Awesome-CUA 回填第三波）

- 查新来源：Awesome-CUA 目录第三波扩充 → 104 篇回填候选（queue/2026-11-06-1800，材料 101 abstract_intro + 3 abstract）。
- L1：inc-l1-42..47 六批 104/104（exclude 87 / to_l2 17——第三波以范围外经典为主）。
- L2：inc-l2-31/32 两批 24/24（to_l2 17 全部 + 漏检抽查 7，欠账 5.3 清偿 5，余 ~1.0）。档位/范围改判 3 篇（含抽查纠偏 1 篇）。**8 篇 P3/confirmed/to_l3**（2504.12516/2505.15146/2506.03610/2509.21143/2510.23691/2510.26787/2601.13142/2609.35143）；7 篇 pending_material；3 篇 pending_experiment；6 篇 exclude。抽查 7 篇漏检晋级 0。
- 漏检抽查：seed=20261109，名额 2（预算 17×10%）+欠账 5 补抽，池 177 抽 7。
- to_l3 池：48 - 已选 + 5 ≈ 视 selection-011 消耗（已用 2 席）后约 46+5。

## 2026-11-07 14:17 巡检班（GitHub 查新）

- 查新来源：Awesome-CUA 更新 → 3 篇（queue/2026-11-07-0549，材料 3/3 abstract_intro）；三仓 inbox 空。
- L1（小批快通道 L1+L2）：inc-l1-48 3/3——2602.05156（机器人手接触结构）、2611.02752（HPC 代码优化）均 out_of_scope；2611.06939 P2/to_l2。
- L2：inc-l2-33 1/1——2611.06939 P2/pending_experiment/park（物理 GUI 机制对题但运行时 XML 来源不明，缺端到端自主测试；§4 缺章已从 arXiv 原站补读）。
- to_l3 池：维持（~53）。
