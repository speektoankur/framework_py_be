# User Management API - Backend Testing Framework

A comprehensive FastAPI backend service with an advanced testing framework designed to demonstrate modern API testing practices, automation, and reporting capabilities.

## 🎯 Project Overview

This project showcases a complete **Backend Testing Framework** implementation featuring:
- **FastAPI Backend Service** with User Management APIs
- **Comprehensive Test Framework** with pytest and Allure reporting
- **Environment-based Testing** (localhost/release configurations)
- **API Automation** with custom assertions and data builders
- **Advanced Reporting** with interactive HTML reports

## High Level Flow Visualization 
<img width="1273" height="294" alt="Screenshot 2025-10-15 at 11 05 30 PM" src="https://github.com/user-attachments/assets/59735d20-ecf0-420f-8964-4866b300be5f" />

## Test Report View
<img width="1498" height="787" alt="Screenshot 2025-10-15 at 11 12 00 PM" src="https://github.com/user-attachments/assets/af517641-c73c-434c-9239-1bad47e035c2" />
<img width="755" height="393" alt="Screenshot 2025-10-15 at 11 13 10 PM" src="https://github.com/user-attachments/assets/76142038-59ac-41bb-b33b-ff8fddd1fda2" />

## 🏗️ Project Architecture

```
framework_py_be/
├── 📁 Backend Service (FastAPI)
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py              # Pydantic models for request/response
│   ├── user_service.py        # Business logic and dummy data
│   ├── routers/
│   │   ├── __init__.py
│   │   └── user_router.py     # User API endpoints
│   └── requirements.txt       # Backend dependencies
│
├── 📁 Test Framework (pytest + Allure)
│   ├── api/                   # API encapsulation layer
│   │   └── user_api.py        # User API client
│   ├── common/                # Common utilities
│   │   ├── assertions.py      # Custom assertions
│   │   ├── config_reader.py   # Configuration management
│   │   ├── data_builder.py    # Test data builders
│   │   └── logger.py          # Test logging
│   ├── config/                # Environment configurations
│   │   ├── localhost.json     # Local development config
│   │   └── release.json       # Production config
│   ├── testcases/             # Test cases
│   │   └── test_user_management.py  # User API tests
│   ├── reports/               # Test reports
│   │   ├── allure-results/    # Allure raw results
│   │   ├── allure-report/     # Generated Allure reports
│   │   └── pytest_report.html # Pytest HTML report
│   ├── conftest.py           # Pytest fixtures
│   ├── pytest.ini           # Pytest configuration
│   ├── allure_config.py     # Allure configuration
│   ├── run_tests.py         # Test runner script
│   ├── requirements.txt     # Test dependencies
│   └── README.md           # Test framework documentation
│
└── README.md               # This unified documentation
```

## 🚀 Quick Start Guide

### 1. Setup Backend Service

```bash
# Navigate to project directory
cd /Users/ankur/Documents/framework_py_be

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start the API server
python3 main.py
```

**API Access:**
- Base URL: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Setup Test Framework

```bash
# Install test dependencies
pip install -r test/requirements.txt

# Install Allure (optional, for advanced reporting)
# macOS: brew install allure
# Linux/Windows: Download from https://github.com/allure-framework/allure2/releases
```

### 3. Run Tests

```bash
# Run all tests against localhost
python3 test/run_tests.py --env=localhost

# Run tests against release environment
python3 test/run_tests.py --env=release

# Run only smoke tests
python3 test/run_tests.py --type=smoke

# Run without Allure report generation
python3 test/run_tests.py --no-report

# List available environments
python3 test/run_tests.py --list-envs
```

## 📊 API Endpoints & Testing Coverage

| Method | Endpoint | Description | Test Coverage |
|--------|----------|-------------|---------------|
| POST | `/api/v1/users` | Create a new user | ✅ Valid data, ❌ Invalid data, ❌ Duplicates |
| GET | `/api/v1/users/{user_id}` | Get user details | ✅ Valid ID, ❌ Invalid ID |
| PUT | `/api/v1/users/{user_id}` | Update user email | ✅ Valid update, ❌ Invalid ID |
| DELETE | `/api/v1/users/{user_id}` | Delete user | ✅ Valid deletion, ❌ Invalid ID |
| GET | `/api/v1/users` | List users (paginated) | ✅ Pagination, ✅ Search, ✅ Structure |

### Response Format
```json
{
  "code": 200,
  "data": {...},
  "msg": "success"
}
```

## 🧪 Test Framework Features

### **1. Environment Management**
- **Localhost Environment**: `http://localhost:8000` with test data
- **Release Environment**: `https://api.example.com` with production config
- **JSON-based Configuration**: Easy environment switching via CLI
- **Flexible Settings**: Timeout, retry, and test data configurations

