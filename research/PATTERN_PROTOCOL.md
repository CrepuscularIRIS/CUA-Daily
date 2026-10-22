# GUI Agents：严格沿用 ResearchStudio 15+31，迁移到领域判断

版本：v2.2，状态为评分执行协议草案。用户本轮明确要求使用原 15+31；本协议取代此前“只把原卡当可选参考”的表述。
固定原卡见 [reference](reference/researchstudio-15-31/README.md)。每篇的初评都必须进行原卡识别，再做领域模式判断，不能省略原卡层。
严格遵循的是原定义、操作签名、适用条件、主子卡关系及研究分析顺序；原规则允许无匹配，不能为了“严格”硬贴标签。
15+31 是研究模式数量，不是 46 个打分维度，也不要求三个领域各自恰好生成 15+31 张卡。

## 两层记录，不能混用

| 层 | 权威定义 | 记录 |
|---|---|---|
| ResearchStudio 原卡 | research/reference/researchstudio-15-31/ | `rs_pattern.primary`、supporting、sub_pattern；父类关系须命中 PARENTS.tsv |
| 本项目领域卡 | patterns/、research/patterns/taxonomy*.json | `domain_pattern.namespace=gui`、main、sub、条件/失败/期望与版本 |

原卡 ID 序列保持原文，例如 `controlled_diagnostic_design` / `rs:C02`；领域子卡引用必须写 namespace，不可用裸 C02 推断来源。
既有领域卡保留，先审计证据与映射；它们不能替代原卡识别。映射不是字符串翻译，不是一劳永逸的标签对照。
同一领域卡在不同论文里可能对应不同原卡；每篇必须给 operation/evidence 引用及映射理由。

## 每篇必须完成的识别

1. 阅读固定版本方法、实验、附录，写操作签名和 gap/最近邻。先确定论文执行什么，而不是先选好卡再套正文。
2. 浏览原 15 主卡 overview 与 31 子卡 overview；挑最接近的 1–3 主卡，打开卡全文，查定义、signature、when-to-apply、成功条件、失败与审稿关注。
3. 指定一张 primary、至多两张 supporting，只有不同操作确实需要它才选 supporting。无主卡适配填 outside_taxonomy 与原因，仍评价论文。
4. 子卡只能从对应父类选；可为空并说明具体差异。不要因术语相同、应用领域相同、用了多个模块而认定匹配。
5. 主卡匹配的每项都要绑定论文 operation/信息/条件；子卡写 tactic、step-by-step 里本篇执行/缺失哪些、为何区别于同父兄弟卡。
6. 对照既有领域卡：实际 object → feedback → operation → output → selection/retention（如适用），以及作用条件/失败边界。写原卡到领域操作的逐篇映射。
7. 分开记录 `executes_pattern` 与 `resolves_problem`。仅报告改进通常不能证明问题被关闭；声称 resolves 必须引用能支持该结论的证据，不能凭术语、名气或高引用。
8. 将成功条件、失败风险、审稿期望变成对这篇中心主张适用的具体问题，再进入 SCORE_SPEC；不计“匹配卡数”分，不将缺少失败报告奖励为成功。

每批报告 outside_taxonomy 比率；累计超过 30% 时按原 rubric 发 coverage warning，检查检索范围与领域差异。
这是覆盖诊断，不是强行重标以达标；scope 内但无匹配的论文不能因此被排除。不得为了降低比率改原卡定义。

## 从大量语料逆向归纳领域卡

批次中先保存逐篇 signatures、原卡匹配、领域卡匹配和未匹配操作；领域归纳必须引用这些记录及固定全文。
按操作＋信息可见性＋条件聚类，不按标题热词聚类。已有领域卡能够覆盖则补来源与边界；新机制才提出新卡候选。
独立工作至少两篇全文支持才可 candidate_pattern，单篇 case；每项条件/失败/反例都绑定来源，重复版本不算多篇。
保留原卡的分析栏目：definition、operational signature、when-to-apply、sub-pattern/tactic、step-by-step、
success conditions、failure modes、gap（何种执行把问题解决得更充分）、reviewer expectations、cognitive barriers、lessons。
没有实际审稿/录用标签时写 not_collected；gap 改为证据支持的执行差异，不编造 accepted/rejected 对比。

第一轮先在校准样本上检查映射；生产各轮积累 revision proposals，阶段末再聚合复核，保持稳定领域卡 ID。
批内禁止边改卡边打分。新卡/条件若影响评分，另建资产版本并列出受影响论文重评；纯来源增补也记录版本。
这一工作可交给 Open Scientist 的领域研究循环；不得改写其控制状态或把未核 proposal 标成 checked。
