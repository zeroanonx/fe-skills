## ADDED Requirements

### Requirement: Code review skill migration

`skills/code-review/` MUST 包含从独立仓库 `zeroanonx/code-review` 迁移的完整 skill 包：`SKILL.md`、`rules/`、`workflow/`、`template/`、`meta/`，行为与源仓库一致。

#### Scenario: Seven-step workflow preserved

- **WHEN** 用户在业务项目中触发 code-review skill
- **THEN** Agent MUST 按序执行 Archive → Context → Scope → Review → Report → Archive → Deliver 七步工作流，不得跳步

#### Scenario: Review output in target project

- **WHEN** code review 完成
- **THEN** 报告与 backup MUST 写入被审查项目内的 `code-review/code-review-result/` 与 `code-review/backup/`，archive MUST 写入被审查项目的 `code-review/archive/`

### Requirement: Cross-skill standards references

code-review skill MUST 保留对同级 skill 的相对路径引用（如 `../vue-best-practices/SKILL.md`）；当配套 skill 未安装时 MUST 跳过对应检查并在摘要中注明，不阻塞主审查流程。

#### Scenario: Optional vue-best-practices missing

- **WHEN** 被审项目含 Vue 依赖但 `vue-best-practices` skill 未安装
- **THEN** Agent MUST 继续执行 CR，仅跳过 Vue 专项检查并在输出中说明缺失项

### Requirement: Skill metadata

`skills/code-review/SKILL.md` frontmatter MUST 保留 `name: code-review` 及原有 description、license、metadata（author、version）；迁移后 version MAY 递增 patch 以反映包归属变更。

#### Scenario: Slash and natural language trigger

- **WHEN** 用户输入 `/code-review` 或「帮我 CR 当前分支变更」
- **THEN** Agent MUST 加载并遵循 `skills/code-review/SKILL.md`
