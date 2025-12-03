# Implementation Execution Pattern (Critical - No Interruption)

This document defines the automated behavior for implementing confirmed OpenSpec proposals without interruption.

## When to Apply This Pattern

**Trigger Conditions**:
- User explicitly requests implementation with keywords (see "Keywords" section below)
- Proposal status is "ready" (all files complete, tasks unchecked) or "implementing" (some tasks checked)
- Project is in Brownfield phase (has code + has specs)

## IMPORTANT RULES

When proposal status is "ready" or "implementing" AND user explicitly requests implementation:

**Do NOT**:
- ❌ Create TodoWrite task list (tasks already exist in tasks.md)
- ❌ Ask "Should I start?" (user already confirmed by saying "实施")
- ❌ Enter plan mode
- ❌ Ask for additional confirmation

**DO**:
- ✅ Treat user's "实施" command as explicit authorization to proceed
- ✅ Read tasks.md directly
- ✅ Execute tasks sequentially without interruption
- ✅ Mark tasks complete in real-time

## Execution Steps

### 1. Read the Task List

```bash
# Read tasks.md to understand what needs to be done
cat openspec/changes/<proposal-name>/tasks.md
```

### 2. Execute Tasks Sequentially

For each unchecked task in tasks.md (lines matching `- [ ] ...`):

a. Read task description and understand requirements
b. Implement the task (write code, modify files, run commands, etc.)
c. Verify task is complete
d. Mark task complete by editing tasks.md: change `- [ ]` to `- [x]`
e. Continue to next unchecked task **without asking for confirmation**

### 3. During Execution

- Update tasks.md in real-time as tasks complete
- Add implementation notes or findings as comments if needed
- Keep user informed of progress (e.g., "Completed task 2/5: Update API endpoint")
- Continue without interruption until all tasks are checked

### 4. After All Tasks Complete

- Run tests if test tasks were in the list
- Summarize what was implemented
- Suggest archiving: "All tasks complete! Run 'openspec archive <proposal-name>' to merge changes to specs?"

## Keywords

### Implementation Intent

Triggers the Implementation Detection Flow:

**Chinese**:
- 实施
- 开始实施
- 实施这个提案
- 实施提案
- 执行
- 开始执行
- 继续实施

**English**:
- implement
- start implementation
- implement this proposal
- implement the proposal
- execute
- start executing
- resume implementation

### New Feature Intent

Triggers the Proposal Creation Flow:

**Chinese**:
- 新功能
- 添加功能
- 创建提案
- 新建提案

**English**:
- new feature
- add feature
- create proposal
- new proposal

## Implementation Detection Flow

When implementation keywords are detected:

### Step 1: Run Status Detection

```bash
bash scripts/check-proposal-status.sh
```

### Step 2: Find Ready Proposals

Identify proposals in "ready" or "implementing" state.

### Step 3: Determine Which Proposal

- **If user mentions proposal name**: use that specific proposal
- **If only one ready/implementing proposal exists**: use that one
- **If multiple ready proposals exist**: show list and ask user to choose

### Step 4: Check Status and Act

| Status | Definition | Action |
|--------|-----------|--------|
| **ready** | All files complete, no tasks started | Start from first task |
| **implementing** | Some tasks done | Resume from first unchecked task |
| **completed** | All tasks done | Suggest archiving instead |
| **draft** | Files incomplete | Ask user to complete proposal files first |

### Step 5: Execute Implementation

Follow the Execution Steps defined above.

## Example: Correct Flow

```
User: "实施 add-auth"

→ Claude: bash scripts/check-proposal-status.sh add-auth
→ Status: ready
→ Claude: cat openspec/changes/add-auth/tasks.md
→ Claude: "Starting implementation of add-auth proposal..."
→ Claude: [Implements task 1] [Marks task 1 as [x]]
→ Claude: [Implements task 2] [Marks task 2 as [x]]
→ Claude: [Implements task 3] [Marks task 3 as [x]]
→ Claude: "All tasks complete! Would you like to archive this proposal?"
```

**Key Characteristics**:
- ✅ No interruption
- ✅ No TodoWrite created
- ✅ No confirmation asked
- ✅ Tasks marked in tasks.md directly
- ✅ Continuous execution

## Anti-Pattern: What NOT to Do

```
User: "实施这个提案"

→ Claude: "Let me create a task list first..."        ❌ WRONG - tasks already exist
→ Claude: [Creates TodoWrite]                          ❌ WRONG - use tasks.md
→ Claude: "Should I start implementing?"               ❌ WRONG - user already confirmed
```

**Why This is Wrong**:
- Creates duplicate task tracking (TodoWrite vs tasks.md)
- Interrupts the flow with unnecessary confirmation
- Wastes user's time
- Violates the principle: "user's 实施 command IS the confirmation"

## Edge Cases

### Empty tasks.md

**Detection**: `grep -c "^- \[" tasks.md` returns 0

**Action**: Report as "draft" state. Message: "tasks.md is empty. Please add implementation tasks in format: `- [ ] Task description`"

### Multiple Ready Proposals

**Detection**: Multiple proposals with state "ready"

**Action**: List all ready proposals, ask: "Which proposal do you want to implement? (1) add-auth (2) update-api"

### No Proposal Name Given

**User input**: Just "实施" without proposal name

**Action**:
1. Run `check-proposal-status.sh` without args
2. Show all ready proposals
3. Ask user to choose

### Partial Implementation (Resume)

**Detection**: Proposal status is "implementing" (some tasks [x], some [ ])

**Action**: Resume from first unchecked task. Do NOT restart from task 1.

**Example**:
```
Tasks in tasks.md:
- [x] Task 1 (already done)
- [x] Task 2 (already done)
- [ ] Task 3 (resume here)
- [ ] Task 4
- [ ] Task 5

→ Claude starts from Task 3, continues to Task 5
```

## Status Verification

Use `check-proposal-status.sh` to verify proposal state:

```bash
# Check specific proposal
bash scripts/check-proposal-status.sh <proposal-name>

# List all proposals with status
bash scripts/check-proposal-status.sh
```

**Possible outputs**:
- `draft`: Proposal files incomplete or tasks.md empty
- `ready`: All files exist, all tasks unchecked
- `implementing`: Mix of checked and unchecked tasks
- `completed`: All tasks checked

## Integration with Brownfield Workflow

This pattern is part of the Brownfield scenario workflow. See `openspec-workflow.md` Phase 4 for the complete context.

**Related Files**:
- `SKILL.md`: Brownfield Scenario section
- `openspec-workflow.md`: Phase 4 Implementation
- `scripts/check-proposal-status.sh`: Status detection script
- `scripts/detect-transition.sh`: Phase transition detection

## Success Criteria

Implementation is successful when:

1. ✅ User says "实施" → Claude executes without asking "Should I start?"
2. ✅ No TodoWrite list created → tasks.md is used directly
3. ✅ Tasks marked [x] in tasks.md → not in separate list
4. ✅ Continuous execution → no interruptions between tasks
5. ✅ Status detection accurate → correct state identification
6. ✅ Resume works correctly → partial implementations continue from last unchecked task
