# Vue 组件编码细则

Vue 修改按项目版本、现有组件模式和适用 Vue 技能处理；新 Vue 3 组件没有其他约定时采用 Composition API、script setup 与明确类型，维护旧组件不擅自整体迁移。

- SFC 标签顺序按项目约定；无约定时 template → script → style。script 内按 import、props/emits、状态、hooks、computed/watch、业务方法、生命周期、expose 的职责组织，复用业务分区。
- props、emits、v-model、slots 明确类型/用途；类型定义或运行时声明以实际使用方式决定，required/default 不机械强制二选一。
- 复杂模板表达式移入 computed 或业务函数；computed 只派生状态，有副作用的流程放事件/watch/composable。
- v-for 使用稳定业务 key；v-if/v-show 根据渲染成本与显隐频率选择，不使用索引掩盖项目顺序变化。
- 生命周期只编排初始化与清理，较复杂业务逻辑抽函数/composable；监听、订阅和计时器按生命周期停止。
- 组件样式保持项目 scoped/CSS Modules 等作用域，全局通用样式进入 assets/styles；指令集中在 directives，避免无理由手动 DOM 操作。
- 页面放 views/PascalCase/index.vue，私有常量与表格列按 [最小结构](project-structure.md) 分离；组件通信和样式命名继续沿用项目规范。
- 路由传参、懒加载、权限使用现有 router；不以共享持久化状态替代 URL 参数的正常导航职责。

复杂函数、computed 与 composable 注释见 [注释规则](comments.md)，运行时检查见 [校验](validation.md)。
