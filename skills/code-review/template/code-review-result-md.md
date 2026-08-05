# Code Review Markdown 备份模板

> **读取位置**：Skill 包 `{skill-root}/template/code-review-result-md.md`（禁止读被审查项目内 template）。
> **写入位置**：被审查项目 `code-review/backup/{branch}-{run-id}-code-review-result.md`。评分见 [workflow/review.md](../workflow/review.md)。

**生成规则（必须遵守）**

| 区块 | 规则 |
| ---- | ---- |
| 历史回归 | **仅输出「命中」项**；无命中或 archive 为空则**整节省略** |
| 综合评估 | 字段与 HTML header（grade / verdict / debt / stat-strip）保持一致 |
| P0/P1/P2 | 每条须含「原代码」与「修复/优化建议」代码块 |

````markdown
# Code Review 报告

## 本次审查总结

- 审查范围: [选项编号 + 描述，如「1 · origin/main...HEAD（merge-base abc1234），共 N 个 commit」]
- 文件数量: [数字] 个文件
- 变更类型: [新增/修改/删除]
- 审查时间: [时间戳]
- 分支: [分支名]

<!-- 仅当 archive 回归有「命中」项时输出；全部未命中或 archive 为空则整节省略 -->

## 历史问题回归检查

- [命中项列表 + case 链接]

## [P0] 阻塞性问题（必须修复）

### 1. [问题标题]

**文件**: `path/to/file.ts:行号`
**等级**: P0
**描述**: [具体问题描述]

**原代码**:

```typescript
// 错误代码
```

**修复建议**:

```typescript
// 正确代码
```

## [P1] 建议优化项（强烈建议）

### 1. [问题标题]

**文件**: `path/to/file.ts:行号`
**等级**: P1
**描述**: [优化理由]

**原代码**:

```typescript
// 当前代码
```

**优化建议**:

```typescript
// 推荐代码
```

## [P2] 可选建议（非强制）

### 1. [问题标题]

**文件**: `path/to/file.ts:行号`
**等级**: P2
**描述**: [具体问题描述]

**原代码**:

```typescript
// 当前代码
```

**优化建议**:

```typescript
// 推荐代码
```

## 综合评估

- **代码质量评分**: [A/B/C/D]
- **评分依据**: [如「无 P0，P1=1 → A」，见 scoring-rubric]
- **建议合入**: 是 / 否 / 修复后合入
- **技术债风险评估**: [低/中/高]
- **下次审查重点**: [重点关注项]
````
