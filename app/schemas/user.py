from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserBase(BaseModel):
    email: Optional[str] = None
    username: str
    # password: Optional[str] = None
    # address: Optional[str] = None
    # avatar: Optional[str] = None
    # is_activate: Optional[bool] = True
    # sex: Optional[str] = None
    # fullname: Optional[str] = None
    # birthday: Optional[date] = None
    # description: Optional[str] = None

    class Config:
        orm_mode = True

class UserCreateParams(BaseModel):
    email: str
    username: str
    password: str
    password_confirm: str

class UserCreate(BaseModel):
    id: str
    email: str
    username: str
    hashed_password: str


class UserUpdate(BaseModel):
    id: Optional[str] = None
    address: Optional[str] = None
    avatar: Optional[str] = None
    is_activate: Optional[bool] = True
    sex: Optional[str] = None
    fullname: Optional[str] = None
    birthday: Optional[date] = None
    description: Optional[str] = None
    image_cover: Optional[str] = None
    time_create: Optional[datetime] = None


class User(UserBase):
    id: str

    class Config:
        orm_mode = True
