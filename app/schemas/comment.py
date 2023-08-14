from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from app.schemas.user import UserInfo


class CommentBase(BaseModel):
    content: str
    lesson_id: str
    user_id: str


class CommentCreateParams(BaseModel):
    content: str
    lesson_id: str


class CommentCreate(CommentBase):
    id: str


class CommentUpdateParams(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    id: str


class CommentResponse(CommentBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
