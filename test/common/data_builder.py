import random
import string
from typing import Dict, Any, List, Optional
from datetime import datetime

class UserDataBuilder:
    """Data builder for creating test user data"""
    
    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """Generate random string of specified length"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    @staticmethod
    def generate_email(domain: str = "example.com") -> str:
        """Generate random email address"""
        username = UserDataBuilder.generate_random_string(6)
        return f"{username}@{domain}"
    
    @staticmethod
    def build_valid_user(username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Dict[str, str]:
        """
        Build valid user data
        
        Args:
            username: Optional username, will generate if not provided
            email: Optional email, will generate if not provided
            password: Optional password, will generate if not provided
            
        Returns:
            Dictionary with user data
        """
        return {
            "username": username or f"user_{UserDataBuilder.generate_random_string(6)}",
            "email": email or UserDataBuilder.generate_email(),
            "password": password or f"pass_{UserDataBuilder.generate_random_string(8)}"
        }
    
    @staticmethod
    def build_invalid_user_data() -> List[Dict[str, Any]]:
        """
        Build list of invalid user data for negative testing
        
        Returns:
            List of dictionaries with invalid user data
        """
        return [
            {
                "username": "",
                "email": "valid@example.com",
                "password": "password123",
                "expected_error": "Username is required"
            },
            {
                "username": "validuser",
                "email": "",
                "password": "password123",
                "expected_error": "Email is required"
            },
            {
                "username": "validuser",
                "email": "invalid-email-format",
                "password": "password123",
                "expected_error": "Invalid email format"
            },
            {
                "username": "validuser",
                "email": "valid@example.com",
                "password": "",
                "expected_error": "Password is required"
            },
            {
                "username": "validuser",
                "email": "valid@example.com",
                "password": "123",  # Too short
                "expected_error": "Password too short"
            }
        ]
    
    @staticmethod
    def build_existing_user_data() -> List[Dict[str, Any]]:
        """
        Build list of existing user data (from dummy data)
        
        Returns:
            List of dictionaries with existing user data
        """
        return [
            {
                "id": 1,
                "username": "test",
                "email": "t@x.com"
            },
            {
                "id": 2,
                "username": "john_doe",
                "email": "john@example.com"
            },
            {
                "id": 3,
                "username": "jane_smith",
                "email": "jane@example.com"
            },
            {
                "id": 4,
                "username": "admin",
                "email": "admin@company.com"
            },
            {
                "id": 5,
                "username": "demo_user",
                "email": "demo@test.com"
            }
        ]
    
    @staticmethod
    def build_update_user_data() -> Dict[str, str]:
        """
        Build user update data (email only)
        
        Returns:
            Dictionary with update data
        """
        return {
            "email": UserDataBuilder.generate_email("updated.com")
        }
    
    @staticmethod
    def build_pagination_test_data() -> List[Dict[str, Any]]:
        """
        Build pagination test data
        
        Returns:
            List of pagination test scenarios
        """
        return [
            {
                "page": 1,
                "size": 5,
                "expected_max_items": 5
            },
            {
                "page": 2,
                "size": 3,
                "expected_max_items": 3
            },
            {
                "page": 1,
                "size": 10,
                "expected_max_items": 10
            },
            {
                "page": 1,
                "size": 100,
                "expected_max_items": 100
            }
        ]
    
    @staticmethod
    def build_search_test_data() -> List[Dict[str, Any]]:
        """
        Build search test data
        
        Returns:
            List of search test scenarios
        """
        return [
            {
                "keyword": "test",
                "expected_results": ["test"]
            },
            {
                "keyword": "john",
                "expected_results": ["john_doe"]
            },
            {
                "keyword": "admin",
                "expected_results": ["admin"]
            },
            {
                "keyword": "nonexistent",
                "expected_results": []
            },
            {
                "keyword": "example.com",
                "expected_results": ["john@example.com", "jane@example.com"]
            }
        ]
    
    @staticmethod
    def build_duplicate_user_data() -> Dict[str, Any]:
        """
        Build duplicate user data for testing duplicate username/email scenarios
        
        Returns:
            Dictionary with duplicate user data
        """
        return {
            "username": "test",  # Existing username
            "email": "duplicate@example.com",
            "password": "password123",
            "expected_error": "Username already exists"
        }
    
    @staticmethod
    def build_duplicate_email_data() -> Dict[str, Any]:
        """
        Build duplicate email data for testing duplicate email scenarios
        
        Returns:
            Dictionary with duplicate email data
        """
        return {
            "username": "newuser",
            "email": "t@x.com",  # Existing email
            "password": "password123",
            "expected_error": "Email already exists"
        }

class TestDataManager:
    """Manager for test data operations"""
    
    def __init__(self):
        self.created_users: List[Dict[str, Any]] = []
        self.test_start_time = datetime.now()
    
    def add_created_user(self, user_data: Dict[str, Any]):
        """Add user to created users list for cleanup"""
        self.created_users.append(user_data)
    
    def get_created_users(self) -> List[Dict[str, Any]]:
        """Get list of created users"""
        return self.created_users
    
    def clear_created_users(self):
        """Clear created users list"""
        self.created_users.clear()
    
    def get_test_run_id(self) -> str:
        """Get unique test run ID"""
        return self.test_start_time.strftime("%Y%m%d_%H%M%S")

# Global test data manager instance
test_data_manager = TestDataManager()

