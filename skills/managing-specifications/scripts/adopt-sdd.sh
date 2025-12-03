#!/bin/bash
# One-command SDD adoption: Detect project phase and guide through the complete process

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==================================="
echo "   SDD Framework Adoption Wizard"
echo "==================================="

# Step 1: Detect project phase
echo -e "\n📊 Step 1/4: Detecting project phase..."
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" | head -n 1)
echo "   Detection result: $PHASE"

# Step 2: Framework initialization
echo -e "\n⚙️  Step 2/4: Initializing SDD framework..."
case $PHASE in
    "greenfield")
        # Check if uv/uvx is installed
        if ! command -v uvx &> /dev/null; then
            echo "   ⚠️  uvx not detected, installing uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        else
            echo "   ✓ uvx installed"
        fi

        # Check if specify-cli is installed (use local version if available)
        if command -v specify &> /dev/null; then
            echo "   ✓ specify-cli installed, using local version"
            read -p "   Project name: " project_name
            specify init "$project_name"
        else
            echo "   Using uvx to run spec-kit temporarily..."
            read -p "   Project name: " project_name
            uvx --from git+https://github.com/github/spec-kit.git specify init "$project_name"
        fi

        echo "   ✅ spec-kit initialization complete"
        echo "   Available commands: /specify, /plan, /tasks"
        ;;

    "legacy"|"brownfield")
        # Check if Node.js and npm are installed
        if ! command -v npm &> /dev/null; then
            echo "   ❌ Error: Node.js and npm required"
            echo "   Please install Node.js first: https://nodejs.org/"
            exit 1
        fi

        # Check if OpenSpec is installed
        if ! command -v openspec &> /dev/null; then
            echo "   OpenSpec not detected, installing..."
            npm install -g @fission-ai/openspec@latest
        else
            echo "   ✓ OpenSpec installed"
        fi

        # Check if project is already initialized with OpenSpec
        if [ ! -d "openspec" ]; then
            echo "   Initializing OpenSpec..."
            openspec init
            echo "   ✅ OpenSpec initialization complete"
        else
            echo "   ✓ OpenSpec already initialized"
        fi

        # Step 3: Analyze project and generate baseline specs (legacy only)
        if [ "$PHASE" = "legacy" ]; then
            echo -e "\n🔍 Step 3/4: Analyzing project and generating baseline specs..."

            # Check if uv is installed (for running Python scripts)
            if ! command -v uv &> /dev/null; then
                echo "   ⚠️  uv not detected, installing..."
                curl -LsSf https://astral.sh/uv/install.sh | sh
                export PATH="$HOME/.cargo/bin:$PATH"
            fi

            # Run analysis with --generate-specs flag
            uv run "$SCRIPT_DIR/analyze-project-context.py" --generate-specs

            echo ""
            echo "   ✅ Generated baseline spec files:"
            echo "      - openspec/specs/project.md"
            echo "      - openspec/specs/architecture.md"
            echo "      - openspec/specs/features/"
            echo ""
            echo "   ✅ Project context saved: .claude/project-context.json"
        fi

        # Step 4: Guide for completing setup in Claude Code
        echo -e "\n🤖 Step 4/4: Complete setup in Claude Code"
        echo ""
        if [ "$PHASE" = "legacy" ]; then
            echo "   OpenSpec initialized and baseline specs generated!"
            echo ""
            echo "   📝 Baseline spec files contain basic information from code analysis"
            echo "   🔧 Please refine the sections marked with [TODO] in Claude Code"
            echo ""
            echo "   Recommended commands to run in Claude Code:"
            echo ""
            echo "   1️⃣  Refine project specs:"
            echo "   \"Please read openspec/specs/project.md and help me"
            echo "    complete all [TODO] sections with proper details\""
            echo ""
            echo "   2️⃣  Document core features:"
            echo "   \"Help me identify and document the core features"
            echo "    in openspec/specs/features/\""
            echo ""
            echo "   3️⃣  Create first change proposal:"
            echo "   \"I want to add [YOUR FEATURE]. Please create an"
            echo "    OpenSpec change proposal for this feature\""
        else
            echo "   OpenSpec initialized! Run these commands in Claude Code:"
            echo ""
            echo "   1️⃣  Fill in project context:"
            echo "   \"Please read openspec/specs/project.md and help me fill it out"
            echo "    with details about my project, tech stack, and conventions\""
            echo ""
            echo "   2️⃣  Create first change proposal (optional):"
            echo "   \"I want to add [YOUR FEATURE HERE]. Please create an"
            echo "    OpenSpec change proposal for this feature\""
            echo ""
            echo "   3️⃣  Learn OpenSpec workflow:"
            echo "   \"Please explain the OpenSpec workflow"
            echo "    and how I should work with you on this project\""
        fi
        ;;

    *)
        echo "   ❌ Unknown project phase: $PHASE"
        exit 1
        ;;
esac

echo -e "\n✨ SDD framework adoption complete!"
echo "   📚 Reference documentation: reference/legacy-adoption.md"
