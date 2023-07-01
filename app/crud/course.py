import logging
import uuid

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import Course

from ..schemas import CourseCreate, CourseUpdate, CourseType, CourseCreateParams


logger = logging.getLogger(__name__)

class CRUDCourse(CRUDBase[Course, CourseCreate, CourseUpdate]):
    @staticmethod
    def get_course_by_id(db: Session, course_id: str) -> Optional[Course]:
        current_course = db.query(Course).get(course_id)
        return current_course
    
    @staticmethod
    def get_course_by_KEY(db: Session, KEY: str) -> Optional[Course]:
        current_course = db.query(Course).filter(Course.KEY == KEY).first()
        return current_course
    
    @staticmethod
    def list_course(db: Session, skip: int, limit: int) -> Optional[Course]:
        db_query = db.query(Course)
        total_course = db_query.offset(skip).limit(limit).count()
        list_course = db_query.all()

        result = {
            "total_course": total_course,
            "list_course": list_course
        }
        return result
    
    def create_course(self, db: Session, course_create: Dict):
        current_course = Course(**course_create.dict())
        db.add(current_course)
        db.commit()
        db.refresh(current_course)
        return current_course

crud_course = CRUDCourse(Course)
