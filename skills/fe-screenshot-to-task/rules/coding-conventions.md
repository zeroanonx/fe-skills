# 代码映射规范

> 步骤 3「映射」子步骤。无代码库时在任务中写 `{待映射}` 并注明「实现时须匹配项目结构」。

## 扫描路径

| 路径                                  | 提取                     |
| ------------------------------------- | ------------------------ |
| `package.json`                        | 框架、TS/JS、构建工具    |
| `src/router/**`                       | 路由组织方式             |
| `src/views/**` / `src/pages/**`       | 页面目录、命名、脚本风格 |
| `src/components/**`                   | 组件 props/emits 风格    |
| `src/api/**` / `src/services/**`      | 请求封装                 |
| `src/constants/**`                    | 常量/枚举                |
| `src/composables/**` / `src/hooks/**` | hooks 写法               |

## 对照原则

1. 找 1～2 个同模块相似文件作参照，任务中标注路径
2. 新文件放在项目已有目录职责对应位置
3. 命名、导入 alias、Composition API 写法与项目一致
4. 不引入项目未使用的状态库/请求库/样式方案

## JSDoc 范围

| 类型                        | 必须 |
| --------------------------- | ---- |
| 导出函数/方法（含业务逻辑） | ✓    |
| 复杂常量/配置对象           | ✓    |
| 组件 props / emits          | ✓    |
| composable 返回值           | ✓    |
| 简单 `ref(false)`           | 不必 |

```ts
/**
 * @description 查询列表
 * @param {typeof searchForm} params - 筛选参数
 * @returns {Promise<void>}
 */
async function fetchList(params: typeof searchForm): Promise<void> { ... }
```

项目已有注释风格优先于本示例。

## 任务条目写法

```markdown
- [ ] 3.1 新建 `src/views/Example/List/index.vue`（**新建页面**）
  - **参照**：`src/views/Example/SimilarList/index.vue`
  - 关键函数须 JSDoc（见上）
  - 来源：[01-列表页](screenshot/01-列表页.png)
```
