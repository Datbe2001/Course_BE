from enum import Enum
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class UserSystemRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    MEMBER = "MEMBER"


class CourseType(str, Enum):
    FREE = "FREE"
    PRO = "PRO"


class CourseRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class NotificationType(str, Enum):
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"
    COURSE_NOTIFICATION = "COURSE_NOTIFICATION"
    POST_NOTIFICATION = "POST_NOTIFICATION"
    COMMENT_NOTIFICATION = "COMMENT_NOTIFICATION"
