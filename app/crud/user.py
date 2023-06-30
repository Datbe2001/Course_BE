import logging
import uuid

from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import User

from app.schemas.user import UserCreate, UserUpdate, UserResponse


logger = logging.getLogger(__name__)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        current_email = db.query(User).filter(User.email == email).first()
        return current_email

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        current_user = db.query(User).filter(User.id == user_id).first()
        return current_user
    
    @staticmethod
    def list_users(db: Session, skip: int, limit: int) -> Optional[User]:
        total_users = db.query(User).count()
        list_users = db.query(User).offset(skip).limit(limit).all()

        result = {
            "total_users": total_users,
            "list_users": list_users
        }
        return result

    def create_user(self, db: Session, create_user: UserCreate):
        current_user = User(**create_user.dict())
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user
    
    def update_user(self, db: Session, current_user: str, update_user: UserUpdate):
        result = super().update(db, obj_in=update_user, db_obj=current_user)
        return result
    
    def update_user_role(self, db: Session, current_user: str, user_role: str):
        logger.info("CRUDUser: update_user_role called.")
        current_user.system_role = user_role
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: update_user_role called successfully.")
        return current_user
    

crud_user = CRUDUser(User)
