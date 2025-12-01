# OpenSpec Workflow (1→N Projects)

## Phase 1: Propose change

**Trigger**: New feature request or modification needed

**Steps**:

1. Create change proposal:

```bash
   openspec proposal add-feature-name
```

2. Edit `openspec/changes/add-feature-name/proposal.md`:
   - Problem statement: Why is this needed?
   - Proposed solution: What will change?
   - Impact analysis: What else is affected?
   - Alternatives considered

3. Collaborate to refine:
   - Clarify requirements
   - Identify edge cases
   - Consider existing architecture

## Phase 2: Design details

**Trigger**: Proposal is approved

**Steps**:

1. Create detailed design in design.md:
   - API changes
   - Database migrations
   - UI modifications
   - Integration points

2. List affected files and components

## Phase 3: Task breakdown

**Steps**:

1. Edit tasks.md with implementation steps:

```markdown
## Implementation tasks

- [ ] Update database schema (migrations/XXX_add_field.sql)
- [ ] Modify API endpoint (src/api/routes.js)
- [ ] Add validation logic (src/validators/feature.js)
- [ ] Update frontend component (src/components/Feature.jsx)
- [ ] Add tests (tests/feature.test.js)
- [ ] Update documentation (docs/api.md)
```

2. Order by dependencies
3. Estimate complexity for each task

## Phase 4: Implementation

**Steps**:

1. Work through tasks.md checklist
2. Mark completed tasks with [x]
3. Update proposal.md status as progress

## Phase 5: Archive

**Trigger**: All tasks completed and tested

**Steps**:

1. Archive change:

```bash
   openspec archive add-feature-name
```

2. Updates made:
   - Changes merged to `openspec/specs/`
   - Change folder removed from `openspec/changes/`
   - Project specs reflect new truth

## Quality gates

Before archiving:

- [ ] All tasks completed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Specs synchronized with implementation
