from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.books.routes import router as books_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting application")
    await init_db()
    yield
    print("server has been stopped")



version = "v1"
app = FastAPI(
    title="Books API",
    description="A simple API to manage books",
    version = version,
    lifespan=life_span
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["Books"])