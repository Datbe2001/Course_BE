from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr
from pydantic import Field
from ..model.base import CourseRole


class UserCourseBase(BaseModel):
    user_id: str
    course_id: str
    course_role: CourseRole


class UserCourseCreate(UserCourseBase):
    id: str


class UserCourseUpdate(UserCourseBase):
    pass


class UserCourse(UserCourseBase):
    id: str

    class Config:
        orm_mode = True
