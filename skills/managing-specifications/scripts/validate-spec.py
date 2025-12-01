#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# requires-python = ">=3.8"
# ///
"""
Validate specification completeness for spec-kit and OpenSpec files.

Usage:
    uv run scripts/validate-spec.py <spec-file-path>
    uv run scripts/validate-spec.py specs/001-feature/spec.md
    uv run scripts/validate-spec.py openspec/changes/feature-name/proposal.md
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple


def validate_spec_kit_spec(content: str) -> List[str]:
    """Validate spec-kit specification file."""
    issues = []

    # Required sections for spec-kit specs
    required_sections = [
        ("# Overview", "Overview section"),
        ("# User Stories", "User Stories section"),
        ("# Requirements", "Requirements section"),
        ("# Acceptance Criteria", "Acceptance Criteria section"),
    ]

    for pattern, name in required_sections:
        if pattern.lower() not in content.lower():
            issues.append(f"Missing: {name}")

    # Check for concrete examples
    if "example" not in content.lower():
        issues.append("No examples found. Add concrete usage examples.")

    # Check for edge cases
    if "edge case" not in content.lower() and "error" not in content.lower():
        issues.append("No edge cases or error handling documented.")

    # Check for user story format
    if "as a" not in content.lower() or "i want" not in content.lower():
        issues.append("User stories may be incomplete. Use format: 'As a [user], I want...'")

    # Check for non-functional requirements
    nfr_keywords = ["performance", "security", "scalability", "availability"]
    if not any(kw in content.lower() for kw in nfr_keywords):
        issues.append("Consider adding non-functional requirements (performance, security, etc.)")

    return issues


def validate_openspec_proposal(content: str) -> List[str]:
    """Validate OpenSpec proposal file."""
    issues = []

    # Required sections for OpenSpec proposals
    required_sections = [
        ("# Problem", "Problem statement"),
        ("# Solution", "Proposed solution"),
        ("# Impact", "Impact analysis"),
    ]

    for pattern, name in required_sections:
        if pattern.lower() not in content.lower():
            issues.append(f"Missing: {name}")

    # Check for rationale
    if "why" not in content.lower() and "because" not in content.lower():
        issues.append("Missing rationale. Explain why this change is needed.")

    # Check for alternatives
    if "alternative" not in content.lower():
        issues.append("Consider documenting alternatives considered.")

    # Check for affected files/components
    if "affect" not in content.lower() and "impact" not in content.lower():
        issues.append("Document what files/components are affected.")

    return issues


def validate_openspec_tasks(content: str) -> List[str]:
    """Validate OpenSpec tasks file."""
    issues = []

    # Check for task list format
    task_pattern = r"- \[[ x]\]"
    tasks = re.findall(task_pattern, content)

    if not tasks:
        issues.append("No task checkboxes found. Use '- [ ] Task description' format.")
    elif len(tasks) < 2:
        issues.append("Only one task found. Consider breaking down further.")

    # Check for dependencies
    if "depend" not in content.lower() and "after" not in content.lower():
        issues.append("Consider documenting task dependencies.")

    return issues


def validate_openspec_design(content: str) -> List[str]:
    """Validate OpenSpec design file."""
    issues = []

    # Check for technical details
    technical_sections = [
        ("api", "API design"),
        ("database", "Database changes"),
        ("schema", "Schema changes"),
    ]

    found_technical = False
    for keyword, name in technical_sections:
        if keyword in content.lower():
            found_technical = True
            break

    if not found_technical:
        issues.append("Consider adding technical details (API, database, schema changes).")

    return issues


def detect_spec_type(path: Path) -> Tuple[str, callable]:
    """Detect specification type and return appropriate validator."""
    path_str = str(path)

    if "specs/" in path_str and path.name == "spec.md":
        return "spec-kit specification", validate_spec_kit_spec
    elif "openspec/changes" in path_str:
        if path.name == "proposal.md":
            return "OpenSpec proposal", validate_openspec_proposal
        elif path.name == "tasks.md":
            return "OpenSpec tasks", validate_openspec_tasks
        elif path.name == "design.md":
            return "OpenSpec design", validate_openspec_design
    elif "openspec/specs" in path_str:
        return "OpenSpec specification", validate_openspec_proposal  # Similar structure

    return None, None


def print_results(spec_type: str, path: Path, issues: List[str]) -> int:
    """Print validation results."""
    print(f"\n{'=' * 50}")
    print(f"Validating: {spec_type}")
    print(f"File: {path}")
    print('=' * 50)

    if not issues:
        print("\n✓ Specification is complete!\n")
        return 0
    else:
        print(f"\n⚠ Found {len(issues)} issue(s):\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
        return 1


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    spec_path = Path(sys.argv[1])

    if not spec_path.exists():
        print(f"Error: File not found: {spec_path}")
        sys.exit(1)

    # Read file content
    try:
        content = spec_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Detect spec type and get validator
    spec_type, validator = detect_spec_type(spec_path)

    if not validator:
        print(f"Unknown specification type: {spec_path}")
        print("\nSupported types:")
        print("  - specs/XXX-feature/spec.md (spec-kit)")
        print("  - openspec/changes/feature/proposal.md")
        print("  - openspec/changes/feature/tasks.md")
        print("  - openspec/changes/feature/design.md")
        sys.exit(1)

    # Validate and print results
    issues = validator(content)
    exit_code = print_results(spec_type, spec_path, issues)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
