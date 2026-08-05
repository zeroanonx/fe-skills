---
name: fe-yuque-docs
description: >-
  通过 Cookie 读取和搜索语雀私有文档。
  只读：总结正文、搜索知识库、查看目录；不支持写入。
  在用户分享 yuque.com 链接、要求读/搜/总结语雀，或提及语雀时使用。
license: MIT
metadata:
  author: zeroanonx
  version: "1.0.0"
---

# 语雀文档

通过 Cookie 认证**只读**访问语雀私有文档。所有操作经 `scripts/yuque.py` 完成，禁止使用 yuque-mcp 或直接调用 API。

## 何时使用

- 用户分享 `*.yuque.com` 文档或知识库链接
- 用户要求总结、搜索或浏览语雀内容
- 用户提及语雀 / Yuque Cookie / 读语雀文档

**不要用于**新建、更新或移动语雀文档——应拒绝并引导用户去语雀网页端操作。

## 工作原理

1. 校验 Cookie（`credentials/cookie.txt`），并从用户语雀链接解析 `base_url`
2. 将意图映射到 CLI 子命令（`read`、`search`、`books`、`toc`、`info`）
3. 执行 `python3 scripts/yuque.py <子命令> ...`
4. 返回结构化摘要，并附带完整文档链接

`base_url` 从用户提供的任意 URL 解析 `https://{租户}.yuque.com`，并保存到 `credentials/config.json`。

## 初始化

```bash
CLI="python3 scripts/yuque.py"

# 检查鉴权（需已保存 base_url，或附带 --url）
$CLI cookie --check
$CLI cookie --check --url "https://{租户}.yuque.com/group/book/doc"

# 仅保存 base_url
$CLI cookie --url "https://{租户}.yuque.com/..."

# 保存 Cookie（用户从浏览器 DevTools → Network → Cookie 请求头复制）
$CLI cookie --set 'lang=zh-cn; yuque_ctoken=...; _yuque_session=...'
```

**引导用户获取 Cookie：** 浏览器登录语雀 → F12 → Network → 刷新页面 → 复制完整 `Cookie` 值（不要带 `Cookie:` 前缀）。

成功：`cookie --check` 返回 `{"ok": true, "user": "...", "base_url": "..."}`。  
失败：exit code `2` → 先更新 Cookie 再重试。

## 用法

```bash
CLI="python3 scripts/yuque.py"
```

| 任务           | 命令                                                    |
| -------------- | ------------------------------------------------------- |
| 读文档         | `$CLI read "<文档URL>"`                                 |
| 读 JSON        | `$CLI read "<文档URL>" --format json`                   |
| 在知识库内搜索 | `$CLI search "关键词" --book-url "<知识库URL>"`         |
| 在团队内搜索   | `$CLI search "关键词" --group <团队login>`              |
| 列出知识库     | `$CLI books --group <团队login> --url "<任意语雀链接>"` |
| 知识库目录     | `$CLI toc --book-url "<知识库URL>"`                     |
| 解析 ID        | `$CLI info "<文档URL>"`                                 |

URL 格式：`https://{租户}.yuque.com/{group}/{book}/{doc}` — `{group}` 即 `--group` 的值。

## 输出要求

- **读文档：** 标题 + 链接 + 结构化摘要（默认）；仅当用户明确要求时才输出全文
- **搜索：** 表格列出匹配项（标题、知识库、URL）
- **目录 / 知识库列表：** 树形或表格，带链接
- 对话中**不得**泄露 Cookie

## 约束

| 允许             | 禁止                              |
| ---------------- | --------------------------------- |
| 读取、总结、搜索 | `write`、`create`、`title` 子命令 |
| 列知识库 / 目录  | 新建或编辑正文                    |
| `info` 查元信息  | 外部 MCP / 手动 curl              |

拒绝写入时使用：

```text
fe-yuque-docs 仅用于读取和查找，不支持新建或写入。请在语雀网页端手动编辑。
```

## 故障排查

| 现象                | 处理                                        |
| ------------------- | ------------------------------------------- |
| exit 2 / auth_error | 重新执行初始化；更新 Cookie                 |
| 缺少 base_url       | 任意命令加 `--url`，或对用户链接执行 `read` |
| 搜索无结果          | 加 `--book-url`；换关键词                   |

API 细节见 [rules/api.md](rules/api.md)
