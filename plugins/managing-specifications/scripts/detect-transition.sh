#!/bin/bash
# Detect if project should transition to a different phase
# Returns transition status and recommendations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get current project phase
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" 2>/dev/null | head -n 1)

case $PHASE in
    "greenfield")
        # Check if should migrate to brownfield
        # Conditions: has spec-kit specs + has source code implementation
        if [ -d "specs" ] && ([ -d "src" ] || [ -d "app" ] || [ -d "lib" ]); then
            echo "ready-for-migration"
            echo "✨ Detected initial development is complete" >&2
            echo "Recommendation: Migrate to OpenSpec for iterative development" >&2
            echo "Run: bash scripts/migrate-to-openspec.sh" >&2
            exit 0
        else
            echo "stay-greenfield"
            echo "Current phase: Greenfield (0→1 development in progress)" >&2
            echo "Continue using spec-kit to complete initial development" >&2
            exit 0
        fi
        ;;

    "legacy")
        # Check if baseline specs have been generated
        if [ -d "openspec/specs" ] && [ -f "openspec/specs/project.md" ]; then
            # Further check if specs have been refined (check TODO count)
            TODO_COUNT=$(grep -r "\[TODO" openspec/specs/ 2>/dev/null | wc -l || echo "0")

            if [ "$TODO_COUNT" -lt 5 ]; then
                echo "ready-for-iteration"
                echo "✅ Baseline specs have been refined" >&2
                echo "Recommendation: Can now start using OpenSpec to create feature proposals" >&2
                echo "Example: openspec proposal add-new-feature" >&2
            else
                echo "refining-baseline"
                echo "📝 Baseline specs generated, but $TODO_COUNT TODOs remain to be refined" >&2
                echo "Recommendation: Refine spec files in Claude Code" >&2
            fi
            exit 0
        else
            echo "needs-baseline"
            echo "⚠️  Baseline specs not yet generated" >&2
            echo "Recommendation: Run bash scripts/adopt-sdd.sh" >&2
            exit 0
        fi
        ;;

    "spec-kit-only")
        echo "needs-migration"
        echo "🔄 Detected spec-kit project" >&2
        echo "Recommendation: Migrate to OpenSpec to support continuous iteration" >&2
        echo "Run: bash scripts/migrate-to-openspec.sh" >&2
        exit 0
        ;;

    "brownfield")
        # Check OpenSpec usage status
        if [ -d "openspec/changes" ]; then
            ACTIVE_CHANGES=$(find openspec/changes -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l || echo "0")
            if [ "$ACTIVE_CHANGES" -gt 0 ]; then
                echo "active-iteration"
                echo "✅ Project is actively iterating ($ACTIVE_CHANGES active changes)" >&2
            else
                echo "stable-iteration"
                echo "📋 Project is in stable state, can create new change proposals" >&2
            fi
        else
            echo "active-iteration"
            echo "✅ Project managed with OpenSpec" >&2
        fi
        exit 0
        ;;

    *)
        echo "unknown"
        echo "❌ Unable to recognize project phase: $PHASE" >&2
        exit 1
        ;;
esac
