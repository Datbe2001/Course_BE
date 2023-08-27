import logging

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from .base import CRUDBase
from ..model import Comment, ReplyComment

from ..schemas import CommentCreate, CommentUpdate

logger = logging.getLogger(__name__)


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):

    @staticmethod
    def get_comment_by_id(db: Session, comment_id: str):
        current_comment = db.query(Comment).get(comment_id)
        return current_comment
    
    @staticmethod
    def get_comment_by_user(db: Session, user_id: str, comment_id: str):
        current_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
        return current_comment

    @staticmethod
    def list_comment(db: Session, lesson_id: str, skip: int, limit: int):
        db_query = db.query(Comment).filter(Comment.lesson_id == lesson_id).options(
            joinedload(Comment.user),
            joinedload(Comment.reply_comments).joinedload(ReplyComment.user))
        total_comment = db_query.count()
        list_comment = db_query.order_by(desc(Comment.created_at)).offset(skip).limit(limit).all()
        return total_comment, list_comment


crud_comment = CRUDComment(Comment)
