## Context

前端 Agent Skills 分散在 `Zero/code-review`、`Zero/yuque-docs`、`Zero/screenshot-to-task` 三个独立 git 仓库。用户希望统一到 `fe-skills`，采用 Vercel Skills CLI 模式 A（Skill Package）：一条 `npx skills add` 安装多个 skill，无需 gstack 式 setup 脚本。

当前 `fe-skills` 仓库仅有 OpenSpec 脚手架（`.cursor/commands/opsx-*`、openspec 生成 skills），尚无实际业务 skill。源 skill 均采用「仓库内嵌套一层 skill 目录」结构（如 `code-review/code-review/SKILL.md`），需拍平为 `skills/<name>/`。

## Goals / Non-Goals

**Goals:**

- 将 code-review、yuque-docs、screenshot-to-task 完整迁入 `fe-skills/skills/`
- 提供根级 README 与 `.gitignore`，支持 `npx skills add zeroanonx/fe-skills --all -g` 安装
- 保持各 skill 运行时行为不变（产出路径、工作流、硬约束）
- 保留 skill frontmatter `name` 不变，避免破坏现有 `/code-review` 等触发方式

**Non-Goals:**

- 不迁移 create-rules、zero-skills 其余 skill（后续变更）
- 不删除 fe-skills 内 OpenSpec 自动生成文件（用户后续处理）
- 不修改旧独立仓库（本阶段仅 fe-skills 侧迁入）
- 不实现 `/fe-skills/review` 斜杠命名空间（沿用 `/code-review` 等现有 name）
- 不编写 setup 脚本或 Cursor Commands 包装层

## Decisions

### 1. 目录布局：`skills/<skill-name>/`

**选择**：所有 skill 放在 `fe-skills/skills/` 下，与 Vercel `agent-skills` 一致。

**理由**：Skills CLI 默认识别 `skills/`；与 OpenSpec、未来 README 分离清晰。

**备选**：skill 放仓库根目录 → 与 fe-skills 元文件混杂，否决。

### 2. 拍平嵌套：去掉仓库内重复目录名

**选择**：

| 源路径 | 目标路径 |
|--------|----------|
| `code-review/code-review/**` | `fe-skills/skills/code-review/**` |
| `yuque-docs/yuque-docs/**` | `fe-skills/skills/yuque-docs/**` |
| `screenshot-to-task/screenshot-to-task/**` | `fe-skills/skills/screenshot-to-task/**` |

**理由**：Skill Package 内一层目录即 skill 根；CLI 按 `skills/<name>/SKILL.md` 发现。

**不迁移**：各源仓库的 `.cursor/commands/*.md`（项目级 command，非 skill 包必需）；独立仓库 README 内容合并进 fe-skills 根 README 的 skill 清单节。

### 3. 保留 skill `name` 不变

**选择**：`name: code-review`、`name: yuque-docs`、`name: screenshot-to-task` 不改。

**理由**：用户已习惯 `/code-review` 等触发；Skills CLI 按 name 安装到同名目录；避免 breaking 已有文档与 muscle memory。

**备选**：改为 `fe-skills-review` → 需更新所有引用与用户习惯，本阶段否决。

### 4. 跨 skill 相对路径

**选择**：code-review 内 `../vue-best-practices/SKILL.md` 等路径**不修改**。

**理由**：安装后各 skill 在 `~/.cursor/skills/` 下仍为兄弟目录，相对路径继续有效；配套 skill 未安装时源 skill 已有降级逻辑。

### 5. 敏感文件与凭证

**选择**：

- `.gitignore` 添加 `skills/yuque-docs/credentials/cookie.txt`
- 保留 `cookie.txt.example`；不迁移源仓库中真实的 `cookie.txt`

**理由**：防止 Cookie 泄露；用户本地自行创建。

### 6. 安装与分发

**选择**：仅依赖 Skills CLI，不添加 `./setup`。

**安装命令**（写入 README）：

```bash
npx skills add zeroanonx/fe-skills --all -g -a cursor -a codex -y
npx skills update -g -y
```

**理由**：与模式 A 一致，维护成本最低；Cursor/Codex 双端由 CLI 处理 symlink。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 旧仓库用户仍用分散安装 | 后续在旧仓库 README 加迁移说明；fe-skills README 明确替代关系 |
| vue-best-practices 等未迁入，CR Vue 检查不完整 | 已有跳过逻辑；后续变更可迁入配套 skill |
| 源 skill 内硬编码路径假设 skill 包结构 | 迁移后检查 SKILL.md 内自引用路径（如 `rules/`）均为相对路径，应无需改 |
| yuque-docs Python 脚本依赖 | 保持 `scripts/yuque.py`，README 注明需 Python 3 |
| 双份维护窗口期 | 本变更完成后以 fe-skills 为唯一源码，旧仓库冻结 |

## Migration Plan

1. 创建 `skills/` 及三个目标目录
2. 从源仓库复制 skill 包内容（排除 `.git`、真实 cookie、`.cursor/commands`）
3. 添加根 `README.md`、`.gitignore`
4. 本地验证：`npx skills add ./fe-skills --list` 与 `--skill code-review` 试装
5. 手动 smoke test：各 skill 触发一次基本流程
6. （后续）旧仓库 README 指向 fe-skills；可选 archive 独立 repo

**Rollback**：删除 `skills/` 下新增目录即可；fe-skills 此前无业务 skill，无用户影响。

## Open Questions

- fe-skills GitHub remote 是否已创建为 `zeroanonx/fe-skills`？（README 安装命令依赖此 slug）
- 本变更合并后是否立即在旧三个仓库 README 加 deprecation _notice？（proposal 标为后续）
