#!/bin/bash
# Migrate from spec-kit to OpenSpec
# Usage: bash migrate-to-openspec.sh [--dry-run]

set -e

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE - No changes will be made ==="
    echo ""
fi

echo "=== Migration from spec-kit to OpenSpec ==="
echo ""

# Verify spec-kit exists
if [ ! -d "specs" ]; then
    echo "Error: No specs/ directory found. Not a spec-kit project?"
    exit 1
fi

# Check for existing OpenSpec
if [ -d "openspec" ]; then
    echo "Warning: openspec/ directory already exists."
    echo "This project may have already been migrated."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Create archive
echo "1. Archiving spec-kit files..."
if [ "$DRY_RUN" = false ]; then
    mkdir -p docs/initial-specs
    cp -r specs/* docs/initial-specs/
    echo "   ✓ Archived to docs/initial-specs/"
else
    echo "   [DRY RUN] Would archive specs/* to docs/initial-specs/"
fi

# Step 2: Check if OpenSpec is installed
echo ""
echo "2. Checking OpenSpec installation..."
if ! command -v openspec &> /dev/null; then
    echo "   OpenSpec not found. Installing..."
    if [ "$DRY_RUN" = false ]; then
        npm install -g @fission-ai/openspec@latest
        echo "   ✓ OpenSpec installed"
    else
        echo "   [DRY RUN] Would run: npm install -g @fission-ai/openspec@latest"
    fi
else
    echo "   ✓ OpenSpec already installed: $(openspec --version 2>/dev/null || echo 'version unknown')"
fi

# Step 3: Initialize OpenSpec
echo ""
echo "3. Initializing OpenSpec..."
if [ "$DRY_RUN" = false ]; then
    openspec init
    echo "   ✓ OpenSpec initialized"
else
    echo "   [DRY RUN] Would run: openspec init"
fi

# Step 4: Create migration notes
echo ""
echo "4. Creating migration guide..."
if [ "$DRY_RUN" = false ]; then
    cat > docs/migration-notes.md << 'EOF'
# Migration Notes: spec-kit → OpenSpec

## Migration Date
<!-- Auto-generated -->

## Completed
- [x] Archived spec-kit files to docs/initial-specs/
- [x] Initialized OpenSpec structure

## TODO
- [ ] Convert specs/001-*/spec.md to openspec/specs/project.md
- [ ] Convert specs/001-*/plan.md to openspec/specs/architecture.md
- [ ] Update .claude/CLAUDE.md with OpenSpec workflow
- [ ] Create first test change proposal
- [ ] Train team on OpenSpec workflow

## Conversion Guide

### From spec.md → project.md
- Extract product vision
- List core features
- Document key decisions
- Remove implementation details

### From plan.md → architecture.md
- System architecture
- Technology stack
- Design patterns
- Integration points

### Keep research.md as docs/technical-decisions.md
- Reference for future decisions
- Historical context

## Reference
See docs/initial-specs/ for original spec-kit documentation.
EOF
    echo "   ✓ Created docs/migration-notes.md"
else
    echo "   [DRY RUN] Would create docs/migration-notes.md"
fi

echo ""
echo "=== Migration complete! ==="
echo ""
echo "Next steps:"
echo "1. Review docs/migration-notes.md"
echo "2. Convert key specs to OpenSpec format"
echo "3. Run: openspec proposal test-feature (to verify setup)"
echo "4. Update team documentation"
echo ""
echo "See reference/migration-guide.md for detailed instructions."
