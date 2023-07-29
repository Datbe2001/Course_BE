import uuid, smtplib
import logging
import string, secrets

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from app.core.settings import settings

from ..model import User
from ..schemas import UserCreate, UserCreateParams, UserUpdateParams, LoginUser, UserResponse, ChangePassword, UserBase
from ..crud.user import crud_user

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, user_id: str):
        current_user = crud_user.get_user_by_id(db=self.db,user_id=user_id)
        return UserResponse.from_orm(current_user)
    
    async def list_users(self, skip: int, limit: int):
        result = crud_user.list_users(db=self.db,skip=skip, limit=limit)
        return result


    async def create_user(self, create_user: UserCreateParams):

        email_lower = create_user.email.lower()
        username_lower = create_user.username.lower()
        current_email = crud_user.get_by_email(db=self.db,email=email_lower)
        if current_email:
            if current_email.hashed_password is None:
                update_user = UserBase(email=email_lower, username=username_lower)
                result = crud_user.update_user(db=self.db,current_user=current_email, update_user=update_user)
            else:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)
        
        else:
            result = crud_user.create_user(db=self.db, create_user=UserCreate(
                                                id=str(uuid.uuid4()),
                                                username=username_lower,
                                                email=email_lower))
        await self.get_verification_code(email=email_lower, action="is_active")
        return UserResponse.from_orm(result)
    

    async def get_verification_code(self, email: str, action: str):
        email_lower = email.lower()
        current_email = crud_user.get_by_email(db=self.db,email=email_lower)

        if not current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        email_from = settings.COURSE_EMAIl
        email_password = settings.COURSE_EMAIL_PASSWORD
        characters = string.ascii_letters + string.digits
        verify_code = ''.join(secrets.choice(characters) for _ in range(8))
        receiver_email = email

        if action == "forget_password":
            subject = "[FULL STACK] Verification code to change your password"
        elif action == "is_active":
            subject = "[FULL STACK] Verification code to user authentication"
            
        title = subject.replace("[FULL STACK]", "")
        html = """
        <html>
            <body>
                <h1>{}</h1>
                <p>Your verification code is <strong>{}</strong>. Please do not share it with anyone.</p>
            </body>
        </html>
        """.format(title, verify_code)

        try:
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(html, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
            server.quit()

            crud_user.update_verification_code(self.db, current_user=current_email, verify_code=verify_code)
        except Exception:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def login(self, login_request: LoginUser):
        email_lower = login_request.email.lower()
        current_user = crud_user.get_by_email(db=self.db, email=email_lower)

        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        
        if current_user.is_active == False:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INACTIVE_USER)
        
        if not hash_lib.verify_password(login_request.password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)
        
        return UserResponse.from_orm(current_user)
    

    async def update_profile(self, user_id: str, update_user: UserUpdateParams):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        result = crud_user.update_user(db=self.db, current_user=current_user, update_user=update_user)
        return UserResponse.from_orm(result)


    async def update_user_role(self, user_id: str, user_role: str):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        result = crud_user.update_user_role(self.db, current_user=current_user, user_role=user_role)
        return UserResponse.from_orm(result)
    
    async def verify_code(self, email: str,
                          verify_code: str,
                          new_password: str,
                          password_confirm: str):
        email_lower = email.lower()
        current_user = crud_user.get_by_email(db=self.db,email=email_lower)

        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        if not hash_lib.verify_code(verify_code, current_user.verify_code):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_VERIFY_CODE)

        if len(new_password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)
        elif new_password != password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONFIRM_PASSWORD_DOES_NOT_MATCH)

        result = crud_user.verify_code(self.db, current_user=current_user, new_password=new_password)
        return UserResponse.from_orm(result)


    async def change_password(self, current_user: dict, obj_in: ChangePassword):
        logger.info("Service_user: change_password called")

        if not hash_lib.verify_password(obj_in.old_password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INCORRECT)
        
        if len(obj_in.new_password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)

        if obj_in.new_password != obj_in.new_password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_WRONG)

        hashed_password = hash_lib.hash_password(obj_in.new_password)

        result = crud_user.change_password(db=self.db, current_user=current_user, new_password=hashed_password)
        logger.info("Service_user: change_password called successfully")
        return UserResponse.from_orm(result)
