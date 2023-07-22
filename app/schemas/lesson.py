from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class LessonBase(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: str
    video_id: Optional[str] = None
    video_url: Optional[str] = None


class LessonCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    course_id: str


class LessonCreate(LessonBase):
    id: str


class LessonUpdate(BaseModel):
    name: str
    description: Optional[str] = None


class Lesson(LessonBase):
    id: str

    class Config:
        orm_mode = True
