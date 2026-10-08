# 问题清单与双格式交付

在 `fe-spec/ui-verification/{模块}/{run-id}/` 生成 `report.html` 与 `report.md`，截图放 `screenshot/`。新轮次不覆盖历史，同次复验同步更新两份报告并追加记录。

内容字段使用 [Markdown 模板](../template/report.md)，展示使用 [HTML 模板](../template/report.html)，生成和打开遵循 [HTML 交付](html-delivery.md)。

每条问题有稳定 ID、区域/状态、复现步骤、设计期望、实测、影响、优先级、建议与状态；另设完整修改意见列表，包含同问题关联的选择 ID、方案、影响/依赖、验证方法和是否选中。统计区分发现总数、未关闭、复验通过、已确认例外；待复验不算关闭。无问题也保留环境、覆盖表和证据。

报告结论按入口规则选择通过、未通过、部分验证或受阻。没有可靠量化方法不得填还原度百分比。

交付前读取 [检查清单](workflow-checklist.md)，**主动打开本次 report.html**，检查真实渲染后给出 HTML 和 MD 绝对路径。打开失败明确说明，不用源码阅读代替已打开声明。

完整意见展示并打开报告后，按 [选择流程](workflow-modification-selection.md) 询问是否修改；收到选择后只执行所选项。
