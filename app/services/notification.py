import uuid

from sqlalchemy.orm import Session


from ..crud import crud_notification
from ..model.base import NotificationType


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def list_notifications(self, user_id: str, skip: int, limit: int):
        total_notifications, list_notifications = crud_notification.list_notifications(db=self.db, user_id=user_id,
                                                                                       skip=skip, limit=limit)
        result = dict(total_notifications=total_notifications, list_notifications=list_notifications)
        return result
