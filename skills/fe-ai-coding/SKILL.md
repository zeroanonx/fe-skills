---
name: fe-ai-coding
description: >-
  编写或修改前端业务代码时，先读取项目规则与同类实现，再按既有目录、类型、组件、API、
  路由、状态、主题和注释约定落地并校验；支持识别项目规范及生成 Cursor/Codex/Claude 规则。
  在用户要求前端开发、补注释、调整样式、建立项目目录规范、生成 AI 编码规则或调用 /fe-ai-coding 时使用。
license: MIT
metadata:
  author: zeroanonx
  version: "1.2.1"
---

# 前端编码规范与分区注释

在目标项目的真实约束下完成代码修改，保持可复用的业务边界、清晰的分区注释和可验证的交付。适用于 React、Vue 等现有前端项目，新 Vue 项目以团队最小目录分层为基线，既有项目按真实约定接入。

## 何时使用

- 编写、修改、补全前端页面、组件、请求或交互逻辑
- 补充业务注释、整理函数分区、调整 CSS / Less / SCSS / Vue style
- 识别老项目约定，或按要求生成 `.cursor/rules/*.mdc`、`AGENTS.md`、`CLAUDE.md`
- 触发：`/fe-ai-coding`；Codex 可用 `$fe-ai-coding`，也可自然语言调用

不用于无关重构、全库格式化或为自解释代码制造注释。

## 规则优先级

1. 用户本次明确要求与适用的项目指令
2. 项目 Lint / Formatter / TypeScript / 构建配置
3. 同目录、同业务线反复出现的现有写法
4. 本技能的默认约定

先检查目标范围适用的 `AGENTS.md`、`CLAUDE.md`、`.agents/rules/`、`.cursor/rules/` 和团队文档，按目录/文件范围加载；不假定这些路径一定存在。规则与配置冲突时说明冲突并定位影响，不照抄旧代码绕过校验。只有影响实施且无法从现有证据解决的歧义才询问用户。

## 产出

- **编码模式**：本次任务需要的代码、必要注释与测试；交付修改位置、实现行为、实际校验结果和未验证项
- **规则生成模式**：目标工具对应的项目规则文件；交付目录画像、规则依据、文件链接和未确认项
- 普通编码不自动改写项目 rules；用户要求生成规则时，按 [规则生成流程](rules/generate-project-rules.md) 创建或合并对应文件。产出写入目标项目

## 工作流程

### 1. 选择工作模式

- **编码模式**：按本次任务识别局部规范，读取相关细则，修改代码并校验。
- **规则生成模式**：用户要求长期规则时，按 [项目画像](rules/project-profile.md) 扫描，执行 [规则生成](rules/generate-project-rules.md)。用户已指定目标工具时直接沿用，未明确时先确定输出格式。完成规则生成后直接交付，不进入业务编码步骤；用户同时要求写代码时再执行编码模式。

新建项目或指定采用团队目录时读取 [最小项目结构](rules/project-structure.md)，落实全局模块 modules/index、页面 PascalCase 目录和私有常量/表格列的职责边界。

### 2. 编码模式：熟悉局部规范

- 查看工作区变更，保留用户已有修改；读目标文件和 2～3 个可用的同类文件，小项目按实际数量
- 从 lockfile 与 `package.json` 确认包管理器、已有依赖和脚本；读相关 TS、Lint、Formatter 配置
- 确认目录职责、命名、导入导出、组件通信、请求封装、错误提示、路由、状态及文案来源
- 查找可复用组件、hooks/composables、utils、API、types、constants、素材和设计 token
- 较大修改在对话中简述 3～5 条已确认约定；小改动直接应用，不生成额外规范文档

### 3. 编码模式：按需加载细则

| 场景 | 读取 |
| --- | --- |
| 识别规范、输出目录画像 | [项目画像](rules/project-profile.md) |
| 新项目目录或职责分层 | [最小结构](rules/project-structure.md) |
| 生成项目 AI 规则 | [规则生成](rules/generate-project-rules.md) |
| Vue 组件或模板 | [Vue 细则](rules/vue.md) |
| 语言/模板写法 | [语言细则](rules/language.md) |
| 新建、移动、拆分文件 | [文件规则](rules/files.md)、[命名规则](rules/naming.md) |
| 调整导入导出或依赖 | [导入规则](rules/imports.md) |
| 请求模型、props、共享类型 | [类型规则](rules/types.md) |
| 创建或拆分组件 | [组件规则](rules/components.md) |
| 接口封装、调用和错误处理 | [API 规则](rules/api.md) |
| 新页面、路由和菜单 | [路由规则](rules/routing.md) |
| 状态、并发或副作用 | [状态规则](rules/state.md) |
| 后端未就绪、临时数据 | [Mock 规则](rules/mock.md) |
| 文案、字典和枚举展示 | [文案规则](rules/content.md) |
| 业务函数、注释、hooks/composables | [注释规则](rules/comments.md) |
| 样式、主题、图片/图标 | [样式规则](rules/styles.md) |
| 完成修改 | [校验与交付](rules/validation.md) |

完整职责导航见 [架构索引](rules/architecture.md)。

只读本次相关细则；不要为了使用技能而加载全部框架教程或引入新工具。

### 4. 编码模式：执行与交付

按上述细则完成本次必要改动，复用项目已有目录、公共契约和组件。状态/异常/文案按对应规则处理，业务函数保持清晰分区与必要说明。

完成后按 [校验与交付](rules/validation.md) 执行项目门禁，提供文件链接、行为变化、真实校验结果与未完成事项。用户仅要求补注释时，不扩展为业务重构或样式重写。
