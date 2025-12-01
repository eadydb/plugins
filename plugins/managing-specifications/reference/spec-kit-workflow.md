# spec-kit Workflow (0→1 Projects)

## Phase 1: Specification definition

**Trigger**: User describes product requirements

**Steps**:

1. Ask clarifying questions:
   - Core features and user stories
   - Technical constraints
   - Success criteria
   - Target users

2. Generate specification:

```bash
   cd specs/001-feature-name
   # Edit spec.md with detailed requirements
```

3. Include in spec.md:
   - User stories and acceptance criteria
   - Functional requirements
   - Non-functional requirements (performance, security)
   - Edge cases and error handling

## Phase 2: Technical planning

**Trigger**: Specification is approved

**Steps**:

1. Gather technical context:
   - Preferred technology stack
   - Infrastructure constraints
   - Integration requirements

2. Create implementation plan in plan.md:
   - Architecture overview
   - Technology choices with justification
   - API design
   - Database schema
   - Security considerations

3. Document key decisions

## Phase 3: Research supplement

**Trigger**: Complex technical areas need investigation

**Steps**:

1. Identify research topics from plan.md
2. Document findings in research.md:
   - Technology comparisons
   - Best practices
   - Performance benchmarks
   - Security patterns

## Phase 4: Task breakdown

**Trigger**: Plan is complete

**Steps**:

1. Break plan into implementable tasks
2. Each task should be:
   - Independently testable
   - 1-4 hours of work
   - Clear acceptance criteria

3. Order tasks by dependencies

## Validation checklist

Before proceeding to implementation:

- [ ] Spec.md covers all user requirements
- [ ] Plan.md has clear architecture
- [ ] Technology choices are justified
- [ ] Tasks are granular and testable
- [ ] Non-functional requirements addressed
