# Test Suite

Comprehensive test suite for the Personal Portfolio application.

## Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_runner.py           # Simple test runner script
├── unit/                    # Unit tests
│   ├── test_main.py        # FastAPI endpoint tests
│   ├── test_config.py      # Configuration tests
│   ├── test_local_data.py  # Local data management tests
│   └── test_services.py    # Service layer tests
├── integration/            # Integration tests
│   └── test_app_integration.py # Full application workflow tests
└── fixtures/               # Test data and utilities
    └── sample_data.py      # Sample data for tests

```

## Running Tests

### Quick Start
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_main.py

# Run with verbose output
pytest -v

# Using the test runner script
python tests/test_runner.py
```

### Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only  
pytest tests/integration/

# Run tests by marker
pytest -m "not slow"          # Skip slow tests
pytest -m integration         # Only integration tests
pytest -m unit               # Only unit tests
```

### Development Workflow
```bash
# Run tests with file watching (if pytest-watch is installed)
ptw

# Run specific test method
pytest tests/unit/test_main.py::TestMainEndpoints::test_home_endpoint

# Run tests with debugger on failure
pytest --pdb

# Generate coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Test Coverage

The test suite covers:

- ✅ **FastAPI Endpoints** - All HTTP endpoints with various scenarios
- ✅ **Service Layer** - GitHub, Email, and PDF services with mocking
- ✅ **Configuration** - Settings loading and validation
- ✅ **Data Management** - Local file operations (JSON loading/saving)
- ✅ **Integration Workflows** - Complete user journeys
- ✅ **Error Handling** - Exception scenarios and fallbacks
- ✅ **HTMX Endpoints** - Dynamic content loading

## Test Configuration

Tests are configured in `pyproject.toml` with:

- **Coverage target**: 80% minimum
- **Async support**: Automatic async test detection
- **Markers**: Unit, integration, slow test categorization
- **Output**: Terminal and HTML coverage reports
- **Warnings**: Filtered to reduce noise

## Fixtures

Key test fixtures available:

- `client` - FastAPI test client
- `mock_settings` - Test configuration
- `temp_data_dir` - Temporary directory for file operations
- `mock_github_response` - GitHub API mock data
- `mock_smtp_server` - Email service mock
- `sample_contact_data` - Contact form test data

## Mocking Strategy

- **External APIs**: GitHub API calls are mocked
- **Email Service**: SMTP operations are mocked
- **PDF Generation**: WeasyPrint operations are mocked
- **File System**: Temporary directories for file tests
- **Configuration**: Override settings for test isolation

## CI/CD Integration

The test suite is integrated with GitHub Actions:

- Runs on every pull request
- Includes code quality checks (black, isort, flake8, mypy)
- Generates test coverage reports
- Fails build if coverage drops below 80%

## Adding New Tests

1. **Unit Tests**: Add to appropriate file in `tests/unit/`
2. **Integration Tests**: Add to `tests/integration/test_app_integration.py`
3. **New Fixtures**: Add to `tests/conftest.py`
4. **Sample Data**: Add to `tests/fixtures/sample_data.py`

Follow the existing patterns and naming conventions for consistency.
