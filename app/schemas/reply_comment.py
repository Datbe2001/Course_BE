from datetime import datetime
from typing import Optional

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
