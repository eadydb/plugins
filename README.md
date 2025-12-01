# Dev Workflow Tools

A Claude Code plugin marketplace providing essential development workflow tools for specification-driven development.

## Available Plugins

### Managing Specifications

Comprehensive specification-driven development (SDD) workflow management with spec-kit and OpenSpec support.

**Features**:
- Automatic project phase detection (greenfield/brownfield/legacy)
- Legacy code analysis and baseline spec generation
- Specification validation and quality checks
- Migration tools from spec-kit to OpenSpec

**Use cases**:
- Starting new projects with specification-first approach
- Adding features to existing codebases
- Adopting SDD for legacy projects

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
