## Why

前端 Agent Skills（code-review、yuque-docs、screenshot-to-task）目前分散在 `Zero/` 下多个独立 git 仓库中，重复维护成本高，安装方式不统一。需要将三者合并到 `fe-skills` 单一 Skill Package，采用 Skills CLI 模式 A（`npx skills add zeroanonx/fe-skills`）一次安装、统一更新，作为后续所有前端 skills 的唯一维护入口。

## What Changes

- 在 `fe-skills/skills/` 下新增三个 skill 目录：`code-review/`、`yuque-docs/`、`screenshot-to-task/`，从现有独立仓库迁移完整 skill 包（SKILL.md、rules、workflow、scripts 等）
- 新增根级 `README.md`：fe-skills 品牌说明、技能清单、一条命令安装与更新指引
- 新增 `.gitignore`：忽略 `yuque-docs` 的 `credentials/cookie.txt` 等敏感文件
- 拍平嵌套目录结构（如 `code-review/code-review/` → `skills/code-review/`）
- 保留各 skill 原有行为与产出路径（如 CR 写入被审项目的 `code-review/`，screenshot-to-task 写入 `task/`）
- 本阶段**不包含**：create-rules、zero-skills 其余 skill 的迁移；旧独立仓库的归档/README _redirect（可后续变更处理）
- 本阶段**不包含**：删除 fe-skills 内 OpenSpec 自动生成的 `.cursor/commands/opsx-*` 与 `openspec-*` skills（用户后续单独处理）

## Capabilities

### New Capabilities

- `skill-package`: fe-skills 仓库作为 Skill Package 的目录规范、安装/更新命令、skills.sh 发布要求
- `code-review`: 前端 Code Review skill（7 步工作流、P0/P1/P2 分级、HTML/MD 报告、archive 知识库）
- `yuque-docs`: 语雀私有文档只读/搜索 skill（Cookie 认证、`scripts/yuque.py`）
- `screenshot-to-task`: 截图转前端任务清单 skill（Phase 0–6 工作流、`task/*.md` 产出）

### Modified Capabilities

（无——`openspec/specs/` 下尚无既有 capability spec）

## Impact

- **新增文件**：`fe-skills/skills/{code-review,yuque-docs,screenshot-to-task}/**`、`README.md`、`.gitignore`
- **源仓库**（只读迁移，本变更不修改）：`/Users/linhan/Desktop/Zero/code-review`、`yuque-docs`、`screenshot-to-task`
- **用户安装方式变更**：从 `npx skills add zeroanonx/code-review --skill code-review` 等分散命令，变为 `npx skills add zeroanonx/fe-skills --all -g -y`（或按 skill 名选择性安装）
- **跨 skill 依赖**：code-review 引用的 `../vue-best-practices/` 等配套 skill 本阶段未迁入，缺失时 skill 内已有跳过逻辑，不阻塞 CR 主流程
- **Breaking（对用户）**：独立仓库安装路径将废弃，需改用 fe-skills 包（旧仓库可保留 README 指向 fe-skills）
