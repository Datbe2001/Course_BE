import uuid
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import User
from ..schemas import CourseType, CourseCreate
from ..crud import crud_course

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    async def create_course(self, user_id: str, course_type: CourseType, course_create: CourseCreate):
        course_KEY = crud_course.get_course_by_KEY(db=self.db, KEY=course_create.KEY)
        if course_KEY:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PROJECT_KEY_CONFLICT)
        
        current_course = crud_course.create_course(db=self.db, course_create=CourseCreate(
                                                    id=str(uuid.uuid4()),
                                                    name=course_create.name,
                                                    description=course_create.description,
                                                    banner=course_create.banner,
                                                    KEY=course_create.KEY,
                                                    course_type=course_type,
                                                    created_by=user_id))
        
        return current_course
