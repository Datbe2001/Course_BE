import logging
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import Notification

from ..schemas import NotificationCreate, NotificationUpdate

logger = logging.getLogger(__name__)


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    @staticmethod
    def get_notification_by_id(db: Session, notification_id: str):
        current_notification = db.query(Notification).get(notification_id)
        return current_notification

    def list_notifications(self, db: Session, user_id: str, skip: int, limit: int):
        db_query = db.query(Notification).filter(Notification.user_id == user_id)
        total_notifications = db_query.count()
        list_notifications = db_query.orderby(desc(Notification.created_at)).offset(skip).limit(limit).all()
        return total_notifications, list_notifications


crud_notification = CRUDNotification(Notification)
