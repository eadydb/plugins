#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# requires-python = ">=3.8"
# ///
"""
Analyze existing codebase and generate project context for AI assistance
Usage: uv run scripts/analyze-project-context.py [--output-file .claude/project-context.json]
"""

import sys
import os
import json
import argparse
from pathlib import Path
from collections import defaultdict

def detect_project_type(root_path):
    """Detect project type and tech stack"""
    markers = {
        'python': ['setup.py', 'requirements.txt', 'pyproject.toml'],
        'node': ['package.json', 'yarn.lock'],
        'go': ['go.mod', 'go.sum'],
        'rust': ['Cargo.toml'],
        'java': ['pom.xml', 'build.gradle'],
        'ruby': ['Gemfile'],
    }

    detected = []
    for lang, files in markers.items():
        if any((root_path / f).exists() for f in files):
            detected.append(lang)

    return detected

def analyze_directory_structure(root_path):
    """Analyze project structure"""
    structure = {
        'source_dirs': [],
        'test_dirs': [],
        'config_dirs': [],
        'doc_dirs': []
    }

    common_patterns = {
        'source_dirs': ['src', 'app', 'lib', 'pkg', 'internal'],
        'test_dirs': ['test', 'tests', '__tests__', 'spec'],
        'config_dirs': ['config', 'conf', 'settings'],
        'doc_dirs': ['docs', 'doc', 'documentation']
    }

    for category, patterns in common_patterns.items():
        for pattern in patterns:
            path = root_path / pattern
            if path.exists() and path.is_dir():
                structure[category].append(str(path.relative_to(root_path)))

    return structure

def find_api_endpoints(root_path):
    """Find API endpoints by scanning common patterns"""
    endpoints = []

    # Common route patterns to search for
    patterns = [
        r'@app\.route\(["\']([^"\']+)',           # Flask
        r'@router\.(get|post|put|delete)\(["\']([^"\']+)',  # FastAPI
        r'app\.(get|post|put|delete)\(["\']([^"\']+)',      # Express
        r'Route::(\w+)\(["\']([^"\']+)',          # Laravel
    ]

    # Scan relevant files
    for ext in ['.py', '.js', '.ts', '.php', '.rb']:
        for file_path in root_path.rglob(f'*{ext}'):
            if 'node_modules' in str(file_path) or '.git' in str(file_path):
                continue

            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                # Simple pattern matching (can be enhanced with AST parsing)
                if 'route' in content.lower() or 'endpoint' in content.lower():
                    endpoints.append({
                        'file': str(file_path.relative_to(root_path)),
                        'type': 'api_route'
                    })
            except Exception:
                continue

    return endpoints

def find_database_schemas(root_path):
    """Find database schema files"""
    schemas = []

    schema_patterns = [
        'migrations/*.sql',
        'schema.sql',
        'models.py',
        'schema.rb',
        'schema/*.sql'
    ]

    for pattern in schema_patterns:
        for file_path in root_path.rglob(pattern):
            schemas.append(str(file_path.relative_to(root_path)))

    return schemas

def extract_dependencies(root_path, project_types):
    """Extract project dependencies"""
    dependencies = {}

    dep_files = {
        'python': ['requirements.txt', 'Pipfile', 'pyproject.toml'],
        'node': ['package.json'],
        'go': ['go.mod'],
        'rust': ['Cargo.toml'],
        'java': ['pom.xml', 'build.gradle']
    }

    for lang in project_types:
        for dep_file in dep_files.get(lang, []):
            file_path = root_path / dep_file
            if file_path.exists():
                dependencies[dep_file] = f"Found at {file_path.relative_to(root_path)}"

    return dependencies

def scan_existing_docs(root_path):
    """Scan for existing documentation"""
    docs = []

    doc_files = ['README.md', 'ARCHITECTURE.md', 'API.md', 'CONTRIBUTING.md']

    for doc_file in doc_files:
        file_path = root_path / doc_file
        if file_path.exists():
            docs.append({
                'file': doc_file,
                'size': file_path.stat().st_size,
                'exists': True
            })

    # Scan docs directory
    docs_dir = root_path / 'docs'
    if docs_dir.exists():
        for doc in docs_dir.rglob('*.md'):
            docs.append({
                'file': str(doc.relative_to(root_path)),
                'size': doc.stat().st_size,
                'exists': True
            })

    return docs

def generate_baseline_specs(analysis, output_dir):
    """Generate baseline SDD specifications"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate project.md
    project_md = output_path / 'project.md'
    with open(project_md, 'w') as f:
        f.write(f"""# Project Overview

> Auto-generated baseline specification from legacy codebase analysis
> Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}

## Project Type

Detected technologies: {', '.join(analysis['project_types'])}

## Architecture

### Directory Structure

""")

        for category, dirs in analysis['structure'].items():
            if dirs:
                f.write(f"**{category.replace('_', ' ').title()}**: {', '.join(dirs)}\n")

        f.write(f"""

### Dependencies

""")
        for dep_file, location in analysis['dependencies'].items():
            f.write(f"- `{dep_file}`: {location}\n")

        f.write(f"""

## Existing Documentation

""")
        if analysis['existing_docs']:
            for doc in analysis['existing_docs']:
                f.write(f"- `{doc['file']}` ({doc['size']} bytes)\n")
        else:
            f.write("No existing documentation found.\n")

        f.write(f"""

## Next Steps

1. Review this baseline specification
2. Refine with business context and requirements
3. Document key features in `features/` directory
4. Add architecture decisions to `architecture.md`
5. Begin using OpenSpec for new changes

