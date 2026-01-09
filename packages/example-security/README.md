# Victor Example Security Vertical

**IMPORTANT**: This is an **example package** for demonstration purposes only. It showcases the structure and format of a proper Victor vertical package submission. This package does not provide any actual functionality.

## Purpose

This example package demonstrates:
- Proper `victor-vertical.toml` structure
- Required `metadata.json` format
- Comprehensive documentation
- Package organization

## What This Package Would Provide (If Real)

If this were a real security vertical, it would provide:

### Tools
- `security_scan` - Scan code for security vulnerabilities
- `vulnerability_check` - Check dependencies for known vulnerabilities
- `dependency_audit` - Audit project dependencies for security issues

### Workflows
- `security_review` - Automated security review workflow
- `vulnerability_assessment` - Comprehensive vulnerability assessment

### Capabilities
- Static Application Security Testing (SAST)
- Dependency scanning
- Security reporting

## Installation (Example)

```bash
# This would install the vertical (if it were real)
victor vertical install victor-example-security

# Or from PyPI (if published)
pip install victor-example-security
```

## Usage (Example)

```bash
# This would list security tools (if functional)
victor vertical info example-security

# This would run a security scan (if implemented)
victor chat --vertical example-security "Scan my code for vulnerabilities"
```

## Package Structure

This example package includes all required files:

```
packages/example-security/
├── victor-vertical.toml    # Package metadata (REQUIRED)
├── metadata.json             # Registry metadata (REQUIRED)
└── README.md                 # This file (REQUIRED)
```

## victor-vertical.toml Breakdown

### Required Fields
- `name` - Unique identifier (example_security)
- `version` - Semantic version (1.0.0)
- `description` - Brief description
- `authors` - Author information
- `license` - SPDX license identifier (Apache-2.0)
- `requires_victor` - Minimum Victor version
- `class.module` - Python module path
- `class.class_name` - Vertical class name

### Optional Fields Shown
- `python_package` - PyPI package name (null for this example)
- `homepage`, `repository`, etc. - URLs
- `category` - Category for grouping (example)
- `tags` - Search tags
- `provides_tools` - Tools provided by this vertical
- `provides_workflows` - Workflows provided
- `provides_capabilities` - Capabilities exposed
- `dependencies` - Runtime dependencies
- `compatibility` - Provider and platform requirements
- `security` - Security metadata
- `installation` - Installation hints

## metadata.json Breakdown

### Required Fields
- `name` - Package name (must match victor-vertical.toml)
- `status` - One of: active, deprecated, unmaintained
- `maintainer` - Primary maintainer information

### Optional Fields Shown
- `verified` - Whether verified by registry maintainers
- `featured` - Whether to feature in the registry
- `links` - Related URLs
- `statistics` - Download counts, stars, etc.
- `reviews` - User reviews and ratings
- `quality` - Quality scores
- `notes` - Additional notes

## Creating Your Own Package

To create your own vertical package:

1. **Copy this example**
   ```bash
   cp -r packages/example-security packages/your-vertical-name
   ```

2. **Edit victor-vertical.toml**
   - Change `name` to your vertical name
   - Update `version`, `description`, `authors`
   - Modify `class.module` and `class.class_name`
   - Add your tools, workflows, capabilities
   - Adjust dependencies and compatibility

3. **Edit metadata.json**
   - Update `name` to match victor-vertical.toml
   - Add your maintainer information
   - Update links and statistics

4. **Write your README.md**
   - Include installation instructions
   - Provide usage examples
   - Document configuration options
   - Add troubleshooting section

5. **Validate your package**
   ```bash
   python scripts/validate-package.py packages/your-vertical-name
   ```

6. **Submit to registry**
   - Fork the registry repository
   - Add your package directory
   - Create a pull request

## Requirements (If Real)

- Victor >= 0.5.0
- Python >= 3.10
- Tool calling support (Anthropic, OpenAI, Google)

## License

Apache License 2.0

## Contributing

This is an example package. For contributing to the actual registry, see:
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [packages/README.md](../README.md)

## Resources

- [Victor Documentation](https://docs.victor.dev)
- [Vertical Development Guide](https://docs.victor.dev/verticals)
- [Registry Guidelines](../../CONTRIBUTING.md)
- [Package Structure Guide](../README.md)

## Support

For questions about creating your own vertical:
- [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)
- [GitHub Issues](https://github.com/vjsingh1984/victor-registry/issues)
- Email: singhvjd@gmail.com

---

**Note**: Again, this is an **example package only**. It is not functional and cannot be installed or used.
