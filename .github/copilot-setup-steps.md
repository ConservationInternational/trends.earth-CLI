# GitHub Copilot Setup Steps for trends.earth CLI

This document provides step-by-step instructions for setting up the development environment for the trends.earth CLI project. Follow these steps before starting development or when GitHub Copilot requests setup guidance.

## Prerequisites

- Python 3.9 or higher
- Git
- Docker (for running and testing scripts locally)

## Development Environment Setup

### Option 1: Using Poetry (Recommended)

1. **Install Poetry** (if not already installed)
   ```bash
   # Linux/macOS
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Windows PowerShell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   
   # Add Poetry to PATH and restart terminal
   ```

2. **Clone and setup the repository**
   ```bash
   git clone https://github.com/ConservationInternational/trends.earth-CLI
   cd trends.earth-CLI
   ```

3. **Install all dependencies** (including development dependencies)
   ```bash
   # Install the package and all dependencies in development mode
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

4. **Install pre-commit hooks**
   ```bash
   poetry run pre-commit install
   ```

5. **Verify installation**
   ```bash
   # Test the CLI command
   trends --help
   
   # Or using poetry run (without shell activation)
   poetry run trends --help
   
   # Check that the package is properly installed
   poetry show trends-earth-cli
   ```

### Option 2: Using pip (Alternative)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ConservationInternational/trends.earth-CLI
   cd trends.earth-CLI
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in development mode**
   ```bash
   pip install -e .
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov ruff mypy types-PyYAML types-requests types-python-dateutil types-pytz pre-commit
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Configuration Setup

1. **Copy example configuration**
   ```bash
   cp .tecli.yml.example ~/.tecli.yml
   ```

2. **Edit configuration** (optional for local development)
   ```bash
   # Edit ~/.tecli.yml with your preferred editor
   nano ~/.tecli.yml
   ```

## Verification Steps

Run these commands to verify your setup is working:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=tecli

# Run linting
ruff check .

# Run type checking
mypy tecli/

# Run code formatting
ruff format .

# Run all quality checks
pre-commit run --all-files

# Test CLI functionality
trends --help
trends create  # Optional: test project creation
```

## Docker Setup

For running and testing scripts locally, ensure Docker is installed and running:

```bash
# Verify Docker installation
docker --version

# Test Docker is working
docker run hello-world
```

## Troubleshooting

### Command not found errors
- Make sure you've activated the virtual environment (`poetry shell` or `source venv/bin/activate`)
- Use `poetry run trends` if not in shell
- Try `python -m tecli` as fallback

### Permission errors with Docker
```bash
# On Linux, add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

### Dependencies not installing
- Update pip: `pip install --upgrade pip`
- Clear pip cache: `pip cache purge`
- For Poetry: `poetry cache clear --all pypi`

## IDE Integration

### VS Code
- Install Python extension
- Install GitHub Copilot extension
- Open project folder in VS Code
- Select correct Python interpreter (Poetry venv or created venv)

### PyCharm
- Open project folder
- Configure Python interpreter to use Poetry venv or created venv
- Enable GitHub Copilot plugin

## Next Steps

After setup completion:
1. Read [Copilot Instructions](./.github/copilot-instructions.md) for development guidance
2. Review [Contributing Guidelines](../CONTRIBUTING.md) if available
3. Check [README.md](../README.md) for project overview and usage