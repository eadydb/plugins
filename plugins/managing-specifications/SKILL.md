---
name: managing-specifications
description: "Manages specification-driven development with spec-kit and OpenSpec. Use when: starting new projects, creating specifications, adding features to existing codebases, generating specs from legacy code, adopting SDD for legacy projects, or migrating from spec-kit to OpenSpec."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Specification Management

智能化的规范驱动开发(SDD)管理，根据项目阶段自动选择合适的框架和工作流。

## 核心能力

- **自动阶段检测**: 识别 Greenfield/Legacy/Brownfield 项目类型
- **智能框架选择**: Greenfield→spec-kit, Brownfield→OpenSpec
- **Legacy 项目采用**: 代码分析 + 基准规范自动生成 + AI 辅助完善
- **阶段转换建议**: 自动识别并引导项目过渡到下一阶段
- **全流程指导**: 从规范创建到迭代管理的端到端支持

## 自动行为（Skill 触发时）

当用户提出与规范相关的请求时，Skill 应该：

### 1. 首次检测项目状态

**必须执行**:
```bash
bash scripts/detect-phase.sh
```

根据检测结果决定后续行动。不要猜测项目类型，必须运行检测命令。

### 2. 根据项目阶段采取行动

#### Greenfield 场景（无代码 + 无规范）

**触发条件**: 检测结果为 "greenfield"

**自动化行为**:
1. 确认用户意图（创建新项目规范）
2. 收集需求信息：
   - 核心功能和用户故事
   - 技术栈偏好
   - 技术约束（性能、安全等）
   - 目标用户群体
3. 引导 spec-kit 初始化（如果未初始化）:
   ```bash
   # 推荐使用这个命令
   uvx --from git+https://github.com/github/spec-kit.git specify init <project-name> --here --ai claude
   ```
4. 协助完成规范文件：
   - `specs/001-<feature>/spec.md` - 详细需求规范
   - `specs/001-<feature>/plan.md` - 技术方案
   - `specs/001-<feature>/research.md` - 技术调研（如需要）

**检查点**: 确保每个规范文件完整且可实施

#### Legacy 场景（有代码 + 无规范）

**触发条件**: 检测结果为 "legacy"

**自动化行为**:
1. 检查是否已运行分析:
   - 查找 `.claude/project-context.json`
   - 查找 `openspec/specs/project.md`

2. 如未分析，**主动建议**运行采用流程:
   ```bash
   bash scripts/adopt-sdd.sh
   ```
   说明：这将自动初始化 OpenSpec 并生成基准规范

3. 分析完成后，**必须执行**:
   - 读取 `openspec/specs/project.md`
   - 读取 `openspec/specs/architecture.md`
   - 读取 `.claude/project-context.json`（项目分析数据）

4. 引导用户完善规范：
   - 识别所有 `[TODO]` 标记
   - 逐项询问细节并更新文件
   - 确保业务上下文、架构决策清晰

5. 建议创建功能文档:
   ```
   "让我帮你识别核心功能并在 openspec/specs/features/ 创建文档"
   ```

**完成标准**: 基准规范文件中 TODO 少于 5 个

#### Brownfield 场景（有代码 + 有规范）

**触发条件**: 检测结果为 "brownfield"

**自动化行为**:
1. 检查 OpenSpec 是否已初始化：
   - 查找 `openspec/` 目录
   - 如未初始化，建议运行 `openspec init`

2. 理解用户需求：
   - 新功能？修改现有功能？Bug 修复？

3. 创建变更提案:
   ```bash
   openspec proposal <feature-name>
   ```

4. 引导完成提案文件：
   - `proposal.md` - 问题陈述、解决方案、影响分析
   - `design.md` - 技术设计细节
   - `tasks.md` - 实施任务分解

5. 实施完成后，引导归档:
   ```bash
   openspec archive <feature-name>
   ```

### 3. 检测阶段转换需求

**在每次 Skill 触发时检查**:
```bash
bash scripts/detect-transition.sh
```

#### Greenfield → Brownfield 转换

**触发条件**:
- `specs/` 目录存在完整规范
- 有源代码实现（`src/`、`app/` 等存在）
- 用户提到"迭代"、"新功能"、"下一步"等关键词

**自动建议**:
```
"检测到你的项目已完成初始开发。建议迁移到 OpenSpec 以支持持续迭代。
运行: bash scripts/migrate-to-openspec.sh"
```

#### Legacy → Brownfield 转换

**触发条件**:
- `openspec/specs/` 已有基准规范
- 基准规范已被完善（TODO < 5）
- 用户提到"添加功能"、"修改"等关键词

**自动建议**:
```
"基准规范已完善！现在可以使用 OpenSpec 创建功能提案了。
你想添加什么功能？"
```

## 决策流程图

```
用户请求
   ↓
检测项目阶段（detect-phase.sh）
   ↓
┌─────────────┬──────────────┬─────────────┐
│ Greenfield  │   Legacy     │ Brownfield  │
└─────────────┴──────────────┴─────────────┘
     ↓              ↓               ↓
spec-kit 流程   分析+生成      OpenSpec 流程
     ↓              ↓               ↓
收集需求      运行 adopt-sdd   创建 proposal
     ↓              ↓               ↓
创建 spec.md   读取基准规范    完成 design.md
     ↓              ↓               ↓
编写 plan.md   引导完善 TODO   分解 tasks.md
     ↓              ↓               ↓
研究(可选)    验证完整性      实施和归档
     ↓              ↓               ↓
   检测转换       检测转换        持续迭代
```

## 快速采用

一键命令（推荐）:

