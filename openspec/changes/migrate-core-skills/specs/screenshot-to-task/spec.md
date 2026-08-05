## ADDED Requirements

### Requirement: Screenshot to task skill migration

`skills/screenshot-to-task/` MUST 包含从独立仓库 `zeroanonx/screenshot-to-task` 迁移的完整 skill 包：`SKILL.md`、`rules/`、`examples/`。

#### Scenario: Phase gate before write

- **WHEN** Agent 执行 screenshot-to-task 工作流
- **THEN** Agent MUST 在 Phase 6 之前禁止写入 `task/{中文任务名称}.md`；Phase 5 落地前确认 MUST 完成

#### Scenario: Task output in target project

- **WHEN** 用户确认理解摘要并允许落盘
- **THEN** Agent MUST 在用户项目根目录生成 `task/{中文任务名称}.md`，截图归档至 `task/screenshot/{中文任务名称}/`

### Requirement: User confirmation gates

有任何不理解、路由未确认、或落地前未获用户明确确认时，Agent MUST 暂停并使用 AskQuestion 或等效交互询问用户，禁止自行猜测。

#### Scenario: Ambiguous interaction on screenshot

- **WHEN** 截图中交互逻辑存在歧义
- **THEN** Agent MUST 列出「需您确认」项并等待用户回复后再继续

### Requirement: Frontend-only scope

产出文档 MUST 仅包含前端任务（§0–§9 结构），MUST NOT 包含 API 章节、验证清单或后端实现细节。

#### Scenario: User requests backend tasks

- **WHEN** 用户要求包含 API 或后端任务
- **THEN** Agent MUST 将后端相关内容归入 §8 范围外或拒绝扩 scope，保持前端-only 约束

### Requirement: Skill metadata

`skills/screenshot-to-task/SKILL.md` frontmatter MUST 保留 `name: screenshot-to-task` 及原有 description、license、metadata。

#### Scenario: Slash trigger

- **WHEN** 用户输入 `/screenshot-to-task` 并提供截图或路径
- **THEN** Agent MUST 加载并遵循 `skills/screenshot-to-task/SKILL.md` 的 Phase 0–6 工作流
