---
name: fe-screenshot-to-task
description: >-
  将产品截图、UI 稿、PRD 交互说明转为可执行的前端任务 Markdown。
  仅产出前端范围任务；不确定处须 AskQuestion 确认；用户确认后才写入 task/*.md。
  Use when converting design screenshots or PRD images into frontend task documents.
disable-model-invocation: true
license: MIT
metadata:
  author: zeroanonx
  version: "2.0.0"
---

# Screenshot to Task

把截图/PRD 转成**前端任务清单**，写入被审项目的 `task/` 目录。

## 何时使用

- 用户提供 UI 截图、设计稿、PRD 交互说明
- 用户要求「拆任务」「写前端任务文档」「截图转 task」
- 触发：`/fe-screenshot-to-task`

**不要用于**：后端/API 设计、测试用例、部署方案——记入 §8 范围外，不单独成章。

## 工作原理

```text
1. 归档   保存截图 → task/screenshot/{任务名}/
2. 理解   读图 + 产品五问；有歧义 → AskQuestion 暂停
3. 准备   路由确认 + 任务拆解 + 可选代码映射（仅对话，不写文件）
4. 落盘   AskQuestion 确认摘要 → 用户同意 → 写入 task/{任务名}.md
```

**硬约束：步骤 4 之前禁止写入 `task/*.md`。**

## 步骤 1 — 归档

```text
{项目根}/task/screenshot/{中文任务名称}/{两位序号}-{描述}.{ext}
```

任务名未定用 `待命名`；落盘后按最终名称同步目录。

## 步骤 2 — 理解

按 [rules/extraction.md](rules/extraction.md) 落实**产品五问**，识别业务线、端、页面类型（新建/改造/组件）。

**确认门禁（全程）：** 交互、字段、业务线、状态流转、PRD/UI 冲突、截图不清等——**立即 `AskQuestion` 暂停**，不得猜测后继续。

```text
## 需您确认
- 问题：{不清楚的点}
- 我的理解：{如有}
- 涉及截图：{文件名}
- 可选：A. … / B. …
```

用户确认后记录结论，再继续。

## 步骤 3 — 准备

在对话中完成以下内容，**不写磁盘**：

| 子步骤 | 动作 |
|--------|------|
| 路由 | `AskQuestion`：新建路由 or 改造已有？新建须用户提供 path/name/菜单位置；改造须源 path/页面路径。**禁止自行推断路由。** |
| 拆解 | 按 [rules/task-template.md](rules/task-template.md) 准备 §0～§9（§0 尽可能详细） |
| 映射 | 有 `src/` 时扫描项目，任务细化到文件路径；参照同模块已有代码，见 [rules/coding-conventions.md](rules/coding-conventions.md) |

扫描优先：`src/router/`、`src/views/`、`src/pages/`、`src/api/`、`src/components/`、`src/composables/`。

## 步骤 4 — 落盘

### 4.1 呈现摘要

至少包含：任务名、业务线、端、做什么/怎么做、页面全景、核心路径、**已确认的路由**、读图阶段全部确认结论。

### 4.2 AskQuestion（不可跳过）

```text
标题：请您确认
问题：以上理解是否准确？是否需要补充？

选项：
- 理解准确，直接生成文档（Recommended）
- 理解有偏差，需要修正
- 需要补充内容
```

| 选择 | 处理 |
|------|------|
| 理解准确 | → 写入文件 |
| 有偏差 | 收集修正 → 更新摘要 → **重新 AskQuestion** |
| 需补充 | 收集补充 → 写入 §0 或 §9 → **重新 AskQuestion** |

禁止纯文字代替选择框；禁止未选「理解准确」就落盘。

### 4.3 写入

```text
{项目根}/task/{中文任务名称}.md
{项目根}/task/screenshot/{中文任务名称}/*
```

落盘后告知：文件路径、任务名、§9 待补充项说明。

## 产出结构

文档章节顺序见 [rules/task-template.md](rules/task-template.md)：

`§0 预览` → `§1 路由` → `§2 常量` → `§3 页面` → `§4 组件` → `§5 交互` → `§6 校验` → `§7 权限` → `§8 范围外` → `§9 待补充`

## 约束

| 允许 | 禁止 |
|------|------|
| 前端页面/组件/路由/交互/校验/权限任务 | API 章节、验证清单章节 |
| §0 详尽预览；§9 留待补充 | 用户确认前写 `task/*.md` |
| 代码任务标注参照文件 + JSDoc 要求 | 自行编造路由 path/name |
| 后端逻辑记入 §8 范围外 | 引入项目未使用的技术栈 |

质量门槛见 [rules/standards.md](rules/standards.md)。格式示例见 [examples/example-task-format.md](examples/example-task-format.md)。
