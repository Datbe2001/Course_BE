import uuid
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import User
from ..schemas import CourseType, CourseCreate, CourseUpdate, UserCourseCreate
from ..crud import crud_course, crud_user_course
from ..model.base import CourseRole

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    async def get_course_by_id(self, course_id):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_EXIST)
        
        return current_course
    

    async def list_course(self, skip: int, limit: int):
        result = crud_course.list_course(db=self.db, skip=skip, limit=limit)
        return result


    async def create_course(self, user_id: str, course_type: CourseType, course_create: CourseCreate):
        course_KEY = crud_course.get_course_by_KEY(db=self.db, KEY=course_create.KEY)
        if course_KEY:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_KEY_CONFLICT)
        
        current_course = crud_course.create_course(db=self.db, course_create=CourseCreate(
                                                    id=str(uuid.uuid4()),
                                                    name=course_create.name,
                                                    description=course_create.description,
                                                    banner=course_create.banner,
                                                    KEY=course_create.KEY,
                                                    course_type=course_type,
                                                    created_by=user_id))
        
        crud_user_course.create_user_course(db=self.db,
                                            user_course_create=UserCourseCreate(id=str(uuid.uuid4()),
                                                                                user_id=user_id,
                                                                                course_id=current_course.id,
                                                                                course_role=CourseRole.OWNER))
        
        return current_course


    async def has_course_permissions(self, user_id: str, course_id: str):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_EXIST)
        elif current_course.created_by != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)


    async def update_course(self, course_id: str, course_update: CourseUpdate):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_EXIST)
        
        result = crud_course.update_course(db=self.db, current_course=current_course, course_update=course_update)
        return result


    async def delete_course(self, course_id: str):
            current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
            if not current_course:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_EXIST)
            
            result = crud_course.delete_course(db=self.db, current_course=current_course)
            return result
