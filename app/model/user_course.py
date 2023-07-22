from sqlalchemy import (Column, String, text, func, TIMESTAMP)
from sqlalchemy.orm import relationship

from app.model.base import Base

class UserCourse(Base):
    __tablename__ = "user_course"

    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), nullable=False)
    course_id = Column(String(255), nullable=False)
    course_role = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())
    
    # course = relationship("Course", back_populates="user_courses")
