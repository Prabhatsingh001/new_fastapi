from pydantic import BaseModel


class BookCreateModel(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    published_year: int
    ISBN: str
    no_of_copies: int

class BookResponseModel(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    published_year: int

    class Config:
        from_attributes = True