""")

    # Generate architecture.md
    arch_md = output_path / 'architecture.md'
    with open(arch_md, 'w') as f:
        f.write(f"""# System Architecture

> Auto-generated baseline - requires manual refinement

## Technology Stack

""")
        for tech in analysis['project_types']:
            f.write(f"- {tech.title()}\n")

        f.write(f"""

## Components

### Source Code Structure

""")
        for src_dir in analysis['structure']['source_dirs']:
            f.write(f"- `{src_dir}/`: [TODO: Describe component purpose]\n")

        if analysis['api_endpoints']:
            f.write(f"""

### API Endpoints

Found {len(analysis['api_endpoints'])} potential API route files:

""")
            for endpoint in analysis['api_endpoints'][:5]:  # Limit to first 5
                f.write(f"- `{endpoint['file']}`\n")

            if len(analysis['api_endpoints']) > 5:
                f.write(f"- ... and {len(analysis['api_endpoints']) - 5} more\n")

            f.write("\n**TODO**: Document actual endpoints, methods, and parameters\n")

        if analysis['database_schemas']:
            f.write(f"""

### Database

Schema files found:

""")
            for schema in analysis['database_schemas']:
                f.write(f"- `{schema}`\n")

            f.write("\n**TODO**: Document data model and relationships\n")

        f.write(f"""

## Design Patterns

**TODO**: Document architectural patterns used:
- [ ] MVC / MVVM / Clean Architecture
- [ ] Dependency Injection
- [ ] Repository Pattern
- [ ] Service Layer
- [ ] API Gateway
- [ ] Microservices / Monolith

## Infrastructure

**TODO**: Document deployment and infrastructure:
- [ ] Hosting platform
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Scalability approach

""")

    # Create features directory
    features_dir = output_path / 'features'
    features_dir.mkdir(exist_ok=True)

    readme = features_dir / 'README.md'
    with open(readme, 'w') as f:
        f.write("""# Features

Document each major feature of the system in separate markdown files.

## Template

Create a file for each feature (e.g., `user-authentication.md`):
````markdown
# [Feature Name]

## Purpose
What problem does this feature solve?

## User Stories
- As a [user type], I want to [action] so that [benefit]

## Functionality
Detailed description of what the feature does

## API/Interface
How users/systems interact with this feature

## Dependencies
What this feature depends on

## Technical Notes
Implementation details worth documenting
````

## Next Steps

1. Identify core features from codebase
2. Create a file for each feature
3. Collaborate with team to document accurately
""")

    return {
        'project_md': str(project_md),
        'architecture_md': str(arch_md),
        'features_dir': str(features_dir)
    }

def main():
    parser = argparse.ArgumentParser(
        description='Analyze project and generate context for AI assistance'
    )
    parser.add_argument(
        '--output-file',
        default='.claude/project-context.json',
        help='Output file for project context (default: .claude/project-context.json)'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='Project root directory (default: current directory)'
    )

    args = parser.parse_args()

    root_path = Path(args.project_root).resolve()

    if not root_path.exists():
        print(f"Error: Project root not found: {root_path}")
        sys.exit(1)

    # Check if OpenSpec is initialized
    if not (root_path / 'openspec').exists():
        print("⚠️  项目尚未初始化 OpenSpec")
        print("\n请先运行初始化命令：")
        print("  bash scripts/adopt-sdd.sh")
        print("\n或手动初始化：")
        print("  npm install -g @fission-ai/openspec@latest && openspec init")
        sys.exit(1)

    print("=== 分析项目上下文 ===\n")

    # Perform analysis
    print("1. 检测项目类型...")
    project_types = detect_project_type(root_path)
    print(f"   发现: {', '.join(project_types) if project_types else 'Unknown'}")

    print("2. 分析目录结构...")
    structure = analyze_directory_structure(root_path)

    print("3. 查找 API 模式...")
    api_endpoints = find_api_endpoints(root_path)
    print(f"   发现 {len(api_endpoints)} 个潜在的路由文件")

    print("4. 定位数据库模式...")
    schemas = find_database_schemas(root_path)
    print(f"   发现 {len(schemas)} 个模式文件")

    print("5. 提取依赖...")
    dependencies = extract_dependencies(root_path, project_types)

    print("6. 扫描现有文档...")
    existing_docs = scan_existing_docs(root_path)
    print(f"   发现 {len(existing_docs)} 个文档文件")

    # Compile analysis
    analysis = {
        'analysis_date': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'project_types': project_types,
        'structure': structure,
        'api_endpoints': api_endpoints,
        'database_schemas': schemas,
        'dependencies': dependencies,
        'existing_docs': existing_docs
    }

    # Save context file
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"\n✅ 项目上下文已保存到: {output_path}")

    print("\n" + "="*60)
    print("下一步：使用 AI 生成规范")
    print("="*60)
    print("\n在 Claude Code 中运行以下命令之一：")
    print("\n1️⃣  填充项目上下文（推荐）：")
    print('   "Please read openspec/project.md and help me fill it out')
    print('    with details about my project, tech stack, and conventions"')
    print("\n2️⃣  让 Claude 参考上下文创建规范：")
    print(f'   "Please read {output_path} for project analysis,')
    print('    then help me create comprehensive OpenSpec documentation"')
    print("\n3️⃣  创建功能提案：")
    print('   "I want to add [YOUR FEATURE]. Please create an')
    print('    OpenSpec change proposal for this feature"')
    print("\n📚 参考文档: reference/legacy-adoption.md")
    print("="*60)

if __name__ == "__main__":
    main()
