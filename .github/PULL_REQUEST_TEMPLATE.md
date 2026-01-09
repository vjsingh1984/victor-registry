---
name: Package Submission
about: Submit a new vertical package to the registry
title: 'Add victor-<package-name> package'
labels: submission
assignees: ''
---

<!-- Thank you for submitting a package to the Victor Registry! -->

<!-- Please complete the following checklist -->

## Package Information

- **Package Name**: victor-{{ package name }}
- **Version**: {{ version }}
- **Category**: {{ security / data / devops / etc. }}
- **Description**: {{ brief description }}

## Submission Checklist

- [ ] I have read the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
- [ ] I have validated my package using `python scripts/validate-package.py`
- [ ] My package name is unique (checked `index.json`)
- [ ] My package follows the naming conventions (lowercase, alphanumeric)
- [ ] My package includes all required files:
  - [ ] `victor-vertical.toml`
  - [ ] `metadata.json`
  - [ ] `README.md`
- [ ] My package is published on PyPI or accessible via git
- [ ] My package uses a permissive license (Apache-2.0, MIT, BSD)
- [ ] My package includes clear documentation and examples

## Package Description

<!-- Describe what your vertical does and why it's useful -->

{{ detailed description }}

## Installation

<!-- How do users install your package? -->

```bash
pip install victor-{{ package name }}
```

## Usage Example

<!-- Provide a brief usage example -->

```bash
victor chat --vertical {{ package name }} "{{ example prompt }}"
```

## Additional Notes

<!-- Any additional information for reviewers -->

- **Dependencies**: {{ list major dependencies }}
- **Requires Tool Calling**: Yes/No
- **Preferred Providers**: {{ anthropic, openai, etc. }}
- **Known Limitations**: {{ any limitations }}

## Review Focus Areas

<!-- Please highlight areas you'd like reviewers to focus on -->

- {{ e.g., Documentation clarity }}
- {{ e.g., Installation process }}
- {{ e.g., Security considerations }}

---

**Note**: This PR will be automatically validated. Please check the Actions tab for validation results.
