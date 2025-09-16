from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from src.books.schemas import Book
from typing import List
from src.reviews.schemas import ReviewModel

class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    first_name: str = Field(max_length=26)
    last_name: str = Field(max_length=26)
    email: str = Field(max_length=40)
    password: str = Field(min_length=8, max_length=20)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserBookModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserLoginModel(BaseModel):
    email: str
    password: str


class EmailModel(BaseModel):
    addresses: List[str]

class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str