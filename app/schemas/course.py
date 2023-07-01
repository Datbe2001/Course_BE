from enum import Enum

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr
from pydantic import Field
from ..model.base import CourseType


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
    banner: Optional[str] = None
    KEY: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    banner: Optional[str] = None
