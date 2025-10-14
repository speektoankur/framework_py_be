import pytest
import os
import sys
from typing import Generator, Dict, Any

# Add test directory to Python path
test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, test_dir)

from api.user_api import UserAPI
from common.config_reader import config_reader
from common.logger import test_logger
from common.data_builder import test_data_manager
from common.assertions import TestAssertions

@pytest.fixture(scope="session")
def environment(request) -> str:
    """
    Get environment from command line or default to localhost
    
    Usage: pytest --env=release
    """
    return request.config.getoption("--env", default="localhost")

@pytest.fixture(scope="session")
def config(environment: str) -> Dict[str, Any]:
    """
    Load configuration for the specified environment
    
    Args:
        environment: Environment name (localhost/release)
        
    Returns:
        Configuration dictionary
    """
    test_logger.info(f"Loading configuration for environment: {environment}")
    return config_reader.load_config(environment)

@pytest.fixture(scope="session")
def base_url(config: Dict[str, Any]) -> str:
    """
    Get base URL from configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Base URL string
    """
    url = config.get("base_url", "")
    test_logger.info(f"Using base URL: {url}")
    return url

@pytest.fixture(scope="session")
def user_api(base_url: str) -> UserAPI:
    """
    Create UserAPI instance with base URL
    
    Args:
        base_url: Base URL for API calls
        
    Returns:
        UserAPI instance
    """
    test_logger.info("Creating UserAPI instance")
    return UserAPI(base_url)

@pytest.fixture(scope="session")
def test_data(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get test data from configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Test data dictionary
    """
    return config.get("test_data", {})

@pytest.fixture(scope="function")
def assertions() -> TestAssertions:
    """
    Create TestAssertions instance
    
    Returns:
        TestAssertions instance
    """
    return TestAssertions()

@pytest.fixture(scope="function", autouse=True)
def setup_test_data(user_api):
    """
    Setup test data before each test and cleanup after
    
    This fixture runs before and after each test function
    """
    # Reset test data before each test
    try:
        user_api.reset_test_data()
        test_logger.info("Test data reset completed")
    except Exception as e:
        test_logger.warning(f"Could not reset test data: {e}")
    
    # Setup before test
    test_data_manager.clear_created_users()
    test_logger.info("Test data setup completed")
    
    yield
    
    # Cleanup after test
    test_logger.info("Test data cleanup completed")

@pytest.fixture(scope="function")
def health_check(user_api: UserAPI, assertions: TestAssertions):
    """
    Perform health check before running tests
    
    Args:
        user_api: UserAPI instance
        assertions: TestAssertions instance
    """
    test_logger.info("Performing health check")
    response = user_api.health_check()
    
    assertions.assert_status_code(response["status_code"], 200, "Health check should return 200")
    assertions.assert_response_code(response["response"].get("status"), "healthy", "Service should be healthy")
    
    test_logger.info("Health check passed")
    return response

@pytest.fixture(scope="function")
def existing_user_data(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get existing user data for testing
    
    Args:
        test_data: Test data from configuration
        
    Returns:
        Existing user data
    """
    existing_users = test_data.get("existing_users", [])
    if existing_users:
        return existing_users[0]  # Return first existing user
    return {}

@pytest.fixture(scope="function")
def valid_user_data(test_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Get valid user data for testing
    
    Args:
        test_data: Test data from configuration
        
    Returns:
        Valid user data
    """
    valid_users = test_data.get("valid_users", [])
    if valid_users:
        return valid_users[0]  # Return first valid user
    return {}

@pytest.fixture(scope="function")
def invalid_user_data(test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get invalid user data for negative testing
    
    Args:
        test_data: Test data from configuration
        
    Returns:
        Invalid user data
    """
    invalid_users = test_data.get("invalid_users", [])
    if invalid_users:
        return invalid_users[0]  # Return first invalid user
    return {}

def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--env",
        action="store",
        default="localhost",
        help="Environment to run tests against (localhost/release)"
    )

def pytest_configure(config):
    """Configure pytest with custom settings"""
    # Set test session name
    env = config.getoption("--env", default="localhost")
    if hasattr(config, '_metadata'):
        config._metadata["Environment"] = env
        config._metadata["Test Framework"] = "pytest + Allure"

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    env = config.getoption("--env", default="localhost")
    
    # Add environment marker to all tests
    for item in items:
        item.add_marker(pytest.mark.env(env))
