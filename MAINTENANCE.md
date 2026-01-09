# Victor Registry Maintenance Guide

This document is for registry maintainers and covers the operational aspects of managing the victor-registry repository.

## Table of Contents

- [Overview](#overview)
- [Registry Structure](#registry-structure)
- [Daily Operations](#daily-operations)
- [Updating index.json](#updating-indexjson)
- [Validating Packages](#validating-packages)
- [Handling Submissions](#handling-submissions)
- [Security Considerations](#security-considerations)
- [Release Process](#release-process)
- [Troubleshooting](#troubleshooting)

## Overview

The victor-registry is a GitHub-native package registry for Victor verticals. It uses:
- Pull requests for submissions
- JSON index for programmatic access
- Automated validation via GitHub Actions
- Manual review for quality assurance

### Maintainer Responsibilities

- Review and merge package submissions
- Validate packages before acceptance
- Update index.json after merges
- Handle security reports
- Respond to user inquiries
- Maintain documentation

### Service Level Goals

- Initial PR response: 1-3 business days
- Full review: 1-2 weeks
- Security issues: 24 hours
- Critical bugs: 48 hours

## Registry Structure

```
victor-registry/
├── index.json                  # Master package index (SOURCE OF TRUTH)
├── packages/                   # Package entries
│   ├── example-security/      # Example package
│   │   ├── victor-vertical.toml
│   │   ├── metadata.json
│   │   └── README.md
│   └── [other packages]
└── scripts/
    ├── validate-index.py       # Validate index.json
    ├── validate-package.py    # Validate single package
    └── sync-from-pypi.py       # Sync from PyPI (TODO)
```

### Key Files

- `index.json` - Master index, source of truth for all packages
- `packages/*/victor-vertical.toml` - Package metadata (from author)
- `packages/*/metadata.json` - Registry metadata (maintained by us)
- `packages/*/README.md` - Package documentation (from author)

## Daily Operations

### Checking for New PRs

```bash
# List open PRs
gh pr list --state open

# Review a specific PR
gh pr view 123

# Checkout PR for testing
gh pr checkout 123
```

### Validating Incoming Packages

```bash
# Validate a single package
python scripts/validate-package.py packages/new-package

# Validate entire index
python scripts/validate-index.py

# Check for duplicates
python scripts/check-duplicates.py
```

### Updating Registry Statistics

Statistics are currently manual. Future automation will:
- Track download counts
- Monitor GitHub stars
- Calculate quality scores
- Generate usage reports

## Updating index.json

### When to Update

Update `index.json` when:
- A new package is merged
- A package version is updated
- A package is deprecated
- Statistics change significantly

### Manual Update Process

1. **Add New Package**

    After merging a package PR, add it to `index.json`:

    ```json
    {
      "name": "newpackage",
      "version": "1.0.0",
      "description": "Package description",
      "author": "Author Name",
      "license": "Apache-2.0",
      "homepage": "https://github.com/user/victor-newpackage",
      "repository": "https://github.com/user/victor-newpackage",
      "documentation": "https://github.com/user/victor-newpackage#readme",
      "python_package": "victor-newpackage",
      "category": "security",
      "tags": ["security", "scanning"],
      "requires_victor": ">=0.5.0",
      "registry_entry": "packages/newpackage",
      "download_count": 0,
      "star_count": 0,
      "last_updated": "2025-01-09T00:00:00Z",
      "verified": false,
      "featured": false
    }
    ```

2. **Update Existing Package**

    When a package releases a new version:

    ```bash
    # Edit index.json
    vim index.json

    # Update version and last_updated
    # Keep other fields the same
    ```

3. **Deprecate Package**

    To mark a package as deprecated:

    ```json
    {
      "name": "oldpackage",
      "status": "deprecated",
      "deprecation_notice": "Use newpackage instead"
    }
    ```

4. **Update Statistics**

    ```json
    {
      "statistics": {
        "total_verticals": 42,
        "categories": {
          "security": 10,
          "data": 8,
          "devops": 12
        },
        "last_sync": "2025-01-09T00:00:00Z"
      }
    }
    ```

5. **Validate Changes**

    ```bash
    python scripts/validate-index.py
    ```

### Automated Update (Future)

Currently manual. Future automation will:

1. Watch for package PR merges
2. Auto-update index.json
3. Validate changes
4. Commit and push

```bash
# Future command
python scripts/auto-update-index.py
```

## Validating Packages

### Pre-Merge Validation

Before merging any package PR:

```bash
# 1. Checkout the PR
gh pr checkout 123

# 2. Validate package structure
python scripts/validate-package.py packages/new-package

# 3. Check for conflicts
python scripts/check-name-conflict.py newpackage

# 4. Verify package accessibility
python scripts/check-package-access.py packages/new-package

# 5. Review documentation
python scripts/check-documentation.py packages/new-package
```

### Validation Checklist

- [ ] Package name is unique
- [ ] Package name follows conventions
- [ ] `victor-vertical.toml` is valid
- [ ] `metadata.json` is complete
- [ ] `README.md` is comprehensive
- [ ] Package is accessible (PyPI or git)
- [ ] License is permissive
- [ ] No security vulnerabilities
- [ ] Code quality is acceptable

### Manual Review Process

1. **Automated Checks** (GitHub Actions)
   - TOML schema validation ✓
   - JSON schema validation ✓
   - Name uniqueness ✓
   - File presence ✓

2. **Manual Review** (Maintainer)
   - Code quality
   - Documentation
   - Security
   - Usefulness

3. **Testing** (Optional)
   ```bash
   # Install package
   pip install victor-newpackage

   # Test with Victor
   victor vertical install victor-newpackage
   victor vertical info newpackage
   ```

## Handling Submissions

### Submission Workflow

1. **Author submits PR**
   - Creates package directory
   - Adds required files
   - Opens PR

2. **Automated validation runs**
   - Checks schema
   - Validates structure
   - Reports errors

3. **Maintainer reviews**
   - Checks quality
   - Tests functionality
   - Requests changes if needed

4. **Feedback to author**
   - Approve or request changes
   - Provide clear reasons
   - Be constructive

5. **Merge or close**
   - Merge if approved
   - Close with explanation if rejected
   - Update index.json

### Response Templates

#### Approval

```markdown
Thanks for your submission! I've reviewed your package and it looks great.

- ✓ Schema validation passed
- ✓ Documentation is comprehensive
- ✓ Code quality is good
- ✓ License is compatible

I'll merge this PR and update the index. Your package should be available in the registry within 24 hours.

One final note: Please add a release tag in your repository for version 1.0.0 so we can track updates.
```

#### Request Changes

```markdown
Thanks for your submission! I have a few requests before we can merge:

1. **Documentation**: The README doesn't include usage examples. Please add a "Usage" section with at least one complete example.

2. **License**: The license field in victor-vertical.toml is "GPL-3.0". We require permissive licenses (Apache-2.0, MIT, BSD). Would you be willing to relicense?

3. **Dependencies**: The package depends on `requests==2.0.0` which is very old. Consider updating to `requests>=2.31.0`.

Please address these issues and submit an updated PR. Feel free to ask if you have any questions!
```

#### Rejection

```markdown
Thank you for your interest in contributing to the Victor registry. Unfortunately, I'm unable to merge this package for the following reasons:

1. **Duplicate functionality**: This package duplicates the existing `security` vertical without significant improvements. We recommend contributing to the existing vertical instead.

2. **Security concerns**: The package downloads and executes arbitrary code from URLs without validation. This is a security risk we cannot accept in the registry.

3. **Incomplete documentation**: The README lacks installation instructions and usage examples.

If you'd like to address these issues, particularly the security concerns, we'd be happy to review a revised submission. Alternatively, we'd welcome contributions to the existing `security` vertical.

Please don't be discouraged - we appreciate your contribution to the Victor ecosystem!
```

## Security Considerations

### Package Security Review

When reviewing packages, check for:

1. **Code Execution**
   - No arbitrary code execution
   - No `eval()` or `exec()` on user input
   - Safe subprocess calls

2. **Network Access**
   - Validate URLs before requesting
   - Use timeouts
   - No hardcoded credentials

3. **File Access**
   - Validate file paths
   - Restrict to safe directories
   - No symlink attacks

4. **Dependencies**
   - Check for known vulnerabilities
   - Review transitive dependencies
   - Keep dependencies updated

5. **Input Validation**
   - Sanitize all user input
   - Validate file paths
   - Check for injection attacks

### Security Incident Response

If a security vulnerability is discovered:

1. **Assess severity**
   - Critical: Immediate action (24h)
   - High: Urgent action (48h)
   - Medium: Planned action (1 week)
   - Low: Backlog (1 month)

2. **Notify author**
   ```markdown
   We identified a potential security issue in your package.

   Issue: [description]
   Severity: [critical/high/medium/low]
   CVSS: [score]

   Please review and address within [timeline].

   Let us know if you have questions or need guidance.
   ```

3. **Temporary measures**
   - Mark as deprecated in index.json
   - Add security notice to README
   - Consider removal if critical

4. **Coordinate disclosure**
   - Work with author on fix
   - Announce after fix is released
   - Document in security advisories

### Malicious Packages

If you discover a malicious package:

1. **Immediately remove**
   ```bash
   # Remove from index
   # Mark repository as archived
   # Notify GitHub if needed
   ```

2. **Document incident**
   - Create security advisory
   - Document what happened
   - Share lessons learned

3. **Prevent recurrence**
   - Review validation process
   - Add new checks
   - Update guidelines

## Release Process

### Registry Releases

The registry itself follows semantic versioning:

- **Major** (1.0.0 → 2.0.0): Breaking changes to index format
- **Minor** (1.0.0 → 1.1.0): New fields, features
- **Patch** (1.0.0 → 1.0.1): Bug fixes, documentation

### Release Checklist

1. **Update version in index.json**
   ```json
   {
     "version": "1.1.0",
     "last_updated": "2025-01-09T00:00:00Z"
   }
   ```

2. **Update CHANGELOG.md**
   ```markdown
   ## [1.1.0] - 2025-01-09

   ### Added
   - New field: `quality` in metadata.json
   - Validation for README sections

   ### Changed
   - Improved validation error messages
   - Updated documentation

   ### Fixed
   - Fixed duplicate detection
   ```

3. **Create git tag**
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

4. **Create GitHub release**
   ```bash
   gh release create v1.1.0 --notes "Release v1.1.0"
   ```

### Announcements

Announce significant releases:

- [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)
- [Victor blog](https://victor.dev/blog)
- [Twitter/X](https://twitter.com/victorai)

## Troubleshooting

### Common Issues

#### index.json Validation Fails

```bash
ERROR: statistics.total_verticals (10) does not match actual count (11)
```

**Fix**: Update `statistics.total_verticals` to match the actual number of packages in the `verticals` array.

#### Package Not Found

```bash
ERROR: Package newpackage: Registry entry path does not exist
```

**Fix**: Ensure the package directory exists at `packages/newpackage/` with all required files.

#### Duplicate Package Name

```bash
ERROR: Duplicate package name: security
```

**Fix**: Check for existing entries with the same name. Names must be unique.

#### TOML Parse Error

```bash
ERROR: Invalid TOML: Invalid string (at line 15, column 8)
```

**Fix**: Check the TOML file for syntax errors. Common issues:
- Unclosed quotes
- Invalid escape sequences
- Missing commas

### Getting Help

If you encounter issues:

1. **Check documentation**
   - [README.md](./README.md)
   - [CONTRIBUTING.md](./CONTRIBUTING.md)
   - [packages/README.md](./packages/README.md)

2. **Search issues**
   - [GitHub Issues](https://github.com/vjsingh1984/victor-registry/issues)

3. **Ask for help**
   - [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)
   - Email: singhvjd@gmail.com

### Maintenance Scripts

#### Validate Everything

```bash
# Validate index
python scripts/validate-index.py

# Validate all packages
for dir in packages/*/; do
    python scripts/validate-package.py "$dir"
done
```

#### Check for Broken Links

```bash
# Check PyPI links
python scripts/check-pypi-links.py

# Check GitHub links
python scripts/check-github-links.py
```

#### Generate Statistics

```bash
# Count packages by category
python scripts/generate-stats.py --by-category

# List all maintainers
python scripts/generate-stats.py --list-maintainers

# Find unmaintained packages
python scripts/generate-stats.py --unmaintained
```

## Appendix

### Maintainer Checklist

Daily:
- [ ] Check for new PRs
- [ ] Review submissions
- [ ] Update index.json if needed
- [ ] Respond to inquiries

Weekly:
- [ ] Review closed PRs
- [ ] Update documentation
- [ ] Check for security issues
- [ ] Review statistics

Monthly:
- [ ] Review deprecated packages
- [ ] Update CHANGELOG
- [ ] Generate statistics report
- [ ] Review and improve processes

### Contact

Primary maintainer: Vijaykumar Singh (singhvjd@gmail.com)

For urgent issues, contact via GitHub Issues with the "urgent" label.

---

Last updated: 2025-01-09
