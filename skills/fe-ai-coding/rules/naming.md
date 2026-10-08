# 命名规则

新增或重命名标识符、目录、文件时读取。先查项目明确约定与同模块现有命名；下表只作为缺少约定时的默认值，不用于批量改旧代码。

| 对象 | 默认方式 | 示例与边界 |
| --- | --- | --- |
| views 页面目录 | PascalCase，大写开头 | UserList、OrderDetail，入口 index.vue |
| 其他业务目录/路由 URL | 同级现状优先，缺约定时 kebab-case | 路由目录大写不等于 URL 必须大写 |
| 组件符号、类型、接口、类 | PascalCase | UserCard、UserQuery；不强制 I 前缀 |
| 变量/普通函数 | camelCase | selectedIds、normalizeQuery |
| 布尔状态 | is/has/can/should + 含义 | isSubmitting、hasMore、canEdit；避免双重否定 |
| 集合/单值 | 复数或业务集合名/单数 | users、user；沿用 userList 时保持一致 |
| 模块常量 | UPPER_SNAKE_CASE | PAGE_SIZE；局部临时量不强制大写 |
| 枚举 | 类型 PascalCase，成员沿用项目 | AuditStatus.APPROVED 或 Approved，不混用 |
| React hook/Vue composable | use + 能力名 | useFileUpload；仅普通工具不加 use |
| 事件处理 | onXxx 或 handleXxx，遵从项目 | 项目区分时 onFormSubmit 表示事件，handleSubmit 表示内部处理 |
| API | 操作 + 业务对象 | getUserList/getUserDetail/createUser/updateUser/deleteUser |

## 文件名与导出

组件目录可能是 user-card/index.tsx，也可能是 UserCard.tsx 或 UserCard.vue；以同目录为准，不统一强推一种。样式文件沿用 module.scss、scoped style 等项目约定，测试按既有 *.test.* / *.spec.* 命名。

文件名、导出名与业务职责相符，避免 data.ts、common.ts、utils2.ts、newPage.ts 等无法表达职责的名称。既有 Page/Loader/index 等约定名称不适用此限制。

## 语义一致

- 区分查询条件 query、提交 body、接口 DTO 与展示 model，避免同一名称代表不同单位或数据形态。
- 时间/容量等带单位：timeoutMs、sizeBytes；遵从项目单位约定，不静默换算。
- 缩写只使用团队共识；不把后端字段随意更名后破坏序列化契约。
- Props 事件、emits、store action 与调用方保持同一业务术语。
- 不全局禁止 fetch 等已有前缀；外部 API、框架文件名与事件契约不能随意重命名。

重命名前查引用、动态字符串、路由名与持久化键；仅为美观不扩大本次改动。

采用 [团队结构](project-structure.md) 时，页面私有文件按约定使用 constans.ts、columns.ts；全局模块名使用语义英文，公开入口 index.ts。已有 constants.ts 等拼写保持原有约定，不混用新旧名称造成重复定义。
