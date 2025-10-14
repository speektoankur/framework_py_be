import requests
from typing import Dict, Any, Optional
import json

class UserAPI:
    """API encapsulation layer for User Management endpoints"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            username: Unique username
            email: Valid email address
            password: User password
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users"
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = self.session.post(url, json=payload)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get user details by ID
        
        Args:
            user_id: User ID to retrieve
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users/{user_id}"
        
        response = self.session.get(url)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def update_user_email(self, user_id: int, email: str) -> Dict[str, Any]:
        """
        Update user's email address
        
        Args:
            user_id: User ID to update
            email: New email address
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users/{user_id}"
        payload = {"email": email}
        
        response = self.session.put(url, json=payload)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Delete a user
        
        Args:
            user_id: User ID to delete
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users/{user_id}"
        
        response = self.session.delete(url)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def get_users_list(self, page: int = 1, size: int = 10, keyword: Optional[str] = None) -> Dict[str, Any]:
        """
        Get paginated list of users with optional search
        
        Args:
            page: Page number
            size: Number of items per page
            keyword: Optional search keyword
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users"
        params = {"page": page, "size": size}
        
        if keyword:
            params["keyword"] = keyword
        
        response = self.session.get(url, params=params)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status
        
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/health"
        
        response = self.session.get(url)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
    
    def reset_test_data(self) -> Dict[str, Any]:
        """
        Reset test data to original state
        
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users/reset"
        
        response = self.session.post(url)
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "headers": dict(response.headers)
        }
