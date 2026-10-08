# 分区与注释规范

遵守目标项目配置和明确约定；以下标签是团队默认写法，不要求重写无关旧代码。编写业务逻辑或整理注释时读取。

文中示例展示注释与分区结构，省略项目依赖和类型定义；实际交付必须补齐实现，不提交示例空壳。

## 注释标签速查

按代码角色选择注释标签，避免同一类代码一会儿写 `@function`、一会儿写普通注释。

| 代码角色 | 标签 / 写法 | 说明 |
| -------- | ----------- | ---- |
| 业务函数 / 事件处理 | `@function` | 说明函数做什么；有参数补 `@param`，非显然返回值补 `@return` |
| Vue 业务 computed | `@computed` | 说明派生的业务含义和使用目的 |
| Hooks / Composables | `@hooks` | 说明封装能力、使用场景和关键副作用 |
| API / 请求封装 | `@api` | 说明接口用途、关键入参、返回结构和错误处理约定 |
| 导出常量 | `@constant` | 说明常量业务含义，避免魔法值 |
| 枚举 / 字典 | `@enum` | 说明枚举值含义，和后端/字典来源保持一致 |
| 局部状态变量 | `//` 单行注释 | 说明状态含义，不给自解释临时变量加注释 |

## 重点规则：分区注释

当同一文件内有多个相关函数，或逻辑自然分为查询、表单、弹窗、上传、权限等模块时，优先使用成对分区注释。导入语句不需要分区。

使用要求：

- 文件已有分区时，新增函数必须放入语义匹配的既有分区；没有合适分区再新增
- 同一文件新增 3 个及以上业务函数，或同时涉及 2 个及以上业务模块时，应先建立分区
- 分区名要表达业务职责，不写 `工具方法`、`其它`、`公共方法` 这类兜底名，除非项目旧代码已有固定叫法
- 分区内部按“状态/变量 → computed/watch → 业务函数 → 事件处理”的项目既有顺序摆放；没有既有顺序时按业务调用链摆放
- 分区注释只包业务逻辑，不包 import、类型声明、纯常量集合和简单导出

```ts
/** *********************************** S 列表查询 **************************************** */

/**
 * @function 初始化查询
 */
function initQuery() {}

/**
 * @function 获取列表数据
 */
function getTableList() {}

/** *********************************** E 列表查询 **************************************** */
```

要求：

- `S` 与 `E` 后的分区名必须一致
- 分区名使用业务动作或模块名，如 `列表查询`、`表单提交`、`文件上传`
- 小文件只有 1～2 个简单函数时，不必为了形式加分区
- 禁止只写开始不写结束，或跨越多个无关职责形成超大分区

## 函数注释

业务函数、导出函数、复杂事件处理、异步流程函数必须写 JSDoc。简单 computed、纯展示格式化函数可按项目现有习惯处理。

```ts
/**
 * @function 按筛选条件刷新列表，查询期间保留上次结果
 * @param {UserQuery} query 查询参数
 * @return {Promise<void>}
 */
async function getTableList(query: UserQuery): Promise<void> {
  // getUserList 为项目已有请求封装，错误提示和异常边界遵从项目契约。
  const result = await getUserList(query);
  userList.value = result.list;
}
```

要求：

- 必填 `@function`
- 有参数时补 `@param`
- 有非显然返回值时补 `@return`
- 注释补充调用场景、约束或目的，不只重复函数名；类型与实现使用项目真实定义
- `async/await` 逻辑需要错误边界，不能只补注释掩盖异常处理缺失

## Vue computed 注释

Vue 中的业务 computed 必须写 `@computed` 注释，说明它派生的业务含义和使用目的。简单透传、纯格式化且项目同类代码不写注释时，可沿用项目现状。

```ts
/**
 * @computed 已选文件数量，用于控制批量操作按钮是否可用
 */
const selectedFileCount = computed(() => selectedFileList.value.length);
```

要求：

- 必填 `@computed`
- 注释说明“是什么”和“有什么用”，不要只重复变量名
- 复杂 computed 内部应拆出语义清晰的局部变量，避免把业务判断塞进模板
- computed 只做派生状态；有副作用的逻辑应放到 watcher、事件处理或业务函数中

## Hooks / Composables 注释

自定义 hooks / composables 必须写 `@hooks` 注释，说明它封装的业务能力、使用目的和关键副作用。包括 React `useXxx`、Vue `useXxx` composable，以及项目中以 hook 命名的业务封装。

```ts
/**
 * @hooks 已选文件数量，用于控制批量操作按钮是否可用
 */
function useSelectedFileCount(selectedFileList: Ref<FileItem[]>) {
  return computed(() => selectedFileList.value.length);
}
```

要求：

- 必填 `@hooks`
- 注释说明 hook 封装了什么能力、给哪个业务场景使用
- 有参数时补 `@param`；返回对象字段不直观时补 `@return`
- hook 内如有请求、订阅、缓存、事件监听、定时器等副作用，必须在注释中点明
- hook 返回值命名要与项目同类 hook 保持一致，避免调用方二次猜测

## API / 枚举注释

新增或修改请求封装、接口适配、业务字典、枚举常量时，必须补充对应注释，避免调用方猜字段含义。

```ts
/**
 * @api 获取文件列表，用于列表页初始化和筛选查询
 * @param {FileListQuery} query 查询参数
 * @return {Promise<FileListResponse>}
 */
export function getFileList(query: FileListQuery): Promise<FileListResponse> {
  // projectApi 为项目已有封装，路径和响应解构按真实接口填写。
  return projectApi.get<FileListResponse>('/files', { params: query });
}

/**
 * @enum 文件审核状态，与后端 auditStatus 字段保持一致
 */
export const FILE_AUDIT_STATUS = {
  pending: 1,
  approved: 2,
  rejected: 3,
} as const;
```

要求：

- API 注释说明接口用途和调用场景，不复制接口名
- 枚举注释说明业务来源，如后端字段、字典项、权限码或产品状态
- 新增状态值时同步检查使用方、展示文案和权限/操作矩阵
- 禁止在页面内临时复制一份同名枚举；优先复用已有 constants / enums

## 变量注释

状态变量、枚举、权限开关、表格列配置、表单默认值等需要说明业务含义；临时变量或名称清晰的局部变量不强制注释。

```ts
// 文件列表
const fileList = ref<FileItem[]>([]);

// 是否正在提交表单
const isSubmitting = ref(false);
```

导出的常量或枚举可使用 JSDoc：

```ts
/**
 * @enum 审核状态，与后端状态值保持一致
 */
export const AUDIT_STATUS = {
  pending: 1,
  approved: 2,
  rejected: 3,
} as const;
```

## 其它注释

使用标准单行注释标记后续工作：

```ts
// TODO: 接入后端返回的真实字段
// FIXME: 修复分页切换时的重复请求
```

要求：

- TODO / FIXME 必须说明具体待办，不写空泛占位
- 不保留调试注释、废弃代码块、无意义分隔线

## 模板与样式分区

HTML/Vue template 的大块业务区域可按项目习惯使用 `<!-- S 筛选区 -->` 与 `<!-- E 筛选区 -->`，名称一致；简单模板不强行添加。CSS/LESS/SCSS 用 `/* */` 说明主题映射、布局限制或组件覆写原因，分区只包相关职责，不复述每条属性。文件头作者/日期等元信息只在项目要求时添加，不生成虚假署名。
