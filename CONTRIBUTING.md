# Contributing to Victor Registry

Thank you for your interest in contributing to the Victor Vertical Registry! This document provides guidelines for submitting vertical packages.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Submission Guidelines](#submission-guidelines)
- [Package Structure](#package-structure)
- [Validation Process](#validation-process)
- [Review Criteria](#review-criteria)
- [Getting Help](#getting-help)

## Code of Conduct

- Be respectful and constructive
- Follow the [Victor Code of Conduct](https://github.com/vijay-singh/codingagent/blob/main/CODE_OF_CONDUCT.md)
- Accept feedback gracefully
- Help others improve their submissions

## Submission Guidelines

### Before Submitting

1. **Search the registry** - Ensure your vertical doesn't already exist
2. **Read the package guide** - Review [packages/README.md](./packages/README.md)
3. **Create your package** - Follow the vertical package structure
4. **Test locally** - Install and test your vertical thoroughly
5. **Document thoroughly** - Include clear documentation and examples

### Creating Your Submission

1. **Fork the repository**
   ```bash
   gh repo fork vjsingh1984/victor-registry
   ```

2. **Create your package directory**
   ```bash
   mkdir packages/your-vertical-name
   cd packages/your-vertical-name
   ```

3. **Add required files**
   - `victor-vertical.toml` - Package metadata
   - `metadata.json` - Registry metadata
   - `README.md` - Package documentation

4. **Validate your package**
   ```bash
   python scripts/validate-package.py packages/your-vertical-name
   ```

5. **Submit a pull request**
   ```bash
   git add packages/your-vertical-name
   git commit -m "Add victor-your-vertical package"
   git push origin main
   gh pr create --title "Add victor-your-vertical package"
   ```

### Pull Request Checklist

- [ ] Package name is unique (check `index.json`)
- [ ] Package name follows naming conventions (lowercase, alphanumeric)
- [ ] `victor-vertical.toml` is complete and valid
- [ ] `metadata.json` includes all required fields
- [ ] `README.md` provides clear documentation
- [ ] Package is published on PyPI or publicly accessible via git
- [ ] Package passes local validation
- [ ] PR title follows format: "Add victor-your-vertical package"
- [ ] PR description includes summary of vertical functionality

## Package Structure

### Required Files

Every package submission MUST include:

```
packages/your-vertical-name/
├── victor-vertical.toml    # Package metadata (REQUIRED)
├── metadata.json             # Registry metadata (REQUIRED)
└── README.md                 # Package documentation (REQUIRED)
```

### victor-vertical.toml

This is the core package metadata file. See [packages/README.md](./packages/README.md#victor-verticaltoml-specification) for the complete specification.

**Minimum required fields**:
```toml
[vertical]
name = "yourvertical"
version = "1.0.0"
description = "Brief description"
authors = [{name = "Your Name", email = "you@example.com"}]
license = "Apache-2.0"
requires_victor = ">=0.5.0"

[vertical.class]
module = "victor_yourvertical"
class_name = "YourVertical"
```

### metadata.json

Registry-specific metadata (not in victor-vertical.toml):

```json
{
  "name": "yourvertical",
  "status": "active",
  "verified": false,
  "featured": false,
  "maintainer": {
    "name": "Your Name",
    "github": "yourusername",
    "email": "you@example.com"
  },
  "links": {
    "pypi": "https://pypi.org/project/victor-yourvertical/",
    "github": "https://github.com/yourusername/victor-yourvertical"
  }
}
```

### README.md

Package documentation should include:

- Title and brief description
- Installation instructions
- Usage examples
- Configuration options
- Requirements and dependencies
- License information
- Contributing guidelines
- Changelog

## Validation Process

### Automated Checks

Your PR will automatically be checked for:

1. **Schema Validation**
   - Valid TOML syntax
   - All required fields present
   - Correct data types

2. **Name Uniqueness**
   - No conflict with existing packages
   - No reserved names (victor, core, tools, etc.)

3. **Version Compatibility**
   - Valid semantic version
   - Compatible Victor version requirement

4. **License Validation**
   - Recognized SPDX license identifier
   - Permissive license (Apache-2.0, MIT, BSD)

5. **Package Accessibility**
   - PyPI package exists (if specified)
   - Git repository is accessible (if specified)

### Manual Review

After passing automated checks, your submission will be reviewed for:

1. **Code Quality**
   - Clean, readable code
   - Follows Python best practices
   - Proper error handling

2. **Documentation**
   - Clear and comprehensive
   - Includes examples
   - API documentation if applicable

3. **Security**
   - No malicious code
   - Proper input validation
   - Secure dependency management

4. **Usefulness**
   - Solves a real problem
   - Not duplicating existing functionality
   - Aligns with Victor's goals

## Review Criteria

### Acceptance Criteria

Packages will be accepted if they:

- Pass all automated checks
- Have clear, comprehensive documentation
- Provide demonstrable value to Victor users
- Follow the package structure guidelines
- Use a permissive license
- Are actively maintained

### Common Rejection Reasons

Packages may be rejected if they:

- Fail automated validation
- Have incomplete or unclear documentation
- Duplicate existing functionality without improvement
- Use restrictive licenses (GPL, AGPL, etc.)
- Contain security vulnerabilities
- Are unmaintained or abandoned
- Violate the code of conduct

### Response Timeline

- Initial automated feedback: Immediate
- Initial maintainer response: 1-3 business days
- Complete review: 1-2 weeks
- Rejection will always include reasons

## Updating Your Package

### Minor Updates

For version updates and documentation improvements:

1. Update your package files
2. Open a PR with title: "Update victor-your-vertical to X.Y.Z"
3. No review required for minor version bumps

### Major Updates

For significant changes:

1. Update version (major version bump)
2. Include changelog in PR description
3. Full review required
4. May require new validation

### Deprecation

To deprecate your package:

1. Update `metadata.json`: `"status": "deprecated"`
2. Add deprecation notice to README
3. Open a PR with title: "Deprecate victor-your-vertical"
4. Include migration guide if applicable

## Naming Conventions

### Package Names

- Must be lowercase
- Must start with a letter
- Can contain letters, numbers, and underscores
- Must be unique in the registry
- Should be descriptive but concise

**Good examples**:
- `security`
- `data_viz`
- `api_tester`

**Bad examples**:
- `Security` (uppercase)
- `123package` (starts with number)
- `my-package` (hyphens not allowed)

### Python Package Names

Should follow PyPI conventions:
- All lowercase
- Use hyphens for separation
- Prefix with `victor-` recommended

**Good examples**:
- `victor-security`
- `victor-data-viz`
- `victor-api-tester`

## Getting Help

### Resources

- [Package Structure Guide](./packages/README.md)
- [Example Package](./packages/example-security/)
- [Victor Documentation](https://docs.victor.dev)
- [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)

### Asking Questions

1. **Check existing issues** - Your question may already be answered
2. **Search discussions** - Community knowledge base
3. **Create a discussion** - For questions and ideas
4. **Open an issue** - For bugs and problems

### Contact

- Email: singhvjd@gmail.com
- GitHub: @vjsingh1984

## Recognition

Contributors will be:
- Listed in the registry contributors section
- Mentioned in release notes (with permission)
- Eligible for contributor badges (future)

## License

By contributing to this registry, you agree that your contribution will be licensed under the Apache License 2.0.

## Security

If you discover a security vulnerability, please email singhvjd@gmail.com instead of creating an issue.

---

Thank you for contributing to the Victor ecosystem!
