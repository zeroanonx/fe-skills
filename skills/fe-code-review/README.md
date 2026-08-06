# Fe Code Review

对前端代码变更做系统性审查，输出 P0/P1/P2 分级报告（HTML + Markdown），并在项目内沉淀易错模式供后续回归检查。

---

## 使用前必读

1. 被审查项目需为 **Git 仓库**，Agent 需能执行 `git diff`
2. 按项目技术栈需安装 **配套 skill**（Vue / React / TypeScript），缺失时本 skill **会停止**并提示安装命令
3. 报告与备份写入 `{项目根}/fe-spec/code-review/`，首次使用建议在业务项目 `.gitignore` 中忽略 `code-review-result/` 与 `backup/`

安装后重新开启 Agent 会话。

---

## 能做什么

| 能力          | 说明                                                   |
| ------------- | ------------------------------------------------------ |
| 分支/PR 审查  | 对比远程主分支或工作区变更，按 diff 审查               |
| 分级报告      | P0 阻塞 / P1 建议 / P2 可选，附文件行号与修复示例      |
| HTML 报告     | 生成交互式 HTML，完成后自动打开本次报告                |
| 易错模式库    | P0/P1 抽象为普遍性模式，写入 `archive/` 供下次 CR 回归 |
| OpenSpec 对齐 | 项目有 `openspec/` 时，自动对照未归档提案              |

## 审查依据

- 内置 [rules/standards.md](rules/standards.md)（始终加载）
- 配套 skill：`vue-best-practices` / `vercel-react-best-practices` / `typescript-best-practices`（按技术栈，**缺失即停止**）

---

## 怎么用

### 触发

```text
/fe-code-review
```

```text
帮我 CR 一下当前分支相对 origin/main 的变更
审查这次 PR 的前端代码
```

Skill 会先让你选择审查范围（三选一）：

| 选项      | 说明                                                       |
| --------- | ---------------------------------------------------------- |
| 1（推荐） | 当前分支 vs 远程主分支（`origin/main` 或 `origin/master`） |
| 2         | 工作区 + 暂存区未提交变更                                  |
| 3         | 特定文件或目录（叠加在 1 或 2 上）                         |

### 产出位置

```text
{项目根}/fe-spec/code-review/
├── archive/              # 易错模式库（建议提交 Git）
│   ├── index.md
│   └── cases/
├── code-review-result/   # HTML 报告（建议 gitignore）
└── backup/               # MD 备份，与 HTML 同 run-id（建议 gitignore）
```

建议在业务项目 `.gitignore` 追加：

```gitignore
fe-spec/code-review/code-review-result/
fe-spec/code-review/backup/
```

---

## 注意

- 本 skill **只产出报告**，不会自动改代码
- 配套 skill 缺失时无法继续，安装后需重新开启 Agent 会话
- 每次 CR 使用新的 `run-id`，**不会覆盖**历史报告
- 详细流程见 [SKILL.md](SKILL.md)
