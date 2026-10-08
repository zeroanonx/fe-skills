# Flex 分配异常

**触发**：设计要求均分/铺满，实际出现非预期留白或溢出。

先测量容器和项目，再查 flex-grow/shrink/basis、min/max-width、gap、wrap 与内容最小尺寸。固定宽卡片留白可能符合设计，不默认判错。

```css
/* 允许按剩余空间增长，基础尺寸为 280px */
.item {
  flex: 1 1 280px;
  min-width: 0;
}
```

basis 不是最小宽度；是否允许缩小按设计决定。不能在 flex 简写使用 Grid 的 minmax 函数。验证一项、多项、换行及长内容；末行等宽要求见 [跨行列宽](errors-flex-column-width.md)。
