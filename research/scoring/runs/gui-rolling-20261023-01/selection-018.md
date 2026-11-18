# Selection 018 — gui-rolling-20261023-01 增量轮

- 日期：2026-11-18
- 执行模型：glm-5.3（日班单席，指定配置）。不冒称旧提示词中的 Opus 5.5。
- 候选池 6 篇（P3 / confirmed / to_l3，全部未消费）：2510.11977（HAL）、2611.11306（ScrapeBench）、2611.22223（GapLeak）、2611.22591（PACT）、2611.22722（text-pixels）、2611.22971（SEAM）。
- L1 记录：batches/inc-l1-100.jsonl（2510.11977、2611.11306）、inc-l1-101.jsonl（其余四篇）。L2 最新记录：batches/inc-l2-54.jsonl（2510.11977、2611.11306）、inc-l2-55.jsonl（2611.22223、2611.22591、2611.22722、2611.22971，含 12:17 班产出）。
- 入选 3 / 发布 3 / fail 0 / correction 0。

## 1. 候选与近邻核对

| paper | 档位 | q3 / 族 | 主卡 | L2 记录位置 | 结果 |
|---|---|---|---|---|---|
| 2510.11977 HAL | P3 | judgment / F2,F3 | online_evaluation_methodology | inc-l2-54 | 编辑排除 |
| 2611.11306 ScrapeBench | P3 | judgment / F2,F4 | online_evaluation_methodology / agent_initiated_user_interaction | inc-l2-54 | 编辑排除 |
| 2611.22223 GapLeak | P3 | capability / F4 | injection_defense_isolation / environmental_injection_attacks | inc-l2-55 | 入选 |
| 2611.22591 PACT | P3 | capability / F1 | trajectory_level_policy_training / rule_reward_single_step_rl | inc-l2-55 | 入选 |
| 2611.22722 text-pixels | P3 | capability / F3,F1 | calibrate_simulator_to_real / structured_screen_observation | inc-l2-55 | 编辑排除 |
| 2611.22971 SEAM | P3 | capability / F2,F4 | online_evaluation_methodology / environmental_injection_attacks | inc-l2-55 | 入选 |

与现有 52 张 ready 的机制重复压力：

- **HAL** ↔ 第十四期 Harness Matters（2611.11971，scaffold×模型防御率）、第十七期 EVIDENT（2611.20488，证据支持审计）同属评测方法论族，连续第三期出现该族海报；HAL 的跨模型×跨 scaffold 排行榜基础设施与"更高推理努力 21/36 更差"是独立增量，但按机制/覆盖面优先+同族轮换原则让位。判断为编辑排除，非 L2 错误。
- **ScrapeBench** ↔ 法律合规全库首例，但与既有"表面合规 vs 实际行为"轴（2508.00935 聊天拒绝≠电脑不做、EVIDENT 表面成功 87%→有据 56%）在"检查了≠做到了"的呈现结构上同构（P4 robots 检查 100%/合规 14.2%），六篇内排位靠后。
- **text-pixels** ↔ 第七期 Stale Screenshots 感知域邻接；更重的是证据生态：MobileGym 中文模拟 app、reader 与 policy 同 Qwen 谱系、AndroidControl 迁移只剩 25.2% 降幅——对本雷达以真实 GUI 为主的覆盖面贡献弱于其余三篇。
- **GapLeak** ↔ 第二期 CAPED（2606.12666 隐私遮蔽）同隐私域但机制相反（遮蔽输入 vs 引导代理升级访问），互补不重复。
- **PACT** ↔ 训练侧信用分配全库少有近邻（第五期 AndroidFlux 检查点重排是推理侧）。
- **SEAM** ↔ 跨屏组合安全全库首例（现有注入/误用基准均单屏或恶意指令）。

## 2. 原文核对（全部经缓存全文，0 correction）

六篇均逐条核对 L2 引用事实与缓存全文（research/fulltext/<pid>.txt，FULLTEXT: html）。结果：**全部一致，0 条实质错误，0 条 correction**。要点摘录：

