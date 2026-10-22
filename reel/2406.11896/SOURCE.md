# SOURCE · 2406.11896 DigiRL

- 论文：DigiRL: Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning，Bai, Zhou, Cemri, Pan, Suhr, Levine, Kumar
- 版本：arXiv **2406.11896v1**（2024-06-14）。abs 页只有 v1，没有后续版本。
- 阅读材料：`research/fulltext/2406.11896.txt` 是裁剪版，缺 §1 后半、§2–§3、全部附录。已按 v1 HTML 全文（`https://arxiv.org/html/2406.11896`，本地 /tmp，不提交）补读 §1–§6、App. A–I。Fig. 6/7/8/9 在 HTML 里是图像，正文和图注里的说法已读；图中的柱高和曲线点没有读数，画报也没有使用这些读数。
- 初筛记录：run `gui-pc11-20261022-01`。L1 记录在 `batches/p007.jsonl`，L2 记录在 `batches/l*.jsonl`（stage L2，status confirmed，P3 / capability / F3）。selection.md 第 7 行。

## 数字与断言映射

| 画报位置 | 内容 | 原文出处 |
|---|---|---|
| 标题副行、①②③标牌 | General 14.6 / 61.5±1.1 / 71.9±1.1；Shopping 17.7 / 57.8±2.6 / 67.2±1.5 | Table 1 测试列：AutoUI、Off-to-On Filtered BC、Off-to-On Ours |
| 标牌注 | 离线 3 次、在线 2 次，均值±标准差 | Table 1 图注 |
| 横梁 | AutoUI-Base = 1.1B 视觉编码器 + 200M LM；FBC 和 DigiRL 从训练好的 AutoUI-Base 检查点出发，冻结图像编码器 | §5 “Baselines…”“Base VLM and offline dataset” |
| 横梁 | 测试取 General / Web Shopping 测试集的前 96 条，所有行都由自主评估器判定 | Table 1 图注；App. A.1 |
| 横梁、研究动作 | 评估器以 Gemini 1.5 Pro 为骨干，用少量人工标注的 few-shot 示例；只看任务和截图，不读模拟器内部状态 | §3 “Setup for reliable…”；App. G |
| ① 侧壁 | AutoUI 在包含 AitW 的人类演示上做监督训练；它是 ②③ 的初始检查点和离线数据的采集策略 | §5 “Baselines”“Base VLM and offline dataset” |
| ② 侧壁 | 离线→在线：起步离线轨迹 General 608 / Shopping 528 条，再加约 1000 条在线轨迹；每轮 16 条 | §5；App. A.1；App. I Table 7（rollout trajectories 16） |
| ② 侧壁 | FBC 保留判成功的轨迹做 BC，方法沿用 [26] Pan et al.（arXiv 2404.06474） | §2 第三类相关工作；§5 (c)；参考文献 [26]。正文没有重写 FBC 的过滤规则，这一条是我们依据 [26] 和 §5 “DigiRL 离线阶段改用全部成功轨迹”做的概括 |
| ③ 侧壁 | 指令级价值 A^instruct = r − V^instruct(c)，取 top-p；步级双稳健优势阈值 1/H；价值函数用交叉熵训练；演员用 MLE | §4.2 式 4.3；§4.3 式 4.4–4.6；Fig. 5 图注 |
| ③ 侧壁 | 两种方法的学习率、批量、缓冲区相同 | App. I Table 7 |
| 级差 | +46.9 / +40.1，+10.4 / +9.4 | 计算：Table 1 测试列逐项相减 |
| 图例 | General H=10，Shopping H=20 | App. A.1 |
| 梯外 · 纯离线 | FBC 50.7 / 45.8，DigiRL 62.8 / 45.8；约 1500 条（G 1552 / S 1296） | Table 1 Offline 行；§5；App. A.1 |
| 梯外 · 其他 | CogAgent 25.0 / 38.5；GPT-4V SoM 13.5 / 8.3；Gemini SoM 16.7 / 11.5；AppAgent GPT-4V 17.7 / 8.3；AppAgent Gemini 16.7 / 8.3 | Table 1 测试列 |
| 梯外 · 不一致 | §5.1 “17.7→71.9”“57.8→61.4”“75% vs 62.8%”；§6 “17.7→68.2” | §5.1 Main Results / Comparison of RL approaches；§6 |
| 2 左 · 公式 | A_step 定义，λ = 0.5 | 式 4.3；App. I Table 7（GAE λ 0.5） |
| 2 左 · 消融 | 交叉熵价值函数约 +12%，步级优势提效约 12%，自动课程提速约 25%（Web Shopping） | §5.2 “Ablation study”；Fig. 9 左图注 |
| 2 右 · 网站在变 | 用 6/1–6/3 数据训练的检查点，在 6/7–6/11 冻结使用时退化，持续更新的版本保持住 | §3 “Challenges of stochasticity”；Fig. 4 图注 |
| 2 右 · 失败类型 | 人工标注三类失败；作者称 RL 对“犯错后无法恢复”的减少最一致；举例：AutoUI 误触语音输入后退不出来 | §5.2 “Failure modes analysis”；Fig. 7 图注；§5.1；App. C.2 |
| 限制 | 模拟器加实时网站；Shopping 只含 5 个网站和 3 种操作；与人工判定差 <3%，平均误差 2.8%；Fig. 8 每种配置只报最高分那次运行；两次在线运行在不同日期启动 | §3；App. A.1；§1；§5.2；Fig. 8 图注；Fig. 6 图注 |

## 自绘与示意

- 阶梯本身是我们按 Table 1 数字等比例绘制的（7 px 对应 1 个百分点，纵轴从 0 起），不是原论文的图。
- “同一条成功轨迹，两种过滤”中的 bestbuy 轨迹和被丢弃的那一步是示意，用来说明式 4.3 的作用，不是论文里的实测轨迹。
- Fig. 4 的两条曲线是示意，只画出作者描述的走向，原图没有读数。
- 所有图标（演示文档、手机、循环、漏斗、价值表）均为自绘示意。
