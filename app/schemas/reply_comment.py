from datetime import datetime
from typing import Optional
from app.schemas.user import UserInfo

from pydantic import BaseModel


class ReplyCommentBase(BaseModel):
    content: str
    user_id: str
    comment_id: str


class ReplyCommentCreateParams(BaseModel):
    comment_id: str
    content: str


class ReplyCommentCreate(ReplyCommentBase):
    id: str


class ReplyCommentUpdateParams(BaseModel):
    content: str


class ReplyCommentUpdate(ReplyCommentBase):
    id: str


class ReplyComment(ReplyCommentBase):
    id: str

    class Config:
        orm_mode = True


class ReplyCommentResponse(ReplyCommentBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
