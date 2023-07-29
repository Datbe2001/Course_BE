import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.depend import oauth2
from app.api.depend.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.model import User
from app.services.user import UserService
from app.utils.response import make_response_object
from ...schemas import UserCreate, UserCreateParams, UserUpdateParams, LoginUser, ChangePassword
from ...model.base import UserSystemRole

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/user/list")
async def list_users(skip = 0,
                    limit = 10,
                    user: User = Depends(oauth2.admin),
                    db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    user_response = await user_service.list_users(skip=skip, limit=limit)
    return make_response_object(user_response)


@router.get("/user/me")
async def read_me(user: User = Depends(oauth2.get_current_user),
                db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    user_response = await user_service.get_user_by_id(user_id=user.id)
    return make_response_object(user_response)


@router.post("/auth/register")
async def create_user(create_user: UserCreateParams,
                       db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    user_response = await user_service.create_user(create_user=create_user)
    return make_response_object(user_response)


@router.post("/auth/login")
async def login(login_request: LoginUser,
                db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    current_user = await user_service.login(login_request=login_request)

    created_access_token = create_access_token(data={"uid": current_user.id})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id})
    return make_response_object(data=dict(access_token=created_access_token,
                                              refresh_token=created_refresh_token))

@router.post("/auth/refresh")
async def refresh_token(decoded_refresh_token=Depends(verify_refresh_token),
                        db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    current_user = await user_service.get_user_by_id(decoded_refresh_token['uid'])

    if not current_user:
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

    created_access_token = create_access_token(data={"uid": current_user.id})
    created_refresh_token = create_refresh_token(data={"uid": current_user.id})

    return make_response_object(data=dict(access_token=created_access_token,
                                          refresh_token=created_refresh_token))


@router.post("/auth/reset_password")
async def change_password(
        request: ChangePassword,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)
):
    user_service = UserService(db=db)
    logger.info("Endpoint_user: change_password called")

    user_response = await user_service.change_password(current_user=user, obj_in=request)
    logger.info("Endpoint_user: change_password called successfully")
    return make_response_object(user_response)


@router.put("/user/update_me")
async def update_profile(update_user: UserUpdateParams,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    user_service = UserService(db=db)
    user_response = await user_service.update_profile(user_id=user.id, update_user=update_user)
    return make_response_object(user_response)


@router.put("/user/{user_id}/role")
async def update_user_role(
        user_role: UserSystemRole,
        user_id: str,
        user: User = Depends(oauth2.admin),
        db: Session = Depends(get_db)):
    
    user_service = UserService(db=db)

    user_response = await user_service.update_user_role(user_id=user_id, user_role=user_role)
    return make_response_object(user_response)


@router.put("/auth/verify_code")
async def verify_code(
        email: str,
        verify_code: str,
        new_password: str,
        password_confirm: str,
        db: Session = Depends(get_db)):
    
    user_service = UserService(db=db)

    user_response = await user_service.verify_code(email=email,
                                                   verify_code=verify_code, 
                                                   new_password=new_password, 
                                                   password_confirm=password_confirm)

    return make_response_object(user_response)


@router.put("/auth/forget_password")
async def forget_password(
        email: str,
        db: Session = Depends(get_db)):

    user_service = UserService(db=db)

    user_response = await user_service.get_verification_code(email=email, action="forget_password")
    logger.info("Endpoint_user: get_verification_code called successfully")
    return make_response_object(user_response)
