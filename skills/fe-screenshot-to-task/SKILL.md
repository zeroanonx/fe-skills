---
name: fe-screenshot-to-task
description: >-
  将产品截图、UI 稿、PRD 交互说明转为可执行的前端任务 Markdown。
  仅产出前端范围任务；不确定处须 AskQuestion 确认；用户确认后才写入 fe-spec/tasks/{任务名}/docs.md。
  Use when converting design screenshots or PRD images into frontend task documents.
disable-model-invocation: true
license: MIT
metadata:
  author: zeroanonx
  version: "1.0.0"
---

# Screenshot to Task

把截图/PRD 转成**前端任务清单**，写入被审项目的 `fe-spec/tasks/` 目录。

## 何时使用

- 用户提供 UI 截图、设计稿、PRD 交互说明
- 用户要求「拆任务」「写前端任务文档」「截图转 task」
- 触发：`/fe-screenshot-to-task`

**不要用于**：后端/API 设计、测试用例、部署方案——记入 §8 范围外，不单独成章。

## 产出目录

```text
fe-spec/tasks/
└── {中文任务名称}/
    ├── docs.md           # 任务文档
    └── screenshot/
        └── 01-xxx.png    # 截图归档
```

## 工作原理

```text
1. 归档   保存截图 → fe-spec/tasks/{任务名}/screenshot/
2. 理解   读图 + 产品五问；有歧义 → AskQuestion 暂停
3. 准备   路由确认 + 任务拆解 + 可选代码映射（仅对话，不写文件）
4. 落盘   AskQuestion 确认摘要 → 用户同意 → 写入 docs.md
```

**硬约束：步骤 4 之前禁止写入 `fe-spec/tasks/{任务名}/docs.md`。**

---

## 步骤 1 — 归档

```text
{项目根}/fe-spec/tasks/{中文任务名称}/screenshot/{两位序号}-{描述}.{ext}
```

任务名未定用 `待命名`；落盘后按最终名称同步目录。

---

## 步骤 2 — 理解

### 产品五问（必答，写入 §0）

| #   | 问题             | 提取要点                                    |
| --- | ---------------- | ------------------------------------------- |
| 1   | **做什么**       | 产品目标、用户动作、解决什么问题            |
| 2   | **怎么做**       | 页面/组件/交互如何实现                      |
| 3   | **从哪里到哪里** | 入口菜单 → 中间页 → 终点                    |
| 4   | **新建什么**     | 逐页标注：新建 / 改造 / 复用                |
| 5   | **点什么出什么** | 每个关键按钮 → 跳转/弹窗/抽屉/提交/状态变更 |

识别业务线（侧边栏、Logo、PRD 标题）；页面类型：新建 / 改造 / 新建组件 / 复用。

### 确认门禁（全程）

交互、字段、业务线、状态流转、PRD/UI 冲突、截图不清等——**立即 `AskQuestion` 暂停**，不得猜测。

```text
## 需您确认
- 问题：{不清楚的点}
- 我的理解：{如有}
- 涉及截图：{文件名}
- 可选：A. … / B. …
```

---

## 步骤 3 — 准备

在对话中完成，**不写磁盘**：

| 子步骤 | 动作                                                                                               |
| ------ | -------------------------------------------------------------------------------------------------- |
| 路由   | `AskQuestion`：新建 or 改造？新建须 path/name/菜单位置；改造须源 path/页面路径。**禁止自行推断。** |
| 拆解   | 按 [rules/task-template.md](rules/task-template.md) 准备 §0～§9（§0 尽可能详细）                   |
| 映射   | 有 `src/` 时扫描项目，参照同模块已有代码细化到文件路径                                             |

扫描优先：`src/router/`、`src/views/`、`src/pages/`、`src/api/`、`src/components/`、`src/composables/`。

**代码映射原则**：找 1～2 个同模块相似文件作参照；命名/目录与项目一致；关键函数须 JSDoc（以项目现有风格为准）。

---

## 步骤 4 — 落盘

### 4.1 呈现摘要

至少包含：任务名、业务线、端、做什么/怎么做、页面全景、核心路径、**已确认的路由**、读图阶段全部确认结论。

### 4.2 AskQuestion（不可跳过）

```text
标题：请您确认
选项：
- 理解准确，直接生成文档（Recommended）
- 理解有偏差，需要修正
- 需要补充内容
```

| 选择     | 处理                              |
| -------- | --------------------------------- |
| 理解准确 | → 写入文件                        |
| 有偏差   | 修正 → **重新 AskQuestion**       |
| 需补充   | 纳入 §0/§9 → **重新 AskQuestion** |

### 4.3 写入

```text
{项目根}/fe-spec/tasks/{中文任务名称}/docs.md
{项目根}/fe-spec/tasks/{中文任务名称}/screenshot/*
```

文档内截图链接：`screenshot/01-xxx.png`（相对于 `docs.md`）。

落盘后告知：目录路径、`docs.md` 位置、§9 待补充项说明。

---

## 约束

| 允许                              | 禁止                     |
| --------------------------------- | ------------------------ |
| 前端页面/组件/路由/交互/校验/权限 | API 章节、验证清单章节   |
| §0 详尽；§9 留待补充              | 用户确认前写 `docs.md`   |
| 代码任务标注参照 + JSDoc          | 自行编造路由 path/name   |
| 写入 `fe-spec/tasks/{任务名}/`    | 写入旧路径 `task/`       |
| 页面/路由/交互/校验/权限          | 后端/API/部署（记入 §8） |

## 规范加载

| 文件                                                               | 用途         |
| ------------------------------------------------------------------ | ------------ |
| [rules/task-template.md](rules/task-template.md)                   | 输出章节模板 |
| [examples/example-task-format.md](examples/example-task-format.md) | 完整格式示例 |
