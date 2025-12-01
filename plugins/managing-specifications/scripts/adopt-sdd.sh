#!/bin/bash
# One-command SDD adoption: Detect project phase and guide through the complete process

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==================================="
echo "   SDD 框架采用向导"
echo "==================================="

# Step 1: Detect project phase
echo -e "\n📊 步骤 1/4: 检测项目阶段..."
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" | head -n 1)
echo "   检测结果: $PHASE"

# Step 2: Framework initialization
echo -e "\n⚙️  步骤 2/4: 初始化 SDD 框架..."
case $PHASE in
    "greenfield")
        # Check if uv/uvx is installed
        if ! command -v uvx &> /dev/null; then
            echo "   ⚠️  未检测到 uvx，正在安装 uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        else
            echo "   ✓ uvx 已安装"
        fi

        # Check if specify-cli is installed (use local version if available)
        if command -v specify &> /dev/null; then
            echo "   ✓ specify-cli 已安装，使用本地版本"
            read -p "   项目名称: " project_name
            specify init "$project_name"
        else
            echo "   使用 uvx 临时运行 spec-kit..."
            read -p "   项目名称: " project_name
            uvx --from git+https://github.com/github/spec-kit.git specify init "$project_name"
        fi

        echo "   ✅ spec-kit 初始化完成"
        echo "   可用命令: /specify, /plan, /tasks"
        ;;

    "legacy"|"brownfield")
        # Check if Node.js and npm are installed
        if ! command -v npm &> /dev/null; then
            echo "   ❌ 错误: 需要 Node.js 和 npm"
            echo "   请先安装 Node.js: https://nodejs.org/"
            exit 1
        fi

        # Check if OpenSpec is installed
        if ! command -v openspec &> /dev/null; then
            echo "   未检测到 OpenSpec，正在安装..."
            npm install -g @fission-ai/openspec@latest
        else
            echo "   ✓ OpenSpec 已安装"
        fi

        # Check if project is already initialized with OpenSpec
        if [ ! -d "openspec" ]; then
            echo "   正在初始化 OpenSpec..."
            openspec init
            echo "   ✅ OpenSpec 初始化完成"
        else
            echo "   ✓ OpenSpec 已初始化"
        fi

        # Step 3: Analyze project and generate baseline specs (legacy only)
        if [ "$PHASE" = "legacy" ]; then
            echo -e "\n🔍 步骤 3/4: 分析项目并生成基准规范..."

            # Check if uv is installed (for running Python scripts)
            if ! command -v uv &> /dev/null; then
                echo "   ⚠️  未检测到 uv，正在安装..."
                curl -LsSf https://astral.sh/uv/install.sh | sh
                export PATH="$HOME/.cargo/bin:$PATH"
            fi

            # Run analysis with --generate-specs flag
            uv run "$SCRIPT_DIR/analyze-project-context.py" --generate-specs

            echo ""
            echo "   ✅ 已生成基准规范文件："
            echo "      - openspec/specs/project.md"
            echo "      - openspec/specs/architecture.md"
            echo "      - openspec/specs/features/"
            echo ""
            echo "   ✅ 项目上下文已保存: .claude/project-context.json"
        fi

        # Step 4: Guide for completing setup in Claude Code
        echo -e "\n🤖 步骤 4/4: 在 Claude Code 中完成设置"
        echo ""
        if [ "$PHASE" = "legacy" ]; then
            echo "   OpenSpec 已初始化并生成基准规范！"
            echo ""
            echo "   📝 基准规范文件已包含从代码分析得出的基础信息"
            echo "   🔧 请在 Claude Code 中完善标记为 [TODO] 的部分"
            echo ""
            echo "   建议在 Claude Code 中依次运行以下命令："
            echo ""
            echo "   1️⃣  完善项目规范："
            echo "   \"Please read openspec/specs/project.md and help me"
            echo "    complete all [TODO] sections with proper details\""
            echo ""
            echo "   2️⃣  记录核心功能："
            echo "   \"Help me identify and document the core features"
            echo "    in openspec/specs/features/\""
            echo ""
            echo "   3️⃣  创建第一个变更提案："
            echo "   \"I want to add [YOUR FEATURE]. Please create an"
            echo "    OpenSpec change proposal for this feature\""
        else
            echo "   OpenSpec 已初始化！请在 Claude Code 中依次运行以下命令："
            echo ""
            echo "   1️⃣  填充项目上下文："
            echo "   \"Please read openspec/specs/project.md and help me fill it out"
            echo "    with details about my project, tech stack, and conventions\""
            echo ""
            echo "   2️⃣  创建第一个变更提案（可选）："
            echo "   \"I want to add [YOUR FEATURE HERE]. Please create an"
            echo "    OpenSpec change proposal for this feature\""
            echo ""
            echo "   3️⃣  学习 OpenSpec 工作流："
            echo "   \"Please explain the OpenSpec workflow"
            echo "    and how I should work with you on this project\""
        fi
        ;;

    *)
        echo "   ❌ 未知的项目阶段: $PHASE"
        exit 1
        ;;
esac

echo -e "\n✨ SDD 框架采用完成！"
echo "   📚 参考文档: reference/legacy-adoption.md"
