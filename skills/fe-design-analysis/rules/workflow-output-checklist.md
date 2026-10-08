# 输出、校验与打开

默认目录：`fe-spec/design-analysis/{模块}/{run-id}/`，同时生成 `analysis.html`、`analysis.md`，证据放 `screenshot/`。沿用入口定义的 run-id 与用户指定路径规则。

1. 按 [内容结构](output-analysis-checklist.md) 整理同一份分析内容。
2. 填写 [Markdown 模板](../template/analysis.md)，以 [HTML 模板](../template/analysis.html) 生成可阅读的 HTML；读取 [HTML 交付细则](html-delivery.md)。
3. 核对两份报告的范围、区域 ID、来源、数值、状态与待确认项一致。
4. 核对标题、目录锚点、表格、图片和相对链接；模板字段全部替换，无证据不造链接。
5. **主动打开本次 analysis.html** 并检查渲染；提供 HTML 与 MD 的绝对路径链接。无打开能力或调用失败时，说明原因和文件位置，不声称已打开。

输出前读取 [遗漏检查](checklist-common-misses.md)。缺少部分设计可交付标明限制的分析，不应因局部未知伪造完整结果。
