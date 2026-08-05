## ADDED Requirements

### Requirement: Skill Package directory layout

fe-skills 仓库 MUST 采用 Skills CLI 可扫描的 Skill Package 布局：所有 skill 源码位于 `skills/<skill-name>/` 目录，每个目录 MUST 包含 `SKILL.md` 及该 skill 所需的 rules、workflow、scripts、template 等附属文件。

#### Scenario: CLI discovers skills in package

- **WHEN** 用户运行 `npx skills add zeroanonx/fe-skills --list`
- **THEN** CLI MUST 列出 `code-review`、`yuque-docs`、`screenshot-to-task` 三个 skill

#### Scenario: Flat skill install path

- **WHEN** 用户运行 `npx skills add zeroanonx/fe-skills --all -g -y`
- **THEN** 各 skill MUST 安装到 agent 全局 skills 目录的顶层（如 `~/.cursor/skills/code-review/`），而非嵌套在 `fe-skills/` 子目录下

### Requirement: Package README and install documentation

仓库根目录 MUST 提供 `README.md`，说明 fe-skills 为前端组统一 Skill Package，并包含一条命令安装全部 skill、按 skill 名选择性安装、以及 `npx skills update -g -y` 更新指引。

#### Scenario: User installs entire package

- **WHEN** 用户按 README 执行 `npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y`
- **THEN** 三个 core skill MUST 均可被 Cursor 与 Codex 发现并使用

### Requirement: Sensitive file exclusion

仓库 MUST 通过 `.gitignore` 排除 `skills/yuque-docs/credentials/cookie.txt` 等用户本地凭证；MUST 保留 `cookie.txt.example` 或等效示例文件供用户参考。

#### Scenario: Cookie not committed

- **WHEN** 开发者本地存在 `skills/yuque-docs/credentials/cookie.txt`
- **THEN** 该文件 MUST NOT 被 git 跟踪或提交到远程仓库
