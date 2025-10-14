# User Management API Test Framework

A comprehensive test framework for the User Management FastAPI backend service using pytest and Allure reporting.

## 🏗️ Test Framework Structure

```
test/
├── api/                    # API encapsulation layer
│   ├── __init__.py
│   └── user_api.py        # User API client
├── common/                # Common utilities
│   ├── __init__.py
│   ├── assertions.py      # Custom assertions
│   ├── config_reader.py   # Configuration management
│   ├── data_builder.py    # Test data builders
│   └── logger.py          # Test logging
├── config/                # Environment configurations
│   ├── localhost.json     # Local development config
│   └── release.json       # Production config
├── testcases/             # Test cases
│   ├── __init__.py
│   └── test_user_management.py  # User API tests
├── reports/               # Test reports
│   ├── allure-results/    # Allure raw results
│   ├── allure-report/     # Generated Allure reports
│   └── pytest_report.html # Pytest HTML report
├── logs/                  # Test execution logs
├── conftest.py           # Pytest fixtures
├── pytest.ini           # Pytest configuration
├── allure_config.py     # Allure configuration
├── run_tests.py         # Test runner script
├── requirements.txt     # Test dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -r test/requirements.txt

# Install Allure (optional, for report generation)
# macOS
brew install allure

# Linux
# Download from https://github.com/allure-framework/allure2/releases

# Windows
# Download from https://github.com/allure-framework/allure2/releases
```

### 2. Start the API Server

```bash
# In the project root directory
python main.py
```

### 3. Run Tests

```bash
# Run all tests against localhost
python test/run_tests.py

# Run tests against release environment
python test/run_tests.py --env=release

# Run only smoke tests
python test/run_tests.py --type=smoke

# Run tests without generating Allure report
python test/run_tests.py --no-report

# List available environments
python test/run_tests.py --list-envs
```

### 4. Alternative: Direct pytest

```bash
# Run all tests
pytest test/testcases/ --env=localhost

# Run specific test file
pytest test/testcases/test_user_management.py --env=localhost

# Run with specific markers
pytest test/testcases/ -m smoke --env=localhost

# Run with verbose output
pytest test/testcases/ -v --env=localhost
```

## 📊 Test Reports

### Allure Reports
- **Location**: `test/reports/allure-report/index.html`
- **Features**: Interactive test results, trends, categories, environment info
- **Generate**: Automatically generated after test execution
- **View**: Open `index.html` in browser or use `allure open test/reports/allure-report`

### Pytest HTML Reports
- **Location**: `test/reports/pytest_report.html`
- **Features**: Simple HTML report with test results
- **Generate**: Automatically generated after test execution

### Test Logs
- **Location**: `test/logs/`
- **Features**: Detailed execution logs with timestamps
- **Format**: Both console and file logging

## 🎯 Test Categories

### Test Types
- **Smoke Tests**: Critical functionality tests (`@pytest.mark.smoke`)
- **Regression Tests**: Full feature tests (`@pytest.mark.regression`)
- **API Tests**: API-specific tests (`@pytest.mark.api`)

### Test Severity (Allure)
- **Critical**: Core functionality tests
- **Normal**: Standard feature tests
- **Minor**: Edge case tests
- **Trivial**: Non-critical tests

## 🔧 Configuration

### Environment Configuration

#### Localhost Environment (`test/config/localhost.json`)
```json
{
  "environment": "localhost",
  "base_url": "http://localhost:8000",
  "timeout": 30,
  "retry_count": 3,
  "test_data": {
    "valid_users": [...],
    "existing_users": [...]
  }
}
```

#### Release Environment (`test/config/release.json`)
```json
{
  "environment": "release",
  "base_url": "https://api.example.com",
  "timeout": 60,
  "retry_count": 5,
  "test_data": {...}
}
```

### Test Data Management

The framework includes comprehensive test data builders:

- **Valid User Data**: For positive test scenarios
- **Invalid User Data**: For negative test scenarios
- **Existing User Data**: For tests using pre-existing data
- **Pagination Data**: For pagination testing
- **Search Data**: For search functionality testing

## 🧪 Test Cases Coverage

### User Management API Tests

1. **Create User**
   - ✅ Valid user creation
   - ✅ Invalid data validation
   - ✅ Duplicate username handling
   - ✅ Duplicate email handling

2. **Get User**
   - ✅ Valid user retrieval
   - ✅ Invalid user ID handling
   - ✅ User data validation

3. **Update User**
   - ✅ Valid email update
   - ✅ Invalid user ID handling
   - ✅ Update verification

4. **Delete User**
   - ✅ Valid user deletion
   - ✅ Invalid user ID handling
   - ✅ Deletion verification

5. **List Users**
   - ✅ Default pagination
   - ✅ Custom pagination
   - ✅ Search functionality
   - ✅ Response structure validation

6. **Health Check**
   - ✅ API health verification

## 🛠️ Customization

### Adding New Test Cases

1. Create test methods in `test/testcases/test_user_management.py`
2. Use appropriate Allure decorators for reporting
3. Use fixtures from `conftest.py` for setup
4. Use assertions from `test/common/assertions.py`

### Adding New Environments

1. Create new JSON config file in `test/config/`
2. Follow the same structure as existing configs
3. Use `--env=<new_env>` to run tests

### Custom Assertions

Add new assertion methods in `test/common/assertions.py`:

```python
@staticmethod
def assert_custom_field(actual, expected, message=""):
    """Custom assertion method"""
    with allure.step(f"Verify custom field: {actual} == {expected}"):
        assert actual == expected, f"Custom assertion failed: {message}"
```

## 📝 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Data Cleanup**: Use fixtures for setup/teardown
3. **Descriptive Names**: Use clear, descriptive test names
4. **Allure Integration**: Use Allure decorators for better reporting
5. **Environment Flexibility**: Use configuration files for different environments
6. **Logging**: Use the test logger for debugging information
7. **Assertions**: Use custom assertions for consistent error messages

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Connection Errors**: Verify API server is running
3. **Allure Report Issues**: Check if Allure is properly installed
4. **Environment Config**: Verify JSON config files are valid

### Debug Mode

```bash
# Run with debug logging
pytest test/testcases/ -v -s --log-cli-level=DEBUG

# Run single test with debug
pytest test/testcases/test_user_management.py::TestUserManagement::test_create_user_valid_data -v -s
```

## 📈 Continuous Integration

The test framework is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run API Tests
  run: |
    python test/run_tests.py --env=localhost --type=regression
    
- name: Generate Allure Report
  run: |
    allure generate test/reports/allure-results -o test/reports/allure-report
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add appropriate test coverage
3. Update documentation
4. Use consistent naming conventions
5. Add Allure decorators for new tests

