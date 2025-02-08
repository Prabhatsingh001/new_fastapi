from sqlmodel import SQLModel,Field,Column
import sqlalchemy.dialects.postgresql as pq
from datetime import datetime
import uuid


class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pq.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    genre: str
    published_year: int
    ISBN: str
    no_of_copies: int
    created_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))


    def __repr__(self):
        return f"<Book {self.title}>"