# 2608.21794 画报来源映射

- 论文:Lexical Coupling in GUI Element Grounding: Sentence Embeddings Track Labels across Mobile and Web(Qijia Chen & Giulio Jacucci,University of Helsinki;cs.CL)
- 版本:**2608.21794v1**(2026-08-22)
- 材料:`https://arxiv.org/html/2608.21794v1` 本地缓存 `/tmp/2608.21794.html`(完整正文 + 附录 A–P,未提交);补充 `research/fulltext/2608.21794.txt`(core 裁剪)
- 初评记录:`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`(G4/M4/X4/E4,screen 100,claim_support=supported_in_material)
- 核对:`research/v3/runs/gui-v3-20261022-01/verify/2608.21794.md`(verdict: verify_ok)
- 仅阅读原文,未运行代码,不构成复现。所有图形均依据原文数字自绘,未使用原文图片。

## 标题 / 关键动作区

| 画报内容 | 原文定位 |
|---|---|
| 测量审计,不提新 grounding 模型 | §1 "this paper is an audit of how GUI grounding is measured, not a proposal for a new grounding model" |
| 同屏排序;中位 62 个候选 | §3.1 AndroidControl("median 62 per step");§3.3 |
| 词法与编码器读同一份文本串 | §3.4 |
| 5 个编码器及参数量(22M/110M/335M/335M/0.6B) | §3.5 |
| BM25 每屏独立 IDF | §3.5 BM25 段 |
| episode 簇 bootstrap,B=2000,95% 区间 | §3.9 |
| "tap Settings" 例子 | §5 Benchmark-design recommendations("tap Settings" while viewing a button labeled "Settings")。屏幕列表(Wi-Fi/Display 等)为**示意**,非原文数据 |
| 遮蔽后回退 resource_id / 类名 | 附录 G("textualisation falls back to the target's resource_id or class name") |

## 级联矩阵(R@1)

| 层 | 数值 | 原文 |
|---|---|---|
| 0 原样排序 | n=32,646;随机 .022;Jaccard .547;BM25 .557;MiniLM .489;MPNet .467;BGE .520;E5 .507;Qwen3 .481 | 表1、§4.1 |
| 0 注 | BM25 高于全部 5 个编码器,配对 CI 均不含 0 | §4.1、附录 E(表5) |
| 1 隐藏目标文字 | 等配额三层抽样 n=3,000(每层 1,000);只清空目标 text/content_description | 附录 G 正文 |
| 1 数值 | BM25 .508→.125(−.383);MiniLM .487→.165(−.321);MPNet .434→.139(−.296);BGE .503→.188(−.315);E5 .470→.159(−.311);Qwen3 .466→.251(−.216) | 表6 |
| 1′ 微调对照 | held-out 测试子集 n=2,949;BM25 .558→.134(−.423);零样本 MiniLM .518→.178(−.340);微调 MiniLM .694→.151(−.542,CI [−.562,−.520]) | 表12、§4.4 |
| 1′ 注 | 微调比 BM25 高 13.6pp;LCC .877(零样本 .865) | §4.4、表11 |
| 2 无可读标签 | 表2 全部 DB 行:text-only n=21,539(BM25 .624 / Mini .520 / MPNet .504 / BGE .563 / E5 .552 / Qwen3 .507);resource-only n=9,669(.064/.085/.085/.099/.095/.124);none n=13,132(.013/.016/.011/.006/.006/.020,随机 .027) | 表2 |
| 3 融合 | 表8 n=32,646,BM25=.555;oracle Δ:+.033/+.071/+.060/+.062/+.144/+.151(R@1 .706);真 RRF Δ:+.023 [+.021,+.025] / +.012 / +.011 / +.005 / −.011 / −.009 [−.013,−.005](R@1 .546) | 表8、§4.5、附录 I |
| 3 注 | "破坏性融合" 命名 | §5 "a pattern we name destructive fusion" |
| 3 注 | 校准线性融合 4 个编码器 +1.46~+2.81pp;BGE α=1.00 退化为 BM25;oracle +5.97~+6.88pp | 附录 J(表9,val 调参) |

**分母说明**:各层样本不同(32,646 / 3,000 / 2,949 / 表2 分层 / 32,646),画报已在每层标注 n 与出处,并提示不跨层比较绝对值。BM25 clean-main 在表1 为 .557、表8 为 .555(原文内部差 0.002),层 0 用表1、层 3 用表8,同层内不混用。

## 底部三栏

| 画报内容 | 类型 | 原文 |
|---|---|---|
| 命中可由词法秩、候选池大小、标签类型预测;LCC .825–.882 | 作者结果 | Abstract;表4(三语料 LCC 最小 .825 MoTIF-MPNet,最大 .882 AC-E5) |
| MoTIF、Mind2Web 无编码器在 R@1 显著超过 BM25 | 作者结果 | §4.2、表3 |
| 报告建议(词法基线 / 分层 / 遮蔽 / oracle 与可部署分开) | 作者结果 | §5 Reporting recommendations |
| "我们的读法"三条 | 我们的阅读判断,非原文结论 | 依据表1、表2、表6、表12 数值 |
| 只评文本元数据排序,不覆盖截图/OCR/像素 grounding | 限制 | Limitations 第 1 段 |
| 不评在线 agent 行为 | 限制 | Limitations 第 2 段 / 附录 N(不预测下游行为);§2 端到端 agent 在范围外 |
| 遮蔽为目标感知诊断;等配额均值非语料加权 | 限制 | 附录 G 末段;初评 caveat |
| LCC 是描述性 AUC | 限制 | §3.7(descriptive high-coupling regime, not a hypothesis-test cutoff) |
| 仅单向量编码器 + RRF/线性融合 | 限制 | Limitations 第 3 段 |
