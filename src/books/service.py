from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookUpdateModel,BookCreateModel
from sqlmodel import select,desc
from src.db.models import Books
import uuid

class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Books).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        return result.all()

    
    
    async def get_book(self, book_uuid:uuid.UUID, session:AsyncSession):
        statement = select(Books).where(Books.uid == book_uuid)
        result = await session.exec(statement)
        book =  result.first()
        return book if book is not None else None

    
    
    async def create_book(self, book_data:BookCreateModel ,user_uid:uuid.UUID , session:AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Books(
            **book_data_dict
        )

        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        return new_book

    
    
    async def update_book(self,book_uid: uuid.UUID, update_data:BookUpdateModel, session:AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k,v in update_data_dict.items():
                setattr(book_to_update,k,v)
            await session.commit()
            return book_to_update
        else:
            return None

    
    
    
    async def delete_book(self, book_uid:uuid.UUID, session:AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete
        else:
            return None
        

    async def get_user_books(self, user_id: uuid.UUID, session:AsyncSession):
        statement = select(Books).where(Books.user_uid == user_id).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        return result.all()