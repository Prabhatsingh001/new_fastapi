from fastapi import APIRouter, HTTPException, status, Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from .schemas import Book,BookUpdateModel

router = APIRouter()
book_service = BookService()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data:Book,session:AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book_data,session)
    return new_book


@router.get("/{book_id}", response_model=Book,status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int, session:AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.put("/{book_id}",response_model=Book,status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: BookUpdateModel,session:AsyncSession = Depends(get_session)):
    update_book = await book_service.update_book(book_id,book,session)
    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, session:AsyncSession = Depends(get_session)):
    book = await book_service.delete_book(book_id, session)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return