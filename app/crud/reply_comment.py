import logging

from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import ReplyComment

from ..schemas import ReplyCommentCreate, ReplyCommentUpdate

logger = logging.getLogger(__name__)


class CRUDReplyComment(CRUDBase[ReplyComment, ReplyCommentCreate, ReplyCommentUpdate]):

    @staticmethod
    def get_reply_comment_by_id(db: Session, reply_comment_id: str):
        current_reply_comment = db.query(ReplyComment).get(reply_comment_id)
        return current_reply_comment


crud_reply_comment = CRUDReplyComment(ReplyComment)
