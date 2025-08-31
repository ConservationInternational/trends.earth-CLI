# trends.earth CLI

[![CI](https://github.com/ConservationInternational/trends.earth-CLI/actions/workflows/ci.yaml/badge.svg)](https://github.com/ConservationInternational/trends.earth-CLI/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

The official command-line interface for the trends.earth platform, enabling local development, testing, and deployment of custom geospatial analysis scripts.

## About trends.earth

This project is part of the [trends.earth](https://trends.earth/) ecosystem, a platform for monitoring land change using Earth observation data. The CLI enables researchers and developers to create custom analysis scripts that can be deployed to the trends.earth cloud platform.

### Related Components

- 🌐 [trends.earth API](https://github.com/Vizzuality/trends.earth-API) - Backend API services
- 🏗️ [trends.earth Environment](https://github.com/Vizzuality/trends.earth-Environment) - Core platform infrastructure
- 🖥️ [trends.earth UI](https://github.com/Vizzuality/trends.earth-UI) - Web application interface

## 🚀 Quick Start

### Installation

**Option 1: Using Poetry (Recommended)**
```bash
git clone https://github.com/ConservationInternational/trends.earth-CLI
cd trends.earth-CLI
poetry install
poetry shell
```

> **Note**: After `poetry install`, the `trends` command should be available in the virtual environment.

**Option 2: Using pip with source**
```bash
git clone https://github.com/ConservationInternational/trends.earth-CLI
cd trends.earth-CLI
pip install -e .
```

### Basic Usage

After installation, use the `trends` command:

**If using Poetry:**
```bash
# Method 1: Activate the shell first (recommended)
poetry shell
trends --help
trends create

# Method 2: Use poetry run for each command
poetry run trends --help
poetry run trends create
```

**If using pip installation:**
```bash
# Direct usage (after activating your virtual environment)
trends --help
trends create
```

**Common commands:**
```bash
# Verify installation
trends --help

# Create a new script project
trends create

# Run a script locally
trends start

# Login to trends.earth platform
trends login

# Publish your script to the platform
trends publish
```

## 📋 Requirements

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Poetry** (recommended) - [Install Poetry](https://python-poetry.org/docs/#installation)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **Docker** (for local script execution) - [Install Docker](https://docs.docker.com/get-docker/)

## 🛠️ Development Setup

### Using Poetry (Recommended)

1. **Install Poetry**
   ```bash
   # Install Poetry (if not already installed)
   curl -sSL https://install.python-poetry.org | python3 -
   # Or on Windows:
   # (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/ConservationInternational/trends.earth-CLI
   cd trends.earth-CLI
   ```

3. **Install dependencies and project**
   ```bash
   # Install all dependencies (including dev dependencies)
   # This also installs the project itself in development mode
   poetry install

   # Activate the virtual environment
   poetry shell
   ```

4. **Verify installation**
   ```bash
   # Test the trends command (after poetry shell)
   trends --help

   # Or using poetry run (without shell activation)
   poetry run trends --help

   # Check that the package is installed
   poetry show trends-earth-cli
   ```

5. **Run CLI commands**
   ```bash
   # Using poetry run
   poetry run trends create

   # Or after activating the shell
   trends create
   ```

### From Source (Alternative)

If you prefer not to use Poetry:

1. **Clone the repository**
   ```bash
   git clone https://github.com/ConservationInternational/trends.earth-CLI
   cd trends.earth-CLI
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv

   # Activate the environment
   # On Unix/macOS:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

4. **Verify installation**
   ```bash
   # Test the trends command
   trends --help
   ```

5. **Run CLI commands**
   ```bash
   trends create
   ```

### Configuration

The CLI uses a configuration file located at `~/.tecli.yml`. You can copy the example configuration:

```bash
cp .tecli.yml.example ~/.tecli.yml
```

See [Configuration](#configuration) section for details.

## 🧪 Testing & Development

> **⚠️ Prerequisites**: Before running tests or development tasks, complete the setup steps in [GitHub Copilot Setup Steps](.github/copilot-setup-steps.md) to ensure all dependencies are properly installed.

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=tecli

# Run specific test file
poetry run pytest tests/test_commands.py
```

### Code Quality

```bash
# Run linting and formatting
poetry run ruff check .
poetry run ruff format .

# Run type checking
poetry run mypy tecli/

# Run all quality checks
poetry run pre-commit run --all-files
```

### Development Workflow

1. **Set up development environment**
   
   Follow the complete setup guide in [GitHub Copilot Setup Steps](.github/copilot-setup-steps.md), or run:
   ```bash
   poetry install
   poetry run pre-commit install
   ```

2. **Make changes and test**
   ```bash
   # Run tests
   poetry run pytest

   # Check code quality
   poetry run ruff check .
   poetry run mypy tecli/
   ```

3. **Build package locally**
   ```bash
   poetry build
   ```

For detailed development guidance and coding standards, see [GitHub Copilot Instructions](.github/copilot-instructions.md).

## 📖 Commands Reference

### Project Management

#### `trends create`
Creates a new script project with the basic structure.

```bash
trends create
# You'll be prompted to enter a project name
```

This creates:
- `configuration.json` - Project metadata
- `requirements.txt` - Python dependencies
- `src/main.py` - Main script file
- `src/__init__.py` - Python package initialization

#### `trends start [options]`
Runs your script locally in a Docker container.

```bash
trends start                          # Run with no parameters
trends start --queryParams "param=value&param2=value2"  # With query parameters
trends start --payload payload.json  # With JSON payload file
```

**Options:**
- `queryParams` - URL-encoded query parameters
- `payload` - Path to JSON file containing input parameters

### Authentication & Publishing

#### `trends login`
Authenticate with the trends.earth platform.

```bash
trends login
# You'll be prompted for email and password
```

#### `trends publish [options]`
Deploy your script to the trends.earth platform.

```bash
trends publish                    # Private script
trends publish --public=True     # Public script
trends publish --overwrite=True  # Overwrite existing script
```

**Options:**
- `public` - Make script publicly accessible (default: False)
- `overwrite` - Overwrite existing script without confirmation (default: False)

### Monitoring & Information

#### `trends info`
Display information about the current script project.

```bash
trends info
```

Shows:
- Script ID and name
- Publication status
- Creation date
- API endpoint URL

#### `trends logs [options]`
View build and execution logs for your script.

```bash
trends logs              # Show logs from last hour
trends logs --since=24   # Show logs from last 24 hours
```

**Options:**
- `since` - Hours of logs to display (default: 1)

#### `trends download <script_id>`
Download an existing script from the platform.

```bash
trends download abc123
# Downloads script to ./abc123/ directory
```

### Configuration Management

#### `trends config <action> <variable> [value]`
Manage CLI configuration settings.

```bash
# Set configuration values
trends config set EE_SERVICE_ACCOUNT your-service-account
trends config set EE_PRIVATE_KEY your-base64-encoded-key
trends config set url_api https://api.trends.earth

# View current values
trends config show EE_SERVICE_ACCOUNT
trends config show url_api

# Remove configuration
trends config unset EE_SERVICE_ACCOUNT
```

**Common Variables:**
- `EE_SERVICE_ACCOUNT` - Google Earth Engine service account email
- `EE_PRIVATE_KEY` - Base64-encoded GEE private key
- `EE_SERVICE_ACCOUNT_JSON` - Complete GEE service account JSON
- `url_api` - trends.earth API endpoint (default: https://api.trends.earth)
- `ROLLBAR_SCRIPT_TOKEN` - Error tracking token

#### Encoding GEE Private Key
```bash
# Convert PEM key to base64 (required format)
cat privatekey.pem | base64
```

### Maintenance

#### `trends clear`
Remove temporary Docker images created during local development.

```bash
trends clear
```

## ⚙️ Configuration

The CLI stores configuration in `~/.tecli.yml`. Copy the example configuration:

```bash
cp .tecli.yml.example ~/.tecli.yml
```

### Configuration File Structure

```yaml
# API Configuration
url_api: "https://api.trends.earth"

# Authentication (set via 'trends login' or manually)
JWT: "your-jwt-token-here"
email: "your-email@example.com"
password: "your-password"  # Optional, will be prompted if not set

# Google Earth Engine Configuration
EE_SERVICE_ACCOUNT: "your-service-account@project.iam.gserviceaccount.com"
EE_PRIVATE_KEY: "base64-encoded-private-key"
EE_SERVICE_ACCOUNT_JSON: "complete-service-account-json"

# Error Tracking
ROLLBAR_SCRIPT_TOKEN: "your-rollbar-token"

# Development Settings
environment: "trends.earth-environment"  # Docker environment
environment_version: "0.1.6"            # Environment version
```

### Environment Variables

You can also use environment variables (they override config file values):

```bash
export TECLI_URL_API="https://api.trends.earth"
export TECLI_EE_SERVICE_ACCOUNT="service-account@project.iam.gserviceaccount.com"
export TECLI_EE_PRIVATE_KEY="base64-encoded-key"
```

## 📁 Project Structure

When you create a new script with `trends create`, you'll get this structure:

```
my-script/
├── configuration.json    # Project metadata
├── requirements.txt     # Python dependencies
└── src/
    ├── __init__.py     # Package initialization
    └── main.py         # Main script logic
```

### Script Template

The main script must implement a `run` function:

```python
def run(params, logger):
    """
    Main script entry point.

    Args:
        params (dict): Input parameters from API call
        logger: Logging instance for output

    Returns:
        Script results (any JSON-serializable object)
    """
    logger.debug(f"Received parameters: {params}")

    # Your analysis logic here
    result = {"status": "success", "data": "analysis results"}

    return result
```

### Google Earth Engine Scripts

For scripts using Google Earth Engine, the template includes a `gee_runner` parameter:

```python
def run(params, logger, gee_runner=None):
    """
    GEE script entry point.

    Args:
        params (dict): Input parameters
        logger: Logging instance
        gee_runner: Function to execute GEE operations
    """

    def my_gee_analysis(param1, param2, logger):
        import ee
        # GEE analysis logic
        return results

    if gee_runner:
        return gee_runner(my_gee_analysis, param1, param2, logger)
    else:
        # Direct execution for local testing
        return my_gee_analysis(param1, param2, logger)
```

## 📚 Examples

The repository includes several example scripts demonstrating different use cases:

### 🔢 NumPy Example (`examples/example_numpy/`)
Basic array operations and custom Python classes.

```bash
cd examples/example_numpy
trends start
```

**Features:**
- Array concatenation
- Custom class definitions
- Basic logging

### 🧠 TensorFlow Example (`examples/example_tensorflow/`)
Machine learning model for MNIST digit recognition.

```bash
cd examples/example_tensorflow
trends start
```

**Features:**
- Neural network training
- MNIST dataset processing
- Model evaluation

### 🌍 Google Earth Engine Examples

#### Basic GEE (`examples/example_gee/`)
Forest change analysis using Hansen Global Forest Change data.

```bash
cd examples/example_gee
trends start --queryParams "thresh=30&begin=2010-01-01&end=2020-12-31"
```

#### GEE with Queue (`examples/example_gee_queue/`)
Advanced GEE processing with queue management.

#### GEE Continuous Integration (`examples/example_gee_ci/`)
NDVI trend analysis with Mann-Kendall statistics.

```bash
cd examples/example_gee_ci
trends start --queryParams "year_start=2003&year_end=2015"
```

## 🐳 Docker Environment

Scripts run in a containerized environment based on the `trends.earth-environment` Docker image. You can customize the environment in your `configuration.json`:

```json
{
  "name": "my-script",
  "environment": "trends.earth-environment",
  "environment_version": "0.1.6"
}
```

### Local Testing vs Production

- **Local**: Docker container with mounted source code
- **Production**: Code uploaded and executed in secure cloud environment

## 🔧 Development Workflow

1. **Create Project**
   ```bash
   trends create
   cd my-new-script
   ```

2. **Install Dependencies**
   Add packages to `requirements.txt`, then test locally:
   ```bash
   echo "numpy>=1.20.0" >> requirements.txt
   trends start
   ```

3. **Develop & Test**
   Edit `src/main.py` and test iterations:
   ```bash
   trends start --queryParams "test=true"
   ```

4. **Configure for Production**
   Set up authentication and publishing:
   ```bash
   trends login
   trends config set EE_SERVICE_ACCOUNT your-account@project.iam.gserviceaccount.com
   ```

5. **Deploy**
   ```bash
   trends publish --public=True
   trends info  # Get API endpoint
   ```

6. **Monitor**
   ```bash
   trends logs --since=24
   ```

## 🚨 Troubleshooting

### Common Issues

**`trends` command not found after installation**
```bash
# Try these solutions:

# 1. Restart your terminal/command prompt

# 2. If using Poetry, make sure you're in the poetry shell
poetry shell
trends --help

# 3. If still not working, try reinstalling with Poetry
poetry install --sync
poetry shell

# 4. Use poetry run as an alternative
poetry run trends --help
poetry run trends create

# 5. Use the module directly as fallback
python -m tecli --help
python -m tecli create

# 6. For development installs with pip, ensure you're in the right environment
# If using virtual environment, make sure it's activated

# 7. Check that the installation completed successfully
poetry show trends-earth-cli  # Should show the package if installed correctly
```

**Docker not found**
```bash
# Install Docker Desktop or Docker Engine
# Verify installation:
docker --version
```

**Permission denied on Docker commands**
```bash
# On Linux, add user to docker group:
sudo usermod -aG docker $USER
# Logout and login again
```

**Google Earth Engine authentication errors**
```bash
# Verify service account setup:
trends config show EE_SERVICE_ACCOUNT
trends config show EE_PRIVATE_KEY

# Re-encode private key:
cat service-account-key.json | base64 -w 0
trends config set EE_SERVICE_ACCOUNT_JSON "base64-encoded-json"
```

**Script execution timeouts**
- Check script efficiency and processing requirements
- Monitor logs with `trends logs`
- Consider breaking large analyses into smaller chunks

**API connection issues**
```bash
# Check API endpoint:
trends config show url_api

# Verify authentication:
trends login
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. **Set up development environment**: Follow [GitHub Copilot Setup Steps](.github/copilot-setup-steps.md) for complete setup instructions
4. Make your changes following [GitHub Copilot Instructions](.github/copilot-instructions.md)
5. Run tests and linting: `poetry run pytest && poetry run ruff check .`
6. Submit a pull request

### Code Style

This project uses [Ruff](https://github.com/astral-sh/ruff) for code formatting and linting, and [mypy](https://mypy.readthedocs.io/) for type checking. Pre-commit hooks are available:

```bash
# Install development dependencies and pre-commit hooks
poetry install
poetry run pre-commit install

# Run quality checks manually
poetry run ruff check .        # Linting
poetry run ruff format .       # Formatting
poetry run mypy tecli/         # Type checking
poetry run pytest             # Tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Conservation International

This project is maintained by [Conservation International](https://www.conservation.org/), a nonprofit environmental organization working to protect nature for the benefit of humanity.

## 📞 Support

- 📖 [Documentation](https://trends.earth/docs/)
- 🐛 [Issues](https://github.com/ConservationInternational/trends.earth-CLI/issues)
- 💬 [Discussions](https://github.com/ConservationInternational/trends.earth-CLI/discussions)
- 📧 Email: [trends.earth@conservation.org](mailto:trends.earth@conservation.org)
```
