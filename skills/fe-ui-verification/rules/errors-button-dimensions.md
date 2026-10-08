# 按钮尺寸诊断

必须用实际页面边界与截图核对，不能仅凭 padding 推算通过。

- 对比 width/height、min/max-size、box-sizing、边框、padding、font-size、line-height。
- 检查组件库 size、图标间距和 loading 图标是否改变外框。
- 覆盖约定的默认、hover、focus、active、disabled、loading 状态；未能触发标未验证。
- 长文案、窄视口检查换行、收缩与触达区域，不擅自压小文字来凑宽度。

记录设计尺寸、实际尺寸、测量单位及前后证据。位置问题另外按 [按钮定位](errors-button-position.md) 检查。
