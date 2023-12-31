from sqlalchemy import (Boolean, Column, Date, String, text, func, ForeignKey, TIMESTAMP)
from sqlalchemy.orm import relationship

from app.model.base import Base


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(String(255), primary_key=True)
    name = Column(String(42), nullable=False)
    description = Column(String(255), nullable=True)
    video_id = Column(String(255), nullable=False)
    video_url = Column(String(255), nullable=False)
    course_id = Column(String(255), ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # Relationship
    comments = relationship("Comment", back_populates="lesson", passive_deletes=True)
    course = relationship("Course", back_populates="lessons")
