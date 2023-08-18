from fastapi import UploadFile

from sqlalchemy import Integer, func
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

import cloudinary
from cloudinary.uploader import upload

from ..model import Lesson
from ..schemas import LessonCreate, LessonUpdate, LessonCreateParams
from ..crud import crud_lesson, crud_course, crud_user_course
from ..model.base import CourseRole


class LessonService:

    def __init__(self, db: Session):
        self.db = db

    async def get_lesson_by_id(self, lesson_id):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)

        return current_lesson

    async def list_lesson(self, course_id: str, skip: int, limit: int):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)

        result = crud_lesson.list_lesson(db=self.db, course_id=current_course.id, skip=skip, limit=limit)
        return result

    async def has_lesson_permission(self, user_id: str, lesson_id: str):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)
        current_user_course = await self.has_course_permission(user_id=user_id, course_id=current_lesson.course_id)
        return current_user_course

    async def has_course_permission(self, user_id: str, course_id: str):
        current_course = crud_course.get_course_by_id(db=self.db, course_id=course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)
        current_user_course = crud_user_course.get_by_course_id_user_id(db=self.db, user_id=user_id,
                                                                        course_id=course_id)
        if not current_user_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_NOT_JOINED_TO_COURSE)

        return current_user_course

    async def create_lesson(self, lesson_create: LessonCreateParams,
                            video_id: str, video_url: UploadFile,
                            user_course_role: CourseRole):
        if not video_id and not video_url or (video_id and video_url):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_VIDEO_INPUT)

        current_course = crud_course.get_course_by_id(db=self.db, course_id=lesson_create.course_id)
        if not current_course:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_NOT_FOUND)

        if user_course_role != CourseRole.OWNER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)

        if video_url:
            try:
                upload_result = cloudinary.uploader.upload(video_url.file, resource_type='video', folder="video")
                video_url = upload_result['url']
            except Exception as error:
                raise error_exception_handler(error=error, app_status=AppStatus.ERROR_BAD_REQUEST)

        last_lesson_id = self.db.query(Lesson.id).filter(Lesson.id.like(f"{current_course.KEY}-%")).order_by(
            func.substr(Lesson.id, func.char_length(current_course.KEY) + 2).cast(Integer).desc()).first()
        if last_lesson_id:
            last_lesson_number = int(last_lesson_id[0].split('-')[1])
        else:
            last_lesson_number = 0
        new_lesson_number = last_lesson_number + 1
        new_lesson_id = f"{current_course.KEY}-{new_lesson_number}"

        current_lesson = crud_lesson.create_lesson(db=self.db, lesson_create=LessonCreate(
            id=new_lesson_id,
            name=lesson_create.name,
            description=lesson_create.description,
            video_id=video_id,
            video_url=video_url,
            course_id=lesson_create.course_id))
        return current_lesson

    async def update_lesson(self, user_course_role: CourseRole, lesson_id: str, lesson_update: LessonUpdate):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)

        if user_course_role != CourseRole.OWNER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)

        result = crud_lesson.update_lesson(db=self.db, current_lesson=current_lesson, lesson_update=lesson_update)
        return result

    async def delete_lesson(self, lesson_id: str, user_course_role: CourseRole):
        current_lesson = crud_lesson.get_lesson_by_id(db=self.db, lesson_id=lesson_id)
        if not current_lesson:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LESSON_NOT_FOUND)

        if user_course_role != CourseRole.OWNER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COURSE_METHOD_NOT_ALLOWED)

        result = crud_lesson.delete_lesson(db=self.db, current_lesson=current_lesson)
        return result
