from fastapi import APIRouter
from fastapi import Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object

from ...model import User
from ...services import NotificationService

router = APIRouter()


@router.get("/notifications/list")
async def list_notifications(unread: Optional[bool] = None,
                             page: Optional[int] = None,
                             limit: Optional[int] = None,
                             user: User = Depends(oauth2.get_current_user),
                             db: Session = Depends(get_db)):
    notification_service = NotificationService(db=db)
    notification_response = await notification_service.list_notifications(user_id=user.id, unread=unread, page=page,
                                                                          limit=limit)
    return make_response_object(notification_response)


@router.get("/notifications/{notification_id}/detail")
async def detail_notification(notification_id: str,
                              user: User = Depends(oauth2.get_current_user),
                              db: Session = Depends(get_db)):
    notification_service = NotificationService(db=db)
    notification_response = await notification_service.detail_notification(notification_id=notification_id)
    return make_response_object(notification_response)


@router.delete("/notifications/{notification_id}")
async def delete_notification(notification_id: str,
                              user: User = Depends(oauth2.get_current_user),
                              db: Session = Depends(get_db)):
    notification_service = NotificationService(db=db)
    notification_response = await notification_service.delete_notification(notification_id=notification_id)
    return make_response_object(notification_response)
