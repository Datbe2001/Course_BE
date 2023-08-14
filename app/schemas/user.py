from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, constr
from pydantic import Field


class UserBase(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    full_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    is_active: Union[bool, None] = None
    system_role: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreateParams(BaseModel):
    email: str
    username: str


class UserUpdateParams(BaseModel):
    username: Optional[str] = None
    avatar: Optional[str] = None
    full_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None


class UserCreate(BaseModel):
    id: str
    email: str
    username: str


class UserUpdate(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    full_name: Optional[str] = None
    birthday: Optional[date] = None
    phone: Optional[str] = None
    is_activate: Optional[bool] = True


class LoginUser(BaseModel):
    email: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str


class UserInfo(BaseModel):
    id: str
    avatar: Optional[str] = None
    username: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class UserResponse(UserBase):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: int(v.timestamp())
        }
