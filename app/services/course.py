import uuid
from fastapi import HTTPException, UploadFile, File

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
import cloudinary
from cloudinary.uploader import upload
from cloudinary import uploader, CloudinaryVideo

from ..model import User
from ..schemas import CourseType, CourseCreate, CourseUpdate, UserCourseCreate
from ..crud import crud_course, crud_user_course, crud_user
from ..model.base import CourseRole
from app.core.settings import settings

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    async def get_course_by_id(self, course_id: str):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        
        return current_course
    
    async def get_course_by_me(self, user_id: str, skip: int, limit: int):
        current_course = crud_course.get_course_by_me(db=self.db, user_id=user_id, skip=skip, limit=limit)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        
        return current_course
    

    async def list_course(self, skip: int, limit: int):
        result = crud_course.list_course(db=self.db, skip=skip, limit=limit)
        return result


    async def create_course(self, user_id: str, course_type: CourseType,
                            course_create: CourseCreate, banner: UploadFile = File(...)):
        course_KEY = crud_course.get_course_by_KEY(db=self.db, KEY=course_create.KEY)
        if course_KEY:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_KEY_CONFLICT)
        
        banner = cloudinary.uploader.upload(banner.file, folder="banner")
        banner_url = banner.get("secure_url")

        current_course = crud_course.create_course(db=self.db, course_create=CourseCreate(
                                                    id=str(uuid.uuid4()),
                                                    name=course_create.name,
                                                    description=course_create.description,
                                                    banner=banner_url,
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
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        user_course = crud_user_course.get_by_course_id_user_id(db=self.db, user_id=user_id, course_id=course_id)
        if not user_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)
        
        return user_course


    async def update_course(self, course_id: str, course_update: CourseUpdate,
                            banner: UploadFile, user_course: CourseRole):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        if user_course != CourseRole.OWNER:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)
        if banner:
            uploaded_banner = upload(banner.file)
            banner_url = uploaded_banner['secure_url']
            course_update.banner = banner_url

        result = crud_course.update_course(db=self.db, current_course=current_course, course_update=course_update)
        return result


    async def invite_participant_to_course(self, course_id: str,
                                            course_role: CourseRole,
                                            user_id: str,
                                            user_course_role: CourseRole):

        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        
        if user_course_role == CourseRole.OWNER:
            if course_role != CourseRole.MEMBER:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)
        
        current_user_course = crud_user_course.get_by_course_id_user_id(db=self.db, user_id=user_id, course_id=course_id)
        if current_user_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ALREADY_JOINED_TO_COURSE)
        else:
            user_course = crud_user_course.invite_or_join_to_user_course(db=self.db, user_id=user_id,
                                                              course_id=course_id,
                                                              course_role=course_role)
            return user_course
        

    async def join_to_course(self, *, user_id: str, course_id: str):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        
        current_user_course = crud_user_course.get_by_course_id_user_id(db=self.db, user_id=user_id, course_id=course_id)
        if current_user_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ALREADY_JOINED_TO_COURSE)
        
        user_course = crud_user_course.invite_or_join_to_user_course(self.db,  user_id=user_id,
                                                       course_id=course_id,
                                                       course_role=CourseRole.MEMBER)
        return user_course


    async def delete_course(self, course_id: str, user_course: CourseRole):
            current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
            if not current_course:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
            if user_course != CourseRole.OWNER:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)
            
            result = crud_course.delete_course(db=self.db, current_course=current_course)
            return result
