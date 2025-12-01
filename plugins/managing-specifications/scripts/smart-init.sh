#!/bin/bash
# Smart initialization: Detect project phase and call the correct framework command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Detect project phase
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" | head -n 1)

# 2. Show detected phase
echo "检测到项目阶段: $PHASE"

# 3. Ask user confirmation
read -p "是否执行推荐的初始化? (y/n) " confirm

if [ "$confirm" != "y" ]; then
    echo "已取消初始化"
    exit 0
fi

case $PHASE in
    "greenfield")
        # Check if uv/uvx is installed
        if ! command -v uvx &> /dev/null; then
            echo "未检测到 uvx，正在安装 uv..."
            curl -LsSf https://astral.sh/uv/install.sh | sh
            export PATH="$HOME/.cargo/bin:$PATH"
        else
            echo "✓ uvx 已安装"
        fi

        # Check if specify-cli is installed (use local version if available)
        if command -v specify &> /dev/null; then
            echo "✓ specify-cli 已安装，使用本地版本"
            read -p "请输入项目名称: " project_name
            specify init "$project_name"
        else
            echo "使用 uvx 临时运行 spec-kit..."
            read -p "请输入项目名称: " project_name
            uvx --from git+https://github.com/github/spec-kit.git specify init "$project_name"
        fi

        echo "✅ spec-kit 初始化完成！"
        echo "可用命令: /specify, /plan, /tasks"
        ;;

    "legacy"|"brownfield")
        # Check if npm is installed
        if ! command -v npm &> /dev/null; then
            echo "❌ 错误: 需要 Node.js 和 npm"
            echo "请先安装: https://nodejs.org/"
            exit 1
        fi

        # Check if OpenSpec is installed
        if ! command -v openspec &> /dev/null; then
            echo "未检测到 OpenSpec，正在安装..."
            npm install -g @fission-ai/openspec@latest
        else
            echo "✓ OpenSpec 已安装"
        fi

        # Check if project is already initialized
        if [ ! -d "openspec" ]; then
            openspec init
            echo "✅ OpenSpec 初始化完成！"
        else
            echo "✓ 项目已初始化 OpenSpec"
        fi
        ;;

    *)
        echo "❌ 未知的项目阶段: $PHASE"
        exit 1
        ;;
esac

echo "✅ 初始化完成！框架已自动创建 commands 和目录结构。"
