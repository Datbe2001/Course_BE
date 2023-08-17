from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object
from app.schemas.reply_comment import ReplyCommentCreateParams, ReplyCommentUpdateParams

from ...model import User

from ...services import ReplyCommentService

router = APIRouter()


@router.get("/reply_comments/{reply_comment_id}")
async def get_reply_comment_by_id(reply_comment_id: str,
                                  user: User = Depends(oauth2.get_current_user),
                                  db: Session = Depends(get_db)):
    reply_comment_service = ReplyCommentService(db=db)
    reply_comment_response = await reply_comment_service.get_reply_comment_by_id(reply_comment_id=reply_comment_id)
    return make_response_object(reply_comment_response)


@router.post("/reply_comments/")
async def create_reply_comment(reply_comment: ReplyCommentCreateParams,
                               user: User = Depends(oauth2.get_current_user),
                               db: Session = Depends(get_db)):
    reply_comment_service = ReplyCommentService(db=db)
    reply_comment_response = await reply_comment_service.create_reply_comment(user_id=user.id,
                                                                              reply_comment=reply_comment)
    return make_response_object(reply_comment_response)


@router.put("/reply_comments/")
async def update_reply_comment_by_id(reply_comment_id: str, reply_comment: ReplyCommentUpdateParams,
                                     user: User = Depends(oauth2.get_current_user),
                                     db: Session = Depends(get_db)):
    reply_comment_service = ReplyCommentService(db=db)
    await reply_comment_service.has_reply_comment_permission(user_id=user.id, reply_comment_id=reply_comment_id)
    reply_comment_response = await reply_comment_service.update_reply_comment(reply_comment_id=reply_comment_id,
                                                                              reply_comment=reply_comment)
    return make_response_object(reply_comment_response)


@router.delete("/reply_comments/")
async def delete_reply_comment_by_id(reply_comment_id: str,
                                     user: User = Depends(oauth2.get_current_user),
                                     db: Session = Depends(get_db)):
    reply_comment_service = ReplyCommentService(db=db)
    await reply_comment_service.has_reply_comment_permission(user_id=user.id, reply_comment_id=reply_comment_id)
    reply_comment_response = await reply_comment_service.delete_reply_comment_by_id(reply_comment_id=reply_comment_id)
    return make_response_object(reply_comment_response)
