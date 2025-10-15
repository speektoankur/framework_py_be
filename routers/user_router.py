from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from models import (
    CreateUserRequest, 
    UpdateUserRequest, 
    ApiResponse, 
    UserListResponse,
    ResponseCode
)
from user_service import user_service

router = APIRouter()

@router.post("/users", response_model=ApiResponse)
async def create_user(user_request: CreateUserRequest):
    """
    Create a new user
    
    - **username**: Unique username for the user
    - **email**: Valid email address
    - **password**: User password
    """
    try:
        user_data = user_service.create_user(
            username=user_request.username,
            email=user_request.email,
            password=user_request.password
        )
        return ApiResponse(
            code=ResponseCode.SUCCESS,
            data=user_data,
            msg="success"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=ResponseCode.BAD_REQUEST,
            detail=ApiResponse(
                code=ResponseCode.BAD_REQUEST,
                data=None,
                msg=str(e)
            ).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

@router.get("/users/{user_id}", response_model=ApiResponse)
async def get_user_details(user_id: int):
    """
    Retrieve details of a specific user
    
    - **user_id**: ID of the user to retrieve
    """
    try:
        user_data = user_service.get_user_by_id(user_id)
        return ApiResponse(
            code=ResponseCode.SUCCESS,
            data=user_data,
            msg="success"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=ResponseCode.NOT_FOUND,
            detail=ApiResponse(
                code=ResponseCode.NOT_FOUND,
                data=None,
                msg=str(e)
            ).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

@router.put("/users/{user_id}", response_model=ApiResponse)
async def update_user_email(user_id: int, user_request: UpdateUserRequest):
    """
    Update a user's email address
    
    - **user_id**: ID of the user to update
    - **email**: New email address
    """
    try:
        if user_request.email is None:
            raise ValueError("Email is required for update")
        
        user_service.update_user_email(user_id, user_request.email)
        return ApiResponse(
            code=ResponseCode.SUCCESS,
            data=None,
            msg="success"
        )
    except ValueError as e:
        # Check if it's a "User not found" error
        if "User not found" in str(e):
            raise HTTPException(
                status_code=ResponseCode.NOT_FOUND,
                detail=ApiResponse(
                    code=ResponseCode.NOT_FOUND,
                    data=None,
                    msg=str(e)
                ).dict()
            )
        else:
            raise HTTPException(
                status_code=ResponseCode.BAD_REQUEST,
                detail=ApiResponse(
                    code=ResponseCode.BAD_REQUEST,
                    data=None,
                    msg=str(e)
                ).dict()
            )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

@router.delete("/users/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: int):
    """
    Delete a specific user
    
    - **user_id**: ID of the user to delete
    """
    try:
        user_service.delete_user(user_id)
        return ApiResponse(
            code=ResponseCode.SUCCESS,
            data=None,
            msg="success"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=ResponseCode.NOT_FOUND,
            detail=ApiResponse(
                code=ResponseCode.NOT_FOUND,
                data=None,
                msg=str(e)
            ).dict()
        )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

@router.get("/users", response_model=UserListResponse)
async def batch_query_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    keyword: Optional[str] = Query(None, description="Search keyword for username or email")
):
    """
    Paginate/filter user list (supports search)
    
    - **page**: Page number (default: 1)
    - **size**: Number of items per page (default: 10, max: 100)
    - **keyword**: Optional search keyword for username or email
    """
    try:
        user_list_data = user_service.get_users_list(page=page, size=size, keyword=keyword)
        return UserListResponse(
            code=ResponseCode.SUCCESS,
            data=user_list_data,
            msg="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

@router.post("/users/reset", response_model=ApiResponse)
async def reset_test_data():
    """
    Reset test data to original state (for testing purposes only)
    """
    try:
        user_service.reset_test_data()
        return ApiResponse(
            code=ResponseCode.SUCCESS,
            data=None,
            msg="Test data reset successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=ResponseCode.INTERNAL_ERROR,
            detail=ApiResponse(
                code=ResponseCode.INTERNAL_ERROR,
                data=None,
                msg="Internal server error"
            ).dict()
        )

