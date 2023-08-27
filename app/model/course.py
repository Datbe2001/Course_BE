from sqlalchemy import (Boolean, Column, Date, String, text, func, ForeignKey, TIMESTAMP)
from sqlalchemy.orm import relationship

from app.model.base import Base


class Course(Base):
    __tablename__ = "course"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False)
    banner = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    course_type = Column(String(255), nullable=False)
    KEY = Column(String(255), nullable=False)
    created_by = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # Relationship
    user = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course", passive_deletes=True)
    user_course = relationship("UserCourse", back_populates="courses", passive_deletes=True)
