import uuid
from fastapi import HTTPException

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler

from ..model import User
from ..schemas import UserCreate, UserCreateParams, UserUpdateParams, LoginUser, UserResponse
from ..crud.user import crud_user

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, user_id: str):
        current_user = crud_user.get_user_by_id(db=self.db,user_id=user_id)
        return UserResponse.from_orm(current_user)
    
    async def list_users(self, skip: int, limit: int):
        result = crud_user.list_users(db=self.db,skip=skip, limit=limit)
        return result


    async def create_user(self, create_user: UserCreateParams):

        email_lower = create_user.email.lower()
        username_lower = create_user.username.lower()
        current_email = crud_user.get_by_email(db=self.db,email=email_lower)
        if current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        
        if len(create_user.password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)
        
        if create_user.password != create_user.password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONFIRM_PASSWORD_DOES_NOT_MATCH)
        
        
        create_user.password = hash_lib.hash_password(create_user.password)

        result = crud_user.create_user(db=self.db, create_user=UserCreate(
                                                    id=str(uuid.uuid4()),
                                                    username=username_lower,
                                                    email=email_lower,
                                                    hashed_password=create_user.password))
        return UserResponse.from_orm(result)
    
    async def login(self, login_request: LoginUser):
        email_lower = login_request.email.lower()
        current_user = crud_user.get_by_email(db=self.db, email=email_lower)

        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        
        if not hash_lib.verify_password(login_request.password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)
        
        return UserResponse.from_orm(current_user)
    

    async def update_profile(self, user_id: str, update_user: UserUpdateParams):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        result = crud_user.update_user(db=self.db, current_user=current_user, update_user=update_user)
        return UserResponse.from_orm(result)


    async def update_user_role(self, user_id: str, user_role: str):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        result = crud_user.update_user_role(self.db, current_user=current_user, user_role=user_role)
        return UserResponse.from_orm(result)
