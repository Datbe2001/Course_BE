from sqlalchemy import (Boolean, Column, String, text, func, ForeignKey, TIMESTAMP, JSON)
from sqlalchemy.orm import relationship

from app.model.base import Base


class Notification(Base):
    __tablename__ = "notification"

    id = Column(String(255), primary_key=True)
    data = Column(JSON(), nullable=False)
    unread = Column(Boolean, default=True)
    notification_type = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # Relationship
    user = relationship("User", back_populates="notifications")
