# 导入、导出与依赖

- 按 ESLint/Formatter 及相邻文件使用顺序，沿用相对路径或 alias；不为本次功能重排无关导入。
- 复用依赖前查 package.json、锁文件、项目封装与真实导出，避免使用当前版本不存在的能力。
- named/default export、barrel、type-only import 与项目一致；公共模块内部优先避免经自身 barrel 反向导入。
- 副作用 import（样式、polyfill、注册器）不可当普通导入随意排序，确认执行顺序影响。
- 路由和组件 lazy/dynamic import 保持既有加载边界，不重复懒加载同一入口。
- 不深引包私有路径，不引入第二套请求、状态、日期或 class 工具；确需新依赖时依据任务范围和用户要求处理。
- 修改导出时检查所有使用方；删除未用 import，不把诊断日志留入最终代码。
