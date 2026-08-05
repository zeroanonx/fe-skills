# fe-skills

前端组统一的 **Agent Skills 技能包**（Skill Package）。一次安装，包含 Code Review、语雀文档读取、截图转任务等能力。

遵循 [Agent Skills](https://agentskills.io/) 规范，通过 [Skills CLI](https://skills.sh) 分发。

## 安装

```bash
# 全局安装全部 skill（推荐）
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y

# 仅安装指定 skill
npx skills add zeroanonx/fe-skills --skill code-review --skill yuque-docs -g -y

# 本地开发试装（在 fe-skills 仓库根目录）
npx skills add . --all -g -y
```

安装后重新开启 Agent 会话。

## 更新

```bash
npx skills update -g -y
```

## 技能清单

| Skill | 触发 | 说明 | 主要产出 |
|-------|------|------|----------|
| **code-review** | `/code-review` 或「帮我 CR」 | 7 步前端 Code Review，P0/P1/P2 分级，HTML/MD 报告 | 被审项目内 `code-review/code-review-result/`、`code-review/archive/` |
| **yuque-docs** | `/yuque-docs` 或分享语雀 URL | 通过 Cookie **只读/搜索**语雀私有文档（不支持写入） | 对话内总结；Cookie 存于 skill 包 `credentials/cookie.txt` |
| **screenshot-to-task** | `/screenshot-to-task` | 截图/PRD 转前端任务清单，落地前须用户确认 | 被审项目内 `task/{中文任务名称}.md`、`task/screenshot/` |

## 配套 Skill（尚未迁入本包）

`code-review` 会按技术栈引用以下同级 skill，**未安装时跳过对应检查，不阻塞主流程**：

| 配套 Skill | 用途 |
|------------|------|
| `vue-best-practices` | Vue / Nuxt 项目专项检查 |
| `vercel-react-best-practices` | React / Next 性能与规范 |
| `typescript-best-practices` | TypeScript 类型安全 |

可从其他来源单独安装，安装后需与 fe-skills skill 位于同一 agent skills 父目录（如 `~/.cursor/skills/`）以保持 `../vue-best-practices/SKILL.md` 相对路径有效。

## 仓库结构

```
fe-skills/
├── README.md
├── skills/
│   ├── code-review/       # SKILL.md + rules/ workflow/ template/
│   ├── yuque-docs/        # SKILL.md + scripts/yuque.py
│   └── screenshot-to-task/# SKILL.md + rules/ examples/
└── openspec/              # 变更规划（可选）
```

## 从独立仓库迁移

以下 skill 已合并进本包，旧仓库不再单独维护：

- `zeroanonx/code-review` → `skills/code-review/`
- `zeroanonx/yuque-docs` → `skills/yuque-docs/`
- `zeroanonx/screenshot-to-task` → `skills/screenshot-to-task/`

## License

MIT