```bash
bash scripts/adopt-sdd.sh
```

此命令会自动：
1. 检测项目阶段
2. 初始化对应框架（spec-kit 或 OpenSpec）
3. Legacy 项目：分析代码并生成基准规范
4. 引导后续步骤

手动检测阶段:

```bash
bash scripts/detect-phase.sh
```

| 检测结果 | 含义 | 推荐行动 |
|--------|------|---------|
| greenfield | 无代码、无规范 | 使用 spec-kit → `reference/spec-kit-workflow.md` |
| brownfield | 有代码、有规范 | 使用 OpenSpec → `reference/openspec-workflow.md` |
| legacy | 有代码、无规范 | 运行 adopt-sdd.sh → `reference/legacy-adoption.md` |
| spec-kit-only | 有 spec-kit，需要 OpenSpec | 迁移 → `reference/migration-guide.md` |

## 可用脚本

| 脚本 | 用途 | 何时使用 |
|------|------|---------|
| `scripts/adopt-sdd.sh` | **一键 SDD 采用**（推荐） | 任何新项目或 Legacy 项目开始采用 SDD |
| `scripts/detect-phase.sh` | 检测项目阶段 | Skill 首次触发时必须运行 |
| `scripts/detect-transition.sh` | 检测阶段转换 | 每次 Skill 触发时检查（自动） |
| `scripts/analyze-project-context.py` | 分析项目并生成基准规范 | Legacy 项目初次采用（由 adopt-sdd.sh 调用）|
| `scripts/migrate-to-openspec.sh` | 从 spec-kit 迁移到 OpenSpec | Greenfield 项目完成初始开发后 |
| `scripts/validate-spec.py` | 验证规范完整性 | 规范创建完成后、实施前 |

**Running Python scripts**: Use `uv run scripts/<script-name>.py`

**Example**:
```bash
# Recommended: one-command adoption
bash scripts/adopt-sdd.sh

# Or analyze project context separately
uv run scripts/analyze-project-context.py

# Validate specifications
uv run scripts/validate-spec.py specs/001-feature/spec.md
```

## Workflows

- **Greenfield (0→1)**: `reference/spec-kit-workflow.md`
- **Brownfield (1→N)**: `reference/openspec-workflow.md`
- **Legacy adoption**: `reference/legacy-adoption.md`
- **Migration**: `reference/migration-guide.md`
- **Initialization**: `reference/init-commands.md`

## 常见任务处理

| 用户请求示例 | 自动化行为 | 执行步骤 |
|------------|----------|---------|
| "为 [功能] 创建规范" | 1. 检测阶段<br>2. 选择框架<br>3. 引导创建 | Greenfield: spec-kit 完整流程<br>Brownfield: OpenSpec proposal |
| "为现有项目添加新功能" | 1. 确认 OpenSpec 存在<br>2. 创建提案<br>3. 完成 design/tasks | `openspec proposal <name>`<br>引导完善三个文件 |
| "采用 SDD 开发" | 1. 检测为 Legacy<br>2. 运行 adopt-sdd.sh<br>3. 引导完善规范 | 自动生成基准规范<br>AI 辅助完善 TODO |
| "准备迭代开发" | 1. 检测转换需求<br>2. 建议迁移<br>3. 执行迁移脚本 | `bash scripts/migrate-to-openspec.sh` |
| "完善项目文档" | 1. 读取现有规范<br>2. 识别 TODO<br>3. 逐项询问更新 | 针对 Legacy 项目基准规范 |
| "验证规范质量" | 1. 运行验证脚本<br>2. 报告问题<br>3. 建议改进 | `uv run scripts/validate-spec.py` |

## 质量检查点

### 规范完整性检查

**触发时机**: 规范创建完成后、实施前

**检查项**:
- [ ] 规范文件存在且完整
- [ ] 技术方案有明确文档
- [ ] 任务分解清晰可测试
- [ ] 设计符合项目架构
- [ ] 非功能性需求已考虑
- [ ] 依赖关系已识别

**自动验证**:
```bash
uv run scripts/validate-spec.py <spec-file>
```

### Legacy 项目特殊检查

**基准规范完成度**:
- [ ] `project.md` 中 TODO < 3
- [ ] `architecture.md` 中 TODO < 2
- [ ] 至少有 1 个功能文档在 `features/`
- [ ] 业务上下文清晰
- [ ] 架构决策有文档

**完成标准**: 当 TODO 总数 < 5 时，可以开始创建功能提案

### OpenSpec 提案质量

**proposal.md**:
- [ ] 问题陈述清晰
- [ ] 解决方案具体
- [ ] 影响分析完整
- [ ] 考虑了替代方案

**design.md**:
- [ ] API 变更明确
- [ ] 数据模型清晰
- [ ] 集成点已识别

**tasks.md**:
- [ ] 任务分解合理（每个 1-4 小时）
- [ ] 依赖关系正确
- [ ] 可独立测试

## Prerequisites

- **Python scripts**: Requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- **spec-kit**: Uses `uvx` (included with uv)
- **OpenSpec**: Requires Node.js 16+ and `npm`

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Error Handling

If commands fail, check prerequisites:

1. **Python scripts & spec-kit**: Requires `uv`
2. **OpenSpec**: Requires Node.js 16+ and `npm`

See `reference/init-commands.md` for installation commands.

## 版本历史

- **v1.1.0**: 智能化增强
  - 添加自动阶段检测和转换建议
  - Legacy 项目自动生成基准规范
  - 详细的决策逻辑和自动化行为
  - 完整的质量检查点
- **v1.0.0**: 初始实现
