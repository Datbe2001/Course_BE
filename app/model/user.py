from sqlalchemy import (Boolean, Column, Date, String, text, JSON, Integer, func, TIMESTAMP)
from sqlalchemy.orm import relationship

from app.model.base import Base, UserSystemRole


class User(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), nullable=False)
    full_name = Column(String(42), nullable=True)
    avatar = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text("false"))
    hashed_password = Column(String(255), nullable=True)
    verify_code = Column(String(255), nullable=True)
    qr_code = Column(String(255), nullable=True)
    system_role = Column(String(255), nullable=False, default=UserSystemRole.MEMBER)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    comments = relationship("Comment", back_populates="user")
    courses = relationship("Course", back_populates="user")
    user_courses = relationship("UserCourse", back_populates="user")
    reply_comments = relationship("ReplyComment", back_populates="user")
