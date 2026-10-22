# 问题核心：三项目统一的评价规范

版本 `problem-core-v1.1`（2026-10-22）。**三个项目（HarnessRSI Daily、CUA-Daily、Embodied-Harness-Daily）共用本文件，内容逐字相同；修改时三处同步。** 各项目的问题族到领域卡映射见同目录 [PROBLEM_MAP.md](PROBLEM_MAP.md)。

状态：规范已写定，**尚未试点，尚未执行任何评分**。第 9 节试点完成并经用户授权前，不启动全量运行。本文件取代 `sol-domain-v3.1` 的 G/M/X/E 四轴和 `screen_score`；[SOL_BATCH_PROMPT.md](SOL_BATCH_PROMPT.md)、[SELECTION.md](SELECTION.md)、[OPUS_REEL_PROMPT.md](OPUS_REEL_PROMPT.md) 均按本文件执行。

v1.1 相对 v1 的修订：排除自我比较；影响面不再按卡片数量；问题成立依据与“换场景”定义细化；问题档位、阅读优先级、证据状态、下一步分开记录；子卡检查改为检查条件而非步骤；执行入口同步。

## 1. 两层，分开记录

| 层 | 问什么 | 依据 | 范围 |
|---|---|---|---|
| 第一层：问题 | 问题是否成立、是否开放、解决后改变什么、方法是否对准它 | 第 2–4 节；本项目主卡的认知障碍与失败模式 | 三项目统一 |
| 第二层：执行 | 机制依赖的条件是否成立、关键失败是否排除 | 第 6 节；本项目子卡 | 各项目自己的卡 |

两层不相加成总分，也不加权。判断依据仍是本项目领域卡原文；问题族只负责组织，不是评分项。

## 2. 五个问题族（只用于组织）

归纳自三个项目主卡的“认知障碍”和“失败模式”。

| 族 | 核心问法 | 典型被挑战的共识 |
|---|---|---|
| **F1 归因** | 收益真的来自所声称的部件，而不是额外算力、数据、骨干、harness 或其他部件吗？ | “提升属于模型／属于这个模块” |
| **F2 信号可信** | 用于选择、奖励、门控、评估的信号可靠吗？会被利用吗？ | “judge 准确率高就能当 reward”“执行检查器就是真值” |
| **F3 迁移边界** | 结论离开产生它的环境、任务、模型或代理后还成立吗？ | “记忆随处可迁移”“自生成数据普遍提升能力” |
| **F4 信息访问** | 方法用到的信息部署时拿得到吗？是否接触测试流、真值或攻击者可写内容？ | “复制特权专家即可迁移其能力” |
| **F5 单调假设** | “X 越多越好”真的成立吗？ | 更多历史、候选、角色、教师数据、推理文本 |
| **F0 其他** | 不属于以上各族的问题，例如新能力或实际工程瓶颈 | — |

一篇可属于 1–2 个族。**F0 与 F1–F5 晋级资格相同**，不因不挑战共识而降档；F0 的比例只用来提示问题族需要修订。

## 3. 四个问题

### Q1 问题是否成立（`q1_basis`）

| 取值 | 含义 |
|---|---|
| `measured_own` | 本文自己的测量显示问题存在 |
| `measured_cited_checked` | 引用他人测量，且已核对被引来源原文 |
| `measured_cited_unchecked` | 引用他人测量，仅有本文转述 |
| `proof` | 有证明 |
| `counterexample` | 有明确、可核查的反例 |
| `constraint_conflict` | 可核查的约束冲突，例如部署时拿不到训练所用信息 |
| `asserted` | 只有陈述 |
| `unknown` | 现有材料看不出 |

### Q2 问题是否开放（`q2_open`）

**只与先前工作比较：排除本文及其所有版本，只看本文首个版本发布之前的工作，并且要求同一问题、同一条件。** 卡片由本语料归纳而来，本文本身或更晚的论文可能就是卡片成员，不能拿来证明本文的问题“已被解决”。

| 取值 | 含义 |
|---|---|
| `challenges_barrier` | 挑战本项目卡片记录的某条认知障碍 |
| `open_failure` | 针对先前工作仍开着的失败模式或审稿期望缺口 |
| `new_bottleneck` | 卡片未覆盖的新瓶颈或新能力，有 Q1 依据 |
| `vertical_port` | **只换了应用对象，问题约束、机制和可用能力都没变**。从仿真到真机、从特权信息到部署可见信息、从离线到在线等改变约束的情形不算 |
| `prior_solved` | 有先前工作在同一问题、同一条件下已解决；必须写出该工作 |
| `unknown` | 现有材料无法判断 |

如果后来出现更好的工作，记 `later_work` 字段。它可以降低今天的阅读优先级，但**不改变本文的问题档位**，也不能倒推本文没有贡献。

