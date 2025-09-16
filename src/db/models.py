from sqlmodel import SQLModel,Field,Column,Relationship
from sqlalchemy.dialects import postgresql as pq
from datetime import datetime
from typing import List,Optional
import uuid



class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class User(SQLModel, table=True):
    __tablename__ = "users"  #type: ignore

    uid: uuid.UUID = Field(
        sa_column=Column(
            pq.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
        )
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(
        pq.VARCHAR, nullable=False, server_default="user"
    ))
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    is_active: bool = Field(default=True)
    books: List["Books"] = Relationship(
        back_populates="user", 
        sa_relationship_kwargs={'lazy': "selectin"}
    )
    reviews: List["Reviews"] = Relationship(
        back_populates="user", 
        sa_relationship_kwargs={'lazy': "selectin"}
    )


    def __repr__(self):
        return f"<User {self.username}>"
    


class Books(SQLModel, table=True):
    __tablename__ = "books" #type: ignore

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
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    
    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(
        back_populates="books", 
        sa_relationship_kwargs={'lazy': "selectin"}
    )
    tags: List["Tag"] = Relationship(
        back_populates="books",
        link_model=BookTag,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Book {self.title}>"
    

class Reviews(SQLModel, table=True):
    __tablename__ = "reviews" #type: ignore

    uid: uuid.UUID = Field(
        sa_column=Column(
            pq.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(back_populates="reviews")
    books: Optional[Books] = Relationship(back_populates="reviews")


    def __repr__(self):
        return f"<review for {self.book_uid} by user {self.user_uid}>"


class Tag(SQLModel, table=True):
    __tablename__ = "tags" #type: ignore
    uid: uuid.UUID = Field(
        sa_column=Column(pq.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pq.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pq.TIMESTAMP, default=datetime.now))
    books: List["Books"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
