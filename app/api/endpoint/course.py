from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object
import cloudinary
import cloudinary.uploader
from app.core.settings import settings

from ...schemas.course import CourseCreateParams, CourseUpdate
from ...model.base import CourseType, CourseRole
from ...model import User
from ...services import CourseService


router = APIRouter()

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
    )

@router.get("/course/list")
async def list_course(user: User = Depends(oauth2.get_current_user),
                      db: Session = Depends(get_db),
                      skip=0,
                      limit=10):
    
    course_service = CourseService(db=db)

    course_response = await course_service.list_course(skip=skip, limit=limit)
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

    course_create = CourseCreateParams(name=name, KEY=KEY, description=description)

    course_response = await course_service.create_course(user_id=user.id, 
                                                        course_type=course_type,
                                                        course_create=course_create,
                                                        banner=banner)
    db.refresh(course_response)
    return make_response_object(course_response)


@router.put("/course/update/{course_id}")
async def update_course(course_id: str,
                        name: str=None,
                        description: str=None,
                        banner: UploadFile = File(None),
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    # authorization
    user_course = await course_service.has_course_permissions(user_id=user.id, course_id=course_id)
    course_update = CourseUpdate(name=name, description=description)

    course_response = await course_service.update_course(course_id=course_id,
                                                         course_update=course_update,
                                                         banner=banner,
                                                         user_course=user_course.course_role)
    return make_response_object(course_response)


@router.delete("/course/{course_id}/delete")
async def delete_course(course_id: str,
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    # authorization
    user_course = await course_service.has_course_permissions(user_id=user.id, course_id=course_id)

    course_response = await course_service.delete_course(course_id=course_id, user_course=user_course.course_role)
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
