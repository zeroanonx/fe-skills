# Fe AI Coding

让 AI 在编写或修改前端业务代码前先熟悉目标库风格，并重点使用分区注释组织业务逻辑，再遵守团队的目录、导入、类型、状态、组件边界、文案、样式、注释和校验习惯。

> 它不是格式化工具，也不会替代项目已有 ESLint / Prettier / Stylelint / CSSLint / TS 配置；项目现有风格优先。

---

## 使用前必读

1. 先观察目标文件及同目录 2～3 个相似文件，优先沿用项目现状
2. 先确认包管理器、目录职责、导入导出方式、组件/API/状态管理模式
3. 新增或改造多个业务函数时，优先判断是否需要成对分区注释
4. 只给本次新增或修改的关键逻辑补注释，不为了形式制造注释墙
5. 涉及 CSS / Less / SCSS / Vue style 时，先检查 Stylelint / CSSLint / PostCSS 和 `package.json` 样式脚本
6. 导入语句和自解释的简单代码不需要分区或注释

安装后重新开启 Agent 会话。

---

## 能做什么

| 能力 | 说明 |
| ---- | ---- |
| 规范画像 | 编码前识别目标库包管理器、目录职责、导入导出、组件/API 模式 |
| 分区注释 | 核心能力：用成对分区注释组织查询、表单、弹窗、上传、权限等业务模块 |
| 函数 JSDoc | 为业务函数、导出函数、复杂事件处理补 `@function`、`@param`、`@return` |
| Computed 注释 | 为 Vue 业务 computed 补 `@computed`，说明派生含义和使用目的 |
| Hooks 注释 | 为 hooks / composables 补 `@hooks`，说明封装能力、使用目的和关键副作用 |
| API/枚举注释 | 为请求封装、导出常量、枚举字典补 `@api`、`@constant`、`@enum` |
| 变量说明 | 为状态、枚举、权限、配置、表格列等变量补业务含义 |
| 状态异常 | 按项目模式处理 loading、empty、error、disabled、submitting 和副作用清理 |
| 组件边界 | 沿用项目 props、emits、v-model、slots、组件拆分与复用方式 |
| 文案约束 | 复用 i18n、字典、文案常量或同类页面文案，不随手硬编码 |
| 样式一致性 | 检查样式 lint 配置和属性顺序，保证新增样式与目标库一致 |
| 资产复用 | 优先复用已有组件、hooks/composables、utils、api、stores、types、常量 |
| 公共约束 | 避免硬编码已有 i18n、字典、权限、路由、埋点、设计 token |
| 空行整理 | 保持函数、变量、分区之间一个空行，避免过密或过散 |
| 工程校验 | 按项目已有脚本跑必要 lint、typecheck、stylelint、测试 |

## 怎么用

### 触发

```text
/fe-ai-coding
```

```text
写这段前端代码时按团队注释规范处理
新增这些方法时按业务模块加分区注释
给这些 computed 补 @computed 注释
给这些 hook 补 @hooks 注释
给接口和枚举补 @api / @enum 注释
新增交互时按项目模式补齐 loading/empty/error 状态
这些按钮和提示文案要走项目 i18n/字典
帮我把这个 Vue 页面的方法和变量注释整理一下
改这个样式前先按项目 CSSLint/Stylelint 顺序来
```

---

## 注意

- 不用于大规模纯格式化或无关重构
- 不给 import、自解释临时变量、简单表达式强行加注释
- `async/await` 仍需真实错误处理，不能只靠注释掩盖风险
- 不新建平行目录体系，不引入新的框架、状态库、请求库或样式方案，除非用户明确要求
- 不把 `console.log`、`debugger`、临时 mock、无关格式化和 AI 生成标记带进最终代码
- 详细规则见 [SKILL.md](SKILL.md)
