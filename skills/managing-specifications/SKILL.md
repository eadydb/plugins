---
name: managing-specifications
description: "Manages specification-driven development with spec-kit and OpenSpec. Use when: starting new projects, creating specifications, adding features to existing codebases, generating specs from legacy code, adopting SDD for legacy projects, or migrating from spec-kit to OpenSpec."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Specification Management

Guides specification-driven development (SDD) by selecting the appropriate framework based on project phase.

## When to Use

- Starting a new project (greenfield → spec-kit)
- Adding features to existing codebase (brownfield → OpenSpec)
- Adopting SDD for legacy projects (legacy → analyze + OpenSpec)
- Migrating from spec-kit to OpenSpec

## Quick Start

Detect project phase first:

```bash
bash scripts/detect-phase.sh
```

| Result | Meaning | Action |
|--------|---------|--------|
| greenfield | No code, no specs | Use spec-kit → `reference/spec-kit-workflow.md` |
| brownfield | Has code + specs | Use OpenSpec → `reference/openspec-workflow.md` |
| legacy | Has code, no specs | Analyze first → `reference/legacy-adoption.md` |
| spec-kit-only | Has spec-kit, needs OpenSpec | Migrate → `reference/migration-guide.md` |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/detect-phase.sh` | Detect project state (greenfield/brownfield/legacy) |
| `scripts/analyze-legacy-project.py` | Generate baseline specs from existing code |
| `scripts/migrate-to-openspec.sh` | Migrate from spec-kit to OpenSpec |
| `scripts/validate-spec.py` | Validate specification completeness |

**Running Python scripts**: Use `uv run scripts/<script-name>.py`

**Example**:
```bash
uv run scripts/analyze-legacy-project.py --output-dir openspec/specs
uv run scripts/validate-spec.py specs/001-feature/spec.md
```

## Workflows

- **Greenfield (0→1)**: `reference/spec-kit-workflow.md`
- **Brownfield (1→N)**: `reference/openspec-workflow.md`
- **Legacy adoption**: `reference/legacy-adoption.md`
- **Migration**: `reference/migration-guide.md`
- **Initialization**: `reference/init-commands.md`

## Common Tasks

| User Request | Action |
|--------------|--------|
| "Create specification for [feature]" | Detect phase → spec-kit or OpenSpec |
| "Add new feature to existing project" | Create OpenSpec proposal |
| "Adopt SDD for this project" | Run legacy analysis first |
| "Ready for iterations" | Migrate spec-kit → OpenSpec |

## Quality Checklist

Before implementation:

- [ ] Specification exists and is complete
- [ ] Technical approach documented
- [ ] Tasks broken down and testable
- [ ] Design aligns with architecture

Validate specs: `uv run scripts/validate-spec.py <spec-file>`

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

## Version History

- v1.1.0: Refactored per Claude Code Skills best practices
- v1.0.0: Initial implementation
