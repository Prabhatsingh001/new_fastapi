from fastapi import APIRouter,status, Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from .schemas import Book,BookUpdateModel,BookCreateModel,BookDetail
from typing import List
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import (
    BookNotFound
)
import uuid

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))


@router.get("/",
    response_model=List[Book],
    status_code=status.HTTP_200_OK, 
    dependencies=[role_checker]
)
async def get_all_books(
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    books = await book_service.get_all_books(session)
    return books



@router.get("/{book_id}", 
    response_model=BookDetail,
    status_code=status.HTTP_200_OK, 
    dependencies=[role_checker]
)
async def get_book_by_id(
    book_id: uuid.UUID, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise BookNotFound()



@router.post("/", 
    response_model=Book ,
    status_code=status.HTTP_201_CREATED, 
    dependencies=[role_checker]
)
async def create_book(
    book_data:BookCreateModel,
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    user_id = token_details['user']['user_uid']
    new_book = await book_service.create_book(book_data,user_id,session)
    return new_book



@router.patch("/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK, 
    dependencies=[role_checker]
)
async def update_book(
    book_id: uuid.UUID, 
    book: BookUpdateModel,
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    update_book = await book_service.update_book(book_id,book,session)
    if update_book:
        return update_book
    else:
        raise BookNotFound()



@router.delete("/{book_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
    dependencies=[role_checker]
)
async def delete_book(
    book_id: uuid.UUID, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    book = await book_service.delete_book(book_id, session)
    if book is None:
        raise BookNotFound()
    else:
        return {}
    

@router.get("/user/{user_uid}",
    response_model=List[Book],
    status_code=status.HTTP_200_OK, 
    dependencies=[role_checker]
)
async def get_user_book_submission(user_uid: uuid.UUID, 
    session:AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    books = await book_service.get_user_books(user_uid, session)
    return books