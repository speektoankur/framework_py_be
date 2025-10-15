from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr


class CreateUserRequestModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class UpdateUserRequestModel(BaseModel):
    email: EmailStr


class UserDataModel(BaseModel):
    id: int
    username: str
    email: Optional[str] = None


class UserListDataModel(BaseModel):
    total: int
    list: List[UserDataModel]


class ApiResponseModel(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str


class UserListResponseModel(BaseModel):
    code: int
    data: UserListDataModel
    msg: str


