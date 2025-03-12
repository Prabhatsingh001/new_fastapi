from fastapi import APIRouter, HTTPException, status, Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from .schemas import Book,BookUpdateModel,BookCreateModel
from typing import List
from src.auth.dependencies import AcessTokenBearer

router = APIRouter()
book_service = BookService()
access_token_bearer = AcessTokenBearer()

@router.get("/",response_model=List[Book],status_code=status.HTTP_200_OK)
async def get_all_books(session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books


@router.get("/{book_id}", response_model=Book,status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: str, session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



@router.post("/", response_model=Book ,status_code=status.HTTP_201_CREATED)
async def create_book(book_data:BookCreateModel,session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    new_book = await book_service.create_book(book_data,session)
    return new_book



@router.patch("/{book_id}",response_model=Book,status_code=status.HTTP_200_OK)
async def update_book(book_id: str, book: BookUpdateModel,session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    update_book = await book_service.update_book(book_id,book,session)
    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, session:AsyncSession = Depends(get_session), user_detail = Depends(access_token_bearer)):
    book = await book_service.delete_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return {}