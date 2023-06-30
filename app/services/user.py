import uuid
from fastapi import HTTPException

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.untils import hash_lib

from ..model import User
from ..schemas import UserCreate, UserCreateParams
from ..crud.user import crud_user

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_user(self, create_user: UserCreateParams):

        email_lower = create_user.email.lower()
        username_lower = create_user.username.lower()
        current_email = crud_user.get_by_email(db=self.db,email=email_lower)
        if current_email:
            raise ValueError(AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        if create_user.password != create_user.password_confirm:
            raise ValueError(AppStatus.ERROR_REGISTER_NOT_MATCH_PASSWORD)
        
        create_user.password = hash_lib.hash_password(create_user.password)

        result = crud_user.create_user(db=self.db, create_user=UserCreate(
                                                    id=str(uuid.uuid4()),
                                                    username=username_lower,
                                                    email=email_lower,
                                                    hashed_password=create_user.password))
        return result
