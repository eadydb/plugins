# Initialization Commands

## Prerequisites

### uv (for Python scripts and spec-kit)

```bash
# Install uv (includes uvx for spec-kit)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
uvx --version
```

**Note**: `uv` provides both the `uv` command (for running Python scripts) and `uvx` (for running spec-kit).

## spec-kit (for greenfield projects)

### Initialize

```bash
# Basic initialization
uvx --from git+https://github.com/github/spec-kit.git specify init PROJECT_NAME

# Creates structure:
# .
# ├── CLAUDE.md              # AI assistant configuration
# ├── memory/
# │   └── constitution.md    # Project charter
# ├── specs/
# │   └── 001-feature-name/
# │       ├── spec.md        # Feature specification
# │       ├── plan.md        # Implementation plan
# │       ├── research.md    # Technical research
# │       └── data-model.md  # Data structures
# └── templates/
```

### Available commands

- `/specify` - Create detailed specification
- `/plan` - Generate technical plan
- `/tasks` - Break down into tasks

## OpenSpec (for brownfield projects)

### Prerequisites

```bash
# Requires Node.js 16+
node --version
npm --version
```

### Initialize

```bash
# Install globally
npm install -g @fission-ai/openspec@latest

# Initialize in project
cd your-project
openspec init

# Creates structure:
# openspec/
# ├── specs/              # Current truth
# │   ├── project.md
# │   └── features/
# └── changes/            # Proposed changes
#     └── feature-name/
#         ├── proposal.md
#         ├── tasks.md
#         └── design.md
```

### Available commands

- `openspec proposal <name>` - Create change proposal
- `openspec apply <name>` - Implement changes
- `openspec archive <name>` - Archive completed changes
