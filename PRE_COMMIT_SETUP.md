# Pre-commit Setup for Find File Type

This document describes the pre-commit configuration for the Find File Type project.

## What is Pre-commit?

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It helps ensure code quality, formatting, and other checks before commits are made to the repository.

## Installation

Pre-commit is included in the dev dependencies and will be installed when you run:

```bash
pip install -e ".[dev]"
```

After installation, activate pre-commit hooks:

```bash
pre-commit install
```

## Configured Hooks

### 1. General File Checks
- **trailing-whitespace**: Removes trailing whitespace from files
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML file syntax
- **check-toml**: Validates TOML file syntax
- **check-json**: Validates JSON file syntax
- **check-added-large-files**: Prevents large files (>1MB) from being committed
- **check-case-conflict**: Prevents case conflicts in filenames
- **check-merge-conflict**: Detects merge conflict markers
- **mixed-line-ending**: Fixes mixed line endings

### 2. Python Code Quality

#### Import Sorting (isort)
- Automatically sorts Python imports according to PEP8
- Configured to work with Black formatter
- Settings in `pyproject.toml`

#### Code Formatting (Black)
- Automatic Python code formatting
- Line length: 88 characters
- Compatible with isort

#### Linting (Flake8)
- Python code linting with additional plugins:
  - `flake8-docstrings`: Docstring checks
  - `flake8-bugbear`: Additional bug and design problems
  - `flake8-comprehensions`: List/dict comprehension improvements
  - `flake8-simplify`: Code simplification suggestions
- Configured to ignore certain docstring requirements for brevity

#### Type Checking (MyPy)
- Static type checking for Python
- Configuration in `pyproject.toml`
- Additional dependencies for better type inference

#### Security Linting (Bandit)
- Security issue detection in Python code
- Configuration in `pyproject.toml`
- Excludes test directories

#### Python Syntax Upgrade (PyUpgrade)
- Automatically upgrades Python syntax to modern versions
- Targets Python 3.8+ syntax

#### Docstring Style (Pydocstyle)
- Ensures consistent docstring formatting
- Uses Google docstring convention
- Relaxed settings for development

### 3. Project-Specific Checks

#### Test Execution
- **pytest-check**: Runs the test suite on commit
- **coverage-check**: Ensures minimum 90% test coverage on push

## Usage

### Automatic Execution
Pre-commit hooks run automatically when you make a commit:

```bash
git add .
git commit -m "Your commit message"
```

### Manual Execution
Run all hooks on all files:

```bash
pre-commit run --all-files
```

Run specific hook:

```bash
pre-commit run black
pre-commit run flake8
pre-commit run pytest-check
```

Run hooks on specific files:

```bash
pre-commit run --files src/fft/detector.py
```

### Bypassing Hooks
If you need to commit without running hooks (not recommended):

```bash
git commit --no-verify -m "Emergency commit"
```

## Configuration Files

### `.pre-commit-config.yaml`
Main pre-commit configuration file with all hook definitions.

### `pyproject.toml`
Contains tool-specific configurations:
- `[tool.black]`: Black formatter settings
- `[tool.isort]`: Import sorting settings
- `[tool.mypy]`: Type checker settings
- `[tool.bandit]`: Security linter settings

## Troubleshooting

### Hook Installation Issues
If hooks aren't running, reinstall them:

```bash
pre-commit uninstall
pre-commit install
```

### Update Hooks
Update to latest hook versions:

```bash
pre-commit autoupdate
```

### Skip Failing Hooks
Temporarily skip specific hooks:

```bash
SKIP=flake8,mypy git commit -m "Commit message"
```

### Performance Issues
Pre-commit caches environments for better performance. To clear cache:

```bash
pre-commit clean
```

## Benefits

1. **Consistent Code Style**: Automatic formatting ensures uniform code style
2. **Early Bug Detection**: Linting catches potential issues before they reach CI/CD
3. **Security**: Bandit helps identify security vulnerabilities
4. **Type Safety**: MyPy catches type-related errors
5. **Test Coverage**: Ensures tests pass and maintain coverage standards
6. **Automated Maintenance**: Reduces manual code review overhead

## Integration with CI/CD

While pre-commit runs locally, the same checks should be mirrored in your CI/CD pipeline to ensure code quality for all contributors, including those who might bypass local hooks.

Example GitHub Actions workflow snippet:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.8'

- name: Install dependencies
  run: |
    pip install -e ".[dev]"

- name: Run pre-commit
  run: pre-commit run --all-files
```

This ensures that all code quality checks are enforced both locally and in the CI environment. 
