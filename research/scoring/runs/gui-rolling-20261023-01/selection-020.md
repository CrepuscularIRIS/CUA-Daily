# selection-020 — gui-rolling-20261023-01 增量轮（日班单席）

日期：2026-11-21 · 执行模型：**glm-5.3**（实际执行模型，单席串行，不冒称提示词模板中的 Opus 5.5） · 仓库：cua-architecture-radar · 规则：problem-core-v1.1

## 候选池与核对（3 篇，P3/confirmed/to_l3，7 天窗口，全部未发布）

| pid | 论文 | L2 批次 | 全文核对 | 结论 |
|---|---|---|---|---|
| 2510.11977 | HAL 跨模型评测方法论 | inc-l2-54 | 一致（§1–§5；附录 A2/A4/A7/A9/A11 不在缓存） | 编辑排除（第五期同族压力，理由与 selection-019 一致） |
| 2611.24977 | CANDID 本地 CUA 环恢复＋全票 DONE 门控 | inc-l2-56 | 一致（缓存缺 §2+Table 1，见 L2 biggest_gap） | 入选，发布 |
| 2611.25387 | TuringSpace 程序化空间行动环基准 | inc-l2-56 | 一致（缓存缺 §2+失败分析，见 L2 biggest_gap） | 入选，发布 |

核对零 correction：三篇 L2 字段（problem_tier/q1–q4/主卡/卡锚）与缓存全文逐项一致，无判断错误退回 Sol。

## 编辑判断与终选理由

**入选 2：**

- **2611.24977 CANDID（F5 执行控制 / capability）**：池内唯一的执行控制新机制证据，卡锚 agent_loop_context_control＋simulated_lookahead_selection。核心轴"候选分歧做执行信号"：文本反馈无效（35.31→33.30）、per-step 逐点采样崩到 23.48% vs 稀疏 38.80%（Table 6）、候选 1→4 升 4→8 递减（Fig 6）——稀疏分歧信号优于密集干预的证据链完整；全票 DONE 门控作者自认只是保守过滤器（precision 56.7%），画报如实呈现。与在库 GTA-1（2611.04879）的计划采样不同轴（计划层 vs 执行层）。
- **2611.25387 TuringSpace（F2+F5 空间行动环 / capability，池内唯一 q2 new_bottleneck）**：MCQ 可猜/DOM 暴露使"答对"不构成理解证据→程序化无限实例＋终态 checker 从根上关掉两条泄漏路径；9B 微调 1.6→33.1 超 Kimi K3 且 7/7 OOD 上涨、ReCAP 反向 ≤1.6%，方向性证据强。与 PointerBench（粒度轴）、Accessibility Debt（标注轴）不同卡。

**排除 1（编辑排除，不改 L2）：**

- **2510.11977 HAL**：与 selection-019 排除理由一致——评测方法论族本期再遇同族压力（014 Harness Matters 2611.11971、017 EVIDENT 2611.20488、018/019 连续两期排除或让位，本期为该族第五期出现）；核心呈现轴（外壳×模型矩阵）与 2611.11971 重叠、机制无增量；其 gap（21/36 无显著性检验）属评测工艺而非新机制。018 让位、019 编辑排除的先例路径本期延续，L2 判断本身无误，不写 correction。

**缓存缺口处理**：CANDID 缺 §2+Table 1（"scaling 只挪不移"仅引言断言，画报注记 §4.3 消融间接印证）；TuringSpace 缺 §2+失败分析（"推理虚构证据辩护"仅摘要级，画报边界卡注明不引用其量化）。两处 biggest_gap 已在 L2 记录，画报全部避开未缓存小节。

## 画报与 QA 全账

| pid | 版式 | 画布 | render-check | 视觉 QA | 重做 | fail |
|---|---|---|---|---|---|---|
| 2611.24977 | 深紫夜色执行舱（候选芯片＋双闸门＋哑铃） | 1500×2880 | contentBottom 2870 / overflow [] / fontOK / PDF 1 页 → pass | 全图＋4 段全分辨率裁图逐段目检通过 | 0 | 0 |
| 2611.25387 | 浅纸色验证馆（五类卡＋九行榜＋方向性迁移） | 1500×2820 | contentBottom 2730 / overflow [] / fontOK / PDF 1 页 → pass | 全图＋4 段全分辨率裁图逐段目检通过 | 0 | 0 |

每张画布预检一次达标（不占重做额度）。字体为本地 Noto Sans CJK SC woff2 子集，渲染无远程请求。渲染工具为本期临时脚本 reel/render_poster.py（未入库）。

## 数量账

- 候选池 3 → 核对一致 3（0 correction）→ 编辑排除 1（HAL）→ 终选 2 → 发布 2（0 重做、0 fail）。
- Reel 总量：58 → **61**；rolling run：39 → **42**（reel/README.md 末行与根 README.md 头部已同步）。
- 提交：单条 commit，仅含本期产出路径（两张 poster 的 PNG/PDF/SOURCE/QA、reel/README.md、README.md、本文件）；工作区 Grok 预删的 inbox/ 等改动未触碰、未 stash、未入库。
