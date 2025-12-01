# Dev Workflow Tools

A Claude Code plugin marketplace providing essential development workflow tools for specification-driven development.

## Available Plugins

### Managing Specifications

智能化的规范驱动开发(SDD)工作流管理，支持 spec-kit 和 OpenSpec。

**核心特性** (v1.1.0):
- **自动阶段检测**: 智能识别 Greenfield/Legacy/Brownfield 项目类型
- **Legacy 项目自动化**: 代码分析 + 基准规范自动生成 + AI 辅助完善
- **阶段转换建议**: 自动检测并引导项目过渡到下一阶段
- **智能工作流选择**: 根据项目状态自动选择 spec-kit 或 OpenSpec
- **质量检查点**: 内置规范完整性验证和质量保证

**适用场景**:
- 从零开始的新项目（Greenfield → spec-kit）
- 为现有项目添加功能（Brownfield → OpenSpec）
- 为 Legacy 代码库采用 SDD（Legacy → 分析 + OpenSpec）
- 从 spec-kit 迁移到 OpenSpec（完成初始开发后）

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - For Python scripts (optional)

Install uv (optional, but recommended):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Quick Install

**Step 1: Add the marketplace**

In Claude Code, run:
```bash
/plugin marketplace add eadydb/plugins
```

**Step 2: Install plugin**

```bash
/plugin install managing-specifications@dev-workflow-tools
```

**Step 3: Restart Claude Code**

The plugin will be available after restart.

### Verify Installation

```bash
# Check installed plugins
/plugin

# View available skills
/help

# Test the plugin
"Create a specification for a new feature"
```

## Usage

Once installed, the plugin is automatically activated when relevant. Example prompts:

```
"Create a specification for the user authentication feature"
"Detect what phase my project is in for SDD"
"Analyze this legacy project and generate baseline specs"
```

## License

MIT License
