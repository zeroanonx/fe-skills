# Fe Design Analysis

分析设计稿中的布局、文字、图片、层级、样式和已提供的状态，形成前端开发与 UI 验收共用的清单。

## 怎么用

安装见[仓库 README](../../README.md)，安装或更新后重新开启 Agent 会话。

```text
/fe-design-analysis 分析这份 Figma 设计的商品列表页，提取布局和样式
/fe-design-analysis 分析附件截图，无法精确读取的值标为待确认
```

Codex 可用 `$fe-design-analysis`，也可说「分析这份设计稿，输出 UI 分析清单」。提供设计链接、`.pen` 或截图，以及页面/节点、目标端；有项目时补充项目位置，已有上下文可直接沿用。

## 产出

```text
{目标项目}/fe-spec/design-analysis/{页面或模块名}/{run-id}/
├── analysis.html    # 可视报告，交付时主动打开
├── analysis.md
└── screenshot/
```

清单包含来源、区域索引、逐区信息、样式与 token 对应、素材缺口、状态、实现建议、验收项和待确认项。run-id 防止覆盖历史；截图只在能真实保存时归档，用户指定输出路径时优先使用。

## 使用边界

- Figma、Pencil 使用当前环境可用工具；仅有截图时区分估算和实测，不编造字体、交互或断点。
- 从上到下、从左到右、从外到里分析，包含右侧和底部；没有源码也能分析。
- 本技能不直接写业务代码；拆产品任务用 `fe-screenshot-to-task`，实际页面验收用 `fe-ui-verification`。

详细流程见 [SKILL.md](SKILL.md)。

## 细则与 HTML 交付

分析细则按主题组织为独立文件，见 [规则索引](rules/analysis.md)。提取字段、检查点和示例按场景加载，修正过度绝对化的判断。

HTML 和 Markdown 同轮次、同内容生成；交付时主动打开本次 HTML 并检查渲染。打开受限时说明原因并提供文件链接，不能声称已打开。详见 [HTML 交付细则](rules/html-delivery.md)。
