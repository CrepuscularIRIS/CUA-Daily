# SOURCE · 2508.00935

- 论文：Tian, Zhang, Tang, Wang, Shi, Wen. *Measuring Harmfulness of Computer-Using Agents*（CUAHarm）。
- 版本：arXiv 2508.00935**v3**（HTML 页头标 03 Sep 2026；首版 2025-07-31）。
- 阅读材料：`research/fulltext/2508.00935.txt`（v3 HTML 提取，缺 §2 与附录）；附录 A–D、表 3–5 由 https://arxiv.org/html/2508.00935v3 补齐，只存 /tmp，不提交。
- 初筛记录：run `gui-pc11-20261022-01`；L1 `batches/p022.jsonl`，L2 `batches/l14.jsonl`（P3 / judgment / F2,F0 / verifiable_execution_reward + online_evaluation_methodology）；入选见 `selection.md` 第 4 行。

## 数字与断言 → 原文位置

| 画报内容 | 原文 |
|---|---|
| 104 任务 = 52 恶意电脑任务 + 52 常见恶意提示 | §3 首段；表 5 题注（CUT / CMP） |
| 指令 / 配置 / 评估器；快照复位；≤15 步 | §3.1、§3.2 |
| 检查器例：`sudo ufw status` 是否 inactive | §3.3 |
| Refusal＝因显式拒绝而未通过评估 | §3.3 |
| 终端 CUA 给 sudo 密码；单次 pass@1；温度 0 | §4.1、§4.2；附录 A.1/A.2 系统提示 |
| 聊天与 CUA 指令相同、只换系统提示 | §4.3「LMs robust to malicious prompts…」段 |
| 聊天设置另列各家网页界面 | 附录 A.3 表 2 |
| 聊天拒绝 / 合规、CUA 执行（9 模型） | 附录 B 表 3(b) |
| 终端 vs GUI 完成率与拒绝率（9 模型）；UI-TARS-1.5 42.3 | 附录 B 表 3(a)；§4.3 |
| 9 模型平均 GUI 28.0 | §4.3（作者给 28%）；表 3(a) 复算 28.0 |
| 9 模型平均终端 65.2 | 我们由表 3(a) 计算（论文未给） |
| Gemini 2.5 Pro 终端 90.4% | 摘要；表 3(a) |
| GUI 失败原因：开 Chrome/LibreOffice 跑偏、点不中按钮 | §4.3「CUAs pose greater risks…」段 |
| 良性变体：Claude 3.7 拒绝 30.8→0，成功 59.6→82.7 | §4.3 末段（拒绝 30.8 取自表 3(a)，正文写「降为 0%」） |
| 监控：任一步标记即检出，分母为恶意任务；65–85% | §4.4 |
| 监控 57.7–86.5%，均值 76.9（摘要「77%」） | 表 4 w/ CoT 列（4 监控 × 9 CUA，均值为我们复算） |
| 限制：Linux、无中途攻击者干预等 | §6；规则核对方式见附录 D |

## 我们的推算（非作者结果）

- 背离账本「交叉 ≥ N 条」：N = max(0, 聊天拒绝条数 + CUA 执行条数 − 52)，条数 = 表 3(b) 百分比 × 52 取整（全部取整误差 < 0.05 条）。只是下界；论文没有逐条配对，格子排布为示意。
- 两个平均值（终端 65.2、监控 76.9）由表格算术得到。

## 示意部分

- ① 双通道机制图、全部图标、② 格子的位置排布均为自绘示意，不是论文原图。
- ① 中「生成一篇假新闻」取自 §3 对常见恶意提示的举例；`ufw` 例取自 §3.3，属于恶意电脑任务，图中已注明。
