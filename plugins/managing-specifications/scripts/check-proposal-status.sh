#!/bin/bash
# Check status of a proposal in openspec/changes/
# Usage:
#   check-proposal-status.sh <proposal-name>  # Check specific proposal
#   check-proposal-status.sh                  # List all proposals with status

set -e

PROPOSAL_NAME="${1:-}"

# Function to check a single proposal's status
check_proposal() {
    local proposal_dir="$1"
    local proposal_name=$(basename "$proposal_dir")

    # Check file existence
    if [ ! -f "$proposal_dir/proposal.md" ] || \
       [ ! -f "$proposal_dir/design.md" ] || \
       [ ! -f "$proposal_dir/tasks.md" ]; then
        echo "draft"
        return
    fi

    # Check tasks.md content
    TOTAL_TASKS=$(grep -c "^- \[" "$proposal_dir/tasks.md" 2>/dev/null || echo "0")

    if [ "$TOTAL_TASKS" -eq 0 ]; then
        echo "draft"
        return
    fi

    COMPLETED_TASKS=$(grep -c "^- \[x\]" "$proposal_dir/tasks.md" 2>/dev/null || echo "0")
    UNCHECKED_TASKS=$(grep -c "^- \[ \]" "$proposal_dir/tasks.md" 2>/dev/null || echo "0")

    if [ "$COMPLETED_TASKS" -eq 0 ] && [ "$UNCHECKED_TASKS" -gt 0 ]; then
        echo "ready"
    elif [ "$COMPLETED_TASKS" -eq "$TOTAL_TASKS" ] && [ "$UNCHECKED_TASKS" -eq 0 ]; then
        echo "completed"
    elif [ "$UNCHECKED_TASKS" -gt 0 ]; then
        echo "implementing"
    else
        echo "draft"
    fi
}

if [ -z "$PROPOSAL_NAME" ]; then
    # Auto-detect: find all proposals and their status
    if [ ! -d "openspec/changes" ]; then
        echo "No openspec/changes directory found" >&2
        exit 1
    fi

    for change_dir in openspec/changes/*/; do
        if [ -d "$change_dir" ]; then
            name=$(basename "$change_dir")
            status=$(check_proposal "$change_dir")
            echo "$name:$status"
        fi
    done
else
    # Check specific proposal
    PROPOSAL_DIR="openspec/changes/$PROPOSAL_NAME"

    if [ ! -d "$PROPOSAL_DIR" ]; then
        echo "Proposal not found: $PROPOSAL_NAME" >&2
        exit 1
    fi

    check_proposal "$PROPOSAL_DIR"
fi

exit 0
