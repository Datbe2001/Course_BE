from fastapi import APIRouter

from app.api.endpoint import user
from app.api.endpoint import course

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(course.router, tags=["courses"])
