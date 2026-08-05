## ADDED Requirements

### Requirement: Yuque docs skill migration

`skills/yuque-docs/` MUST 包含从独立仓库 `zeroanonx/yuque-docs` 迁移的完整 skill 包：`SKILL.md`、`scripts/yuque.py`、`rules/`、`credentials/cookie.txt.example`、`credentials/config.json`（若源仓库有）。

#### Scenario: Read-only operations

- **WHEN** 用户请求读取、总结或搜索语雀文档
- **THEN** Agent MUST 仅通过 `scripts/yuque.py` 执行读/搜/列目录操作

#### Scenario: Write operations rejected

- **WHEN** 用户请求新建、更新语雀文档正文或改标题
- **THEN** Agent MUST 拒绝并引导用户到语雀网页端手动编辑

### Requirement: Cookie credential handling

Cookie MUST 存储于 skill 包内 `credentials/cookie.txt`（用户本地，gitignore）；首次无 Cookie 时 Agent MUST 引导用户粘贴 Cookie 并保存后继续。

#### Scenario: Cookie expired

- **WHEN** `yuque.py` 返回认证失败
- **THEN** Agent MUST 提示用户重新获取 Cookie 并更新 `credentials/cookie.txt` 后重试

### Requirement: Skill metadata

`skills/yuque-docs/SKILL.md` frontmatter MUST 保留 `name: yuque-docs` 及原有 description 与硬约束（只读、禁止外部 MCP 仓库）。

#### Scenario: Yuque URL trigger

- **WHEN** 用户分享 yuque.com URL 或提及语雀文档
- **THEN** Agent MUST 识别并应用 yuque-docs skill
