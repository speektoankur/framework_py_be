from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from enum import Enum

class ResponseCode(int, Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

# Request Models
class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None

# Response Models
class UserData(BaseModel):
    id: int
    username: str
    email: str

class UserListData(BaseModel):
    total: int
    list: List[UserData]

class ApiResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str

class UserListResponse(BaseModel):
    code: int
    data: UserListData
    msg: str

# Internal User Model (for service layer)
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

