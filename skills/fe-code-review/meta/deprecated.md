# Deprecated · 禁止使用的旧路径

| 废弃 | 现行 |
| ---- | ---- |
| `code-review/reports/`、`code-review/output/` | `code-review-result/` + `backup/` |
| `code-review/result/` | `code-review/code-review-result/` |
| `template/crr-html.md`、`template/crr-md.md` | `template/code-review-result-html.md`、`code-review-result-md.md` |
| `{branch}-{run-id}-crr.*`、`-crr.html`、`-crr.md` | `{branch}-{run-id}-code-review-result.*` |
| `{branch}-{YYYYMMDD}-crr.*`（无 run-id） | `{branch}-{run-id}-code-review-result.*` |
| 被审查项目内 `code-review/template/` | Skill 包 `template/` |
| 覆盖已有 code-review-result/backup | 每次新建 run-id 文件 |
