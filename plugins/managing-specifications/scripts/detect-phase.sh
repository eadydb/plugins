#!/bin/bash
# Detect project phase: greenfield (0→1), brownfield (1→N), or legacy (existing without SDD)

set -e

HAS_SOURCE=false
HAS_SPEC_KIT=false
HAS_OPENSPEC=false

# Check for source code in common locations
if [ -d "src" ] || [ -d "app" ] || [ -d "lib" ] || [ -d "pkg" ] || \
   [ -f "package.json" ] || [ -f "setup.py" ] || [ -f "go.mod" ] || \
   [ -f "Cargo.toml" ] || [ -f "pom.xml" ]; then
    HAS_SOURCE=true
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
