#!/bin/bash
# Smart initialization: Detect project phase and call the correct framework command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Detect project phase
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" | head -n 1)

# 2. Show detected phase
echo "Detected project phase: $PHASE"

# 3. Ask user confirmation
read -p "Execute recommended initialization? (y/n) " confirm

if [ "$confirm" != "y" ]; then
    echo "Initialization cancelled"
    exit 0
fi

case $PHASE in
    "greenfield")
        # Check if uv/uvx is installed
        if ! command -v uvx &> /dev/null; then
            echo "uvx not detected, installing uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        else
            echo "✓ uvx installed"
        fi

        # Check if specify-cli is installed (use local version if available)
        if command -v specify &> /dev/null; then
            echo "✓ specify-cli installed, using local version"
            read -p "Enter project name: " project_name
            specify init "$project_name"
        else
            echo "Using uvx to run spec-kit temporarily..."
            read -p "Enter project name: " project_name
            uvx --from git+https://github.com/github/spec-kit.git specify init "$project_name"
        fi

        echo "✅ spec-kit initialization complete!"
        echo "Available commands: /specify, /plan, /tasks"
        ;;

    "legacy"|"brownfield")
        # Check if npm is installed
        if ! command -v npm &> /dev/null; then
            echo "❌ Error: Node.js and npm required"
            echo "Please install first: https://nodejs.org/"
            exit 1
        fi

        # Check if OpenSpec is installed
        if ! command -v openspec &> /dev/null; then
            echo "OpenSpec not detected, installing..."
            npm install -g @fission-ai/openspec@latest
        else
            echo "✓ OpenSpec installed"
        fi

        # Check if project is already initialized
        if [ ! -d "openspec" ]; then
            openspec init
            echo "✅ OpenSpec initialization complete!"
        else
            echo "✓ Project already initialized with OpenSpec"
        fi
        ;;

    *)
        echo "❌ Unknown project phase: $PHASE"
        exit 1
        ;;
esac

echo "✅ Initialization complete! Framework has automatically created commands and directory structure."
