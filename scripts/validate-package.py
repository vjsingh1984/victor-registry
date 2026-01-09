#!/usr/bin/env python3
"""
Validate a single victor-vertical package.

This script validates a package directory for:
- Required files
- TOML schema
- JSON schema
- README presence
"""

import json
import sys
from pathlib import Path


def validate_package_name(name: str) -> list[str]:
    """Validate package name format.

    Package names in victor-vertical.toml should use underscores (e.g., example_security).
    Directory names can use hyphens for readability (e.g., example-security).
    """
    errors = []

    # Must be lowercase
    if name != name.lower():
        errors.append("Package name must be lowercase")

    # Must start with letter
    if not name[0].isalpha():
        errors.append("Package name must start with a letter")

    # Must be alphanumeric with underscores or hyphens
    # TOML uses underscores, directories can use hyphens
    if not all(c.isalnum() or c in ("_", "-") for c in name):
        errors.append("Package name must contain only letters, numbers, underscores, or hyphens")

    # Check for reserved names
    reserved = {
        "victor",
        "core",
        "tools",
        "providers",
        "config",
        "ui",
        "tests",
        "framework",
        "agent",
        "workflows",
    }
    # Remove hyphens for reserved name check (normalize)
    normalized_name = name.replace("-", "_")
    if normalized_name in reserved:
        errors.append(f"Package name '{name}' conflicts with reserved name '{normalized_name}'")

    return errors


def validate_toml(toml_path: Path) -> list[str]:
    """Validate victor-vertical.toml file."""
    errors = []

    if not toml_path.exists():
        errors.append("Missing victor-vertical.toml")
        return errors

    # Try to parse TOML
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib

        with open(toml_path, "rb") as f:
            data = tomllib.load(f)

    except ImportError:
        errors.append("TOML parser not available (install tomli)")
        return errors
    except Exception as e:
        errors.append(f"Invalid TOML: {e}")
        return errors

    # Check for [vertical] section
    if "vertical" not in data:
        errors.append("Missing [vertical] section")
        return errors

    vertical = data["vertical"]

    # Required fields
    required_fields = [
        "name",
        "version",
        "description",
        "authors",
        "license",
        "requires_victor",
    ]
    for field in required_fields:
        if field not in vertical:
            errors.append(f"Missing required field: {field}")

    # Validate name
    if "name" in vertical:
        errors.extend(validate_package_name(vertical["name"]))

    # Validate version
    if "version" in vertical:
        try:
            from packaging.version import Version
            Version(vertical["version"])
        except Exception as e:
            errors.append(f"Invalid version: {e}")

    # Validate requires_victor
    if "requires_victor" in vertical:
        try:
            from packaging.requirements import Requirement
            req_str = vertical["requires_victor"]
            if not req_str.startswith("victor-ai"):
                req_str = f"victor-ai{req_str}"
            Requirement(req_str)
        except Exception as e:
            errors.append(f"Invalid requires_victor: {e}")

    # Check for [vertical.class] section
    if "class" not in vertical:
        errors.append("Missing [vertical.class] section")
    else:
        class_spec = vertical["class"]
        class_required = ["module", "class_name"]
        for field in class_required:
            if field not in class_spec:
                errors.append(f"Missing [vertical.class] field: {field}")

    return errors


def validate_metadata(metadata_path: Path) -> list[str]:
    """Validate metadata.json file."""
    errors = []

    if not metadata_path.exists():
        errors.append("Missing metadata.json")
        return errors

    # Try to parse JSON
    try:
        with open(metadata_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return errors

    # Required fields
    required_fields = ["name", "status", "maintainer"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate status
    if "status" in data:
        valid_statuses = ["active", "deprecated", "unmaintained"]
        if data["status"] not in valid_statuses:
            errors.append(f"Invalid status: {data['status']} (must be one of {valid_statuses})")

    # Validate maintainer
    if "maintainer" in data:
        maintainer = data["maintainer"]
        if not isinstance(maintainer, dict):
            errors.append("Field 'maintainer' must be an object")
        else:
            if "name" not in maintainer:
                errors.append("Missing maintainer.name")

    return errors


def validate_readme(readme_path: Path) -> list[str]:
    """Validate README.md file."""
    errors = []

    if not readme_path.exists():
        errors.append("Missing README.md")
        return errors

    # Check for required sections
    content = readme_path.read_text()
    required_sections = ["## Installation", "## Usage", "## License"]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing section: {section}")

    # Check minimum length
    if len(content) < 200:
        errors.append("README.md is too short (should be at least 200 characters)")

    return errors


def validate_consistency(package_dir: Path) -> list[str]:
    """Validate consistency between files."""
    errors = []

    toml_path = package_dir / "victor-vertical.toml"
    metadata_path = package_dir / "metadata.json"

    if not toml_path.exists() or not metadata_path.exists():
        return errors

    # Load names
    try:
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib

        with open(toml_path, "rb") as f:
            toml_data = tomllib.load(f)
        toml_name = toml_data.get("vertical", {}).get("name")

        with open(metadata_path) as f:
            metadata_data = json.load(f)
        metadata_name = metadata_data.get("name")

        # Normalize names for comparison (treat hyphens and underscores as equivalent)
        toml_normalized = toml_name.replace("-", "_") if toml_name else None
        metadata_normalized = metadata_name.replace("-", "_") if metadata_name else None

        if toml_normalized != metadata_normalized:
            errors.append(
                f"Name mismatch: victor-vertical.toml has '{toml_name}', "
                f"metadata.json has '{metadata_name}'"
            )

        # Check against directory name (normalize hyphens/underscores)
        dir_name = package_dir.name
        dir_normalized = dir_name.replace("-", "_")
        if toml_normalized != dir_normalized:
            errors.append(
                f"Name mismatch: directory is '{dir_name}', "
                f"victor-vertical.toml has '{toml_name}' (normalized: {toml_normalized} vs {dir_normalized})"
            )

    except Exception as e:
        errors.append(f"Error checking consistency: {e}")

    return errors


def main():
    """Main validation entry point."""
    if len(sys.argv) != 2:
        print("Usage: python validate-package.py <package-directory>")
        print()
        print("Example:")
        print("  python validate-package.py packages/example-security")
        sys.exit(1)

    package_dir = Path(sys.argv[1])

    if not package_dir.exists():
        print(f"ERROR: Package directory not found: {package_dir}")
        sys.exit(1)

    if not package_dir.is_dir():
        print(f"ERROR: Not a directory: {package_dir}")
        sys.exit(1)

    print(f"Validating package: {package_dir.name}")
    print()

    all_errors = []

    # Validate victor-vertical.toml
    print("Checking victor-vertical.toml...")
    all_errors.extend(validate_toml(package_dir / "victor-vertical.toml"))

    # Validate metadata.json
    print("Checking metadata.json...")
    all_errors.extend(validate_metadata(package_dir / "metadata.json"))

    # Validate README.md
    print("Checking README.md...")
    all_errors.extend(validate_readme(package_dir / "README.md"))

    # Validate consistency
    print("Checking file consistency...")
    all_errors.extend(validate_consistency(package_dir))

    # Report results
    print()
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) found")
        print()
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED: Package {package_dir.name} is valid")
        sys.exit(0)


if __name__ == "__main__":
    main()
