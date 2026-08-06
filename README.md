# ✨ fe-skills 🛠️

前端组的 Agent 技能包 🎒，把团队在前端开发里反复用到的工作方式沉淀成可安装的 Skill，供 Cursor 🤖、Codex 💻、Claude 🧠 等 AI 助手统一调用。安装后即可在 Agent 会话里通过 `/fe-*` 命令或自然语言使用，具体能力见下方技能清单 👇

## 安装 🚀

### 🥳 推荐：使用 zero-tui（首选）

> **团队首选安装方式** — 一条命令添加技能包，后续 `/skill update all` 一键同步最新版，不用记 npx 参数 💪

```bash
npm install --global zero-tui && zero
```

进入 zero 后执行：

```text
/skill add zeroanonx/fe-skills
/skill update all
```

安装后重新开启 Agent 会话 ✨ 让 Skill 生效～

<details>
<summary>📦 备选：使用 npx skills CLI</summary>

未安装 zero-tui 时，可用 Skills CLI 直接安装：

```bash
# 全局安装全部 skill
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y

# 仅安装指定 skill
npx skills add zeroanonx/fe-skills --skill fe-code-review --skill fe-yuque-docs --skill fe-screenshot-to-task --skill fe-create-rules -g -a cursor -y
```

安装后同样需要重新开启 Agent 会话。

</details>

## 技能清单 📋

| 目录                       | Docs 路径                                                                        | 触发                            | 说明                                          | 主要产出                                      |
| -------------------------- | -------------------------------------------------------------------------------- | ------------------------------- | --------------------------------------------- | --------------------------------------------- |
| `fe-code-review` 🔍        | [skills/fe-code-review/README.md](skills/fe-code-review/README.md)               | `/fe-code-review` 或「帮我 CR」 | 7 步前端 Code Review，P0/P1/P2 分级           | `fe-spec/code-review/`                        |
| `fe-yuque-docs` 📖         | [skills/fe-yuque-docs/README.md](skills/fe-yuque-docs/README.md)                 | `/fe-yuque-docs` 或分享语雀 URL | Cookie **只读/搜索**语雀（不支持写入）        | 对话内总结                                    |
| `fe-screenshot-to-task` 📸 | [skills/fe-screenshot-to-task/README.md](skills/fe-screenshot-to-task/README.md) | `/fe-screenshot-to-task`        | 截图/PRD 转前端任务，落地前须确认             | `fe-spec/tasks/{任务名}/`                     |
| `fe-create-rules` 📐       | [skills/fe-create-rules/README.md](skills/fe-create-rules/README.md)             | `/fe-create-rules`              | 分析老项目，生成 Cursor/Codex/Claude 编码规则 | `.cursor/rules/` 或 `AGENTS.md` / `CLAUDE.md` |

Happy coding 🎉
