---
name: fe-code-review
description: >-
  对前端代码变更进行系统性审查，输出 P0/P1/P2 分级报告（HTML/MD），
  并在 fe-spec/code-review/archive 沉淀易错模式。
  在用户要求 CR、Code Review、PR/diff 审查、分支变更审查时使用。
disable-model-invocation: true
license: MIT
metadata:
  author: zeroanonx
  version: "2.2.0"
---

# 前端 Code Review

系统性审查前端变更，输出 HTML/Markdown 报告，用 `fe-spec/code-review/archive/` 沉淀易错模式供回归检查。

## 何时使用

- 用户要求 CR、Code Review、审查 PR/分支变更
- 用户要求评估代码质量、找 P0/P1 问题
- 触发：`/fe-code-review`

**不要用于**：大规模自动改代码、审查与本次 diff 无关的文件。

## 产出目录

```text
fe-spec/code-review/
├── archive/              # 易错模式库（建议提交 Git）
│   ├── index.md
│   └── cases/
├── code-review-result/   # HTML 报告（建议 gitignore）
└── backup/               # MD 备份（与 HTML 同 run-id）
```

Skill 包 `template/` 仅作读取，**禁止**在被审项目 `fe-spec/code-review/` 下创建 template。

## 工作原理

严格按序 7 步，**禁止跳步 1、3**。

```text
1. Archive   读 archive/index，记录检测关键词
2. Context   检测配套 skill + 加载 standards + OpenSpec（若有）
3. Scope     AskQuestion 确定范围 → 获取 diff
4. Review    P0→P1→P2 + archive 回归 + OpenSpec 对齐
5. Report    生成 HTML + MD（run-id，禁止覆盖）
6. Archive   P0/P1 抽象为普遍性错误模式（P2 禁止）
7. Deliver   open 本次 HTML + 输出绝对路径
```

---

## 步骤 1 · Archive 读取

路径：`fe-spec/code-review/archive/index.md`、`archive/cases/{序号}-{slug}.md`

1. 读 `index.md`（无则按本文「Archive 索引模板」创建）
2. 记录「检测关键词」与 case 链接
3. 高相关 case 按需预读 — 关注**普遍性原因**，非单次实例

步骤 3 取 diff 后在步骤 4 做回归比对。

---

## 步骤 2 · Context

### 项目文件

读 `package.json`、`README.md`、构建配置、`tsconfig.json`、eslint 配置、styles配置，和项目其他约束性配置。无 `package.json` 时在报告注明项目类型，不阻塞 CR。

### 编码规范

**始终加载** [rules/standards.md](rules/standards.md)。

### 配套 skill（硬约束 · 缺失即停止）

按技术栈检测，**任一所需 skill 缺失 → 立即停止**，输出安装指引，禁止继续步骤 3～7。

| 条件                                           | 所需 skill                    | 检测路径（任一存在）                                           |
| ---------------------------------------------- | ----------------------------- | -------------------------------------------------------------- |
| 含 `vue` / `@vue/` / `nuxt`                    | `vue-best-practices`          | `~/.cursor/skills-cursor/vue-best-practices/SKILL.md`          |
| 含 `react` / `react-dom` / `next`              | `vercel-react-best-practices` | `~/.cursor/skills-cursor/vercel-react-best-practices/SKILL.md` |
| 含 TS / `tsconfig.json` / diff 含 `.ts`/`.tsx` | `typescript-best-practices`   | `~/.cursor/skills-cursor/typescript-best-practices/SKILL.md`   |

缺失时输出：

```text
无法继续 Code Review：缺少配套 skill。请先安装（安装后重新开启 Agent 会话）：

npx skills add hyf0/vue-skills@vue-best-practices -g -a cursor -y
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -a cursor -y
npx skills add cursor/plugins@typescript-best-practices -g -a cursor -y

安装路径：~/.cursor/skills-cursor/{skill-name}/
安装完成后重新执行 /fe-code-review。
```

存在时读取对应 `SKILL.md` 全文，与 standards 叠加（冲突取更严格者）。

### Git 预检

检查 `.gitignore` 忽略 `fe-spec/code-review/code-review-result/`、`backup/`。缺失则步骤 7 提示追加。`archive/` 建议提交。

### OpenSpec（有 `openspec/` 时必做）

- **步骤 2**：读 `openspec/changes/` 未归档提案（至少 `proposal.md`、`tasks.md`）
- **步骤 3 后**：diff 文件列表与提案交叉匹配
- **步骤 4**：对齐 CR — 范围、需求 delta、设计、tasks 一致性；遗漏 → P1/P0；标题前缀 `[OpenSpec · <change-name>]`

---

## 步骤 3 · Scope

**AskQuestion 三选一，必须先问**，禁止静默默认：

```text
1. 当前分支 vs 远程主分支（推荐）— origin/main … HEAD
2. 工作区 + 暂存区未提交变更
3. 特定文件或目录 — 叠加在 1 或 2 上
```

| 情形                     | 行为                                 |
| ------------------------ | ------------------------------------ |
| 用户选 1 或「推荐/默认」 | 执行选项 1                           |
| 消息已写明范围           | 映射对应选项，报告复述，可不重复弹窗 |
| 仅说「code review」      | **必须** AskQuestion                 |

**Git 命令**

