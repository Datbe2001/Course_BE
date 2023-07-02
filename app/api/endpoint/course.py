from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object

from ...schemas.course import CourseCreateParams, CourseUpdate
from ...model.base import CourseType
from ...model import User
from ...services import CourseService


router = APIRouter()

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
                        course_create: CourseCreateParams,
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    course_response = await course_service.create_course(user_id=user.id,
                                                       course_type=course_type,
                                                       course_create=course_create)
    db.refresh(course_response)
    return make_response_object(course_response)


@router.put("/course/update/{course_id}")
async def update_course(course_id: str,
                        course_update: CourseUpdate,
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    # authorization
    await course_service.has_course_permissions(user_id=user.id, course_id=course_id)

    course_response = await course_service.update_course(course_id=course_id,
                                                         course_update=course_update)
    return make_response_object(course_response)


@router.delete("/course/delete/{course_id}")
async def delete_course(course_id: str,
                        user: User = Depends(oauth2.user_manager),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    # authorization
    await course_service.has_course_permissions(user_id=user.id, course_id=course_id)

    course_response = await course_service.delete_course(course_id=course_id)
    return make_response_object(course_response)
