---
name: code-review
description: >-
  Reviews frontend code changes with P0/P1/P2 findings, HTML/Markdown reports,
  and project archive for regression patterns. Use for code review, CR, PR/diff
  review, branch changes, or code quality assessment.
license: MIT
metadata:
  author: zeroanonx
  version: "1.5.2"
---

# Code Review

系统性审查前端变更，输出 HTML/Markdown 报告，用被审查项目内 `code-review/archive/` 沉淀易错模式。

## 目录分层

| 层 | 路径 | 用途 |
| -- | ---- | ---- |
| 入口 | `SKILL.md` | 工作流与纪律 |
| 规约 | `rules/` | 编码标准 |
| 流程 | `workflow/` | 各步骤细则 |
| 模板 | `template/` | 报告与 archive 骨架 |
| 元信息 | `meta/` | 废弃路径等 |

**被审查项目**（读写，与 Skill 包分离）：`code-review/code-review-result/`、`backup/`、`archive/`。

## Workflow

严格按序执行，不得跳步。

```
- [ ] 1. Archive     读 index + 关键词
- [ ] 2. Context     项目文件 + 规范 + OpenSpec（若有）
- [ ] 3. Scope       AskQuestion → 获取 diff
- [ ] 4. Review      P0→P1→P2 + archive 回归 + OpenSpec 对齐
- [ ] 5. Report      建目录 → run-id → HTML + MD
- [ ] 6. Archive     P0/P1 写入 cases（P2 禁止）
- [ ] 7. Deliver     打开 HTML + 聊天输出绝对路径
```

| 步骤 | 动作 | 参考 |
| :--: | ---- | ---- |
| 1 | 读 `archive/index.md`（无则按 `template/archive-index.md` 创建） | [workflow/archive.md](workflow/archive.md) |
| 2 | 读项目文件；加载 [rules/standards.md](rules/standards.md)；有 `openspec/` 则读未归档提案 | [workflow/context.md](workflow/context.md) |
| 3 | **AskQuestion** 三选一后再 diff；禁止静默默认 | [workflow/scope.md](workflow/scope.md) |
| 4 | 对照 standards + archive 回归；diff 后匹配 OpenSpec 并重点 CR | [workflow/review.md](workflow/review.md) |
| 5 | 从 `template/code-review-result-*.md` 生成 `{branch}-{run-id}-code-review-result.*` | [workflow/report.md](workflow/report.md) |
| 6 | P0/P1 更新 `archive/` | [workflow/archive.md](workflow/archive.md) |
| 7 | `open` 本次 HTML；输出完整绝对路径 | [workflow/report.md](workflow/report.md) |

## Rules

- 每条问题：具体描述 + 文件行号 + 可运行修复示例；禁止模糊好评
- 报告格式以 **`template/code-review-result-html.md` / `code-review-result-md.md` 顶部规则表** 为准（不在别处复述）
- ❌ 禁止跳步 1、3；禁止只聊天不写 code-review-result/backup
- ❌ 禁止步骤 5 完成前写 archive；禁止覆盖历史 code-review-result/backup
- ❌ 禁止读/写被审查项目内 `code-review/template/`
- ❌ 禁止 [meta/deprecated.md](meta/deprecated.md) 中的旧路径与写法
- ❌ 不主动大规模改代码；不审范围外文件

## Output layout（被审查项目）

```
code-review/
├── archive/              # 建议提交 Git
├── code-review-result/   # HTML，建议 gitignore
└── backup/               # MD，与 code-review-result 同 run-id
```
