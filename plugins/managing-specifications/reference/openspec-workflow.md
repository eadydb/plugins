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

**Trigger**: User explicitly requests implementation with keywords:
- Chinese: "实施", "开始实施", "实施这个提案", "实施提案", "执行", "开始执行", "继续实施"
- English: "implement", "start implementation", "implement this proposal", "implement the proposal", "execute", "start executing", "resume implementation"

AND proposal status is "ready" (all files complete, tasks unchecked) or "implementing" (some tasks checked)

**Automated Behavior (via Claude Code managing-specifications skill)**:

1. **Detect ready state**:
   ```bash
   bash scripts/check-proposal-status.sh <proposal-name>
   ```

   Verification:
   - All 3 files exist (proposal.md, design.md, tasks.md)
   - tasks.md contains task items (format: `- [ ] Task description`)
   - At least one task is unchecked

2. **Direct execution** (NO interruption, NO TodoWrite, NO confirmation):
   - Read tasks.md to get task list
   - Execute tasks sequentially from first unchecked task
   - Mark each task complete in tasks.md as it's done: `- [ ]` → `- [x]`
   - Continue automatically until all tasks are checked
   - Do NOT create separate TodoWrite list
   - Do NOT ask for confirmation (user's "实施" IS the confirmation)

3. **During implementation**:
   - Update task checkboxes in tasks.md in real-time
   - Add implementation notes as comments if needed
   - Keep user informed of progress

4. **After completion**:
   - Suggest running tests if applicable
   - Ask if user wants to archive: `openspec archive <proposal-name>`

**Manual Steps** (if not using Claude Code):

1. Open `openspec/changes/<proposal-name>/tasks.md`
2. Work through each task in order
3. Mark completed tasks with [x]: `- [x] Completed task`
4. When all tasks done, run: `openspec archive <proposal-name>`

**Key Principle**:
When user says "实施/implement" for a ready proposal, treat it as explicit authorization. The system should execute directly from tasks.md without creating additional task lists or asking for confirmation. The user's implementation request IS the confirmation.

**Status-Based Behavior**:

| Status | Detected When | Action |
|--------|--------------|--------|
| ready | All files exist, all tasks unchecked | Start from first task |
| implementing | Some tasks checked, some unchecked | Resume from first unchecked task |
| completed | All tasks checked | Suggest archiving instead |
| draft | Missing files or no tasks | Ask user to complete proposal first |

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
