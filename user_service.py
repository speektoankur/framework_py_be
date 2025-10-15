from typing import Optional, Dict
from models import User, UserData, UserListData

class UserService:
    def __init__(self):
        # Dummy data storage - in a real application, this would be a database
        self.users: Dict[int, User] = {
            1: User(id=1, username="test", email="t@x.com", password="123456"),
            2: User(id=2, username="john_doe", email="john@example.com", password="password123"),
            3: User(id=3, username="jane_smith", email="jane@example.com", password="securepass"),
            4: User(id=4, username="admin", email="admin@company.com", password="admin123"),
            5: User(id=5, username="demo_user", email="demo@test.com", password="demo123")
        }
        self.next_id = 6

    def create_user(self, username: str, email: str, password: str) -> UserData:
        """Create a new user and return user data without password"""
        # Validate required fields
        if not username or username.strip() == "":
            raise ValueError("Username is required")
        
        if not email or email.strip() == "":
            raise ValueError("Email is required")
            
        if not password or password.strip() == "":
            raise ValueError("Password is required")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Check if username already exists
        for user in self.users.values():
            if user.username == username:
                raise ValueError("Username already exists")
        
        # Check if email already exists
        for user in self.users.values():
            if user.email == email:
                raise ValueError("Email already exists")
        
        new_user = User(
            id=self.next_id,
            username=username,
            email=email,
            password=password
        )
        
        self.users[self.next_id] = new_user
        self.next_id += 1
        
        return UserData(id=new_user.id, username=new_user.username)

    def get_user_by_id(self, user_id: int) -> UserData:
        """Get user details by ID"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        user = self.users[user_id]
        return UserData(id=user.id, username=user.username, email=user.email)

    def update_user_email(self, user_id: int, email: str) -> None:
        """Update user's email address"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        # Check if email already exists for another user
        for uid, user in self.users.items():
            if uid != user_id and user.email == email:
                raise ValueError("Email already exists")
        
        self.users[user_id].email = email

    def delete_user(self, user_id: int) -> None:
        """Delete a user"""
        if user_id not in self.users:
            raise ValueError("User not found")
        
        del self.users[user_id]

    def get_users_list(self, page: int = 1, size: int = 10, keyword: Optional[str] = None) -> UserListData:
        """Get paginated list of users with optional keyword search"""
        all_users = list(self.users.values())
        
        # Filter by keyword if provided
        if keyword:
            keyword_lower = keyword.lower()
            filtered_users = [
                user for user in all_users 
                if keyword_lower in user.username.lower() or keyword_lower in user.email.lower()
            ]
        else:
            filtered_users = all_users
        
        # Calculate pagination
        total = len(filtered_users)
        start_index = (page - 1) * size
        end_index = start_index + size
        
        # Get paginated users
        paginated_users = filtered_users[start_index:end_index]
        
        # Convert to UserData (without password)
        user_data_list = [
            UserData(id=user.id, username=user.username, email=user.email) 
            for user in paginated_users
        ]
        
        return UserListData(total=total, list=user_data_list)

    def reset_test_data(self):
        """Reset test data to original state"""
        self.users = {
            1: User(id=1, username="test", email="t@x.com", password="123456"),
            2: User(id=2, username="john_doe", email="john@example.com", password="password123"),
            3: User(id=3, username="jane_smith", email="jane@example.com", password="securepass"),
            4: User(id=4, username="admin", email="admin@company.com", password="admin123"),
            5: User(id=5, username="demo_user", email="demo@test.com", password="demo123")
        }
        self.next_id = 6

# Global service instance
user_service = UserService()

