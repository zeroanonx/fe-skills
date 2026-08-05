# Report · 步骤 5–7

## 步骤 5 · 生成

1. 创建 `code-review/code-review-result/`、`backup/`、`archive/`、`archive/cases/`（若不存在）
2. 分配 `run-id`：`YYYYMMDD-HHmmss`（路径冲突则 `-2`、`-3`…，禁止覆盖）
3. 写入：
   - `{项目}/code-review/code-review-result/{branch}-{run-id}-code-review-result.html` ← Skill 包 `template/code-review-result-html.md`
   - `{项目}/code-review/backup/{branch}-{run-id}-code-review-result.md` ← Skill 包 `template/code-review-result-md.md`

**格式规则**：生成前读 `../template/code-review-result-*.md` **顶部「生成规则」表**，不在此复述。

Archive 模板：`../template/archive-index.md`、`../template/archive-case.md`

## 步骤 7 · 交付

```bash
open "{report-path}"          # macOS
start "" "{report-path}"      # Windows
xdg-open "{report-path}"      # Linux
```

聊天**必须**输出本次 HTML 的完整绝对路径。仅打开**本次** `run-id` 文件，禁止打开目录内最新/任意历史报告。

若步骤 2 发现缺少 gitignore 规则，在此一并提示用户追加 `code-review/code-review-result/` 与 `code-review/backup/`。
