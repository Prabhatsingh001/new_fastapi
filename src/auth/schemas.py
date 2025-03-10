from pydantic import BaseModel, Field
from datetime import datetime
import uuid

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