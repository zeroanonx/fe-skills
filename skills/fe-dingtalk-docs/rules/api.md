# DingTalk Docs API

## 认证

| Header     | 值                       |
| ---------- | ------------------------ |
| Cookie     | 完整浏览器 Cookie        |
| User-Agent | Chrome/Safari 桌面浏览器 |
| Referer    | 当前钉钉文档完整 URL     |

## 链接解析

当前支持：

```text
https://alidocs.dingtalk.com/i/nodes/{nodeId}?corpId=...
https://alidocs.dingtalk.com/i/nodes/{nodeId}?iframeQuery=entrance%3Ddata%26sheetId%3D...%26viewId%3D...
```

解析字段：

| 字段      | 来源                                  | 说明               |
| --------- | ------------------------------------- | ------------------ |
| node_id   | `/i/nodes/{nodeId}`                   | 文档 / 表格节点 ID |
| corp_id   | query `corpId`                        | 企业 ID            |
| sheet_id  | query 或 `iframeQuery` 中的 `sheetId` | 智能表格 sheet     |
| view_id   | query 或 `iframeQuery` 中的 `viewId`  | 智能表格 view      |

## 本 skill 使用的只读动作

| 操作     | 方法 | 目标                         |
| -------- | ---- | ---------------------------- |
| 检查登录 | GET  | 用户给出的 alidocs 页面 URL  |
| 读取页面 | GET  | 用户给出的 alidocs 页面 URL  |
| 提取正文 | 本地 | HTML body / 内嵌 JSON / meta |

> 不写死钉钉私有 API 路径。若后续确认稳定只读接口，可补充到本文件，并仍然只允许 GET 类读取。

## 禁止

| 操作         | 原因                 |
| ------------ | -------------------- |
| 新建文档     | 写入类能力           |
| 更新正文     | 可能破坏格式 / 图片  |
| 提交表格数据 | 写入类能力           |
| 修改权限     | 外部状态变更         |
| 删除 / 移动  | 破坏性操作           |

## 搜索与目录

当前不提供团队全局搜索和目录遍历。若需要扩展，必须先拿到已验证的只读接口样本，再把接口记录在本文件。
