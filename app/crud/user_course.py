import logging
import uuid

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import UserCourse
from ..model.base import CourseRole

from ..schemas import UserCourseCreate, UserCourseUpdate


logger = logging.getLogger(__name__)


class CRUDUserCourse(CRUDBase[UserCourse, UserCourseCreate, UserCourseUpdate]):

    def get_by_course_id_user_id(self, db: Session, *, user_id: str, course_id: str):
        user_course = db.query(UserCourse).filter(UserCourse.user_id == user_id,
                                                  UserCourse.course_id == course_id).first()
        return user_course

    def create_user_course(self, db: Session, user_course_create: Dict):
        current_user_course = UserCourse(**user_course_create.dict())
        db.add(current_user_course)
        db.commit()
        db.refresh(current_user_course)
        return current_user_course
    
    def invite_or_join_to_user_course(self, db: Session, user_id: str, course_id: str, course_role: CourseRole):
        current_user_course = UserCourse(
            id = str(uuid.uuid4()),
            user_id = user_id,
            course_id=course_id,
            course_role=course_role
        )
        db.add(current_user_course)
        db.commit()
        db.refresh(current_user_course)
        return current_user_course

crud_user_course = CRUDUserCourse(UserCourse)
