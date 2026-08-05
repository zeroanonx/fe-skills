# 代码实现规范

> 与 [SKILL.md](../SKILL.md) 配套。任务文档中涉及代码实现时，必须遵循本规范。

## 一、项目风格优先（硬约束）

生成或描述代码时，**必须先阅读项目现有代码**，沿用项目既有结构和体系，禁止引入与项目不一致的写法。

### Phase 4 必须扫描的内容

| 路径                                  | 提取什么                                    |
| ------------------------------------- | ------------------------------------------- |
| `package.json`                        | 框架、TS/JS、构建工具                       |
| `src/router/**`                       | 路由组织方式、模块拆分                      |
| `src/views/**` / `src/pages/**`       | 页面目录结构、命名、`<script setup>` 等写法 |
| `src/components/**`                   | 组件命名、props/emits 风格                  |
| `src/api/**` / `src/services/**`      | 请求封装方式                                |
| `src/constants/**`                    | 常量/枚举组织                               |
| `src/composables/**` / `src/hooks/**` | hooks 写法                                  |
| `src/utils/**`                        | 工具函数风格                                |
| `.eslintrc*` / `eslint.config.*`      | Lint 约束                                   |

### 对照原则

1. **找参照文件**：在同目录或同业务模块找 1～2 个最相似已有文件，任务中注明「参照 `xxx`」
2. **目录归位**：新文件放在项目已有目录职责对应位置，不自创目录层级
3. **命名一致**：变量、函数、组件、文件命名与项目现有风格一致
4. **导入一致**：alias 路径（如 `@/`）、相对路径规则与项目一致
5. **不引入新体系**：不新增项目未使用的状态库、请求库、样式方案，除非用户明确要求

任务中写代码时须标注：

```markdown
- [ ] 4.1 新建 `src/views/.../index.vue`（**新建页面**）
  - **参照**：`src/views/.../SimilarPage/index.vue`（同目录列表页写法）
  - 沿用项目 `<script setup lang="ts">` + Composition API 风格
```

无代码库时，任务中写明：

```markdown
- 实现时须先阅读项目同模块已有代码，匹配既有结构和风格
```

---

## 二、JSDoc 注释（硬约束）

任务文档中的**代码示例**及**实现要求**必须包含标准 JSDoc。执行任务的 AI/开发者须按此规范编写。

### 必须加 JSDoc 的范围

| 类型                     | 是否必须        | 说明                                |
| ------------------------ | --------------- | ----------------------------------- |
| 导出的函数/方法          | **必须**        | 含业务逻辑、接口调用、数据处理      |
| 复杂变量 / 常量对象      | **必须**        | 枚举、配置对象、状态映射            |
| 组件 props / emits       | **必须**（Vue） | 或项目已有的等效注释方式            |
| composable / hook 返回值 | **必须**        | 说明用途和返回值                    |
| 单行简单赋值             | 不必            | `const loading = ref(false)` 可不加 |

### 函数 JSDoc 标准格式

```ts
/**
 * @description 审核积分兑换申请
 * @param {string} id - 申请单 ID
 * @param {'approve' | 'reject'} action - 审核动作
 */
async function handleAudit(
  id: string,
  action: "approve" | "reject",
): Promise<void> {
  // ...
}
```

### 变量 / 常量 JSDoc 标准格式

```ts
/**
 * @description 兑换申请状态枚举
 */
export const EXCHANGE_STATUS = {
  pending: "待审核",
  approved: "已通过",
  rejected: "已拒绝",
} as const;

/**
 * @description 列表页筛选表单
 */
const searchForm = reactive({
  phone: "",
  status: undefined as string | undefined,
  dateRange: [] as string[],
});
```

### Vue 组件

```vue
<script setup lang="ts">
// 抽屉是否可见
const visible = defineModel<boolean>("visible", { default: false });

// 当前申请单 ID
const props = defineProps<{
  /** 申请单 ID */
  applicationId: string;
}>();

//  审核通过后通知父组件刷新列表
const emit = defineEmits<{
  success: [];
}>();

/**
 * @description 提交审核
 * @param {'approve' | 'reject'} action
 */
async function onAudit(action: "approve" | "reject") {
  // ...
}
</script>
```

若项目已有注释风格（如仅用 `@param` 不要 `@description`），**以项目现有文件为准**，任务中注明参照文件。

### 关键逻辑块注释

复杂 `if/else`、状态判断、权限分支等**关键逻辑**须加行内或块注释说明意图：

```ts
// 仅待审核态展示通过/拒绝按钮
const showAuditActions = computed(
  () => detail.value?.status === EXCHANGE_STATUS.pending,
);
```

---

## 三、任务中的代码写法

含代码片段的任务条目须同时满足：

1. 标注**参照文件**路径
2. 代码片段含**必要 JSDoc**（函数、关键变量）
3. 说明与项目哪部分风格保持一致

示例：

````markdown
- [ ] 4.1 新建 `src/views/MemberMarketing/PointsExchange/index.vue`
  - **参照**：`src/views/MemberMarketing/CouponList/index.vue`
  - 关键逻辑须加 JSDoc，示例：
  ```ts
  /**
   * @description 查询兑换申请列表
   * @param {typeof searchForm} params - 筛选参数
   * @returns {Promise<void>}
   */
  async function fetchList(params: typeof searchForm) { ... }
  ```
````

```

---

## 四、禁止事项

- 禁止不读项目代码就写与项目风格冲突的示例
- 禁止关键函数/变量无 JSDoc
- 禁止引入项目未使用的技术栈或目录结构
- 禁止 JSDoc 与项目已有同类文件风格明显不一致
```
