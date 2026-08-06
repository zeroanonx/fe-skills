---
name: fe-create-rules
description: >-
  分析老项目技术栈与代码风格，生成 Cursor/Codex/Claude 编码规则。
  项目事实优先，不强行现代化。在用户维护老项目、生成 AI 规则时使用。
disable-model-invocation: true
license: MIT
metadata:
  author: zeroanonx
  version: "2.1.0"
---

# 生成 AI 编码规则

分析项目已有规范，生成可被 AI 长期遵守的规则文件。**项目事实优先，通用最佳实践其次**——不为「现代化」强行改变老项目风格。

## 何时使用

- 维护老项目，希望 AI 遵循原有代码风格
- 用户要求生成 `.cursor/rules`、`AGENTS.md`、`CLAUDE.md`
- 触发：`/fe-create-rules`

**不要用于**：大规模重构、替换技术栈、覆盖用户已有规则而不询问。

## 工作原理

```text
1. 扫描   读配置 + standards + 配套 skill + 抽样代码 + 目录树
2. 选择   AskQuestion：cursor / codex / claude
3. 生成   基于证据 + standards 提炼规则（短、准、可执行）
4. 写入   检查已有文件 → 合并或新建，禁止覆盖
```

**硬约束：**

- 步骤 1 中 **standards 始终加载**；**配套 skill 缺失即停止**
- 步骤 2 完成前禁止写入任何规则文件

---

## 步骤 1 · 扫描

### 优先读取

| 文件                                                   | 用途                  |
| ------------------------------------------------------ | --------------------- |
| `package.json`                                         | 依赖、脚本、包管理器  |
| `README.md`                                            | 运行方式、维护约定    |
| `vite.config.*` / `webpack.config.*` / `next.config.*` | 构建配置              |
| `tsconfig.json` / `eslint.config.*` / `.prettierrc*`   | TS/Lint/格式化        |
| `stylelint.config.*`                                   | 样式 Lint（有则必读） |
| `src/router/**` `src/views/**` `src/pages/**`          | 路由与页面组织        |
| `src/components/**` `src/api/**` `src/stores/**`       | 组件、请求、状态      |
| `tests/**`                                             | 测试习惯              |

缺失则跳过，在最终摘要注明。

### 抽样代码

读 2～3 个同模块真实文件，识别：命名、组件写法、请求封装、样式组织、注释风格。

### 目录树（必输出）

```text
src/
├── main.ts          # 应用入口
├── api/             # 接口封装，页面不直接调 SDK
├── components/      # 跨页面组件
├── views/           # 页面模块
└── router/          # 路由与权限
```

忽略 `node_modules`、`dist`、`.git`。无法判断用途标注「需确认」，不编造。大项目先输出核心目录并说明省略范围。

### 编码规范（始终加载）

**始终加载** [rules/standards.md](rules/standards.md)。

生成规则时：项目证据优先；与 standards 冲突时**以项目现状为准**，在摘要中说明；证据不足时从 standards 补充（标注「待项目确认」）。

### 规则优先级

1. 项目 Lint/构建配置
2. 真实代码中重复出现的模式
3. README / 团队文档
4. [rules/standards.md](rules/standards.md)
5. 框架通用最佳实践

**冲突时遵守项目现状**，在摘要中说明风险。

### 配套 skill（硬约束 · 缺失即停止）

读 `package.json` 判断技术栈。**任一所需 skill 缺失 → 立即停止**，输出安装指引，禁止继续步骤 2～4。

| 条件                                          | 所需 skill                    | 检测路径（任一存在）                                                                          |
| --------------------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------- |
| 含 `vue` / `@vue/` / `nuxt`                   | `vue-best-practices`          | `~/.cursor/skills-cursor/` 或 `~/.agents/skills/` 下的 `vue-best-practices/SKILL.md`          |
| 含 `react` / `react-dom` / `next`             | `vercel-react-best-practices` | `~/.cursor/skills-cursor/` 或 `~/.agents/skills/` 下的 `vercel-react-best-practices/SKILL.md` |
| 含 TS / `tsconfig.json` / 项目含 `.ts`/`.tsx` | `typescript-best-practices`   | `~/.cursor/skills-cursor/` 或 `~/.agents/skills/` 下的 `typescript-best-practices/SKILL.md`   |

