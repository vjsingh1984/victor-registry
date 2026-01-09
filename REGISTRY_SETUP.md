# Victor Registry Setup Guide

This guide walks you through setting up the victor-registry repository on GitHub and preparing it for package submissions.

## Prerequisites

- GitHub account
- Git installed
- Python 3.10+ installed
- Basic familiarity with GitHub and pull requests

## Step 1: Create the GitHub Repository

### 1.1 Initialize Repository

```bash
# Navigate to the temporary registry location
cd /tmp/victor-registry

# Initialize git repository
git init

# Add all files
git add .

# Make scripts executable
chmod +x scripts/*.py

# Initial commit
git commit -m "Initial commit: Victor registry setup"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `victor-registry`
3. Description: `Central registry for Victor vertical packages`
4. Visibility: **Public** (important for discoverability)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 1.3 Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/vjsingh1984/victor-registry.git

# Push main branch
git push -u origin main
```

## Step 2: Configure Repository Settings

### 2.1 Enable Branch Protection

1. Go to **Settings** → **Branches**
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Dismiss stale reviews when new commits are pushed
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
5. Click "Create"

### 2.2 Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Select "Allow all actions and reusable workflows"
3. Click "Save"

### 2.3 Enable Issues and Discussions

1. Go to **Settings** → **General**
2. Features:
   - ✅ Issues
   - ✅ Discussions
   - ✅ Wiki (optional)
   - ✅ Projects (optional)

### 2.4 Set Up Labels

Go to **Issues** → **Labels** and create:

- `submission` - Blue - For package submissions
- `bug` - Red - For bugs
- `enhancement` - Green - For improvements
- `documentation` - Purple - For docs
- `security` - Red - For security issues
- `urgent` - Red - For urgent matters
- `good first issue` - Green - For new contributors

## Step 3: Create GitHub Actions Workflows

### 3.1 Package Validation Workflow

Create `.github/workflows/validate-package.yml`:

```yaml
name: Validate Package

on:
  pull_request:
    paths:
      - 'packages/**'
  push:
    paths:
      - 'packages/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml packaging

      - name: Validate changed packages
        run: |
          # Find changed package directories
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            echo "Finding changed packages in PR..."
            # Use git to find changed directories
            git diff --name-only ${{ github.event.pull_request.base.sha }} ${{ github.sha }} | \
              grep '^packages/' | \
              cut -d'/' -f2 | \
              sort -u | \
              while read pkg; do
                if [ -n "$pkg" ]; then
                  echo "Validating $pkg..."
                  python scripts/validate-package.py "packages/$pkg"
                fi
              done
          else
            echo "Validating all packages..."
            for pkg in packages/*/; do
              echo "Validating $pkg..."
              python scripts/validate-package.py "$pkg"
            done
          fi

      - name: Validate index.json
        run: |
          python scripts/validate-index.py
```

### 3.2 Index Update Workflow

Create `.github/workflows/update-index.yml`:

```yaml
name: Update Index

on:
  push:
    branches: [main]
    paths:
      - 'packages/**'

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Check index consistency
        run: |
          python scripts/validate-index.py

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ Package validated successfully! Please update index.json manually before merging.'
            })
```

### 3.3 Commit Workflows

```bash
# Add workflows
git add .github/workflows/

# Commit
git commit -m "Add GitHub Actions workflows for validation"

# Push
git push
```

## Step 4: Create Documentation

### 4.1 Add Code of Conduct

Create `CODE_OF_CONDUCT.md`:

```markdown
# Contributor Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

## Scope

This Code of Conduct applies within all community spaces, and also applies
when an individual is officially representing the community in public spaces.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project team: singhvjd@gmail.com

All complaints will be reviewed and investigated and will result in a response
that is deemed necessary and appropriate to the circumstances.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.0.

[homepage]: https://www.contributor-covenant.org
```

### 4.2 Add Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this registry, please email
singhvjd@gmail.com rather than creating a public issue.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if known)

We will:
- Acknowledge receipt within 24 hours
- Provide initial assessment within 48 hours
- Coordinate disclosure and fix
- Credit you for the discovery

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Security Audits

