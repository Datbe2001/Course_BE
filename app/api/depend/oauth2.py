from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app import crud, model
from app.core.settings import settings
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.base import UserSystemRole
from app.constant.app_status import AppStatus


def create_token(data: dict, token_type: str):
    to_encode = data.copy()

    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN_DAYS)
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRES_IN_DAYS)
    to_encode.update({"token_type": token_type, "exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, token_type="access")


def create_refresh_token(data: dict):
    return create_token(data, token_type="refresh")


def verify_token(credentials: HTTPAuthorizationCredentials, db: Session):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AppStatus.ERROR_MISSING_TOKEN_ERROR.meta
        )

    try:
        decoded_token = jwt.decode(credentials.credentials,
                                   settings.JWT_SECRET_KEY,
                                   algorithms=settings.JWT_ALGORITHM)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AppStatus.ERROR_INVALID_TOKEN.meta
        )

    # check user existence
    uid = decoded_token['uid']
    user = crud.user.get(db=db, entry_id=uid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AppStatus.ERROR_USER_NOT_FOUND.meta
        )

    return decoded_token


def verify_access_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        db: Session = Depends(get_db),
):
    decoded_token = verify_token(credentials, db)
    if decoded_token['token_type'] != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AppStatus.ERROR_INVALID_TOKEN.meta
        )
    return decoded_token


def verify_refresh_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        db: Session = Depends(get_db),
):
    decoded_token = verify_token(credentials, db)
    if decoded_token['token_type'] != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AppStatus.ERROR_INVALID_TOKEN.meta
        )
    return decoded_token


def get_current_user(
        token: dict = Depends(verify_access_token),
        db: Session = Depends(get_db)
):
    user_id = token['uid']
    user = crud.user.get_user_by_id(db=db, user_id=user_id)
    return user


def get_current_active_user(
        current_user: model.User = Depends(get_current_user),
) -> model.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=AppStatus.ERROR_INACTIVE_USER.meta)

    return current_user


def user_manager(
        current_user: model.User = Depends(get_current_active_user)
) -> model.User:
    if current_user.system_role not in [UserSystemRole.MANAGER, UserSystemRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=AppStatus.ERROR_INVALID_ROLE.meta)

    return current_user


def admin(
        current_user: model.User = Depends(get_current_active_user)
) -> model.User:
    if not current_user.system_role == UserSystemRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=AppStatus.ERROR_INVALID_ROLE.meta)

    return current_user
