# QA 记录 — 2611.24977 CANDID

**结论：ready（0 重做 / 0 fail）。**

流程：
1. 渲染（reel/render_poster.py，google-chrome headless）：1500×2880，render-check.json = contentBottom 2870 ≤ 2880、overflow []、fontOK true（PosterCN 400/700 loaded）、pdfPages 1 → pass。
2. 画布预检一次即达标（初稿即 2880，未加高），不占重做额度。
3. 视觉 QA：read_image 实开 poster.png 全图 + 4 段全分辨率裁图（0–780/720–1500/1440–2220/2160–2880）逐段目检：无溢出、无裁切、无重叠；候选芯片行（cut 线/keep 绿）对齐正常；六行哑铃两端数值与横杆无碰撞；Table 5 小表列宽正常；footer 完整落画布内。
4. 字体：本地 Noto Sans CJK SC woff2 子集（reel/2611.24977/assets/fonts/），渲染无远程请求。
5. 数字核对：画报全部数值与 research/fulltext/2611.24977.txt 及 SOURCE.md 映射一致；§2/Table 1 未缓存小节未引用。

遗留观察：无。
