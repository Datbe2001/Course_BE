import logging
import uuid

from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import Lesson

from ..schemas import LessonCreate, LessonUpdate


logger = logging.getLogger(__name__)


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):

    @staticmethod
    def get_lesson_by_id(db: Session, lesson_id: str) -> Optional[Lesson]:
        current_lesson = db.query(Lesson).get(lesson_id)
        return current_lesson


    @staticmethod
    def list_lesson(db: Session, skip: int, limit: int) -> Optional[Lesson]:
        db_query = db.query(Lesson)
        total_lesson = db_query.offset(skip).limit(limit).count()
        list_lesson = db_query.all()

        result = {
            "total_lesson": total_lesson,
            "list_lesson": list_lesson
        }
        return result


    def create_lesson(self, db: Session, lesson_create: Dict):
        current_lesson = Lesson(**lesson_create.dict())
        db.add(current_lesson)
        db.commit()
        db.refresh(current_lesson)
        return current_lesson
    

    def update_lesson(self, db: Session, current_lesson: Dict, lesson_update: LessonUpdate):
        result = super().update(db, obj_in=lesson_update, db_obj=current_lesson)
        return result


    def delete_lesson(self, db: Session, current_lesson: Dict):
        db.delete(current_lesson)
        db.commit()
        return current_lesson


crud_lesson = CRUDLesson(Lesson)