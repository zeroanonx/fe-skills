# Scope · 步骤 3

## AskQuestion（三选一）

**必须先问**。禁止因「默认推荐选项 1」而跳过。

```
1. 当前分支 vs 远程主分支（推荐）— origin/main 或 origin/master … HEAD
2. 工作区 + 暂存区未提交变更
3. 特定文件或目录 — 叠加在 1 或 2 上
```

| 情形 | 行为 |
| ---- | ---- |
| 用户选中 1 或「推荐/默认」 | 执行选项 1 |
| 同条消息已写明范围（如「只审工作区」） | 映射对应选项，报告复述，可不重复弹窗 |
| 仅说「code review」未指明范围 | **必须** AskQuestion |

## Git 命令

**选项 1**

```bash
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

远程主分支不可用 → 提示 `git fetch origin`；仍不可用则中止。

**选项 2**：`git diff` + `git diff --cached`

**选项 3**：在选项 1 或 2 命令后加 `-- <path>`

## 写入报告「审查范围」

- HTML「范围选项」：只写描述，**禁止** `1 ·` / `2 ·` 前缀（编号仅 MD「本次审查总结」保留）
- 选项 1：远程主分支名、merge-base 短 hash、commit 数
- 选项 2：注明「仅未提交变更」
- 选项 3：路径过滤说明