缺失时输出：

```text
无法继续生成规则：缺少配套 skill。请先安装（安装后重新开启 Agent 会话）：

npx skills add hyf0/vue-skills@vue-best-practices -g -a cursor -y
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -a cursor -y
npx skills add cursor/plugins@typescript-best-practices -g -a cursor -y

安装路径：~/.cursor/skills-cursor/{skill-name}/
安装完成后重新执行 /fe-create-rules。
```

存在时读取对应 `SKILL.md` 全文，与 standards 叠加（冲突取更严格者，仍须服从项目现状优先原则）。

---

## 步骤 2 · 选择目标 AI

扫描完成后 **AskQuestion**（不可跳过）：

```text
请选择后续主要使用的 AI 工具：
- cursor（Recommended）
- codex
- claude
```

| 选择     | 产出                  |
| -------- | --------------------- |
| `cursor` | `.cursor/rules/*.mdc` |
| `codex`  | `AGENTS.md`           |
| `claude` | `CLAUDE.md`           |

未选择前：可展示分析摘要和大纲，**禁止写入文件**。

---

## 步骤 3 · 生成规则

依据 **standards + 配套 skill + 项目证据** 提炼；输出短规则，禁止复制 standards 全文。

### 必须写入的 AI 工作方式

- 改代码前先观察同目录已有写法，优先沿用
- 复用已有组件、utils、api、stores、types
- 不引入新框架/状态库/请求库/样式方案（除非用户要求）
- 不绕过 ESLint / Prettier / Stylelint / TS 配置
- 不为现代化重构无关老代码
- 新文件放在已有目录职责对应位置

### Stylelint（项目有时）

rules 中只写三项，**禁止**搬配置原文：

```markdown
样式校验：pnpm lint:style
修改 CSS/LESS/SCSS 后须 0 error 再交付。
常见：`order/properties-order` 重排属性；`no-descending-specificity` 调整选择器顺序。
```

新代码遵守 stylelint；改旧代码只修本次涉及范围。

### Cursor 格式（选 cursor 时）

```markdown
---
description: 项目编码规范
globs:
  - "**/*"
alwaysApply: true
---

# Project Conventions

## File Tree

## Coding Rules

## Style Rules

## AI Workflow
```

- 文件名 kebab-case，如 `project-overview.mdc`
- `globs` 尽量精准；仅全局规则用 `"**/*"`
- `alwaysApply: true` 只用于必须始终加载的规则
- 大项目拆分：`project-overview` / `coding-conventions` / `style-conventions` / `ai-workflow`
- 小项目合并：`project-conventions.mdc`

样式规则示例 globs：`**/*.{css,less,scss,vue}`

### Codex / Claude

复用同一份项目事实，转为单文件 `AGENTS.md` 或 `CLAUDE.md`，不生成 `.cursor/rules`。

---

## 步骤 4 · 写入

| 选择   | 检查                         |
| ------ | ---------------------------- |
| cursor | `.cursor/rules/` 已有 `.mdc` |
| codex  | 根目录 `AGENTS.md`           |
| claude | 根目录 `CLAUDE.md`           |

- 不存在 → 创建并写入
- 已存在 → 先读取，**禁止覆盖**；可补充缺失文件；冲突则展示 diff 由用户决定

---

## 最终摘要

- 技术栈、包管理器
- 目录树与关键文件
- 已加载 standards / 配套 skill
- 目标 AI 与生成/建议的文件列表
- ESLint / Prettier / Stylelint / TS 约束摘要
- 未确认项

---

## 约束

| 允许                            | 禁止                      |
| ------------------------------- | ------------------------- |
| 基于证据 + standards 生成短规则 | 写完整规范手册            |
| 合并补充已有规则                | 覆盖用户已有 rules        |
| 展示分析后再 AskQuestion        | 未选 AI 就写文件          |
| 项目现状优先                    | 无证据的强制规则          |
|                                 | 配套 skill 缺失时继续生成 |
|                                 | 把外部最佳实践当项目规范  |

## 相关资源

| 文件                                     | 用途                 |
| ---------------------------------------- | -------------------- |
| [rules/standards.md](rules/standards.md) | 编码标准（始终加载） |
