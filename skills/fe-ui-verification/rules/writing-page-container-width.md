# 页面容器宽度

实现或修复前先确认设计是流式铺满、限宽居中还是侧栏加自适应内容，记录设计宽度和左右间距。不要将所有 max-width 当错误。

```css
/* 仅示意限宽居中；具体数值来自项目设计 */
.page {
  width: 100%;
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: 16px;
  box-sizing: border-box;
}
```

流式页面按可用容器宽度布局，侧栏宽度和父级 padding 一起计算。检查约定视口下是否出现非预期横向滚动、单侧留白或内容过窄；异常排查见 [容器错误](errors-page-container-width.md)。
