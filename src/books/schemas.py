from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    genre: str
    published_year: int
    ISBN: str
    no_of_copies: int
    created_at: datetime 
    updated_at: datetime 

class BookCreateModel(BaseModel):
    title: str
    author: str
    genre: str
    published_year: int
    ISBN: str
    no_of_copies: int

class BookUpdateModel(BaseModel):
    title: str
    author: str
    genre: str
    published_year: int
    no_of_copies: int