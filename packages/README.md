# Victor Vertical Packages

This directory contains all registered vertical packages. Each subdirectory represents a single vertical package with its metadata and documentation.

## Package Structure

Each package MUST include the following files:

```
packages/your-vertical-name/
├── victor-vertical.toml    # REQUIRED: Package metadata
├── metadata.json             # REQUIRED: Registry metadata
└── README.md                 # REQUIRED: Package documentation
```

## victor-vertical.toml Specification

The `victor-vertical.toml` file is the core metadata file for your vertical package. It follows the TOML format and MUST include all required fields.

### Required Fields

```toml
[vertical]
# Package identity
name = "yourvertical"                   # Required: Unique, lowercase, alphanumeric
version = "1.0.0"                       # Required: Semantic version
description = "Brief description"       # Required: One-line description
authors = [{name = "Your Name"}]         # Required: At least one author
license = "Apache-2.0"                   # Required: SPDX license identifier

# Victor compatibility
requires_victor = ">=0.5.0"             # Required: Minimum Victor version

# Entry point
[vertical.class]
module = "victor_yourvertical"          # Required: Python module path
class_name = "YourVertical"             # Required: Vertical class name
```

### Optional Fields

```toml
[vertical]
# Python package information
python_package = "victor-yourvertical"  # Optional: PyPI package name

# URLs
homepage = "https://github.com/user/victor-yourvertical"
repository = "https://github.com/user/victor-yourvertical"
documentation = "https://docs.victor.dev/verticals/yourvertical"
issues = "https://github.com/user/victor-yourvertical/issues"

# Categorization
category = "security"                    # Optional: Category for grouping
tags = ["security", "scanning", "sast"]  # Optional: Search tags

[vertical.class]
# Capability advertisement
provides_tools = ["scan", "audit"]       # Optional: Tools provided
provides_workflows = ["security_review"] # Optional: Workflows provided
provides_capabilities = ["sast"]         # Optional: Capabilities provided

[vertical.dependencies]
# Runtime dependencies
python = ["requests>=2.0", "pyyaml>=6.0"]
verticals = ["coding"]                   # Other verticals required

[vertical.compatibility]
# Provider and platform requirements
requires_tool_calling = true             # Default: true
preferred_providers = ["anthropic", "openai"]
min_context_window = 100000              # Optional: Minimum tokens
python_version = ">=3.10"                # Default: ">=3.10"
platforms = ["linux", "macos", "windows"] # Default: all platforms

[vertical.security]
# Security metadata
signed = false                           # Default: false
verified_author = false                  # Default: false
permissions = ["network:read", "filesystem:read"]

[vertical.installation]
# Installation hints
install_command = "pip install victor-yourvertical"
```

## metadata.json Specification

The `metadata.json` file contains registry-specific metadata that is not part of the core package specification.

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
    "github": "https://github.com/yourusername/victor-yourvertical",
    "readthedocs": "https://victor-yourvertical.readthedocs.io/"
  },
  "statistics": {
    "downloads": 0,
    "stars": 0,
    "last_commit": "2025-01-09T00:00:00Z"
  },
  "reviews": {
    "count": 0,
    "average_rating": 0.0
  }
}
```

### metadata.json Fields

- `name` (required): Package name (must match victor-vertical.toml)
- `status` (required): One of "active", "deprecated", "unmaintained"
- `verified` (optional): Whether the package is verified by maintainers
- `featured` (optional): Whether to feature in the registry
- `maintainer` (required): Primary maintainer information
- `links` (optional): Related URLs
- `statistics` (optional): Download counts, stars, etc.
- `reviews` (optional): User reviews and ratings

## README.md Guidelines

Each package MUST include a README.md with the following sections:

### Required Sections

1. **Title and Description**
   ```markdown
   # Victor YourVertical

   Brief one-line description of your vertical.
   ```

2. **Installation**
   ```markdown
   ## Installation

   \`\`\`bash
   pip install victor-yourvertical
   \`\`\`
   ```

3. **Usage**
   ```markdown
   ## Usage

   Basic usage example...

   \`\`\`python
   # Example code
   \`\`\`
   ```

4. **Requirements**
   ```markdown
   ## Requirements

   - Victor >= 0.5.0
   - Python >= 3.10
   - Additional dependencies...
   ```

5. **License**
   ```markdown
   ## License

   This project is licensed under the Apache License 2.0 - see LICENSE file for details.
   ```

### Recommended Sections

- Configuration
- Examples
- API Reference
- Contributing
- Changelog
- Troubleshooting

## Creating a New Package

### 1. Create Directory

```bash
mkdir packages/your-vertical-name
cd packages/your-vertical-name
```

### 2. Create victor-vertical.toml

```bash
cat > victor-vertical.toml << 'EOF'
[vertical]
name = "yourvertical"
version = "1.0.0"
description = "Your vertical description"
authors = [{name = "Your Name", email = "you@example.com"}]
license = "Apache-2.0"
requires_victor = ">=0.5.0"

[vertical.class]
module = "victor_yourvertical"
class_name = "YourVertical"
EOF
```

### 3. Create metadata.json

```bash
cat > metadata.json << 'EOF'
{
  "name": "yourvertical",
  "status": "active",
  "verified": false,
  "featured": false,
  "maintainer": {
    "name": "Your Name",
    "github": "yourusername",
    "email": "you@example.com"
  }
}
EOF
```

### 4. Create README.md

```bash
cat > README.md << 'EOF'
# Victor YourVertical

Brief description.

## Installation

```bash
pip install victor-yourvertical
```

## Usage

...

## License

Apache License 2.0
EOF
```

### 5. Validate

```bash
cd ../..
python scripts/validate-package.py packages/your-vertical-name
```

## Naming Conventions

### Directory Names

- Must match the `name` field in victor-vertical.toml
- Use lowercase, alphanumeric characters and underscores
- Examples: `security`, `data_viz`, `api_tester`

### Python Package Names

- Should follow PyPI conventions
- Use lowercase with hyphens
- Prefix with `victor-` recommended
- Examples: `victor-security`, `victor-data-viz`

## Categories

Recommended categories for verticals:

- `development` - Development tools and utilities
- `security` - Security analysis and scanning
- `data` - Data processing and visualization
- `devops` - DevOps and infrastructure
- `testing` - Testing and quality assurance
- `documentation` - Documentation tools
- `monitoring` - Monitoring and logging
- `integration` - Third-party integrations
- `productivity` - Productivity enhancements
- `example` - Example and demo packages

## Validation

All packages are validated before acceptance. Validation checks:

1. **TOML Schema**
   - Valid TOML syntax
   - All required fields present
   - Correct data types

2. **Package Uniqueness**
   - No duplicate names
   - No reserved names

3. **Version Compatibility**
   - Valid semantic version
   - Compatible Victor version

4. **License**
   - Recognized SPDX identifier
   - Permissive license

5. **Accessibility**
   - PyPI package exists (if specified)
   - Git repository accessible (if specified)

Run validation locally:

```bash
python scripts/validate-package.py packages/your-vertical-name
```

## Example Package

See [example-security/](./example-security/) for a complete, production-ready example.

## Resources

- [Main Registry README](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Victor Documentation](https://docs.victor.dev)
- [Vertical Development Guide](https://docs.victor.dev/verticals)

## Support

For questions or issues:
- [GitHub Issues](https://github.com/vjsingh1984/victor-registry/issues)
- [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)
- Email: singhvjd@gmail.com
