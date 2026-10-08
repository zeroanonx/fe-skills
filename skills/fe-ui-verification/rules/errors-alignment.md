# 对齐偏差诊断

**触发**：图标、文字或操作区与设计参照线不一致。

先查 flex-direction 与交叉轴，默认对齐不能笼统说成 flex-start；核对 computed style。再查字体加载、line-height、baseline、图标 viewBox/透明留白及局部 transform。

单行垂直居中可使用 align-items: center，多行顶部对齐可使用 flex-start，文字基线可使用 baseline；按设计选择。

截图保留参照元素，记录边界和文字行信息。修复后验证长文案、不同字号和指定交互状态，参照 [对齐规则](writing-alignment.md)。
