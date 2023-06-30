import logging
import uuid

from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import User

from app.schemas.user import UserCreate, UserUpdate


logger = logging.getLogger(__name__)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        current_email = db.query(User).filter(User.email == email).first()
        return current_email

    def create_user(self, db: Session, create_user: UserCreate):
        current_user = User(**create_user.dict())
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user
    

crud_user = CRUDUser(User)
