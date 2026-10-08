# Fe AI Coding

编写前端代码前读取项目规则和同类实现，按既有目录、类型、组件、API、路由、状态、主题与注释规范完成修改和校验。支持 React、Vue 等现有项目。

## 怎么用

安装见[仓库 README](../../README.md)，安装或更新后重新开启 Agent 会话。

```text
/fe-ai-coding 为当前列表页增加筛选，沿用项目接口、错误提示和样式规范
/fe-ai-coding 整理这个文件的业务分区，补充必要 JSDoc
```

Codex 可用 `$fe-ai-coding`；自然语言如「写代码按团队规范」「给这些 hook 补注释」也可触发。提供目标文件和需求即可，已有上下文不需重复填写。

## 执行方式

1. 查看适用 rules、校验配置与同类代码，确认局部规范。
2. 按任务加载注释、架构或样式细则，复用既有组件和公共契约。
3. 完成代码修改，处理状态异常、提示去重、主题与素材边界。
4. 运行必要检查，交付修改位置、行为、实际结果与未验证项。

## 主要约束

| 范围 | 约定 |
| --- | --- |
| 分区与注释 | 成对业务分区，关键逻辑 JSDoc，保留团队标签，避免注释墙 |
| 目录与组件 | 单页组件留在业务模块，公共组件按复用需要提取 |
| API | 复用请求层、类型与认证；统一错误提示不重复弹出，仍处理失败状态 |
| 路由与状态 | 保持现有路由来源与加载方式；局部状态不无故提升为全局/持久化 |
| 样式与素材 | 配置和真实 token 优先，缺失素材标明替换点 |
| Mock | 用户允许时按项目机制隔离，明确未接真实接口的范围 |
| 校验 | 项目门禁优先，检查结果与视觉验收分别说明 |

参考项目规则中的职责原则已提炼为通用约束，不强制安装 React、Zustand、Ant Design 或 ShenTu 依赖。用户要求和项目明确规则优先，其次为校验配置、既有写法、本技能默认约定。

## 产出

直接修改本次需要的代码、注释和必要测试；对话内提供文件链接、校验结果及限制。普通编码默认不新增报告或改写项目 rules；用户要求生成规则时按对应模式创建或合并。只要求补注释时不顺手重构业务。

详细流程见 [SKILL.md](SKILL.md)。

## 规则目录

细则位于 `rules/`，按场景读取：[新增文件](rules/files.md)、[命名](rules/naming.md)、[导入](rules/imports.md)、[类型](rules/types.md)、[组件](rules/components.md)、[API](rules/api.md)、[路由](rules/routing.md)、[状态](rules/state.md)、[Mock](rules/mock.md)、[文案](rules/content.md)、[样式](rules/styles.md)、[注释](rules/comments.md)、[校验](rules/validation.md)。[架构索引](rules/architecture.md) 统一说明各规则适用范围。

## 最小目录与规范生成

[团队最小结构](rules/project-structure.md) 定义 assets/styles/images/icons、分层 components、各全局模块的 modules/index、views/PascalCase/index.vue、页面 constans.ts/columns.ts、shared/utils、router 和 directives。新项目采用该基线，维护已有项目按真实目录接入。

```text
/fe-ai-coding 按团队最小结构新增 UserList 页面
/fe-ai-coding 扫描这个项目并生成 Cursor 编码规则
/fe-ai-coding 基于现有代码完善 AGENTS.md
```

[项目画像](rules/project-profile.md) 读取技术栈、配置、抽样代码与目录职责，[规则生成](rules/generate-project-rules.md) 支持 Cursor、Codex、Claude。目标工具已明确时直接使用；已有文件先读取再合并，规则冲突时展示具体差异。

语言和 Vue 的落地细节分别见 [语言规则](rules/language.md)、[Vue 规则](rules/vue.md)。
