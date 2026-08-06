# fe-skills

前端组统一的 Agent Skills 技能包。

## 安装

```bash
# 全局安装全部 skill（推荐）
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y

# 仅安装指定 skill
npx skills add zeroanonx/fe-skills --skill fe-code-review --skill fe-yuque-docs --skill fe-screenshot-to-task -g -a cursor -y
```

安装后重新开启 Agent 会话。

### fe-code-review 配套 skill（必装）

CR 前按项目技术栈安装，缺失时 skill 会停止并提示：

```bash
npx skills add hyf0/vue-skills@vue-best-practices -g -a cursor -y
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -a cursor -y
npx skills add cursor/plugins@typescript-best-practices -g -a cursor -y
```

### 使用 zero-tui 安装

```bash
npm install --global zero-tui && zero
```

```text
/skill add zeroanonx/fe-skills
/skill update all
```

## 技能清单

| 目录 | 触发 | 说明 | 主要产出 |
|------|------|------|----------|
| `fe-code-review` | `/fe-code-review` 或「帮我 CR」 | 7 步前端 Code Review，P0/P1/P2 分级 | `fe-spec/code-review/` |
| `fe-yuque-docs` | `/fe-yuque-docs` 或分享语雀 URL | Cookie **只读/搜索**语雀（不支持写入） | 对话内总结 |
| `fe-screenshot-to-task` | `/fe-screenshot-to-task` | 截图/PRD 转前端任务，落地前须确认 | `fe-spec/tasks/{任务名}/` |

## 被审项目产出结构（fe-spec）

```text
{项目根}/fe-spec/
├── code-review/              # fe-code-review
│   ├── archive/
│   ├── code-review-result/   # HTML，建议 gitignore
│   └── backup/               # MD，建议 gitignore
└── tasks/                    # fe-screenshot-to-task
    └── {任务名}/
        ├── docs.md
        └── screenshot/
```

建议在业务项目 `.gitignore` 中忽略 `fe-spec/code-review/code-review-result/` 与 `fe-spec/code-review/backup/`。

## 从独立仓库迁移

- `zeroanonx/code-review` → `skills/fe-code-review/`
- `zeroanonx/yuque-docs` → `skills/fe-yuque-docs/`
- `zeroanonx/screenshot-to-task` → `skills/fe-screenshot-to-task/`