### Q3 解决后改变什么（`q3_change`）

写出问题造成的**具体损失**，以及解决后改变的**能力或研究判断**。不按涉及卡片的数量评价。

| 取值 | 含义 |
|---|---|
| `capability` | 消除一个阻塞性损失，或带来以前做不到的能力，例如一个 STOP 错误、一个奖励漏洞、一个蒸馏信息缺口 |
| `judgment` | 改变本领域的一个研究判断或常用做法 |
| `incremental` | 已有能力上的改进，损失和改变都有限 |
| `local` | 只影响本文的设置 |

### Q4 方法是否对准问题（`q4_fit`）

`fits`／`partial`／`misfit`／`unknown`。诊断、审计、负结果、benchmark 论文看其受控实验是否真正隔离了所说的问题，不要求有正向提升。L1 通常是 `unknown`，L2 才确认。

## 4. 四个独立字段

| 字段 | 回答什么 | 取值 |
|---|---|---|
| `problem_tier` | 问题本身有多好 | P0–P3，或 `null`（材料不足以判断） |
| `evidence_status` | 这个判断确认到哪一步 | `confirmed`／`pending_method`／`pending_experiment`／`pending_material` |
| `priority` | 现在值不值得花阅读预算 | `high`／`medium`／`low`／`none` |
| `next_action` | 下一步做什么 | `to_l2`／`to_l3`／`park`／`exclude` |

### problem_tier

| 档 | 条件 |
|---|---|
| **P3** | Q1 为 `asserted`/`unknown` 以外的依据；Q2 为 `challenges_barrier`、`open_failure` 或 `new_bottleneck`；Q3 为 `capability` 或 `judgment` |
| **P2** | 问题成立且开放，但 Q3 为 `incremental`；或 Q1 只有 `asserted`／`measured_cited_unchecked` |
| **P1** | Q3 为 `local`，或 Q2 为 `vertical_port` |
| **P0** | Q2 为 `prior_solved`，或材料显示问题不成立，或 Q4 为 `misfit` 且问题本身也弱 |

封顶规则：
- Q4 `misfit` → 最高 P1。
- Q1 `asserted` → 最高 P2；`measured_cited_unchecked` 在核对被引来源之前同样最高 P2。
- Q2 `vertical_port` → 最高 P1。
- 任一项为 `unknown` 并影响档位判断时：能判断就给出档位并在 `evidence_status` 标待核对；完全无法判断记 `null`，**不记 P0**。

**P3 是否最终成立取决于 `evidence_status`**：L1 给出的 P3 通常是 `pending_method`，L2 确认 Q4 为 `fits` 后才改为 `confirmed`。

### priority

- 按问题档位和潜在价值判断：P3 或可能 P3 → `high`；P2 → `medium`；P1 → `low`；P0 → `none`。
- **材料未知本身不降低优先级。** `problem_tier=null` 但摘要显示可能是 P2/P3 的论文，按潜在档位给 `medium` 或 `high`，并写出缺哪段材料。
- 可下调一档的理由只有：`later_work` 已有更好的同题工作，或与已选论文内容重复。写出理由。

### next_action

- `to_l2`：`priority` 为 `high`，或为 `medium` 且 `evidence_status` 不是 `confirmed`。受 L2 预算限制（第 5 节）。
- `to_l3`：P3 且 `confirmed`；或 P2 且 `confirmed`，并写出编辑理由（例如扎实地解决单个关键瓶颈）。
- `park`：暂存，可在下一期或预算放宽时再取。
- `exclude`：P0，或 `out_of_scope`。

不按代码链接、venue、录用、引用数、作者或写作风格调整任何字段。三个项目的档位不混成一个总榜。

## 5. 检索漏斗与预算

| 层 | 材料 | 执行 | 产出 |
|---|---|---|---|
| L1 初筛 | 摘要＋引言，由脚本从已缓存原文按标题切出；切不出则只用摘要，标 `abstract` | Sol 原生 Subagent，4 并发，每批 20 篇起 | 第一层全部字段 |
| L2 核对 | 方法与主要实验的关键段，附章节/表号 | Sol，每批 10–20 篇 | 确认 Q1、Q4，更新档位与证据状态；填第二层子卡检查 |
| L3 选题 | 候选原文 | Opus 5.5 | 跨项目小池比较、去重，选少于 10 篇做 Reel |

**L2 预算**：每次 run 在 `run.md` 写明本项目 L2 的篇数上限和 token 上限，默认不超过 L1 篇数的 20%。进入顺序：`high` → `medium`。另外**固定留出 L2 预算的 10%**，从 P0/P1、F0、`needs_material`、`park` 中随机抽取做漏检核对；抽中的记录照常更新，并在 run 记录中单独统计“初筛漏检数”。

