import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..schemas import ReplyComment, ReplyCommentCreateParams, ReplyCommentUpdateParams
from ..crud import crud_reply_comment, crud_comment


class ReplyCommentService:

    def __init__(self, db: Session):
        self.db = db

    async def get_reply_comment_by_id(self, reply_comment_id: str):
        current_reply_comment = crud_reply_comment.get_reply_comment_by_id(db=self.db,
                                                                           reply_comment_id=reply_comment_id)
        if current_reply_comment is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_NOT_FOUND)
        return current_reply_comment

    async def has_reply_comment_permission(self, user_id: str, reply_comment_id):
        current_reply_comment = crud_reply_comment.get_reply_comment_by_id(db=self.db,
                                                                           reply_comment_id=reply_comment_id)
        if current_reply_comment is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_NOT_FOUND)
        if current_reply_comment.user_id != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_METHOD_NOT_ALLOWED)
        return current_reply_comment

    async def create_reply_comment(self, user_id: str, reply_comment: ReplyCommentCreateParams):
        current_reply_comment = crud_comment.get_comment_by_id(db=self.db,
                                                               comment_id=reply_comment.comment_id)
        if current_reply_comment is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_NOT_FOUND)
        obj_in = ReplyComment(id=str(uuid.uuid4()), content=reply_comment.content, user_id=user_id,
                              comment_id=reply_comment.comment_id)

        result = crud_reply_comment.create(db=self.db, obj_in=obj_in)
        return result

    async def update_reply_comment(self, reply_comment_id: str, reply_comment: ReplyCommentUpdateParams):
        current_reply_comment = crud_reply_comment.get_reply_comment_by_id(db=self.db,
                                                                           reply_comment_id=reply_comment_id)
        result = crud_reply_comment.update(db=self.db, obj_in=reply_comment, db_obj=current_reply_comment)
        return result

    async def delete_reply_comment_by_id(self, reply_comment_id: str):
        result = crud_reply_comment.remove(db=self.db, entry_id=reply_comment_id)
        return result
