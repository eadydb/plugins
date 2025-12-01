#!/bin/bash
# 检测项目是否应该进行阶段转换
# 返回转换状态和建议

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 获取当前项目阶段
PHASE=$(bash "$SCRIPT_DIR/detect-phase.sh" 2>/dev/null | head -n 1)

case $PHASE in
    "greenfield")
        # 检查是否应该迁移到 brownfield
        # 条件：有 spec-kit 规范 + 有源代码实现
        if [ -d "specs" ] && ([ -d "src" ] || [ -d "app" ] || [ -d "lib" ]); then
            echo "ready-for-migration"
            echo "✨ 检测到初始开发已完成" >&2
            echo "建议: 迁移到 OpenSpec 以进行迭代开发" >&2
            echo "运行: bash scripts/migrate-to-openspec.sh" >&2
            exit 0
        else
            echo "stay-greenfield"
            echo "当前阶段: Greenfield (0→1 开发中)" >&2
            echo "继续使用 spec-kit 完成初始开发" >&2
            exit 0
        fi
        ;;

    "legacy")
        # 检查是否已完成基准规范生成
        if [ -d "openspec/specs" ] && [ -f "openspec/specs/project.md" ]; then
            # 进一步检查规范是否已被完善（检查TODO数量）
            TODO_COUNT=$(grep -r "\[TODO" openspec/specs/ 2>/dev/null | wc -l || echo "0")

            if [ "$TODO_COUNT" -lt 5 ]; then
                echo "ready-for-iteration"
                echo "✅ 基准规范已完善" >&2
                echo "建议: 可以开始使用 OpenSpec 创建功能提案" >&2
                echo "示例: openspec proposal add-new-feature" >&2
            else
                echo "refining-baseline"
                echo "📝 基准规范已生成，但还有 $TODO_COUNT 个 TODO 待完善" >&2
                echo "建议: 在 Claude Code 中完善规范文件" >&2
            fi
            exit 0
        else
            echo "needs-baseline"
            echo "⚠️  尚未生成基准规范" >&2
            echo "建议: 运行 bash scripts/adopt-sdd.sh" >&2
            exit 0
        fi
        ;;

    "spec-kit-only")
        echo "needs-migration"
        echo "🔄 检测到 spec-kit 项目" >&2
        echo "建议: 迁移到 OpenSpec 以支持持续迭代" >&2
        echo "运行: bash scripts/migrate-to-openspec.sh" >&2
        exit 0
        ;;

    "brownfield")
        # 检查 OpenSpec 使用情况
        if [ -d "openspec/changes" ]; then
            ACTIVE_CHANGES=$(find openspec/changes -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l || echo "0")
            if [ "$ACTIVE_CHANGES" -gt 0 ]; then
                echo "active-iteration"
                echo "✅ 项目正在迭代中 ($ACTIVE_CHANGES 个活跃变更)" >&2
            else
                echo "stable-iteration"
                echo "📋 项目处于稳定状态，可以创建新的变更提案" >&2
            fi
        else
            echo "active-iteration"
            echo "✅ 项目使用 OpenSpec 管理" >&2
        fi
        exit 0
        ;;

    *)
        echo "unknown"
        echo "❌ 无法识别项目阶段: $PHASE" >&2
        exit 1
        ;;
esac
