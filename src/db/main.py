from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(
    create_engine(
        url = settings.DATABASE_URL,
        echo = True
    )
)

# async def init_db():
#     async with engine.begin() as conn:
#         from src.db.models import Books 
#         await conn.run_sync(SQLModel.metadata.create_all)



async def get_session():
    Session = sessionmaker( #type: ignore
        bind = engine,       #type: ignore
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session: #type: ignore
        yield session