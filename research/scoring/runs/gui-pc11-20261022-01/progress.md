# progress — gui-pc11-20261022-01(problem-core-v1.1)

- L1 完成:68/68 批,1331/1331 篇,l1_check 全通过;{'assessed': 1230, 'out_of_scope': 44, 'needs_material': 57};档位 {'P3': 748, 'None': 95, 'P2': 479, 'P1': 9}
- L2 队列:主池 1278 → 取 240(priority high→medium);抽查 26(seed 20261022,取自 P0/P1、F0、needs_material、park);l2_queue.json
- L2 批次 l01–l18,每 15 篇;材料=research/fulltext/<id>.txt(40k 裁剪 core)
- L2 完成:18/18 批 266/266 篇(主池 240 + 抽查 26,seed 20261022),l1_check 86 批全过
- 漏检抽查:26 篇 5 改判,4 篇升至 P3(2103.16057、2604.14956、2509.23866、2506.07672),1 篇 None→P1(2503.13843)——漏检率约 15%,集中在材料缺失类
- 候选池 to_l3 162 篇(P3 161 / P2 1);按主卡机械去重得 L3 短名单 29 篇(l3_shortlist.tsv,覆盖 16 主卡)
- 下一阶段:Opus 5.5 L3 跨池比较去重 → ≤9 篇 Reel
- Reel 完成:9/9 ready(版式 9 种互不相同);画报核对产生 5 条修订(l19-l23),WebArena 降 P2 按编辑理由保留
- run 结束
- 全量 L2 完成:l24–l91 共 68 批 1013 篇(加首轮 266 篇 = 1279 篇过 L2);l1_check 159 批全过
- 最终统计:1331/1331 | P3 901 / P2 347 / P1 16 / null 67 | to_l3 候选池 584(P3 558 / P2 26)
- candidates.tsv 重写为最终 584 篇;本 Reel(9 篇)基于首轮 266 篇时的选择,不变
- B 组(同材料仍 to_l2 的 80 篇)与 C 组(pending_* 状态的 479 篇)待新材料或新实验后补核
