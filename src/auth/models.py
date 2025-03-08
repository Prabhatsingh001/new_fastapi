from sqlmodel import SQLModel,Field,Column
from sqlalchemy.dialects import postgresql as pq
from datetime import datetime
import uuid


"""
class user:
    uid: uuid.UUID
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime
"""
class User(SQLModel, table=True):
    __tablename__ = "users"

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