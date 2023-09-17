import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.orm.attributes import flag_modified

from .base import CRUDBase
from ..model import Notification

from ..schemas import NotificationCreate, NotificationUpdate

logger = logging.getLogger(__name__)


class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    @staticmethod
    def detail_notification(db: Session, notifications_id: str) -> Notification:
        db_query = db.query(Notification).get(notifications_id)
        return db_query

    def list_notifications(self, db: Session, user_id: str, unread: bool, skip: int = None, limit: int = None):
        db_query = db.query(Notification).filter(Notification.user_id == user_id)
        if unread is not None:
            db_query = db_query.filter(Notification.unread == unread)

        db_query = db_query.order_by(desc(Notification.created_at))

        total_notifications = db_query.count()
        if skip is not None and limit is not None:
            list_notifications = db_query.offset(skip).limit(limit).all()
        else:
            list_notifications = db_query.all()
        return total_notifications, list_notifications

    def list_notifications_unread(self, db: Session, user_id: str, skip: int = None, limit: int = None):
        db_query = db.query(Notification).filter(Notification.user_id == user_id, Notification.unread == True).order_by(
            desc(Notification.created_at))
        total_notifications = db_query.count()
        if skip is not None and limit is not None:
            list_notifications = db_query.offset(skip).limit(limit).all()
        else:
            list_notifications = db_query.all()
        return total_notifications, list_notifications

    def mark_notification_as_read(self, db: Session, current_notification: Notification, unread: bool):
        notification_data = current_notification.data
        notification_data.get("data").update(
            dict(created_at=current_notification.created_at.timestamp() * 1000, unread=current_notification.unread,
                 notification_id=current_notification.id))
        current_notification.unread = unread
        current_notification.data = notification_data
        flag_modified(current_notification, "data")
        db.commit()
        db.refresh(current_notification)
        return current_notification

    def create_multi_notification(self, db: Session, list_request_data: list):
        notification_objects = db.bulk_insert_mappings(Notification, [item.dict() for item in list_request_data])
        db.commit()
        return notification_objects



crud_notification = CRUDNotification(Notification)
