# Quality Checkpoints

Comprehensive quality checks for specifications at different project phases.

## Specification Completeness Check

**When to Trigger**: After spec creation, before implementation

**Checklist**:
- [ ] Specification files exist and are complete
- [ ] Technical solution has clear documentation
- [ ] Task breakdown is clear and testable
- [ ] Design aligns with project architecture
- [ ] Non-functional requirements considered
- [ ] Dependencies identified

**Automated Validation**:
```bash
uv run scripts/validate-spec.py <spec-file>
```

## Legacy Project Special Checks

**Baseline Specification Completeness**:
- [ ] `project.md` has TODO < 3
- [ ] `architecture.md` has TODO < 2
- [ ] At least 1 feature document in `features/`
- [ ] Business context is clear
- [ ] Architectural decisions documented

**Completion Standard**: When total TODOs < 5, can start creating feature proposals

## OpenSpec Proposal Quality

### proposal.md
- [ ] Problem statement is clear
- [ ] Solution is specific
- [ ] Impact analysis is complete
- [ ] Alternative solutions considered

### design.md
- [ ] API changes are clear
- [ ] Data models are clear
- [ ] Integration points identified

### tasks.md
- [ ] Task breakdown is reasonable (each 1-4 hours)
- [ ] Dependencies are correct
- [ ] Independently testable

## Spec-Kit Specification Quality

### spec.md
- [ ] Problem statement and context clear
- [ ] User stories and acceptance criteria defined
- [ ] Success metrics identified
- [ ] Edge cases considered

### plan.md
- [ ] Architecture approach documented
- [ ] Technology choices justified
- [ ] Implementation steps clear
- [ ] Testing strategy defined

### research.md (if needed)
- [ ] Technical investigation complete
- [ ] Alternatives compared
- [ ] Recommendations clear
- [ ] Trade-offs documented

## Pre-Implementation Validation

Before starting implementation, verify:

1. **Completeness**: All required files exist and have content
2. **Clarity**: Technical approach is unambiguous
3. **Feasibility**: No obvious blockers or unknowns
4. **Testability**: Clear criteria for completion
5. **Alignment**: Matches project architecture and standards

## Post-Implementation Validation

After implementation, before archiving:

- [ ] All tasks completed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Code reviewed (if applicable)
- [ ] Specs synchronized with implementation

## Quality Gates by Phase

| Phase | Quality Gate | Criteria |
|-------|-------------|----------|
| Greenfield | Spec complete | spec.md + plan.md complete, research.md if needed |
| Legacy | Baseline refined | TODO count < 5 in baseline specs |
| Brownfield | Proposal ready | All 3 files (proposal.md, design.md, tasks.md) complete |
| Implementation | Tasks done | All checkboxes [x] in tasks.md |
| Archive | Verified | Tests pass, docs updated, specs synced |

## Common Quality Issues

### Issue: Vague Requirements
**Symptom**: "Improve performance" without metrics
**Fix**: Add specific, measurable criteria

### Issue: Missing Edge Cases
**Symptom**: Only happy path documented
**Fix**: Add error handling and boundary conditions

### Issue: Incomplete Task Breakdown
**Symptom**: Tasks like "Implement feature" (too large)
**Fix**: Break into 1-4 hour subtasks

### Issue: Unclear Dependencies
**Symptom**: Tasks can't be executed in order
**Fix**: Identify and document dependencies explicitly

### Issue: No Testing Strategy
**Symptom**: No test tasks or acceptance criteria
**Fix**: Add test tasks for each feature/change

## Quality Metrics

Track these metrics to improve spec quality:

- **Specification Completeness**: % of required fields filled
- **TODO Count**: Number of TODOs in specs (target: < 5)
- **Task Granularity**: Average task size (target: 1-4 hours)
- **Implementation Match**: % of implemented features matching specs
- **Revision Count**: Number of spec revisions needed

## Automation Tools

Use these scripts for automated quality checks:

```bash
# Validate specification
uv run scripts/validate-spec.py <spec-file>

# Check proposal status
bash scripts/check-proposal-status.sh <proposal-name>

# Detect phase and readiness
bash scripts/detect-phase.sh
bash scripts/detect-transition.sh
```
