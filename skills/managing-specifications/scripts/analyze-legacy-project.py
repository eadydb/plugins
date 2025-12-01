#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# requires-python = ">=3.8"
# ///
"""
Analyze existing codebase and generate baseline SDD specifications
Usage: uv run scripts/analyze-legacy-project.py [--output-dir openspec/specs]
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
        description='Analyze legacy project and generate baseline SDD specs'
    )
    parser.add_argument(
        '--output-dir',
        default='openspec/specs',
        help='Output directory for generated specs (default: openspec/specs)'
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

    print("=== Analyzing Legacy Project ===\n")

    # Perform analysis
    print("1. Detecting project type...")
    project_types = detect_project_type(root_path)
    print(f"   Found: {', '.join(project_types) if project_types else 'Unknown'}")

    print("2. Analyzing directory structure...")
    structure = analyze_directory_structure(root_path)

    print("3. Finding API endpoints...")
    api_endpoints = find_api_endpoints(root_path)
    print(f"   Found {len(api_endpoints)} potential route files")

    print("4. Locating database schemas...")
    schemas = find_database_schemas(root_path)
    print(f"   Found {len(schemas)} schema files")

    print("5. Extracting dependencies...")
    dependencies = extract_dependencies(root_path, project_types)

    print("6. Scanning existing documentation...")
    existing_docs = scan_existing_docs(root_path)
    print(f"   Found {len(existing_docs)} documentation files")

    # Compile analysis
    analysis = {
        'project_types': project_types,
        'structure': structure,
        'api_endpoints': api_endpoints,
        'database_schemas': schemas,
        'dependencies': dependencies,
        'existing_docs': existing_docs
    }

    # Generate specifications
    print(f"\n7. Generating baseline specifications in {args.output_dir}...")
    generated = generate_baseline_specs(analysis, args.output_dir)

    print("\n=== Analysis Complete ===\n")
    print("Generated files:")
    for key, path in generated.items():
        print(f"  ✓ {path}")

    print("\n" + "="*50)
    print("NEXT STEPS:")
    print("="*50)
    print("1. Review and refine generated specifications")
    print("2. Add business context and requirements")
    print("3. Document features in openspec/specs/features/")
    print("4. Initialize OpenSpec: openspec init")
    print("5. Start using OpenSpec for new changes")
    print("\nSee reference/legacy-adoption.md for detailed guide")

    # Save analysis report
    report_path = Path(args.output_dir) / 'analysis-report.json'
    with open(report_path, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\nFull analysis saved to: {report_path}")

if __name__ == "__main__":
    main()
