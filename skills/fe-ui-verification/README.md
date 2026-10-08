# Fe UI Verification

在浏览器中把实际页面与设计稿对照，输出有证据、可复验的 UI 差异报告。

## 怎么用

安装见[仓库 README](../../README.md)，安装或更新后重新开启 Agent 会话。

```text
/fe-ui-verification 对照附件设计验收 http://localhost:5173/products，只输出问题
/fe-ui-verification 对照这份 Figma 验收，先列出修改意见供我勾选，之后按桌面 1440px 复验
```

Codex 可用 `$fe-ui-verification`，也可说「检查这个页面的设计还原度」。提供页面 URL、设计来源、目标视口/状态；可附 `fe-design-analysis` 的清单，但不是前置依赖。

## 产出

```text
{目标项目}/fe-spec/ui-verification/{页面或模块名}/{run-id}/
├── report.html    # 可视报告，交付时主动打开
├── report.md
└── screenshot/
```

报告包含环境与基准、覆盖情况、P0/P1/P2 差异、证据和复验状态。等级按影响判定，不把所有布局差异都定为 P0。默认新建轮次保留历史；同次复验追加记录，用户指定路径时优先使用。

## 使用边界

- 先列出全部修改意见并询问是否修改；用户勾选并提交所选 ID 后，执行对应修改并复验。
- 必须查看实际页面；没有浏览器、页面权限或设计基准时说明受阻/未验证范围。
- 结论为通过、未通过、部分验证或受阻，不输出无依据的还原度百分比。
- 已修改代码但未重新查看页面的项目标「已修复待复验」。

详细流程见 [SKILL.md](SKILL.md)。

## 细则与 HTML 交付

验收细则按主题组织为独立文件，见 [比对索引](rules/comparison.md) 与 [流程检查](rules/workflow-checklist.md)。提取字段、检查点和示例按场景加载，修正过度绝对化的判断。

HTML 和 Markdown 同轮次、同内容生成；交付时主动打开本次 HTML 并检查渲染。打开受限时说明原因并提供文件链接，不能声称已打开。详见 [HTML 交付细则](rules/html-delivery.md)。

## 选择修改意见

报告包含全部修改意见及默认未选的复选框。可使用对话多选，或在 HTML 勾选后生成指令并发回对话；也可直接回复「修改 UI-001、UI-003」。收到选择才开始修改。仅在报告内勾选不会自动启动 Agent。详见 [修改意见与勾选](rules/workflow-modification-selection.md)。

修改指令绑定本次报告的完整路径与更新时间。执行前核实清单版本、方案和依赖；没有待执行意见时直接交付，不再询问是否修改。
