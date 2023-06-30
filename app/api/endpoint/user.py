from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.depend import oauth2
from app.db.database import get_db
from app.model import User
from app.services.user import UserService
from ...schemas import UserCreate, UserCreateParams

route = APIRouter()

@route.post("/user/register")
async def create_user(create_user: UserCreateParams, db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    user_response = await user_service.create_user(create_user=create_user)
    return user_response
