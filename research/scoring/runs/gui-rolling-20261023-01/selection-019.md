# selection-019 — gui-rolling-20261023-01 增量轮

- 日期：2026-11-19
- 执行模型：glm-5.3（单席串行，不冒称旧提示词中的 Opus 5.5）
- 候选池：4 篇（P3 / confirmed / to_l3，最近 7 天新确认，全部未发布）
- 结果：入选 3、编辑排除 1、发布 3、fail 0、correction 0

## 候选与 L2 核对

| paper | L2 最新记录 | 核对结论 |
|---|---|---|
| 2510.11977 HAL | inc-l2-54（11-18 04:10）q1 measured_own / q2 open_failure / q3 judgment / F2,F3 / online_evaluation_methodology | 与全文一致 |
| 2611.11306 ScrapeBench | inc-l2-54 q1 measured_own / q2 open_failure / q3 judgment / F2,F4 / online_evaluation_methodology + agent_initiated_user_interaction | 与全文一致 |
| 2611.22722 text-pixels | inc-l2-55（11-18 06:36）q1 measured_own / q2 challenges_barrier / q3 capability / F3,F1 / calibrate_simulator_to_real + structured_screen_observation | 与全文一致 |
| 2611.15600 MemCredit | inc-l2-45（11-13，supersedes inc-l1-91#2611.15600）q1 measured_own / q2 new_bottleneck / q3 judgment / F2,F5 / experience_memory_retrieval + agent_loop_context_control | 与全文一致 |

四篇均逐篇核对 `research/fulltext/<pid>.txt` 全文缓存与 L2 最新记录，判断口径一致，无 correction。

## 终选（3 入选 / 1 排除）

### 入选 2611.15600 MemCredit

- 池内唯一 q2 new_bottleneck：记忆条目"相关但不该带上"的效用归因缺失。机制完整可讲：五型原子记忆 → 预算匹配参考上下文配对环境重放取 signed credit → ExtraTrees 效用回归 → 在线贪心逐条插入，相关性只做召回不做仲裁。
- 与 55 张 ready 的机制重复压力：experience_memory_retrieval 已有 StreamEmbed（2611.18516，编码吞吐轴）与 2409.07429（信息边界归纳轴），但"以环境重放定价记忆条目"的效用归因轴均未覆盖；agent_loop_context_control 侧与 PACT（2611.22591，训练侧信用分配）同是 credit assignment 但一个在记忆检索、一个在计划/动作，不构成同卡。
- selection-016 曾以"证据完整度"编辑排除（附录 A.1 shaped reward、WebShop 协议细节缺失）。本缓存含完整 Table 2（0.612/152.1 vs MemArbiter 0.586/427.6 等）与 §3 方法全协议；附录 A.1 仍不在缓存，画报 SOURCE.md 如实注明"WebShop 干预次数与置信区间未在正文给出"。上期未消费，本期入选。

### 入选 2611.11306 ScrapeBench

- 法律合规的动作通道测量，真实站点规模（CrUX top3000→1895 站，EP 1626/NEP 269，κ=0.91 抽检）。
- 与 55 张 ready 的机制重复压力：与 2508.00935（聊天拒绝≠电脑不做）同在"声明/检查 vs 动作背离"呈现轴，但对象不同（站点 ToS/robots 合规 vs 用户指令拒绝）、数据源不同（真实站点标注 vs 自建双通道）；与 EVIDENT（2611.20488）"检查了≠做到了"有呈现重叠。选其独有轴：8 级压力阶梯 × 检查/合规背离（GPT robots 100% 检查/14.2% 合规）× 违规理由拆解（69.7% 无视 ToS + 18.5% 误读）× 人类基线（48.9%，行动跟随所读）。此定位写进 reel/README.md 表格。

### 入选 2611.22722 text-pixels

- 证据链干净的机制因果：−44.5 点落差跨五种训练法稳定（含三种已花截图的，全部 ≥29.5 点）→ 误读系统性（73.2% vs 30.9%，同错字 98.9%）证明注噪抓不住结构 → 读屏器对齐的预算对照（同一笔 2000 张：80.9% vs 55.6%，另两实例集 +27.6/+26.6 复现）→ 传染性（救回三个纯文本策略 ≥24.0 点）。
- 上期（selection-018）排除理由——中文模拟生态弱、reader/policy 同 Qwen 谱系、屏幕精确重复 36.9%——本期不回避：全部以画报"部署边界"卡如实呈现（留出 app 70.4% vs 73.6% 无差异、MobileGym 中文模拟口径、lookup 回收 70% 增益配 27.03→2.92% 新屏误读率侧证）。
- 与 55 张 ready 重复压力：calibrate_simulator_to_real 无在库（迁移轴仅 VEX 的教程条件）；structured_screen_observation 在库有 Accessibility Debt（2611.16107，标注覆盖轴），text-pixels 是读屏器误读结构轴，不同卡。

### 排除 2510.11977 HAL（编辑排除，不改 L2）

- 评测方法论族连续第四期出现（014 Harness Matters 2611.11971、017 EVIDENT 2611.20488、018 已让位一次），族轮换原则下继续让位。
- 核心呈现轴（外壳×模型矩阵对完成率/防御率的影响）与在库 2611.11971 重叠，机制无增量；gap（21/36 推理努力无显著性检验等）为评测工艺层面，非新机制。selection-018 已以同族压力排除过一次，本期待池内竞争者机制更强，维持排除。

## 画报与 QA 全账

| poster | 画布 | 画布预检 | 重做 | fail | QA |
|---|---|---|---|---|---|
| 2611.15600 MemCredit | 1500×2660 | 首版 2760 收紧一次（预检口径，不占额度） | 0 | 0 | ready |
| 2611.11306 ScrapeBench | 1500×2780 | 首版 2680 contentBottom 2695 超 15px，加高一次（预检口径） | 0 | 0 | ready |
| 2611.22722 text-pixels | 1500×2820 | 首版 2700 contentBottom 2715 超 15px，加高一次（预检口径） | 0 | 0 | ready |

- 三张版式互不相同，且与近三期（017/018）已用骨架不同：MemCredit 暖沙色"账本+分光镜"、ScrapeBench 冷灰蓝"合规检核单"、text-pixels 深墨绿"文本⇄像素双世界"。
- 每张 poster.png 三段裁图逐一目检（溢出/裁切/重叠），PDF 均单页，render-check 全部 pass。字体 pyftsubset 子集嵌入，无 tofus。
- 数值修正：ScrapeBench 初稿 P3 占位值 31.2% 渲染前对照 §4.1 改 40.1%（成品前修正，非重做）；其余两张无数值修正。
- 五件套（poster.png/poster.pdf/poster.html/SOURCE.md/QA.md）齐全；poster.html 与 assets 字体受旧 .gitignore 规则仅存本地。

## 数量账

- Reel 合计：55 → **58**（rolling run 36 → **39**）。根 README.md 头部与 reel/README.md 尾部节同步更新。
