# Migrating from spec-kit to OpenSpec

## When to migrate

Migrate when:

- Core features are implemented
- Initial version is running
- Entering continuous iteration phase
- Team needs lightweight change management

## Migration process

### 1. Prepare for migration

```bash
# Create archive directory
mkdir -p docs/initial-specs

# Backup spec-kit files
cp -r specs/* docs/initial-specs/
```

### 2. Initialize OpenSpec

```bash
# Install and initialize
npm install -g @fission-ai/openspec@latest
openspec init
```

### 3. Convert core specifications

Transform key spec-kit documents:

**From specs/001-core/spec.md → openspec/specs/project.md**:

- Extract product vision
- List core features
- Document key decisions
- Remove implementation details

**From specs/001-core/plan.md → openspec/specs/architecture.md**:

- System architecture
- Technology stack
- Design patterns
- Integration points

**Keep specs/001-core/research.md as docs/technical-decisions.md**:

- Reference for future decisions
- Historical context

### 4. Update AI configuration

Edit `.claude/CLAUDE.md` or similar:

```markdown
# Specification Framework

This project uses OpenSpec for specification management.

## Structure

- `openspec/specs/`: Current project truth
- `openspec/changes/`: Proposed changes

## Workflow

1. Create proposal for new features
2. Refine with design details
3. Break down into tasks
4. Implement and test
5. Archive when complete

See docs/initial-specs/ for historical spec-kit documentation.
```

### 5. Train team

Create `docs/openspec-quickstart.md`:

- How to create proposals
- Change review process
- Archiving completed work
- When to update specs/

## Verification checklist

- [ ] OpenSpec initialized successfully
- [ ] Core specs migrated to openspec/specs/
- [ ] Historical specs archived in docs/
- [ ] Team documentation updated
- [ ] First test change proposal created
- [ ] CI/CD recognizes new structure

## Rollback plan

If migration issues arise:

```bash
# Remove OpenSpec
rm -rf openspec/

# Restore spec-kit
git checkout specs/

# Continue with spec-kit
```
