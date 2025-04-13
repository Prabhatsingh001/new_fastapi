from fastapi import APIRouter, Depends, HTTPException,status, dependencies
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBookModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_blocklist
from src.errors import (
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermission,
    InvalidCredentials,
    InvalidToken
)


REFRESH_TOKEN_EXPIRY = 2

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])


@auth_router.post(
        "/signup",
        status_code=status.HTTP_201_CREATED,
        response_model=UserModel
)
async def create_user(
        user_data: UserCreateModel,
        session: AsyncSession = Depends(get_session)):
    
    email = user_data.email
    user_exist = await user_service.user_exists(email, session)
    if user_exist:
        raise UserAlreadyExists()
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(
    user_data: UserLoginModel, 
    session: AsyncSession = Depends(get_session)
):
    
    login_email = user_data.email
    login_password = user_data.password

    user = await user_service.get_user_by_email(login_email,session)

    if user is not None:
        password_valid = verify_password(login_password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                data = {
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role' : user.role
                }
            )

            refresh_token = create_access_token(
                data = {
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


@auth_router.get('/me', response_model=UserBookModel)
async def get_curr_user(user = Depends(get_current_user), _:bool = Depends(role_checker)):
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
