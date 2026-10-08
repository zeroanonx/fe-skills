# 换行后列宽不一致

**触发**：设计要求跨行同列等宽，实际末行元素明显变宽。

Flex 各行独立分配空间，`flex-grow: 1` 可拉伸末行。这是布局行为，只有违背设计才是缺陷。

需要跨行等宽时考虑现有 Grid 方案或固定 basis；选择 auto-fill/auto-fit 时检查空轨道与少量数据表现，不一概替换。

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
  gap: 16px;
}
```

对比第一行和最后一行实际卡片边界，验证 1 项、满行、差一项和窄视口。设计允许最后一行拉伸时不报错。
