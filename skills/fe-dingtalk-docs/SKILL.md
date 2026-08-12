---
name: fe-dingtalk-docs
description: >-
  通过 Cookie 读取钉钉文档 / 钉钉智能表格（alidocs.dingtalk.com）内容。
  只读：解析链接、读取正文、提取页面/内嵌数据；不支持新建、更新、删除或移动文档。
  在用户分享 alidocs.dingtalk.com 链接、要求读/总结钉钉文档时使用。
disable-model-invocation: true
license: MIT
metadata:
  author: zeroanonx
  version: "1.0.0"
---

# 钉钉文档

通过 Cookie 认证**只读**访问钉钉文档 / 钉钉智能表格。所有操作经 `scripts/dingtalk_docs.py` 完成，禁止直接 curl、禁止使用写入接口。

## 何时使用

- 用户分享 `https://alidocs.dingtalk.com/i/nodes/...` 链接
- 用户要求总结、读取、解析钉钉文档或钉钉智能表格
- 用户提及钉钉文档 / alidocs / DingTalk Docs / Cookie

**不要用于**新建、更新、删除、移动、分享权限变更、表格写入等操作。遇到写入需求时拒绝，并引导用户在钉钉文档网页端操作。

## 工作原理

1. 校验 Cookie（`credentials/cookie.txt`），并解析用户链接中的 `node_id`、`corpId`、`sheetId`、`viewId`
2. 将意图映射到 CLI 子命令（`cookie`、`info`、`read`）
3. 执行 `python3 scripts/dingtalk_docs.py <子命令> ...`
4. 返回标题、链接、结构化摘要，并附带完整文档链接

> 钉钉文档页面是 SPA，正文可能来自浏览器运行时接口。脚本只读取页面 HTML 与内嵌 JSON；若正文未出现在可读响应中，应提示用户提供已登录 Cookie 或补充只读接口样本，禁止猜测写入接口。

## 初始化

```bash
CLI="python3 scripts/dingtalk_docs.py"

# 检查鉴权（建议附带任意钉钉文档 URL）
$CLI cookie --check --url "https://alidocs.dingtalk.com/i/nodes/..."

# 保存 Cookie（用户从浏览器 DevTools → Network → Cookie 请求头复制）
$CLI cookie --set 'locale=zh_CN; token=...; ...'
```

**引导用户获取 Cookie：** 浏览器登录钉钉文档 → F12 → Network → 刷新文档页面 → 点击发往 `alidocs.dingtalk.com` 的请求 → 复制完整 `Cookie` 值（不要带 `Cookie:` 前缀）。

成功：`cookie --check --url <链接>` 返回 `{"ok": true, ...}`。  
失败：exit code `2` → 先更新 Cookie 再重试。

## 用法

```bash
CLI="python3 scripts/dingtalk_docs.py"
```

| 任务     | 命令                                      |
| -------- | ----------------------------------------- |
| 解析链接 | `$CLI info "<钉钉文档URL>"`               |
| 读文档   | `$CLI read "<钉钉文档URL>"`               |
| 读 JSON  | `$CLI read "<钉钉文档URL>" --format json` |

支持链接形态：

```text
https://alidocs.dingtalk.com/i/nodes/{nodeId}?corpId=...
https://alidocs.dingtalk.com/i/nodes/{nodeId}?iframeQuery=...sheetId=...viewId=...
```

## 输出要求

- **读文档：** 标题 + 链接 + 结构化摘要；正文太长时先摘要，再按用户要求展开
- **解析链接：** 输出 `node_id`、`corpId`、`sheetId`、`viewId`、清理后的 URL
- 对话中**不得**泄露 Cookie
- 读取失败时区分：Cookie 过期 / 无权限 / 页面未暴露正文 / URL 无效

## 约束

| 允许                      | 禁止                                    |
| ------------------------- | --------------------------------------- |
| 读取、总结、解析链接      | 新建、更新、删除、移动文档              |
| 读取页面 HTML 与内嵌 JSON | 调用写入接口、提交表格数据、变更权限    |
| 保存 / 检查本地 Cookie    | 在对话中输出 Cookie                     |
| 提示用户补充只读接口样本  | 猜测私有写入 API 或伪造已成功读取的正文 |

拒绝写入时使用：

```text
fe-dingtalk-docs 仅用于读取和查找，不支持新建、更新、删除或移动钉钉文档。请在钉钉文档网页端手动编辑。
```

## 故障排查

| 现象                   | 处理                                                    |
| ---------------------- | ------------------------------------------------------- |
| exit 2 / auth_error    | 重新获取并保存 Cookie                                   |
| 页面只有标题没有正文   | 钉钉正文可能由运行时接口加载；请补充只读接口样本        |
| 403 / 无权限           | 确认当前钉钉账号是否有该文档权限                        |
| 智能表格没有单元格数据 | 检查链接是否带 `sheetId` / `viewId`，或补充只读接口样本 |

API 细节见 [rules/api.md](rules/api.md)。
