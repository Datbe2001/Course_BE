import uuid
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import Lesson
from ..schemas import LessonCreate, LessonUpdate, LessonCreateParams
from ..crud import crud_lesson, crud_course
from ..model.base import CourseRole

class LessonService:

    def __init__(self, db: Session):
        self.db = db


    async def get_lesson_by_id(self, lesson_id):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)
        
        return current_lesson


    async def list_lesson(self, skip: int, limit: int):
        result = crud_lesson.list_lesson(db=self.db, skip=skip, limit=limit)
        return result


    async def create_lesson(self, lesson_create: LessonCreateParams):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=lesson_create.course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        
        current_lesson = crud_lesson.create_lesson(db=self.db, lesson_create=LessonCreate(
                                                    id=str(uuid.uuid4()),
                                                    name=lesson_create.name,
                                                    description=lesson_create.description,
                                                    video_id=lesson_create.video_id,
                                                    course_id=lesson_create.course_id))
        return current_lesson


    async def update_lesson(self, lesson_id: str, lesson_update: LessonUpdate):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)
        
        result = crud_lesson.update_lesson(db=self.db, current_lesson=current_lesson, lesson_update=lesson_update)
        return result

    async def delete_lesson(self, lesson_id: str):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)
        
        result = crud_lesson.delete_lesson(db=self.db, current_lesson=current_lesson)
        return result
