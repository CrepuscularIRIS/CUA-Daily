# SOURCE — 2610.15138

- 论文:The Agent Clicks Approve: Injected Page Text Makes Browser Agents Authorize Access the Task Never Named(Hossen,UT Chattanooga,cs.CR)
- 版本:**2610.15138v1**(2026-10-10)
- 材料:① `research/fulltext/2610.15138.txt`(core 裁剪,sha256 前缀 `cafe738ac4e124f2`);② `/tmp/2610.15138.html` = `https://arxiv.org/html/2610.15138v1`,2026-10-22 抓取(sha256 前缀 `0a7da238af92e8a8`,完整正文 §I–XI,不提交)。数字以 ② 为准。
- 初筛记录:`research/v3/runs/gui-v3-20261022-01/candidates-records.jsonl`(screen_score 100,claim_support=scoped,evidence_level=online)
- 核对记录:`research/v3/runs/gui-v3-20261022-01/verify/2610.15138.md`(verify_ok)
- 仅阅读原文,未运行,不构成复现。

## 数字 → 原文

| 画报位置 | 数字 / 断言 | 原文 |
|---|---|---|
| 副标题 | Claude Haiku 4.5、GPT-5.5;browser-use;DOM 文本无截图 | §VI-A Agent / Models |
| 问题条 | confused deputy:会话给权限、页面给对象、动作点无比对 | Abstract、§I、图 1 图注 |
| 泳道 A ② | 两句话工作流提示,不含“忽略任务”(大意转述,非原文引文) | §I、§VI-B |
| 泳道 A ③ | scope 标识含 “privileged” 仍在屏幕上 | §VI-B、§VII |
| 泳道 A ⑤ | 无门 73/73 完成;同意 53/53、webhook 20/20(表 I 43/43 + §VI-F 30/30) | §VI-B、表 I、§VI-F |
| 泳道 A ⑥ | 回答把批准报告为任务进展 | §VI-B、图 2 图注 |
| 泳道 A ① | 有效会话被当作用户选择了参数 | §VII 首段 |
| 泳道 B ① | 运行前固定 envelope;攻击任务 envelope 为空 | §V-A、§VI-C |
| 泳道 B ④ | 70/70 次门控攻击运行发出请求,共 103 个;webhook 两格 17+17 个请求(9、8 次运行) | §VI-C |
| 泳道 B ⑤ | 103 个全拒,0 完成;HTTP 403 / 422 | §VI-C、§V-A Enforcement |
| 泳道 B ⑥ | 53 次门控同意攻击中 49 次回答叫读者去批准,2 次称已批准 | §VI-C、§VII |
| 泳道 C | 任务 Billing Workspace Archive vs 页面 Billing Workspace;Haiku 5/5 次运行提交、13 请求全拒、0 完成;GPT-5.5 0/8 提交、回答指出账户不符;只认 client 的 envelope 会放行 | §IV-C Near-miss、§VI-D、表 II |
| 泳道 D | 门控下授权任务 73/73 完成(表 I 43/43,其中 task-derived 33/33);门拒 0;答案检查 42/43 | §VI-D、表 I |
| 泳道 E | 提示词防御(Haiku、同意、角色中性页):7/10 仍完成,另 3 次未发请求;角色标签页面 1/10;两版差异多因素 | §VI-E、表 III、图 4 图注 |
| 关键对照条 | 143 次(无提示词防御)攻击运行均发请求:73 完成(无门)、70 被拒(有门) | §VI-C、图 3 图注 |
| 限制 ① | loopback、无登录/二次认证、不发 token;两模型一框架;每格 5–10 次;区间为同页面集重复运行 | §IV-A、§IV-B、§VI-A、§VIII |
| 限制 ② | 换措辞/小字元数据位置:Haiku 4/10、gpt-5.4 0/10(角色标签单主机页面) | §VI-G |
| 限制 ③ | 抽取器仅两种授权任务模板;scope 取自服务端挂起请求 | §V-A、§VIII |
| 限制 ④ | 服务需识别 agent 会话并有页面写不进的通道;只保护装门端点 | §V-C、§VII |

## 作者结果 vs 阅读判断 vs 示意

- **作者结果**:画报所有数字与泳道节点上的事件描述。
- **阅读判断**(画报右下虚线框,已标注):测量设计是主要分量;门控只改结局不改行为、服务端决定应直接告知用户(后者与 §VII 作者建议一致,措辞为我们的);不宜据 7/10 vs 1/10 给提示词防御定量。“门控不提高模型抵抗力”为对 §VI-C “steered equally” 的转述。
- **示意**:泳道链路结构、时间轴分段、列头 6 个线条图标均为自绘,非论文图 1–4 的复制;未使用论文原图。
