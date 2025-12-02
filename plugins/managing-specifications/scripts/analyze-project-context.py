#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# requires-python = ">=3.8"
# ///
"""
Analyze existing codebase and generate project context for AI assistance
Usage: uv run scripts/analyze-project-context.py [--output-file .claude/project-context.json] [--generate-specs]
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

def load_template(template_name):
    """Load a template file"""
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / 'templates' / template_name

    if not template_path.exists():
        # Fallback to simple template if file not found
        return None

    with open(template_path, 'r') as f:
        return f.read()

def extract_readme_content(root_path):
    """Extract content from README.md"""
    readme_path = root_path / 'README.md'
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8')
            # Extract first paragraph or first 500 characters
            lines = content.split('\n')
            description_lines = []
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    description_lines.append(line)
                    if len('\n'.join(description_lines)) > 500:
                        break
            return '\n'.join(description_lines[:3]) if description_lines else "No description available"
        except Exception:
            pass
    return "No description available"

def infer_architecture_pattern(structure):
    """Infer architecture pattern from directory structure"""
    source_dirs = structure.get('source_dirs', [])

    patterns = []
    if any('model' in d.lower() for d in source_dirs):
        patterns.append("Likely uses MVC or layered architecture")
    if any('controller' in d.lower() for d in source_dirs):
        patterns.append("Detected Controller layer")
    if any('service' in d.lower() for d in source_dirs):
        patterns.append("Detected Service layer")
    if any('repository' in d.lower() or 'dao' in d.lower() for d in source_dirs):
        patterns.append("Detected Repository/DAO layer")

    if patterns:
        return '\n'.join(f"- {p}" for p in patterns)
    return "- [To be analyzed] Please add architecture patterns based on code structure"

def format_tech_stack(project_types, dependencies):
    """Format detected technologies"""
    lines = []
    for tech in project_types:
        lines.append(f"- **{tech.title()}**")

    # Add framework hints from dependencies
    frameworks = {
        'package.json': 'Node.js ecosystem',
        'requirements.txt': 'Python packages',
        'go.mod': 'Go modules',
        'Cargo.toml': 'Rust crates'
    }

    for dep_file in dependencies.keys():
        if dep_file in frameworks:
            lines.append(f"  - {frameworks[dep_file]}: `{dep_file}`")

    return '\n'.join(lines) if lines else "- [To be detected] Please add tech stack information"

def format_directory_tree(structure):
    """Format directory structure as a tree"""
    lines = []
    for category, dirs in structure.items():
        if dirs:
            category_name = category.replace('_', ' ').title()
            lines.append(f"{category_name}:")
            for d in dirs:
                lines.append(f"  {d}/")
    return '\n'.join(lines) if lines else "[To be scanned] Project directory structure"

def format_api_endpoints(endpoints):
    """Format API endpoints"""
    if not endpoints:
        return "[Not detected] Please add API endpoint information"

    lines = ["**Detected route files**:"]
    for endpoint in endpoints[:10]:  # Limit to first 10
        lines.append(f"- `{endpoint['file']}`")

    if len(endpoints) > 10:
        lines.append(f"- ... and {len(endpoints) - 10} more files")

    return '\n'.join(lines)

def format_database_schemas(schemas):
    """Format database schema files"""
    if not schemas:
        return "[Not detected] Please add database design information"

    lines = ["**Detected Schema files**:"]
    for schema in schemas[:5]:
        lines.append(f"- `{schema}`")

    if len(schemas) > 5:
        lines.append(f"- ... and {len(schemas) - 5} more files")

    return '\n'.join(lines)

def format_system_components(structure):
    """Format system components"""
    source_dirs = structure.get('source_dirs', [])
    if not source_dirs:
        return "[To be identified] Please add system component descriptions"

    lines = []
    for src_dir in source_dirs:
        lines.append(f"- **`{src_dir}/`**: [TODO] Add component responsibility description")

    return '\n'.join(lines)

def generate_baseline_specs(analysis, output_dir, root_path):
    """Generate baseline SDD specifications using templates"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract project name from directory
    project_name = root_path.name.replace('-', ' ').replace('_', ' ').title()
    project_description = extract_readme_content(root_path)

    # Prepare template variables
    template_vars = {
        'PROJECT_NAME': project_name,
        'PROJECT_DESCRIPTION': project_description,
        'DETECTED_TECHNOLOGIES': format_tech_stack(analysis['project_types'], analysis['dependencies']),
        'PROJECT_STRUCTURE': format_directory_tree(analysis['structure']),
        'API_ENDPOINTS': format_api_endpoints(analysis['api_endpoints']),
        'DATABASE_SCHEMA': format_database_schemas(analysis['database_schemas']),
        'ARCHITECTURE_OVERVIEW': infer_architecture_pattern(analysis['structure']),
        'SYSTEM_COMPONENTS': format_system_components(analysis['structure']),
        'TECH_STACK_DETAILS': format_tech_stack(analysis['project_types'], analysis['dependencies']),
        'DATA_STORAGE': format_database_schemas(analysis['database_schemas']),
        'SECURITY_CONSIDERATIONS': "- [TODO] Add authentication and authorization mechanisms\n- [TODO] Add data encryption strategies\n- [TODO] Add security audit plans"
    }

    # Generate project.md from template
    project_template = load_template('project.md.template')
    if project_template:
        project_content = project_template
        for key, value in template_vars.items():
            project_content = project_content.replace('{' + key + '}', value)

        project_md = output_path / 'project.md'
        with open(project_md, 'w') as f:
            f.write(project_content)
    else:
        # Fallback to simple generation
        project_md = output_path / 'project.md'
        with open(project_md, 'w') as f:
            f.write(f"""# {project_name}

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

    # Generate architecture.md from template
    arch_template = load_template('architecture.md.template')
    if arch_template:
        arch_content = arch_template
        for key, value in template_vars.items():
            arch_content = arch_content.replace('{' + key + '}', value)

        arch_md = output_path / 'architecture.md'
        with open(arch_md, 'w') as f:
            f.write(arch_content)
    else:
        # Fallback to simple generation
        arch_md = output_path / 'architecture.md'
        with open(arch_md, 'w') as f:
            f.write(f"""# System Architecture

> Auto-generated baseline - requires manual refinement

## Technology Stack

{template_vars['TECH_STACK_DETAILS']}

## Components

{template_vars['SYSTEM_COMPONENTS']}

## Design Patterns

[TODO] Add architecture patterns
""")

    # Create features directory with README
    features_dir = output_path / 'features'
    features_dir.mkdir(exist_ok=True)

    readme = features_dir / 'README.md'
    with open(readme, 'w') as f:
        f.write("""# Features

This directory is used to document various system features.

## Usage

Create a separate Markdown file for each major feature, e.g., `user-authentication.md`.

You can use `../templates/feature.md.template` as a template.

## Next Steps

1. Identify core feature modules of the system
2. Create corresponding documentation files for each feature
3. Collaborate with the team to refine feature descriptions

---

*Tip: You can ask Claude to help identify and document features*
""")

    # Save generation metadata
    metadata = {
        'generated_at': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'analysis_summary': {
            'project_types': analysis['project_types'],
            'api_endpoints_count': len(analysis['api_endpoints']),
            'database_schemas_count': len(analysis['database_schemas']),
            'documentation_count': len(analysis['existing_docs'])
        }
    }

    metadata_file = output_path / '.analysis-metadata.json'
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    return {
        'project_md': str(project_md),
        'architecture_md': str(arch_md),
        'features_dir': str(features_dir),
        'metadata': str(metadata_file)
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
    parser.add_argument(
        '--generate-specs',
        action='store_true',
        help='Generate baseline OpenSpec specifications from analysis'
    )

    args = parser.parse_args()

    root_path = Path(args.project_root).resolve()

    if not root_path.exists():
        print(f"Error: Project root not found: {root_path}")
        sys.exit(1)

    # Check if OpenSpec is initialized
    if not (root_path / 'openspec').exists():
        print("⚠️  Project not yet initialized with OpenSpec")
        print("\nPlease run initialization command first:")
        print("  bash scripts/adopt-sdd.sh")
        print("\nOr initialize manually:")
        print("  npm install -g @fission-ai/openspec@latest && openspec init")
        sys.exit(1)

    print("=== Analyzing Project Context ===\n")

    # Perform analysis
    print("1. Detecting project type...")
    project_types = detect_project_type(root_path)
    print(f"   Found: {', '.join(project_types) if project_types else 'Unknown'}")

    print("2. Analyzing directory structure...")
    structure = analyze_directory_structure(root_path)

    print("3. Finding API patterns...")
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

    print(f"\n✅ Project context saved to: {output_path}")

    # Generate baseline specs if requested
    if args.generate_specs:
        print("\n7. Generating baseline specification files...")
        specs_dir = root_path / 'openspec' / 'specs'
        generated_files = generate_baseline_specs(analysis, specs_dir, root_path)

        print("   ✅ Generated baseline spec files:")
        print(f"      - {generated_files['project_md']}")
        print(f"      - {generated_files['architecture_md']}")
        print(f"      - {generated_files['features_dir']}/")
        print(f"      - {generated_files['metadata']}")

        print("\n" + "="*60)
        print("✨ Baseline specification generation complete")
        print("="*60)
        print("\n📝 Generated spec files contain basic information from code analysis")
        print("🔧 Please refine sections marked with [TODO] in Claude Code\n")
        print("Recommended next steps:")
        print("\n1️⃣  Refine specs in Claude Code:")
        print('   "Please read openspec/specs/project.md and help me')
        print('    complete all [TODO] sections with proper details"')
        print("\n2️⃣  Document core features:")
        print('   "Help me identify and document the core features')
        print('    in openspec/specs/features/"')
        print("\n3️⃣  Create first change proposal:")
        print('   "I want to add [FEATURE]. Please create an')
        print('    OpenSpec change proposal"')
    else:
        print("\n" + "="*60)
        print("Next steps: Generate baseline specs or collaborate with AI")
        print("="*60)
        print("\n💡 Tip: Add --generate-specs flag to automatically generate baseline spec files")
        print("\nRun one of the following commands in Claude Code:")
        print("\n1️⃣  Have Claude read the analysis results:")
        print(f'   "Please read {output_path} and help me')
        print('    create OpenSpec documentation for this project"')
        print("\n2️⃣  Create feature proposal:")
        print('   "I want to add [YOUR FEATURE]. Please create an')
        print('    OpenSpec change proposal for this feature"')

    print("\n📚 Reference documentation: reference/legacy-adoption.md")
    print("="*60)

if __name__ == "__main__":
    main()
