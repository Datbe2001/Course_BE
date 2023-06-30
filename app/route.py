from fastapi import APIRouter

from app.api.endpoint import user
from app.api.endpoint import course

route = APIRouter()

route.include_router(user.route, tags=["users"])
route.include_router(course.route, tags=["courses"])
