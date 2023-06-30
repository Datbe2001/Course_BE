from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

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
    is_activate: Optional[bool] = True
    system_role: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreateParams(BaseModel):
    email: str
    username: str
    password: str
    password_confirm: str

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
    hashed_password: str

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

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class UserResponse(UserBase):

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: int(v.timestamp())
        }
