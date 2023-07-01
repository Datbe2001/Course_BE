from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object

from ...schemas.course import CourseCreateParams
from ...model.base import CourseType
from ...model import User
from ...services import CourseService


router = APIRouter()

@router.post("/course/create")
async def create_course(course_type: CourseType,
                        course_create: CourseCreateParams,
                        user: User = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    
    course_service = CourseService(db=db)

    user_response = await course_service.create_course(user_id=user.id,
                                                       course_type=course_type,
                                                       course_create=course_create)
    return make_response_object(user_response)
