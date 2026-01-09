# Victor Vertical Registry

Central registry for Victor vertical packages - the official marketplace for discovering, sharing, and installing third-party verticals for the Victor AI coding assistant.

## What is a Vertical?

A **vertical** is a domain-specific extension for Victor that provides specialized tools, workflows, and capabilities. Examples include:
- Security analysis and vulnerability scanning
- Data visualization and reporting
- CI/CD pipeline automation
- Database management
- API testing and mocking

## About This Registry

This registry serves as the central index of all available vertical packages. It's a GitHub-native repository that uses:
- Pull requests for package submissions
- JSON index for programmatic access
- Automated validation via GitHub Actions
- Community-driven review process

## For Users

### Browse Verticals

Visit the [packages/](./packages/) directory to see all available verticals. Each package has:
- `victor-vertical.toml` - Package metadata
- `metadata.json` - Additional metadata (downloads, ratings)
- `README.md` - Package documentation

### Install a Vertical

```bash
# List available verticals
victor vertical list --source available

# Search for verticals
victor vertical search security

# Get detailed information
victor vertical info victor-security

# Install from PyPI
victor vertical install victor-security

# Install from git
victor vertical install git+https://github.com/user/victor-security.git

# Install from local path
victor vertical install /path/to/victor-security
```

### Update the Registry

Victor caches the registry locally. To force an update:

```bash
victor vertical cache --clear
victor vertical list --source available
```

## For Package Authors

### Submitting a Vertical

1. **Create your vertical package** following the [vertical package structure](./packages/README.md)

2. **Add your package to this registry** by creating a pull request:
   - Fork this repository
   - Create a new directory in `packages/your-vertical-name/`
   - Add your package files (see below)
   - Submit a PR

3. **Required Files**:
   ```
   packages/your-vertical-name/
   ├── victor-vertical.toml    # REQUIRED: Package metadata
   ├── metadata.json             # REQUIRED: Registry metadata
   └── README.md                 # REQUIRED: Package documentation
   ```

### Package Requirements

Your package MUST:
- Follow the [victor-vertical.toml specification](./packages/README.md#victor-verticaltoml-specification)
- Pass validation checks (automatic)
- Be published on PyPI or publicly accessible via git
- Include documentation and examples
- Follow semantic versioning
- Use a permissive license (Apache-2.0, MIT, BSD)

### Validation

All submissions are automatically validated:
- TOML schema validation
- Package name uniqueness
- Version compatibility check
- License validation
- Required fields completeness

### Review Process

1. **Automated Checks** (via GitHub Actions)
   - Schema validation
   - Name collision detection
   - Version format check

2. **Manual Review** (by maintainers)
   - Code quality
   - Documentation completeness
   - Security review
   - Usefulness to community

3. **Acceptance Criteria**
   - Passes all automated checks
   - Has clear documentation
   - Provides real value
   - Follows best practices

### Timeline

- Initial response: 1-3 business days
- Full review: 1-2 weeks
- Rejection reasons will always be provided

## For Maintainers

### Registry Management

See [MAINTENANCE.md](./MAINTENANCE.md) for detailed instructions on:
- Updating `index.json`
- Validating packages
- Handling updates
- Security considerations
- Release process

### Quick Commands

```bash
# Validate index.json
python scripts/validate-index.py

# Sync from PyPI
python scripts/sync-from-pypi.py

# Generate stats
python scripts/generate-stats.py
```

## Registry Structure

```
victor-registry/
├── README.md                   # This file
├── index.json                  # Master package index
├── CONTRIBUTING.md             # Contribution guidelines
├── MAINTENANCE.md              # Maintainer guide
├── packages/                   # Package entries
│   ├── README.md              # Package submission guide
│   ├── example-security/      # Example package
│   │   ├── victor-vertical.toml
│   │   ├── metadata.json
│   │   └── README.md
│   └── [other packages]
└── scripts/
    ├── validate-index.py       # Validate index.json
    ├── validate-package.py    # Validate single package
    └── sync-from-pypi.py       # Sync PyPI packages
```

## API Access

The registry is accessible via HTTP:

```bash
# Get all verticals
curl https://registry.victor.dev/api/v1/verticals

# Get specific vertical
curl https://registry.victor.dev/api/v1/verticals/victor-security

# Search verticals
curl https://registry.victor.dev/api/v1/verticals?search=security
```

**Note**: HTTP API is not yet implemented. Currently, Victor reads directly from this GitHub repository.

## License

This registry is licensed under the Apache License 2.0. Individual packages retain their own licenses.

## Contact

- Issues: [GitHub Issues](https://github.com/vjsingh1984/victor-registry/issues)
- Discussions: [GitHub Discussions](https://github.com/vjsingh1984/victor-registry/discussions)
- Email: singhvjd@gmail.com

## See Also

- [Victor Documentation](https://docs.victor.dev)
- [Victor GitHub](https://github.com/vijay-singh/codingagent)
- [Vertical Development Guide](https://docs.victor.dev/verticals)
