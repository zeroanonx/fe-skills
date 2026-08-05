# Review · 步骤 4

## 问题等级

| 等级 | 名称 | 写入 archive |
| :--: | ---- | :----------: |
| P0 | 阻塞 | 是 |
| P1 | 建议 | 是 |
| P2 | 可选 | 否 |

顺序 **P0 → P1 → P2**。依据 [rules/standards.md](../rules/standards.md) 及配套 Vue/React/TS skill。

## Archive 回归

步骤 3 拿到 diff 后，用 index「检测关键词」比对变更。结论规则见 [archive.md](archive.md)。

## OpenSpec

有 `openspec/` 时按 [context.md](context.md#openspec有-openspec-时必做) 在 diff 上匹配提案并重点 CR。

## 评分 A–D

| 评分 | 条件 | 建议合入 |
| :--: | ---- | -------- |
| A | 无 P0，P1 ≤ 2 | 是 |
| B | 无 P0，P1 ≥ 3 | 修复后合入 |
| C | 有 P0，均可快速修复（非安全、面小） | 修复后合入 |
| D | 多个 P0，或存在安全问题 | 否 |

- 安全问题不低于 C；严重漏洞 → D
- P2 不参与升降级

**报告字段**（HTML 在 header，MD 在「综合评估」）：评分、依据、P0/P1/P2 计数、建议合入、技术债。HTML 展示细则见 `template/code-review-result-html.md` 顶部规则表。

## 特殊场景

| 情况 | 报告 | archive |
| ---- | ---- | ------- |
| 通过 | 简洁；回归节仅命中时输出 | 不新增 |
| 仅 P2 | 含 code-diff 的建议 | 禁止写入 |
| 有 P0/P1 | 完整清单 | P0/P1 写入 cases |
