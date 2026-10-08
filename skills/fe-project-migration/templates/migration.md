# {{module}} 迁移报告

- 模式 / 结论：{{mode}} / {{conclusion}}
- 轮次 / 更新时间：{{run_id}} / {{updated_at}}
- 旧项目参照：{{source_path_branch_commit}}
- 目标实施：{{target_path_branch_commit}}
- 已有改动保护：{{existing_changes}}
- 目标、包含范围、排除范围及约束：{{scope}}
- 环境与参照材料：{{environment_and_references}}

## 业务地图

| 入口/角色/状态 | 动作 | 数据与最终请求 | 后续/失败状态 | 依据 | 待确认 |
| --- | --- | --- | --- | --- | --- |
{{business_rows}}

## 新旧映射与决策

| 旧职责/位置 | 业务不变项 | 目标落点/复用 | 保留/适配/替代/删除/待确认 | 影响及验证 |
| --- | --- | --- | --- | --- |
{{mapping_rows}}

## 规则、规格与待确认项

{{rules_and_spec_links}}

{{unknowns_and_affected_batches}}

## 批次与实际变更

| 批次/依赖 | 范围/关联规则和场景 | 实现状态 | 验证状态 | 文件/版本/证据 |
| --- | --- | --- | --- | --- |
{{batch_rows}}

## 验收记录

| 场景/规则 | 条件/数据/操作 | 明确预期 | 实际结果 | 状态 | 环境/版本/证据 |
| --- | --- | --- | --- | --- | --- |
{{scenario_rows}}

## 门禁、遗留与续接

- 代码检查：{{code_checks}}
- 构建终态：{{build_result}}
- 发布/切换状态：{{release_status}}
- 失败、受阻、未执行与补验方式：{{gaps}}
- 下一步及所需决定：{{next_steps}}
- HTML：{{html_link}}

按模式和风险删减章节；替换全部占位符，未执行场景如实保留，示例不得作为实际证据。
