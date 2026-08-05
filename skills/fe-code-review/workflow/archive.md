# Archive · 步骤 1 读 / 步骤 6 写

路径均在**被审查项目**：`code-review/archive/index.md`、`archive/cases/{序号}-{slug}.md`

## 步骤 1 · 读取

1. 读 `index.md`（无则按 Skill 包 `template/archive-index.md` 创建）
2. 记录「检测关键词」与 case 链接
3. 高相关 case 按需预读

回归比对在步骤 3 取 diff 后、步骤 4 执行。

## 步骤 6 · 写入

仅 **P0 + P1**；**P2 禁止**。

1. 新建 `cases/{三位序号}-{slug}.md`（模板：Skill 包 `template/archive-case.md`）
2. 同步更新 `index.md`
3. case 引用本次 `backup/{branch}-{run-id}-code-review-result.md`
4. 去重：同「标签 + 检测关键词」→ 只更新「最后命中」与 backup 链接

## 回归检查结论（写入报告）

- **命中** → HTML/MD 仅列命中项（含 case id）
- **未命中 / archive 为空** → **整段省略**（不写「未发现」占位）
