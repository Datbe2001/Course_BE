from enum import Enum


class NotificationTemplate(Enum):
    CRUD_COURSE_NOTIFICATION_MSG = lambda course_type, course_name, action, user_name: f"The {course_name} {course_type} has just been {action} by {user_name} <span style=\"background: linear-gradient(to right, #7AF4AE 0%, #3262DD 100%);-webkit-background-clip: text; background-clip: text; color: transparent; font-weight: bold;\"></span>"
