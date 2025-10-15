import pytest
import allure
from typing import Dict, Any

from common.data_builder import UserDataBuilder, test_data_manager
from common.models import (
    CreateUserRequestModel,
    UpdateUserRequestModel,
    ApiResponseModel,
    UserListResponseModel,
)
from common.logger import test_logger

@allure.epic("User Management API")
@allure.feature("User CRUD Operations")
class TestUserManagement:
    """Test cases for User Management APIs"""

    @allure.story("Create User")
    @allure.title("Create user with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_valid_data(self, user_api, assertions, valid_user_data):
        """Test creating a user with valid data"""
        test_logger.info("Testing create user with valid data")
        
        # Create user
        request_model = CreateUserRequestModel(**valid_user_data)
        response = user_api.create_user(payload=request_model)
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Create user should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        assertions.assert_response_message(response["response"]["msg"], "success", "Response message should be success")
        
        # Verify user data in response
        # Prefer model when available
        if "response_model" in response:
            model: ApiResponseModel = response["response_model"]
            user_data = model.data  # type: ignore[assignment]
        else:
            user_data = response["response"]["data"]
        assertions.assert_user_data(user_data, ["id", "username"], "User data should contain id and username")
        assertions.assert_field_value(user_data["username"], valid_user_data["username"], "username")
        assertions.assert_not_empty(user_data["id"], "user_id")
        
        # Store created user for cleanup
        test_data_manager.add_created_user(user_data)
        
        test_logger.info(f"User created successfully with ID: {user_data['id']}")

    @allure.story("Create User")
    @allure.title("Create user with invalid data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_data", UserDataBuilder.build_invalid_user_data())
    def test_create_user_invalid_data(self, user_api, assertions, invalid_data):
        """Test creating a user with invalid data"""
        test_logger.info(f"Testing create user with invalid data: {invalid_data}")
        
        # Create user with invalid data
        # For invalid data we bypass local model validation when needed
        response = user_api.create_user(
            username=invalid_data["username"],
            email=invalid_data["email"],
            password=invalid_data["password"],
        )
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 400, "Create user with invalid data should return 400")
        assertions.assert_response_code(response["response"]["code"], 400, "Response code should be 400")
        
        test_logger.info("Invalid user creation properly rejected")

    @allure.story("Create User")
    @allure.title("Create user with duplicate username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_duplicate_username(self, user_api, assertions, existing_user_data):
        """Test creating a user with duplicate username"""
        test_logger.info("Testing create user with duplicate username")
        
        # Create user with existing username
        response = user_api.create_user(
            username=existing_user_data["username"],
            email="newemail@example.com",
            password="password123"
        )
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 400, "Create user with duplicate username should return 400")
        assertions.assert_response_code(response["response"]["code"], 400, "Response code should be 400")
        
        test_logger.info("Duplicate username properly rejected")

    @allure.story("Get User")
    @allure.title("Get user details with valid ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_valid_id(self, user_api, assertions, existing_user_data):
        """Test getting user details with valid ID"""
        test_logger.info(f"Testing get user with valid ID: {existing_user_data['id']}")
        
        # Get user details
        response = user_api.get_user(existing_user_data["id"])
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Get user should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        assertions.assert_response_message(response["response"]["msg"], "success", "Response message should be success")
        
        # Verify user data
        if "response_model" in response:
            model: ApiResponseModel = response["response_model"]
            user_data = model.data  # type: ignore[assignment]
        else:
            user_data = response["response"]["data"]
        assertions.assert_user_data(user_data, ["id", "username", "email"], "User data should contain all fields")
        assertions.assert_field_value(user_data["id"], existing_user_data["id"], "user_id")
        assertions.assert_field_value(user_data["username"], existing_user_data["username"], "username")
        assertions.assert_field_value(user_data["email"], existing_user_data["email"], "email")
        
        test_logger.info("User details retrieved successfully")

    @allure.story("Get User")
    @allure.title("Get user details with invalid ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_invalid_id(self, user_api, assertions):
        """Test getting user details with invalid ID"""
        test_logger.info("Testing get user with invalid ID")
        
        # Get user with non-existent ID
        response = user_api.get_user(99999)
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 404, "Get user with invalid ID should return 404")
        assertions.assert_response_code(response["response"]["code"], 404, "Response code should be 404")
        
        test_logger.info("Invalid user ID properly handled")

    @allure.story("Update User")
    @allure.title("Update user email with valid data")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user_email_valid(self, user_api, assertions, existing_user_data):
        """Test updating user email with valid data"""
        test_logger.info(f"Testing update user email for ID: {existing_user_data['id']}")
        
        # Update user email
        new_email = "updated@example.com"
        update_model = UpdateUserRequestModel(email=new_email)
        response = user_api.update_user_email(existing_user_data["id"], payload=update_model)
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Update user should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        assertions.assert_response_message(response["response"]["msg"], "success", "Response message should be success")
        assertions.assert_field_value(response["response"]["data"], None, "data", "Data should be null for update")
        
        # Verify email was updated by getting user details
        get_response = user_api.get_user(existing_user_data["id"])
        if "response_model" in get_response:
            model = get_response["response_model"]
            updated_user_data = model.data  # type: ignore[assignment]
        else:
            updated_user_data = get_response["response"]["data"]
        assertions.assert_field_value(updated_user_data["email"], new_email, "email", "Email should be updated")
        
        test_logger.info("User email updated successfully")

    @allure.story("Update User")
    @allure.title("Update user email with invalid ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_user_email_invalid_id(self, user_api, assertions):
        """Test updating user email with invalid ID"""
        test_logger.info("Testing update user email with invalid ID")
        
        # Update user with non-existent ID
        response = user_api.update_user_email(99999, "newemail@example.com")
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 404, "Update user with invalid ID should return 404")
        assertions.assert_response_code(response["response"]["code"], 404, "Response code should be 404")
        
        test_logger.info("Invalid user ID for update properly handled")

    @allure.story("Delete User")
    @allure.title("Delete user with valid ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_valid_id(self, user_api, assertions):
        """Test deleting user with valid ID"""
        test_logger.info("Testing delete user with valid ID")
        
        # First create a user to delete
        user_data = UserDataBuilder.build_valid_user()
        create_response = user_api.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        
        user_id = create_response["response"]["data"]["id"]
        test_logger.info(f"Created user with ID {user_id} for deletion test")
        
        # Delete user
        response = user_api.delete_user(user_id)
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Delete user should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        assertions.assert_response_message(response["response"]["msg"], "success", "Response message should be success")
        assertions.assert_field_value(response["response"]["data"], None, "data", "Data should be null for delete")
        
        # Verify user is deleted by trying to get it
        get_response = user_api.get_user(user_id)
        assertions.assert_status_code(get_response["status_code"], 404, "Deleted user should not be found")
        
        test_logger.info("User deleted successfully")

    @allure.story("Delete User")
    @allure.title("Delete user with invalid ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_invalid_id(self, user_api, assertions):
        """Test deleting user with invalid ID"""
        test_logger.info("Testing delete user with invalid ID")
        
        # Delete user with non-existent ID
        response = user_api.delete_user(99999)
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 404, "Delete user with invalid ID should return 404")
        assertions.assert_response_code(response["response"]["code"], 404, "Response code should be 404")
        
        test_logger.info("Invalid user ID for delete properly handled")

    @allure.story("List Users")
    @allure.title("Get users list with default pagination")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_users_list_default(self, user_api, assertions):
        """Test getting users list with default pagination"""
        test_logger.info("Testing get users list with default pagination")
        
        # Get users list
        response = user_api.get_users_list()
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Get users list should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        assertions.assert_response_message(response["response"]["msg"], "success", "Response message should be success")
        
        # Verify list structure
        if "response_model" in response:
            model: UserListResponseModel = response["response_model"]
            list_data = model.data.model_dump()
        else:
            list_data = response["response"]["data"]
        assertions.assert_user_list_structure(list_data, "User list should have proper structure")
        assertions.assert_not_empty(list_data["total"], "total", "Total should not be empty")
        
        test_logger.info("Users list retrieved successfully")

    @allure.story("List Users")
    @allure.title("Get users list with custom pagination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("pagination_data", UserDataBuilder.build_pagination_test_data())
    def test_get_users_list_pagination(self, user_api, assertions, pagination_data):
        """Test getting users list with custom pagination"""
        test_logger.info(f"Testing get users list with pagination: {pagination_data}")
        
        # Get users list with custom pagination
        response = user_api.get_users_list(
            page=pagination_data["page"],
            size=pagination_data["size"]
        )
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Get users list should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        
        # Verify pagination
        if "response_model" in response:
            model: UserListResponseModel = response["response_model"]
            list_data = model.data.model_dump()
        else:
            list_data = response["response"]["data"]
        assertions.assert_user_list_structure(list_data, "User list should have proper structure")
        assertions.assert_pagination(
            list_data["total"],
            pagination_data["page"],
            pagination_data["size"],
            len(list_data["list"]),
            "Pagination should work correctly"
        )
        
        test_logger.info("Users list pagination working correctly")

    @allure.story("List Users")
    @allure.title("Search users with keyword")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("search_data", UserDataBuilder.build_search_test_data())
    def test_search_users(self, user_api, assertions, search_data):
        """Test searching users with keyword"""
        test_logger.info(f"Testing search users with keyword: {search_data['keyword']}")
        
        # Search users
        response = user_api.get_users_list(keyword=search_data["keyword"])
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Search users should return 200")
        assertions.assert_response_code(response["response"]["code"], 200, "Response code should be 200")
        
        # Verify search results
        if "response_model" in response:
            model: UserListResponseModel = response["response_model"]
            list_data = model.data.model_dump()
        else:
            list_data = response["response"]["data"]
        assertions.assert_user_list_structure(list_data, "Search results should have proper structure")
        
        # If we expect results, verify they contain the keyword
        if search_data["expected_results"]:
            for user in list_data["list"]:
                username = user["username"].lower()
                email = user.get("email", "").lower()
                keyword = search_data["keyword"].lower()
                assert keyword in username or keyword in email, f"Search result should contain keyword '{keyword}'"
        
        test_logger.info(f"Search for '{search_data['keyword']}' completed successfully")

    @allure.story("Health Check")
    @allure.title("API health check")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_health_check(self, user_api, assertions):
        """Test API health check"""
        test_logger.info("Testing API health check")
        
        # Perform health check
        response = user_api.health_check()
        
        # Assertions
        assertions.assert_status_code(response["status_code"], 200, "Health check should return 200")
        assertions.assert_field_value(response["response"]["status"], "healthy", "status", "Service should be healthy")
        
        test_logger.info("API health check passed")
