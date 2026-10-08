# 容器留白或宽度异常

**触发**：设计要求铺满但页面过窄，或设计限宽而页面过度拉伸。

1. 测量视口、父容器、内容外框与左右 padding；确认滚动条和侧栏占用。
2. 检查 width/max-width/min-width、box-sizing、grid/flex 分配和 margin。
3. 判断限制来自页面还是祖先，定位生效声明后局部修复。

若设计本身限宽居中，保留 max-width；若目标要求满宽，才移除错误限制。`width: 100%` 叠加 padding 在 content-box 下可能溢出，不能无条件添加。

复验原视口及受影响的相邻视口，记录修复前后边界。参照 [容器规则](writing-page-container-width.md)。
