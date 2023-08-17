from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr
from pydantic import Field
from ..model.base import CourseType
from app.schemas.user import UserInfo


class CourseBase(BaseModel):
    id: str
    course_type: Optional[str] = None
    name: str
    description: Optional[str] = None
    banner: Optional[str] = None
    KEY: str
    created_by: str


class CourseCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    KEY: str


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None


class CourseResponse(CourseBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
