from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from .schemas import UserCreateModel, UserModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router = APIRouter()
user_service = UserService()

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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User already exists")
    
    new_user = await user_service.create_user(user_data, session)
    return new_user
