# Contributing to AIGo

Thank you for your interest in contributing to AIGo! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. We expect:

- Professional and courteous communication
- Constructive feedback and criticism
- Focus on what's best for the project
- Respect for differing viewpoints and experiences

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of compilers/interpreters
- Familiarity with Python development practices

### First Steps

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/aigo.git
   cd aigo
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/aigo-lang/aigo.git
   ```

4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Install Dependencies

```bash
# Install in development mode
pip install -e .[dev,test]

# Install pre-commit hooks
pre-commit install
```

### Verify Installation

```bash
# Run tests
pytest

# Check code quality
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/
mypy src/aigo

# Run example
aigo examples/hello.aigo
```

## How to Contribute

### Areas for Contribution

We welcome contributions in these areas:

1. **Core Language Features**
   - Lexer improvements
   - Parser enhancements
   - Interpreter optimizations
   - New language features

2. **Standard Library**
   - New modules (math, string, collections, etc.)
   - Function implementations
   - Documentation

3. **Tooling**
   - CLI improvements
   - REPL development
   - Debugging tools
   - IDE integrations

4. **Testing**
   - Unit tests
   - Integration tests
   - Performance benchmarks
   - Example programs

5. **Documentation**
   - API documentation
   - Tutorials
   - Language reference
   - Examples

6. **Infrastructure**
   - CI/CD improvements
   - Build system
   - Package distribution

### Finding Issues to Work On

- Check the [issue tracker](https://github.com/aigo-lang/aigo/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Ask in the issue comments if you want to work on something
- Check the [Development Roadmap](DEVELOPMENT_ROADMAP.md) for planned features

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 100 characters (not 79)
- **Quotes**: Double quotes for strings
- **Imports**: Organized using isort with black profile
- **Type hints**: Required for all public functions

### Code Formatting

We use automated formatters:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/
```

### Type Hints

All public functions must have type hints:

```python
def tokenize(self, source: str) -> List[Token]:
    """Tokenize source code."""
    ...

def parse_expression(self) -> Expression:
    """Parse an expression."""
    ...
```

### Documentation

All public classes and functions must have docstrings:

```python
def interpret_program(self, program: Program) -> None:
    """
    Interpret an AIGo program.

    Args:
        program: The parsed program to interpret

    Raises:
        AIGoError: If interpretation fails
    """
    ...
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `TokenType`, `Parser`)
- **Functions**: snake_case (e.g., `parse_expression`, `tokenize`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_TOKENS`, `VERSION`)
- **Private**: Prefix with underscore (e.g., `_internal_method`)

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Test both success and error cases
- Use descriptive test names

### Test Structure

```python
class TestFeature:
    """Test suite for feature X."""

    def test_basic_functionality(self):
        """Test basic use case."""
        # Arrange
        code = "let x = 42"

        # Act
        result = parse(code)

        # Assert
        assert result.value == 42

    def test_error_handling(self):
        """Test error case."""
        with pytest.raises(ParseError):
            parse("invalid code")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run with coverage
pytest --cov=src/aigo --cov-report=html

# Run specific test
pytest tests/test_parser.py::TestParser::test_basic_functionality
```

### Test Coverage

- Aim for 80%+ coverage for new code
- Critical paths should have 100% coverage
- Check coverage report: `open htmlcov/index.html`

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **perf**: Performance improvements

### Examples

```
feat(parser): add support for match expressions

Implement pattern matching syntax parsing with support for
multiple match arms and guard clauses.

Closes #123
```

```
fix(lexer): handle unicode characters correctly

Fixed issue where unicode characters were causing tokenization
to fail with encoding errors.

Fixes #456
```

```
docs(examples): add sorting algorithms examples

Added bubble sort, quick sort, and merge sort examples
to the algorithms directory.
```

### Rules

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be 50 characters or less
- Reference issues and PRs in the footer

## Pull Request Process

### Before Submitting

1. **Update your branch** with latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all checks**:
   ```bash
   # Format code
   black src/ tests/
   isort src/ tests/

   # Run linters
   flake8 src/ tests/
   mypy src/aigo

   # Run tests
   pytest

   # Run pre-commit hooks
   pre-commit run --all-files
   ```

3. **Update documentation** if needed

4. **Add tests** for new features

### Submitting

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub

3. Fill out the PR template completely

4. Link related issues using keywords (e.g., "Fixes #123")

### PR Requirements

Your PR must:

- Pass all CI/CD checks
- Maintain or improve code coverage
- Include tests for new features
- Update documentation if needed
- Follow coding standards
- Have a clear description

### Review Process

1. Maintainers will review your PR
2. Address feedback and requested changes
3. Push updates to your branch
4. Once approved, maintainers will merge your PR

### After Merge

1. Delete your feature branch
2. Pull latest changes:
   ```bash
   git checkout main
   git pull upstream main
   ```

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Try to reproduce with the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. Execute code '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- AIGo version: 1.0.0
- Python version: 3.11
- OS: Ubuntu 22.04

**Code Sample**
```aigo
// Minimal code to reproduce
let x = 42
```

**Error Message**
```
Full error traceback
```

**Additional Context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Proposed Solution**
How you'd like it to work

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Examples, mockups, or references

**Implementation Plan**
(Optional) Your thoughts on how to implement
```

## Documentation

### Documentation Types

1. **Code Documentation**
   - Docstrings for all public APIs
   - Inline comments for complex logic
   - Type hints

2. **User Documentation**
   - README.md updates
   - Tutorial additions
   - Example programs

3. **API Documentation**
   - Comprehensive function documentation
   - Usage examples
   - Parameter descriptions

### Writing Documentation

- Use clear, concise language
- Include code examples
- Explain the "why" not just the "what"
- Keep it up-to-date with code changes

### Building Documentation

```bash
# Generate API docs (if using Sphinx)
cd docs
make html

# View documentation
open _build/html/index.html
```

## Development Workflow

### Typical Workflow

1. Pick an issue or feature to work on
2. Create a feature branch
3. Write code and tests
4. Run tests and linters locally
5. Commit changes with clear messages
6. Push to your fork
7. Open a Pull Request
8. Address review feedback
9. Merge after approval

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Refactoring
- `test/description` - Test additions

### Keeping Up to Date

Regularly sync with upstream:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Chat**: Join our Discord/Slack (if available)
- **Email**: contact@aigo-lang.org (if available)
- **Issues**: For bugs and feature requests

## Recognition

Contributors are recognized in:

- CHANGELOG.md for their contributions
- README.md contributors section
- Release notes
- Project website (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AIGo! 🚀
