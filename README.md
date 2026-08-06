# fe-skills

前端组统一的 Agent Skills 技能包。

## 安装

```bash
# 全局安装全部 skill（推荐）
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y

# 仅安装指定 skill
npx skills add zeroanonx/fe-skills --skill fe-code-review --skill fe-yuque-docs -g -y
```

安装后重新开启 Agent 会话。

### 使用 zero-tui 安装

先安装 zero-tui：

```bash
npm install --global zero-tui
```

启动后在终端执行：

```bash
zero
```

```text
/skill add zeroanonx/fe-skills
/skill update all
```

更新 skill：

```text
/skill upgrade all --pull
/skill update all
```

## 技能清单

| 目录 | 触发 | 说明 | 主要产出 |
|------|------|------|----------|
| `fe-code-review` | `/fe-code-review` 或「帮我 CR」 | 7 步前端 Code Review，P0/P1/P2 分级，HTML/MD 报告 | 被审项目内 `fe-spec/code-review/`；需配套 vue/react/ts skill |
| `fe-yuque-docs` | `/fe-yuque-docs` 或分享语雀 URL | 通过 Cookie **只读/搜索**语雀私有文档（不支持写入） | 对话内总结；Cookie 存于 skill 包 `credentials/cookie.txt` |
| `fe-screenshot-to-task` | `/fe-screenshot-to-task` | 截图/PRD 转前端任务清单，落地前须用户确认 | 被审项目内 `fe-spec/tasks/{任务名}/docs.md` |

## 从独立仓库迁移

以下 skill 已合并进本包，旧仓库不再单独维护：

- `zeroanonx/code-review` → `skills/fe-code-review/`
- `zeroanonx/yuque-docs` → `skills/fe-yuque-docs/`
- `zeroanonx/screenshot-to-task` → `skills/fe-screenshot-to-task/`
