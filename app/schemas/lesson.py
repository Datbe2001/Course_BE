from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class LessonBase(BaseModel):
    name: str
    description: Optional[str] = None
    video_id: str
    course_id: str


class LessonCreateParams(LessonBase):
    pass


class LessonCreate(LessonBase):
    id: str


class LessonUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    video_id: str


class Lesson(LessonBase):
    id: str

    class Config:
        orm_mode = True