#!/usr/bin/env python3
"""
Validate victor-registry index.json file.

This script validates the master index.json file for:
- JSON structure
- Required fields
- Data types
- Package references
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_index(index_path: Path) -> Dict[str, Any]:
    """Load and parse index.json."""
    try:
        with open(index_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {index_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {index_path}: {e}")
        sys.exit(1)


def validate_structure(index: Dict[str, Any]) -> List[str]:
    """Validate index.json structure."""
    errors = []

    # Required top-level fields
    required_fields = ["version", "last_updated", "verticals", "statistics"]
    for field in required_fields:
        if field not in index:
            errors.append(f"Missing required field: {field}")

    # Check verticals is a list
    if "verticals" in index and not isinstance(index["verticals"], list):
        errors.append("Field 'verticals' must be a list")

    # Check statistics is a dict
    if "statistics" in index and not isinstance(index["statistics"], dict):
        errors.append("Field 'statistics' must be a dict")

    return errors


def validate_vertical(vertical: Dict[str, Any], repo_root: Path) -> List[str]:
    """Validate a single vertical entry."""
    errors = []
    name = vertical.get("name", "unknown")

    # Required fields
    required_fields = [
        "name",
        "version",
        "description",
        "author",
        "license",
        "requires_victor",
        "registry_entry",
    ]
    for field in required_fields:
        if field not in vertical:
            errors.append(f"{name}: Missing required field: {field}")

    # Check registry_entry exists
    if "registry_entry" in vertical:
        entry_path = repo_root / vertical["registry_entry"]
        if not entry_path.exists():
            errors.append(f"{name}: Registry entry path does not exist: {entry_path}")

        # Check for required files
        if entry_path.exists():
            required_files = ["victor-vertical.toml", "metadata.json", "README.md"]
            for file in required_files:
                if not (entry_path / file).exists():
                    errors.append(f"{name}: Missing required file: {file}")

    # Validate data types
    if "name" in vertical and not isinstance(vertical["name"], str):
        errors.append(f"{name}: Field 'name' must be a string")

    if "version" in vertical and not isinstance(vertical["version"], str):
        errors.append(f"{name}: Field 'version' must be a string")

    if "tags" in vertical and not isinstance(vertical["tags"], list):
        errors.append(f"{name}: Field 'tags' must be a list")

    if "download_count" in vertical and not isinstance(vertical["download_count"], int):
        errors.append(f"{name}: Field 'download_count' must be an integer")

    if "verified" in vertical and not isinstance(vertical["verified"], bool):
        errors.append(f"{name}: Field 'verified' must be a boolean")

    if "featured" in vertical and not isinstance(vertical["featured"], bool):
        errors.append(f"{name}: Field 'featured' must be a boolean")

    return errors


def validate_statistics(index: Dict[str, Any]) -> List[str]:
    """Validate statistics section."""
    errors = []

    if "statistics" not in index:
        return errors

    stats = index["statistics"]

    # Check total_verticals matches actual count
    if "total_verticals" in stats:
        expected = stats["total_verticals"]
        actual = len(index.get("verticals", []))
        if expected != actual:
            errors.append(
                f"statistics.total_verticals ({expected}) does not match actual count ({actual})"
            )

    return errors


def check_duplicates(index: Dict[str, Any]) -> List[str]:
    """Check for duplicate package names."""
    errors = []
    seen = set()

    for vertical in index.get("verticals", []):
        name = vertical.get("name")
        if name:
            if name in seen:
                errors.append(f"Duplicate package name: {name}")
            seen.add(name)

    return errors


def main():
    """Main validation entry point."""
    # Find index.json
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.resolve()
    index_path = repo_root / "index.json"

    if not index_path.exists():
        print(f"ERROR: index.json not found at {index_path}")
        sys.exit(1)

    print(f"Validating {index_path}...")
    print()

    # Load index
    index = load_index(index_path)

    # Validate
    all_errors = []

    # Structure validation
    print("Checking structure...")
    all_errors.extend(validate_structure(index))

    # Vertical entries validation
    print("Checking vertical entries...")
    for vertical in index.get("verticals", []):
        all_errors.extend(validate_vertical(vertical, repo_root))

    # Statistics validation
    print("Checking statistics...")
    all_errors.extend(validate_statistics(index))

    # Duplicate check
    print("Checking for duplicates...")
    all_errors.extend(check_duplicates(index))

    # Report results
    print()
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) found")
        print()
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        vertical_count = len(index.get("verticals", []))
        print(f"VALIDATION PASSED: {vertical_count} vertical(s) validated successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