This registry is intended to be a trusted source of packages. All submissions
are reviewed for security issues before being accepted.
```

### 4.3 Create LICENSE

This should already be covered by the Apache License 2.0 in the README, but create the actual LICENSE file:

```bash
# Add Apache 2.0 license
cat > LICENSE << 'EOF'
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   [Full license text - see https://www.apache.org/licenses/LICENSE-2.0]
EOF

git add LICENSE CODE_OF_CONDUCT.md SECURITY.md
git commit -m "Add license and policies"
git push
```

## Step 5: Configure Repository Description

### 5.1 Update Repository Topics

On GitHub, go to your repository → **Settings** → **Topics**, and add:
- `victor`
- `victor-ai`
- `package-registry`
- `python-package`
- `verticals`
- `ai-coding-assistant`

### 5.2 Set Up Repository Description

In **Settings** → **General**:
- Description: `Central registry for Victor vertical packages - the official marketplace for discovering and installing third-party extensions`
- Website URL: `https://docs.victor.dev`

## Step 6: Initial Package Setup

### 6.1 Review Example Package

The example package is already set up in `/tmp/victor-registry/packages/example-security/`. This serves as a template for submitters.

### 6.2 Test Validation

```bash
# Test validation scripts
cd /tmp/victor-registry

# Validate index
python scripts/validate-index.py

# Validate example package
python scripts/validate-package.py packages/example-security

# Should output:
# VALIDATION PASSED: Package example-security is valid
```

## Step 7: Create First Submission

### 7.1 Test the Submission Process

To test the PR workflow, create a test package:

```bash
# Create test package
cd /tmp/victor-registry
mkdir -p packages/test-security

# Copy from example
cp packages/example-security/victor-vertical.toml packages/test-security/
cp packages/example-security/metadata.json packages/test-security/

# Edit names
sed -i '' 's/example_security/test_security/g' packages/test-security/victor-vertical.toml
sed -i '' 's/example_security/test_security/g' packages/test-security/metadata.json

# Create README
cat > packages/test-security/README.md << 'EOF'
# Test Security Vertical

This is a test package to validate the submission process.

## Installation

```bash
pip install victor-test-security
```

## License

Apache License 2.0
EOF

# Validate
python scripts/validate-package.py packages/test-security

# Commit
git add packages/test-security
git commit -m "Add test-security package for validation testing"

# Push (you'll need to create a branch first)
git checkout -b test-package
git push -u origin test-package

# Create PR via GitHub CLI
gh pr create --title "Test: Add test-security package" --body "Testing PR workflow"
```

### 7.2 Review Validation

1. Go to the PR on GitHub
2. Check the Actions tab to see validation results
3. Review the automated checks
4. Test the merge process (or close the PR)

## Step 8: Announce the Registry

### 8.1 Create Announcement

Draft an announcement for:

**Victor Blog**:
```markdown
# Announcing the Victor Vertical Registry

We're excited to announce the official Victor Vertical Registry - a central
marketplace for discovering and installing third-party verticals.

## What's a Vertical?

[Explain verticals...]

## How to Submit

[Link to CONTRIBUTING.md]

## Current Packages

[List initial packages...]

## Get Started

```bash
victor vertical list --source available
```
```

**GitHub Discussions**:
- Create a "Welcome" post
- Pin to top of discussions

**Twitter/X**:
```
🎉 Excited to announce the Victor Vertical Registry!

Discover and install third-party extensions for Victor AI coding assistant.

📦 View packages: https://github.com/vjsingh1984/victor-registry
📖 Learn more: https://docs.victor.dev/verticals

#VictorAI #Python #CodingAssistant
```

### 8.2 Update Documentation

Update Victor documentation to reference the registry:
- Installation guide
- Vertical development guide
- API reference

## Step 9: Ongoing Maintenance

### 9.1 Regular Tasks

**Daily**:
- Monitor incoming PRs
- Review submissions
- Update index.json

**Weekly**:
- Review and merge approved PRs
- Update statistics
- Respond to inquiries

**Monthly**:
- Generate statistics report
- Review deprecated packages
- Update documentation

### 9.2 Monitor Metrics

Track:
- Number of packages
- PR merge rate
- Average review time
- Package downloads (if available)

## Step 10: Future Enhancements

### Planned Features

1. **HTTP API**
   - REST API for package queries
   - Package search endpoint
   - Version information

2. **Automated Sync**
   - Auto-sync from PyPI
   - Update package versions
   - Detect deprecated packages

3. **Quality Metrics**
   - Download counts
   - Star counts
   - User ratings
   - Quality scores

4. **Web Interface**
   - Browse packages online
   - Search and filter
   - Package comparisons

## Verification Checklist

After setup, verify:

- [ ] Repository created on GitHub
- [ ] All files pushed to main branch
- [ ] Branch protection enabled
- [ ] GitHub Actions workflows created
- [ ] Example package validates successfully
- [ ] Index validation passes
- [ ] Documentation complete
- [ ] Security policy in place
- [ ] Code of conduct added
- [ ] Repository topics set
- [ ] Test PR created and validated
- [ ] Ready for submissions

## Troubleshooting

### Scripts Not Executable

```bash
chmod +x scripts/*.py
git add scripts/*.py
git commit -m "Make scripts executable"
git push
```

### Validation Fails

```bash
# Check Python version
python --version  # Should be 3.10+

# Install dependencies
pip install pyyaml packaging

# Validate manually
python scripts/validate-index.py
```

### GitHub Actions Fail

1. Check Actions tab for error logs
2. Verify Python version in workflow
3. Check for missing dependencies
4. Ensure scripts are executable

## Next Steps

1. Create first real package submission
2. Announce registry to community
3. Gather feedback
4. Iterate on process
5. Add automation

## Support

For questions or issues:
- GitHub Issues: https://github.com/vjsingh1984/victor-registry/issues
- GitHub Discussions: https://github.com/vjsingh1984/victor-registry/discussions
- Email: singhvjd@gmail.com

---

**Congratulations!** Your victor-registry is now set up and ready for package submissions.

Last updated: 2025-01-09
