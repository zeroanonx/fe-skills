# Archive Case 模板

> **读取位置**：Skill 包 `{skill-root}/template/archive-case.md`。
> **写入目标**：被审查项目 `code-review/archive/cases/{序号}-{slug}.md`。序号三位递增（如 `001-type-any-api`）。

````markdown
## [标签] 问题标题

- **等级**: P0 | P1
- **首次发现**: YYYY-MM-DD | 分支 {branch} | CR: backup/{branch}-{run-id}-code-review-result.md
- **文件模式**: `src/**/*.vue` 或具体路径
- **检测关键词**: `any`, `v-html`

### 原错误代码

```typescript
// 错误代码片段
```

### 问题分析

说明为何是问题。

### 优化代码示例

```typescript
// 推荐写法
```

### 防止复现

- 团队规范引用（如 standards.md 规约条目）
- 建议 ESLint / 审查 checklist 条目

### 状态

- [ ] 已在项目中修复
- [ ] 已加 lint 规则
````
