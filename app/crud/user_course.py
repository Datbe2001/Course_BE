import logging
import uuid

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import UserCourse

from ..schemas import UserCourseCreate, UserCourseUpdate


logger = logging.getLogger(__name__)


class CRUDUserCourse(CRUDBase[UserCourse, UserCourseCreate, UserCourseUpdate]):
    def create_user_course(self, db: Session, user_course_create: Dict):
        current_user_course = UserCourse(**user_course_create.dict())
        db.add(current_user_course)
        db.commit()
        db.refresh(current_user_course)
        return current_user_course

crud_user_course = CRUDUserCourse(UserCourse)
