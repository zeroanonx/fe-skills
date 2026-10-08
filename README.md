# ✨ fe-skills

前端组的 Agent 技能包 🎒，把团队在前端开发里反复用到的工作方式沉淀成可安装的 Skill，供 Cursor 🤖、Codex 💻、Claude 🧠 等 AI 助手统一调用。安装后即可在 Agent 会话里通过 `/fe-*` 命令（Codex 可用 `$fe-*`）或自然语言使用，具体能力见下方技能清单 👇

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

### 📦 备选：使用 npx skills CLI

未安装 zero-tui 时，可用 Skills CLI 直接安装：

```bash
# 全局安装全部 skill
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y

# 仅安装指定 skill
npx skills add zeroanonx/fe-skills --skill fe-code-review --skill fe-yuque-docs --skill fe-screenshot-to-task --skill fe-ai-coding --skill fe-design-analysis --skill fe-ui-verification --skill fe-project-migration -g -a cursor -y
```

安装后同样需要重新开启 Agent 会话 ✨

## 技能清单 📋

| 目录                       | Docs 路径                                                                        | 触发                                         | 说明                                   | 主要产出                                                     |
| -------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------- | ------------------------------------------------------------ |
| `fe-code-review` 🔍        | [skills/fe-code-review/README.md](skills/fe-code-review/README.md)               | `/fe-code-review` 或「帮我 CR」              | 7 步前端 Code Review，P0/P1/P2 分级    | `fe-spec/code-review/`                                       |
| `fe-yuque-docs` 📖         | [skills/fe-yuque-docs/README.md](skills/fe-yuque-docs/README.md)                 | `/fe-yuque-docs` 或分享语雀 URL              | Cookie **只读/搜索**语雀（不支持写入） | 对话内总结                                                   |
| `fe-screenshot-to-task` 📸 | [skills/fe-screenshot-to-task/README.md](skills/fe-screenshot-to-task/README.md) | `/fe-screenshot-to-task`                     | 截图/PRD 转前端任务，落地前须确认      | `fe-spec/tasks/{任务名}/`                                    |
| `fe-design-analysis` 🎨    | [skills/fe-design-analysis/README.md](skills/fe-design-analysis/README.md)       | `/fe-design-analysis` 或「分析设计稿」       | 提取视觉基准，HTML + MD 并打开 HTML    | `fe-spec/design-analysis/{模块}/{run-id}/`                   |
| `fe-ui-verification` 🖼️    | [skills/fe-ui-verification/README.md](skills/fe-ui-verification/README.md)       | `/fe-ui-verification` 或「UI 验收」          | 浏览器验收，HTML/MD 修改意见勾选后执行 | `fe-spec/ui-verification/{模块}/{run-id}/`                   |
| `fe-ai-coding` ✍️          | [skills/fe-ai-coding/README.md](skills/fe-ai-coding/README.md)                   | `/fe-ai-coding` 或「写代码按团队规范」       | 目录分层、编码规范及项目 AI 规则生成   | 代码修改；按需生成 Cursor/Codex/Claude 规则                  |
| `fe-project-migration` 🔄  | [skills/fe-project-migration/README.md](skills/fe-project-migration/README.md)   | `/fe-project-migration` 或「老项目迁新项目」 | 业务还原、工程映射、分批迁移与验收     | 代码；`fe-spec/project-migration/{模块}/{run-id}/` HTML + MD |

## 设计到验收

`fe-design-analysis` 提取视觉基准 → `fe-ai-coding` 按项目规范实现 → `fe-ui-verification` 在真实页面上对照验收。需要产品流程与开发任务拆解时，配合 `fe-screenshot-to-task`。各技能可独立使用，不要求固定安装路径。

老业务迁入新工程使用 `fe-project-migration`：先还原操作链路与参数契约，再对照目标工程、形成规格、分批实现与验收。支持只读梳理和仅方案模式，不把方案产出当作迁移完成。

Happy coding 🎉
