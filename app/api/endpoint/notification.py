from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object

from ...model import User
from ...services import NotificationService

router = APIRouter()


@router.get("/notifications/list")
async def list_notifications(user: User = Depends(oauth2.get_current_user),
                             db: Session = Depends(get_db),
                             skip=0,
                             limit=10):
    notification_service = NotificationService(db=db)
    notification_response = await notification_service.list_notifications(user_id=user.id, skip=skip, limit=limit)
    return make_response_object(notification_response)
