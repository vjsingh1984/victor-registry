#!/usr/bin/env python3
"""
Sync victor-registry from PyPI.

This script searches PyPI for packages that start with 'victor-'
and updates the registry index with package information.

Usage:
    python scripts/sync-from-pypi.py [--dry-run]
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx


@dataclass
class PyPIPackage:
    """PyPI package information."""

    name: str
    version: str
    summary: str
    author: str
    license: str
    home_page: Optional[str]
    project_url: Optional[str]
    requires_python: Optional[str]


def search_pypi() -> List[PyPIPackage]:
    """Search PyPI for victor-* packages."""
    packages = []

    try:
        # Use PyPI's search API
        response = httpx.get(
            "https://pypi.org/search/",
            params={"q": "victor"},
            headers={"Accept": "application/json"},
            timeout=30.0,
        )

        # PyPI search doesn't have a proper JSON API, so we'll use the simple index
        # This is a simplified approach - a production version would be more robust
        response = httpx.get(
            "https://pypi.org/simple/",
            timeout=30.0,
        )

        # Parse HTML to find victor-* packages
        # For now, return empty list as this is a placeholder
        print("Note: PyPI sync is not fully implemented yet")
        print("In production, this would query PyPI's API or parse the simple index")

    except Exception as e:
        print(f"WARNING: Failed to query PyPI: {e}")

    return packages


def update_index(
    index_path: Path,
    pypi_packages: List[PyPIPackage],
    dry_run: bool = False,
) -> None:
    """Update index.json with PyPI packages."""
    # Load existing index
    try:
        with open(index_path) as f:
            index = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {index_path} not found")
        sys.exit(1)

    # Update statistics
    index["statistics"]["last_sync"] = "2025-01-09T00:00:00Z"

    # For each PyPI package, check if it's in the index
    for package in pypi_packages:
        print(f"Checking {package.name}...")

        # Look for existing entry
        existing = None
        for vertical in index["verticals"]:
            if vertical["name"] == package.name.replace("victor-", ""):
                existing = vertical
                break

        if existing:
            # Update version if needed
            if existing["version"] != package.version:
                print(f"  Updating {package.name} from {existing['version']} to {package.version}")
                if not dry_run:
                    existing["version"] = package.version
                    existing["last_updated"] = "2025-01-09T00:00:00Z"
        else:
            print(f"  New package: {package.name}")
            if not dry_run:
                # Add new entry (placeholder)
                new_vertical = {
                    "name": package.name.replace("victor-", ""),
                    "version": package.version,
                    "description": package.summary,
                    "author": package.author,
                    "license": package.license,
                    "homepage": package.home_page,
                    "repository": package.project_url,
                    "python_package": package.name,
                    "category": "unknown",
                    "tags": [],
                    "requires_victor": ">=0.5.0",
                    "registry_entry": f"packages/{package.name.replace('victor-', '')}",
                    "download_count": 0,
                    "star_count": 0,
                    "last_updated": "2025-01-09T00:00:00Z",
                    "verified": False,
                    "featured": False,
                }
                index["verticals"].append(new_vertical)

    # Update statistics
    index["statistics"]["total_verticals"] = len(index["verticals"])

    # Write back
    if not dry_run:
        with open(index_path, "w") as f:
            json.dump(index, f, indent=2)
        print(f"\nUpdated {index_path}")
    else:
        print("\nDry run - no changes made")


def main():
    """Main sync entry point."""
    parser = argparse.ArgumentParser(description="Sync victor-registry from PyPI")
    parser.add_argument("--dry-run", action="store_true", help="Don't make any changes")
    args = parser.parse_args()

    # Find index.json
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    index_path = repo_root / "index.json"

    print(f"Syncing from PyPI...")
    print(f"Index: {index_path}")
    print()

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print()

    # Search PyPI
    packages = search_pypi()

    if not packages:
        print("No victor-* packages found on PyPI")
        print("This is expected - sync is not fully implemented yet")
        return

    # Update index
    update_index(index_path, packages, dry_run=args.dry_run)

    print()
    print("Sync complete")


if __name__ == "__main__":
    main()