### **2. Test Categories & Markers**
- **Smoke Tests**: Critical functionality (`@pytest.mark.smoke`)
- **Regression Tests**: Full feature coverage (`@pytest.mark.regression`)
- **API Tests**: API-specific tests (`@pytest.mark.api`)
- **Severity Levels**: Critical, Normal, Minor, Trivial

### **3. Advanced Test Utilities**
- **Custom Assertions**: Specialized API testing assertions
- **Data Builders**: Dynamic test data generation
- **Test Logger**: File and console logging with timestamps
- **Config Reader**: Environment-specific configuration management

### **4. Comprehensive Test Cases**
- **24 Test Methods** covering all API endpoints
- **Positive & Negative Scenarios** with proper validation
- **Parameterized Tests** for data-driven testing
- **Allure Integration** with proper decorators and severity levels

## 📈 Test Reports & Analytics

### **Allure Reports** (Interactive)
- **Location**: `test/reports/allure-report/index.html`
- **Features**: 
  - Interactive test results with trends
  - Environment information and build details
  - Test categorization by severity and features
  - Detailed test steps and attachments
  - Historical test execution data

### **Pytest HTML Reports** (Simple)
- **Location**: `test/reports/pytest_report.html`
- **Features**: Clean HTML report with test results summary

### **Test Logs** (Detailed)
- **Location**: `test/logs/`
- **Features**: Detailed execution logs with timestamps and context

## 🔧 Test Framework Configuration

### Environment Configuration Example
```json
{
  "environment": "localhost",
  "base_url": "http://localhost:8000",
  "timeout": 30,
  "retry_count": 3,
  "test_data": {
    "valid_users": [...],
    "existing_users": [...],
    "pagination": {...}
  }
}
```

### Test Data Management
- **Valid User Data**: For positive test scenarios
- **Invalid User Data**: For negative test scenarios  
- **Existing User Data**: For tests using pre-existing data
- **Pagination Data**: For pagination testing
- **Search Data**: For search functionality testing

## 🎯 Testing Framework Demonstration

### **1. API Automation**
```python
# Example test case
def test_create_user_valid_data(self, user_api, assertions, valid_user_data):
    response = user_api.create_user(
        username=valid_user_data["username"],
        email=valid_user_data["email"],
        password=valid_user_data["password"]
    )
    
    assertions.assert_status_code(response["status_code"], 200)
    assertions.assert_response_code(response["response"]["code"], 200)
    assertions.assert_user_data(response["response"]["data"], ["id", "username"])
```

### **2. Environment Flexibility**
```bash
# Switch between environments seamlessly
python3 test/run_tests.py --env=localhost    # Local testing
python3 test/run_tests.py --env=release      # Production testing
```

### **3. Advanced Reporting**
- **Allure Integration**: Rich interactive reports
- **Test Categorization**: By severity, features, and stories
- **Environment Tracking**: Build and environment information
- **Historical Analysis**: Test execution trends

## 🛠️ Customization & Extension

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
```python
@staticmethod
def assert_custom_field(actual, expected, message=""):
    """Custom assertion method"""
    with allure.step(f"Verify custom field: {actual} == {expected}"):
        assert actual == expected, f"Custom assertion failed: {message}"
```

## 📝 Best Practices Demonstrated

1. **Test Isolation**: Each test is independent with proper setup/teardown
2. **Data Management**: Centralized test data with builders and cleanup
3. **Environment Flexibility**: Easy switching between test environments
4. **Comprehensive Reporting**: Multiple report formats for different needs
5. **API Encapsulation**: Clean separation between test logic and API calls
6. **Configuration Management**: Environment-specific settings
7. **Logging & Debugging**: Detailed logging for troubleshooting

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

## 🎉 Framework Benefits

### **For Developers**
- **Rapid Test Development**: Pre-built utilities and fixtures
- **Environment Flexibility**: Easy switching between environments
- **Rich Reporting**: Multiple report formats for different stakeholders
- **Maintainable Code**: Clean architecture and separation of concerns

### **For QA Teams**
- **Comprehensive Coverage**: All API endpoints with positive/negative scenarios
- **Data-Driven Testing**: Parameterized tests with various data sets
- **Visual Reports**: Interactive Allure reports for analysis
- **CI/CD Ready**: Designed for continuous integration

### **For Stakeholders**
- **Test Visibility**: Clear reports showing test coverage and results
- **Environment Tracking**: Know which environment was tested
- **Historical Data**: Track test execution trends over time
- **Quality Metrics**: Understand API quality and stability

## 🚀 Next Steps

1. **Run the Tests**: Execute the test suite to see the framework in action
2. **Explore Reports**: Check out the Allure and HTML reports
3. **Customize**: Add your own test cases and environments
4. **Integrate**: Use in CI/CD pipelines for automated testing
5. **Extend**: Add more API endpoints and test scenarios

---

**This project demonstrates a production-ready testing framework that can be used as a template for testing any REST API service. The combination of FastAPI backend and comprehensive test automation provides a complete solution for API testing and validation.**

