import allure
from typing import Any, Dict, List, Optional
from .logger import test_logger

class TestAssertions:
    """Custom assertions for API testing"""
    
    @staticmethod
    def assert_status_code(actual: int, expected: int, message: str = ""):
        """
        Assert HTTP status code
        
        Args:
            actual: Actual status code
            expected: Expected status code
            message: Optional assertion message
        """
        with allure.step(f"Verify status code: {actual} == {expected}"):
            test_logger.info(f"Asserting status code: {actual} == {expected}")
            assert actual == expected, f"Status code mismatch. Expected: {expected}, Actual: {actual}. {message}"
    
    @staticmethod
    def assert_response_code(actual: int, expected: int, message: str = ""):
        """
        Assert API response code (from response body)
        
        Args:
            actual: Actual response code
            expected: Expected response code
            message: Optional assertion message
        """
        with allure.step(f"Verify response code: {actual} == {expected}"):
            test_logger.info(f"Asserting response code: {actual} == {expected}")
            assert actual == expected, f"Response code mismatch. Expected: {expected}, Actual: {actual}. {message}"
    
    @staticmethod
    def assert_response_message(actual: str, expected: str, message: str = ""):
        """
        Assert API response message
        
        Args:
            actual: Actual response message
            expected: Expected response message
            message: Optional assertion message
        """
        with allure.step(f"Verify response message: '{actual}' == '{expected}'"):
            test_logger.info(f"Asserting response message: '{actual}' == '{expected}'")
            assert actual == expected, f"Response message mismatch. Expected: '{expected}', Actual: '{actual}'. {message}"
    
    @staticmethod
    def assert_user_data(user_data: Dict[str, Any], expected_fields: List[str], message: str = ""):
        """
        Assert user data contains expected fields
        
        Args:
            user_data: User data dictionary
            expected_fields: List of expected field names
            message: Optional assertion message
        """
        with allure.step(f"Verify user data contains fields: {expected_fields}"):
            test_logger.info(f"Asserting user data fields: {expected_fields}")
            for field in expected_fields:
                assert field in user_data, f"Missing field '{field}' in user data. {message}"
    
    @staticmethod
    def assert_user_list_structure(user_list_data: Dict[str, Any], message: str = ""):
        """
        Assert user list response structure
        
        Args:
            user_list_data: User list data dictionary
            message: Optional assertion message
        """
        with allure.step("Verify user list response structure"):
            test_logger.info("Asserting user list response structure")
            
            # Check required fields
            required_fields = ["total", "list"]
            for field in required_fields:
                assert field in user_list_data, f"Missing field '{field}' in user list data. {message}"
            
            # Check total is integer
            assert isinstance(user_list_data["total"], int), f"Total should be integer. {message}"
            
            # Check list is array
            assert isinstance(user_list_data["list"], list), f"List should be array. {message}"
    
    @staticmethod
    def assert_pagination(total: int, page: int, size: int, actual_list_length: int, message: str = ""):
        """
        Assert pagination logic
        
        Args:
            total: Total number of items
            page: Current page number
            size: Page size
            actual_list_length: Actual length of returned list
            message: Optional assertion message
        """
        with allure.step(f"Verify pagination: page={page}, size={size}, total={total}"):
            test_logger.info(f"Asserting pagination: page={page}, size={size}, total={total}")
            
            # Calculate expected list length
            start_index = (page - 1) * size
            remaining_items = max(0, total - start_index)
            expected_length = min(size, remaining_items)
            
            assert actual_list_length == expected_length, \
                f"Pagination mismatch. Expected {expected_length} items, got {actual_list_length}. {message}"
    
    @staticmethod
    def assert_field_value(actual: Any, expected: Any, field_name: str, message: str = ""):
        """
        Assert field value
        
        Args:
            actual: Actual value
            expected: Expected value
            field_name: Name of the field being asserted
            message: Optional assertion message
        """
        with allure.step(f"Verify {field_name}: '{actual}' == '{expected}'"):
            test_logger.info(f"Asserting {field_name}: '{actual}' == '{expected}'")
            assert actual == expected, f"{field_name} mismatch. Expected: '{expected}', Actual: '{actual}'. {message}"
    
    @staticmethod
    def assert_not_empty(data: Any, field_name: str, message: str = ""):
        """
        Assert field is not empty
        
        Args:
            data: Data to check
            field_name: Name of the field being asserted
            message: Optional assertion message
        """
        with allure.step(f"Verify {field_name} is not empty"):
            test_logger.info(f"Asserting {field_name} is not empty")
            assert data, f"{field_name} should not be empty. {message}"
    
    @staticmethod
    def assert_contains(data: str, substring: str, field_name: str, message: str = ""):
        """
        Assert string contains substring
        
        Args:
            data: String to search in
            substring: Substring to find
            field_name: Name of the field being asserted
            message: Optional assertion message
        """
        with allure.step(f"Verify {field_name} contains '{substring}'"):
            test_logger.info(f"Asserting {field_name} contains '{substring}'")
            assert substring in data, f"{field_name} should contain '{substring}'. {message}"