- L1 每批从 20 篇起，确认实际输入量后再决定是否放宽到 30–50；放宽要写入 run 记录。
- 复用已缓存原文，不新增一轮模型摘要，不为全量重新下载。
- `needs_material` 的论文按 `priority` 排队补材料，补齐后进 L2；不因缺材料被隐性淘汰。

## 6. 第二层：子卡条件检查（L2）

固定的是**判断问题**，不是实现步骤。从子卡已有章节抽出这个机制**依赖的条件**和**关键失败**，不另写新卡：

| 项目 | 子卡章节 | 转成的问题 |
|---|---|---|
| HarnessRSI | Step-by-Step、Tactical failure mode | 每一步所保证的条件是否成立（例如“经验流与评测流分离”保证无泄漏）；该失败模式是否被排除 |
| CUA、Embodied | Operation、When it works、When it fails、Counterexamples | 生效条件是否成立；失败条件是否被排除；是否落入已知反例 |

每题取值：

| 取值 | 含义 |
|---|---|
| `holds` | 条件成立或失败已排除，不论论文用的是否是卡片里的做法 |
| `partial` | 部分成立，写清覆盖范围 |
| `fails` | 有材料显示条件不成立或失败出现 |
| `unknown` | 当前材料未覆盖；不当作失败，也不当作成立 |
| `NA` | 机制上不适用，写明原因 |
| `challenged_with_evidence` | 论文有证据表明该条件本身不必要或可替代 |

论文没有照卡片步骤做，不算 `fails`；只看条件是否被保证。同一子卡的论文用同一组问题，不能看完论文后挑它做过的条件。只报告覆盖情况，例如“适用 4 项：2 成立、1 部分、1 未知”，不折算成分数。没有合适子卡时记 `unassigned`，不扣分。

## 7. 每篇输出

每篇一条 JSONL；L2 在同一 `paper_id` 下另写一条，`stage` 为 `L2`，用 `supersedes` 指向 L1 记录，不覆盖原记录。

```json
{
  "paper_id": "2601.00000v1", "stage": "L1", "supersedes": null,
  "status": "assessed | needs_material | out_of_scope",
  "material": "abstract | abstract_intro | core | full",
  "problem_statement": "一句话，用论文自己的对象和条件",
  "problem_source": "author_claimed | card_supported",
  "families": ["F1"], "cards": ["main/<card_id>"],
  "card_anchor": "被挑战的认知障碍或失败模式要点，附卡片节名",
  "q1_basis": "measured_own", "q2_open": "challenges_barrier",
  "q2_prior": "若为 prior_solved，写先前工作 ID；否则 null",
  "later_work": null,
  "q3_change": "capability", "q3_loss": "问题造成的具体损失与解决后的改变",
  "q4_fit": "unknown",
  "problem_tier": "P3", "evidence_status": "pending_method",
  "priority": "high", "next_action": "to_l2",
  "subcard_checks": [],
  "facts": [{"loc": "§1 ¶3", "fact": "定位到原文的事实"}],
  "biggest_gap": "最大缺口及它会改变什么决定",
  "audit_sample": false
}
```

- `subcard_checks`（L2 填）：每项含 `card`、`section`、`question`、`verdict`、`paper_evidence`。
- `facts` 最多 2 条，必须有原文定位。`audit_sample` 标记是否为第 5 节的漏检抽查。
- worker 只写自己批次的文件。

## 8. 边界

- 作者声称和卡片印证分开记（`problem_source`）。Q2 只对照本项目卡片和论文自述的最近邻，不声称做过全网新颖性检索。
- 卡片在一次 run 中固定版本，不为匹配论文改卡；新机制记作后续卡片维护线索。
- 结构校验通过、引用存在、字段齐全都不代表科学判断正确，也不代表任何结果已复现。

## 9. 试点（全量前必做）

1. 三个项目各取 10 篇：至少覆盖 4 个问题族，包含 1 篇诊断／审计论文、1 篇疑似 `vertical_port`、2 篇只有摘要的记录、1 篇卡片只有它一个来源的论文（检查自我比较是否已排除）。
2. 全部跑 L1。对 L1 判为 `to_l2` 的论文跑 L2；**另外每个项目至少抽 3 篇 P0/P1、F0 或 `needs_material` 一并跑 L2**。
3. 用户人工看，验收重点：
   - 有没有漏掉值得读的论文，漏在哪一步、为什么；
   - L2 是否推翻了 L1 的判断；
   - 实际输入输出用量与人工复查负担。
   不追求档位分布好看。
4. 根据结果修订本文件（三处同步）和 PROBLEM_MAP，再由用户决定是否全量运行。
