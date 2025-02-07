from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.books.routes import router as books_router

version = "v1"
app = FastAPI(
    title="Books API",
    description="A simple API to manage books",
    version = version
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["Books"])