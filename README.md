# Dev Workflow Tools

A Claude Code plugin marketplace providing essential development workflow tools for specification-driven development.

## Available Plugins

### Managing Specifications

Intelligent Specification-Driven Development (SDD) workflow management, supporting spec-kit and OpenSpec.

**Core Features** (v1.1.0):
- **Automatic Phase Detection**: Intelligently identifies Greenfield/Legacy/Brownfield project types
- **Legacy Project Automation**: Code analysis + baseline spec auto-generation + AI-assisted refinement
- **Phase Transition Suggestions**: Automatically detects and guides project transitions to the next phase
- **Intelligent Workflow Selection**: Automatically chooses spec-kit or OpenSpec based on project state
- **Quality Checkpoints**: Built-in specification completeness validation and quality assurance

**Use Cases**:
- New projects from scratch (Greenfield → spec-kit)
- Adding features to existing projects (Brownfield → OpenSpec)
- Adopting SDD for legacy codebases (Legacy → Analysis + OpenSpec)
- Migrating from spec-kit to OpenSpec (after completing initial development)

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
