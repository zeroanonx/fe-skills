# 对齐方式

确定布局轴向和设计对齐参照。`align-items` 控制交叉轴，row 时通常是垂直方向，column 时通常是水平方向。

```css
/* 设计为图标与单行文字垂直居中时 */
.icon-text {
  display: flex;
  align-items: center;
  gap: 8px;
}
```

多行描述可能需要 flex-start，文字行可能需要 baseline；不能统一替换为 center。核对文字可见字形、line-height、图标自身留白与外框，光看外框中心可能产生视觉偏移。

按钮/卡片检查 padding、margin 和定位参照；见 [对齐诊断](errors-alignment.md)、[按钮位置](errors-button-position.md)。
