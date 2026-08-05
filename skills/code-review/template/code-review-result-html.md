# Code Review HTML 报告模板

> **读取位置**：Skill 包 `{skill-root}/template/code-review-result-html.md`（禁止读被审查项目内 template）。
> **写入位置**：被审查项目 `code-review/code-review-result/{branch}-{run-id}-code-review-result.html`。

**生成规则（必须遵守）**

| 区块         | 规则                                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 评分依据     | **禁止**输出 `header-foot`；依据仅写入 `grade` 的 `title` 属性（悬停可见）                                         |
| 审查范围     | 「范围选项」只写**描述文案**，**禁止**前缀 `1 ·` / `2 ·` / `3 ·` 等选项编号                                        |
| 历史回归     | **仅输出「命中」项**；无命中则**整段省略**该 section                                                               |
| 做得好的地方 | **不输出**                                                                                                         |
| 问题代码     | **P0/P1 每条**、**P2 每个 `p2-item`** 均须含 `code-diff-grid`（「源代码」/「优化后」左右分栏）；禁止仅输出文字描述 |
| 合入结论     | **建议合入** + **技术债** + **P0/P1/P2 计数** 均在 **header** 内；不单独输出 KPI 行与「综合评估」                  |
| 离线可读     | **禁止** Google Fonts、highlight.js 等第三方 CDN；报告须断网可完整阅读                                             |

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#f3f4f6" />
    <link
      rel="icon"
      href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>CR</text></svg>"
    />
    <title>Code Review 报告 - [项目名]</title>
    <style>
      :root {
        --ink: #0f172a;
        --ink-muted: #64748b;
        --ink-faint: #94a3b8;
        --paper: #ffffff;
        --canvas: #eef2f7;
        --canvas-deep: #e2e8f0;
        --line: #e2e8f0;
        --line-strong: #cbd5e1;
        --accent: #2563eb;
        --accent-soft: #eff6ff;
        --p0: #dc2626;
        --p0-soft: #fef2f2;
        --p1: #d97706;
        --p1-soft: #fffbeb;
        --p2: #64748b;
        --p2-soft: #f8fafc;
        --ok: #059669;
        --ok-soft: #ecfdf5;
        --radius: 10px;
        --radius-lg: 14px;
        --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
        --shadow-md: 0 4px 16px rgba(15, 23, 42, 0.06);
        --shadow-lg: 0 12px 36px rgba(15, 23, 42, 0.08);
        --font:
          -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
          "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: var(--font);
        font-size: 15px;
        line-height: 1.65;
        color: var(--ink);
        background:
          radial-gradient(
            ellipse 120% 80% at 50% -20%,
            rgba(37, 99, 235, 0.06),
            transparent 55%
          ),
          var(--canvas);
        -webkit-font-smoothing: antialiased;
      }

      .page {
        max-width: 1200px;
        margin: 0 auto;
        padding: 28px 32px 64px;
      }

      /* ── Header ── */
      .report-header {
        margin-bottom: 16px;
        background: var(--paper);
        color: var(--ink);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        overflow: hidden;
      }

      .header-main {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: space-between;
        gap: 24px;
        padding: 28px 32px 24px;
      }

      .header-left {
        flex: 1;
        min-width: 280px;
      }

      .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin: 0 0 10px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--accent);
        background: var(--accent-soft);
        border-radius: 999px;
      }

      .eyebrow::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
      }

      .header-left h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.2;
      }

      .header-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
      }

      .header-meta span {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        font-size: 13px;
        color: var(--ink-muted);
        background: var(--p2-soft);
        border: 1px solid var(--line);
        border-radius: 999px;
      }

      .header-meta strong {
        color: var(--ink-faint);
        font-weight: 500;
        font-size: 12px;
      }

      .header-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 14px;
        flex-shrink: 0;
      }

      .header-metrics {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 12px 16px;
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid var(--line);
        border-radius: var(--radius);
      }

      .stat-strip {
        display: flex;
        align-items: center;
        gap: 0;
      }

      .stat {
        display: flex;
        align-items: baseline;
        gap: 6px;
        padding: 0 14px;
        border-right: 1px solid var(--line);
      }

      .stat:last-child {
        border-right: none;
      }
      .stat:first-child {
        padding-left: 0;
      }

      .stat .n {
        font-size: 22px;
        font-weight: 700;
        line-height: 1;
        font-variant-numeric: tabular-nums;
        letter-spacing: -0.02em;
      }

      .stat .l {
        font-size: 12px;
        font-weight: 600;
        color: var(--ink-faint);
      }

      .stat-p0 .n {
        color: var(--p0);
      }
      .stat-p1 .n {
        color: var(--p1);
      }
      .stat-p2 .n {
        color: var(--p2);
      }

      .grade-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        padding-left: 4px;
      }

      .grade {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.04em;
        box-shadow: var(--shadow-sm);
      }

      .grade-a {
        background: linear-gradient(145deg, #ecfdf5, #d1fae5);
        color: var(--ok);
      }
      .grade-b {
        background: linear-gradient(145deg, #eff6ff, #dbeafe);
        color: var(--accent);
      }
      .grade-c {
        background: linear-gradient(145deg, #fffbeb, #fef3c7);
        color: #b45309;
      }
      .grade-d {
        background: linear-gradient(145deg, #fef2f2, #fee2e2);
        color: var(--p0);
      }

      .grade-label {
        font-size: 11px;
        font-weight: 600;
        color: var(--ink-faint);
        letter-spacing: 0.02em;
      }

      .verdict-stack {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-end;
        gap: 8px;
      }

      .verdict-pill,
      .debt-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 600;
        white-space: nowrap;
        border: 1px solid transparent;
      }

      .verdict-pill .pill-label,
      .debt-pill .pill-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--ink-muted);
      }

      .verdict-pill .pill-label::after,
      .debt-pill .pill-label::after {
        content: "·";
        margin-left: 6px;
        color: var(--ink-faint);
      }

      .verdict-yes {
        background: var(--ok-soft);
        border-color: #a7f3d0;
      }
      .verdict-yes .pill-value {
        color: var(--ok);
      }
      .verdict-no {
        background: var(--p0-soft);
        border-color: #fecaca;
      }
      .verdict-no .pill-value {
        color: var(--p0);
      }
      .verdict-pending {
        background: var(--p1-soft);
        border-color: #fde68a;
      }
      .verdict-pending .pill-value {
        color: #b45309;
      }
      .debt-low {
        background: var(--ok-soft);
        border-color: #a7f3d0;
      }
      .debt-low .pill-value {
        color: var(--ok);
      }
      .debt-mid {
        background: var(--p1-soft);
        border-color: #fde68a;
      }
      .debt-mid .pill-value {
        color: #b45309;
      }
      .debt-high {
        background: var(--p0-soft);
        border-color: #fecaca;
      }
      .debt-high .pill-value {
        color: var(--p0);
      }

      @media (max-width: 720px) {
        .page {
          padding: 16px 16px 48px;
        }
        .header-main {
          padding: 22px 20px 18px;
        }
        .header-right {
          width: 100%;
          align-items: stretch;
        }
        .header-metrics {
          justify-content: space-between;
        }
        .verdict-stack {
          justify-content: flex-start;
        }
      }

      /* ── Panels ── */
      .panel {
        background: var(--paper);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: var(--radius-lg);
        margin-bottom: 14px;
        box-shadow: var(--shadow-sm);
        overflow: hidden;
      }

      .panel-title {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 22px;
        font-size: 15px;
        font-weight: 600;
        color: var(--ink);
        border-bottom: 1px solid var(--line);
        background: #fafbfc;
      }

      .panel-title::before {
        content: "";
        width: 3px;
        height: 16px;
        border-radius: 2px;
        background: var(--accent);
      }

      .panel-body {
        padding: 18px 22px 20px;
      }

      .scope-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin: 0;
        padding: 0;
        list-style: none;
      }

      @media (max-width: 560px) {
        .scope-grid {
          grid-template-columns: 1fr;
        }
      }

      .scope-grid li {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding: 12px 14px;
        font-size: 15px;
        background: #f8fafc;
        border: 1px solid var(--line);
        border-radius: var(--radius);
      }

      .scope-grid .key {
        font-size: 12px;
        font-weight: 600;
        color: var(--ink-faint);
        text-transform: none;
        letter-spacing: 0;
      }

      .scope-grid .val {
        color: var(--ink);
        word-break: break-word;
        font-weight: 500;
      }

      .scope-grid .val code {
        font-family: var(--mono);
        font-size: 13px;
        padding: 2px 6px;
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 5px;
        color: #334155;
      }

      /* Regression */
      .panel-regression .panel-title::before {
        background: var(--p1);
      }

      .hit-list {
        margin: 0;
        padding: 0;
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .hit-list li {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 14px 18px;
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: var(--radius);
      }

      .hit-list li > div {
        flex: 1;
        min-width: 0;
      }

      .hit-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        width: 44px;
        height: 26px;
        margin-top: 1px;
        padding: 0;
        font-size: 12px;
        font-weight: 700;
        line-height: 1;
        border-radius: 6px;
        border: 1px solid #fcd34d;
        background: #fef3c7;
        color: #b45309;
      }

      .hit-id {
        display: block;
        font-family: var(--mono);
        font-size: 13px;
        font-weight: 500;
        color: var(--p1);
        margin-bottom: 4px;
      }

      .hit-desc {
        margin: 0;
        font-size: 15px;
        color: var(--ink);
        line-height: 1.55;
      }

      /* ── Issues ── */
      .issues-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0 12px;
        padding: 0 4px;
      }

      .issues-head span {
        font-size: 15px;
        font-weight: 600;
        color: var(--ink);
      }

      .issues-head button {
        font-family: var(--font);
        font-size: 13px;
        font-weight: 500;
        padding: 7px 14px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--paper);
        color: var(--ink-muted);
        cursor: pointer;
        box-shadow: var(--shadow-sm);
        transition:
          border-color 0.15s,
          color 0.15s;
      }

      .issues-head button:hover {
        border-color: var(--line-strong);
        color: var(--ink);
      }

      .issue-card {
        background: var(--paper);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: var(--radius-lg);
        margin-bottom: 10px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 0.15s;
      }

      .issue-card:hover {
        box-shadow: var(--shadow-md);
      }

      .issue-card.sev-p0 {
        border-left: 4px solid var(--p0);
      }
      .issue-card.sev-p1 {
        border-left: 4px solid var(--p1);
      }
      .issue-card.sev-p2 {
        border-left: 4px solid var(--p2);
      }

      .issue-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 20px;
        cursor: pointer;
        user-select: none;
        transition: background 0.15s;
      }

      .issue-header:hover {
        background: #f8fafc;
      }

      .badge {
        flex-shrink: 0;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 9px;
        border-radius: 999px;
        letter-spacing: 0.03em;
      }

      .badge-p0 {
        background: var(--p0-soft);
        color: var(--p0);
      }
      .badge-p1 {
        background: var(--p1-soft);
        color: var(--p1);
      }
      .badge-p2 {
        background: var(--p2-soft);
        color: var(--p2);
        border: 1px solid var(--line);
      }

      .issue-title-text {
        flex: 1;
        min-width: 0;
        font-size: 15px;
        font-weight: 600;
        color: var(--ink);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .chevron {
        flex-shrink: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--ink-faint);
        font-size: 16px;
        border-radius: 6px;
        background: #f1f5f9;
        transition:
          transform 0.18s ease,
          background 0.15s;
      }

      .issue-header:hover .chevron {
        background: #e2e8f0;
      }
      .issue-card.open .chevron {
        transform: rotate(90deg);
      }

      .issue-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.22s ease;
      }

      .issue-card.open .issue-content {
        max-height: 12000px;
      }

      .issue-inner {
        padding: 4px 20px 20px;
        border-top: 1px solid var(--line);
        background: #fafbfc;
      }

      .issue-file {
        display: inline-block;
        margin: 16px 0 10px;
        padding: 5px 11px;
        font-family: var(--mono);
        font-size: 13px;
        color: var(--accent);
        background: var(--accent-soft);
        border: 1px solid #bfdbfe;
        border-radius: 6px;
      }

      .issue-desc {
        margin: 0 0 14px;
        font-size: 15px;
        color: var(--ink-muted);
      }

      /* Code diff — 宽屏保持左右分栏 */
      .code-diff-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-top: 10px;
      }

      @media (max-width: 640px) {
        .code-diff-grid {
          grid-template-columns: 1fr;
        }
      }

      .diff-col {
        min-width: 0;
        border-radius: var(--radius);
        border: 1px solid var(--line);
        box-shadow: var(--shadow-sm);
        display: flex;
        flex-direction: column;
      }

      .diff-col-before {
        border-top: 3px solid #f87171;
      }
      .diff-col-after {
        border-top: 3px solid #34d399;
      }

      .diff-col-head {
        padding: 9px 14px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
      }

      .diff-col-before .diff-col-head {
        background: var(--p0-soft);
        color: #b91c1c;
      }

      .diff-col-after .diff-col-head {
        background: var(--ok-soft);
        color: #047857;
      }

      .diff-col pre {
        margin: 0 !important;
        padding: 14px 16px !important;
        font-size: 13px !important;
        line-height: 1.55 !important;
        background: var(--paper) !important;
        border-top: 1px solid var(--line);
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }

      .diff-col pre code {
        display: block;
        white-space: pre;
        word-wrap: normal;
        overflow-wrap: normal;
      }

      .p2-item {
        padding: 14px 0;
        border-bottom: 1px solid var(--line);
      }

      .p2-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
      }

      .p2-item-title {
        margin: 0 0 10px;
        font-size: 14px;
        font-weight: 600;
        color: var(--ink);
      }

      .footer {
        margin-top: 28px;
        text-align: center;
        font-size: 13px;
        color: var(--ink-faint);
      }
    </style>
  </head>
  <body>
    <div class="page">
      <header class="report-header">
        <div class="header-main">
          <div class="header-left">
            <p class="eyebrow">Code Review</p>
            <h1>[项目名]</h1>
            <div class="header-meta">
              <span><strong>时间</strong> [时间戳]</span>
              <span><strong>分支</strong> [分支名]</span>
              <span><strong>run-id</strong> [YYYYMMDD-HHmmss]</span>
              <span><strong>审查</strong> z-code-review</span>
            </div>
          </div>
          <div class="header-right">
            <div class="header-metrics">
              <div class="stat-strip">
                <div class="stat stat-p0">
                  <span class="n">[0]</span><span class="l">P0</span>
                </div>
                <div class="stat stat-p1">
                  <span class="n">[0]</span><span class="l">P1</span>
                </div>
                <div class="stat stat-p2">
                  <span class="n">[0]</span><span class="l">P2</span>
                </div>
              </div>
              <!-- grade-a / grade-b / grade-c / grade-d -->
              <div class="grade-wrap">
                <div class="grade grade-b" title="[评分依据]">[B]</div>
                <span class="grade-label">综合评分</span>
              </div>
            </div>
            <div class="verdict-stack">
              <!-- verdict-yes / verdict-no / verdict-pending -->
              <div class="verdict-pill verdict-pending">
                <span class="pill-label">建议合入</span>
                <span class="pill-value">[修复后合入]</span>
              </div>
              <!-- debt-low / debt-mid / debt-high -->
              <div class="debt-pill debt-low">
                <span class="pill-label">技术债</span>
                <span class="pill-value">[低]</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <section class="panel">
        <div class="panel-title">审查范围</div>
        <div class="panel-body">
          <ul class="scope-grid">
            <li>
              <span class="key">范围选项</span
              ><span class="val">[范围描述，如「当前分支相对 origin/master 的全部待合入变更」；禁止写 1 · / 2 · 前缀]</span
              >
            </li>
            <li>
              <span class="key">远程主分支</span
              ><span class="val">[origin/main 或 merge-base abc1234]</span>
            </li>
            <li>
              <span class="key">Commit 数</span><span class="val">[N]</span>
            </li>
            <li>
              <span class="key">变更文件</span><span class="val">[N] 个</span>
            </li>
            <li>
              <span class="key">路径过滤</span
              ><span class="val">[无 / 具体路径]</span>
            </li>
          </ul>
        </div>
      </section>

      <!-- 仅当 archive 回归有「命中」项时输出；无命中则整段省略 -->
      <section class="panel panel-regression">
        <div class="panel-title">历史回归 · [N] 项命中</div>
        <div class="panel-body">
          <ul class="hit-list">
            <!--
            <li>
              <span class="hit-badge">命中</span>
              <div>
                <span class="hit-id">002 data-display</span>
                <p class="hit-desc">[命中描述]</p>
              </div>
            </li>
            -->
          </ul>
        </div>
      </section>

      <div class="issues-head">
        <span>问题清单</span>
        <button type="button" id="toggle-all">全部展开</button>
      </div>

      <section class="issues" id="issues">
        <!-- 示例 issue-card（生成时按此结构填充，删除注释块） -->
        <!--
        <article class="issue-card sev-p1">
          <div class="issue-header" role="button" tabindex="0" aria-expanded="false">
            <span class="badge badge-p1">P1</span>
            <span class="issue-title-text">问题标题</span>
            <span class="chevron" aria-hidden="true">›</span>
          </div>
          <div class="issue-content">
            <div class="issue-inner">
              <div class="issue-file">path/to/file.ts:42</div>
              <p class="issue-desc">问题描述</p>
              <div class="code-diff-grid">
                <div class="diff-col diff-col-before">
                  <div class="diff-col-head">源代码</div>
                  <pre><code class="language-typescript">// 源代码</code></pre>
                </div>
                <div class="diff-col diff-col-after">
                  <div class="diff-col-head">优化后</div>
                  <pre><code class="language-typescript">// 优化后</code></pre>
                </div>
              </div>
            </div>
          </div>
        </article>

        P2 多项合并为一卡；每个 p2-item 必须含 issue-file + issue-desc + code-diff-grid（禁止仅标题+描述）：
        <div class="p2-item">
          <p class="p2-item-title">子项标题</p>
          <div class="issue-file">path/to/file.vue:42</div>
          <p class="issue-desc">问题描述</p>
          <div class="code-diff-grid">
            <div class="diff-col diff-col-before">
              <div class="diff-col-head">源代码</div>
              <pre><code class="language-vue">// 源代码</code></pre>
            </div>
            <div class="diff-col diff-col-after">
              <div class="diff-col-head">优化后</div>
              <pre><code class="language-vue">// 优化后</code></pre>
            </div>
          </div>
        </div>
        -->
      </section>

      <footer class="footer">Generated by z-code-review · [run-id]</footer>
    </div>

    <script>
      document
        .querySelectorAll(".issue-card .issue-header")
        .forEach(function (header) {
          function toggle() {
            var card = header.closest(".issue-card");
            var open = card.classList.toggle("open");
            header.setAttribute("aria-expanded", open ? "true" : "false");
          }
          header.addEventListener("click", toggle);
          header.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              toggle();
            }
          });
        });

      var toggleBtn = document.getElementById("toggle-all");
      if (toggleBtn) {
        var expanded = false;
        toggleBtn.addEventListener("click", function () {
          expanded = !expanded;
          document.querySelectorAll(".issue-card").forEach(function (card) {
            card.classList.toggle("open", expanded);
            var h = card.querySelector(".issue-header");
            if (h) h.setAttribute("aria-expanded", expanded ? "true" : "false");
          });
          toggleBtn.textContent = expanded ? "全部收起" : "全部展开";
        });
      }
    </script>
  </body>
</html>
```