- **2510.11977 HAL**：21,730 rollouts、9 模型×9 基准、$40k、21/36 推理努力持平或更差、$171 vs $1577（9x 成本 2pp 差）、Online Mind2Web 均价 $450、专用 scaffold 胜 generalist（CORE 9/12、SWE 11/12）、Docent 六类 rubric、AssistantBench 猜模式/8 例 gold answer、订票误用信用卡、2.5B token 日志、TAU-bench Few Shot 因泄露剔除——均与 inc-l2-54 记录一致。缓存止于结论，附录 A2/A4/A7 未含，但 L2 引用事实全在正文。
- **2611.11306 ScrapeBench**：1895→1626 EP/269 NEP、139 无 ToS/77 无 robots、κ=0.91、P1 合规≈0（Grok 11%）、P5 >70%、P7 Claude 85.9%/Gemini 85.7%、P8 Claude 99.7% 合规但 98.5% 一刀切、GPT P4 检查 100%/82.8% 但合规 14.2%、69.7%+18.5%≈88% 法律解释失败、人类基线 n=180（48.9%/38.9%、读 ToS 67.1% vs 55.7%）——一致。
- **2611.22223 GapLeak**：威胁模型（合法文本无注入）、三阶段、RQ2 反例（编造邮箱 TS→0、travel SSE 反升）、RQ3（medical 48.2→6.1、travel TS 50→31.7、e-commerce PCS 21.7→56.7、挡提交不挡升级）、RQ4（OD 36.2/TPD 38.6/PCS 6/12 零、DoBrowser TPD 96.3%）、STV >96%、benign-complete 83.3%——一致。
- **2611.22591 PACT**：O 60.34→OA 61.21→OAR 62.93→PACT 68.97（+8.63）、OA C_rule 80.04（降）、ΔE：OA −31（High）/OAR +129/PACT −78、保留 89.51/92.37 vs OAR 86.34/89.07、净正确 +207/+313、fixed-plan 56.52→100、joint repair 43.33→63.33、同初始化同数据 KL η=0.01、单骨干 9B——一致。画报制作中发现初稿把 ΔE +129 误挂 OA 名下（实为 OAR），写作期修正，非 L2 错误。
- **2611.22722 text-pixels**：≥29.5 点 gap、复发 73.2/30.9、M≤0.70 vs 0.90、80.9 vs 55.6、lookup 70%、+11.5、25.62→1.56、27.03→2.92、AndroidControl 25.2%、500 张 63.4%——一致。
- **2611.22971 SEAM**：17.5–91.6% vs 1.1–22.0%、≥99.3%、≤3.6%（3/5 搁置良性）、91.8–99.6% 良性孪生、单屏区分 0.00/0/600 p<.05、全集 +0.88~+0.92、81–87%/50–69%（LLM judge）、150×27×8×49、3000 实例/6E ≤0.7 点、步预算 40 中位 11–12、温度 0.2 复跑 ≤2 点——一致。

## 3. 阅读范围

| paper | 阅读材料 | 未读部分 |
|---|---|---|
| 2510.11977 | 缓存全文（正文至结论，含 §2–§4 全部关键数字） | 附录 A2/A4/A7/A9/A11、图 2/3/4 高分辨率版 |
| 2611.11306 | 缓存全文（§1–§8 全） | 附录 B/E（标注 prompt、人类基线 UI 截图）、图 3–6 高分辨率版 |
| 2611.22223 | 缓存全文（§1、§3–§7、Table 2、Figure 4–6 数字均在正文） | §2 Related、§4 实现细节、附录 A–G |
| 2611.22591 | 缓存全文（§1、§3–§8、Tables 1–6） | 补充材料（S1–S8 图、S1/S3 表） |
| 2611.22722 | 缓存全文（§1、§3–§7、Tables 1–5） | 补充 Sec B–K |
| 2611.22971 | 缓存全文（§1、§3–§4、§6） | §2 Related、§5 正文未在缓存（引用自 §1 发现(i)-(iii)与 §4）、附录 D–R |

## 4. Correction 与待补

- **0 条 correction**：六篇 L2 记录与全文核对全部一致。
- 待补（不影响本期判断）：SEAM 缓存缺 §5 正文（只有 §1 转述），若后续引用 §5 细节数字需先补抓；HAL 附录 A2（Docent precision 表）未在缓存。

## 5. 成品与 QA

| paper | 版式 | 尺寸 | PDF | QA | 备注 |
|---|---|---|---|---|---|
| 2611.22971 SEAM | 深青蓝双屏最小对证据卡 | 1400×3100 | 1 页 | ready | 首版画布 2600 溢出→预检修 3100（成品落盘前，不消耗重做额度）；实际打开 PNG 全图+三块全分辨率裁图核过 |
| 2611.22591 PACT | 浅纸色训练账本 | 1700×2650 | 1 页 | ready | 同上口径（2200→2650）；ΔE +129 归属写作期自纠（OAR 非 OA），SOURCE.md 勘误节记录 |
| 2611.22223 GapLeak | 白底红黑泄压图 | 1500×2880 | 1 页 | ready | 同上口径（2500→2880） |

三张版式互不相同，且与近三期（15/16/17 期）版式不重名：15 期=手机界面示意+覆盖率条+哑铃+森林图；16 期=米色计票账本/非对称机制侧栏；17 期=暖米色三步重试流/紫灰纵向审计账单/蓝色硬件双栏板。本期 SEAM 的"双哑铃"与 15 期"哑铃"同为对比条形态但配色、布局、上下文（深青蓝证据卡 vs 手机界面示意）不同构；PACT 阶梯条与账本隐喻不同于 16 期米色计票账本的表格骨架；GapLeak 攻击链纵向流与 17 期三步重试流都含"步骤"但内容结构（双层范围卡+矩阵表）不同。字体为本地 Noto Sans CJK SC 的 woff2 子集（fontTools 生成，含粗体），渲染无远程请求。

各目录含 poster.png / poster.pdf / SOURCE.md / QA.md / assets/render-check.json 及本地可编辑 poster.html（HTML/assets 沿用既有 .gitignore 忽略规则，不修改 .gitignore）。

## 6. 索引维护

- reel/README.md：追加第十八期表格与说明，头部无总数字段需改（分节计数在每期末行）；十七期末行 52 篇/rolling 33 保持历史记录，本期末行新增 55/36。
- 根 README.md 第 9 行：`52 posters in Reel (33 from rolling run ...)` → `55 posters in Reel (36 from rolling run ...)`。

## 7. 提交

单条 commit：`reel: selection-018 (SEAM, PACT, GapLeak — 3 ready, 0 fail, 0 correction)`。只 add 本期产出路径（reel/2611.22971、reel/2611.22591、reel/2611.22223、reel/README.md、README.md、本文件），不含工作区既有的 Grok 预删 inbox 改动，不 pull/push/rebase。
