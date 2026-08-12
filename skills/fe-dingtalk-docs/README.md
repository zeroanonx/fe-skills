# Fe DingTalk Docs

让 AI 通过 Cookie **读取和总结**钉钉文档 / 钉钉智能表格内容的 Skill。

> 本 skill 只读，不做新建、更新、删除、移动、权限变更或表格写入。写入请在钉钉文档网页端操作。

---

## 使用前必读

1. **Cookie 是登录凭证，只粘贴给 AI 用于读取文档，不要公开分享**
2. **只读、只总结**——写文档请用钉钉文档网页端
3. 当前读取方式优先解析页面 HTML 与内嵌 JSON；若钉钉将正文完全放到运行时接口里，需要补充只读接口样本

安装后重新开启 Agent 会话。

---

## 能做什么

| 能力     | 说明                                      |
| -------- | ----------------------------------------- |
| 读文档   | 读取钉钉文档正文，生成摘要或回答问题      |
| 读表链接 | 解析智能表格链接中的 `sheetId` / `viewId` |
| 解析链接 | 提取 `node_id`、`corpId`、清理后的 URL     |

## 不能做什么

| 能力         | 说明                     |
| ------------ | ------------------------ |
| 新建文档     | 请在钉钉文档网页端操作   |
| 更新正文     | 禁止调用写入接口         |
| 写入智能表格 | 禁止提交单元格或表单数据 |
| 改权限/移动  | 请在钉钉文档网页端操作   |

---

## 怎么用

### 第一次使用

```text
/fe-dingtalk-docs，读一下这个文档：https://alidocs.dingtalk.com/i/nodes/...
```

如果还没有 Cookie，AI 会提示你获取并粘贴 Cookie。你把 Cookie 发给它后，AI 保存到本地并继续读取。

### 日常使用

```text
/fe-dingtalk-docs，总结这个钉钉文档：https://alidocs.dingtalk.com/i/nodes/...
```

```text
/fe-dingtalk-docs，解析这个智能表格链接里的 sheetId 和 viewId：https://alidocs.dingtalk.com/i/nodes/...
```

### 若要求写文档

请明确拒绝：

```text
fe-dingtalk-docs 仅用于读取和查找，不支持新建、更新、删除或移动钉钉文档。请在钉钉文档网页端手动编辑。
```

---

## 如何获取 Cookie

1. 浏览器打开钉钉文档并登录：`https://alidocs.dingtalk.com`
2. 按 `F12` 打开开发者工具
3. 切换到 **Network / 网络** 面板
4. 刷新文档页面
5. 点击任意一条发往 `alidocs.dingtalk.com` 的请求
6. 在 **Headers / 标头** → **Request Headers / 请求标头** 中找到 `Cookie`
7. 复制完整 Cookie 值（不要带 `Cookie:` 前缀）
8. 粘贴到 Agent 聊天框

Cookie 会过期，过期后按同样步骤重新获取并粘贴即可。

详细流程与 CLI 说明见 [SKILL.md](SKILL.md)。