```bash
# 选项 1
REMOTE_MAIN=$(
  git rev-parse --verify origin/main 2>/dev/null ||
  git rev-parse --verify origin/master 2>/dev/null ||
  git rev-parse --verify main 2>/dev/null ||
  git rev-parse --verify master
)
git diff "$REMOTE_MAIN"...HEAD
git log "$REMOTE_MAIN"..HEAD --oneline
git diff --name-status "$REMOTE_MAIN"...HEAD
```

选项 2：`git diff` + `git diff --cached`。选项 3：加 `-- <path>`。远程主分支不可用 → 提示 `git fetch origin`。

**写入报告**：HTML 只写描述（禁止 `1 ·` 前缀）；选项 1 含主分支名、merge-base、commit 数。

---

## 步骤 4 · Review

**P0 → P1 → P2**，依据 standards + 配套 skill。

### 问题分级

| 等级 | 含义     | 写入 archive |
| :--: | -------- | :----------: |
|  P0  | 阻塞合入 |      是      |
|  P1  | 建议修复 |      是      |
|  P2  | 可选优化 |      否      |

每条须：**具体描述 + 文件行号 + 可运行修复示例**。禁止模糊好评。

### 评分 A–D

| 评分 | 条件                | 建议合入   |
| :--: | ------------------- | ---------- |
|  A   | 无 P0，P1 ≤ 2       | 是         |
|  B   | 无 P0，P1 ≥ 3       | 修复后合入 |
|  C   | 有 P0，均可快速修复 | 修复后合入 |
|  D   | 多个 P0 或安全问题  | 否         |

安全问题不低于 C；P2 不参与升降级。报告字段见 `template/code-review-result-*.md` 顶部规则表。

### Archive 回归

用 index「检测关键词」比对 diff。**命中** → 报告仅列命中项；**未命中/空** → 整段省略。

### 特殊场景

| 情况     | 报告               | archive          |
| -------- | ------------------ | ---------------- |
| 通过     | 简洁               | 不新增           |
| 仅 P2    | 含 code-diff 建议  | 禁止写入         |
| 有 P0/P1 | 完整清单（含行号） | 抽象为普遍性模式 |

---

## 步骤 5–7 · Report & Deliver

### 步骤 5 · 生成

1. 创建 `code-review-result/`、`backup/`、`archive/cases/`（若不存在）
2. `run-id` = `YYYYMMDD-HHmmss`（冲突加 `-2`…，**禁止覆盖**）
3. 写入：
   - `fe-spec/code-review/code-review-result/{branch}-{run-id}-code-review-result.html`
   - `fe-spec/code-review/backup/{branch}-{run-id}-code-review-result.md`

生成前读 `template/code-review-result-*.md` **顶部「生成规则」表**。

### 步骤 7 · 交付

```bash
open "{report-path}"    # macOS
```

聊天**必须**输出本次 HTML **完整绝对路径**。仅打开本次 `run-id` 文件。

---

## 步骤 6 · Archive 写入

仅 **P0 + P1**。**沉淀普遍性错误模式**，禁止复制单次 diff。

| 应该写                         | 禁止写                |
| ------------------------------ | --------------------- |
| 普遍性原因、典型表现、抽象标题 | 某文件第 N 行错了什么 |
| 检测关键词（回归用）           | 把 backup 原样粘贴    |

流程：从 P0/P1 **抽象** → 写入 case；同模式则**更新**非新建。

1. 新建/更新 `cases/{三位序号}-{slug}.md`（见下方模板）
2. 更新 `index.md`「摘要」— 写模式概括
3. 「代表实例」链接本次 backup

---

## Archive 模板

**index.md**（空索引仅保留表头）：

```markdown
# Code Review 错误模式索引

> 下次 CR 必读。命中关键词或模式时，读取对应 case 文件。

| ID  | 标签 | 摘要（模式 · 普遍性原因） | 检测关键词 | 首次发现 | 最后命中 | Case |
| --- | ---- | ------------------------- | ---------- | -------- | -------- | ---- |
```

**case 文件**：

```markdown
## [标签] {抽象模式名}

- **等级**: P0 | P1
- **首次发现**: YYYY-MM-DD | 分支 {branch}
- **最后命中**: YYYY-MM-DD | 分支 {branch}
- **文件模式**: `src/**/*.vue`（泛化 glob）
- **检测关键词**: `any`, 裸 `await` 等

### 普遍性原因

{为何反复出现 — 根因、认知误区}

### 典型表现

- {常见变体 1}
- {常见变体 2}

### 推荐写法

{可复用修正模式，非本次 diff 复制}

### 防止复现

- 对应 standards.md 规约条目
- ESLint / tsconfig / CR checklist

### 代表实例

- CR: [backup/{branch}-{run-id}-code-review-result.md](../../backup/...)
```

---

## 约束

| 允许                      | 禁止                     |
| ------------------------- | ------------------------ |
| 写 HTML/MD 报告与 archive | 只聊天不写 report/backup |
| P0/P1 沉淀普遍性错误模式  | 单次错误原样写入 archive |
| 读 Skill 包 `template/`   | 覆盖历史 report/backup   |
| OpenSpec 对齐（有则必做） | 配套 skill 缺失时继续 CR |
|                           | 步骤 5 完成前写 archive  |
|                           | 读/写被审项目内 template |

## 规范加载

| 文件                                                                       | 用途                 |
| -------------------------------------------------------------------------- | -------------------- |
| [rules/standards.md](rules/standards.md)                                   | 编码标准（始终加载） |
| [template/code-review-result-html.md](template/code-review-result-html.md) | HTML 报告骨架        |
| [template/code-review-result-md.md](template/code-review-result-md.md)     | MD 备份骨架          |
