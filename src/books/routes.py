from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from ..books.schemas import BookCreateModel, BookResponseModel
from ..books.book_data import books


router = APIRouter()

@router.get("/",response_model=List[BookResponseModel], status_code=status.HTTP_200_OK)
async def get_books(limit: Optional[int]=2):
    try:
        if limit<1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit should be greater than 0")
        return books[:limit]
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit should be an integer")




@router.post("/",response_model=BookResponseModel,status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreateModel):
    new_book = book.dict()
    books.append(new_book)
    return new_book




@router.get("/{book_id}", response_model=BookResponseModel,status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.put("/{book_id}",response_model=BookResponseModel,status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: BookCreateModel):
    for b in books:
        if b["id"] == book_id:
            b["title"] = book.title
            b["author"] = book.author
            b["genre"] = book.genre
            b["published_year"] = book.published_year
            b["ISBN"] = book.ISBN
            b["no_of_copies"] = book.no_of_copies
            return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            books.remove(b)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")