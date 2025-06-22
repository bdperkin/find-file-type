# GitHub CI/CD Setup for Find File Type

This document describes the GitHub Actions CI/CD workflows implemented for the Find File Type project.

## Overview

The project uses GitHub Actions for continuous integration, automated testing, security scanning, and release management. The CI/CD setup consists of two main workflows and supporting configurations.

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)

The main CI workflow runs on every push and pull request to `main` and `develop` branches.

#### Jobs

**Code Quality Checks**
- Runs on Python 3.8-3.12
- Executes all pre-commit hooks
- Performs type checking with MyPy
- Security scanning with Bandit
- Uploads security reports as artifacts

**Test Suite**
- Comprehensive test execution across Python versions
- Code coverage reporting (minimum 90%)
- Coverage upload to Codecov
- Test results uploaded as artifacts

**Integration Tests**
- Full CLI functionality testing
- Package installation verification
- Real-world usage scenarios
- Import verification

**OS Compatibility Tests**
- Tests on Ubuntu, Windows, and macOS
- Python 3.8 and 3.11 versions
- Platform-specific dependency handling

**Dependency Security Check**
- Safety scanning for known vulnerabilities
- JSON and text report generation
- Artifact upload for review

**Build Test**
- Package building with `python -m build`
- Distribution validation with `twine check`
- Build artifacts upload

**Documentation Check**
- README validation
- Package metadata verification
- Version information check

**CI Summary**
- Aggregates all job results
- Provides clear pass/fail status
- Fails if critical jobs fail

### 2. Release Workflow (`.github/workflows/release.yml`)

Automated release management triggered by version tags or manual dispatch.

#### Jobs

**Test Before Release**
- Full test suite on all Python versions
- Quality gate before release

**Build**
- Creates distribution packages
- Validates package integrity
- Stores build artifacts

**Create Release**
- Generates changelog from git history
- Creates GitHub release
- Uploads release assets
- Automatic release notes

**Publish to PyPI**
- Publishes to PyPI on tag push
- Uses trusted publishing (OIDC)
- Hash verification

**Publish to Test PyPI**
- Manual testing on Test PyPI
- Safe testing environment

**Post-Release Tasks**
- Creates post-release checklist issue
- Automated tracking of release tasks

**Notification**
- Success/failure notifications
- Release status reporting

## Supporting Configurations

### Dependabot (`.github/dependabot.yml`)

Automated dependency updates:
- Weekly Python dependency updates
- GitHub Actions updates
- Proper labeling and assignment
- Ignore patterns for stability

### Issue Templates

**Bug Report Template** (`.github/ISSUE_TEMPLATE/bug_report.yml`)
- Structured bug reporting
- Version and environment information
- Reproduction steps
- Pre-submission checklist

**Feature Request Template** (`.github/ISSUE_TEMPLATE/feature_request.yml`)
- Feature proposal format
- Use case description
- Priority assessment
- Contribution options

## Trigger Events

### CI Workflow Triggers
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

### Release Workflow Triggers
```yaml
on:
  push:
    tags: [ 'v*' ]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to release'
        required: true
```

## Environment Requirements

### System Dependencies
- `libmagic1` (Ubuntu/Debian)
- `libmagic` (macOS via Homebrew)
- Windows: Automatic with python-magic-bin

### Python Dependencies
- All development dependencies from `pyproject.toml`
- Additional tools: `safety`, `build`, `twine`

## Security Features

### Dependency Scanning
- **Bandit**: Source code security analysis
- **Safety**: Known vulnerability scanning
- **Dependabot**: Automated security updates

### Publishing Security
- **Trusted Publishing**: OIDC-based PyPI publishing
- **Artifact Verification**: Hash checking
- **Environment Protection**: Release environments

## Artifacts and Reports

### Generated Artifacts
- **Test Results**: JUnit XML, HTML coverage reports
- **Security Reports**: Bandit JSON, Safety JSON
- **Build Packages**: Wheel and source distributions
- **Coverage Data**: XML for Codecov integration

### Report Integration
- **Codecov**: Coverage visualization and tracking
- **GitHub**: Inline security and quality reports
- **PyPI**: Package distribution and statistics

## Branch Protection

Recommended branch protection rules for `main`:

```yaml
required_status_checks:
  strict: true
  contexts:
    - "Code Quality Checks"
    - "Test Suite"
    - "Integration Tests"
    - "Documentation Check"
enforce_admins: true
required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true
```

## Usage Examples

### Running CI Locally

```bash
# Install dependencies
pip install -e ".[dev]"

# Run the same checks as CI
pre-commit run --all-files
pytest tests/ --cov=fft --cov-fail-under=90
mypy src/fft --config-file pyproject.toml
bandit -r src/
safety check
```

### Manual Release Process

```bash
# Create and push version tag
git tag v1.2.0
git push origin v1.2.0

# Or trigger manual release
# Go to GitHub Actions -> Release workflow -> Run workflow
```

### Testing Release Process

```bash
# Test build locally
python -m build
twine check dist/*

# Test installation
pip install dist/*.whl
fft --version
```

## Monitoring and Maintenance

### Regular Tasks
- Monitor CI success rates
- Review security scan results
- Update dependencies via Dependabot PRs
- Check coverage trends

### Performance Optimization
- Caching pip dependencies
- Parallel job execution
- Selective testing for draft PRs
- Artifact retention policies

### Troubleshooting

**Common Issues:**
1. **Test Failures**: Check temp file handling in different OS
2. **Magic Library**: Ensure libmagic is properly installed
3. **Coverage**: Verify test coverage doesn't drop below 90%
4. **Publishing**: Check PyPI credentials and permissions

**Debug Commands:**
```bash
# Local test debugging
pytest tests/ -v -s --tb=long

# Pre-commit debugging
pre-commit run --all-files --verbose

# Build debugging
python -m build --verbose
```

## Integration with Development Workflow

### Pull Request Process
1. Create feature branch
2. Make changes with tests
3. Push triggers CI checks
4. Review feedback from automated checks
5. Merge after approval and CI success

### Release Process
1. Update version in `pyproject.toml`
2. Update CHANGELOG or release notes
3. Create and push version tag
4. Automated release workflow executes
5. Monitor release completion
6. Complete post-release checklist

This CI/CD setup ensures code quality, security, and reliable releases while providing comprehensive feedback to developers throughout the development process. 
