# Fe Screenshot to Task

把产品截图、UI 稿、PRD 交互说明转成**可执行的前端任务文档**，写入被审项目的 `fe-spec/tasks/` 目录。

> **只写前端范围**：不含 API 章节、验证清单、后端逻辑；有歧义时会暂停问你，**确认后才写入文件**。

---

## 使用前必读

1. 路由 path/name **不会自行推断**，生成前须你确认新建或改造方案
2. 读图、交互、业务线等有不确定处 → Agent 会 **AskQuestion 暂停**
3. **用户确认前禁止写入** `docs.md`；落盘是最后一步

安装后重新开启 Agent 会话。

---

## 能做什么

| 能力 | 说明 |
| ---- | ---- |
| 截图归档 | 保存到 `fe-spec/tasks/{任务名}/screenshot/` |
| 产品五问 | 做什么 / 怎么做 / 从哪里到哪里 / 新建什么 / 点什么出什么 |
| 详尽 §0 | 整体任务预览：字段表、用户路径、全量点击操作、业务规则 |
| 路由确认 | 新建须 path/name/菜单位置；改造须源 path 与页面路径 |
| 代码映射 | 有 `src/` 时参照同模块已有代码细化到文件路径（可选） |
| 确认门禁 | 落盘前呈现理解摘要，你确认后才写入 |

## 文档章节

| 章节 | 内容 |
| ---- | ---- |
| §0 整体任务预览 | 核心业务说明（尽可能详细） |
| §1 路由与菜单 | 须先确认的路由方案 |
| §2～§7 | 常量、页面、组件、交互、校验、权限 |
| §8 范围外 | 后端等排除项 |
| §9 待补充项 | 用户后续填写（必填） |

格式示例见 [examples/example-task-format.md](examples/example-task-format.md)。

---

## 怎么用

### 触发

```text
/fe-screenshot-to-task
```

```text
/fe-screenshot-to-task 请根据这些截图生成前端任务文档
使用 fe-screenshot-to-task 分析 PRD 截图，映射到项目代码路径
```

### 工作流程

```text
1. 归档   截图 → fe-spec/tasks/{任务名}/screenshot/
2. 理解   读图 + 产品五问；有歧义 → AskQuestion
3. 准备   路由确认 + 任务拆解 + 可选代码映射（仅对话，不写文件）
4. 落盘   呈现摘要 → 你确认 → 写入 docs.md
```

### 产出位置

```text
{项目根}/fe-spec/tasks/
└── {中文任务名称}/
    ├── docs.md           # 任务文档
    └── screenshot/
        └── 01-xxx.png
```

---

## 注意

- 不要用于后端 API 设计、测试用例、部署方案
- 理解有偏差或需补充时，Agent 会修正后**再次请你确认**
- 详细模板见 [rules/task-template.md](rules/task-template.md)，流程见 [SKILL.md](SKILL.md)
