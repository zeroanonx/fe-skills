# 列表布局选择

先确认固定列、自动换列还是横向滚动；记录卡片宽度范围、gap、末行是否拉伸、跨行是否等宽。

```css
/* 多行等宽，允许窄屏收缩 */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: 16px;
}
/* 每行独立分配，末行可能拉伸 */
.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.item {
  flex: 1 1 280px;
  min-width: 0;
}
```

示例值需替换。固定列和 `flex-grow: 0` 在设计要求固定卡片时合理；半露卡片可能用于提示可滚动。flex-basis 不能使用 minmax，basis 也不是硬性最小宽度。

窄容器检查内容最小宽度、图片收缩和长文案；数据 0、1、多项及末行分别查看。异常定位见 [Grid](errors-grid-container-width.md)、[Flex](errors-flex-layout.md)、[跨行列宽](errors-flex-column-width.md)。
