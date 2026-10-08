# 最小项目文件结构与职责分层

团队最小目录基线。新建 Vue 前端项目或目标项目没有明确目录约定时采用以下结构；已有项目按现有规则接入，不为了套目录迁移无关文件。明确要求采用本结构时，以本结构约定为准。

```text
src/
├── assets/                      # 静态资源
│   ├── styles/                  # 全局通用样式、Tailwind（tw）入口
│   │   └── index.css            # 全局样式入口
│   ├── images/                  # 全局图片
│   └── icons/                   # 全局图标
├── components/                  # 全局通用组件，按职责分层
│   └── {组件层}/                # 层名沿用项目，如基础层、业务通用层
├── constants/                   # 全局通用常量，按业务模块分类
│   ├── modules/
│   │   └── {业务模块}.ts
│   └── index.ts                 # 公共导出入口
├── hooks/                       # 全局通用 hooks/composables
│   ├── modules/
│   │   └── use{业务能力}.ts
│   └── index.ts
├── views/                       # 页面/窗口
│   └── UserList/                # 路由页面目录大写开头（PascalCase）
│       ├── index.vue            # 页面入口
│       ├── constans.ts          # 页面私有常量，按团队约定保留此文件名
│       └── columns.ts           # 页面表格列配置
├── shared/
│   └── utils/                   # 全局通用函数封装
│       ├── modules/
│       │   └── {功能模块}.ts
│       └── index.ts
├── stores/                      # 状态存储，按业务模块分类
│   ├── modules/
│   │   └── {业务模块}.ts
│   └── index.ts
├── types/                       # 全局共享类型，按业务模块分类
│   ├── modules/
│   │   └── {业务模块}.ts
│   └── index.ts
├── router/                      # 路由注册、守卫与权限入口
└── directives/                  # 自定义指令
```

该树描述职责与落点，按功能需要创建文件；无表格页面不创建空 columns.ts，无私有常量不创建空 constans.ts。项目已有 constants.ts 等名称时遵从已有名称，不批量改成 constans.ts。

## 全局与页面私有边界

- assets/styles 只放全局入口、主题、复用样式和已使用的 tw 配置；页面样式留在页面/组件。项目未使用 Tailwind 时不新增依赖。
- assets/images/icons 放全局复用素材；页面专属资源按现有局部资源约定存放。
- components 的全局组件按职责分层；没有明确层名时参照已有组件或当前职责拟定，不创建只有空目录的层。单页组件留在对应 views 页面。
- constants/hooks/shared/utils/stores/types 的全局模块放 modules，index.ts 汇总公开能力。模块内部不通过自身 index 反向导入，避免循环。
- 页面 constans.ts 放私有枚举/默认值；columns.ts 放列定义和列相关适配。跨页复用后再提升到全局对应模块。
- views 的目录使用 PascalCase（如 UserList、OrderDetail）；路由 URL 和路由 name 分别沿用 router 的约定，不能因目录大写自动改变 URL。
- shared/utils 放无 UI 副作用的通用函数；hooks 封装响应式、生命周期或业务能力；stores 放共享数据与行为，不把三者混用。
- types 仅维护真实共享类型，页面私有类型留在当前模块；使用项目类型导出约定。
- router 管理路由和守卫，directives 管理 DOM 指令；页面不重复维护全局路由或指令注册。

## 扩展边界

请求层、入口文件、测试、构建配置等不在这份最小树中穷举。已有 api/http 等目录继续使用；确需新增职责时查项目约定，不将“最小结构”理解为禁止必要文件。

新增位置、命名和注册按 [文件规则](files.md)、[命名规则](naming.md)、[导入规则](imports.md) 核对。
