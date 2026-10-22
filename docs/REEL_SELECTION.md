# 评分后选题：动态阈值与少量 Reel

状态：设计契约；待 rubric 校准冻结后实现 selector，不是已运行的自动选题器。
每期通常少于 10 篇，`max_items=9` 为默认上限而非必须凑够的配额；可以由维护者调小或另设明确上限。

## 输入与资格

只消费同一领域、同一冻结 rubric/profile 版本、同一比较类型的有效评分快照。
主榜类型 system_method / component_training / evaluation_resource 分开；跨类型或跨领域编一期时预先分配各池名额，不能混分数排序。
重复 paper/version 只能有一条明确有效的 judgment；新版本 supersedes 旧版本。重复冲突、rubric 混用直接停止选择并报告。

允许进入候选池的条件：

- 阅读完整、coverage=1、总分可重算、独立语义审核 passed 且 hash 对应当前 judgment。
- claim_support 是 supported，或 scoped 且收窄理由已审核、画报会明确披露；unsupported / contradicted / unresolved 不进正常精选。
- 不把缺证据/未审阅论文用推测高分补进来；负结果/审计研究可以凭它自己的结论支持度入选。
- 本期未做过同版本 Reel；实质更新才允许重做，并记录版本差异。

## 选择算法

参数：`quality_floor`（校准后由维护者设定，当前不写死为 60/80 等数值）、`max_items`（默认 9）、
`max_per_mechanism`（可选，同一主要机制过多时由维护者启用）、`batch_id`、明确的候选时间/语料范围。

1. 固定资格池，过滤 `score_raw < quality_floor`；比较未四舍五入分数，不用显示分数跨线。
2. 按 score_raw 降序；同分按 paper_id、version 的固定字典序。相同论文多个版本先按 supersedes 解决，不能靠 v9/v10 字符顺序选最新。
3. 如启用机制上限，使用已审核的主要操作分组（不是标题关键词），达到限额的论文记 deferred_redundancy；继续向下扫描合格候选。
4. 取最多 max_items 条。数量不足允许 0 篇，不自动降低 quality_floor、不拿低分填满。
5. 保存所有入选和未选原因。有效截断点 = 数量上限确实截断时的末位入选原始分数，否则为 quality_floor；它只用于说明，不替代明确名单。

这样质量底线固定时，论文多的一期实际入选分数会更高；维护者也可根据分数分布/制作预算调整底线后重新选择。
调阈值或上限只产生新的 selection snapshot，不重评论文，不改 rubric、权重或已冻结分数。
如果阈值附近集中在同一种机制，可以启用机制上限或少做几篇；不能为视觉多样性让低于底线的论文插队。

## 选题记录与发布

每期记录：selection ID/time、候选集合及其 hash、rubric/expectation/profile hash、评分文件 hash、参数、
各阶段数量（输入/有效/过线/去重后/入选）、selected IDs+versions+judgment hashes、有效截断点、同分和排除理由、操作者。
旧 selection 保留但标 superseded；无当前有效 selection 不启动 Reel。
`papers/` 可后续提供内部评分索引；对外画报入口只展示入选且成品 QA passed 的论文。
每期名额是制作预算，前端分页不是筛选机制；禁止先为全部论文做海报再过滤展示。

校准期不发布“高分精选”。冻结后可以先在选中名单中做 1–3 篇样片检查设计质量，再完成该期余下入选论文。
这不改变先评分、再阈值选题的顺序；样片不能绕过评分或拿旧分数作通行证。
