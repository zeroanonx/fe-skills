# 布局比对

从上到下、从左到右、从外到里核对指定范围。该维度必查，但问题等级按 [分级规则](comparison.md) 的实际影响决定。

- 对齐视口与页面状态后，核对区域位置、宽高、排列方向、列数、padding/gap/margin 和相邻距离。
- 容器留白读 [容器宽度](errors-page-container-width.md)；列数异常读 [Grid 宽度](errors-grid-container-width.md)。
- 列表不铺满读 [Flex 分配](errors-flex-layout.md)；换行不一致读 [跨行列宽](errors-flex-column-width.md)。
- 裁切读 [元素完整性](writing-element-completeness.md)；错位读 [对齐](errors-alignment.md)。
- 样式失效读 [层叠](errors-css-priority.md)；按钮读 [尺寸](errors-button-dimensions.md) 与 [定位](errors-button-position.md)。
- 记录区域边界实测与设计期望，未支持的断点只报告可用性，不编造设计还原要求。

每项记录通过、存在差异、未验证或不适用；后两者写原因。差异用稳定 ID 关联设计与实际证据，不将未验证计为通过。
