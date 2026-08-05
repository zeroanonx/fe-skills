# Context · 步骤 2

## 项目文件

| 文件 | 用途 |
| ---- | ---- |
| `package.json` | 依赖、脚本、项目类型 |
| `README.md` | 说明与运行方式 |
| `vite.config.*` / `webpack.config.*` / `next.config.*` | 构建配置 |
| `tsconfig.json` | TypeScript |
| `.eslintrc*` / `eslint.config.*` | Lint（如有） |

无 `package.json`：在 MD「本次审查总结」注明项目类型；仅加载 [standards.md](../rules/standards.md)，不阻塞 CR。

## 规范加载

**始终**：[rules/standards.md](../rules/standards.md)

**按依赖**（同级 skills；缺失则跳过并在报告中注明）：

| 条件 | 路径 |
| ---- | ---- |
| `vue` / `@vue/` / `nuxt` | `../vue-best-practices/SKILL.md` |
| `react` / `react-dom` / `next` | `../vercel-react-best-practices/SKILL.md` |
| `typescript` / `tsconfig.json` / 变更含 `.ts`/`.tsx` | `../typescript-best-practices/SKILL.md` |

## Git 预检

检查被审查项目 `.gitignore` 是否忽略 `code-review/code-review-result/`、`code-review/backup/`。缺失则在步骤 7 提示用户追加。`archive/` 建议提交。

## OpenSpec（有 `openspec/` 时必做）

存在 `{项目根}/openspec/` 时，不得只做 diff 表面 CR。

**步骤 2 — 读未归档提案**

- 目录：`openspec/changes/` 下除 `archive/` 外的每个变更文件夹
- 至少读：`proposal.md`、`tasks.md`；若有则读 `design.md`、`specs/**/spec.md`
- 记录变更名、意图、tasks 状态、spec 要点（此阶段不绑 diff）
- CLI（可选）：`openspec list`、`openspec show <name>`

**步骤 3 后 — 匹配 diff**

1. 用步骤 3 的 diff 文件列表（`git diff --name-only` 等）
2. 与各提案的 tasks / design / specs / proposal 交叉比对 → **命中** `<change-name>`
3. 无命中：报告注明；有命中：MD 总结列出名称，步骤 4 以提案为主轴

**步骤 4 — 对齐 CR**

| 维度 | 要点 |
| ---- | ---- |
| 范围 | 是否超出 proposal 声明 |
| 需求 | delta spec ADDED/MODIFIED/REMOVED |
| 设计 | 是否符合 design.md |
| 任务 | tasks 勾选与 diff 是否一致 |
| 遗漏 | 提案要求未实现 → P1（必要可 P0） |

OpenSpec 问题标题前缀：`[OpenSpec · <change-name>]`
