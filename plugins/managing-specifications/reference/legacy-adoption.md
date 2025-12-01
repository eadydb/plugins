# Legacy Project Adoption Guide

For existing projects that want to adopt Specification-Driven Development (SDD) but weren't initialized with spec-kit.

## Table of Contents

- [Overview](#overview)
- [Phase 1: Analysis](#phase-1-analysis)
- [Phase 2: Refinement](#phase-2-refinement)
- [Phase 3: Adoption](#phase-3-adoption)
- [Common Pitfalls](#common-pitfalls)
- [Validation Checklist](#validation-checklist)
- [Maintenance](#maintenance)
- [Success Metrics](#success-metrics)
- [Example: Complete Adoption Flow](#example-complete-adoption-flow)
- [Usage Examples](#usage-examples)

---

## Overview

Legacy adoption follows a streamlined 3-step approach:

1. **Initialize**: Use one-command adoption to set up OpenSpec
2. **Analyze**: Generate project context for AI assistance
3. **Collaborate**: Work with AI to create comprehensive specs

## Quick Start (Recommended)

### One-Command Adoption

```bash
# From project root
bash scripts/adopt-sdd.sh
```

This will automatically:
1. Detect your project as "legacy"
2. Install and initialize OpenSpec (if needed)
3. Analyze your codebase and generate project context
4. Guide you through the next steps in Claude Code

## Manual Step-by-Step

### Step 1: Initialize OpenSpec

```bash
# Install OpenSpec (if not already installed)
npm install -g @fission-ai/openspec@latest

# Initialize in your project
openspec init
```

### Step 2: Analyze Project Context

```bash
# Generate project analysis for AI
uv run scripts/analyze-project-context.py
```

This scans your codebase and generates:

- `.claude/project-context.json` - Structured project analysis for AI

### What gets analyzed

- **Project type**: Python, Node.js, Go, Rust, Java, etc.
- **Directory structure**: Source, tests, configs, docs
- **API endpoints**: Routes and handlers (pattern-based detection)
- **Database schemas**: Migration files and model definitions
- **Dependencies**: Package managers and dependency files
- **Existing docs**: README, architecture docs, API docs

### Review generated specs

The auto-generated specs are **starting points**, not complete documentation:

```bash
# Read generated overview
cat openspec/specs/project.md

# Review architecture baseline
cat openspec/specs/architecture.md
```

Look for `[TODO]` markers - these indicate areas needing manual refinement.

## Phase 2: Refinement

### Collaborate with AI to refine

Work with Claude to enhance the baseline specifications:

**Example conversation:**
You: "Let's refine the architecture.md. Our API uses REST principles with
JSON responses. We have 3 main services: auth, tasks, and notifications."
Claude: I'll update architecture.md with these details...
[Updates file with service descriptions, API patterns, data flow]
You: "The tasks service handles CRUD for tasks, assignments, and priorities.
It uses PostgreSQL with connection pooling."
Claude: Adding tasks service details...

### Document core features

Create individual feature documents in `openspec/specs/features/`:

```bash
# Template for each feature
cat > openspec/specs/features/user-authentication.md << 'EOF'
# User Authentication

## Purpose
Secure user access with JWT-based authentication

## User Stories
- As a user, I want to sign up with email/password
- As a user, I want to log in and receive an access token
- As a user, I want my session to remain active for 24 hours

## Functionality
- User registration with email verification
- Login with credentials
- JWT token generation and validation
- Token refresh mechanism
- Password reset flow

## API Endpoints
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh
- POST /api/auth/reset-password

## Dependencies
- PostgreSQL (user table)
- Redis (token blacklist)
- Email service (verification emails)

## Technical Notes
- Tokens signed with RS256
- Passwords hashed with bcrypt (cost factor 12)
- Rate limiting: 5 login attempts per 15 minutes
EOF
```

### Add missing context

Update `project.md` with business context:

```markdown
## Business Context

**Industry**: Project management SaaS
**Target Users**: Small to medium teams (5-50 people)
**Key Differentiator**: Real-time collaboration features

## Core Value Proposition

Simplify task management with:

- Intuitive interface
- Real-time updates
- Flexible workflows
- Team collaboration tools
```

### Document architectural decisions

Add decision records to `architecture.md`:

```markdown
## Key Decisions

### Decision: Monolith vs Microservices

**Chosen**: Monolith
**Rationale**:

- Team size is small (3 developers)
- Shared database simplifies transactions
- Simpler deployment and monitoring
- Can extract services later if needed

### Decision: REST vs GraphQL

**Chosen**: REST
**Rationale**:

- Simpler for mobile client integration
- Better caching strategies
- Team has more REST experience
```

## Phase 3: Adoption

### Initialize OpenSpec

Once baseline specs are refined:

```bash
# Check if OpenSpec is installed
openspec --version

# If not, install
npm install -g @fission-ai/openspec@latest

# Initialize (will detect existing specs/ directory)
openspec init
```

### Create first change proposal

Test the workflow with a real feature:

```bash
# Propose a new feature
openspec proposal add-task-tags

# Edit the proposal
# openspec/changes/add-task-tags/proposal.md
```

Example proposal:

```markdown
# Add Task Tags

## Problem

Users cannot categorize tasks beyond projects. They need flexible tagging for:

- Cross-project organization
- Filtering and search
- Custom workflows

## Solution

Add tag system:

- Users can create custom tags
- Tags have colors for visual distinction
- Tasks can have multiple tags
- Filter tasks by tag(s)

## Impact

- New database table: `tags`
- New join table: `task_tags`
- New API endpoints: tag CRUD
- UI updates: tag input and filter components

## Alternatives Considered

1. Fixed categories - too rigid
2. Hierarchical tags - too complex for initial version
```

### Update team workflow

Document the new process in `README.md` or `CONTRIBUTING.md`:

````markdown
## Development Workflow (SDD with OpenSpec)

We use Specification-Driven Development. All changes follow this process:

1. **Propose**: Create change proposal in `openspec/changes/`
2. **Review**: Team reviews proposal before implementation
3. **Design**: Add detailed design if complex
4. **Tasks**: Break down into implementation tasks
5. **Implement**: Code following the spec
6. **Archive**: Merge completed changes to `openspec/specs/`

### Making changes

```bash
# Create proposal
openspec proposal feature-name

# After approval, implement
# Follow tasks in openspec/changes/feature-name/tasks.md

# When complete
openspec archive feature-name
```

See [OpenSpec documentation](https://github.com/fission-ai/openspec) for details.
````

## Common Pitfalls

### Over-documenting

- **Avoid**: Documenting every function and variable
- **Do**: Document system-level architecture and feature behavior

### Under-documenting

- **Avoid**: Vague descriptions like "handles data processing"
- **Do**: Specific details like "validates CSV, transforms to JSON, stores in PostgreSQL"

### Stale specifications

- **Avoid**: Specs that don't match current implementation
- **Do**: Update specs as part of every PR/commit

### Skipping refinement

- **Avoid**: Using auto-generated specs without review
- **Do**: Treat generated specs as first draft, refine with team

## Validation Checklist

Before considering adoption complete:

- [ ] Core features documented in `openspec/specs/features/`
- [ ] Architecture decisions explained
- [ ] API endpoints listed with methods and parameters
- [ ] Database schema documented
- [ ] Team trained on OpenSpec workflow
- [ ] First test change proposal completed successfully
- [ ] Team agrees specs match reality
- [ ] Process added to CONTRIBUTING.md

Validate specs with: `uv run scripts/validate-spec.py <spec-file>`

## Maintenance

### Keep specs synchronized

Add to CI/CD or pre-commit hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for unarchived completed changes
if [ -d "openspec/changes" ]; then
    for change in openspec/changes/*/; do
        if grep -q "Status: Completed" "$change/proposal.md" 2>/dev/null; then
            echo "Warning: Completed change not archived: $(basename $change)"
            echo "   Run: openspec archive $(basename $change)"
        fi
    done
fi
```

### Periodic reviews

Schedule quarterly spec reviews:

1. Verify specs match implementation
2. Update outdated sections
3. Remove obsolete features
4. Add missing context

## Success Metrics

You know adoption is successful when:

- Team references specs before coding
- Specs are primary source of truth
- Onboarding uses specs as guide
- Fewer "what does this do?" questions
- Code reviews reference specs
- Design decisions are documented

---

## Example: Complete Adoption Flow

### Starting point

```
legacy-project/
├── src/
│   ├── api/
│   ├── models/
│   └── services/
├── tests/
├── package.json
└── README.md
```

### After analysis

```bash
uv run scripts/analyze-legacy-project.py
```

```
legacy-project/
├── src/                    # Existing code
├── openspec/
│   └── specs/
│       ├── project.md      # Generated
│       ├── architecture.md # Generated
│       ├── features/       # Generated (empty)
│       └── analysis-report.json
├── package.json
└── README.md
```

### After refinement

```
legacy-project/
├── src/
├── openspec/
│   └── specs/
│       ├── project.md          # Refined with business context
│       ├── architecture.md     # Refined with decisions
│       └── features/
│           ├── auth.md         # Manually created
│           ├── tasks.md        # Manually created
│           └── notifications.md
└── README.md                   # Updated with SDD workflow
```

### After first change

```
legacy-project/
├── src/
│   └── api/
│       └── tags.js             # New feature implemented
├── openspec/
│   ├── specs/
│   │   ├── project.md
│   │   ├── architecture.md
│   │   └── features/
│   │       ├── auth.md
│   │       ├── tasks.md
│   │       ├── notifications.md
│   │       └── tags.md         # Archived from changes/
│   └── changes/                # Active changes
└── README.md
```

Now the project is fully adopted and iterating with SDD!

---

## Related Scripts

For migration from spec-kit, use: `bash scripts/migrate-to-openspec.sh`

See `migration-guide.md` for detailed migration instructions.

---

## Usage Examples

### Example 1: Starting a new project

**User request**: "Help me create a task management API"

**Skill behavior**:

1. Run `bash scripts/detect-phase.sh` → returns "greenfield"
2. Recommend spec-kit
3. Guide through specification creation:
   - Ask about core features
   - Ask about technical stack
   - Ask about constraints
4. Initialize: `uvx --from git+https://github.com/github/spec-kit.git specify init task-api`
5. Create detailed spec.md following spec-kit workflow

### Example 2: Adding feature to existing project

**User request**: "Add priority levels to tasks"

**Skill behavior**:

1. Run `bash scripts/detect-phase.sh` → returns "brownfield"
2. Check if OpenSpec exists
3. Create proposal: `openspec proposal add-task-priority`
4. Guide through proposal refinement:
   - Problem: Why priority needed?
   - Solution: How to implement?
   - Impact: What files affected?
5. Generate tasks.md with implementation steps

### Example 3: Legacy project adoption

**User request**: "I have an existing Express.js API, want to adopt SDD"

**Skill behavior**:

1. Run `bash scripts/detect-phase.sh` → returns "legacy"
2. Explain legacy adoption process
3. Run analysis: `uv run scripts/analyze-legacy-project.py`
4. Show generated baseline specs in `openspec/specs/`
5. Guide through refinement:
   - "What's the business purpose of this API?"
   - "Let's document the core features in openspec/specs/features/"
   - "Should we capture any architectural decisions?"
6. Once refined, initialize OpenSpec
7. Create first test change proposal

### Example 4: Migration from spec-kit

**User request**: "We're done with initial development, ready for iterations"

**Skill behavior**:

1. Confirm migration timing
2. Run `bash scripts/migrate-to-openspec.sh`
3. Read `docs/migration-notes.md` and guide through TODO items
4. Help convert first spec to OpenSpec format
5. Verify with test change proposal
