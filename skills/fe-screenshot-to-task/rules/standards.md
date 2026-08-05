# 质量门槛

> 交付前自检。流程见 [SKILL.md](../SKILL.md)，模板见 [task-template.md](task-template.md)。

## 必达项

| # | 规则 |
|---|------|
| 1 | 有歧义必须 `AskQuestion`，用户确认后才继续 |
| 2 | 落盘前必须 `AskQuestion` 确认摘要 |
| 3 | **仅步骤 4** 可写入 `task/*.md` |
| 4 | 产出 `task/{中文任务名}.md` + 截图归档 |
| 5 | §0 详尽；§1 路由来自用户确认 |
| 6 | §8 范围外、§9 待补充项不可省略 |
| 7 | 禁止 API 章节、验证清单章节 |
| 8 | 含代码任务须标注参照文件，关键函数/变量要求 JSDoc |

## 代码任务（有代码库时）

1. 先读同模块相似文件，任务注明「参照 `路径`」
2. 目录/命名/写法与项目一致，不引入新体系
3. 关键函数、复杂变量、props/emits 须 JSDoc（以项目现有风格为准）

详见 [coding-conventions.md](coding-conventions.md)。

## 禁止

- 猜测后静默继续
- 跳过 AskQuestion 直接落盘
- 自行编造路由 path/name
- 步骤 4 之前写 `task/*.md`
