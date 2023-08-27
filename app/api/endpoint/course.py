import uuid
from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object
import cloudinary.uploader
from app.core.settings import settings
from ...constant.template import NotificationTemplate

from ...schemas.course import CourseCreateParams, CourseUpdate
from ...model.base import CourseType, CourseRole, NotificationType
from ...model import User, Course
from ...services import CourseService, NotificationService

router = APIRouter()

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)


@router.get("/course/list")
async def list_course(
        # user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    course_service = CourseService(db=db)

    course_response = await course_service.list_course(skip=skip, limit=limit)
    return make_response_object(course_response)


@router.get("/course/me")
async def get_course_by_me(skip=0, limit=10,
                           user: User = Depends(oauth2.user_manager),
                           db: Session = Depends(get_db)):
    course_service = CourseService(db=db)

    course_response = await course_service.get_course_by_me(user_id=user.id, skip=skip, limit=limit)
    return make_response_object(course_response)


@router.get("/course/{course_id}")
async def get_course_by_id(course_id: str,
                           user: User = Depends(oauth2.get_current_user),
                           db: Session = Depends(get_db)):
    course_service = CourseService(db=db)

    course_response = await course_service.get_course_by_id(course_id=course_id)
    return make_response_object(course_response)


@router.post("/course/create")
async def create_course(course_type: CourseType,
                        name: str,
                        KEY: str,
                        description: str = None,
                        banner: UploadFile = File(...),
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)
    notification_service = NotificationService(db=db)

    course_create = CourseCreateParams(name=name, KEY=KEY, description=description)

    course_response = await course_service.create_course(user_id=user.id,
                                                         course_type=course_type,
                                                         course_create=course_create,
                                                         banner=banner)
    message_template = NotificationTemplate.CRUD_COURSE_NOTIFICATION_MSG
    await notification_service.notify_entity_status(entity=course_response,
                                                    notification_type=NotificationType.COURSE_NOTIFICATION,
                                                    message_template=message_template, action="created",
                                                    current_user=user)

    db.refresh(course_response)
    return make_response_object(course_response)


@router.post("/course/{course_id}/invite")
async def invite_participant_to_course(
        course_id: str,
        course_role: CourseRole,
        user_id: str,
        user: User = Depends(oauth2.user_manager),
        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)

    # authorization
    user_course = await course_service.has_course_permissions(user_id=user.id, course_id=course_id)
    course_response = await course_service.invite_participant_to_course(course_id=course_id,
                                                                        course_role=course_role,
                                                                        user_id=user_id,
                                                                        user_course_role=user_course.course_role)

    return make_response_object(course_response)


@router.post("/course/{course_id}/join")
async def join_to_course(
        course_id: str,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)
    course_response = await course_service.join_to_course(user_id=user.id, course_id=course_id)

    return make_response_object(course_response)


@router.put("/course/update/{course_id}")
async def update_course(course_id: str,
                        name: str = None,
                        description: str = None,
                        banner: UploadFile = File(None),
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)
    notification_service = NotificationService(db=db)

    # authorization
    user_course = await course_service.has_course_permissions(user_id=user.id, course_id=course_id)
    course_update = CourseUpdate(name=name, description=description)

    course_response = await course_service.update_course(course_id=course_id,
                                                         course_update=course_update,
                                                         banner=banner,
                                                         user_course=user_course.course_role)
    message_template = NotificationTemplate.CRUD_COURSE_NOTIFICATION_MSG
    await notification_service.notify_entity_status(entity=course_response,
                                                    notification_type=NotificationType.COURSE_NOTIFICATION,
                                                    message_template=message_template, action="updated",
                                                    current_user=user)
    db.refresh(course_response)
    return make_response_object(course_response)


@router.delete("/course/{course_id}/delete")
async def delete_course(course_id: str,
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)
    notification_service = NotificationService(db=db)

    # authorization
    user_course = await course_service.has_course_permissions(user_id=user.id, course_id=course_id)

    course_response = await course_service.delete_course(course_id=course_id, user_course=user_course.course_role)
    message_template = NotificationTemplate.CRUD_COURSE_NOTIFICATION_MSG
    await notification_service.notify_entity_status(entity=course_response,
                                                    notification_type=NotificationType.COURSE_NOTIFICATION,
                                                    message_template=message_template, action="deleted",
                                                    current_user=user)
    return make_response_object(course_response)


# test update
@router.put("/course/test/{course_id}")
async def delete_course(course_id: str,
                        name: str,
                        description: str,
                        db: Session = Depends(get_db)):
    course_service = CourseService(db=db)
    current_course = await course_service.get_course_by_id(course_id=course_id)
    current_course.name = name
    current_course.description = description
    result = db.add(current_course)
    db.commit()

    # authorization

    return make_response_object(result)


# test create
@router.post("/course/test/create")
async def create_course(course_type: CourseType,
                        name: str,
                        KEY: str,
                        user_id: str,
                        description: str = None,
                        db: Session = Depends(get_db)):
    course_create = Course(id=str(uuid.uuid4()), course_type=course_type, name=name, KEY=KEY, description=description,
                           created_by=user_id)
    db.add(course_create)
    db.commit()
    return course_create
