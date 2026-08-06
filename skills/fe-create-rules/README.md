# Fe Create Rules

分析老项目的技术栈与代码风格，生成可被 AI 长期遵守的编码规则。**项目事实优先**，不为「现代化」强行改变既有写法。

> 不是通用最佳实践模板——它从项目真实代码和配置里提炼约定，让 AI 改代码时更像原来的维护者。

---

## 使用前必读

1. 在**需要生成规则的目标项目**中打开 Agent 会话
2. 扫描完成后须先选择目标 AI：`cursor` / `codex` / `claude`，**未选择前不会写入文件**
3. 按项目技术栈需安装 **配套 skill**（Vue / React / TypeScript），缺失时本 skill **会停止**并提示安装命令
4. 若项目已有规则文件，本 skill **不会覆盖**，只会合并或补充

安装后重新开启 Agent 会话。

---

## 能做什么

| 能力 | 说明 |
| ---- | ---- |
| 项目扫描 | 读 `package.json`、Lint 配置、目录结构与抽样代码 |
| 目录树标注 | 输出带用途说明的项目文件树 |
| 编码规则 | 命名、组件写法、请求封装、样式与 AI 工作方式 |
| Stylelint | 项目有 stylelint 时，写入校验命令与常见修复项 |
| 多工具产出 | 按你的选择生成不同格式 |

## 产出位置

| 选择 | 产出 |
| ---- | ---- |
| `cursor` | `.cursor/rules/*.mdc` |
| `codex` | 项目根目录 `AGENTS.md` |
| `claude` | 项目根目录 `CLAUDE.md` |

大项目可拆分为 `project-overview`、`coding-conventions`、`style-conventions`、`ai-workflow`；小项目可合并为一个 `project-conventions.mdc`。

## 规则依据

- 内置 [rules/standards.md](rules/standards.md)（始终加载）
- 配套 skill：`vue-best-practices` / `vercel-react-best-practices` / `typescript-best-practices`（按技术栈，**缺失即停止**）
- **优先级**：项目 Lint/真实代码 > README > standards > 通用最佳实践；与项目冲突时以项目现状为准

---

## 怎么用

### 触发

```text
/fe-create-rules
```

```text
分析这个项目，生成 Cursor 编码规则
使用 fe-create-rules 扫描老项目，产出 AGENTS.md
```

### 工作流程

```text
1. 扫描   读配置 + standards + 配套 skill + 抽样代码 + 目录树
2. 选择   AskQuestion：cursor / codex / claude
3. 生成   基于证据 + standards 提炼短规则
4. 写入   检查已有文件 → 合并或新建，禁止覆盖
```

扫描完成后 Agent 会先问你：

```text
请选择后续主要使用的 AI 工具：
- cursor（Recommended）
- codex
- claude
```

---

## 注意

- 不会把 `standards.md` 全文复制进规则文件，只提炼可执行条目
- 已有 `.cursor/rules/` 或 `AGENTS.md` 时，冲突部分会展示 diff 由你决定
- 详细流程见 [SKILL.md](SKILL.md)
