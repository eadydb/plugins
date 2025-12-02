#!/bin/bash
# Detect project phase: greenfield (0→1), brownfield (1→N), or legacy (existing without SDD)
#
# Detection logic:
# - greenfield: No code + No specs → spec-kit (0→1)
# - legacy:     Has code + No specs → Analyze + OpenSpec (analyze first, generate baseline specs)
# - brownfield: Has code + Has specs → OpenSpec (feature iteration and change management)
# - spec-kit-only: Has spec-kit → Consider migrating to OpenSpec

set -e

HAS_SOURCE=false
HAS_SPEC_KIT=false
HAS_OPENSPEC=false

# Step 1: Check for source code indicators (fast check)
# Common project structure directories and configuration files
if [ -d "src" ] || [ -d "app" ] || [ -d "lib" ] || [ -d "pkg" ] || \
   [ -d "plugins" ] || [ -d "components" ] || [ -d "scripts" ] || \
   [ -f "package.json" ] || [ -f "setup.py" ] || [ -f "go.mod" ] || \
   [ -f "Cargo.toml" ] || [ -f "pom.xml" ] || [ -f "pyproject.toml" ]; then
    HAS_SOURCE=true
fi

# Step 2: Language-agnostic code detection using Git (fastest and most reliable)
# For git repositories: check if there are any non-documentation files
if [ "$HAS_SOURCE" = false ] && [ -d ".git" ]; then
    # Exclude documentation and config files, include everything else
    # This works for ANY programming language without hardcoding extensions
    TRACKED_FILES=$(git ls-files 2>/dev/null | \
        grep -v -E '\.(md|txt|json|yaml|yml|toml|xml|lock|svg|png|jpg|jpeg|gif|ico|pdf)$' | \
        grep -v -E '^(LICENSE|README|CHANGELOG|\.gitignore|\.gitattributes)' | \
        head -1)
    if [ -n "$TRACKED_FILES" ]; then
        HAS_SOURCE=true
    fi
fi

# Step 3: Fallback for non-git projects
# Simply check if there are any files that are NOT common documentation/config files
if [ "$HAS_SOURCE" = false ]; then
    # Count all files, excluding common non-code patterns
    NON_DOC_FILES=$(find . -type f \
        ! -path "*/node_modules/*" \
        ! -path "*/.git/*" \
        ! -path "*/venv/*" \
        ! -path "*/.venv/*" \
        ! -path "*/env/*" \
        ! -path "*/build/*" \
        ! -path "*/dist/*" \
        ! -path "*/target/*" \
        ! -path "*/__pycache__/*" \
        ! -path "*/.pytest_cache/*" \
        ! -path "*/vendor/*" \
        ! -name "*.md" \
        ! -name "*.txt" \
        ! -name "LICENSE*" \
        ! -name "README*" \
        ! -name "CHANGELOG*" \
        ! -name ".gitignore" \
        2>/dev/null | head -1)

    if [ -n "$NON_DOC_FILES" ]; then
        HAS_SOURCE=true
    fi
fi

# Check for existing spec frameworks
if [ -d "specs" ] && [ -f "specs/001-"*"/spec.md" ] 2>/dev/null; then
    HAS_SPEC_KIT=true
fi

if [ -d "openspec" ] && [ -d "openspec/specs" ]; then
    HAS_OPENSPEC=true
fi

# Decision logic
if [ "$HAS_SOURCE" = false ] && [ "$HAS_SPEC_KIT" = false ] && [ "$HAS_OPENSPEC" = false ]; then
    echo "greenfield"
    echo "Recommendation: Initialize with spec-kit for 0→1 development" >&2
elif [ "$HAS_SOURCE" = true ] && [ "$HAS_SPEC_KIT" = false ] && [ "$HAS_OPENSPEC" = false ]; then
    echo "legacy"
    echo "Recommendation: Analyze project and generate baseline specs, then use OpenSpec" >&2
elif [ "$HAS_SPEC_KIT" = true ] && [ "$HAS_OPENSPEC" = false ]; then
    echo "spec-kit-only"
    echo "Recommendation: Consider migrating to OpenSpec for ongoing iterations" >&2
else
    echo "brownfield"
    echo "Recommendation: Use OpenSpec for feature iterations" >&2
fi

exit 0
