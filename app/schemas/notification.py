from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    data: dict
    user_id: Optional[str] = None
    notification_type: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass
