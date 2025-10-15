import requests
from typing import Dict, Any, Optional, Union
from pydantic import ValidationError
from common.models import (
    CreateUserRequestModel,
    UpdateUserRequestModel,
    ApiResponseModel,
    UserListResponseModel,
)

class UserAPI:
    """API encapsulation layer for User Management endpoints"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def create_user(self, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, payload: Optional[CreateUserRequestModel] = None) -> Dict[str, Any]:
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
        if payload is None:
            # Build via pydantic for validation on the client side too
            payload = CreateUserRequestModel(username=username or "", email=email or "", password=password or "")
        elif not isinstance(payload, CreateUserRequestModel):
            payload = CreateUserRequestModel(**payload)  # type: ignore[arg-type]
        
        response = self.session.post(url, json=payload.dict())
        parsed: Dict[str, Any] = {
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
        try:
            body = response.json() if response.content else {}
            parsed_model = ApiResponseModel.model_validate(body)
            parsed["response_model"] = parsed_model
            parsed["response"] = body
        except Exception:
            parsed["response"] = {}
        return parsed
    
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
    
    def update_user_email(self, user_id: int, email: Optional[str] = None, payload: Optional[UpdateUserRequestModel] = None) -> Dict[str, Any]:
        """
        Update user's email address
        
        Args:
            user_id: User ID to update
            email: New email address
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/api/v1/users/{user_id}"
        if payload is None:
            payload = UpdateUserRequestModel(email=email or "")
        elif not isinstance(payload, UpdateUserRequestModel):
            payload = UpdateUserRequestModel(**payload)  # type: ignore[arg-type]
        
        response = self.session.put(url, json=payload.model_dump())
        parsed: Dict[str, Any] = {
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
        try:
            body = response.json() if response.content else {}
            parsed_model = ApiResponseModel.model_validate(body)
            parsed["response_model"] = parsed_model
            parsed["response"] = body
        except Exception:
            parsed["response"] = {}
        return parsed
    
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
        parsed: Dict[str, Any] = {
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
        try:
            body = response.json() if response.content else {}
            parsed_model = ApiResponseModel.model_validate(body)
            parsed["response_model"] = parsed_model
            parsed["response"] = body
        except Exception:
            parsed["response"] = {}
        return parsed
    
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
        parsed: Dict[str, Any] = {
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
        try:
            body = response.json() if response.content else {}
            parsed_model = UserListResponseModel.model_validate(body)
            parsed["response_model"] = parsed_model
            parsed["response"] = body
        except Exception:
            parsed["response"] = {}
        return parsed
    
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
