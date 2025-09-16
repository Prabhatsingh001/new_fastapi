from fastapi import APIRouter, Depends, HTTPException,status, BackgroundTasks
from fastapi.responses import JSONResponse
from .schemas import (
    UserCreateModel, 
    UserModel, 
    UserLoginModel, 
    EmailModel, 
    PasswordResetRequestModel,
    PasswordResetConfirmModel
)
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import (
    create_access_token, 
    verify_password, 
    create_url_safe_token, 
    decode_url_safe_token,
    generate_password_hash,
)
from datetime import timedelta, datetime
from .dependencies import (
    RefreshTokenBearer, 
    AccessTokenBearer, 
    get_current_user, 
    RoleChecker
)
from src.db.redis import add_jti_blocklist
from src.errors import (
    UserAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    InvalidToken
)
from src.config import settings
from src.celery_tasks import send_email


REFRESH_TOKEN_EXPIRY = 2

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])



@auth_router.post('/send_mail')
async def send_mail(emails: EmailModel):
    emails = emails.addresses #type: ignore
    subject = "welcome to our app"
    html = "<h1>Welcome to the app</h1>"
    send_email.delay(emails, subject, html) #type: ignore
    return {"message":"email sent successfully"}



@auth_router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=UserModel)
async def create_user_Account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email
    user_exist = await user_service.user_exists(email, session)
    if user_exist:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email":email})
    link  = f"http://{settings.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
    <h1>verify your email</h1>
    <p> please click this <a href = "{link}">link</a> to verify your email</p>
    """
    emails = [email]
    subject = "verify your email"
    send_email.delay(emails, subject, html_message) #type: ignore
    return {
        "message": "Account created!! check email to verify your acount",
        "user": new_user
    }


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, 
    session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email,session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role' : user.role
                }
            )

            refresh_token = create_access_token(
                user_data = {
                    'email': user.email,
                    'user_uid': str(user.uid)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )

            return JSONResponse(
                content={
                    "message": "login successful",
                    "access token": access_token,
                    "refresh token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                },
                status_code=status.HTTP_200_OK
            )
        raise InvalidCredentials()
    raise UserNotFound()


@auth_router.get('verify/{token}')
async def verify_user_account(token: str, session:AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email') #type: ignore
    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {'is_verified':True}, session)
        return JSONResponse(
            content={
                "message":"Account verified successfully"
            },
            status_code=status.HTTP_200_OK
        )
    
    return JSONResponse(
        content={
            "message": "Error occured during verification"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR 
    )



@auth_router.get('/refresh_token')
async def get_new_acess_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data = token_details['user']
        )

        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    
    raise InvalidToken()


@auth_router.get('/me')
async def get_curr_user(
    user = Depends(get_current_user), 
    _:bool = Depends(role_checker)
):
    return user


@auth_router.get('/logout')
async def revoke_token(token_details:dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_blocklist(jti)
    return JSONResponse(
        content={
            "message": "logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post('/password-reset-request')
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email
    token = create_url_safe_token({"email":email})
    link  = f"http://{settings.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
    html_message = f"""
    <h1>Reset your password</h1>
    <p> please click this <a href = "{link}">link</a> to reset your password</p>
    """
    recipients=[email]
    subject="verify your email"
    send_email.delay(recipients, subject, html_message) #type: ignore
    return JSONResponse(
        content={
            "message": "password reset link send successfully"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.post('password-reset-confirm/{token}')
async def reset_account_password(token: str, passwords: PasswordResetConfirmModel, session:AsyncSession = Depends(get_session)):

    if passwords.new_password != passwords.confirm_new_password:
        raise HTTPException(
            detail="passwords do not match",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email') #type: ignore

    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        
        password_hash = generate_password_hash(passwords.new_password)
        await user_service.update_user(user, {'password_hash':password_hash}, session)

        return JSONResponse(
            content={
                "message":"password updated successfully"
            },
            status_code=status.HTTP_200_OK
        )
    
    return JSONResponse(
        content={
            "message": "Error occured during password updation"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR 
    )

