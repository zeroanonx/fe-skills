# 设计分析规则导航

每次分析先读 [分析顺序](analysis-order.md) 与 [四类信息](analysis-priorities.md)，再按流程加载：

| 阶段 | 规则 |
| --- | --- |
| 获取设计 | [工具与来源](tools-design-guidelines.md) |
| 建立区域图 | [布局 Map](workflow-layout-map.md) |
| 逐区提取 | [元素提取](workflow-element-extraction.md) |
| 汇总样式 | [样式汇总](workflow-style-summary.md) |
| 输出前复查 | [常见遗漏](checklist-common-misses.md) |
| 给实现建议时 | [布局建议](implementation-guidelines.md)、[错误模式](implementation-common-errors.md) |
| 交付 | [输出检查](workflow-output-checklist.md)、[内容结构](output-analysis-checklist.md) |

提取字段、检查点与示例按场景加载，避免一次读取无关实现细则。

## 证据与数据口径

- 节点/标注实测、截图估算、待确认分开记录；每项保留设计来源、节点或截图引用。
- 示例值用于说明字段，不是项目默认值；未知参数写原因，不为凑完整字段猜测。
- 设计图层描述视觉分组，不强制对应 DOM；叠放顺序不直接推导 CSS z-index。
- 文案重复实例可引用公共规格，但各实例差异需保留；完整性只针对已确认分析范围。
- 相对坐标注明父级，尺寸注明单位和缩放；截图像素不直接等于 CSS 像素。
