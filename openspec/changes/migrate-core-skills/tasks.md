## 1. 仓库脚手架

- [x] 1.1 创建 `skills/` 目录
- [x] 1.2 创建根级 `.gitignore`，忽略 `skills/yuque-docs/credentials/cookie.txt` 及常见 OS/IDE 文件
- [x] 1.3 创建根级 `README.md`：fe-skills 简介、技能清单、安装/更新/按 skill 选择性安装命令

## 2. 迁移 code-review

- [x] 2.1 从 `/Users/linhan/Desktop/Zero/code-review/code-review/` 复制全部内容到 `skills/code-review/`（排除无）
- [x] 2.2 确认 `SKILL.md` frontmatter 保留 `name: code-review` 及 metadata
- [x] 2.3 确认 `rules/`、`workflow/`、`template/`、`meta/` 相对路径在 SKILL.md 内引用正确
- [x] 2.4 确认跨 skill 引用路径 `../vue-best-practices/` 等未被误改

## 3. 迁移 yuque-docs

- [x] 3.1 从 `/Users/linhan/Desktop/Zero/yuque-docs/yuque-docs/` 复制到 `skills/yuque-docs/`（排除真实 `credentials/cookie.txt`）
- [x] 3.2 保留 `credentials/cookie.txt.example` 与 `credentials/config.json`
- [x] 3.3 确认 `scripts/yuque.py` 可执行且 SKILL.md 中脚本路径为 `scripts/yuque.py`
- [x] 3.4 确认 SKILL.md 只读硬约束与拒绝写入话术完整

## 4. 迁移 screenshot-to-task

- [x] 4.1 从 `/Users/linhan/Desktop/Zero/screenshot-to-task/screenshot-to-task/` 复制到 `skills/screenshot-to-task/`
- [x] 4.2 确认 `rules/`、`examples/example-task-format.md` 完整
- [x] 4.3 确认 SKILL.md Phase 0–6 工作流与落地前确认门禁未丢失

## 5. 验证

- [x] 5.1 运行 `npx skills add . --list`（在 fe-skills 根目录）确认列出三个 skill
- [x] 5.2 运行 `npx skills add . --skill code-review --skill yuque-docs --skill screenshot-to-task -g -y -a cursor` 试装
- [x] 5.3 检查 `~/.cursor/skills/` 下三个 skill 目录为顶层安装（非嵌套 fe-skills 子目录）
- [x] 5.4 抽查各 skill：SKILL.md 行数与源仓库一致、无断链相对路径

## 6. 文档收尾

- [x] 6.1 README 技能表补充各 skill 一行说明、触发方式（`/code-review` 等）及主要产出路径
- [x] 6.2 README 注明配套 skill（vue-best-practices 等）尚未迁入、可选安装
