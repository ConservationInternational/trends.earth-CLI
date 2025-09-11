# GitHub Copilot Instructions for trends.earth CLI

This document provides development guidance and coding standards for GitHub Copilot when working on the trends.earth CLI project.

## Project Overview

The trends.earth CLI is a command-line interface for the trends.earth platform, enabling local development, testing, and deployment of custom geospatial analysis scripts. The CLI is built with Python and uses Docker containers for script execution.

## Development Environment

**IMPORTANT**: Before starting any development work, ensure you've completed the setup steps in [copilot-setup-steps.md](./copilot-setup-steps.md).

## Code Style and Standards

### Python Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions and methods (project is transitioning to full type coverage)
- Maintain compatibility with Python 3.10+
- Use descriptive variable and function names
- Add docstrings for all public functions and classes

### Example function with proper typing:
```python
from typing import Optional, Dict, Any

def example_function(param: str, optional_param: Optional[int] = None) -> bool:
    """
    Example function with proper type hints and docstring.

    Args:
        param: Required string parameter
        optional_param: Optional integer parameter

    Returns:
        True if operation successful, False otherwise
    """
    # Implementation here
    return True
```

### Code Quality Tools
The project uses several tools for maintaining code quality:
- **Ruff**: Linting and code formatting
- **mypy**: Type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for quality checks

Always run these before committing:
```bash
# Lint and format code
ruff check .
ruff format .

# Type checking
mypy tecli/

# Run tests
pytest

# Run all quality checks
pre-commit run --all-files
```

## Project Structure

```
trends.earth-CLI/
├── tecli/                  # Main package
│   ├── __init__.py        # Package initialization and main() function
│   ├── __main__.py        # Module entry point
│   ├── commands.py        # Commands class with all CLI commands
│   ├── *.py              # Individual command implementations
│   ├── run/              # Docker configuration
│   └── skeleton/         # Project template files
├── tests/                 # Test files
├── examples/             # Example projects
└── pyproject.toml        # Project configuration
```

## Key Components

### Commands Class (`tecli/commands.py`)
Central class containing all CLI commands as static methods:
- `create()` - Creates new script projects
- `start()` - Runs scripts locally in Docker
- `config()` - Manages configuration
- `login()` - Handles authentication
- `publish()` - Deploys scripts to trends.earth
- `download()` - Downloads existing scripts
- `info()` - Shows project information
- `logs()` - Retrieves execution logs
- `clear()` - Cleans up Docker resources

### Command Implementation Pattern
Each command should follow this pattern:
```python
@staticmethod
def command_name(param1: str, param2: Optional[str] = None) -> None:
    """Command description."""
    try:
        print("Starting command...")
        if module.run(param1, param2):
            print(colored("Success message", "green"))
        else:
            print(colored("Error message", "red"))
    except Exception as error:
        logging.error(error)
```

## Testing Guidelines

### Test Structure
- All tests are in the `tests/` directory
- Use descriptive test names: `test_function_name_expected_behavior`
- Group related tests in classes when appropriate
- Test both success and error cases

### Test Example
```python
def test_command_success_case():
    """Test that command works correctly with valid input."""
    # Arrange
    test_input = "valid_input"

    # Act
    result = commands.Commands.example_command(test_input)

    # Assert
    assert result is True

def test_command_error_case():
    """Test that command handles errors gracefully."""
    # Test error handling
    pass
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_commands.py

# Run with coverage
pytest --cov=tecli

# Run specific test
pytest tests/test_commands.py::test_specific_function
```

## Docker Integration

The CLI uses Docker for script execution:
- Dockerfile is in `tecli/run/Dockerfile`
- Scripts run in containerized environment
- Local testing vs production deployment differences

## Configuration Management

- Configuration file: `~/.tecli.yml`
- Environment variables for sensitive data
- API endpoints and authentication settings
- Google Earth Engine integration settings

## Common Development Tasks

### Adding a New Command
1. Create implementation in `tecli/new_command.py`
2. Add static method to `Commands` class in `tecli/commands.py`
3. Add command to Fire CLI in `tecli/__init__.py` if needed
4. Write tests in `tests/test_commands.py`
5. Update documentation

### Modifying Existing Commands
1. Locate implementation file (e.g., `tecli/start.py`)
2. Make minimal changes preserving existing functionality
3. Update corresponding method in `Commands` class if needed
4. Add/update tests
5. Run quality checks

### Adding Dependencies
1. Add to `pyproject.toml` under `[tool.poetry.dependencies]`
2. Run `poetry install` to update lock file
3. Add type stubs to `[tool.poetry.group.dev.dependencies]` if needed

## Error Handling

### Standard Error Pattern
```python
try:
    # Main logic
    result = perform_operation()
    if result:
        print(colored("Success message", "green"))
    else:
        print(colored("Error message", "red"))
except Exception as error:
    logging.error(error)
    # Optionally re-raise or handle gracefully
```

### Logging
- Use Python's `logging` module
- Log errors with `logging.error()`
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)

## Security Considerations

- Never commit API keys or secrets
- Use environment variables for sensitive configuration
- Validate user inputs
- Handle file operations securely

## Performance Guidelines

- Use efficient file operations for large datasets
- Consider memory usage for geospatial data processing
- Cache API responses when appropriate
- Use Docker efficiently (minimize image size, reuse layers)

## Git Workflow

1. Create feature branch: `git checkout -b feature/description`
2. Make changes following these guidelines
3. Run quality checks: `pre-commit run --all-files`
4. Commit with descriptive messages
5. Push and create pull request

## Documentation

- Update README.md if adding new features
- Add docstrings to all new functions
- Update help text for CLI commands
- Document configuration options

## Common Patterns

### File Operations
```python
import os
from pathlib import Path

def safe_file_operation(file_path: str) -> bool:
    """Safely handle file operations."""
    try:
        path = Path(file_path)
        if path.exists():
            # Perform operation
            return True
        return False
    except Exception as error:
        logging.error(f"File operation failed: {error}")
        return False
```

### API Calls
```python
import requests
from typing import Optional, Dict, Any

def api_call(endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Make API call with error handling."""
    try:
        response = requests.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        logging.error(f"API call failed: {error}")
        return None
```

## Debugging Tips

- Use `trends logs` to check execution logs
- Test Docker containers locally before deploying
- Use `trends config show` to verify configuration
- Check file permissions and paths
- Validate JSON payloads before sending

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [trends.earth Platform Documentation](https://trends.earth/docs/)
